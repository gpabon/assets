import os
import logging
import sys

# Additional imports
import mpt
import pandas as pd
import json

def main():
    prices = pd.read_csv('data/bvc/stocks.csv', index_col=0)
    with open('data/bvc/train_history_out.json', 'r') as train_history_file:
        optimal = json.load(train_history_file)
    opt_backward = optimal['opt_backward']
    weights_arr = mpt.suggested_portfolio(opt_backward, prices, 1)
    weights_ser = pd.Series(weights_arr, index=prices.columns)
    non_zero_weights = weights_ser[weights_ser>0]
    print('Portfolio weights:')
    print(non_zero_weights)
    num_shares, total_price, weights_adjusted = mpt.min_size(weights_arr, 
            prices)
    print()
    print('Portfolio minimal number of shares per asset:')
    print(num_shares[num_shares>0])
    print()
    print('Portfolio minimal cost: COP$ {:,.0f}'.format(total_price))
    print()
    print('Weights adjusted')
    non_zero_weights_adjusted = weights_adjusted[weights_adjusted>0]
    print(non_zero_weights_adjusted)

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
