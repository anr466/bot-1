
from tradingview_ta import TA_Handler, Interval, Exchange
from Bclient import Clnt
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


usdt = []
list_buy = []
busd = []

for i in tk.rules:
    if "USDT" in i:
        usdt.append(i)
    elif "BUSD" in i :
        busd.append(i)



def TA(tikers):
    now = datetime.now()
    dt = now.strftime("%d-%m-%y  %H:%M:%S")
    for x in tikers:   
        try:
            #data frame
            df = gd.get_klines(x ,'1m' ,'30 minutes ago UTC')
            # trading view
            coins = TA_Handler()
            coins.set_symbol_as(x)
            coins.set_exchange_as_crypto_or_stock('Binance')
            coins.set_screener_as_crypto()
            coins.set_interval_as(Interval.INTERVAL_15_MINUTES)
            summary = (coins.get_analysis().summary)
            indicators = coins.get_analysis().indicators 
            # print(df)
            RSI = indicators["RSI"]
            RSI = round(RSI,1)
            CCI = indicators["CCI20"]
            CCI = round(CCI,1)
            ADX_POSITIVE = indicators["ADX+DI"]
            ADX_POSITIVE = round(ADX_POSITIVE,1)
            MACD = indicators["MACD.macd"]
            MACD = round(MACD,1)
      
            if not df.empty:

                # vwap calculator
                vwap_48 = vwap(df , 48)
                vwap_84 = vwap(df , 200)
                df['vwap48'] = vwap_48
                df['vwap84'] = vwap_84
                df['buy'] =ta.cross(df['vwap48'] , df['vwap84'])
                df['sell']=ta.cross(df['vwap84'] , df['vwap48'])
                crosss_buy= df.iloc[-1]["buy"]>0.0
                crosss_sell =df.iloc[-1]["sell"]>0.0
                df['crosss_buy'] = crosss_buy
                df['crosss_sell'] = crosss_sell

                #CCI
                df['cci'] = ta.cci(df['High'], df['Low'], df['Close'])
                cci_buy = df.iloc[-1]['cci']
                cci_buy = round(cci_buy,1)
                df['cci_buy'] = cci_buy
               
                #adx
                adx = ta.adx(df['High'], df['Low'], df['Close'],length=7)
                df['ADX'] = adx['ADX_7']
                adx_buy = df.iloc[-1]['ADX']
                adx_buy = round(adx_buy,1)

                df['adx_buy'] = adx_buy
                
                #RSI
                df['RSI'] = ta.rsi(df['Close'], length=7)
                rsi_buy = df.iloc[-1]['RSI']
                rsi_buy= round(rsi_buy,1)
                df['rsi_buy'] = rsi_buy
            
                #Ema
                df['20_EMA'] = df['Close'].ewm(span = 12, adjust = False).mean()
                df['50_EMA'] = df['Close'].ewm(span = 26, adjust = False).mean()
               
                #MACD
                df['MACD'] = df['20_EMA'] - df['50_EMA']
                df['signal'] = df.MACD.ewm(span=9).mean()
                signal_ema = df['signal']
                df['Histogram'] = df['MACD'] - df['signal']
                histogram = df['Histogram'][-1]
                histogram = round(histogram,1)
                # histogram = histogram
                buy_macd = np.where(df.MACD[-1] > df.signal[-1] , 1.0,0.0)
             


                rsi_fun = gd.RSI(df)
                rsi_fun = rsi_fun[-1]
                rsi_fun = round(rsi_fun,1)

                stoch = gd.Stochastic_RSI(df)
                stoch = stoch[-1]      
                stoch = round(stoch,1) 
                

                if summary['RECOMMENDATION'] == "STRONG_BUY" and RSI>60 and ADX_POSITIVE>55 and CCI>150:
                    #strargy1

                    buy_list = signals.buy_list()

                    if x not in buy_list:

                        price_now = fo.get_ticker_price(x)
                        price_cal = fo.format_price(x , price_now)
                        
                        for c in df['Close'].index:
                            timestap = []
                            timestap.append(c)
                       
                        target = fo.price_calculator(x , price_now , tp1 = 2.5)
                        stoploss = fo.price_calculator(x , price_now , tp1 = -5)
                        tp1 = list(target.values())[0]
                        stopprice = list(stoploss.values())[0]

                        
                        balance = signals.free_balance('balance')

                        # تقسيم الرصيد
                        new_balance1 = round(balance,2)
                        new_balance2 = round((balance/2),2)
                        new_balance3 = round((balance/3),2)
                        new_balance4 = round((balance/4),2)
                        new_balance5 = round((balance/5),2)
                        new_balance6 = round((balance/6),2)
                        new_balance7 = round((balance/7),2)
                        new_balance8 = round((balance/8),2)
                        new_balance9 = round((balance/9),2)
                        new_balance10 = round((balance/10),2)

                        if new_balance10 >= 10.5:

                            #add x to buy_list     
                            

                            buy = signals.buy_balance('balance',new_balance10)
                            signals.add_balance('balance',buy) 
                            balance = signals.free_balance('balance')
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance10}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance10)


                        elif new_balance9 >= 10.5:

                            #add x to buy_list 
                            

                            buy = signals.buy_balance('balance',new_balance9)
                            signals.add_balance('balance',buy)
                            balance = signals.free_balance('balance')  
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance9}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance9)

                        elif new_balance8 >= 10.5:

                            #add x to buy_list 
                            

                            buy = signals.buy_balance('balance',new_balance8)
                            signals.add_balance('balance',buy) 
                            balance = signals.free_balance('balance')                    
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance8}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance8)

                        elif new_balance7 >= 10.5:

                        
                            buy = signals.buy_balance('balance',new_balance7)
                            signals.add_balance('balance',buy)
                            balance = signals.free_balance('balance')
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance7}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance7)

                        
                        elif new_balance6 >= 10.5:

                        
                            buy = signals.buy_balance('balance',new_balance6)
                            signals.add_balance('balance',buy)
                            balance = signals.free_balance('balance')
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance6}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance6)
        
                            
                        elif new_balance5 >= 10.5:

                        
                            buy = signals.buy_balance('balance',new_balance5)
                            signals.add_balance('balance',buy)
                            balance = signals.free_balance('balance')                 
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance5}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance5)
                            
                            
                        elif new_balance4 >= 10.5:

                        
                            buy = signals.buy_balance('balance',new_balance4)
                            signals.add_balance('balance',buy)
                            balance = signals.free_balance('balance') 
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance4}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance4)
                            
                    
                        elif new_balance3 >= 10.5:

                    
                            buy = signals.buy_balance('balance',new_balance3)
                            signals.add_balance('balance',buy)
                            balance = signals.free_balance('balance')
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance3}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance3)
                            
                            
                        elif new_balance2 >= 10.5:

                    
                            buy = signals.buy_balance('balance',new_balance2)
                            signals.add_balance('balance',buy)
                            balance = signals.free_balance('balance')
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance2}\n\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance2)
                            
                            
                        elif new_balance1 >= 10.5:

                        
                            buy = signals.buy_balance('balance',new_balance1)
                            signals.add_balance('balance',buy) 
                            balance = signals.free_balance('balance')
                            send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_cal} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance1}\nالرصيد المتبقي {balance}\nindicators\nrsi = {RSI} \ncci = {CCI} \nADX = {ADX_POSITIVE} \nmacd = {MACD} \n mycode \nrsi_buy = {rsi_buy} \nadx_buy = {adx_buy} \nmacd_buy = {buy_macd} \nstoch = {stoch} \nrsi_fun = {rsi_fun} \ncci = {cci_buy} \n histogram = {histogram} \n vwap = {crosss_buy}')
                            signals.add('buy', dt=dt,tickers= x,price_now= price_cal,tp1= tp1,sl= stopprice,amount=new_balance1)
                    
                    
        except:
            pass
    ti.sleep(60)
                      
               
                          

