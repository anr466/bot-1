import requests

def find_len(num):
    try:
        if int(num[0]) >= 1:
            lenn = 0
        else:
            if "." in num:
                try:
                    if num[2] == "1":
                        lenn = 1
                except Exception:
                    pass
                try:
                    if num[3] =="1":
                        lenn =2
                except Exception:
                    pass


                try:
                    if num[4] =="1":
                        lenn =3
                except Exception:
                    pass

                try:
                    if num[5] =="1":
                        lenn =4
                except Exception:
                    pass

                try:
                    if num[6] =="1":
                        lenn =5
                except Exception:
                    pass

                try:
                    if num[7] =="1":
                        lenn =6
                except Exception:
                    pass
                try:
                    if num[8] =="1":
                        lenn =7
                except Exception:
                    pass

                try:
                    if num[9] =="1":
                        lenn =8
                except Exception:
                    pass
        return lenn
    except Exception:
        pass
     
url = "https://api.binance.com/api/v1/exchangeInfo"


r = requests.get(url).json()
symbols = r["symbols"]
rules = {}
rr = []
ticksss = []
for i in symbols:
    ticker = i["symbol"]
    ticksss.append(ticker)
    ticker_list = []
    filters = i["filters"]
    for fil in filters:
        if fil["filterType"] == "PRICE_FILTER":
            minPrice = fil["minPrice"]
            ticker_list.append(find_len(minPrice))
            tickSize = fil["tickSize"]
            ticker_list.append(find_len(tickSize))
        if fil["filterType"] == "LOT_SIZE":
            minQty = fil["minQty"]
            ticker_list.append(find_len(minQty))
            stepSize = fil["stepSize"]
            ticker_list.append(find_len(stepSize))
        if fil["filterType"] == "LOT_SIZE":
            minNotional = fil["minQty"]
            
            ticker_list.append(float(minNotional))
    rules[ticker]=ticker_list
    


with open('ticker_rules.py', 'x') as f:
    f.write('# 0 -- minPrice \n# 1 -- tickSize \n# 2 -- minQty \n# 3 -- stepSize \n# 4 -- minNotional \nrules = '+str(rules))


