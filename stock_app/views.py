from threading import Thread
from django.http import HttpResponse
from django.shortcuts import render
import time
import queue
import yfinance as yf
from yahoo_fin.stock_info import *


def stockPage(request):
    stock_picker = tickers_nifty50()
    return render(request, "stock_app/stockPage.html", {"stock_picker": stock_picker})


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
    stockpicker = request.POST.getlist("stockpicker")
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
