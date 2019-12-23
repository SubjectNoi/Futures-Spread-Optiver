import torch
from torch.autograd import Variable
import torch.nn as nn
import pandas as pd 
from pandas import DataFrame
import matplotlib.pyplot as plt 
import numpy as np 

DATA_STEP = 60
HIDDEN_CELL = 120
LEARNING_RATE = 0.02
MAX_ITER = 500
TRAIN_PERCENTAGE = 0.4

df = pd.read_excel(r"../../data/proceed/diff.xls")
datas = df.values
x = range(0, len(datas))
# Normalize
max_value = np.max(datas)
min_value = np.min(datas)
# plt.title("LSTM predict")
# plt.scatter(x, datas, s=20, marker='+')
# plt.show()
datas = list(map(lambda x: (x - min_value) / (max_value - min_value), datas))

def create_dataset(datas, look_back):
    data_x = []
    data_y = []
    for i in range(len(datas) - look_back):
        data_x.append(datas[i:i + look_back])
        data_y.append(datas[i + look_back])
    return np.asarray(data_x), np.asarray(data_y)

dataX, dataY = create_dataset(datas, DATA_STEP)

train_size = int(len(dataX) * TRAIN_PERCENTAGE)
axisX = []
axisY = []
eps, step = -400, 800 / 100
for i in range(100):
    axisX.append(float(train_size))
    axisY.append(eps)
    eps += step
trainX = dataX[:train_size]
trainY = dataY[:train_size]
trainX = trainX.reshape(-1, 1, DATA_STEP)
trainY = trainY.reshape(-1, 1, 1)
trainX = torch.from_numpy(trainX).cuda()
trainY = torch.from_numpy(trainY).cuda()

class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()
        self.lstm = nn.LSTM(DATA_STEP, HIDDEN_CELL, 2)
        self.out = nn.Linear(HIDDEN_CELL, 1)
    
    def forward(self, x):
        x1, _ = self.lstm(x)
        a, b, c = x1.shape
        out = self.out(x1.view(-1, c))
        return out.view(a, b, -1)

rnn = RNN()
rnn.cuda()
optimizer = torch.optim.Adam(rnn.parameters(), lr=LEARNING_RATE)
loss_function = nn.MSELoss()


for i in range(MAX_ITER):
    var_x = Variable(trainX).type(torch.FloatTensor).cuda()
    var_y = Variable(trainY).type(torch.FloatTensor).cuda()
    out = rnn(var_x)
    loss = loss_function(out, var_y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (i + 1) % 100 == 0:
        print("Epoch:{}, Loss:{:.5f}".format(i + 1, loss.item()))

dataX1 = dataX.reshape(-1, 1, DATA_STEP)
dataX2 = torch.from_numpy(dataX1)
var_dataX = Variable(dataX2).type(torch.FloatTensor).cuda()
pred = rnn(var_dataX).cuda()
print(min_value, max_value)
pred_test = pred.cpu().view(-1).data.numpy()
pred_test = pred_test * (max_value - min_value) + min_value
dataY = dataY * (max_value - min_value) + min_value
print(pred_test)
f = open("diff-pred.txt", "w+")
for i in pred_test:
    f.write(str(i) + "\n")
f.close()
plt.plot(pred_test, 'r', label='prediction')
plt.plot(dataY, 'b', label='real')
plt.plot(axisX, axisY, 'g')
plt.legend(loc='best')
plt.show()