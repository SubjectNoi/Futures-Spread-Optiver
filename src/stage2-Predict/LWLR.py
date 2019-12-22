import numpy as np 
import matplotlib.pyplot as plt 

def loadData(filename):
    fdata = open(filename, "r")
    data = fdata.readlines()
    xArr = []
    yArr = []
    cnt = 0
    for item in data:
        lineArr = []
        curLine = item.split(",")
        lineArr.append(float(curLine[0]))
        xArr.append(lineArr)
        yArr.append(float(curLine[-1]))
        cnt += 1
        # if cnt == 200:
        #     break
    return xArr, yArr



def lwlr(testPoint, xArr, yArr, k=1.0):
    xMat = np.mat(xArr)
    yMat = np.mat(yArr).T
    m = np.shape(xMat)[0]
    weight = np.mat(np.eye(m))

    for j in range(m):
        diffMat = testPoint - xMat[j,:]
        weight[j, j] = np.exp(diffMat * diffMat.T / -2.0*k**2)
    xTx = xMat.T * (weight * xMat)
    ws = xTx.I * (xMat.T * (weight * yMat))
    return testPoint * ws

def lwlrTest(testArr, xArr, yArr, k=1.0):
    m = np.shape(testArr)[0]
    yHat = np.zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat

# xArr, yArr = loadData("../../data/proceed/jm.txt")
xArr, yArr = loadData("../stage1-Correlation/diff-lwlr.txt")

k = 2
yHat = lwlrTest(xArr, xArr, yArr, k / 100.0)
fin = open("../../data/proceed/diff-%d.txt" % (k), "w+")
for i in range(len(yHat)):
    fin.write(str(i) + "," + str(yHat[i]) + "," + str(yHat[i] - yArr[i]) + "\n")
fin.close()
xPlotArr = [x[0] for x in xArr]
plt.title("Predict")
plt.scatter(xPlotArr, yArr, s=15, marker="+")
plt.plot(xPlotArr, yHat, c='crimson')
plt.show()