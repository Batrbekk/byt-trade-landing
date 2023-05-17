import os.path
import sys
from tkinter import OFF

import pandas as pd
import time
from exchanges.binance import Binance
import asyncio
from helpers.Indicators_math import MA, compare, upper_BB, lower_BB, get_Tradingview_signal
import redis
import json
import random
from db import delete_session_data, worker_data

"""
конструктор стратегий для индикаторов рода средних
"""
    
def __MA_strategy__(symbols, exchange, timeframe_list, condition, api_key, api_secret, client_socket, id_session, redis_client, test_mode_status: str, trailing_stoploss: str, simple_stoploss: str, futures: str, spot: str, coins_list, conditions):

    __crypto = exchange(api_key, api_secret)
    print(__crypto)

    TRADING_VIEW_MODE = False
    CONSTRUCTOR_MODE = False
    NEURAL_MODE = False
    FUTURES =  False
    SPOT = False
    simple_stop_loss = False
    trailing_stop_loss = False

    
    print('hyu')
    if 'TRADINGVIEW' in str(condition):
        TRADING_VIEW_MODE = True
    
    if 'if' in str(condition):
        CONSTRUCTOR_MODE = True
    
    if 'NEURAL' in str(condition):
        NEURAL_MODE = True

    if CONSTRUCTOR_MODE == True:
        action = str(condition).split('->')[1].strip()
        condition = str(condition).split('->')[0]

        print(action)
        
        indicators_values = []
        indicators_list = []
        main_condition = ''
        condition_list = str(condition).split()
        iteration = 0
        indicator_iter = 0

        for _ in range(len(condition_list)):
            while True:
                if iteration == 1:
                    main_condition += f' indicators_values[{indicator_iter}] '
                    indicator_iter += 1
                    iteration = 0
                    indicators_list.append(condition_list[_])
                    break

                if iteration == 0:
                    if condition_list[_] == 'and':
                        main_condition += f' {condition_list[_]}'
                    else:
                        main_condition += condition_list[_]
                    iteration = 1
                    break

        main_condition = main_condition.strip()
        print(main_condition)
        
        print(indicators_list)
        
        indicators_func = []

        for k in range(len(indicators_list)):
            indicator_func = str(indicators_list[k]).replace(')','') + ', history' + ')'
            indicators_func.append(indicator_func)
        
        print(indicators_func)

    livest = 0
    test_mode_status_inter = test_mode_status.split('(')[1].split(')')[0]
    balance = 0

    if test_mode_status_inter == 'True':
        test_mode_status = True
        print(f'STATUS TESTMODE {test_mode_status}')

    elif test_mode_status_inter == 'False':
        test_mode_status = False
    
    if str(trailing_stoploss).split('TRAILING_STOPLOSS(')[1].split(',')[0] == 'True':
        trailing_stop_loss = True
        TRAILING_STOP_LOSS_CONST = float(str(trailing_stoploss).split('TRAILING_STOPLOSS(True,')[1].split(')')[0])
    
    if str(simple_stoploss).split('SIMPLE_STOPLOSS(')[1].split(',')[0] == 'True':
        simple_stop_loss = True
        lower_border = float(str(simple_stoploss).split('SIMPLE_STOPLOSS(True,')[1].split(',')[0])
        lower_border_d = lower_border * 10
        upper_border = float(str(simple_stoploss).split(f'SIMPLE_STOPLOSS(True,{lower_border},')[1].split(')')[0])
        upper_border_d = upper_border * 10
    
    if str(futures).split('FUTURES(')[1].split(',')[0] == 'True':
        FUTURES = True
        credit_shoulder = int(str(futures).split('FUTURES(True,')[1].split(',')[0])
        bet_amount = float(str(futures).split(f'FUTURES(True,{credit_shoulder},')[1].split(')')[0])

    if str(spot).split('SPOT(')[1].split(',')[0] == 'True':
        SPOT = True
        bet_amount = float(str(futures).split('SPOT(True,')[1].split(')')[0])

    #simple_stop_loss = False
    #trailing_stop_loss = True
    #TRAILING_STOP_LOSS_CONST = 0.0003
    

    #ts = __crypto.trading_socket(symbol)
    pointsell = 1
    pointbuy = 1
    DELTA = 0.9997
    OFF_TRADES = 0
    liveltt = 1
    in_trade = False
    up_m = False
    if '<=' or '>=' in main_condition:
        additional_condition = False
    #threading.Thread(target=Graphic).start()
    #asyncio.run(Graphic())
    #async with ts  as tscm:
    #    b = 0
    #    #liveltt = 0

    symbol_list = symbols
    ACTIVE_TRADES = []
    ADDITIONAL_COND_LIST = []

    def SUM_ADDITIONAL(add_list):
        not_error = 0
        for i in range(len(add_list)):
            if add_list[i] == False:
                not_error += 1
        if not_error > 0:
            return False
        if not_error == 0:
            return True
        
    
    for k in range(len(symbol_list)):
        if type(symbol_list[k]) != str:
            ALL_COIN_CONDITION_MODE = True
            coincycle = len(symbol_list[k])
        else:
            ALL_COIN_CONDITION_MODE = False
            coincycle = 1
    
    print(f'ALL_COIN_CONDITION_MODE {ALL_COIN_CONDITION_MODE}')
    try:
        while True:

            if test_mode_status == True:
                balance = float(redis_client.get(f"{id_session}_balance"))
                print(f'BALANCE = {balance}')
            
            if CONSTRUCTOR_MODE == True:
                #additional_condition = redis_client.get(name=f"{symbol}_{id_session}_additional_condition")
                #if str(additional_condition) == 'True':
                #    additional_condition = True
                #else:

                
                #print(redis_client.get(f"{symbol}_{id_session}"))
                #history, livegraph = __crypto.gethistory(symbol, timeframe, ('500' + 'm'))

                #new_price = createframe(res)
                if ALL_COIN_CONDITION_MODE == False:
                    for d in range(len(symbol_list)):

                        symbol = symbol_list[d]
                        print(symbol)
                        print(random.randint(1,9))
                        timeframe = json.loads(timeframe_list)[d]

                        value = json.loads(redis_client.get(f"{symbol}_{id_session}_{timeframe}"))
                        additional_condition = redis_client.get(name=f"{symbol}_{id_session}_additional_condition_{timeframe}")
                        print(f'ADDITIONAL CONDITION {additional_condition}')
                        if additional_condition == b'True':
                            additional_condition = True
                        if additional_condition == b'False':
                            additional_condition = False
                        print(f'ADDITIONAL CONDITION {additional_condition}')

                        livegraph = value[0]
                        history = value[1]
                        for z in range(2):
                            step = z + (2 * d)
                            value_indicator = eval(indicators_func[step])
                            indicators_values.append(value_indicator)

                
                print(indicators_values)

                main_cond_list = main_condition.split(' ')
                print(main_condition)
                
                if ALL_COIN_CONDITION_MODE == False:
                    if additional_condition == False:
                        for p in range(len(main_cond_list)):
                            if main_cond_list[p] == '<=' or main_cond_list[p] == '>=':
                                if main_cond_list[p] == '<=':
                                    additional_condition = eval(f'compare({main_cond_list[p-1]}, {main_cond_list[p+1]}, ">")')
                                    print(f'ADDITIONAL CONDITION {additional_condition}')
                                    if additional_condition == False:
                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')
                                        break
                                    if additional_condition == True:
                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='True')
                                if main_cond_list[p] == '>=':
                                    additional_condition = eval(f'compare({main_cond_list[p-1]}, {main_cond_list[p+1]}, "<")')
                                    print(f'ADDITIONAL CONDITION {additional_condition}')
                                    if additional_condition == False:
                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')
                                        break
                                    if additional_condition == True:
                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='True')
                print('gg')

                if in_trade == False:
                    if '<=' or '>=' in main_condition:
                        for _ in range(coincycle):
                            if ALL_COIN_CONDITION_MODE == True:

                                for d in range(len(symbol_list)):
                                        
                                    if type(symbol) == str:
                                        symbol = symbol_list[d]
                                    else:
                                        symbol = symbol_list[d][_]

                                    print(symbol)
                                    print(random.randint(1,9))
                                    timeframe = json.loads(timeframe_list)[d]
                                    additional_condition = redis_client.get(name=f"{symbol}_{id_session}_additional_condition")
                                    print(f'ADDITIONAL CONDITION {additional_condition}')
                                    if additional_condition == b'True':
                                        additional_condition = True
                                    if additional_condition == b'False':
                                        additional_condition = False
                                    print(f'ADDITIONAL CONDITION {additional_condition}')

                                    value = json.loads(redis_client.get(f"{symbol}_{id_session}_{timeframe}"))
                                    livegraph = value[0]
                                    history = value[1]
                                    for z in range(2):
                                        step = z + (2 * d)
                                        value_indicator = eval(indicators_func[step])
                                        indicators_values.append(value_indicator)

                                    if additional_condition == False:
                                        for p in range(len(main_cond_list)):
                                            if main_cond_list[p] == '<=' or main_cond_list[p] == '>=':
                                                if main_cond_list[p] == '<=':
                                                    additional_condition = eval(f'compare({main_cond_list[p-1]}, {main_cond_list[p+1]}, ">")')
                                                    print(additional_condition)
                                                    if additional_condition == False:
                                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')
                                                        break
                                                    if additional_condition == True:
                                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='True')
                                                if main_cond_list[p] == '>=':
                                                    additional_condition = eval(f'compare({main_cond_list[p-1]}, {main_cond_list[p+1]}, "<")')
                                                    if additional_condition == False:
                                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')
                                                        break
                                                    if additional_condition == True:
                                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='True')

                            if additional_condition == True:
                                print(eval(f'[True {main_condition} else False]'))
                                access_buy = eval(f'[True {main_condition} else False]')
                                access_buy = access_buy[0]
                                print(access_buy)
                                if access_buy == True:
                                    if not in_trade:
                                        in_trade = True
                                        print('IN TRADE!')
                                        action_list = str(action).split('->')

                                        for _ in range(len(action_list)):
                                       
                                            ACTION = action_list[_].split('(')[0]
                                            action_pair = action_list[_].split('(')[1].split(')')[0]
                                            if SPOT == True:
                                                if test_mode_status == False:
                                                    __crypto.spotbuy()
                                            if FUTURES == True:
                                                if ACTION == 'BUY':
                                                    if test_mode_status == False:
                                                        __crypto.buy()
                                                if ACTION == 'SELL':
                                                    if test_mode_status == False:
                                                        __crypto.sell()

                                            balance -= bet_amount
                                            redis_client.set(name=f"{id_session}_balance", value = balance, xx=True)
                                            value = json.loads(redis_client.get(f"{action_pair}_{id_session}_1m"))
                                            livegraph = value[0]
                                            pointbuy = float(livegraph)
                                            pointstoploss = DELTA * pointbuy
                                            status = "ON"
                                            print(f'BUY ON {pointbuy} on {action_pair}!')

                                            ACTIVE_TRADES.append([action_pair, pointbuy, pointstoploss, status, 0, 0, ACTION])
                                    else:
                                        break
                                else:
                                    break
                            else:
                                break
                                

                    if '<=' or '>=' not in main_condition:
                        for _ in range(coincycle):

                            if ALL_COIN_CONDITION_MODE == True:
                                for d in range(len(symbol_list)):
                                    
                                    if type(symbol) == str:
                                        symbol = symbol_list[d]
                                    else:
                                        symbol = symbol_list[d][_]

                                    print(symbol)
                                    print(random.randint(1,9))
                                    timeframe = json.loads(timeframe_list)[d]

                                    value = json.loads(redis_client.get(f"{symbol}_{id_session}_{timeframe}"))
                                    livegraph = value[0]
                                    history = value[1]
                                    for z in range(2):
                                        step = z + (2 * d)
                                        value_indicator = eval(indicators_func[step])
                                        indicators_values.append(value_indicator)

                            print(eval(f'[True {main_condition} else False]'))
                            access_buy = eval(f'[True {main_condition} else False]')
                            access_buy = access_buy[0]
                            print(access_buy)
                            if access_buy == True:
                                if not in_trade:
                                    in_trade = True
                                    print('IN TRADE!')
                                    action_list = str(action).split('->')
                                    print(action_list)

                                    for _ in range(len(action_list)):
                                       
                                        ACTION = action_list[_].split('(')[0]
                                        action_pair = action_list[_].split('(')[1].split(')')[0]
                                        print(action_pair)
                                        if SPOT == True:
                                            if test_mode_status == False:
                                                __crypto.spotbuy()
                                        if FUTURES == True:
                                            if ACTION == 'BUY':
                                                if test_mode_status == False:
                                                    __crypto.buy()
                                            if ACTION == 'SELL':
                                                if test_mode_status == False:
                                                    __crypto.sell()

                                        balance -= bet_amount
                                        print(balance)
                                        redis_client.set(name=f"{id_session}_balance", value = balance, xx=True)
                                        value = json.loads(redis_client.get(f"{action_pair}_{id_session}_1m"))
                                        print(value)
                                        livegraph = value[0]
                                        pointbuy = float(livegraph)
                                        pointstoploss = DELTA * pointbuy
                                        status = "ON"
                                        print(f'BUY ON {pointbuy} on {action_pair}!')

                                        ACTIVE_TRADES.append([action_pair, pointbuy, pointstoploss, status, 0, 0, ACTION])
                                else:
                                    break
                            else:
                                break


            if TRADING_VIEW_MODE == True:
                if in_trade == False:
                    for _ in range(len(symbol_list)):
                        action = get_Tradingview_signal(symbol_list[_],'Crypto',exchange.getstr(), timeframe)
                        if 'SELL' in str(action):
                            action = 'SELL'
                        if 'BUY' in str(action):
                            action = 'BUY'
                        print(f'RECOMMENDATION: {action}')
                        if action:
                            if not in_trade:
                                in_trade = True
                                
                                if SPOT == True:
                                    if test_mode_status == False:
                                        __crypto.spotbuy()
                                if FUTURES == True:
                                    if action == 'BUY':
                                        if test_mode_status == False:
                                            __crypto.buy()
                                        print(f'BUY ON {pointbuy}!')

                                    if action == 'SELL':
                                        if test_mode_status == False:
                                            __crypto.sell()
                                        print(f'SELL ON {pointbuy}!')
                                balance -= bet_amount
                                redis_client.set(name=f"{id_session}_balance", value = balance, xx=True)
                                value = json.loads(redis_client.get(f"{symbol_list[_]}_{id_session}_1m"))
                                livegraph = value[0]
                                pointbuy = float(livegraph)
                                pointstoploss = DELTA * pointbuy
                                status = "ON"

                                ACTIVE_TRADES.append([symbol_list[_], pointbuy, pointstoploss, status, 0, 0, action])
            
            """
            TO DO TRAILING STOP LOSS
            """

            if in_trade == True:
                print(f'trailing stoploss {trailing_stop_loss}')
                for k in range(len(ACTIVE_TRADES)):
                        
                    symbol = ACTIVE_TRADES[k][0]
                    value = json.loads(redis_client.get(f"{symbol}_{id_session}_1m"))
                    livegraph = value[0]
                    pointbuy = ACTIVE_TRADES[k][1]
                    pointstoploss = ACTIVE_TRADES[k][2]
                    status = ACTIVE_TRADES[k][3]
                    action = ACTIVE_TRADES[k][6]
                    redis_client.set(f"{id_session}_balance", value=balance, xx=True)

                    print(symbol, livegraph, pointbuy, pointstoploss, status, action)
                    if status != 'ON':
                        OFF_TRADES += 1
                        continue
                    if OFF_TRADES == len(ACTIVE_TRADES):
                        in_trade = False
                        return end_session(in_trade, 
                                            ACTIVE_TRADES, 
                                            balance, 
                                            redis_client, test_mode_status, id_session)

                    if simple_stop_loss == True:
                        difference = (float(livegraph) / float(pointbuy)) - 1

                        print(f'DIFFERENCE {difference}') 

                        if (lower_border_d < difference < lower_border):
                            print('SELLING!')
                            
                            if SPOT == True:
                                if action == 'BUY':
                                    status = 'LOST'
                                    balance += bet_amount * difference
                                    if test_mode_status == False:
                                        __crypto.close_spot()
                            if FUTURES == True:
                                if action == 'BUY':
                                    status = 'LOST'
                                    balance += (bet_amount * credit_shoulder) * difference
                                    if test_mode_status == False:
                                        __crypto.close_futures()
                                if action == 'SELL':
                                    status = 'GET'
                                    balance += -((bet_amount * credit_shoulder) * difference)
                                    if test_mode_status == False:
                                        __crypto.close_futures()

                            profit_fiat = difference * pointbuy
                            profit = difference*100
                            ACTIVE_TRADES[k][3] = 'OFF'
                            ACTIVE_TRADES[k][4] = profit_fiat
                            ACTIVE_TRADES[k][5] = profit

                            if additional_condition == True:
                                redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')
                            
                        
                        if (upper_border < difference < upper_border_d):
                            print('SELLING!')
                            in_trade = False
                            if SPOT == True:
                                if action == 'BUY':
                                    status = 'GET'
                                    balance += bet_amount * difference
                                    if test_mode_status == False:
                                        __crypto.close_spot()
                            if FUTURES == True:
                                if action == 'BUY':
                                    status = 'GET'
                                    balance += (bet_amount * credit_shoulder) * difference
                                    if test_mode_status == False:
                                        __crypto.close_futures()
                                if action == 'SELL':
                                    status = 'LOST'
                                    balance += -((bet_amount * credit_shoulder) * difference)
                                    if test_mode_status == False:
                                        __crypto.close_futures()

                            profit_fiat = difference * pointbuy
                            profit = difference*100
                            ACTIVE_TRADES[k][3] = 'OFF'
                            ACTIVE_TRADES[k][4] = profit_fiat
                            ACTIVE_TRADES[k][5] = profit

                            if additional_condition == True:
                                redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')

                    if trailing_stop_loss == True:
                        
                        if action == 'BUY':
                            print('sjijaoidjs')
                            difference_loss = (float(livegraph) / float(pointstoploss)) - 1

                            if difference_loss > 0:
                                if difference_loss > TRAILING_STOP_LOSS_CONST:
                                    ACTIVE_TRADES[k][2] *= (1 + (difference_loss - TRAILING_STOP_LOSS_CONST))
                                    
                            
                            print(f'DIFFERENCE_LOSS {difference_loss}')

                            if float(livegraph) <= float(pointstoploss):

                                difference = (float(livegraph) / float(pointbuy)) - 1

                                print(f'DIFFERENCE {difference}')

                                if difference < 0:
                                    print('SELLING!')
                                    in_trade = False
                                    if SPOT == True:
                                        status = 'LOST'
                                        balance += bet_amount * difference
                                        if test_mode_status == False:
                                            __crypto.close_spot()
                                    if FUTURES == True:
                                        status = 'LOST'
                                        balance += (bet_amount * credit_shoulder) * difference
                                        if test_mode_status == False:
                                            __crypto.close_futures()

                                    profit_fiat = difference * pointbuy
                                    profit = difference*100
                                    ACTIVE_TRADES[k][3] = 'OFF'
                                    ACTIVE_TRADES[k][4] = profit_fiat
                                    ACTIVE_TRADES[k][5] = profit

                                    if additional_condition == True:
                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')

                                if difference > 0:
                                    print('SELLING!')
                                    in_trade = False
                                    if SPOT == True:
                                        status = 'GET'
                                        balance += bet_amount * difference
                                        if test_mode_status == False:
                                            __crypto.close_spot()
                                    if FUTURES == True:
                                        status = 'GET'
                                        balance += (bet_amount * credit_shoulder) * difference
                                        if test_mode_status == False:
                                            __crypto.close_futures()

                                    profit_fiat = difference * pointbuy
                                    profit = difference*100
                                    ACTIVE_TRADES[k][3] = 'OFF'
                                    ACTIVE_TRADES[k][4] = profit_fiat
                                    ACTIVE_TRADES[k][5] = profit

                                    if additional_condition == True:
                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')
                        
                        if action == 'SELL':

                            difference_loss = (float(livegraph) / float(pointstoploss)) - 1

                            if difference_loss < 0:
                                if difference_loss < (-TRAILING_STOP_LOSS_CONST):
                                    ACTIVE_TRADES[k][2] *= (1 - ((-difference_loss) - TRAILING_STOP_LOSS_CONST))
                            
                            print(f'DIFFERENCE_LOSS {difference_loss}')
                            
                            if float(livegraph) >= float(pointstoploss):
                                difference = (float(livegraph) / float(pointbuy)) - 1

                                print(f'DIFFERENCE {difference}')

                                if difference < 0:
                                    print('SELLING!')
                                    in_trade = False
                                    status = 'GET'
                                    balance += -((bet_amount * credit_shoulder) * difference)
                                    if test_mode_status == False:
                                        __crypto.close_futures()
                                        
                                    profit_fiat = difference * pointbuy
                                    profit = difference*100
                                    ACTIVE_TRADES[k][3] = 'OFF'
                                    ACTIVE_TRADES[k][4] = profit_fiat
                                    ACTIVE_TRADES[k][5] = profit

                                    if additional_condition == True:
                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')

                                if difference > 0:
                                    print('SELLING!')
                                    in_trade = False
                                    status = 'LOST'
                                    balance += -((bet_amount * credit_shoulder) * difference)
                                    if test_mode_status == False:
                                        __crypto.close_futures()

                                    profit_fiat = difference * pointbuy
                                    profit = difference*100
                                    ACTIVE_TRADES[k][3] = 'OFF'
                                    ACTIVE_TRADES[k][4] = profit_fiat
                                    ACTIVE_TRADES[k][5] = profit

                                    if additional_condition == True:
                                        redis_client.set(name=f"{symbol}_{id_session}_additional_condition", value='False')

                    print(f'TRAILING_STOP_LOSS_CONST {TRAILING_STOP_LOSS_CONST}')
                    print(f'PRICE OF {ACTIVE_TRADES[k][0]} is {livegraph}')
                
                    print(f'CURRENT BALANCE {balance}')
                    
                    #if len(symbol_list) == 1:
                    #    time.sleep(0.5)

                    #if len(symbol_list) > 1 and in_trade == True:
                    #    time.sleep(0.5)

                    #elif len(symbol_list) > 1 and in_trade == False:
                    #    continue

                    datanext = ''
                    if CONSTRUCTOR_MODE == True:
                        for _ in range(len(indicators_values)):
                            datanext += f'{indicators_values[_]}|'
                    datanext += f'{in_trade}|{livegraph}|{pointbuy}|{ACTIVE_TRADES[k][0]}|{balance}'

                    client_socket.send(datanext.encode('utf-8'))
            
            if in_trade == False:
                datanext = ''
                if CONSTRUCTOR_MODE == True:
                    for _ in range(len(indicators_values)):
                        datanext += f'{indicators_values[_]}|'
                datanext += f'{in_trade}|{balance}'

                client_socket.send(datanext.encode('utf-8'))
            
            print(f'CLIENT SOCKET {client_socket}')
            print(f'UP_M = {additional_condition}')
            #livegraph = float(livegraph) 

            indicators_values = []

            if in_trade == True:
                time.sleep(0.7)

            if in_trade == False:
                break

    except ConnectionError:
        print(f"{client_socket}:LEAVED SESSION!")
        delete_session_data(coins_list, redis_client, id_session, conditions)
        redis_client.close()
        indicators_values = []
        return 400

    except Exception as ex:
        print(ex)    
        indicators_values = []
        return 400

    if in_trade == False:
        return 200

def end_session(in_trade, trades_list, balance, redis_client, test_mode_status, id_session):

    if test_mode_status == True:
        redis_client.set(name=f"{id_session}_balance", value = balance)
    profit = 0
    status = 0
    for _ in range(len(trades_list)):
        profit += trades_list[_][4]
    if profit >= 0:
        status = 'GET'
    if profit < 0:
        status = 'LOST'
    
    return f'{in_trade}|{profit}|{balance}|{id_session}|{status}'

def liveSMA(period_MA, live, history):
    new_price = live.Price.values[0]
    history.pop(0)
    history.append(str(new_price))
    sum_price_SMA = 0
    for i in range(len(history)):
        sum_price_SMA += float(history[i])
    print(f'SUM_SMA : {sum_price_SMA}')

    liveMA = (sum_price_SMA) / float(period_MA)
    return liveMA

def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','p']]
    df.columns = ['symbol','Time','Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df
