import time
import datetime
import file_handler

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.StrictRedis(host='172.17.0.1', port=6379)

def upload_data_to_redis(company):
    key = 'stock:' + company
    cache.execute_command('del ' + key)
    cache.execute_command('ts.create ' + key)

    data = file_handler.read_local_data(company)

    for stock in data:
        print(stock['date'], stock['average'])
        time_tuple = time.strptime(stock['date'], '%Y-%m-%d')
        time_epoch = time.mktime(time_tuple)
        time_epoch -=  (7 * 60 * 60) # timezone offset
        time_epoch *= 1000

        cache.execute_command('ts.add ' + key + ' ' + str(int(time_epoch)) + ' ' + str(stock['average']))


if __name__ == '__main__':
    company_list = file_handler.get_company_list()
    for company in company_list:
        upload_data_to_redis(company)
