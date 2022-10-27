# import mplfinance as mpf
from get_data import get_klines 
import pandas_ta as ta
import numpy as np 
import matplotlib  
matplotlib.use('WebAgg')
import matplotlib.pyplot as plt
from ticker_rules import rules
import format_orders as fo
from DB import signals
import threading
import telebot
import requests
import time as ti
from datetime import datetime
# import os
from fun_fig import figure

bot_token = "5243412284:AAElbwcCDmKXOe4XTvG1F3EFdbDleAHH3ew"
bot = telebot.TeleBot(bot_token)
chat_id = "174958495"

def send_msg(text):
    url = "https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id="+chat_id+"parse_mode=Markdown&text="
    req = url+text
    response = requests.get(req)
    return response.json()


def send_photo(path):
    img = open(path, 'rb')

    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}'

    respon = requests.post(url, files={'photo': img})
    return respon.json()



def St_buy(ticker):


    #جمع مبلغ الشراء 
    entry = []

    for x in ticker:
        if x.endswith("USDT"):
            try:
                df = get_klines(x, '1m', '6 hour ago')

                if not df.empty:
                    

                                   
                    ###################################################################################
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
                
                for i in buy:
                    
                    if not np.isnan(i):
                        
                        buy_list = signals.buy_list()

                        if x not in buy_list:


                            


                            now = datetime.now()
                            dt = now.strftime("%d-%m-%y  %H:%M:%S")
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
                            balance = float(balance)

                            
                            free_blanace = balance - 50

                            print('free balance ' , free_blanace)
                            buy_amount = balance - free_blanace
                            print('buy amount' , buy_amount)

                            if free_blanace>=0 and buy_amount >= 10.5 :
                                buy = signals.buy_balance('balance',buy_amount)
                                signals.add_balance('balance',buy) 
                                balance = signals.free_balance('balance')
                                print(f'buy signal {x}')

                                #جمع عمليات الشراء
                                entry.append(buy_amount)




                                # f = figure(x)
                                # print(f)
                                
                                # ti.sleep(2)
                                # a = send_photo('buy.jpg')

                                send_msg(f' \n\n\n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${buy_amount}\n\nالرصيد المتبقي {balance}')
                                signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=buy_amount)
                                


                            # # تقسيم الرصيد
                            # new_balance1 = round(balance,2)
                            # new_balance2 = round((balance/2),2)
                            # new_balance3 = round((balance/3),2)
                            # new_balance4 = round((balance/4),2)
                            # new_balance5 = round((balance/5),2)
                            # new_balance6 = round((balance/6),2)
                            # new_balance7 = round((balance/7),2)
                            # new_balance8 = round((balance/8),2)
                            # new_balance9 = round((balance/9),2)
                            # new_balance10 = round((balance/10),2)

                            # if new_balance10 >= 10.5:

                                
                                # figure(x)
                                # ti.sleep(2)
                                # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance10)
                            #     signals.add_balance('balance',buy) 
                            #     balance = signals.free_balance('balance')
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance10}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance10)
                                


                            # elif new_balance9 >= 10.5:

                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance9)
                            #     signals.add_balance('balance',buy)
                            #     balance = signals.free_balance('balance')  
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance9}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance9)
                                

                            # elif new_balance8 >= 10.5:

                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance8)
                            #     signals.add_balance('balance',buy) 
                            #     balance = signals.free_balance('balance')                    
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance8}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance8)
                                

                            # elif new_balance7 >= 10.5:

                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance7)
                            #     signals.add_balance('balance',buy)
                            #     balance = signals.free_balance('balance')
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance7}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance7)
                                
                            
                            # elif new_balance6 >= 10.5:

                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance6)
                            #     signals.add_balance('balance',buy)
                            #     balance = signals.free_balance('balance')
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance6}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance6)
                                
                                
                            # elif new_balance5 >= 10.5:

                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance5)
                            #     signals.add_balance('balance',buy)
                            #     balance = signals.free_balance('balance')                 
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance5}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance5)
                                  
                                
                            # elif new_balance4 >= 10.5:

                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance4)
                            #     signals.add_balance('balance',buy)
                            #     balance = signals.free_balance('balance') 
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance4}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance4)
                                

                        
                            # elif new_balance3 >= 10.5:

                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance3)
                            #     signals.add_balance('balance',buy)
                            #     balance = signals.free_balance('balance')
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance3}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance3)
                                
                                
                            # elif new_balance2 >= 10.5:


                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance2)
                            #     signals.add_balance('balance',buy)
                            #     balance = signals.free_balance('balance')
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance2}\n\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance2)
                                
                                
                            # elif new_balance1 >= 10.5:

                            #     # figure(x)
                            #     # ti.sleep(2)
                            #     # send_photo('buy.jpg')
                            #     # ti.sleep(1)
                            #     # os.remove('buy.jpg')

                            #     buy = signals.buy_balance('balance',new_balance1)
                            #     signals.add_balance('balance',buy) 
                            #     balance = signals.free_balance('balance')
                            #     send_msg(f' \n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${new_balance1}\nالرصيد المتبقي {balance}')
                            #     signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=new_balance1)
                     
            except:
                pass
    q= round(sum(entry),1)
    r =signals.free_balance('entry')
    u = r+q
    signals.add_balance('entry', u)
    


