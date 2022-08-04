
from tradingview_ta import TA_Handler, Interval, Exchange
from binance_client import Clnt
import ticker_rules as tk
import get_data as gd
import pandas_ta as p_ta
import ta
import pandas as pd
import format_orders as fo
from DB import signals
import threading
import telebot
import requests
import time as ti
from datetime import datetime
import numpy as np 

bot_token = "5243412284:AAElbwcCDmKXOe4XTvG1F3EFdbDleAHH3ew"

bot = telebot.TeleBot(bot_token)

chat_id = "174958495"



def send_msg(text):
    url = "https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id="+chat_id+"parse_mode=Markdown&text="
    req = url+text
    response = requests.get(req)
    return response.json()




def vwap(df , period):
    kline = df
    # calaculate average price for high , low , close
    kline['tp'] = p_ta.hlc3(high= kline['High'] , low= kline['Low'] ,close=kline['Close'])
    kline['tpV'] = kline['tp'] * kline['Volume']
    #using moving average
    kline['mtpv'] = p_ta.sma(kline['tpV'] , length = period)
    kline['mV'] = p_ta.sma(kline['Volume'] , length = period)
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




def TA(tikers):
    now = datetime.now()
    dt = now.strftime("%d-%m-%y  %H:%M:%S")
    for x in tikers:
        
        try:
            #data frame
            df = gd.get_klines(x ,'1m' ,'26 hours ago UTC')
            # trading view
            coins = TA_Handler()
            coins.set_symbol_as(x)
            coins.set_exchange_as_crypto_or_stock('Binance')
            coins.set_screener_as_crypto()
            coins.set_interval_as(Interval.INTERVAL_5_MINUTES)
            summary = (coins.get_analysis().summary)
            indicators = coins.get_analysis().indicators 
            RSI = indicators["RSI"]
            CCI = indicators["CCI20"]
            ADX_POSITIVE = indicators["ADX+DI"]
            MACD = indicators["MACD.macd"]
            
      
            if not df.empty:

                # vwap calculator
                vwap_48 = vwap(df , 30)
                vwap_84 = vwap(df , 60)
                df['vwap48'] = vwap_48
                df['vwap84'] = vwap_84
                df['buy'] =p_ta.cross(df['vwap48'] , df['vwap84'])
                df['sell']=p_ta.cross(df['vwap84'] , df['vwap48'])
                crosss_buy= df.iloc[-1]["buy"]>0.0
                crosss_sell =df.iloc[-1]["sell"]>0.0
                df['crosss_buy'] = crosss_buy
                df['crosss_sell'] = crosss_sell

                #CCI
                df['cci'] = p_ta.cci(df['High'], df['Low'], df['Close'])
                cci_buy = df.iloc[-1]['cci']
                df['cci_buy'] = cci_buy
               
                #adx
                adx = p_ta.adx(df['High'], df['Low'], df['Close'],length=7)
                df['ADX'] = adx['ADX_7']
                adx_buy = df.iloc[-1]['ADX']
                df['adx_buy'] = adx_buy
                
                #RSI
                df['RSI'] = p_ta.rsi(df['Close'], length=7)
                rsi_buy = df.iloc[-1]['RSI']
                df['rsi_buy'] = rsi_buy

                
                #Ema
                df['20_EMA'] = df['Close'].ewm(span = 12, adjust = False).mean()
                df['50_EMA'] = df['Close'].ewm(span = 26, adjust = False).mean()
               
                #MACD
                df['MACD'] = df['20_EMA'] - df['50_EMA']
                df['signal'] = df.MACD.ewm(span=9).mean()
                df['Histogram'] = df['MACD'] - df['signal']
                histogram = df['Histogram'][-1]
                
                # histogram = histogram
                buy_macd = np.where(df.MACD[-1] > df.signal[-1] , 1.0,0.0)
                


                # MACDD = ta.trend.MACD(close=df['Close'], window_fast=12, window_slow=26, window_sign=9)
                # df['MACDD'] = MACDD.macd()
                # df['macdd'] = MACDD.macd_diff()  #MACD HISTOGRAM
                # macd_5=df['macd'].iloc[-7]
                # macd_4=df['macd'].iloc[-6]
                # macd_3=df['macd'].iloc[-5]
                # macd_2=df['macd'].iloc[-4]
                # macd_1=df['macd'].iloc[-3]
                # macd_0=df['macd'].iloc[-2]
                

                
                rsi_fun = gd.RSI(df)
                rsi_fun = rsi_fun[-1]


                stoch = gd.Stochastic_RSI(df)
                stoch = stoch[-1]
                

                if summary['RECOMMENDATION'] == "STRONG_BUY" and rsi_fun>60 and cci_buy>200 and cci_buy<250 and adx_buy>50 and adx_buy<70:
                    #strargy1
                    if x.endswith("USDT") or x.endswith("BUSD"):
        
                        price_now = fo.get_ticker_price(x)
                        price_cal = fo.format_price(x , price_now)    
                        
                        for c in df['Close'].index:
                            timestap = []
                            timestap.append(c)
                       
                        target = fo.price_calculator(x , price_now , tp1 = 2)
                        stoploss = fo.price_calculator(x , price_now , tp1 = -2)
                        tp1 = list(target.values())[0]
                        stopprice = list(stoploss.values())[0]

                        send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                        signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice)  

        except:
            pass                   




