
from tradingview_ta import TA_Handler, Interval, Exchange
from binance_client import Clnt
import ticker_rules as tk
import get_data as gd
import pandas_ta as ta
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



def TA(tikers):
    now = datetime.now()
    dt = now.strftime("%d-%m-%y  %H:%M:%S")
    for x in tikers:
        try:
            #data frame
            data1 = gd.get_klines(x ,'15m' ,'12 hours ago UTC+3')
            # trading view
            coins = TA_Handler()
            coins.set_symbol_as(x)
            coins.set_exchange_as_crypto_or_stock('Binance')
            coins.set_screener_as_crypto()
            coins.set_interval_as(Interval.INTERVAL_15_MINUTES)
            summary = (coins.get_analysis().summary)

            if not data1.empty:

                # vwap calculator
                vwap_48 = vwap(data1 , 48)
                vwap_84 = vwap(data1 , 84)
                data1['vwap48'] = vwap_48
                data1['vwap84'] = vwap_84
                data1['buy'] =ta.cross(data1['vwap48'] , data1['vwap84'])
                data1['sell']=ta.cross(data1['vwap84'] , data1['vwap48'])
                crosss_buy= data1.iloc[-1]["buy"]>0
                crosss_sell =data1.iloc[-1]["sell"]>0
                data1['crosss_buy'] = crosss_buy
                data1['crosss_sell'] = crosss_sell

                #CCI
                data1['cci'] = ta.cci(data1['High'], data1['Low'], data1['Close'])
                cci_buy = data1.iloc[-1]['cci']< -100
                data1['cci_buy'] = cci_buy
               
                #adx
                adx = ta.adx(data1['High'], data1['Low'], data1['Close'],length=7)
                data1['ADX'] = adx['ADX_7']
                adx_buy = data1.iloc[-1]['ADX']< 50
                data1['adx_buy'] = adx_buy
                
                #RSI
                data1['RSI'] = ta.rsi(data1['Close'], length=3)
                rsi_buy = data1.iloc[-1]['RSI']< 20
                data1['rsi_buy'] = rsi_buy

            
                #Ema
                data1['20_EMA'] = data1['Close'].ewm(span = 20, adjust = False).mean()
                data1['50_EMA'] = data1['Close'].ewm(span = 50, adjust = False).mean()
                data1['Signal'] = 0.0  
                data1['Signal'] = np.where(data1['20_EMA'] > data1['50_EMA'], 1.0, 0.0)
                ema_buy = data1.iloc[-1]['Signal']==1.0
                data1['ema_buy'] = ema_buy
                
                if ema_buy==True and  summary['RECOMMENDATION'] == "STRONG_BUY":
     
                    #strargy1
                    if x.endswith("USDT") or x.endswith("BUSD"):
                        price_now = fo.get_ticker_price(x)
                        price_cal = fo.format_price(x , price_now)
                        
                        for c in data1['Close'].index:
                            timestap = []
                            timestap.append(c)
                        target = fo.price_calculator(x , price_now , tp1 = 2.5 ,tp2=5)
                        stoploss = fo.price_calculator(x , price_now , tp1 = -2.5)
                        tp1 = list(target.values())[0]
                        tp2 = list(target.values())[1]
                        stopprice = list(stoploss.values())[0]
                        send_msg(f'stratgy1\nbuy==> ${x} \nprice now==> ${price_cal} \nTime==> {timestap[0]} \ntp1==> ${tp1}\ntp2==>{tp2}\nstoploss==> ${stopprice}')
                        db_ticker = signals.find('buy', x)
                        db_ticker_name = db_ticker[0]
                        db_ticker_price = db_ticker[1]
                        
                        if x == db_ticker_name:
                            if db_ticker_price >= tp1:
                                send_msg(f"profit target Done on stratgy1 ==>{x}\n{tp1}")
                            elif db_ticker_price <= stopprice:
                                send_msg(f"sell done on stoploss stratgy1 ==>{x}")
                            elif db_ticker_price > tp2:
                                send_msg(f"profit target Done on stratgy1 ==>{x}\n{tp2}")
                        signals.add('buy' , dt , x , price_now=price_cal,tp1=tp1,tp2=tp2,sl=stopprice)                    
                else:
                    pass                    
        except:
            pass
    
     



def lunch():
    threading.Thread(target=TA , args=([usdt])).start()
    # threading.Thread(target=TA , args=([btc])).start()
    # threading.Thread(target=TA , args=([busd])).start()
    # threading.Thread(target=TA , args=([eth])).start()
    # threading.Thread(target=TA , args=([bnb])).start()
    # threading.Thread(target=TA , args=([others])).start()
    



def hd():
    interval = [0,15,30,45]
    time_srv = Clnt.get_server_time()#for binance time
    time = pd.to_datetime(time_srv["serverTime"], unit = "ms")
    min_ = time.strftime("%M")
    min_ = int(min_)
    sec_ = time.strftime("%S")
    sec_ = int(sec_)
    for i in interval:
            if min_ == i and sec_ == 3:
                ti.sleep(10)
                lunch()
                

            

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

# bot.infinity_polling()
    
