import numpy as np
from scipy import stats
from math import gamma

distributions_names = ["normal", "cauchy", "uniform", "poisson", "laplace"]


class Distribution:

    def __init__(self, size):
        self.size = size
        self.name_to_distr = {
            'normal': np.random.normal(0, 1, size=size),
            'laplace': np.random.laplace(loc=0, scale=np.sqrt(2) / 2, size=size),
            'uniform': np.random.uniform(low=-np.sqrt(3), high=np.sqrt(3), size=size)
        }

    def generate_distribution(self, name):
        return self.name_to_distr[name]


    def get_cdf(self, name, grid):
        if name == 'normal':
            return stats.norm.cdf(grid, )
        elif name == 'laplace':
            return stats.laplace.cdf(grid)
        else:
            return stats.uniform.cdf(grid, loc=-np.sqrt(3), scale=2 * np.sqrt(3))