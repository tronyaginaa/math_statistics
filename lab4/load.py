import numpy as np
import scipy.optimize as opt
import pandas as pd

def minimization(A, y, eps, lim):
    [m, n] = A.shape

    c = np.concatenate((np.zeros((n, 1)), np.ones((m, 1))), axis=0)
    c = np.ravel(c)

    diag = np.diag(np.full(m, -eps))

    M_1 = np.concatenate((-A, diag), axis=1)
    M_2 = np.concatenate((A, diag), axis=1)
    M = np.concatenate((M_1, M_2), axis=0)

    v = np.concatenate((-y, y), axis=0)

    l_b = np.concatenate((np.full(n, None), np.full(m, lim)), axis=0)
    print(l_b)
    u_b = np.full(n + m, None)

    bounds = [(l_b[i], u_b[i]) for i in range(len(l_b))]

    result = opt.linprog(c=c, A_ub=M, b_ub=v, bounds=bounds)
    y = result.x

    coefs = y[0:n]
    w = y[n:n + m]

    return [coefs, w]


def parser(lim):
    data = pd.read_csv('/Users/tronyagina/Downloads/Статистика-измерений/Канал 1_500nm_0.23mm.csv', sep=';', encoding='cp1251')

    data_mv = np.ravel(data.drop('мА', axis=1).to_numpy())

    data_n = np.arange(1, len(data_mv) + 1, 1)

    data_eps = 1e-4

    data_X = np.stack((np.ones(len(data_mv)), data_n))
    data_X = np.transpose(data_X)
    [data_tau, data_w] = minimization(data_X, data_mv, data_eps, lim)

    with open(f'Chi{lim}.txt', 'w') as f:
        print(f'{data_tau[0]} {data_tau[1]}', file=f)
        for temp in data_w:
            print(temp, file=f)


def load_processed(filename):
    A = 0
    B = 0
    w = []
    with open(filename) as f:
        A, B = [float(t) for t in f.readline().split()]
        for line in f.readlines():
            w.append(float(line))
    return A, B, w