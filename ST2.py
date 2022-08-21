import mplfinance as mpf
from get_data import get_klines 
import pandas_ta as ta




df = get_klines('TLMBUSD', '1m', '50 minutes ago')
df.index.name = 'Date'
df.shape
df.head(2)
df.tail(2)
###################################################################################
def vwap(df , period):
    kline = df
    # calaculate average price for high , low , close
    kline['tp'] = ta.hlc3(high= kline['High'] , low= kline['Low'] ,close=kline['Close'])
    kline['tpV'] = kline['tp'] * kline['Volume']
    #using moving average
    kline['mtpv'] = ta.sma(kline['tpV'] , length = period)
    kline['mV'] = ta.sma(kline['Volume'] , length = period)
    # calaulate vwap
    kline['vwap'] = kline['mtpv'] /  kline['mV']
    vwap = kline['vwap']
    columns = kline.columns

    for i in range(6 , len(columns)):
        del kline[columns[i]]


    return vwap

# vwap calculator
vwap_48 = vwap(df , 20)
vwap_84 = vwap(df , 60)
df['vwap48'] = vwap_48
df['vwap84'] = vwap_84
df['buy'] =ta.cross(df['vwap48'] , df['vwap84'])
df['sell']=ta.cross(df['vwap84'] , df['vwap48'])
crosss_buy= df["buy"]>0.0
crosss_sell =df["sell"]>0.0
df['crosss_buy'] = crosss_buy
df['crosss_sell'] = crosss_sell


vwap = mpf.make_addplot(df['vwap48'])
vwap1 = mpf.make_addplot(df['vwap84'])
x = vwap,vwap1
###################################################################################
title = 'name of symbol'
kwargs = dict(type='candle',volume=True,figratio=(11,8),figscale=0.85)
mpf.plot(df,**kwargs,title=title,style='yahoo',addplot=x)


