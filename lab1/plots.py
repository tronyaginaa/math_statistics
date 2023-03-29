from distributions import Distribution, distributions_names
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
import numpy as np
import seaborn as sns
import os


def plot_density():
    sizes = [10, 50, 1000]
    if not os.path.isdir("graphics"):
        os.makedirs("graphics")
    for name in distributions_names:
        fig, ax = plt.subplots(1, 3, figsize=(12, 4))
        fig.suptitle(name)
        for i in range(len(sizes)):
            generator = Distribution(sizes[i])
            n, bins, patches = ax[i].hist(generator.generate_distribution(name), density=True, histtype="stepfilled")
            ax[i].plot(bins, generator.get_density(name, bins), color='r', linewidth=1)
            ax[i].set_title("n = " + str(sizes[i]))
        plt.savefig("graphics/" + name + "_denst.png")


def plot_box_plot():
    if not os.path.isdir("graphics"):
        os.makedirs("graphics")
    for name in distributions_names:
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.suptitle(name)
        array20 = Distribution(20)
        array100 = Distribution(100)
        ax.boxplot((array20.generate_distribution(name), array100.generate_distribution(name)), labels=["n = 20", "n = 100"], vert=False)
        plt.savefig("graphics/" + name + "_box_plot.png")


def plot_ecdf():
    sizes = [20, 60, 100]
    if not os.path.isdir("graphics"):
        os.makedirs("graphics")
    for name in distributions_names:
        fig, ax = plt.subplots(1, 3, figsize=(12, 4))
        fig.suptitle(name)
        for i in range(len(sizes)):
            if name == 'poisson':
                x = np.linspace(6, 14, 100)
            else:
                x = np.linspace(-4, 4, 100)
            generator = Distribution(sizes[i])
            ecdf = ECDF(generator.generate_distribution(name))(x)
            ax[i].step(x, ecdf)
            ax[i].plot(x, generator.get_cdf(name, x))
            ax[i].set_title("n = " + str(sizes[i]))
        plt.savefig("graphics/" + name + "_ecdf.png")


def plot_kde():
    sizes = [20, 60, 100]
    bw = [0.5, 1, 2]
    if not os.path.isdir("graphics"):
        os.makedirs("graphics")
    for name in distributions_names:
        for i in range(len(sizes)):
            fig, ax = plt.subplots(1, 3, figsize=(12, 4))
            fig.suptitle(name + str(sizes[i]))
            generator = Distribution(sizes[i])
            for j in range(len(bw)):
                if name == 'poisson':
                    x = np.linspace(6, 14, 100)
                    ax[j].set_xlim([6, 14])
                else:
                    x = np.linspace(-4, 4, 100)
                    ax[j].set_xlim([-4, 4])
                ax[j].set_ylim([0, 1])
                sns.kdeplot(generator.generate_distribution(name), ax=ax[j], bw_adjust=bw[j])
                ax[j].plot(x, generator.get_density(name, x))
            plt.savefig("graphics/" + name + str(sizes[i]) + "_kde.png")
