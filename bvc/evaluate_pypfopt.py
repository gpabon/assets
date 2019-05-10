import mpt
import pandas as pd
import numpy as np

if __name__ == '__main__':
    prices = pd.read_csv('data/bvc/stocks.csv', index_col=0)
    returns = mpt.daily_pct_returns(prices)
    ERi = mpt.return_means(returns)
    wi = mpt.random_wi(len(ERi))
    ERp = mpt.portfolio_expected_return(wi, ERi)
    sigma2p = mpt.portfolio_variance(wi, returns)
    sigmap = np.sqrt(sigma2p)
    rf = .027 / (20*12)
    print(mpt.sharpe_ratio(ERp, rf, sigmap))
