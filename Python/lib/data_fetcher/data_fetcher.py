import websocket
import time
import numpy as np
import json

# Finnhub API key
api_key = "bt629rv48v6vp4gagf90"

class Stock:
	def __init__(self, name):
		self.name = name
		self.value = np.nan
		self.timestamp = np.nan
		self.prev_val = np.nan
		self.change = np.nan
		self.change_history = np.array([])

	def update(self, value, timestamp, volume):
		if np.isnan(self.value):
			self.change = value - self.prev_val
			self.prev_val = value
			print("%s is now at %f, last was %f" % (self.name, value, self.prev_val))

		self.value = value
		self.timestamp = timestamp

stock_list = ["TSLA", "AAPL", "GOOGL", "MSFT"]
stock_map = {}


def on_message(ws, message):
	if "data" in message:
		message_as_dict = json.loads(message)
		data = message_as_dict['data'][0]
		symbol = data["s"]
		timestamp = data["t"]
		value = data["p"]
		volume = data["v"]
		stock_map[symbol].update(value, timestamp, volume)

def on_error(ws, error):
	print(error)

def on_close(ws, close):
	print("Shutting down connection.")

def on_open(ws):
	for i in range(0, len(stock_list)):
		symbol = stock_list[i]
		stock_map[symbol] = Stock(symbol)
		ws.send('{"type":"subscribe","symbol":"%s"}' % symbol)

if __name__ == '__main__':
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=%s" % api_key,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()
