
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



bot_token = "5243412284:AAElbwcCDmKXOe4XTvG1F3EFdbDleAHH3ew"

bot = telebot.TeleBot(bot_token , parse_mode=None)

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
    # now = datetime.now()
    # dt = now.strftime("%d-%m-%y  %H:%M:%S")
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
                rsi_buy = data1.iloc[-1]['RSI']< 30
                rsi_sell = data1.iloc[-1]['RSI']> 70
                data1['rsi_buy'] = rsi_buy
                data1['rsi_sell'] = rsi_sell







                if crosss_buy == True and crosss_sell == False and summary['RECOMMENDATION'] == "STRONG_BUY" or rsi_buy == True and rsi_sell == False:

                    # if usdt use usdt balance
                    # if BUSD use BUSD balance
                    # if ETH use ETH balance
                    # if BTC use BTC balance
                    price_now = fo.get_ticker_price(x)
                    price_cal = fo.format_price(x , price_now)
                    oldprice = price_cal
                    for c in data1['Close'].index:
                        timestap = []
                        timestap.append(c)



                    target = fo.price_calculator(x , price_now , tp1 = 3)
                    profit = list(target.values())[0]
                    send_msg(f'ticker buy: {x} \nprice now: {price_cal}\n time:{timestap} \n target price : {profit}')
                    if profit >= oldprice :
                        send_msg(f'ticker {x} \n target is profit : {profit}')

                elif crosss_sell == True and crosss_buy == False and summary['RECOMMENDATION'] == "STRONG_SELL" or rsi_sell == True and rsi_buy == False:
                    price_now = fo.get_ticker_price(x)
                    price_cal = fo.format_price(x , price_now)
                    oldprice = price_cal
                    stoploss = fo.price_calculator(x , price_now , tp1 = -3)
                    profit = list(stoploss.values())[0]
                    send_msg(f'ticker sell: {x} \nprice now: {price_cal}\n time:{timestap} \n stoploss: {profit}')
                    if profit <= oldprice :
                        send_msg(f'ticker {x} \n target is profit sell : {profit}')

                    #signals.add('sell' , dt , x , price_now=price_cal,tp=target)
                # else:
                #     print(x)
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
                send_msg(f"البحث عن عملات ربع ساعة {lunch()}")



def start():
    while True:
        hd()



@bot.message_handler(func=lambda message: True)
def t_mer(message):
    text = message.text
    chid = message.chat.id
    if text == "/start":
        bot.send_message(chid,f"{start()} \n جاري تشغيل البوت")
    elif text == "/off":
        bot.send_message(chid,f"\n ايقاف البوت")
    else:
        bot.send_message(chid,"اشتغل")

while True:
    bot.polling()
