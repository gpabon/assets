import pandas as pd

prices = pd.read_csv('data/bvc/stocks.csv', index_col=0)

colcap = pd.read_csv('data/bvc/COLCAP.csv', index_col=0)

print(prices.join(colcap, how='outer'))
print(prices.shape)
print(colcap.shape)


