import pandas as pd
import numpy as np
from pandas import Series, DataFrame

from pandas_datareader import data

if __name__=="__main__":
    all_stock={}
    for ticker in ["AAPL","IBM","MSFT","GOOG"]:
        all_stock[ticker]=data.get_data_yahoo(ticker)

    price=DataFrame({tic:data["Adj Close"] for tic ,data in all_stock.items()})
    volume=DataFrame({tic:data["Volume"] for tic ,data in all_stock.items()})
    open=DataFrame({tic:data["Open"] for tic ,data in all_stock.items()})
    high=DataFrame({tic:data["High"] for tic ,data in all_stock.items()})
    low=DataFrame({tic:data["Low"] for tic ,data in all_stock.items()})

    print("Volume: \n"); print(volume.head())
    print("Price: \n"); print(price.tail())

    returns=price.pct_change()

    print("percentage change tail:\n"); print(returns.tail())

    print("type of returns:\n"); print(type(returns.MSFT))
    print("returns tail:\n"); print(returns.MSFT.tail())

    print("MSFT IBM corr:\n"); print(returns.MSFT.corr(returns.IBM))
    print("MSFT IBM cov:\n"); print(returns.MSFT.cov(returns.IBM))

    print("corr matrix:\n"); print(returns.corr())
    print("cov matrix:\n"); print(returns.cov())




