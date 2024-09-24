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

Nf = 10
z = np.zeros(N, float)
b = np.zeros(Nf, float)
Fb = np.zeros(Nf, float)

# to find Fourie coeff
for k in range(1, Nf):
    if k % 2 == 0:  # even
        b[k] = 0
    else:  # odd
        b[k] = 2 / pi / k

for n in range(1, N):
    x[n] = x[n - 1] + dx
    z[n] = b[1] * sin(x[n])
    for k in range(2, Nf):
        z[n] = z[n] + b[k] * sin(k * x[n])

plt.plot(x, z, '-b')
plt.plot(x, y, '--r')
plt.grid()
plt.show()
