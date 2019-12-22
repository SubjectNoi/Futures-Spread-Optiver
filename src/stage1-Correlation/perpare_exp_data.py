import os
import numpy as np
import pandas as pd
import math
import h5py
from pprint import pprint
import matplotlib.pyplot as plt


# 计算相关系数
def computeCorrelation(X, Y):
    xBar = np.mean(X)
    yBar = np.mean(Y)
    SSR = 0
    varX = 0  # 公式中分子部分
    varY = 0  # 公式中分母部分
    for i in range(0, len(X)):
        diffXXBar = X[i] - xBar
        diffYYBar = Y[i] - yBar
        SSR += (diffXXBar * diffYYBar)
        varX += diffXXBar ** 2
        varY += diffYYBar ** 2

    SST = math.sqrt(varX * varY)
    return SSR / SST


# 假设有多个自变量的相关系数
def polyfit(x, y, degree):
    # 定义字典
    result = {}
    # polyfit 自动计算回归方程：b0、b1...等系数  degree为x的几次方的线性回归方程
    coeffs = np.polyfit(x, y, degree)
    # 转为list存入字典
    result['polynomial'] = coeffs.tolist()
    # poly1d 返回预测值
    p = np.poly1d(coeffs)
    # 给定一个x的预测值为多少
    y_hat = p(x)
    # 均值
    ybar = np.sum(y) / len(y)
    ssreg = np.sum((y_hat - ybar) ** 2)
    sstot = np.sum((y - ybar) ** 2)
    result['determination'] = ssreg / sstot
    return result


def get_shfe_dataframe(year=2017):
    pd.set_option('display.max_columns', None)
    filedir = os.path.join("../../data", "shfe")
    filename = os.path.join(filedir, str(year) + "price.xls")
    dataframe = pd.read_excel(filename, sheet_name=0, header=2)
    dataframe = dataframe.drop(range(dataframe.shape[0] - 5, dataframe.shape[0]), axis=0)
    columns = dataframe.columns.tolist()
    dataframe = dataframe.drop(columns[-1], axis=1)
    dataframe[columns[0]] = dataframe[columns[0]].ffill()
    return dataframe


# obtain dominant future prices
def get_item_prices(dataframe, itemname):
    cols = dataframe.columns.tolist()
    price_dict = {}
    capacity_dict = {}
    for idx in range(dataframe.shape[0]):
        future_name = dataframe.iloc[idx, 0]
        if not future_name[0:2] == itemname:
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
    return list(price_dict.values()), list(price_dict.keys())


def calc_person(prices_array, item_classes):
    corr_pairs = []
    tot = len(prices_array)
    for i in range(tot):
        for j in range(i + 1, tot):
            corr_value = computeCorrelation(prices_array[i], prices_array[j])
            corr_pairs.append((corr_value, i, j))
    corr_pairs = sorted(corr_pairs)
    corr_pairs.reverse()
    for i in range(min(len(corr_pairs), 5)):
        value = corr_pairs[i][0]
        idx1 = corr_pairs[i][1]
        idx2 = corr_pairs[i][2]
        item1 = item_classes[idx1]
        item2 = item_classes[idx2]
        print("{}, {}, {:.4f}".format(item1, item2, value))
        plt.title("Prices for {} via {} 2015-2018".format(item1, item2))
        plt.xlabel("days")
        plt.ylabel("prices")
        prices1 = prices_array[idx1]
        prices2 = prices_array[idx2]
        x = list(range(len(prices1)))
        plt.plot(x, prices1, label=item_classes[idx1])
        plt.plot(x, prices2, label=item_classes[idx2])
        plt.legend()
        plt.show()




def process_data():
    dataframe = get_shfe_dataframe()
    print(dataframe.head(3))
    print("dataframe shape = ", dataframe.shape)
    cols = dataframe.columns.tolist()
    item_namelist = dataframe[cols[0]].tolist()
    # pprint(list(set(item_namelist)), indent=2)
    item_classes = list(set([item[0:2] for item in item_namelist]))
    # print(item_classes)
    prices_list, date_list = [get_item_prices(dataframe, item_class) for item_class in item_classes]
    prices_array = []
    counts = np.bincount([len(prices) for prices in prices_list])
    num = np.argmax(counts)
    new_item_classes = []
    for idx, prices in enumerate(prices_list):
        if len(prices) == num:
            # print(item_classes[idx], len(prices))
            prices_array.append((prices - np.mean(prices)) / np.std(prices))
            new_item_classes.append(item_classes[idx])
    item_classes = new_item_classes
    print(item_classes)


def process_data_combined():
    data_dict = {}
    name_list = []
    name_list.append(['ru', 'zn', 'au', 'cu', 'pb', 'hc', 'rb', 'bu', 'ag', 'ni', 'sn', 'al'])
    name_list.append(['wr', 'zn', 'rb', 'al', 'bu', 'hc', 'cu', 'pb', 'sn', 'ru', 'ni', 'ag', 'au', 'fu'])
    name_list.append(['al', 'zn', 'ni', 'sn', 'cu', 'bu', 'ag', 'au', 'hc', 'pb', 'wr', 'fu', 'ru', 'rb'])
    name_list.append(['au', 'ru', 'bu', 'ag', 'hc', 'fu', 'zn', 'pb', 'al', 'cu', 'wr', 'rb'])
    for i in range(4):
        name_list[0] = set(name_list[0]).intersection(set(name_list[i]))
    item_classes = sorted(list(name_list[0]))
    print(item_classes)
    prices_array = []
    date_array = []
    begin = 2015
    for year in range(begin, 2019):
        dataframe = get_shfe_dataframe(year)
        print("year = ", year)
        cols = dataframe.columns.tolist()
        item_namelist = dataframe[cols[0]].tolist()
        prices_list = [get_item_prices(dataframe, item_class) for item_class in item_classes]
        for idx, item in enumerate(prices_list):
            prices = item[0]
            date = item[1]
            norm_prices = np.array((prices - np.mean(prices)) / np.std(prices))
            # not for norm
            if year == begin:
                prices_array.append(np.array(prices))
                date_array.append(np.array(date))
            else:
                prices_array[idx] = np.concatenate((prices_array[idx], prices))
                date_array[idx] = np.concatenate((date_array[idx], date))
    with open("../../data/shfe/date.txt", "w") as f:
        for idx in range(date_array[0].shape[0]):
            f.write(date_array[0][idx])
            f.write("\n")
    f = h5py.File("../../data/shfe/data.h5", "w")
    # 1 for Rb, 5 for Hc
    output = np.concatenate((prices_array[7].reshape(1, -1), prices_array[5].reshape(1, -1)))
    print(output.shape)
    f.create_dataset("data", data=output)
    f.close()
    # calc_person(prices_array, item_classes)


if __name__ == "__main__":
    process_data_combined()
