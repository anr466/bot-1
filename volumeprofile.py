

from get_data import get_klines
import talib as ta

ticker = 'BTCUSDT'
interval = '1m'


df = get_klines(ticker, interval, '1 hour ago')

import pandas_ta as ta
df["EMA"] = ta.ema(df.Close, length=200)
df['ATR']= df.ta.atr()


# EMA SIGNAL 
emasignal = [0]*len(df)
backcandles = 4

for row in range(backcandles, len(df)):
    upt = 1
    dnt = 1
    for i in range(row-backcandles, row+1):
        if df.High[i]>=df.EMA[i]:
            dnt=0
        if df.Low[i]<=df.EMA[i]:
            upt=0
    if upt==1 and dnt==1:
        #print("!!!!! check trend loop !!!!")
        emasignal[row]=3
    elif upt==1:
        emasignal[row]=2
    elif dnt==1:
        emasignal[row]=1

df['EMASignal'] = emasignal

print(df)