def targetbalance(goal,new_balance):
    target = float((new_balance / goal) * 100)
    target = round(target,1)
    return target




def track_price():
        now = datetime.now()
        dt = now.strftime("%d-%m-%y  %H:%M:%S")

        balance = []

        buy_list = signals.buy_list()

        for x in buy_list:
            try:

                    db_ticker = signals.find('buy', x)        
                    db_ticker_name = db_ticker[0]
                    db_ticker_price = db_ticker[1]
                    db_ticker_tp1 = db_ticker[2]
                    db_ticker_SL = db_ticker[3]
                    db_balance = db_ticker[4]
                    db_balance = float(db_balance)
                    fee = (2.5*db_balance) / 100
                    fee = round(float(fee),1)
                    print(x)
                    
                    
                    
                    price_now = fo.get_ticker_price(x)
                    price_cal = fo.format_price(x , price_now)

                    print(price_cal,db_ticker_tp1)
                    
                    if price_cal >= db_ticker_tp1:
                        
                        send_msg(f"تحقق هدف البيع للعملة   ==>${x}")#\n tp1 = {db_ticker_tp1}")            
                        signals.add('profit', dt, x, price_cal, db_ticker_tp1, db_ticker_SL,db_balance)
                        pl = (db_balance+fee)
                        
                        balance.append(pl)
                        signals.delete_one('buy', x)
                        

                    elif price_cal <= db_ticker_SL:             
                        send_msg(f"تم البيع على وقف الخسارة ==>${x}")             
                        signals.add('loss', dt, x, price_cal, db_ticker_tp1, db_ticker_SL,db_balance)
                        pl = (db_balance-fee)
                        balance.append(pl) 
                        signals.delete_one('buy', x)
                    else:
                        pass
                            
                            
            except:
                pass 

        try:

            buy_sell_balance= round(sum(balance),1)
            x = signals.free_balance('sellbalance')
            c = x+buy_sell_balance
            exitbalance =signals.free_balance('balance')
            # profitbalance = signals.free_balance('sellbalance')
            new_free_balance = exitbalance+buy_sell_balance
            # new_profit_balance = profitbalance+new_free_balance
            signals.add_balance('balance', new_free_balance)
            signals.add_balance('sellbalance', c)
        except:
            pass
       
         


