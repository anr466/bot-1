from Bclient import Clnt
import pandas as pd
import requests


def get_all_24hours_pct(top):
    tickers_pc = []
    tickers = []
    prices = Clnt.get_ticker()
    for ticker in prices:
        if 'USDT' in ticker['symbol'] and ticker['symbol']   :
            pairs = {'Symbol':ticker['symbol'] , 'pct' :float(ticker['priceChangePercent']) }
            tickers_pc.append(pairs)
    tickers_pc = sorted(tickers_pc, key=lambda x : x['pct'], reverse=True)
    tickers_pc = tickers_pc[:top]
    for ticker in tickers_pc :
        tickers.append(ticker['Symbol'])
    return tickers
# run  ==============
top_10 = get_all_24hours_pct(10)

# print(top_10)