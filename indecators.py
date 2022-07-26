from tradingview_ta import TA_Handler, Interval, Exchange
import get_data as gd
import ta



df = gd.get_klines('BTCUSDT','15m' ,'50 hours ago UTC')

class indicators():

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
    def sma_stochrsi(df):
        df['SMA_200'] = ta.trend.sma_indicator(df.Close , window = 200)
        df['stochrsi_k'] = ta.momentum.stochrsi_k(df.Close , window = 10)
        df.dropna(inplace = True)
        df['buy'] = (df.Close > df.SMA_200) & (df.stochrsi_k < 0.05)
        return df


x = indicators.trading_view(df)

# print(x)
