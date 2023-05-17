import random
from db import worker_data
import sqlite3
import threading
from threading import Thread


with open('/Users/vladilenzubcov/Documents/trade_bot_worker/value_pairs.txt', 'r') as f:
    pairs_list = f.read().split('\n')

base =  sqlite3.connect('crpyto.db')
cur = base.cursor()

CRYPTO_DATA = 'crypto_date'

base.execute(f'CREATE TABLE IF NOT EXISTS {CRYPTO_DATA}(pair PRIMARY KEY, values)')
base.commit()

for i in range(len(pairs_list)):
    cur.execute(f'INSERT INTO {CRYPTO_DATA} VALUES (?, ?)', (pairs_list[i], ''))
    base.commit()
    threading.Thread(target=worker_data, args=(pairs_list[i], i))