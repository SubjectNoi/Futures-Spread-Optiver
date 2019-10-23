# -*- coding: utf-8 -*- 
import re
import calendar
import datetime
import matplotlib.pyplot as plt
import numpy as np
data_path = "../../data/dce/2014/"
import os
data = {}
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
                if goodType not in data:
                    data[goodType] = []
                data[goodType].append(item_float)
    return True

file_reader(data_path, 2014)
data_path = "../../data/dce/2015/"
file_reader(data_path, 2015)
data_path = "../../data/dce/2016/"
file_reader(data_path, 2016)

def normalize(input_list):
    minN = 1e30
    maxN = -1
    for i in input_list:
        minN = min(minN, float(i[2]))
        maxN = max(maxN, float(i[2]))
    return minN, maxN

def plot_futures(begin, end, item_list):
    plot_dict = {}
    for keys in data:
        sorted_data_item = sorted(data[keys], key=lambda x: x[2])
        sub_data = {}
        for item in sorted_data_item:
            if str(item[2]) not in sub_data:
                sub_data[str(item[2])] = []
            sub_data[str(item[2])].append(item)

        tmp_plot_items = []
        for sub_keys in sub_data:
            sorted_sub_data_item = sorted(sub_data[sub_keys], key=lambda y: float(y[13]))
            plot_item = sorted_sub_data_item[-1]
            ch = plot_item[1][0:len(plot_item[1]) - 4]
            if int(plot_item[2]) >= begin and int(plot_item[2]) <= end and (ch in item_list or item_list[0] == "all"):
                tmp_plot_items.append([plot_item[1], int(plot_item[2]), float(plot_item[8])])
    
        plot_dict[keys] = tmp_plot_items

    plt.title("2014")
    for keys in plot_dict:
        x = []
        y = []
        minN, maxN = normalize(plot_dict[keys])
        if len(plot_dict[keys]) > 0:
            name = plot_dict[keys][0][0][0:len(plot_dict[keys][0][0]) - 4]
            # print(name)
            for i in plot_dict[keys]:
                date = datetime.datetime.strptime(str(i[1]), '%Y%m%d')
                axis = datetime.datetime.strptime("20140101", '%Y%m%d')
                x.append(date.__sub__(axis).days)
                y.append((float(i[2]) - minN) / (maxN - minN))
            plt.plot(x, y, label=name, linewidth=1)
            # plt.scatter(x, y, label=name, marker="+", s=15)
            # fproceed = open("../../data/proceed/pp.txt", "w+")
            # for i in range(len(x)):
            #     fproceed.write("%d, %f\n" % (x[i], y[i]))
    plt.legend()
    plt.show()

plot_futures(20140101, 20170101, ["y", "v"])
# [j, jm, v, i], [l, pp], [c, cs], [v, y], [jd, m], [a], [b], [bb], [fb] ? [i, p]