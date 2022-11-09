

from get_data import get_klines 
import pandas_ta as ta
import numpy as np 
import time as ti
import numpy as np
import matplotlib as mpl
mpl.use('tkagg')    #YAAA!!  this finally makes the Damn thing work
import matplotlib.pyplot as plt


def figure(tickers):
    df = get_klines(tickers, '1m', '6 hour ago')

    if not df.empty:

    
        # EMA
        df['10_EMA'] = df['Close'].ewm(span = 4, adjust = False).mean()
        df['20_EMA'] = df['Close'].ewm(span = 50, adjust = False).mean()
        df['50_EMA'] = df['Close'].ewm(span = 700, adjust = False).mean()

        # bollinger bands Calculate
        periods = 20
        df['SMA'] = df['Close'].rolling(window = periods).mean()
        df['STD'] = df['Close'].rolling(window = periods).std()
        df['upper'] = df['SMA'] + (df['STD'] * 2)
        df['Lower'] = df['SMA'] - (df['STD'] * 2)

        #marge ema with bb in one function 
        def get_bb_ema(data):
            buy_signal= []
            sell_signal = []
            for i in range(len(data['Close'])):
                if data['20_EMA'][i] >  data['50_EMA'][i] and data['Close'][i] >  data['upper'][i]: # then sell 
                    buy_signal.append(np.nan)
                    sell_signal.append(data['Close'][i])
                elif data['20_EMA'][i] <  data['50_EMA'][i] and data['Close'][i] <  data['Lower'][i]: # then buy 
                    sell_signal.append(np.nan)
                    buy_signal.append(data['Close'][i])
                else: # notheing all set nan
                    buy_signal.append(np.nan)
                    sell_signal.append(np.nan)
            return (buy_signal , sell_signal)


        df['buy_EMAbb'] = get_bb_ema(df)[0]
        df['sell_EMAbb'] = get_bb_ema(df)[1]

        buy= df.iloc[-1:]["buy_EMAbb"]
        sell = df.iloc[-1:]['sell_EMAbb']


        #style use polt
                
        plt.style.use('fivethirtyeight')
        # configuration the show image with BB
        #get fig and fig size
        fig = plt.figure(figsize=(8,6))
        #Add the subplot
        ax = fig.add_subplot(1,1,1)
        #get index for df
        x_axis = df.index
        #plot area between Upper and Lower and set color grey
        ax.fill_between(x_axis,df['upper'],df['Lower'],color = 'grey')

        # plot Close price
        ax.plot(x_axis , df['Close'] , color = 'gold' , lw = 3 , label = 'Close price' , alpha = 0.5)
        ax.plot(x_axis , df['SMA'] , color = 'blue' , lw = 3 , label = 'Simple Moving Average',alpha = 0.5)
        # ax.plot(x_axis , df['20_EMA'] , color = 'magenta' , lw = 3 , label = '20 EMA' , alpha = 0.5)
        # ax.plot(x_axis , df['50_EMA'] , color = 'black' , lw = 3 , label = '50 EMA',alpha = 0.5)

        ax.scatter(x_axis , df['buy_EMAbb'] , color = 'green' , lw = 3 , label = 'buy', marker = '^',alpha = 0.5)
        ax.scatter(x_axis , df['sell_EMAbb'] , color = 'red' , lw = 3 , label = 'sell',marker = '^',alpha = 0.5)
        # ax.scatter(x_axis , df['buy'] , color = 'black' , lw = 3 , label = 'BUY last candle',marker = '^',alpha = 0.5)
        # ax.scatter(x_axis , df['sell_EMA'] , color = 'yellow' , lw = 3 , label = 'EMA_SELL',marker = '^',alpha = 0.5)

        ax.set_title(f'buy signal for {tickers}')
        ax.set_xlabel('Date')
        ax.set_ylabel('USD Price $')
        plt.xticks(rotation='horizontal')
        ax.legend()
        fig.canvas.draw_idle()
        # ti.sleep(1)
        photo = fig.savefig('buy.jpg', dpi=80, format="jpg")
        # anim = FuncAnimation.save(photo, 'adsd.png')
        ti.sleep(1)
        fig.clear()
        plt.close(fig)
        

    return photo




figure('BNBUSDT')