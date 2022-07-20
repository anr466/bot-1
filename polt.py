from get_data import get_klines
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import pandas_ta as ta
from datetime import date
plt.style.use('fivethirtyeight')
yf.pdr_override()

data = get_klines("BTCUSDT", "30m", "1500 hours ago UTC+3")



data['SMA 30'] = ta.sma(data['Close'],30)
data['SMA 100'] = ta.sma(data['Close'],100)



#SMA BUY SELL
def buy_sell(data):
    signalBuy = []
    signalSell = []
    position = False 
    try:
        for i in data:
            if data['SMA 30'][i] > data['SMA 100'][i]:
                if position == False :
                    signalBuy.append(data['Adj Close'][i])
                    signalSell.append(np.nan)
                    position = True
                else:
                    signalBuy.append(np.nan)
                    signalSell.append(np.nan)
            elif data['SMA 30'][i] < data['SMA 100'][i]:
                if position == True:
                    signalBuy.append(np.nan)
                    signalSell.append(data['Adj Close'][i])
                    position = False
                else:
                    signalBuy.append(np.nan)
                    signalSell.append(np.nan)
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
    except:
        pass
    return pd.Series([signalBuy, signalSell])



print(buy_sell(data))
