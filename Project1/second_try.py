from math import *
import numpy as np
import matplotlib.pyplot as plt

N = int(100)
x = np.zeros(N, float)
y = np.zeros(N, float)

x0 = -pi
xn = pi
dx = (xn - x0) / N
x[0] = x0

for n in range(1, N):
    x[n] = x[n - 1] + dx

    if (x[n] > -pi) and (x[n] < 0):
        y[n] = -1 / 2
    elif (x[n] > 0) and (x[n] < pi):
        y[n] = 1 / 2

plt.plot(x, y, '--r')
plt.grid()
plt.show()
