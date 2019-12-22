import george
from george import kernels
import numpy as np
import matplotlib.pyplot as plt
import re
fileIn = open("../../data/proceed/diff-2.txt")
# fileIn = open("../stage1-Correlation/Price-Diff.txt")
data = fileIn.readlines()
x, y, yerr = [], [], []
for i in data:
    tmp = re.split(r" |,|\n", i)
    # print(tmp)
    x.append(float(tmp[0]))
    y.append(-float(tmp[1]))
    yerr.append(-float(tmp[2]))
# yerr = 0
kernel = np.var(y) * kernels.ExpSquaredKernel(2.5)
gp = george.GP(kernel)
gp.compute(x, yerr)
x_pred = np.linspace(0, 974, 974)
scalar = 2.5
pred, pred_var = gp.predict(y, x_pred, return_var=True)
lower_bound = pred - scalar * np.sqrt(pred_var)
upper_bound = pred + scalar * np.sqrt(pred_var)
filter_size = 60
conv_filter = np.hanning(filter_size)
conv_filter /= conv_filter.sum()
lower_bound_conv = np.convolve(lower_bound, conv_filter, 'valid')
upper_bound_conv = np.convolve(upper_bound, conv_filter, 'valid')
# plt.fill_between(x_pred, lower_bound, upper_bound, color='red', alpha=0.5)
left = int(filter_size / 2 - 1)
right = int(974 - filter_size / 2)
plt.fill_between(x_pred[left:right], lower_bound_conv, upper_bound_conv, color='blue', alpha=0.5)
# left = 0
# right = 974
plt.plot(x_pred[left:right], pred[left:right], "black", alpha=1)
fin = open("diff-pred.txt", "r")
fdata = fin.readlines()
x_pred, y_pred = [], []
for i in range(len(fdata)):
    x_pred.append(i)
    y_pred.append(-float(fdata[i]))
# print(y_pred)
plt.scatter(x_pred, y_pred, s=15, c='green', marker='+')
length = len(x_pred)
# print(len(y_pred), len(lower_bound_conv), len(upper_bound_conv))
print("price\t\tlower\t\tupper\t\tstatus")
info = []
for i in range(length // 2, length):
    price, lower, upper = y_pred[i], lower_bound_conv[i - 1], upper_bound_conv[i - 1]
    info.append([i, price, lower, upper])
    if not (price >= lower and price <= upper):
        ch = ""
        if price < lower: ch = "low"
        else: ch = "high"
        # info.append([price, lower, upper, ch])
        print("%5f\t%5f\t%5f\t%s" % (price, lower, upper, ch)) 
# for i in range(len(y)):
#     y[i] += yerr[i]
# print(left, right)
# plt.scatter(x[left:right], y[left:right], s=15, c='green', marker='+')

# plt.errorbar(x, y, yerr=yerr, fmt="x", capsize=0)
plt.show()

for i in info:
    print(i)