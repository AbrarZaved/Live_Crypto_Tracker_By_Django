from threading import Thread
from django.http import HttpResponse
from django.shortcuts import render
import time
import queue
from LiveStockTracker.settings import BASE_DIR
import yfinance as yf
from yahoo_fin.stock_info import *
import environ
import os
import finnhub

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)


def stockPage(request):
    finnhub_client = finnhub.Client(api_key=env("API_KEY"))
    crypto_picker = finnhub_client.crypto_symbols("BINANCE")
    symbols = [item["symbol"] for item in crypto_picker][:50]
    return render(request, "stock_app/stockPage.html", {"symbols": symbols})


def fetch_stock_info(ticker, q):
    try:
        info = yf.Ticker(ticker).info
        current = info.get("currentPrice")
        previous = info.get("previousClose")
        change = (
            current - previous if current is not None and previous is not None else None
        )

        q.put(
            {
                ticker: {
                    "symbol": info.get("symbol"),
                    "currentPrice": current,
                    "dayHigh": info.get("dayHigh"),
                    "dayLow": info.get("dayLow"),
                    "previousClose": previous,
                    "marketCap": info.get("marketCap"),
                    "volume": info.get("volume"),
                    "sector": info.get("sector"),
                    "change": round(change, 2) if change is not None else "N/A",
                }
            }
        )
    except Exception as e:
        print(f"Failed to fetch {ticker}: {e}")
        q.put({ticker: {"error": str(e)}})


def stockTracker(request):
    stockpicker = request.POST.getlist("symbol")
    stock_data = {}
    start = time.time()
    q = queue.Queue()
    threads = []

    for ticker in stockpicker:
        thread = Thread(target=fetch_stock_info, args=(ticker, q))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not q.empty():
        stock_data.update(q.get())

    end = time.time()
    print(f"Time taken: {end - start}")

    return render(request, "stock_app/stockTracker.html", {"stock_data": stock_data})
