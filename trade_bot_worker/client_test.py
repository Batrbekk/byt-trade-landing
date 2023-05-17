import socket
import time
from utils.tradingview import TradingViewApi
import random


TradingView = TradingViewApi('BINANCE','BTCUSDT')

print(TradingView.get_simple_moving_average_5())

api_key = 'PgaQ2HM8KAdrzs0sBvIr9a7Ouj3y4cIgfm0OlSyZC0n25mqk366tH2s34oK5DO3i'
api_secret = 'vMaiFNS4pleBcKqjXhFGTyF4BZDOMst4ay5K4JWGGVN6o4qxsl7E1EuPUtjlr4eS'

def get_hash():
    import hashlib

    str2hash = ''

    for k in range(random.randint(5,9)):
        str2hash += str(random.randint(1,9))
    
    result = hashlib.md5(str2hash.encode())
    
    print("The hexadecimal equivalent of hash is : ", end ="")
    print(result.hexdigest())

    return result.hexdigest()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect (
    ('127.0.0.1', 8020)
)
client.send(f'[["BTCUSDT"]]:Binance;{api_key}||{api_secret}:["1m"];if MA(7) > MA(25) -> BUY(BTCUSDT) (—->) ((GET)) ["1m"];if EMA(20) >= MA(5) -> BUY(BTCUSDT):TESTMODE(True)[100000]:TRAILING_STOPLOSS(True,0.0003):SIMPLE_STOPLOSS(False,-0.0001,0.0005):FUTURES(True,6,1000):SPOT(False,10000):{str(get_hash())}'.encode('utf8'))
i = 0
while i < 100000:
    data = client.recv(1024)
    print(data)
    if data == b'':
        break
    i += 1
    time.sleep(0.5)

client.close()

