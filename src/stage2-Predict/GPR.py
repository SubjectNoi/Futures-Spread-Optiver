import george
from george import kernels
import numpy as np
import matplotlib.pyplot as plt
import re
import math
fileIn = open("../../data/proceed/diff-2.txt")
# fileIn = open("../stage1-Correlation/Price-Diff.txt")
data = fileIn.readlines()
x, y, yerr = [], [], []
xhc, xrb = [], []
for i in data:
    tmp = re.split(r" |,|\n", i)
    # print(tmp)
    x.append(float(tmp[0]))
    y.append(float(tmp[1]))
    yerr.append(float(tmp[2]))
    xhc.append(float(tmp[4]))
    xrb.append(float(tmp[3]))
# yerr = 0
kernel = np.var(y) * kernels.ExpSquaredKernel(2.5)
gp = george.GP(kernel)
gp.compute(x, yerr)
x_pred = np.linspace(0, 974, 974)
scalar = 2
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
xhc, xrb = xhc[left:right], xrb[left:right]
plt.fill_between(x_pred[left:right], lower_bound_conv, upper_bound_conv, color='blue', alpha=0.5)
# left = 0
# right = 974
plt.plot(x_pred[left:right], pred[left:right], "black", alpha=1)
fin = open("diff-pred.txt", "r")
fdata = fin.readlines()
x_pred, y_pred = [], []
for i in range(len(fdata)):
    x_pred.append(i + filter_size //2)
    y_pred.append(float(fdata[i]))
# print(y_pred)
plt.scatter(x_pred, y_pred, s=15, c='green', marker='+')
length = len(x_pred)
print(len(y_pred), len(lower_bound_conv), len(upper_bound_conv), len(xhc), len(xrb))
print("price-Diff\tlower\t\tupper\t\tstatus")
info = []
funding = 200000
rate = 0.3
money = funding * rate
for i in range(length):
    price_diff_pred, lower, upper = y_pred[i], lower_bound_conv[i - 1], upper_bound_conv[i - 1]
    hc, rb = xhc[i], xrb[i]
    cnt = 0
    if price_diff_pred < lower:
        cnt = -math.floor(money / (hc + rb))
    if price_diff_pred > upper:
        cnt = math.floor(money / (hc + rb))
    print("%d, %f, %f, %d, %f, %f, %f" % (i, hc, rb, cnt, -price_diff_pred, -upper, -lower))
    # if not (price_diff_pred >= lower and price_diff_pred <= upper):
    #     ch = ""
    #     if price_diff_pred < lower: ch = "low"
    #     else: ch = "high"
    #     # info.append([price, lower, upper, ch])
    #     print("%5f\t%5f\t%5f\t%5f\t%5f\t%s" % (price_diff_pred, hc, rb, lower, upper, ch)) 
# for i in range(len(y)):
#     y[i] += yerr[i]
# print(left, right)
# plt.scatter(x[left:right], y[left:right], s=15, c='green', marker='+')

# plt.errorbar(x, y, yerr=yerr, fmt="x", capsize=0)
plt.show()


# floor(funding / (hc + rb)) = cnt