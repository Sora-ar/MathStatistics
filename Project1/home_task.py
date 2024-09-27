import numpy as np
import matplotlib.pyplot as plt
from math import pi, sin

N = 100
x = np.linspace(-pi, pi, N)
y = np.zeros(N, float)

# Defining the rectangular pulse
for n in range(N):
    if -pi < x[n] < 0:
        y[n] = -1 / 2
    elif 0 < x[n] < pi:
        y[n] = 1 / 2


# Function to plot Fourier approximation for different Nf
def fourier_approximation(Nf, x, y):
    b = np.zeros(Nf, float)
    z = np.zeros_like(x)

    # Finding Fourier coefficients
    for k in range(1, Nf):
        if k % 2 == 0:
            b[k] = 0
        else:
            b[k] = 2 / pi / k

    # Constructing Fourier series
    for n in range(N):
        for k in range(1, Nf):
            z[n] += b[k] * sin(k * x[n])

    # Plotting the result
    plt.plot(x, z, '-b', label=f'Nf = {Nf}')
    plt.plot(x, y, '--r', label='Rectangular pulse')
    plt.title(f'Fourier Approximation with Nf = {Nf}')
    plt.grid(True)
    plt.legend()
    plt.show()


for Nf in [5, 10, 20, 30, 40, 50]:
    fourier_approximation(Nf, x, y)

# Fourier approximation for sawtooth signal

N = 100
x = np.linspace(-pi, pi, N)
y = x


def fourier_approximation_sawtooth(Nf, x, y):
    z = np.zeros_like(x)

    # Calculating Fourier coefficients and constructing Fourier series
    b = np.zeros(Nf, float)

    for k in range(1, Nf):
        b[k] = -2 * ((-1) ** k) / k

    z = np.zeros(len(x), float)
    for k in range(1, Nf):
        z += b[k] * np.sin(k * x)

    # Plotting the result
    plt.plot(x, z, '-b', label=f'Nf = {Nf}')
    plt.plot(x, y, '--r', label='Sawtooth signal')
    plt.title(f'Fourier Approximation for Sawtooth Signal (Nf = {Nf})')
    plt.grid(True)
    plt.legend()
    plt.show()


# Test with different values of Nf
for Nf in [5, 10, 20, 30, 40, 50]:
    fourier_approximation_sawtooth(Nf, x, y)
