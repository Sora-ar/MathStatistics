import numpy as np
import matplotlib.pyplot as plt


# Define the function for rectangular pulse
def rectangular_pulse(t):
    return np.where(np.abs(t) <= np.pi / 2, 1, 0)


# Fourier Series approximation for the rectangular pulse
def fourier_series_rectangular_pulse(t, N):
    f_approx = 0.5  # DC component (a_0 term)
    for n in range(1, N + 1):
        # Fourier coefficients for sine terms (b_n)
        f_approx += (2 / (n * np.pi)) * np.sin(n * np.pi / 2) * np.sin(n * t)
    return f_approx


# Time domain from -pi to pi
t = np.linspace(-np.pi, np.pi, 1000)

# Plot the Fourier approximations with different N values
plt.figure(figsize=(10, 6))
for N in [1, 3, 5, 10, 50]:
    f_approx = fourier_series_rectangular_pulse(t, N)
    plt.plot(t, f_approx, label=f'N = {N}')

# Original rectangular pulse
plt.plot(t, rectangular_pulse(t), 'k', label='Original Function', linewidth=2)

# Graph labeling
plt.title('Fourier Series Approximation of a Rectangular Pulse')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.show()


# Fourier Series approximation for y(t) = t
def fourier_series_t_function(t, N):
    f_approx = 0  # y(t) = t has no constant term
    for n in range(1, N + 1):
        # Fourier coefficients for sine terms (b_n)
        f_approx += (-2 * (-1) ** n) / n * np.sin(n * t)
    return f_approx


# Plot the Fourier approximations for y(t) = t with different N values
plt.figure(figsize=(10, 6))
for N in [1, 3, 5, 10, 50]:
    f_approx = fourier_series_t_function(t, N)
    plt.plot(t, f_approx, label=f'N = {N}')

# Original function y(t) = t
plt.plot(t, t, 'k', label='y(t) = t', linewidth=2)

# Graph labeling
plt.title('Fourier Series Approximation of y(t) = t')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.show()
