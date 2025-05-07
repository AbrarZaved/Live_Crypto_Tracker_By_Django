import json
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from channels.generic.websocket import AsyncWebsocketConsumer


class CryptoConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self, crypto_symbol):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        if task.exists():
            task = task.first()
            args = json.loads(task.args)
            if isinstance(args[0], list):  # task.args is [[...]]
                current_symbols = args[0]
            else:
                current_symbols = args

            if crypto_symbol not in current_symbols:
                current_symbols.append(crypto_symbol)
                task.args = json.dumps([current_symbols])
                task.save()
        else:
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=10, period=IntervalSchedule.SECONDS
            )
            task = PeriodicTask.objects.create(
                interval=schedule,
                name="every-10-seconds",
                task="stock_app.tasks.crypto_quotes",
                args=json.dumps([[crypto_symbol]]),  # Wrapped in outer list
            )
            task.save()

    async def connect(self):
        self.symbol = self.scope["url_route"]["kwargs"]["symbol"]
        safe_symbol = self.symbol.replace(":", "_")
        self.room_group_name = f"symbol_{safe_symbol}"
        print(f"Connecting to {self.room_group_name}")
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.addToCeleryBeat(self.symbol)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "crypto_update", "message": message}
        )

    # Receive message from room group

    async def send_crypto_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))
