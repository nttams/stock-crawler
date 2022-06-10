import json

CONFIG_FILE = 'config'
DATA_DIR = 'data'

def read_local_data(company):
    try:
        f = open(DATA_DIR + '/' + company + '.json', 'r')
        data = f.read()
        f.close()
    except Exception as err:
        raise Exception('error: ', err)

    return json.loads(data)

def read_config():
    try:
        f = open(CONFIG_FILE, 'r')
        config = f.read()
        f.close()
    except Exception as error:
        raise Exception('error reading file')

    config_json = json.loads(config)

    return config_json

def write_data(company, data):
    f = open(DATA_DIR + '/' + company + '.json', 'w')
    f.write(data)
    f.close()