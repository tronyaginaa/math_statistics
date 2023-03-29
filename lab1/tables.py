import numpy as np
from distributions import Distribution, distributions_names
import os


def calc_quart(arr, p):
    new_arr = np.sort(arr)
    k = len(arr) * p
    if k.is_integer():
        return new_arr[int(k)]
    else:
        return new_arr[int(k) + 1]


def calc_z_q(arr):
    return (calc_quart(arr, 0.25) + calc_quart(arr, 0.75)) / 2


def calc_z_tr(arr):
    r = int(len(arr) * 0.25)
    new_arr = np.sort(arr)
    sum = 0
    for i in range(r + 1, len(arr) - r):
        sum += new_arr[i]
    return sum / (len(arr) - 2 * r)


def print_outlier():
    repeats = 1000
    sizes = [20, 100]
    rows = []
    if not os.path.isdir("tables"):
        os.makedirs("tables")
    for name in distributions_names:
        count = 0
        for j in range(len(sizes)):
            for i in range(repeats):
                generator = Distribution(sizes[j])
                arr = generator.generate_distribution(name)
                x1 = np.quantile(arr, 0.25) - 1.5 * (np.quantile(arr, 0.75) - np.quantile(arr, 0.25))
                x2 = np.quantile(arr, 0.75) + 1.5 * (np.quantile(arr, 0.75) - np.quantile(arr, 0.25))
                for k in range(0, sizes[j]):
                    if arr[k] > x2 or arr[k] < x1:
                        count += 1
            count /= repeats
            rows.append(name + " n = " + str(sizes[j]) + " " + str(np.around(count / sizes[j], decimals=3)))
    print("Sample   Share of emissions")
    for row in rows:
        print(row)

def print_characteristics():
    repeats = 1000
    sizes = [10, 100, 1000]
    for name in distributions_names:
        print(name)
        print("bar{x}   med(x)   z_R   z_Q   z_{tr}")
        for N in sizes:
            mean = []
            med = []
            z_r = []
            z_q = []
            z_tr = []
            for rep in range(0, repeats):
                generator = Distribution(N)
                arr = generator.generate_distribution(name)
                arr_sorted = np.sort(arr)
                mean.append(np.mean(arr))
                med.append(np.median(arr))
                z_r.append((arr_sorted[0] + arr_sorted[-1]) / 2)
                z_q.append(calc_z_q(arr))
                z_tr.append(calc_z_tr(arr))
            print("n = " + str(N))
            print("E(z)",
                        np.around(np.mean(mean), decimals=4),
                        np.around(np.mean(med), decimals=4),
                        np.around(np.mean(z_r), decimals=4),
                        np.around(np.mean(z_q), decimals=4),
                        np.around(np.mean(z_tr), decimals=4),
                        )
            print("D(z)",
                        np.around(np.mean(np.multiply(mean, mean)) - np.mean(mean) * np.mean(mean), decimals=4),
                        np.around(np.mean(np.multiply(med, med)) - np.mean(med) * np.mean(med), decimals=4),
                        np.around(np.mean(np.multiply(z_r, z_r)) - np.mean(z_r) * np.mean(z_r), decimals=4),
                        np.around(np.mean(np.multiply(z_q, z_q)) - np.mean(z_q) * np.mean(z_q), decimals=4),
                        np.around(np.mean(np.multiply(z_tr, z_tr)) - np.mean(z_tr) * np.mean(z_tr), decimals=4),
                        )
            print("E(z) + sqrt{D(z)}",
                         np.around(np.mean(mean) + np.sqrt(
                             np.mean(np.multiply(mean, mean)) - np.mean(mean) * np.mean(mean)), decimals=4),
                         np.around(np.mean(med) + np.sqrt(
                             np.mean(np.multiply(med, med)) - np.mean(med) * np.mean(med)), decimals=4),
                         np.around(np.mean(z_r) + np.sqrt(
                             np.mean(np.multiply(z_r, z_r)) - np.mean(z_r) * np.mean(z_r)), decimals=4),
                         np.around(np.mean(z_q) + np.sqrt(
                             np.mean(np.multiply(z_q, z_q)) - np.mean(z_q) * np.mean(z_q)), decimals=4),
                         np.around(np.mean(z_tr) + np.sqrt(
                             np.mean(np.multiply(z_tr, z_tr)) - np.mean(z_tr) * np.mean(z_tr)), decimals=4),
                         )
            print("E(z) - sqrt{D(z)}",
                         np.around(np.mean(mean) - np.sqrt(
                             np.mean(np.multiply(mean, mean)) - np.mean(mean) * np.mean(mean)), decimals=4),
                         np.around(np.mean(med) - np.sqrt(
                             np.mean(np.multiply(med, med)) - np.mean(med) * np.mean(med)), decimals=4),
                         np.around(np.mean(z_r) - np.sqrt(
                             np.mean(np.multiply(z_r, z_r)) - np.mean(z_r) * np.mean(z_r)), decimals=4),
                         np.around(np.mean(z_q) - np.sqrt(
                             np.mean(np.multiply(z_q, z_q)) - np.mean(z_q) * np.mean(z_q)), decimals=4),
                         np.around(np.mean(z_tr) - np.sqrt(
                             np.mean(np.multiply(z_tr, z_tr)) - np.mean(z_tr) * np.mean(z_tr)), decimals=4),
                         )
            print()
