import asyncio
import queue
from threading import Thread
import time


from celery import shared_task
import finnhub
import os
from channels.layers import get_channel_layer


def fetch_stock_info(ticker, q):
    try:
        finnhub_client = finnhub.Client(api_key=os.getenv("API_KEY"))
        info = finnhub_client.quote(ticker)

        q.put(
            {
                ticker: {
                    "s": ticker[8:],  # Symbol
                    "c": info.get("c"),  # Current price
                    "d": info.get("d"),  # Change
                    "dp": info.get("dp"),  # Percent change
                    "h": info.get("h"),  # High price of the day
                    "l": info.get("l"),  # Low price of the day
                    "o": info.get("o"),  # Open price of the day
                    "pc": info.get("pc"),  # Previous close price
                    "t": int(time.time()),  # Timestamp
                }
            }
        )
    except Exception as e:
        print(f"Failed to fetch {ticker}: {e}")
        q.put({ticker: {"error": str(e)}})


@shared_task(bind=True)
def crypto_quotes(self, symbols):
    stock_data = {}
    q = queue.Queue()
    threads = []
    for ticker in symbols:
        thread = Thread(target=fetch_stock_info, args=(ticker, q))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not q.empty():
        stock_data.update(q.get())

    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for symbol in symbols:
        group_name = f"symbol_{symbol.replace(':', '_')}"
        loop.run_until_complete(
            channel_layer.group_send(
                group_name,
                {
                    "type": "send_crypto_update",
                    "message": stock_data,
                },
            )
        )

    loop.close()
    return stock_data
