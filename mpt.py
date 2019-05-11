import pandas as pd
import numpy as np

def daily_pct_returns(prices):
    return(prices.pct_change().dropna(how='all'))

def return_means(returns):
    return(returns.mean())

def random_wi(length):
    random_array = np.random.rand(length)
    return(random_array/random_array.sum())

def portfolio_expected_return(wi, ERi):
    return((wi * ERi).sum())

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

if __name__ == '__main__':
    prices = pd.read_csv('data/bvc/stocks.csv', index_col=0)
    returns = daily_pct_returns(prices)
    ERi = return_means(returns)
    wi = random_wi(len(ERi))
    ERp = portfolio_expected_return(wi, ERi)
    sigma2p = portfolio_variance(wi, returns)
    sigmap = np.sqrt(sigma2p)
    rf = .027 / (20*12)
    print(sharpe_ratio(ERp, rf, sigmap))
    wic = clean_wi(wi,2)
    print(wic)
    print(min_size(wic, prices))
