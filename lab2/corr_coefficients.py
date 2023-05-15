import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import os




def quadrant_coefficient(x, y):
    size = len(x)
    med_x = np.median(x)
    med_y = np.median(y)
    n = {1: 0, 2: 0, 3: 0, 4: 0}
    for i in range(size):
        if x[i] >= med_x and y[i] >= med_y:
            n[1] += 1
        elif x[i] < med_x and y[i] >= med_y:
            n[2] += 1
        elif x[i] < med_x and y[i] < med_y:
            n[3] += 1
        elif x[i] >= med_x and y[i] < med_y:
            n[4] += 1
    return (n[1] + n[3] - n[2] - n[4]) / size


def get_coefficients(size, ro, repeats):
    pearson, quadrant, spearman = [], [], []
    for i in range(repeats):
        if ro == 1:
            sample = 0.9 * np.random.multivariate_normal([0, 0], [[1, 0.9], [0.9, 1]], size) + \
                     0.1 * np.random.multivariate_normal([0, 0], [[10, 0.9], [0.9, 10]], size)
        else:
            sample = np.random.multivariate_normal([0, 0], [[1, ro], [ro, 1]], size)
        x, y = sample[:, 0], sample[:, 1]
        pearson.append(stats.pearsonr(x, y)[0])
        spearman.append(stats.spearmanr(x, y)[0])
        quadrant.append(quadrant_coefficient(x, y))
    return pearson, spearman, quadrant, x, y


def coefficients():
    sizes = [20, 60, 100]
    ros = [0, 0.5, 0.9, 1]

    if not os.path.isdir("graphics"):
        os.makedirs("graphics")

    for i in range(len(ros)):
        fig, ax = plt.subplots(1, 3)

        for j in range(len(sizes)):
            p, s, q, x, y = get_coefficients(sizes[j], ros[i], 1000)

            print("Size =", sizes[j], "ro =", ros[i])
            print ('Pearson:', p, '\n', 'Spearman:', s, '\n', 'Quadratic:', q)
            print("E(z)", np.around(np.mean(s), decimals=4), np.around(np.mean(q), decimals=4), np.around(np.mean(p), decimals=4))
            print("E(z^2)",  np.around(np.mean(np.asarray([el * el for el in p])), decimals=4), np.around(np.mean(np.asarray([el * el for el in s])), decimals=4),
            np.around(np.mean(np.asarray([el * el for el in q])), decimals=4))
            print("D(z)", np.around(np.std(p), decimals=4), np.around(np.std(s), decimals=4), np.around(np.std(q), decimals=4), "\n")

            cov = np.cov(x, y)
            pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
            rad_x = np.sqrt(1 + pearson)
            rad_y = np.sqrt(1 - pearson)
            mean_x = np.mean(x)
            mean_y = np.mean(y)
            scale_x = np.sqrt(cov[0, 0]) * 3
            scale_y = np.sqrt(cov[1, 1]) * 3
            ellipse = Ellipse((0, 0), width=rad_x * 2, height=rad_y * 2, facecolor='none', edgecolor='blue')
            transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)
            ellipse.set_transform(transf + ax[j].transData)
            ax[j].add_patch(ellipse)
            ax[j].grid()
            ax[j].scatter(x, y, s=5)
            if ros[i] == 1:
                ax[j].set_title("n = " + str(sizes[j]))
            else:
                ax[j].set_title("n = " + str(sizes[j]) + ", ro = " + str(ros[i]))
        plt.savefig("graphics/" + str(ros[i]) + "_ellipse.png")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
