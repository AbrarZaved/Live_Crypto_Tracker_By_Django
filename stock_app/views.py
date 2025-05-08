from threading import Thread
from django.http import HttpResponse
from django.shortcuts import render
import time
import queue
from LiveStockTracker.settings import BASE_DIR
from django.http import JsonResponse
import environ
import os
import finnhub
from django.core.cache import cache

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)


def crypto_home(request):
    return render(request, "stock_app/crypto_home.html")  # No symbols here


def get_crypto_symbols(request):
    start = time.time()
    symbols = cache.get("binance_crypto_symbols")
    if not symbols:
        finnhub_client = finnhub.Client(api_key=env("API_KEY"))
        crypto_picker = finnhub_client.crypto_symbols("BINANCE")
        symbols = [item["symbol"] for item in crypto_picker]
        top_crypto_symbols = [
            "BINANCE:BTCUSDT",
            "BINANCE:ETHUSDT",
            "BINANCE:BNBUSDT",
            "BINANCE:SOLUSDT",
            "BINANCE:XRPUSDT",
            "BINANCE:ADAUSDT",
            "BINANCE:DOGEUSDT",
            "BINANCE:AVAXUSDT",
            "BINANCE:DOTUSDT",
            "BINANCE:TRXUSDT",
            "BINANCE:MATICUSDT",
            "BINANCE:SHIBUSDT",
            "BINANCE:LTCUSDT",
            "BINANCE:LINKUSDT",
            "BINANCE:ATOMUSDT",
            "BINANCE:XLMUSDT",
            "BINANCE:ETCUSDT",
            "BINANCE:FILUSDT",
            "BINANCE:NEARUSDT",
            "BINANCE:ICPUSDT",
            "BINANCE:APTUSDT",
            "BINANCE:SANDUSDT",
            "BINANCE:AAVEUSDT",
            "BINANCE:EGLDUSDT",
            "BINANCE:VETUSDT",
        ]  # your static curated list
        symbols = [s for s in symbols if s in top_crypto_symbols]
        cache.set("binance_crypto_symbols", symbols, timeout=1800)
    end = time.time()
    return JsonResponse({"symbols": symbols, "load_time": end - start})


def fetch_stock_info(ticker, q):
    try:
        finnhub_client = finnhub.Client(api_key=env("API_KEY"))
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


def crypto_quotes(request):
    symbol_picker = request.POST.getlist("symbols")
    stock_data = {}
    start = time.time()
    q = queue.Queue()
    threads = []

    for ticker in symbol_picker:
        thread = Thread(target=fetch_stock_info, args=(ticker, q))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    while not q.empty():
        stock_data.update(q.get())

    end = time.time()
    print(f"Time taken: {end - start}")

    return render(request, "stock_app/crypto_quotes.html", {"stock_data": stock_data})
