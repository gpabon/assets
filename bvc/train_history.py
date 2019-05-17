import os
import logging
import sys

# Additional imports
import mpt
import pandas as pd
import json

def main():
    MARKET_DAYS = 241
    RISK_FREE_RATIO = .02
    
    prices = pd.read_csv('data/bvc/stocks.csv', index_col=0)
    opt_backward, opt_forward = mpt.train_history(prices, MARKET_DAYS,
            RISK_FREE_RATIO)
    optimal = { 'opt_backward':opt_backward, 'opt_forward': opt_forward}
    with open('data/bvc/train_history_out.json', 'w') as out_file:
        json.dump(optimal, out_file)

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
