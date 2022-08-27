from time import time
import pymongo
import certifi
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://anr466:Saif2019@cluster0.kprxp.mongodb.net/DB_Bot?retryWrites=true&w=majority" ,tlsCAFile=certifi.where())

db = client["DB_Bot"]




class signals:

    def add(col ,dt, tickers,price_now ,tp1,sl,amount):
        col = db[col]
        data = col.insert_one({"Time":dt , "Tickers":tickers,"price":price_now,"TP1":tp1,"SL":sl,"balance":amount})
        return data
    def add_balance(col ,amount):
        col = db[col]
        col.delete_many({})
        data = col.insert_one({"balance":amount})
        return data
    

    def clear_all(collection):
        collection = db[collection]
        collection.delete_many({})

    def find(col,ticker):
        col = db[col]
        find = col.find({})
        tickers= {}
        db_ticker = []
        db_price = []    
        for x in find:
            tickers[x["Tickers"]] = [x["Tickers"],x["price"],x["TP1"],x["SL"],x['balance']]
        if ticker in tickers:
            db_ticker.append(tickers[ticker])
        for x in db_ticker:
            for y in x:
                db_price.append(y)
        return db_price
    def find_all(coll):
        col = db[coll]
        find = col.find({},{'_id': False})
        xx = []
        for x in find:
            xx.append(x.values())
        return xx
    def delete_one(col , ticker):
        col = db[col]
        delete = col.delete_many( { "Tickers": f'{ticker}'} )
        return delete
    def num_table(col):
        col = db[col]
        find = col.find({})
        tickers= {}
        db_ticker = []  
        for x in find:
            tickers[x["Tickers"]] = [x["Tickers"]]
        for x in tickers:
            db_ticker.append(x)
        return len(db_ticker)

    def free_balance(col):
        col = db[col]
        find = col.find({})
        xbalance = {}
        balance = []
        for x in find:
            xbalance[x["balance"]] = [x["balance"]]
        for x in xbalance:
            balance.append(x)
        x = balance[0]
        x = round(x)
        return x
        
    def buy_balance(col,amount):
        amount = float(amount)
        col = db[col]
        find = col.find({})
        balance = {}
        ammount = []
        
        for x in find:
            balance[x["balance"]] = x["balance"]
        for y in balance:
            ammount.append(y)
        
        c = ammount[0]
        if c >=0:

            new_balance = (c-amount)
        return new_balance
    def buy_ticker(col,ticker):
        col = db[col]
        data = col.insert_one({"ticker":ticker})
        return data

    def tracking_ticker(col,ticker):
        col = db[col]
        find = col.find({})
        balance = {}
        ammount = []
        buy_list = []
        for x in find:
            balance[x["ticker"]] = x["ticker"]
        for y in balance:
            ammount.append(y)
        
        return ammount
        
    def buy_list():
        col = db['buy']
        find = col.find({},{'_id': False})
        buylist= []
        for x in find:
            buylist.append(x.get('Tickers'))
        
        return buylist



# x = signals.buy_list()
# print(x)




# signals.buy_ticker('buytik','xxxx')
# x = signals.tracking_ticker('buytik', 'BTCUSDT')
# print(x)



# x= signals.find_all('buy')
# print(x)
# signals.clear_all('buy')
# signals.clear_all('profit')
# signals.clear_all('loss')
# signals.clear_all('balance')
# # # # # h = signals.buy_balance('balance',15)

# signals.add_balance('balance',150)
# signals.add('profit', '2344', 'btc', '5', '5', '5', '10')
# signals.add('profit', '2344', 'eth', '5', '5', '5', '10')
# signals.add('profit', '2344', 'ada', '5', '5', '5', '10')
# signals.delete_one('profit', 'btc')

# signals.add_balance('balance', 1500)
# s= signals.free_balance('balance')

