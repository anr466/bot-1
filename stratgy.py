
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
import time
from datetime import datetime

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
            # time.sleep(1)
            #data frame
            data1 = gd.get_klines(x ,'15m' ,'26 hours ago UTC+3')
            # trading view
            coins = TA_Handler()
            coins.set_symbol_as(x)
            coins.set_exchange_as_crypto_or_stock('Binance')
            coins.set_screener_as_crypto()
            coins.set_interval_as(Interval.INTERVAL_15_MINUTES)
            summary = (coins.get_analysis().summary)

            coins1 = TA_Handler()
            coins1.set_symbol_as(x)
            coins1.set_exchange_as_crypto_or_stock('Binance')
            coins1.set_screener_as_crypto()
            coins1.set_interval_as(Interval.INTERVAL_30_MINUTES)
            summary1 = (coins1.get_analysis().summary)


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
                rsi_buy = data1.iloc[-1]['RSI']< 30
                rsi_sell = data1.iloc[-1]['RSI']> 70
                data1['rsi_buy'] = rsi_buy
                data1['rsi_sell'] = rsi_sell


                #if crosss_buy == True and crosss_sell == False and summary['RECOMMENDATION'] == "STRONG_BUY" or 
                if summary['RECOMMENDATION'] == "STRONG_BUY" and summary1['RECOMMENDATION'] == "STRONG_BUY":
                # if rsi_buy == True and rsi_sell == False:
                    if x.endswith("USDT"):
                        price_now = fo.get_ticker_price(x)
                        price_cal = fo.format_price(x , price_now)
                        
                        for c in data1['Close'].index:
                            timestap = []
                            timestap.append(c)
                        target = fo.price_calculator(x , price_now , tp1 = 2.5)
                        stoploss = fo.price_calculator(x , price_now , tp1 = -2.5)
                        profit = list(target.values())[0]
                        stopprice = list(stoploss.values())[0]
                        send_msg(f'buy==> ${x} \nprice now==> ${price_cal} \nTime==> {timestap[0]} \nbuy_limit==> ${profit}\nstoploss==> ${stopprice}')
                        db_ticker = signals.find('buy', x)
                        db_ticker_name = db_ticker[0]
                        db_ticker_price = db_ticker[1]
                        if x == db_ticker_name:
                            if db_ticker_price >= profit:
                                send_msg(f"profit target Done==>{x}")
                            elif db_ticker_price <= stopprice:
                                send_msg(f"sell done on stoploss==>{x}")
                            else:
                                signals.add('buy' , dt , x , price_now=price_cal,tp=profit)         
        except:
            pass
    
     


def lunch():
    x = threading.Thread(target=TA , args=([usdt])).start()
    # threading.Thread(target=TA , args=([btc])).start()
    # threading.Thread(target=TA , args=([busd])).start()
    # threading.Thread(target=TA , args=([eth])).start()
    # threading.Thread(target=TA , args=([bnb])).start()
    # threading.Thread(target=TA , args=([others])).start()
    return x




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
                lunch()
                time.sleep(10)
    
            




while True:
    hd()
    
    


# @bot.message_handler(func=lambda message: True)  
# def t_mer(message):
#     text = message.text
#     chid = message.chat.id
#     if text == "/start":
#         send_msg("تشغيل البوت")
#         hd()
#     elif text == "/off":
#         bot.send_message(chid," ايقاف البوت")
#     else:
#         bot.send_message(chid,"اشتغل")




# bot.infinity_polling()
    
