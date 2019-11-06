import pandas as pd
import  os
from pandas import DataFrame
import numpy as np


def pare_data(dir):
    filename_list = list(os.walk(dir))[0][2]
    for filename in filename_list:
        singe_date_price = {}
        f = open(dir + '/' + filename)
        list_f = f.readlines()[1:]

        for i in range(len(list_f)):
                list_f[i] = list_f[i][:-2]
                list_f[i] = list_f[i].split(',')
                if year != '2015': #去引号
                    for j in range(len(list_f[i])):
                        list_f[i][j] = list_f[i][j][1:-1]

        price_max = 0
        price_min = 1e10
        for contract in list_f:
            if contract[2] not in singe_date_price:
                singe_date_price[contract[2]] = float(contract[9])
            elif singe_date_price[contract[2]] < float(contract[9]):
                singe_date_price[contract[2]] = float(contract[9])
            else:
                pass
            price_max = max(price_max,float(contract[9]))
            price_min = min(price_min,float(contract[9]))

        FuturesName = list_f[0][1][:-4]
        if year == '2014':
            print(FuturesName, "denotes", filename[:-4])
        for date in singe_date_price:
            singe_date_price[date]=(singe_date_price[date]-price_min)/(price_max-price_min) #归一化
        date_price[FuturesName] = singe_date_price



root="data/dce"
df=DataFrame({})
year_list=['2014','2015','2016']
for year in year_list:
    date_price={}
    dir = root + '/' + year
    pare_data(dir)
    df=df.append(DataFrame(date_price),sort=False)
print(df)

# index=df.index.values.tolist()
# for i in range(1,len(index)):
#     if int(index[i]) <= int(index[i-1]):
#         print("ERROR")
#         break

corr = df.corr()
print("corr matrix:\n",corr)

pd.set_option("display.max_rows",300)
corr_sort=corr.unstack().sort_values(axis=0,ascending=False)
print("sorted corr:\n",corr_sort)





