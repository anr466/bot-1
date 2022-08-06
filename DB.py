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
            tickers[x["Tickers"]] = [x["Tickers"],x["price"],x["TP1"],x["SL"]]
        if ticker in tickers:
            db_ticker.append(tickers[ticker])
        for x in db_ticker:
            for y in x:
                db_price.append(y)
        return db_price
    def find_all(coll):
        col = db[coll]
        find = col.find({})
        for x in find:
            print(x)
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
      
        return db_ticker
    def free_balance(col):
        col = db[col]
        find = col.find({})
        balance = {}
        ammount = []
        for x in find:
            balance[x["balance"]] = [x["balance"]]
        
        
        for x in balance:
            ammount.append(balance[x])
        return x 

        








# x = signals.free_balance('balance')
# print(x)


# y = signals.find(col, ticker)

