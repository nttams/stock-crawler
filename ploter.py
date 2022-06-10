import matplotlib.pyplot as plt
import datetime as dt
import file_handler

fig, ax = plt.subplots()

def draw(companies):
    for company in companies:
        data = file_handler.read_local_data(company)
        x, y = parse_fields(data, 'Close')
        plot(x, y)

    show()

def parse_fields(data, field):
    x = []
    y = []
    for item in data:
        time = dt.datetime.fromtimestamp(item['Date'] / 1e3)
        x.append(time)
        y.append(item[field])
        # y.append(item['Close'])

    return x, y

def plot(x, y):
    ax.plot(x, y)

def show():
    plt.show()