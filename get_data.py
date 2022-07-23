from binance_client import Clnt
import pandas as pd
import pandas_ta as ta
import numpy as np
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
   
        df.dropna(inplace=True)
        for i in range(6 , len(columns)):
             del df[columns[i]]

        return df
    else:
        return None



df=get_klines("BTCUSDT",'15m','12 hours ago UTC')      



def RSI(data: pd.DataFrame, window_length=14) -> pd.Series:
    """
    Calcula el indicador RSI sobre una ventana móvil.
    https://www.investopedia.com/terms/r/rsi.asp
    """
    df_ = data.copy()
    close = df_['Close']
    delta = close.diff()
    up = delta.clip(lower=0)  # transforma en ceros las perdidas
    down = -1 * delta.clip(upper=0)  # transforma en ceros las ganancias
    # WMA
    roll_up = up.ewm(com=window_length - 1, adjust=True, min_periods=window_length).mean()
    roll_down = down.ewm(com=window_length - 1, adjust=True, min_periods=window_length).mean()
    # Calculate the RSI
    RS = roll_up / roll_down
    return 100.0 - (100.0 / (1.0 + RS))


def Stochastic_RSI(data: pd.DataFrame, window_length=14) -> pd.Series:
    """
    The Stochastic RSI (StochRSI) is an indicator used in technical analysis that ranges between zero and one (or zero and 100 on
    some charting platforms) and is created by applying the Stochastic oscillator formula to a set of relative strength index (RSI)
    values rather than to standard price data.
    https://www.investopedia.com/terms/s/stochrsi.asp#:~:text=The%20Stochastic%20RSI%20(StochRSI)%20is,than%20to%20standard%20price%20data.
    """
    df_ = data.copy()
    rsi = RSI(data=df_, window_length=window_length)
    return (rsi - rsi.rolling(window_length).min()) / (rsi.rolling(window_length).max() - rsi.rolling(window_length).min())



# print(df)