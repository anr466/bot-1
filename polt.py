from get_data import get_klines
from matplotlib import pyplot as plt



df = get_klines("BTCUSDT", "1h", "26 hours ago UTC+3")



# plt.plot(df.close) 
# # plt.plot(df.RSI)
# # plt.plot(df.signal) 
# # plt.plot(df.MACD)

# plt.style.use('ggplot')
# plt.show()
