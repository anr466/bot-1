from get_data import get_klines
import talib as ta
import pandas_ta as pt
import numpy as np


df = get_klines('BTCUSDT', '1m', '1 hour ago')

vwaplist = [48,200]


def vwap1(df , period):
    kline = df
    # calaculate average price for high , low , close
    kline['tp'] = pt.hlc3(high= kline['High'] , low= kline['Low'] ,close=kline['Close'])
    kline['tpV'] = kline['tp'] * kline['Volume']
    #using moving average
    kline['mtpv'] = pt.sma(kline['tpV'] , length = period)
    kline['mV'] = pt.sma(kline['Volume'] , length = period)
    # calaulate vwap
    kline['vwap'] = kline['mtpv'] /  kline['mV']
    vwap = kline['vwap']
    columns = kline.columns

    for i in range(6 , len(columns)):
        del kline[columns[i]]


    return vwap




def vwapChart(df, vwapList):
    for v in vwapList:
        # try :
        df['typicalPrice'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['typicalPriceVolume'] = df['typicalPrice'] * df['Volume']
        df['cumulativeTypicalPriceVolume'] = ta.SUM(
            df['typicalPriceVolume'], v)
        df['cumulativeVolume1'] = ta.SUM(df['Volume'], v)
        df[f'chart{v}'] = df['cumulativeTypicalPriceVolume'] / \
            df['cumulativeVolume1']
        del df['typicalPrice']
        del df['typicalPriceVolume']
        del df['cumulativeTypicalPriceVolume']
        del df['cumulativeVolume1']
        

        # except :
        #     df[f'vwap{v}'] = 0
        #     pass

    return df


def vwapScore(df, vwapList):
    for v in vwapList:
        try:
            df['mean'] = ta.SUM(df['Volume']*df['Close'],
                                v) / ta.SUM(df['Volume'], v)
            df['vwapsd'] = np.sqrt(ta.SMA(pow(df['Close']-df['mean'], 2), v))
            df[f'vwap{v}'] = (df['Close']-df['mean']) / df['vwapsd']
            del df['mean']
            del df['vwapsd']
            # del df['Open']
            # del df['High']
            # del df['Low']
            
        except:
            df[f'vwap{v}'] = 0
            pass

    return df



# x = vwapChart(df, vwaplist)

# print(x)