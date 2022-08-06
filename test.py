# import get_rules
# from ticker_rules import rules
# import format_orders as fo
# import os

# tickers = []
# minPrice = []
# tickSize = []
# minQty = []
# stepSize = []
# minNotional = []
# # price_ticker = fo.get_ticker_price()
# for i in rules:
#      tickers.append(i) 
#      minPrice.append(rules[i][0])
#      tickSize.append(rules[i][1])
#      minQty.append(rules[i][2])
#      stepSize.append(rules[i][3])
#      minNotional.append(rules[i][4])

# # ظبط سعر كل عمله ظمن قواعد باينانس مثلا السعر : 4.34534345345 يصبح : 4.3453
# #fo.format_price()

# # ظبط الكميه المدخله لكل عمله ظمن قواعد باينانس مثلا الكميه : 4.34534345345 يصبح : 4.3453
# #fo.format_quantity()


# # قل قيمه مسموح لك بيعها مقابل  USDT 10$
# #true or false .. trure if > 10$ else false
# #fo.check_min_notional()
# # examples when you want sell 
# # istrue = fo.check_min_notional(tickers,quantity)
# # if istrue:
# #     print("sell secssfully")
# # else:
# #     print(" cant sell bucuase quantity under 10$")



# #get your free balance in usdt you can used in buy
# # fee = 0.075 # BNB
# # -0.1% trading fee
# # -0.5% Instant Buy/Sell fee
# # -25% if using Binance coin
# # balance = fo.get_usdt_balance(fee)
# # print(balance)
# #  بالتساوي تقسيم الرصيد
# # aomnt = []
# # quote = 4 #تقسيم السعر على 4
# # for i in rang(quote):
# #     aomnt.append(balance / quote)
# # شراء بالرصيد المقسم بعد التقسيم 
# # for i in aomnt:
# #     print("buy" , i )
# #     #buy orders



# #  الحصول علي كمية العمله بعد الشراء مع خصم العموله
# # fee = 0.15
# # tiker = "SHIBUSDT"
# # تقسيم الكميه على ٣٠ ومعرفة اذا كان مسموح البيع بمعنى الكميه تعادل ١٠ دولار واكثر
# # for i in range(30):
# #     x = 30 - i

# #     quantity = fo.get_token_balance(tiker,fee)
# #     quantity = quantity / x
# #     quantity = fo.format_quantity(tiker , quantity / x)
# #     istrue = fo.check_min_notional(tiker,quantity)
# #     if istrue:
# #         print("sell secssfully" , x )
# #         #sell orders
# #     else:
# #         print(" cant sell bucuase quantity under 10$" , x )




# # # تحديد الاهداف والنسب للبيع 
# # symbol = "SHIBUSDT"
# # fee = 0.15
# # #price_now = price symbol now

# # # تحديد سعر العمله بالميه بيع عند السعر اذا ارتفع ٥٪ وبيع عند ١٠٪ وبيع عند ١٥٪ وهكذا
# # # target = tp1 5% , tp 10% , tp3 15%
# # target = fo.price_calculator(symbol , price_now , tp1= 5 , tp2 = 10 , tp3 = 15)
# # # تحديد كم الكمية من العمله المراد بيعها عند الاهداف 
# # # on tp1 sell 40% of quantity , on tp2 sell 30% on tp3 sell 30% and sell all quantity tp4 = "*"
# # quantity = fo.get_token_balance(symbol,fee) # get quantity 
# # quantities = fo.quantity_calculator(symbol , quantity , tp1 = 40 , tp2= 30 , tp3 = 30)

# # for i in target:
# #     print("sell quantity",quantities[i] ," & " ,target[i], "vs USDT")






# # #تحديد اهداف الشراء 
# #symbol = "SHIBUSDT"
# # fee = 0.15
# # #price_now = price symbol now
# #price_now = fo.get_ticker_price(symbol)