def summary():
    try:

        ammount = signals.free_balance('balance')
        profitbalance = signals.free_balance('sellbalance')
        p = targetbalance(1500,profitbalance)
        numprofit = signals.num_table('profit')
        numloss = signals.num_table('loss')
        still = signals.num_table('buy')
        send_msg(f'اجمالي الرصيد الحالي : {ammount}\n اجمالي عدد الصفقات الناجحه: {numprofit} \n اجمالي عدد الصفقات الخاسرة : {numloss} \n مبلغ الربح : {profitbalance} \n عدد الصفقات المعلقه : {still}\n نسبة الربح من رآس المال % {p} \n \n ')
    except:
        pass   


def telegbot():
    try:
            
        @bot.message_handler(func=lambda message: True)
        def t_mer(message):
            
            text = message.text
            text = text.lower()
            chid = message.chat.id
            if text == "bl":
                bot.send_message(chid,"balance is ")
            elif text == "sum":
                bot.send_message(chid,f"{summary()}")
        
        bot.polling()
    except:
        pass




def infiniteloop1():
    while True:
        TA(usdt)
        ti.sleep(3)

def infiniteloop2():
    while True:
        track_price()
        ti.sleep(1)

def infiniteloop3():
    while True:
        telegbot()
        ti.sleep(1)


thread1 = threading.Thread(target=infiniteloop1)
thread1.start()

thread2 = threading.Thread(target=infiniteloop2)
thread2.start()

thread3 = threading.Thread(target=infiniteloop3)
thread3.start()

