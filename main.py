import data_crawler
import ploter

def main():
    data_crawler.update_all_data()
    ploter.draw_all()

if __name__ == '__main__':
    main()