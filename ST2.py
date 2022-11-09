# import mplfinance as mpf
from get_data import get_klines ,RSI
import pandas_ta as ta
import numpy as np 
from ticker_rules import rules
import format_orders as fo
from DB import signals,rest
from telegram import send_msg,send_photo,bot,chat_id
import time as ti
from datetime import datetime
from tradingview_ta import TA_Handler, Interval, Exchange
from top_volume import top_10





def St_buy(ticker):


    for x in ticker:
            try:
            
                df = get_klines(x, '15m', '4 hour ago')
             
                if not df.empty:                    
                    
                    
                    coins = TA_Handler()
                    coins.set_symbol_as(x)
                    coins.set_exchange_as_crypto_or_stock('Binance')
                    coins.set_screener_as_crypto()
                    coins.set_interval_as(Interval.INTERVAL_2_HOURS)
                    summary = (coins.get_analysis().summary)
    
                    rsi_fun = RSI(df)
                    rsi_fun = rsi_fun[-1]
                    rsi_fun = round(rsi_fun,1)

                    


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
      
                    buy_list = signals.buy_list('buy')
                    pump_list = signals.buy_list('pump')

                    

                    if x not in buy_list and x not in pump_list:

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
                        balance = float(balance) # 1000 

                        free_blanace = (balance - 50)

                        buy_amount = balance - free_blanace
                        buy_amount = float(buy_amount)

                        if summary['RECOMMENDATION'] == "STRONG_BUY" and free_blanace > 0.0 and buy_amount >= 10.5 and rsi_fun > 70:
                            ti.sleep(1)
                            buy = signals.buy_balance('balance',buy_amount)
                            signals.add_balance('balance',buy) 
                            balance = signals.free_balance('balance')

                            # figure(x)
                            # ti.sleep(2)
                            # send_photo('buy.jpg')
                            send_msg(f' \n\n\n\n (----->pump<----) \n\n شراء==> ${x} \nالسعر الحالي==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${buy_amount}\n\nالرصيد المتبقي {balance}')
                            
                            signals.add('pump', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=buy_amount)
                        else:
                            for i in buy:
                                if not np.isnan(i):
                                    if x in top_10:
                                        if free_blanace > 0.0 and buy_amount > 10.5:
                                            buy = signals.buy_balance('balance',buy_amount)
                                            signals.add_balance('balance',buy) 
                                            balance = signals.free_balance('balance')
                                            # figure(x)
                                            # ti.sleep(2)
                                            # send_photo('buy.jpg')
                                            send_msg(f' \n \n\n\n (----->top_volume<----) \n\n شراء==> ${x} \nسعر الشراء ==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${buy_amount}\n\nالرصيد المتبقي {balance}')
                                            
                                            signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=buy_amount)
                                    else:
                                        if free_blanace > 0.0 and buy_amount > 10.5:
                                            buy = signals.buy_balance('balance',buy_amount)
                                            signals.add_balance('balance',buy) 
                                            balance = signals.free_balance('balance')
                                            # figure(x)
                                            # ti.sleep(2)
                                            # send_photo('buy.jpg')
                                            send_msg(f' \n \n\n\n (----->BB_stratgy<----) \n\n شراء==> ${x} \nسعر الشراء ==> {price_now} \nالوقت==> {timestap[0]} \nالهدف==> {tp1}\nوقف الخسارة==> {stopprice}\n مبلغ الشراء ==>${buy_amount}\n\nالرصيد المتبقي {balance}')
                                            
                                            signals.add('buy', dt=dt,tickers= x,price_now= price_now,tp1= tp1,sl= stopprice,amount=buy_amount)

            except:
                pass


def sell_pump():
    try:
    
        buy_list = signals.buy_list('pump')

        balance = []

        free_balance = []

        all_exit_op = []

        all_entry_op = []

        for x in buy_list:

                df = get_klines(x, '5m', '4 hour ago')

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
                    # print(df)        

                    for i in sell:
                                
                        if not np.isnan(i):

                            now = datetime.now()
                            dt = now.strftime("%d-%m-%y  %H:%M:%S")

                            #include Db buy ticker
                            db_ticker = signals.find('pump', x) 
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

                            # وقت البيع 
                            for c in df['Close'].index:
                                timestap = []
                                timestap.append(c)

                            #حساب مبلغ البيع مع خصم العموله
                            fees = ((profit_amount*99.9)/100)
                            fees = round(fees,1)
                            #خصم مبلغ الشراء من مبلغ البيع مع العموله
                            amount_free = (fees - db_balance)
                            #صافي الربح
                            amount_free = round(amount_free,1)

                            

                            if price_now > db_ticker_price and fees > db_balance:

                                if price_now > db_ticker_tp1:
                                    send_msg(f' \n\n pump \n \n تم البيع وتحقق الهدف للعملة  : {x} \n سعر الشراء : {db_ticker_price} \n سعر البيع : {price_now} \n مبلغ الدخول : {db_balance} \n مبلغ الخروج : {fees} \n الوقت : {timestap[0]}\n نسبة تغيير السعر : {pct_amount}% \n  المربح : {amount_free} \n  -------<-Target->--------\n' )

                                    #جمع الارباح 
                                    free_balance.append(amount_free)
                                    #مبلغ الخروج مع احتساب العموله
                                    balance.append(fees)
   
                                    signals.add('sell', dt, x, price_now, tp1 = db_ticker_tp1, sl=db_ticker_SL, amount=db_balance)

                                    signals.delete_one('pump', x)
                                else:
                                    send_msg(f' \n\n pump \n \n تم البيع خروج للعملة  : {x} \n سعر الشراء : {db_ticker_price} \n سعر البيع : {price_now} \n مبلغ الدخول : {db_balance} \n مبلغ الخروج : {fees} \n الوقت : {timestap[0]}\n نسبة تغيير السعر : {pct_amount}% \n  المربح : {amount_free} \n  -------<-Target->--------\n' )

                                    #جمع الارباح 
                                    free_balance.append(amount_free)
                                    #مبلغ الخروج مع احتساب العموله
                                    balance.append(fees)
   
                                    signals.add('sell', dt, x, price_now, tp1 = db_ticker_tp1, sl=db_ticker_SL, amount=db_balance)

                                    signals.delete_one('pump', x)                                   
                              

                            
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
    except:
        pass

    



