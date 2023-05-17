from multiprocessing import Condition
import yfinance as yf
import mplfinance
from exchanges.binance import Binance
from tradingview_ta import TA_Handler, Interval, Exchange
import threading
from threading import Thread
import asyncio
import socket
import time
from MA_start import __MA_strategy__
import json

from utils.constants import OSCILATORS, MOVING_AVEREGES, VALUES_LIST
import redis
from db import worker_data


"""
@HERMES PATIENT
"""



exchange_dict = {
    'Binance': Binance
}


async def client(client_socket, adress):
    print(client_socket)
    print(adress)
    data = str(client_socket.recv(1024).decode('utf-8'))
    """
    получаем список стратегии элементы фиксированы и сплитятся из меседжа через :
    элементы по порядку [id session, валютная пара, БИРЖА;ДАННЫЕ, таймфрейм, индикатор, условие]
    в индикаторе определяется род индикатора(осцилятор,среднее или уровневый(pivot))
    условия фиксированы в конструкторе на сайте larger/greater than, increase/decrease by, crossing below/above.
    """
    data_list = data.split(':')
    print(data_list)

    COIN_MODE = False

    COINS_LIST = json.loads(str(data_list[0]))
    print('sds')
    #if symbol == 'ANY_OF_COINS':
    #    COIN_MODE = True
    service = str(data_list[1]).split(';')[0]
    api_key = (str(data_list[1]).split(';')[1]).split('||')[0]
    api_secret = (str(data_list[1]).split(';')[1]).split('||')[1]
    condition = str(data_list[2])
    test_mode_status = str(data_list[3])
    trailing_stoploss = str(data_list[4])
    simple_stoploss = str(data_list[5])
    futures = str(data_list[6])
    spot = str(data_list[7])
    id_session = str(data_list[-1])
    conditions_list = condition.split('(—->)')
    print(conditions_list)

    print(service, condition, api_key, api_secret)

    for key in range(len(list(exchange_dict.keys()))):
        try:
            print(list(exchange_dict.keys())[key])
            if list(exchange_dict.keys())[key] == str(service):
                exchange = exchange_dict[service]
            else:
                continue
        except Exception as e:
            print(e)
            print('THERE IS NO EXCHANGE IN LIST!')
    
    __data = ''
    restart = False
    symbol_list = []
    __result = ''

    

    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    test_mode_status_inter = test_mode_status.split('(')[1].split(')')[0]
    if test_mode_status_inter == 'True':
        balance = float(test_mode_status.split('[')[1].split(']')[0])
        print(balance)
        redis_client.set(name=f"{id_session}_balance", value = balance)
        
    threading.Thread(target=worker_data, args=(COINS_LIST, 
                                                redis_client, 
                                                id_session, 
                                                exchange, 
                                                api_key, 
                                                api_secret, 
                                                conditions_list, 
                                                client_socket, 
                                                test_mode_status, trailing_stoploss, simple_stoploss, futures, spot, __MA_strategy__)).start()



def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def runner():

    server =socket.create_server(('127.0.0.1', 8020))
    server.listen()
    print('SERVER RUN!')
    loop = asyncio.new_event_loop()
    threading.Thread(target=run_loop, args=(loop,)).start()

    while True:
        try:
            print('WAITING FOR INCOMING CONNECTIONS!')
            client_socket, adress = server.accept()
            #name = client_socket.recv(1024).decode('utf-8')
            asyncio.run_coroutine_threadsafe(client(client_socket, adress), loop)
            #time.sleep(0.05)
        except Exception as e:
            print(f'Error {e}')

runner()