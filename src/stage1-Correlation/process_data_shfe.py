import os
import numpy as np
import pandas as pd
import math
from pprint import pprint
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as st

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


def get_shfe_dataframe(year=2018):
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
    return list(price_dict.values())


def process_data():
    dataframe = get_shfe_dataframe()
    print(dataframe.head(3))
    print("dataframe shape = ", dataframe.shape)
    cols = dataframe.columns.tolist()
    item_namelist = dataframe[cols[0]].tolist()
    # pprint(list(set(item_namelist)), indent=2)
    item_classes = list(set([item[0:2] for item in item_namelist]))
    # print(item_classes)
    prices_list = [get_item_prices(dataframe, item_class) for item_class in item_classes]
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
    tot = len(item_classes)
    corr_pairs = []
    for i in range(tot):
        for j in range(i + 1, tot):
            corr_value = computeCorrelation(prices_array[i], prices_array[j])
            corr_pairs.append((corr_value, i, j))
    corr_pairs = sorted(corr_pairs)
    corr_pairs.reverse()
    for i in range(min(len(corr_pairs), 5)):
        value = corr_pairs[i][0]
        item1 = item_classes[corr_pairs[i][1]]
        item2 = item_classes[corr_pairs[i][2]]
        print("{} via {}, value: {:.4f}".format(item1, item2, value))
    # x = list(range(len_t))
    # plt.title("shfe18")
    # plt.xlabel("product")
    # plt.ylabel("prices")
    # for idx, prices in enumerate(prices_array):
    #     plt.plot(x, prices, label=name_array[idx])
    # plt.legend()
    # plt.show()
    # tot = len(prices_array)
    # for i in range(tot):
    #     for j in range(i + 1, tot):
    #         print("{} via {}".format(name_array[i], name_array[j]))
    #         print("相关系数r:", computeCorrelation(prices_array[i], prices_array[j]))
    #         print("简单线性回归r^2:", str(computeCorrelation(prices_array[i], prices_array[j]) ** 2))


if __name__ == "__main__":
    # process_data()
    df = get_shfe_dataframe()
    xhc, xrb = get_item_prices(df, "hc"), get_item_prices(df, "rb")
    # print(st.adfuller(xhc))
    # print(st.adfuller(xrb)) # 单位根检验ADF

    # print(np.mat([xhc, xrb]).shape)
    # print(st.grangercausalitytests(np.mat([xhc, xrb]).T, maxlag=3)) # 格兰杰因果关系检验
    f = open("diff.txt", "w+")
    Diff = (np.mat(xhc) - np.mat(xrb)).tolist()
    maxN, minN = max(Diff[0]), min(Diff[0])
    print(Diff[0])
    out = [(i - minN) / (maxN - minN) for i in Diff[0]]
    for i in out:
        f.write(str(i) + "\n")