# # balance = fo.get_usdt_balance(fee)
# # تحديد سعر العمله بالميه شراء عند السعر اذا نزل ٥٪ ونزل عند ١٠٪ ونزل عند ١٥٪ وهكذا
# # target = tp1 5% , tp 10% , tp3 15%
# #target = fo.price_calculator(symbol , price_now , tp1 =3)
# # #تقسيم الشراء
# # new_balance = balance / 4
# # for i in target:
# #     if new_balance > 10.5:
# #         #buy limit orders

# #         print("buy ",new_balance[i] ," >> " ,target[i], " USDT")
# #     else:
# #         print("error")



# # #get new balance quantity examples : if you buy with balance 20$ how much quantity you get it
# # quantity = fo.buy_market_quantity(symbol , new_balance)
# # print(balance)
# # print(new_balance)
# # print(quantity)
# # #exapmels .. if you want to buy evry time with 20$ each symbol 
# # usdt = 20
# # symbol = "BTTUSDT"
# # quantity = fo.buy_market_quantity(symbol , usdt)
# # print(usdt)
# # print(quantity)
# # # another exampels if we have many symbol like : ["ADAUSDT" , "BTCUSDT" , "CHZUSDT", "BTTUSDT" , "BNBUSDT" , "ETHUSDT"]
# # # how much quantity with 20$ each symbol
# # symbol = ["ADAUSDT" , "BTCUSDT" , "CHZUSDT", "BTTUSDT" , "BNBUSDT" , "ETHUSDT"]
# # for i in symbol:
# #     quantity = fo.buy_market_quantity(i , usdt)
    
# #     print(usdt , i , quantity)     


# # تثبيت اوامر الشراء عند اسعار محدده 
# # symbol = "ADAUSDT"
# # usdt = 20 
# # price_now = fo.get_ticker_price(symbol)
# # # شراء بقيمة ٢٠$ عند نزول العمله لاهداف محدده
# # buy_limit = fo.price_calculator(symbol,usdt, tp1 = -5 , tp2 = -10 ,tp3 = -15)

# # for i in buy_limit:
# #     quantity = fo.buy_limit_quantity(symbol,usdt,buy_limit[i])
# #     #تثبيت امر الشراء 
# #     # buy_limit_orders = fo.execute_buy_limit_order(symbol , usdt, buy_limit[i])
# #     print("buy" , usdt , "$ in " , symbol , "quntity" ,quantity )



# # # اذا تبي تشتري مباشرة من عمله معينه 
# # ticker = "BTTUSDT"
# # amount = 20
# # detail = fo.execute_buy_market_order(ticker , amount)
# # #لمعرفة السعر الشراء بعد تنفيذ امر الشراء
# # price_buy = detail['price']




# # #اذا تبي تبيع كميه محدده من العمله مباشرة  
# # ticker = "BTTUSDT"
# # fee = 0.15
# # amount = 20
# # quantity = fo.get_token_balance(ticker, fee)
# # print(quantity)
# # quantity = fo.quantity_calculator(ticker,quantity, tp1 = 50 , tp2 = 50)# يتم بيع ٥٠٪ بالميه من الكميه لديك
# # for k in quantity:
# #     print("sell quantity", quantity[k])
# #     #order sell quantity 
# #     # fo.execute_sell_market_order(ticker,quantity[k])

# # tiker = 'CTKBTC'
# # price_now = fo.get_ticker_price(tiker)
# # price_cal = fo.format_price(tiker , price_now)

# # print(price_cal)
                    


# x = "ADAUSDT"
# price_now = fo.get_ticker_price(x)
# price_cal = fo.format_price(x , price_now)

# target = fo.price_calculator(x , price_now , tp1 =2.5 ,tp2 =5)
# profit = list(target.values())[0]
# #buy order


# #sell order


# target = list(target.values())[0]


# #tel.send_msg(f'Strong buy for: {x} \nprice now is : {price_cal}\n target {target}')

# # b = []
# # def balance_profit(amount,fee):
# #     bb = amount+fee
# #     b.append(bb)
# #     return sum(b)
# # def balance_loss(amount,fee):
# #     bb = amount-fee
# #     b.append(bb)
# #     return sum(b)
         

# from DB import signals




# balance = signals.free_balance('balance')
# balance = float(balance)

# new_balance = round((balance/6),2)


# print(new_balance)