def st_sell():
    # try:
            

        buy_list = signals.buy_list()

        balance = []

        free_balance = []

        all_exit_op = []

        all_entry_op = []

        for x in buy_list:
            

                    
                df = get_klines(x, '1m', '6 hour ago')

                if not df.empty:
                    # print(x)

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
                    print(x)

                    

                    for i in sell:
                                
                        if not np.isnan(i):

                        

                            print(f'sell signal {x}')

                            now = datetime.now()
                            dt = now.strftime("%d-%m-%y  %H:%M:%S")

                            #include Db buy ticker
                            db_ticker = signals.find('buy', x) 
                            db_buy_time = db_ticker[0]       
                            db_ticker_name = db_ticker[1]
                            db_ticker_price = db_ticker[2]
                            db_ticker_price= float(db_ticker_price)
                            db_ticker_tp1 = db_ticker[3]
                            db_ticker_tp1 = float(db_ticker_tp1)
                            db_ticker_SL = db_ticker[4]
                            db_ticker_SL = float(db_ticker_SL)
                            db_balance = db_ticker[5]
                            db_balance = float(db_balance)

                            

                            price_now = fo.get_ticker_price(x)

                            price_cal = fo.format_price(x , price_now)
                            price_cal = float(price_cal)

                            

                            # calculate earn money or loss
                            earn = round((price_now - db_ticker_price),1)
                            
                            # calculate earn money
                            profit = ((price_now * db_balance) / db_ticker_price)
                            profit_amount = round(profit,1)

                            loss_amount = round((db_ticker_price - price_now),1)

                            #calculate percantge earn money
                            ticker_pct = round(((earn / db_ticker_price) * 100),2)
                            loss_pct = round(((loss_amount / db_ticker_price) * 100),2)


                            # حساب نسبة الربح اعتماد للمبلغ
                            pct_amount = (((100*profit_amount)/db_balance) - 100)
                            pct_amount = round(pct_amount,2)


                            #حساب مبلغ البيع مع خصم العموله
                            fees = ((profit_amount*99.9)/100)
                            fees = round(fees,1)
                            #خصم مبلغ الشراء من مبلغ البيع مع العموله
                            amount_free = (fees - db_balance)
                            #صافي الربح
                            amount_free = round(amount_free,1)

                            


                            


                            
                            if price_now > db_ticker_price and profit_amount> db_balance:

                                if price_now > db_ticker_tp1:
                                    send_msg(f'تم البيع وتحقق الهدف للعملة : {x} \n سعر الشراء : {db_ticker_price} \n سعر البيع : {price_now} \n مبلغ الدخول : {db_balance} \n مبلغ الخروج : {fees} \n نسبة تغيير السعر : {pct_amount}% \n  المربح : {amount_free} \n  -------<-Target->--------\n' )

                                    #جمع الارباح 
                                    free_balance.append(amount_free)
                                    #مبلغ الخروج مع احتساب العموله
                                    balance.append(fees)

                                    all_entry_op.append(fees)
                                    
                                    signals.add('sell', dt, x, price_now, tp1 = db_ticker_tp1, sl=db_ticker_SL, amount=db_balance)

                                    signals.delete_one('buy', x)
                                else:

                                    print(f'sell signal {x}')

                                        
                                    # figure(x)
                                    # ti.sleep(2)
                                    # send_photo('buy.jpg')
                                    # ti.sleep(2)
                                    # os.remove('buy.jpg')

                                    send_msg(f'تم البيع الاستراتجية للعملة : {x} \n سعر الشراء : {db_ticker_price} \n سعر البيع : {price_now} \n مبلغ الدخول : {db_balance} \n مبلغ الخروج : {fees} \n نسبة تغيير السعر : {pct_amount}% \n  المربح : {amount_free} \n  -------<-Stratgy->--------\n' )
                                    signals.add('sell', dt, x, price_now, tp1 = db_ticker_tp1, sl=db_ticker_SL, amount=db_balance)

                                    #جمع الارباح 
                                    free_balance.append(amount_free)
                                    #مبلغ الخروج مع احتساب العموله
                                    balance.append(fees)

                                    signals.delete_one('buy', x)
            
        # جمع عمليات البيع تضاف الى الرصيد       
        buy_sell_balance= round(sum(balance),1)
        exitbalance =signals.free_balance('balance')
        new_free_balance = exitbalance+buy_sell_balance
        signals.add_balance('balance', new_free_balance)
        #جمع الارباح
        sum_free_balance = round(sum(free_balance),1)
        b = signals.free_balance('sumfree')
        a = round(b + sum_free_balance,1)
        signals.add_balance('sumfree', a)

    # except:
    #     pass




def summary():
    try:

        ammount = signals.free_balance('balance')
        still = signals.num_table('buy')
        sell = signals.num_table('sell')
        free = signals.free_balance('sumfree')
        profit = signals.free_balance('entry')
        sumprofit = (profit+free)
  
        send_msg(f' الرصيد المتاح : {ammount} \n  عمليات الشراء المعلقه : {still}\n  عمليات البيع المنفذه : {sell} \n\n المحفظة  :  {sumprofit}\n\n -----SELL----')
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
        try:
            St_buy(rules)
            ti.sleep(1)
        except:
            pass
        

def infiniteloop2():
    while True:
        try:
            st_sell()
            ti.sleep(1)
        except:
            pass
      
def infiniteloop3():
    while True:
        try:

            telegbot()
            ti.sleep(1)
        except:
            pass





def run():
    try:

        thread1 = threading.Thread(target=infiniteloop1)
        thread1.start()

        thread2 = threading.Thread(target=infiniteloop2)
        thread2.start()

        thread3 = threading.Thread(target=infiniteloop3)
        thread3.start()
    except:
        pass

run()
