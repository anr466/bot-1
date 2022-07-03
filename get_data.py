from binance_client import Clnt
import pandas as pd
import pandas_ta as ta

columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'IGNORE', 'Quote_Volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Can be ignored']


def heikin_ashi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])
    
    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
        
    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)
    
    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)
    
    return heikin_ashi_df

def get_klines(pair,interval,depth):
    data = Clnt.get_historical_klines(pair,interval,depth)
    df = pd.DataFrame(data)
    if not df.empty:
        df.columns = columns
        df['Date'] = pd.to_datetime(df["Date"],unit= 'ms')
        df = df.set_index('Date')
        df['Open'] = pd.to_numeric(df['Open'])
        df['Close']= pd.to_numeric(df['Close'])
        df['High'] = pd.to_numeric(df['High'])
        df['Low'] = pd.to_numeric(df['Low'])
        df['Volume'] = pd.to_numeric(df['Volume'])
        # df['pct'] = (df['Close'] - df['Open'])/(df['Open'])
        df['RSI'] = ta.rsi(df['Close'],length=3)
        df['cci'] = ta.cci(df['High'], df['Low'], df['Close'])
        df['EMA'] = ta.ema(df['Close'],length=50)
        adx = ta.adx(df['High'], df['Low'], df['Close'],length=7)
        df['ADX'] = adx['ADX_7']
        # df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'])


        df.dropna(inplace=True)
        for i in range(6 , len(columns)):
             del df[columns[i]]

        return df
    else:
        return None



# df=get_klines("BTCUSDT",'15m','27 hours ago UTC+3')      


# print(df)



# شراء 
# Cci < -100
# Rsi < 20