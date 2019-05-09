import os
import logging
import sys
import time
import urllib.request
from urllib.error import URLError
import pandas as pd
import io

def _set_colombia_tz():
    os.environ['TZ'] = 'America/Bogota'
    time.tzset()

def _get_today_date():
    _set_colombia_tz()
    return(time.strftime('%Y-%m-%d'))

def _get_date_prices_url(date):
    URL = "http://www.bvc.com.co/mercados/DescargaXlsServlet?" +\
            "archivo=acciones&fecha={}&resultados=100&tipoMercado="
    return(URL.format(date))

def _get_date_stock_prices(date):
    url = _get_date_prices_url(date)
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                logging.error('HTTP error: {}. url: {}'.format(
                        response.status,url))
                sys.exit(1)
            date_stock_prices_io = io.BytesIO(response.read())
    except URLError:
        logging.error('URLError: {}'.format(url))
        sys.exit(1)
    date_stock_prices = pd.read_excel(date_stock_prices_io,
            sheet_name='Resultado', header=1)
    return(date_stock_prices)

def _update_stocks(date, stocks, date_stock_prices):
    if date_stock_prices.empty:
        return(stocks)
    indexes = ['HCOLSEL', 'ICOLCAP', 'ICOLRISK']
    for idx, row in date_stock_prices[['Nemotecnico',
            'Ultimo Precio']].iterrows():
        nemo = row['Nemotecnico'].strip()
        price = row['Ultimo Precio']
        if nemo not in indexes:
            stocks.loc[date, nemo] = price
    return(stocks.ffill())

def update_stock_file(date):
    STOCKS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 
            "..", "data", "bvc", "stocks.csv"))
    stocks = pd.read_csv(STOCKS_FILE, index_col=0)
    date_stock_prices = _get_date_stock_prices(date)
    stocks = _update_stocks(date, stocks, date_stock_prices)
    stocks.to_csv(STOCKS_FILE)

def main():
    if len(sys.argv) > 2:
        logging.error('Too many arguments')
        sys.exit(1)
    if len(sys.argv) == 2:
        update_stock_file(sys.argv[1])
    else:
        update_stock_file(_get_today_date())

# DO NOT TOUCH FROM HERE ... 
if __name__ == '__main__':
    APP_NAME, _ = os.path.splitext(os.path.basename(__file__))
    MODULE_NAME = os.path.basename(os.path.dirname(__file__))
    LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
            "log","{}_{}.log".format(MODULE_NAME, APP_NAME))) 
    logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, filemode='a',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('App started: {}'.format(APP_NAME))
    main()
    logging.info('App successfully ended: {}'.format(APP_NAME))  
