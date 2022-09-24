import datetime
import json
import file_handler
import requests

HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}

def query_server(symbol, start_date, end_date):
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    API_VNDIRECT = 'http://finfo-api.vndirect.com.vn/v4/stock_prices/'
    query = 'code:' + symbol + '~date:gte:' + start_date + '~date:lte:' + end_date  
    delta = datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')
    params = {
        "sort": "date",
        "size": delta.days + 1,
        "page": 1,
        "q": query
    }
    res = requests.get(API_VNDIRECT, params=params, headers=HEADERS)
    data = res.json()['data']
    return data

def get_start_date(data):
    time = datetime.datetime.strptime(data[-1]['date'], '%Y-%m-%d')
    time += datetime.timedelta(days=1)
    return time

def update_data_company(company):
    current_data = []
    try:
        current_data = file_handler.read_local_data(company)
        start_date = get_start_date(current_data)
    except Exception as err:
        start_date = datetime.datetime.fromtimestamp(0)

    end_date  = datetime.datetime.now()

    start_date = clear_hour(start_date)
    end_date = clear_hour(end_date)

    if start_date < end_date:
        print("updating data for: " + company)

        record_count = 0
        new_data = query_server(company, start_date, end_date)

        for item in reversed(new_data):
            record_count += 1
            current_data.append(item)

        current_data = json.dumps(current_data, indent = 4)
        file_handler.write_data(company, current_data)

        print("data is updated for " + company + " with " + str(record_count) + " new records")

        return True
    return False

def clear_hour(date):
    date = date.replace(hour = 0)
    date = date.replace(minute = 0)
    date = date.replace(second = 0)
    date = date.replace(microsecond = 0)
    return date

def update_all_data():

    file_handler.create_data_folder()

    company_list = file_handler.get_company_list()

    is_up_to_date = True
    for company in company_list:
        if update_data_company(company):
            is_up_to_date = False

    if is_up_to_date:
        print("all data is up to date!")
