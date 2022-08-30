import mplfinance as mpf
from get_data import get_klines 
import pandas_ta as ta
from vwap import vwapChart


vwaplist = [48,200]


df = get_klines('BTCUSDT', '1m', '30 minutes ago')


###################################################################################


x = vwapChart(df, vwaplist)



vwap = mpf.make_addplot(x,type='line')


###################################################################################
title = 'name of symbol'

mpf.plot(df,type='candle',title=title,style='yahoo',addplot = vwap)


