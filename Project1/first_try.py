from math import *
import numpy as np
import matplotlib.pyplot as plt

N = int(100)
x = np.zeros(N, float)
y = np.zeros(N, float)
x0 = 0
xn = 10
dx = (xn - x0) / N
x[0] = x0
for n in range(1, N):
    x[n] = x[n - 1] + dx
    y[n] = x[n] ** 2 * sin(x[n])
plt.plot(x, y, '--r')
plt.grid()
plt.show()
