# zpf

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
# from pandas_datareader import data
import re

import os

data_path = "../../data/dce/2014/"
futures_data = {}
def file_reader(file_dir, year):
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            f = open(data_path + str(file_name), encoding='utf-8', errors='ignore')
            tmpf = f.readlines()
            for items in tmpf:
                item = re.split(r",|\n", items)
                item_float = []
                for tmp in item:
                    if year == 2015:
                        item_float.append(str(tmp))
                    else:
                        item_float.append((str(tmp)[1:len(tmp)-1]).strip())
                if year == 2015:
                    goodType = item[1][0:len(item[1]) - 4]
                else:
                    goodType = item[1][1:(len(item[1]) - 5)]
                if goodType not in futures_data:
                    futures_data[goodType] = []
                futures_data[goodType].append(item_float)
    return True

file_reader(data_path, 2014)
data_path = "../../data/dce/2015/"
file_reader(data_path, 2015)
data_path = "../../data/dce/2016/"
file_reader(data_path, 2016)

def get_goods_price(goods):
    df=DataFrame(futures_data[goods]).drop_duplicates(subset=2, keep='last').set_index(2)[3]
    for i in range(0,len(df)):
        df[i]=float(df[i])
    return df

if __name__=="__main__":
    # example start

    # all_stock={}
    # for ticker in ["AAPL","IBM","MSFT","GOOG"]:
    #     all_stock[ticker]=data.get_data_yahoo(ticker)
    #
    # price=DataFrame({tic:data["Adj Close"] for tic ,data in all_stock.items()})
    # volume=DataFrame({tic:data["Volume"] for tic ,data in all_stock.items()})
    # open=DataFrame({tic:data["Open"] for tic ,data in all_stock.items()})
    # high=DataFrame({tic:data["High"] for tic ,data in all_stock.items()})
    # low=DataFrame({tic:data["Low"] for tic ,data in all_stock.items()})
    #
    # print("Volume: \n"); print(volume.head())
    # print("Price: \n"); print(price.tail())
    #
    # returns=price.pct_change()
    #
    # print("percentage change tail:\n"); print(returns.tail())
    #
    # print("type of returns:\n"); print(type(returns.MSFT))
    # print("returns tail:\n"); print(returns.MSFT.tail())
    #
    # print("MSFT IBM corr:\n"); print(returns.MSFT.corr(returns.IBM))
    # print("MSFT IBM cov:\n"); print(returns.MSFT.cov(returns.IBM))
    #
    # print("corr matrix:\n"); print(returns.corr())
    # print("cov matrix:\n"); print(returns.cov())

    # example end


    goods_list=["y","v","j", "jm", "i"]
    price=DataFrame({goods:get_goods_price(goods) for goods in goods_list})
    price_change=price.pct_change()
    print("corr matrix:\n")
    print(price_change.corr())
    print("cov matrix:\n")
    print(price_change.cov())







