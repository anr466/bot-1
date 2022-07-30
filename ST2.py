
from get_data import get_klines
import mplfinance as mpf
import pandas as pd
import pandas_ta as ta
import ticker_rules as tk
import numpy as np

def vwap(df , period):
    kline = df
    # calaculate average price for High , Low , Close
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


tickers = []
for i in tk.rules:
    tickers.append(i)


usdt = []
bnb = []
busd = []
eth = []
btc = []
others = []
for i in tk.rules:
    if "USDT" in i:
        usdt.append(i)
    elif "BNB" in i:
        bnb.append(i)
    elif "BUSD" in i :
        busd.append(i)
    elif "ETH" in i:
        eth.append(i)
    elif "BTC" in i:
        btc.append(i)
    else:
        others.append(i)




def heikin_ashi(df):
    heikin_ashi_df = pd.dfFrame(index=df.index.values, columns=['Open', 'High', 'Low', 'Close','Volume'])
    
    heikin_ashi_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['Open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
        
    heikin_ashi_df['High'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['High']).max(axis=1)
    
    heikin_ashi_df['Low'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['Low']).min(axis=1)
    
    return heikin_ashi_df


# for x in usdt:
#     try:
#         df = get_klines(x, "15m", '1 days ago UTC')
#         # df = heikin_ashi(df)

#         vwap_48 = vwap(df , 30)
#         vwap_84 = vwap(df , 60)
#         df['vwap48'] = vwap_48
#         df['vwap84'] = vwap_84
#         df['buy'] =ta.cross(df['vwap48'] , df['vwap84'])
#         df['sell']=ta.cross(df['vwap84'] , df['vwap48'])
#         crosss_buy= df.iloc[-3]["buy"]>0.0
#         crosss_sell =df.iloc[-3]["sell"]>0.0
#         df['crosss_buy'] = crosss_buy
#         df['crosss_sell'] = crosss_sell
#         if crosss_buy == True:
#            print(x)
        
#     except:
#         pass


# df["macd"], df["macd_signal"], df["macd_hist"] = ta.MACD(df['Close'])
# def intersection(lst_1,lst_2):
#     intersections = []
#     insights = []
#     if len(lst_1) > len(lst_2):
#         settle = len(lst_2)
#     else:
#         settle = len(lst_1)
#     for i in range(settle-1):
#         if (lst_1[i+1] < lst_2[i+1]) != (lst_1[i] < lst_2[i]):
#             if ((lst_1[i+1] < lst_2[i+1]),(lst_1[i] < lst_2[i])) == (True,False):
#                 insights.append('buy')
#             else:
#                 insights.append('sell')
#             intersections.append(i)
#     return intersections,insights
#     profit = 0
#     pat = 1
#     for i in range(len(intersections)-pat):
#         index = intersections[i]
#         true_trade= None
#         if df['Close'][index] < df['Close'][index+pat]:
#             true_trade = 'buy'
#         elif df['Close'][index] > df['Close'][index+pat]:
#             true_trade = 'sell'
#         if true_trade != None:
#             if insights[i] == true_trade:
#                 profit += abs(df['Close'][index]-df['Close'][index+1]) 
#             if insights[i] != true_trade:
#                 profit += -abs(df['Close'][index]-df['Close'][index+1])
# intersections,insights = intersection(df["macd_signal"],df["macd"])



df = get_klines('BTCUSDT', "15m", '1 days ago UTC')

def trading_view(df):
    
    # trading view
    coins = TA_Handler()
    coins.set_symbol_as("BTCUSDT")
    coins.set_exchange_as_crypto_or_stock('Binance')
    coins.set_screener_as_crypto()
    coins.set_interval_as(Interval.INTERVAL_15_MINUTES)
    summary = (coins.get_analysis().summary)
    indicators = coins.get_analysis().indicators

    return indicators
#Ema
df['20_EMA'] = df['Close'].ewm(span = 12, adjust = False).mean()
df['50_EMA'] = df['Close'].ewm(span = 26, adjust = False).mean()

#MACD

df['MACD'] = df['20_EMA'] - df['50_EMA']

df['signal'] = df.MACD.ewm(span=9).mean()
df['Histogram'] = df['MACD'] - df['signal']
df['buy'] = np.where(df.MACD > df.signal , 1.0,0.0)

# x = [mpf.make_addplot(df['Histogram'],panel=1 ,color = 'g'),mpf.make_addplot(df['buy'],type='scatter',markersize=200,marker='v')]
# mpf.plot(df,type='candle' ,addplot = x)