b =[]
def balance_profit(amount,fee):
    bb = amount+fee
    b.append(bb)
    return sum(b)
def balance_loss(amount,fee):
    bb = amount-fee
    b.append(bb)
    return sum(b)
 


def track_price(t_tracking):
    now = datetime.now()
    dt = now.strftime("%d-%m-%y  %H:%M:%S")

    for x in t_tracking:
        try:
            ti.sleep(1)
            db_ticker = signals.find('buy', x)
        
            price_now = fo.get_ticker_price(x)
            price_cal = fo.format_price(x , price_now)
            
            db_ticker_name = db_ticker[0]
            db_ticker_price = db_ticker[1]
            db_ticker_tp1 = db_ticker[2]
            db_ticker_SL = db_ticker[3]

            # print(f'{db_ticker_name} vs {x} \n compare price in db {db_ticker_price} vs real price {price_cal}  ')

            if x == db_ticker_name:
                
                if price_cal >= db_ticker_tp1:
                   
                    balance_profit(20, 0.2)
                    balance = sum(b)
        
                    send_msg(f"تحقق هدف البيع للعملة   ==>${x}\n tp1 = {db_ticker_tp1}\nbalance is {balance}")
                    signals.add('profit', dt, x, price_cal, db_ticker_tp1, db_ticker_SL)
                    signals.delete_one('buy', x)
                    
                elif price_cal <= db_ticker_SL:
                   
                    balance_loss(20, 0.2)
                    balance = sum(b)
                    
                    send_msg(f"تم البيع على وقف الخسارة ==>${x}\n sl = {db_ticker_SL} \nbalance is {balance}")
                    signals.add('loss', dt, x, price_cal, db_ticker_tp1, db_ticker_SL)
                    signals.delete_one('buy', x)
                    
        except:
            pass





def lunch():
    threading.Thread(target=TA , args=([usdt])).start()
   
    # threading.Thread(target=TA , args=([btc])).start()
    threading.Thread(target=TA , args=([busd])).start()
    
    # threading.Thread(target=TA , args=([eth])).start()
    # threading.Thread(target=TA , args=([bnb])).start()
    # threading.Thread(target=TA , args=([others])).start()
    threading.Thread(target=track_price , args=([busd])).start()
    
    threading.Thread(target=track_price , args=([usdt])).start()
    

    
    # ti.sleep(60)
    



def hd():
    one_minute = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]
    two_minute = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58]
    three_minute = [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57]
    five_minute = [0,5,10,15,20,25,30,35,40,45,50,55]
    _15_mintue = [0,15,30,45]
    time_srv = Clnt.get_server_time()#for binance time
    time = pd.to_datetime(time_srv["serverTime"], unit = "ms")
    min_ = time.strftime("%M")
    min_ = int(min_)
    sec_ = time.strftime("%S")
    sec_ = int(sec_)
    for i in two_minute:
        if min_ == i and sec_ == 3:
            ti.sleep(5)
            lunch()
    # for i in three_minute:
    #     if min_ == i and sec_ == 30:
    #         ti.sleep(5)
    #         threading.Thread(target=track_price , args=([busd])).start()
    #         threading.Thread(target=track_price , args=([usdt])).start()
    




# track_price()      
while True:
    hd()


    



# @bot.message_handler(func=lambda message: True)  
# def t_mer(message):
#     text = message.text
#     chid = message.chat.id
#     if text == "/start":
#         bot.send_message(chid," تشغيل البوت")
#     elif text == "/off":
#         bot.send_message(chid," ايقاف البوت")
#     else:
#         bot.send_message(chid,"اشتغل")



# while True:
#     hd()
#     bot.infinity_polling()
    
