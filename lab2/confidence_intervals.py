import numpy as np
from scipy.stats import chi2, t, norm, moment
import os
import matplotlib.pyplot as plt

gamma = 0.95
alpha = 1 - gamma

def st_mo(samples, alpha):
    med = np.mean(samples)
    n = len(samples)
    s = np.std(samples)
    t_a = t.ppf(1 - alpha / 2, n - 1)
    q_1 = med - s * t_a / np.sqrt(n - 1)
    q_2 = med + s * t_a / np.sqrt(n - 1)
    return q_1, q_2

def ch_sigma(samples, alpha):
    n = len(samples)
    s = np.std(samples)
    q_1 =  s * np.sqrt(n) / np.sqrt(chi2.ppf(1 - alpha / 2, n - 1))
    q_2 = s * np.sqrt(n) / np.sqrt(chi2.ppf(alpha / 2, n - 1))
    return q_1, q_2

def mu(samples, alpha):
    med = np.mean(samples)
    n = len(samples)
    s = np.std(samples)
    u = norm.ppf(1 - alpha / 2)
    q_1 = med - s * u / np.sqrt(n)
    q_2 = med + s * u / np.sqrt(n)
    return q_1, q_2

def sigma(samples, alpha):
    n = len(samples)
    s = np.std(samples)
    u = norm.ppf(1 - alpha / 2)
    m4 = moment(samples, 4)
    e = m4 / (s * s * s * s)
    U = u * np.sqrt((e + 2) / n)
    q_1 = s / np.sqrt(1 + U)
    q_2 = s / np.sqrt(1 - U)
    return q_1, q_2

def intervals():
    if not os.path.isdir("graphics"):
        os.makedirs("graphics")

    samples20 = np.random.normal(0, 1, size=20)
    samples100 = np.random.normal(0, 1, size=100)

    student_20 = st_mo(samples20, alpha)
    student_100 = st_mo(samples100, alpha)

    chi_20 = ch_sigma(samples20, alpha)
    chi_100 = ch_sigma(samples100, alpha)

    as_mo_20 = mu(samples20, alpha)
    as_mo_100 = mu(samples100, alpha)

    as_d_20 = sigma(samples20, alpha)
    as_d_100 = sigma(samples100, alpha)

    fig, ax = plt.subplots(1, 2)
    fig.set_figheight(9.6)
    fig.set_figwidth(12.8)
    plt.subplots_adjust(wspace = 0.5)
    ax[0].set_ylim([0,1])
    ax[0].hist(samples20, 10, density = 1, edgecolor = 'black')
    ax[0].set_title('N(0,1) hist, n = 20')
    ax[0].plot([as_mo_20[0], as_mo_20[0]], [0, 1], color='r', marker = '.', linewidth = 1, label = 'min_mo')
    ax[0].plot([as_mo_20[1], as_mo_20[1]], [0, 1], color='r', marker = '.', linewidth = 1, label = 'max_mo')
    ax[0].plot([as_mo_20[0] - as_d_20[1], as_mo_20[0] - as_d_20[1]], [0, 1], color='g', marker = '.', linewidth = 1, label = 'min_mo - max_sigma')
    ax[0].plot([as_mo_20[1] + as_d_20[1], as_mo_20[1] + as_d_20[1]], [0, 1], color='g', marker = '.', linewidth = 1, label = 'max_mo - max_sigma')
    ax[1].set_ylim([0,1])
    ax[1].hist(samples100, 10, density = 1, edgecolor = 'black')
    ax[1].set_title('N(0,1) hist, n = 100')
    ax[1].plot([as_mo_100[0], as_mo_100[0]], [0, 1], color='r', marker='.', linewidth=1, label='min_mo')
    ax[1].plot([as_mo_100[1], as_mo_100[1]], [0, 1], color='r', marker='.', linewidth=1, label='max_mo')
    ax[1].plot([as_mo_100[0] - as_d_100[1], as_mo_100[0] - as_d_100[1]], [0, 1], color='g', marker='.', linewidth=1, label='min_mo - max_sigma')
    ax[1].plot([as_mo_100[1] + as_d_100[1], as_mo_100[1] + as_d_100[1]], [0, 1], color='g', marker='.', linewidth=1, label='max_mo - max_sigma')
    plt.savefig('graphics/hist.png')

    fig, ax = plt.subplots(2, 2)
    fig.set_figheight(9.6)
    fig.set_figwidth(12.8)
    plt.subplots_adjust(wspace = 0.5, hspace = 1)

    ax[0][0].plot([student_20[0], student_20[1]], [0.3, 0.3], color='r', marker = '.', linewidth = 1, label = 'm interval, n = 20')
    ax[0][0].plot([student_100[0], student_100[1]], [0.6, 0.6], color='blue', marker = '.', linewidth = 1, label = 'm interval, n = 100')
    ax[0][0].set_ylim([0,1])
    ax[0][0].set_title('Classic approach')
    ax[0][0].legend()

    ax[0][1].plot([chi_20[0], chi_20[1]], [0.3, 0.3], color='r', marker = '.', linewidth = 1, label = 'sigma interval, n = 20')
    ax[0][1].plot([chi_100[0], chi_100[1]], [0.6, 0.6], color='blue', marker = '.', linewidth = 1, label = 'sigma interval, n = 100')
    ax[0][1].set_ylim([0,1])
    ax[0][1].set_title('Classic approach')
    ax[0][1].legend()

    print(f"Классический подход:\n"
        f"n = 20 \n"
        f"\t m: " + str(student_20) + " \t sigma: " + str(chi_20) + "\n"
        f"n = 100 \n"
        f"\t m: " + str(student_100) + " \t sigma: " + str(chi_100) + "\n")

    ax[1][0].plot([as_mo_20[0], as_mo_20[1]], [0.3, 0.3], color='r', marker = '.', linewidth = 1, label = 'm interval, n = 20')
    ax[1][0].plot([as_mo_100[0], as_mo_100[1]], [0.6, 0.6], color='blue', marker = '.', linewidth = 1, label = 'm interval, n = 100')
    ax[1][0].set_ylim([0,1])
    ax[1][0].set_title('Asymptotic approach')
    ax[1][0].legend()

    ax[1][1].plot([as_d_20[0], as_d_20[1]], [0.3, 0.3], color='r', marker = '.', linewidth = 1, label = 'sigma interval, n = 20')
    ax[1][1].plot([as_d_100[0], as_d_100[1]], [0.6, 0.6], color='blue', marker = '.', linewidth = 1, label = 'sigma interval, n = 100')
    ax[1][1].set_ylim([0,1])
    ax[1][1].set_title('Asymptotic approach')
    ax[1][1].legend()

    plt.savefig('graphics/intervals.png')

    print(f"Асимптотический подход:\n"
        f"n = 20 \n"
        f"\t m: " + str(as_mo_20) + " \t sigma: " + str(as_d_20) + "\n"
        f"n = 100 \n"
        f"\t m: " + str(as_mo_100) + " \t sigma: " + str(as_d_100) + "\n")

if __name__ == "__main__":
    task4()