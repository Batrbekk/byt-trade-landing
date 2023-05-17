import redis
import time
import threading 
from threading import Thread
from exchanges.binance import Binance


def delete_session_data(val_list, redis_client, id_session):
    for _ in range(len(val_list)):
        print(f'DELETING {val_list[_]}')
        redis_client.delete(f"{val_list[_]}_{id_session}")
        redis_client.delete(f"{val_list[_]}_{id_session}_additional_condition")
        redis_client.delete(f"{id_session}_balance")

def db_worker(pair, redis_client, id_session, exchange, timeframe, api_key, api_secret):

    __crypto = exchange(api_key, api_secret)
    print(__crypto)

    while True:

        try:
            timeframe_value = timeframe[-1]
            history, livegraph = __crypto.gethistory(pair, timeframe, ('500' + timeframe_value))
            for i in range(len(history)):
                history[i] = float(history[i])
            lisst = [float(livegraph), history]

            status = redis_client.set(name=f"{pair}_{id_session}", value=f"{lisst}", xx=True)
            if status == None:
                break
        except Exception as ex:
            print(ex)

def worker_data(pair, redis_client, id_session, exchange, timeframe, api_key, api_secret, conditions_list, client_socket, test_mode_status: str, trailing_stoploss, simple_stoploss, futures, spot, CONSTRUCTOR):

    __crypto = exchange(api_key, api_secret)
    print(__crypto)
    __result = 0 
    redis_client.set(name=f"{pair}_{id_session}_additional_condition", value = 'False')

    symbol_list = [pair]

    threading.Thread(target=db_worker, args=(pair, redis_client, id_session, exchange, timeframe, api_key, api_secret)).start()

    """ЖДЕМ ПЕРВЫХ ДАННЫХ 
       О ВАЛЮТНОЙ ПАРЕ В REDIS
    """
    time.sleep(4) 

    while True:
        stop = False
        try:
            for _ in range(len(conditions_list)):

                if stop == True:
                    break

                while True:

                    if '((' in conditions_list[_]:
                        prefix = str(conditions_list[_]).split('((')[1].split('))')[0]
                        print(f'{prefix} {__data}')
                        if __data == prefix:
                            inter = '((' + prefix + '))'  
                            __result = CONSTRUCTOR(symbol_list, exchange, timeframe, str(conditions_list[_]).replace(inter,'').strip(), api_key, api_secret, client_socket, id_session, redis_client, test_mode_status, trailing_stoploss, simple_stoploss, futures, spot)
                            restart = False
                            if __result == 200:
                                print('STRATEGY DID NOT MATCH!')
                                continue
                            if __result == 400:
                                raise Exception("CLIENT DISCONNECT!")
                            elif '|' in __result:
                                __data_list = str(__result).split('|')
                                __data = __data_list[-1]
                                print(f'STATUS OF LAST BET {__data}')
                                break
                        else:
                            restart = True
                    else:
                        restart = True
                    print('STOP!')

                    if restart == True and _ > 0:
                        stop = True
                        break
                    else:
                        __result= CONSTRUCTOR(symbol_list, exchange, timeframe,  str(conditions_list[_]).strip(), api_key, api_secret, client_socket, id_session, redis_client, test_mode_status, trailing_stoploss, simple_stoploss, futures, spot)
                        if __result == 200:
                            print('STRATEGY DID NOT MATCH!')
                            continue
                        if __result == 400:
                            raise Exception("CLIENT DISCONNECT!")
                        elif '|' in __result:
                            __data_list = str(__result).split('|')
                            __data = __data_list[-1]
                            print(f'STATUS OF LAST BET {__data}')
                            break

                    time.sleep(1)

                    """
                    if '&' in condition:
                        new_condition = condition.split('&')[1]
                        if '-$' in new_condition:
                            if float(__data_list):
                                print('d')

                    if float(__data_list[5]) < 0:
                        client_socket.send(datanext.encode('utf-8'))
                    """
        
                    #print('STOP2!')

                    #datanext = 'SOME DATA!'
                    #client_socket.send(datanext.encode('utf-8'))
                    #time.sleep(0.5)

        except Exception as ex:
            print(ex)
            delete_session_data(symbol_list, redis_client, id_session)
            if __result != 400:
                client_socket.send('ERROR APPEAR PLS RESTART STRATEGY!'.encode('utf-8'))
            break