def st_sell():
    try:
    
        buy_list = signals.buy_list('buy')

        balance = []

        free_balance = []

        all_exit_op = []

        all_entry_op = []

        for x in buy_list:

                df = get_klines(x, '15m', '4 hour ago')

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
                    # print(x)        

                    for i in sell:
                                
                        if not np.isnan(i):

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

                            # وقت البيع 
                            for c in df['Close'].index:
                                timestap = []
                                timestap.append(c)

                            #حساب مبلغ البيع مع خصم العموله
                            fees = ((profit_amount*99.9)/100)
                            fees = round(fees,1)
                            #خصم مبلغ الشراء من مبلغ البيع مع العموله
                            amount_free = (fees - db_balance)
                            #صافي الربح
                            amount_free = round(amount_free,1)

                            if price_now > db_ticker_price and fees > db_balance:

                                if price_now > db_ticker_tp1:
                                    send_msg(f'تم البيع وتحقق الهدف للعملة : {x} \n سعر الشراء : {db_ticker_price} \n سعر البيع : {price_now} \n مبلغ الدخول : {db_balance} \n مبلغ الخروج : {fees} \n الوقت : {timestap[0]}\n نسبة تغيير السعر : {pct_amount}% \n  المربح : {amount_free} \n  -------<-Target->--------\n' )

                                    #جمع الارباح 
                                    free_balance.append(amount_free)
                                    #مبلغ الخروج مع احتساب العموله
                                    balance.append(fees)
   
                                    signals.add('sell', dt, x, price_now, tp1 = db_ticker_tp1, sl=db_ticker_SL, amount=db_balance)

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

    except:
        pass


def still_buy():
    try:

        pumpbuy = []
        bb_buy = []


        buy_list1 = signals.buy_list('pump')
        buy_list2 = signals.buy_list('buy')

        for x in buy_list2:
            db_ticker = signals.find('buy', x)
            db_ticker_name = db_ticker[1]
            db_ticker_price = db_ticker[2]
            f = (db_ticker_name , ' : ' , db_ticker_price)
            bb_buy.append(f)
        
        for x in buy_list1:
            db_ticker = signals.find('pump', x)
            db_ticker_name = db_ticker[1]
            db_ticker_price = db_ticker[2]
            f = (db_ticker_name , ' : ' , db_ticker_price)
            pumpbuy.append(f)

        x= ('\n'.join([ str(myelement) for myelement in pumpbuy ]))
        y= ('\n'.join([ str(myelement) for myelement in bb_buy ]))
        send_msg(f' العملات الحالية مع سعر الشراء: \n \n pump buy : {x} \n \n bb startgy: {y}')
    except:
        pass   



def summary():
    try:
        ammount = signals.free_balance('balance')
        still = signals.num_table('buy')
        pump = signals.num_table('pump')
        sell = signals.num_table('sell')
        free = signals.free_balance('sumfree')
        send_msg(f' الرصيد المتاح : {ammount} \n  BB \n عمليات الشراء المعلقه لااستراتجية: {still} \n pump \n عمليات الشراء المعلقه لااستراتجية: {pump}\n  عمليات البيع المنفذه : {sell} \n\n المربح  :  {free}\n\n\n -----<-Summary->----')
    except:
        pass   


def telegbot():
    try:

        @bot.message_handler(func=lambda message: True)
        def t_mer(message):    
            text = message.text
            text = text.lower()
            chid = message.chat.id
            if text == "buy":
                bot.send_message(chid,f"{still_buy()} ")
            elif text == "sum":
                bot.send_message(chid,f"{summary()}")
            elif text == "cl":
                bot.send_message(chid,f"{rest()}")
        bot.polling()
    except:
        pass




