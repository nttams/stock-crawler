import datetime as dt
import investpy as ipy
import json

import file_handler as fh

def query_server(company, start, end):
    start = start.strftime('%d/%m/%Y')
    end = end.strftime('%d/%m/%Y')
    data = ipy.get_stock_historical_data(
        stock = company,
        country = 'vietnam',
        from_date = start,
        to_date = end)

    return data

def get_start_date(data):
    time = data[-1]['Date'] / 1e3
    time += 86400
    time = dt.datetime.fromtimestamp(time)
    return time

def update_data_company(company):
    current_data = []
    lastest_date = 0
    try:
        current_data = fh.read_local_data(company)
        start_date = get_start_date(current_data)
    except Exception as err:
        start_date = dt.datetime.fromtimestamp(0)

    end_date  = dt.datetime.now()

    start_date = clear_hour(start_date)
    end_date = clear_hour(end_date)

    if start_date < end_date:
        print("updating data for", company)
        new_data = query_server(company, start_date, end_date)
        new_data = new_data.reset_index()
        new_data = new_data.to_json(orient='records')
        new_data = json.loads(new_data)
        for item in new_data:
            current_data.append(item)

        current_data = json.dumps(current_data, indent = 2)
        fh.write_data(company, current_data)

        return True
    return False

def clear_hour(date):
    date = date.replace(hour = 0)
    date = date.replace(minute = 0)
    date = date.replace(second = 0)
    date = date.replace(microsecond = 0)
    return date

def update_all_data():

    fh.create_data_folder()

    company_list = fh.read_config()

    is_up_to_date = True
    for company in company_list:
        if update_data_company(company):
            is_up_to_date = False

    if is_up_to_date:
        print("all data is up to date!")
