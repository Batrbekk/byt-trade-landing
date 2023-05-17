import requests

import random
import time
import json
import redis
import sqlite3

connection = sqlite3.connect('emulators.db')

cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS emulators (emulator_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                        indexx INT, timer INT)''')

index = 0
timer = int(time.time())

turple = (index, timer)


cursor.execute('''INSERT INTO emulators(indexx, timer)
                  VALUES(?, ?)
                  ''',turple)

cursor.execute("SELECT * FROM emulators")
print(cursor.fetchall())

cursor.execute("SELECT timer FROM emulators WHERE indexx == 0")

res = cursor.fetchall()
print(res)
print(res[-1][0])


index = 0
timer = int(time.time())

turple = (index, timer)


cursor.execute('''UPDATE emulators SET timer = ? WHERE indexx = ?''', (timer, index))

cursor.execute("SELECT timer FROM emulators WHERE indexx == 0")

res = cursor.fetchall()
print(res)
print(res[-1][0])

cursor.execute('DELETE FROM emulators;',)

cursor.execute("SELECT * FROM emulators")
res = cursor.fetchall()
if res == []:
    print('END')


def test():
    f = 'giirenge'
    print(f[-1])

    host = 'localhost'
    port = 6379
    redis_client = redis.Redis(host=host, port=port, db=0)

    print(redis_client.set(name="test_key", value='True'))

    value = bool(str(redis_client.get("test_key")))
    print(type(value))
    #print(redis_client.delete("test_key3"))
    if redis_client.set(name="test_key6", value=15) == True:
        print('hut')
        print(redis_client.set(name="test_key6", value="[16911.00000000, [17636.40000000]]", xx=True))



    print(str(redis_client.get("BTCUSDT_9270e2060d545579b4fd35cf5f041cdb")))
    lis = json.loads(redis_client.get("test_key6"))
    print(lis[0])

    while True:
        for key in redis_client.scan_iter():
            print(key)
            print(time.sleep(2))

    redis_client.close()