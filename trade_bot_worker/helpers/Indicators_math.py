import random
import numpy as np

import matplotlib.pyplot as plt
import time 
from tradingview_ta import TA_Handler, Interval, Exchange


def get_Tradingview_signal(symbol, screener, exchange, interval):
    
    output = TA_Handler(symbol=symbol, 
                        screener=screener, 
                        exchange=exchange,
                        interval=interval)

    return output.get_analysis().summary['RECOMMENDATION']


def MA(period_MA: int, history: list):

    history = history[(len(history)-period_MA):]
    #history.pop(0)
    #history.append(str(new_price))
    print(len(history))
    sum_price_SMA = 0
    for i in range(len(history)):
        sum_price_SMA += float(history[i])
    print(f'SUM_SMA : {sum_price_SMA}')

    liveMA = (sum_price_SMA) / float(period_MA)
    return liveMA

def upper_BB(period_BB: int, history: list):
    SMA = MA(period_BB, history)
    history = history[(len(history)-period_BB):]
    #history.pop(0)
    #history.append(str(new_price))
    print(len(history))
    sum_price_SMA_deviate = 0
    for i in range(len(history)):
        sum_price_SMA_deviate += float((float(history[i])-SMA)**2)
    print(f'SUM_SMA_: {sum_price_SMA_deviate}')
    SD = np.sqrt((sum_price_SMA_deviate) / float(period_BB))
    upper_band = float(SMA) + (2 * SD)
    return upper_band


def lower_BB(period_BB: int, history: list):

    SMA = MA(period_BB, history)
    history = history[(len(history)-period_BB):]
    #history.pop(0)
    #history.append(str(new_price))
    print(len(history))
    sum_price_SMA_deviate = 0
    for i in range(len(history)):
        sum_price_SMA_deviate += float((float(history[i])-SMA)**2)
    print(f'SUM_SMA_: {sum_price_SMA_deviate}')
    SD = np.sqrt((sum_price_SMA_deviate) / float(period_BB))
    lower_band = float(SMA) - (2 * SD)
    return lower_band

def RSI(period_RSI: int, history: list):
    history = history[(len(history)-period_RSI):]
    print(len(history))

    difference = float(history[0])

def diff_PRICE(period: int, live, history: list):
    new_price = live.Price.values[0]
    history = history[(len(history)-period):]
    diff = ((float(history[-1]) / float(history[0])) - 1) * 100
    
    return diff




def compare(indicator_1, indicator_2, condition):
    print(indicator_1, indicator_2)
    if condition == '>':
        if indicator_1 > indicator_2:
            return True
        else:
            return False

    if condition == '<':
        if indicator_1 < indicator_2:
            return True
        else:
            return False


