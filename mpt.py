import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns

def daily_pct_returns(prices):
    return(prices.pct_change().dropna(how='all'))

def return_means(returns):
    return(returns.mean())

def random_wi(length):
    random_array = np.random.rand(length)
    return(random_array/random_array.sum())

def portfolio_expected_return(wi, ERi):
    return((wi * ERi).sum())

def portfolio_expected_return_from_prices(wi, prices):
    returns = daily_pct_returns(prices)
    ERi = return_means(returns)
    return(portfolio_expected_return(wi, ERi))

def portfolio_variance(wi, returns):
    COVij = returns.cov()
    N = len(wi)
    wiN1 = wi.reshape(N,1)
    wi1N = wi.reshape(1,N)
    wij = np.dot(wiN1,wi1N)
    return((wij * COVij).sum().sum())

def sharpe_ratio(ERp, rf, sigmap):
    return((ERp-rf)/sigmap)

def clean_wi(wi, decimals):
    return(np.round(wi, decimals))

def min_size(wi, prices):
    last_date = max(prices.index)
    last_prices = prices.loc[last_date,:]
    possible_vols = last_prices / wi
    possible_vols = possible_vols.replace(np.inf, 0)
    min_vol = max(possible_vols)
    vols = wi * min_vol
    num_shares = np.round(vols / last_prices,0)
    vols_adjusted = last_prices*num_shares
    return(num_shares, np.round(vols_adjusted.sum(),0))

def tangency_portfolio(prices):
    mu = expected_returns.mean_historical_return(prices)
    S = risk_models.sample_cov(prices)
    ef = EfficientFrontier(mu, S)
    weights_dic = ef.max_sharpe()
    weights_lst = []
    for col in prices.columns:
        weights_lst.append(weights_dic[col])
    return(np.array(weights_lst))


def train_history(prices, market_days, risk_free_rate, 
        num_samples_train_lst = [20, 40, 60, 90, 120],
        num_samples_predict = 20):
    sharpe_ratios_lst = []
    for num_samples_train in num_samples_train_lst:
        left_limit = len(prices) - num_samples_predict - num_samples_train + 1
        daily_returns_lst = []
        for i in range(0, left_limit):
            print('.', end=' ', flush=True)
            prices_train_idxs = prices.index[i:i + num_samples_train]
            prices_train = prices.loc[prices_train_idxs,:].copy()
            weights_train = tangency_portfolio(prices_train)
            prices_predict_idxs = prices.index[i + num_samples_train:\
                    i + num_samples_train + num_samples_predict]
            prices_predict = prices.loc[prices_predict_idxs,:].copy()
            ERp = portfolio_expected_return_from_prices(weights_train, 
                    prices_predict)
            daily_returns_lst.append(ERp)
        print()
        yearly_returns = np.array(daily_returns_lst) * market_days
        mean_yearly_returns = yearly_returns.mean()
        std_yearly_returns = yearly_returns.std()
        sharpe_ratio = (mean_yearly_returns - risk_free_rate) /\
                std_yearly_returns
        print('Numer of days back:', num_samples_train)
        print('Expected return:', mean_yearly_returns)
        print('Expected risk:', std_yearly_returns)
        print('Sharpe ratio:', sharpe_ratio)
        sharpe_ratios_lst.append(sharpe_ratio)
    sharpe_ratios = np.array(sharpe_ratios_lst)
    max_sharpe_ratio = sharpe_ratios.max()
    max_sharpe_ratio_idx = sharpe_ratios.argmax()
    opt_num_samples = num_samples_train_lst[max_sharpe_ratio_idx]
    print()
    print('Optimal number of days back:', opt_num_samples)
    print('Sharpe ratio:', max_sharpe_ratio)
    return(opt_num_samples)

def suggested_portfolio(history_sample_size, prices, decimals=2):
    left_limit = len(prices) - history_sample_size
    last_prices_idxs = prices.index[left_limit:]
    last_prices = prices.loc[last_prices_idxs,:].copy()
    weights = tangency_portfolio(last_prices)
    return(clean_wi(weights, decimals))

if __name__ == '__main__':
    prices = pd.read_csv('data/bvc/stocks.csv', index_col=0)
    #returns = daily_pct_returns(prices)
    #ERi = return_means(returns)
    #wi = random_wi(len(ERi))
    #ERp = portfolio_expected_return(wi, ERi)
    #sigma2p = portfolio_variance(wi, returns)
    #sigmap = np.sqrt(sigma2p)
    #rf = .027 / (20*12)
    #print(sharpe_ratio(ERp, rf, sigmap))
    #wic = clean_wi(wi,2)
    #print(wic)
    #print(min_size(wic, prices))
    #num_samples = train_history(prices, 241, .02)
    weights_arr = suggested_portfolio(40, prices)
    weights_ser = pd.Series(weights_arr, index=prices.columns)
    non_zero_weights = weights_ser[weights_ser>0]
    print(non_zero_weights)
    num_shares, total_price = min_size(weights_arr, prices)
    print(num_shares[num_shares>0])
    print(total_price)
