import numpy as np
import matplotlib.pyplot as plt

def plot(data, part):
    x = range(1, data[:, 0].size + 1)
    x2 = np.array(range(1, data[:, 0].size + 1))
    mask = (data[:, 0] < 0.9196246) & (data[:, 1] > 0.919663)
    y_min = np.maximum(data[:, 1], 0.9196246)
    y_max = np.minimum(data[:, 0], 0.919663)

    if part == 2 and np.any(mask):
        plt.vlines(x, data[:, 0], data[:, 1])
        plt.vlines(x2[mask], y_min[mask], y_max[mask],
                   colors="g")
    elif part == 3:
        plt.vlines(x, data[:, 0], data[:, 1])
        plt.hlines(0.919603, 0, 200, colors="g", lw=2)
    else:
        plt.vlines(x, data[:, 0], data[:, 1])


def interval(data, eps, part, label=""):
    for i in range(len(data)):
        data[i].values[:, 1] = data[i].values[:, 0] + eps
        data[i].values[:, 0] -= eps
        plot(data[i].values, part)

    plt.xlabel('n')
    plt.ylabel('mV')
    plt.title(label)
    plt.show()