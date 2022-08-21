# import binance.threaded_stream
# import datetime
# import ssl


# def on_message(ws, message):
#     print()
#     print(str(datetime.datetime.now()) + ": ")
#     print(message)

# def on_error(ws, error):
#     print(error)

# def on_close(close_msg):
#     print("### closed ###" + close_msg)



# kline = {}



# kline = {}


# def spd(msg):
# 	"""
# 	{
# 		"E": 1499404907056,				# event time
# 		"s": "ETHBTC",					# symbol
# 		"k": {
# 			"t": 1499404860000, 		# start time of this bar
# 			"T": 1499404919999, 		# end time of this bar
# 			"s": "ETHBTC",				# symbol
# 			"i": "1m",					# interval
# 			"f": 77462,					# first trade id
# 			"L": 77465,					# last trade id
# 			"o": "0.10278577",			# open
# 			"c": "0.10278645",			# close
# 			"h": "0.10278712",			# high
# 			"l": "0.10278518",			# low
# 			"v": "17.47929838",			# volume
# 			"n": 4,						# number of trades
# 			"x": false,					# whether this bar is final
# 			"q": "1.79662878",			# quote volume
# 			"V": "2.34879839",			# volume of active buy
# 			"Q": "0.24142166",			# quote volume of active buy
# 			"B": "13279784.01349473"	# can be ignored
# 			}
# 	}
# 	"""

# 	kline[msg["s"]] = msg["k"]["c"]



# def streamKline(currency,spd, interval):
#     websocket.enableTrace(False)
#     socket = f'wss://stream.binance.com:9443/ws/{currency}@kline_{interval}'
    

    

#     ws = websocket.WebSocketApp(socket,
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)
#     ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    

# tickers = ["BTCUSDT", "ADAUSDT", "LTCUSDT"]
# for ticker in tickers:
# 	streamKline(ticker, spd, "1m")


# streamKline('solusdt', '1m')

