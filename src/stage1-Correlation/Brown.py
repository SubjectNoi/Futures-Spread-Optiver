import matplotlib.pyplot as plt

f = open("./diff.txt")
data = f.readlines()
x1 = []
origin = []
pre = 0
d1 = 0
d2 = 0
diff1 = []
diff2 = []
for i in range(0, len(data), 1):
    x1.append(i)
    origin.append(float(data[i]))
    diff = float(data[i]) - pre
    pre = float(data[i])
    d1 += abs(diff)
    d2 += (diff ** 2)
    diff1.append(d1)
    diff2.append(d2)

pre = 0
d3 = 0
d4 = 0
diff3 = []
diff4 = []
x2 = []
for i in range(0, len(data), 3):
    x2.append(i)
    diff = float(data[i]) - pre
    pre = float(data[i])
    d3 += abs(diff)
    d4 += (diff ** 2)
    diff3.append(d3)
    diff4.append(d4)

pre = 0
d5 = 0
d6 = 0
diff5 = []
diff6 = []
x3 = []
for i in range(0, len(data), 5):
    x3.append(i)
    diff = float(data[i]) - pre
    pre = float(data[i])
    d5 += abs(diff)
    d6 += (diff ** 2)
    diff5.append(d5)
    diff6.append(d6)

plt.ylim((0, 10))
plt.plot(x1, origin, label="Origin Data")
plt.plot(x1, diff1, label="First order variation - 1")
plt.plot(x1, diff2, label="Second order variation - 1")
plt.plot(x2, diff3, label="First order variation - 3")
plt.plot(x2, diff4, label="Second order variation - 3")
plt.plot(x3, diff5, label="First order variation - 5")
plt.plot(x3, diff6, label="Second order variation - 5")
plt.legend()
plt.show()