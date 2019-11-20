import george
from george import kernels
import numpy as np
import matplotlib.pyplot as plt
import re
fileIn = open("../../data/proceed/LSTM-GPR.txt")
# fileIn = open("../stage1-Correlation/Price-Diff.txt")
data = fileIn.readlines()
x, y, yerr = [], [], []
for i in data:
    tmp = re.split(r" |,|\n", i)
    print(tmp)
    x.append(float(tmp[0]))
    y.append(float(tmp[1]))
    yerr.append(float(tmp[2]))
# yerr = 0
kernel = np.var(y) * kernels.ExpSquaredKernel(5)
gp = george.GP(kernel)
gp.compute(x, yerr)
x_pred = np.linspace(0, 974, 200)
pred, pred_var = gp.predict(y, x_pred, return_var=True)
plt.fill_between(x_pred, pred - np.sqrt(pred_var), pred + np.sqrt(pred_var), color='k', alpha=0.2)
plt.plot(x_pred, pred, "k", lw=0.2, alpha=0.5)

# plt.errorbar(x, y, yerr=yerr, fmt="x", capsize=0)
plt.show()