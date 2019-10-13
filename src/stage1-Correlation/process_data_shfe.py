import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_shfe_dataframe():
    pd.set_option('display.max_columns', None)
    filedir = os.path.join("../../data", "shfe")
    filename = os.path.join(filedir, "2018price.xls")
    dataframe = pd.read_excel(filename, sheet_name=0, header=2)
    dataframe = dataframe.drop(range(dataframe.shape[0] - 5, dataframe.shape[0]), axis=0)
    columns = dataframe.columns.tolist()
    dataframe = dataframe.drop(columns[-1], axis=1)
    dataframe[columns[0]] = dataframe[columns[0]].ffill()
    return dataframe


def get_ag18_prices(dataframe):
    cols = dataframe.columns.tolist()
    price_dict = {}
    capacity_dict = {}
    for idx in range(dataframe.shape[0]):
        future_name = dataframe.iloc[idx, 0]
        if not future_name[0:2] == 'ag':
            continue
        item = dataframe.iloc[idx, 1]
        price = dataframe.iloc[idx, 8]
        capacity = dataframe.iloc[idx, -2]
        if item in capacity_dict:
            if capacity_dict[item] < capacity:
                capacity_dict[item] = capacity
                price_dict[item] = price
        else:
            price_dict[item] = price
            capacity_dict[item] = capacity
    return list(price_dict.values())


def process_data():
    dataframe = get_shfe_dataframe()
    print(dataframe.head(15))
    print("dataframe shape = ", dataframe.shape)
    ag18 = get_ag18_prices(dataframe)
    # x = range(ag18.shape[0])
    x = range(len(ag18))
    plt.title("ag18")
    plt.xlabel("product")
    plt.ylabel("price")
    plt.plot(x, ag18)
    plt.show()


if __name__ == "__main__":
    process_data()