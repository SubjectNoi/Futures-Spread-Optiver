# -*- coding: utf-8 -*- 
import re
import calendar
import datetime
import matplotlib.pyplot as plt
data_path = "../../data/dce/2014/"
import os
data = {}
def file_reader(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            f = open(data_path + str(file_name), encoding='utf-8', errors='ignore')
            tmpf = f.readlines()
            for items in tmpf:
                item = re.split(r",|\n", items)
                item_float = []
                for tmp in item:
                    item_float.append(str(tmp)[1:len(tmp)-1])
                    # item_float.append(str(tmp))
                goodType = item[1][1:(len(item[1]) - 5)]
                if goodType not in data:
                    data[goodType] = []
                data[goodType].append(item_float)
    return True

file_reader(data_path)

def normalize(input_list):
    minN = 1e30
    maxN = -1
    for i in input_list:
        minN = min(minN, float(i[2]))
        maxN = max(maxN, float(i[2]))
    return minN, maxN



def plot_futures(begin, end):
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
            if int(plot_item[2]) >= begin and int(plot_item[2]) <= end:
                tmp_plot_items.append([plot_item[1], int(plot_item[2]), float(plot_item[13])])
    
        plot_dict[keys] = tmp_plot_items

    plt.title("2014")
    for keys in plot_dict:
        x = []
        y = []
        minN, maxN = normalize(plot_dict[keys])
        for i in plot_dict[keys]:
            date = datetime.datetime.strptime(str(i[1]), '%Y%m%d')
            axis = datetime.datetime.strptime("20140101", '%Y%m%d')
            x.append(date.__sub__(axis).days)
            y.append((float(i[2]) - minN) / (maxN - minN))
        plt.plot(x, y)

    plt.show()

plot_futures(20140101,20140201)