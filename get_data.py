from binance_client import Clnt
import pandas as pd
import pandas_ta as ta

columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'IGNORE', 'Quote_Volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Can be ignored']



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
        df['RSI'] = round(ta.rsi(df['Close'], timeperiod=14),1)
        df['rsi_buy'] = df.iloc[-1]['RSI']< 30
        df['rsi_sell'] = df.iloc[-1]['RSI']> 70
        df.dropna(inplace=True)
        for i in range(6 , len(columns)):
             del df[columns[i]]

        return df
    else:
        return None



df=get_klines("BTCUSDT",'15m','12 hours ago UTC')      
for c in df['Close'].index:
        timestap = []

        timestap.append(c)

