from time import time
import pymongo
import certifi
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://anr466:Saif2019@cluster0.kprxp.mongodb.net/DB_Bot?retryWrites=true&w=majority" ,tlsCAFile=certifi.where())

db = client["DB_Bot"]




class signals:

    def add(col ,dt, tickers,price_now , tp):
        col = db[col]
        data = col.insert_one({"Time":dt , "Tickers":tickers,"price":price_now,"TP":tp})
        return data

    def clear_all(collection):
        collection = db[collection]
        collection.delete_many({})

    def find(col):
       
        col = db[col]
        find = col.find_one().keys()
        ticker = find['Tickers']
        
        # for i in find:
            
        #     ticker.append(i['Tickers'])
        #     ticker.append(i['price'])
                  
        return ticker
    def if_tickers_in(col ,tickers):
        col = signals.find(col=col)
        
        if tickers in col:
            print("found")
        else:
            print("not found")


# x = signals.find('buy')
# # tiker_name = coll[0]
# # price_db_tiker = coll[1]


# print(x)