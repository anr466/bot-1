import mplfinance as mpf
from get_data import get_klines 
import pandas_ta as ta
import numpy as np 


# vwaplist = [48,200]

title = 'ADAUSDT'



df = get_klines(title, '1m', '1 hour ago')

###################################################################################
# chart


a = df['10_EMA'] = df['Close'].ewm(span = 4, adjust = False).mean()
x = df['20_EMA'] = df['Close'].ewm(span = 50, adjust = False).mean()
y = df['50_EMA'] = df['Close'].ewm(span = 700, adjust = False).mean()

buy = []
sell = []

for i in df.index:

    df['buy'] = np.where(df['10_EMA'] > df['50_EMA'] ,1,np.nan)* 1 * df['Low']


    if df['buy'] is not np.nan:

        buysignal = buy.append(df.iloc[-1]['buy'])

    df['sell'] = np.where(df['10_EMA'] < df['50_EMA'] ,1,np.nan)* 1 * df['Low']

    if df['sell'] is not np.nan:

        sellsignal = sell.append(df.iloc[-1]['sell'])






# print(sell)

vwap = [mpf.make_addplot(x,type='line'),mpf.make_addplot(y,type='line'),mpf.make_addplot(a,type='line'),mpf.make_addplot(buy, scatter=True, markersize=100, marker=r'$\Uparrow$', color='green'),mpf.make_addplot(sell, scatter=True, markersize=100, marker=r'$\Uparrow$', color='red')]

mpf.plot(df,type='candle',title=title,style='yahoo',addplot = vwap , volume=True)
###################################################################################
# code 


