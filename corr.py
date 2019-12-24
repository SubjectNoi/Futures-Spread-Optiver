import pandas as pd
import  os
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint
import  statsmodels.api as sm

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
            # price_max = max(price_max,float(contract[9]))
            # price_min = min(price_min,float(contract[9]))

        FuturesName = list_f[0][1][:-4]
        if year == '2014':
            print(FuturesName, "denotes", filename[:-4])
        # for date in singe_date_price:
        #     singe_date_price[date]=(singe_date_price[date]-price_min)/(price_max-price_min) #归一化
        date_price[FuturesName] = singe_date_price



root="data/dce"
df=DataFrame({})
year_list=['2014','2015','2016']
# year_list=['2014']
for year in year_list:
    date_price={}
    dir = root + '/' + year
    pare_data(dir)
    df=df.append(DataFrame(date_price),sort=False)
print("/************************2014-2016*************************/")
print(df,"\n")

index=df.index.values.tolist()
for i in range(1,len(index)):
    if int(index[i]) <= int(index[i-1]):
        print("ERROR")
        break

#相关系数计算
corr = df.corr()
print("/************************corr matrix*************************/:\n",corr,"\n")

pd.set_option("display.max_rows",300)
corr_sort=corr.unstack().sort_values(axis=0,ascending=False)
print("/************************sorted corr*************************/\n",corr_sort,"\n")

j=pd.Series(df['j'].values,index=df['j'].index)
jm=pd.Series(df['jm'].values,index=df['jm'].index)

# 对j，jm的原始时间序列进行单位根校验
print("/************************j,jm ADF校验*************************/")
result_j = adfuller(j,regression='ct')
print(result_j)
result_jm = adfuller(jm,regression='ct')
print(result_jm)

result_j = adfuller(j,regression='c')
print(result_j)
result_jm = adfuller(jm,regression='c')
print(result_jm)

result_j = adfuller(j,regression='nc')
print(result_j)
result_jm = adfuller(jm,regression='nc')
print(result_jm)

# 对j，jm一阶差分后的时间序列进行单位根校验
j_diff=np.diff(j)
jm_diff=np.diff(jm)

result_j_diff=adfuller(j_diff,regression='ct')
print(result_j_diff)
result_jm_diff=adfuller(jm_diff,regression='ct')
print(result_jm_diff)

result_j_diff=adfuller(j_diff,regression='c')
print(result_j_diff)
result_jm_diff=adfuller(jm_diff,regression='c')
print(result_jm_diff)

result_j_diff=adfuller(j_diff,regression='nc')
print(result_j_diff)
result_jm_diff=adfuller(jm_diff,regression='nc')
print(result_jm_diff)

print("\n")

#j，jm协整检验
print("/************************j,jm 协整检验*************************/")
print(coint(j, jm))
print("\n")

# #OLS求jm,j的线性关系
x = sm.add_constant(np.array(jm))
y = np.array(j)
model = sm.OLS(y,x)
results = model.fit()
# print(results.summary())
print("/************************j，jm 价格序列线性关系*************************/")
print("j = {}*jm{}\n".format(results.params[1],results.params[0]))

##画出j，jm价格走势
plt.figure()
plt.title('j,jm price(2014-2016)')
j.plot()
jm.plot()

##画出j，jm价格关系
plt.figure()
plt.title('linearity between j and jm')
x = np.array(jm)
y_fitted = results.fittedvalues
plt.plot(x,y,'o',label = 'data')
plt.plot(x,y_fitted,'r--',label = 'OLS')
plt.xlabel('price of jm')
plt.ylabel('price of j')
plt.legend()
plt.show()











