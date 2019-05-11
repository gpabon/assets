import mpt
import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    prices = pd.read_csv('data/bvc/stocks.csv', index_col=0)
    
    mu = expected_returns.mean_historical_return(prices)
    S = risk_models.sample_cov(prices)
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    wi_opt_lst = []
    for col in prices.columns:
        wi_opt_lst.append(weights[col])
    wi_opt = np.array(wi_opt_lst)

    returns = mpt.daily_pct_returns(prices)
    ERi = mpt.return_means(returns)
    #wi = mpt.random_wi(len(ERi))
    ERp = mpt.portfolio_expected_return(wi_opt, ERi)
    sigma2p = mpt.portfolio_variance(wi_opt, returns)
    sigmap = np.sqrt(sigma2p)
    rf = .027 / (20*12)
    optimal_sharpe = mpt.sharpe_ratio(ERp, rf, sigmap)
    print(optimal_sharpe)

    pf_opt_x = [sigmap]
    pf_opt_y = [ERp]
    ef_x = [0, sigmap]
    ef_y = [rf, ERp]
    pf_x = []
    pf_y = []
    for i in range(10000):
        if i % 100 == 0:
            print('.', end=' ', flush=True)
        wi = mpt.random_wi(len(ERi))
        ERp = mpt.portfolio_expected_return(wi, ERi)
        pf_y.append(ERp)
        sigma2p = mpt.portfolio_variance(wi, returns)
        sigmap = np.sqrt(sigma2p)
        pf_x.append(sigmap)
        sharpe = mpt.sharpe_ratio(ERp, rf, sigmap)
        if sharpe > optimal_sharpe:
            print(sharpe)
            print(wi)
    print()
    plt.scatter(pf_x, pf_y)
    plt.plot(ef_x, ef_y)
    plt.scatter(pf_opt_x, pf_opt_y, c='r')
    plt.savefig('log/foo.png', bbox_inches='tight')

    #wi_opt[np.abs(wi_opt) < 1e-3] = 0
    wi_opt = np.round(wi_opt, 2)
    print(wi_opt)
    print(sum(wi_opt))
