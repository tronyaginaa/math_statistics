import numpy as np
import matplotlib.pyplot as plt
import load


def subinterval_frequencies_and_mode(A, B, eps, data):
    y = []
    for i in range(0, len(data)):
        y.append(data[i] + eps - (A + B * i))
        y.append(data[i] - eps - (A + B * i))

    y = list(set(y))
    y.sort()

    z = []

    for i in range(0, len(y) - 1):
        z.append([y[i], y[i + 1]])

    max_mu = 0
    coefs = []
    mus = []

    for i in range(0, len(z)):
        mu = 0
        for j in range(0, len(data)):
            if data[j] - eps - (A + B * j) <= z[i][0] and data[j] + eps - (A + B * j) >= z[i][1]:
                mu += 1
        mus.append(mu)

        if mu > max_mu:
            max_mu = mu
            coefs = []
            coefs.append(i)

        if mu == max_mu:
            coefs.append(i)

    mode = []

    for i in range(0, len(z)):
        if i in coefs:
            mode.append(z[i])

    for k in range(0, len(mode) - 1):
        if mode[k][1] == mode[k + 1][0]:
            mode[k] = [mode[k][0], mode[k + 1][1]]

    return mode, max_mu, z, mus

def show_plots(data, eps, A1, B1, A0, B0):
    result_0 = subinterval_frequencies_and_mode(A0, B0, eps, data)
    result_1 = subinterval_frequencies_and_mode(A1, B1, eps, data)
    mode_0 = result_0[0]
    mode_1 = result_1[0]
    max_mu_0 = result_0[1]
    max_mu_1 = result_1[1]
    z_0 = np.array(result_0[2])
    z_1 = np.array(result_1[2])
    mu_0 = result_0[3]
    mu_1 = result_1[3]
    plt.figure()
    plt.plot(z_0[:, 0], mu_0, linewidth=0.5)
    plt.plot(z_1[:, 0], mu_1, linewidth=0.5)
    plt.xlabel('mV')
    plt.ylabel('mu')
    plt.savefig('mu.png')
    plt.show()
    print(f'mode_0 = {mode_0} mu_max_0 = {max_mu_0}')
    print(f'mode_1 = {mode_1}, mu_max_1 = {max_mu_1}')