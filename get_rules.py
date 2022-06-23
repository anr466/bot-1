"""
from time to time you have to delete "ticker_rules.py" file
and run this file to create new update to the rules
"""
from genericpath import exists
from binance_client import Clnt
import math
from pathlib import Path
import time
import os

path_to_file = 'ticker_rules.py'
path = Path(path_to_file)
rules = {}
info = Clnt.get_exchange_info()


if path.exists() == True:
    pass
else:

    for i in info["symbols"]:
        minPrice = int(round(-math.log(float(i["filters"][0]["minPrice"]), 10), 0))
        tickSize = int(round(-math.log(float(i["filters"][0]["tickSize"]), 10), 0))
        minQty = int(round(-math.log(float(i["filters"][2]["minQty"]), 10), 0))
        stepSize = int(round(-math.log(float(i["filters"][2]["stepSize"]), 10), 0))
        minNotional = float(i["filters"][3]["minNotional"])
        rules[i["symbol"]] = [minPrice, tickSize, minQty, stepSize, minNotional]

    with open('ticker_rules.py', 'x') as f:
        f.write('# 0 -- minPrice \n# 1 -- tickSize \n# 2 -- minQty \n# 3 -- stepSize \n# 4 -- minNotional \nrules = '+str(rules))
        print('updating')




