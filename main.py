import data_crawler
import file_handler
import ploter

def main():
    data_crawler.update_all_data()
    ploter.draw(['acb', 'bid', 'vhm'])

if __name__ == '__main__':
    main()