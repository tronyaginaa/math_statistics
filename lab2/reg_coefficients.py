import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import os


def ls_coefficients(x, y):
    xy = np.mean(np.multiply(x, y))
    xx = np.mean(np.multiply(x, x))
    x_m = np.mean(x)
    y_m = np.mean(y)
    b1 = (xy - x_m * y_m) / (xx - x_m * x_m)
    b0 = y_m - x_m * b1
    print('a', b0, 'b', b1)
    return b0, b1

def abs_dev_val(b_arr, x, y):
    return np.sum(np.abs(y - b_arr[0] - b_arr[1] * x))

def labs_cefficients(x, y):
    init_b = np.array([0, 1])
    res = minimize(abs_dev_val, init_b, args=(x, y))
    print(res.x)
    return res.x

def coefficients():
    if not os.path.isdir("graphics"):
        os.makedirs("graphics")

    x = np.arange(-1.8, 2.1, 0.2)
    e = np.random.normal(0, 1, size=20)
    y = np.full(20, 2) + (x * 2 + e)
    # y2 with noise
    noise_y = np.copy(y)
    noise_y[0] += 10
    noise_y[19] += -10

    coeff_app = labs_cefficients(x, y)
    coeff_ls = ls_coefficients(x, y)
    noise_coeff_app = labs_cefficients(x, noise_y)
    noise_coeff_ls = ls_coefficients(x, noise_y)

    app = np.full(20, coeff_app[0]) + x * coeff_app[1]
    ls =  np.full(20, coeff_ls[0]) + x * coeff_ls[1]

    noise_app = np.full(20, noise_coeff_app[0]) + x * noise_coeff_app[1]
    noise_ls = np.full(20, noise_coeff_ls[0]) + x * noise_coeff_ls[1]
    #
    #
    plt.plot(x, y, "k.", label='Выборка')
    plt.plot(x, app, label='МНМ')
    plt.plot(x, ls, label='МНК')
    plt.plot(x, y - e, label='Модель')
    plt.grid()
    plt.title("Выборка без возмущения")
    plt.legend()
    plt.savefig("graphics/reg.png")

    plt.cla()

    plt.plot(x, noise_y, "k.", label='Выборка')
    plt.plot(x, noise_app, label='МНМ')
    plt.plot(x, noise_ls, label='МНМ')
    plt.plot(x, y - e, label='Модель')
    plt.grid()
    plt.legend()
    plt.title("Выборка с возмущением")
    plt.savefig("graphics/noise_reg.png")
