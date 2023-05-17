import requests

from binance.client import Client
from binance import BinanceSocketManager
import pandas as pd
import time
import ta
import matplotlib.pyplot as plt

class Binance():

    def __init__(self, apikey, secretkey):

        self.client = Client(apikey,secretkey)
    
    def gethistory(self, symbol, timeframe, period):
        df = pd.DataFrame(self.client.get_historical_klines(symbol, f'{timeframe}',
                                                        f'{str(period)} UTC'))
        closes = pd.DataFrame(df[4])
        closes.columns = ['Close']
        graph = closes['Close'].iloc[-1]
        close_list = closes['Close'].tolist()
        closes.dropna(inplace=True)

        return close_list, graph
    
    @staticmethod
    def getstr():
        return 'Binance'
    
    def close_spot(self):
        print('CLOSING SPOT POSITION!')
    
    def close_futures(self):
        print('CLOSING FUTURES POSITION!')
    
    def trading_socket(self, coin):
        return BinanceSocketManager(self.client).trade_socket(coin)
    
    def spotbuy(self):
        print('BUYING ON SPOT')

    def spotsell(self):
        print('BUYING ON SPOT')

    def buy(self):
        print('BUYING')

    def sell(self):
        print('SELLING')



