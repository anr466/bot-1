from get_data import get_klines
from matplotlib import pyplot as plt



df = get_klines("BTCUSDT", "1h", "350 hours ago UTC+3")


buy = []

for i in range(len(df)):
    if df.MACD.iloc[i] > df.signal.iloc[i] and df.MACD.iloc[-1] < df.signal.iloc[-1]:
        buy.append(i)



# plt.plot(df.) 
# # plt.plot(df.RSI)
# # plt.plot(df.signal) 
# # plt.plot(df.MACD)

# plt.style.use('ggplot')
# plt.show()
