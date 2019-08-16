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
    return(time.strftime('%Y%m%d'))

def _get_date_index_url(date):
    URL = "http://www.bvc.com.co/mercados/DescargaXlsServlet?" +\
            "archivo=indices&tipoMI=RESUMEN&fecha={}&codIndice=IIBR"
    return(URL.format(date))

def _get_date_index(date):
    url = _get_date_index_url(date)
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                logging.error('HTTP error: {}. url: {}'.format(
                        response.status,url))
                sys.exit(1)
            date_index_io = io.BytesIO(response.read())
    except URLError:
        logging.error('URLError: {}'.format(url))
        sys.exit(1)
    date_index = pd.read_excel(date_index_io,
            sheet_name='Resultado', header=1)
    return(date_index)

def _update_colcap(date, colcap, date_index):
    if date_index.empty:
        return(colcap)
    for idx, row in date_index[['Indice',
            'Valor Hoy']].iterrows():
        index = row['Indice'].strip()
        value = row['Valor Hoy']
        if index == 'COLCAP':
            colcap.loc[date, index] = value
    return(colcap.ffill())

def update_stock_file(date):
    COLCAP_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 
            "..", "data", "bvc", "COLCAP.csv"))
    colcap = pd.read_csv(COLCAP_FILE, index_col=0)
    date_index = _get_date_index(date)
    date_separated = date[0:4]+"-"+date[4:6]+"-"+date[6:8]
    colcap = _update_colcap(date_separated, colcap, date_index)
    colcap.to_csv(COLCAP_FILE)

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
