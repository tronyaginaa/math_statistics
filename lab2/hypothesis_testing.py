import numpy as np
import scipy.stats as stats
from distributions import Distribution

def get_cdf(x, mu, sigma):
    return stats.norm.cdf(x, mu, sigma)

def distribution(size, dist_name):
    generator = Distribution(size)
    samples = generator.generate_distribution(dist_name)
    mu_c = np.mean(samples)
    sigma_c = np.std(samples)
    k = 7
    borders = np.linspace(mu_c - 3, mu_c + 3, num=(k - 1))

    p_arr = np.array([get_cdf(borders[0], mu_c, sigma_c)])
    for i in range(len(borders) - 1):
        val = get_cdf(borders[i + 1], mu_c, sigma_c) - get_cdf(borders[i], mu_c, sigma_c)
        p_arr = np.append(p_arr, val)
    p_arr = np.append(p_arr, 1 - get_cdf(borders[-1], mu_c, sigma_c))

    n_arr = np.array([len(samples[samples <= borders[0]])])
    for i in range(len(borders) - 1):
        n_arr = np.append(n_arr, len(samples[(samples <= borders[i + 1]) & (samples >= borders[i])]))
    n_arr = np.append(n_arr, len(samples[samples >= borders[-1]]))

    res_arr = np.divide(np.multiply((n_arr - p_arr * size), (n_arr - p_arr * size)), p_arr * size)

    intervals = [('$-\inf$', str(np.around(borders[0], decimals=2)))]
    for i in range(len(borders) - 1):
        intervals.append((str(np.around(borders[i], decimals=2)), str(np.around(borders[i + 1], decimals=2))))
    intervals.append((str(np.around(borders[-1], decimals=2)), '$+\inf$'))
    rows = [[i + 1, (intervals[i][0] + ', ' + intervals[i][1]),
             "%.2f" % n_arr[i],
             "%.4f" % p_arr[i],
             "%.2f" % (size * p_arr[i]),
             "%.2f" % (n_arr[i] - size * p_arr[i]),
             "%.2f" % ((n_arr[i] - size * p_arr[i]) ** 2 / (size * p_arr[i]))] for i in range(k)]
    rows.append(['$\sum$', '$-$', "%.2f" % np.sum(n_arr), "%.4f" % np.sum(p_arr), "%.2f" % (size * np.sum(p_arr)),
                 "%.2f" % (np.sum(n_arr) - size * np.sum(p_arr)), "%.2f" % np.sum(res_arr)])

def testing():
    distribution(100, "normal")
    distribution(20, "laplace")
    distribution(20, "uniform")
