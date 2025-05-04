import requests
import finnhub

finnhub_client = finnhub.Client(api_key="d0bfkj1r01qo0h63hsjgd0bfkj1r01qo0h63hsk0")
data=finnhub_client.crypto_symbols("BINANCE")
symbols = [item['symbol'] for item in data]
print(symbols)