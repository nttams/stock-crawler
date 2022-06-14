import matplotlib.pyplot as plt
import datetime as dt
import file_handler as fh
import mpld3

fig, ax = plt.subplots()

def draw(companies):
    for company in companies:
        data = fh.read_local_data(company)
        x, y = parse_fields(data, 'Close')
        plot(x, y, company)

    show()

def draw_all():
    company_list = fh.read_config()
    draw(company_list)

def parse_fields(data, field):
    x = []
    y = []
    for item in data:
        time = dt.datetime.fromtimestamp(item['Date'] / 1e3)
        x.append(time)
        y.append(item[field])

    return x, y

def plot(x, y, company):
    ax.plot(x, y, label = company, linewidth = 0.8)

def save_html():
    mpld3.save_html(fig, 'plot.html')

def show_in_web():
    mpld3.show(fig)

def show():
    plt.title("Stock prices")
    plt.xlabel("Time")
    plt.ylabel("Value (VND)")

    plt.legend() # show labels
    plt.grid()

    plt.show()