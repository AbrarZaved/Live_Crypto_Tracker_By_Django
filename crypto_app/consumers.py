import copy
import datetime
import json
from asgiref.sync import sync_to_async
from django.utils import crypto
from prompt_toolkit import keys
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from channels.generic.websocket import AsyncWebsocketConsumer
from crypto_app.models import Crypto


class CryptoConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self, crypto_symbol):
        task_qs = PeriodicTask.objects.filter(name="every-10-seconds")
        if task_qs.exists():
            task = task_qs.first()  # FIXED: get the instance
            args = json.loads(task.args or "[]")

            # args = [[symbol1, symbol2, ...]]
            if args and isinstance(args[0], list):
                current_symbols = args[0]
            else:
                current_symbols = args

            if crypto_symbol not in current_symbols:
                current_symbols.append(crypto_symbol)
                task.args = json.dumps([current_symbols])  # maintain structure
                task.save()
        else:
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=5, period=IntervalSchedule.SECONDS
            )
            task = PeriodicTask.objects.create(
                interval=schedule,
                name="every-10-seconds",
                task="crypto_app.tasks.crypto_quotes",
                args=json.dumps([[crypto_symbol]]),  # Note: wrapped in another list
            )

    @sync_to_async
    def add_to_crypto_list(self, crypto_symbol):
        user = self.scope["user"]
        print(crypto_symbol)
        crypto, created = Crypto.objects.get_or_create(symbol=crypto_symbol)
        if created:
            crypto.user.add(user)
            crypto.save()

    async def connect(self):
        self.symbol = self.scope["url_route"]["kwargs"]["symbol"]
        safe_symbol = self.symbol.replace(":", "_")
        self.room_group_name = f"symbol_{safe_symbol}"
        print(f"Connecting to {self.room_group_name}")
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.addToCeleryBeat(self.symbol)
        await self.add_to_crypto_list(self.symbol)
        await self.accept()

    @sync_to_async
    def helper_function(self):
        user = self.scope["user"]
        user_crypto = Crypto.objects.filter(user=user)

        task = PeriodicTask.objects.get(name="every-10-seconds")
        args = json.loads(task.args or "[]")
        symbols = args[0] if args and isinstance(args[0], list) else []
        # Remove user's symbols
        for crypto in user_crypto:
            symbol = crypto.symbol
            crypto.user.remove(user)
            if crypto.user.count() == 0:
                crypto.delete()
            if symbol in symbols:
                symbols.remove(symbol)

        task.args = json.dumps([symbols])
        task.save()

    async def disconnect(self, close_code):
        await self.helper_function()
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_crypto_update", "message": message}
        )

    @sync_to_async
    def select_user_crypto(self):
        user = self.scope["user"]
        user_crypto = user.crypto_user.values_list("symbol", flat=True)
        return list(user_crypto)

    # Receive message from room group

    async def send_crypto_update(self, event):
        print("WS send_crypto_update triggered at", datetime.datetime.now())

        message = event["message"]
        message = copy.copy(message)
        user_crypto = await self.select_user_crypto()
        keys = message.keys()
        for key in list(keys):
            if key not in user_crypto:
                del message[key]

        print("WS sending to client at", datetime.datetime.now())
        await self.send(text_data=json.dumps(message))
