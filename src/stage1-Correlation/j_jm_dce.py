import re
import calendar
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats 
import statsmodels.tsa.stattools as st
data_path = "../data/dce/2014/"
import os
data = {}
typelist = []
final_result = []
def file_reader(file_dir, year):
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            f = open(data_path + str(file_name), encoding='utf-8', errors='ignore')
            tmpf = f.readlines()    
            del(tmpf[0])
            for items in tmpf:
                item = re.split(r",|\n", items)  #此处得到一个数组，切分方法是逗号或者空格
                item_float = []
                for tmp in item:
                    if year == 2015:
                        item_float.append(str(tmp))
                    else:
                        item_float.append((str(tmp)[1:len(tmp)-1]).strip())
                if year == 2015:
                    goodType = item[1][0:len(item[1]) - 4]   #在文本编辑器中打开2015年的数据可以看到，每个项目少一对引号。
                else:
                    goodType = item[1][1:(len(item[1]) - 5)]
                if goodType not in data:
                    data[goodType] = []
                data[goodType].append(item_float)
                #print(goodType)
        #print(data['pp'])
    return True

file_reader(data_path, 2014)
data_path = "../data/dce/2015/"
file_reader(data_path, 2015)
data_path = "../data/dce/2016/"
file_reader(data_path, 2016)

def normalize(input_list):
    minN = 1e30
    maxN = -1
    for i in input_list:
        minN = min(minN, float(i[2]))
        maxN = max(maxN, float(i[2]))
    return minN, maxN

def cauculate_granger(begin, end):
    plot_dict = {}
    for keys in data:
        sorted_data_item = sorted(data[keys], key=lambda x: x[2])
        sub_data = {}
        for item in sorted_data_item:
            if str(item[2]) not in sub_data:
                sub_data[str(item[2])] = []
            sub_data[str(item[2])].append(item)     #字典索引是日期，sub_data按照日期存储每日的交易内容

        tmp_plot_items = []
        for sub_keys in sub_data:
            sorted_sub_data_item = sorted(sub_data[sub_keys], key=lambda y: float(y[13]))   #找出主力合约
            plot_item = sorted_sub_data_item[-1]           #代表主力合约的交易信息
            ch = plot_item[1][0:len(plot_item[1]) - 4]     #应该是主力合约的收盘价？
            if int(plot_item[2]) >= begin and int(plot_item[2]) <= end and (ch == "j" or ch == "jm"):   #起止日期和绘图中显示的品种的划分
                tmp_plot_items.append([plot_item[1], int(plot_item[2]), float(plot_item[8])])   #品种，合约日期，收盘价
        plot_dict[keys] = tmp_plot_items
    print(plot_dict["jm"][2])
       


    #plt.title("2014")
    final_type = []
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
            final_type.append(y)
            #plt.plot(x, y, label=name, linewidth=1)
            #plt.scatter(x, y, label=name, marker="+", s=15)
            #fproceed = open("../../data/proceed/pp.txt", "w+")
            #for i in range(len(x)):
                #fproceed.write("%d, %f\n" % (x[i], y[i]))

            #plt.legend()
            #plt.show()
    j_list = []
    jm_list = []
    for item in final_type[0]:
        j_list.append(item)
    for item in final_type[1]:
        jm_list.append(item)
    print(j_list)
    print(jm_list)
    print(st.grangercausalitytests(np.mat([j_list, jm_list]).T, maxlag=3)) # 格兰杰因果关系检验

if (__name__ == '__main__'):
    cauculate_granger(20140101, 20180101)
