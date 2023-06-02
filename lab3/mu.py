import matplotlib.pyplot as plt

def mu(data, interval, eps):
    count = 0
    for i in range(len(data)):
        if ((data[i].values[:, 0] + eps) > interval[1]).any() and ((data[i].values[:, 0] - eps) < interval[0]).any():
            count += 1
    return count


def plot(data, eps):
    df = data[0]
    lb = [df.loc[i][0] - eps for i in range(len(df))]
    rb = [df.loc[i][0] + eps for i in range(len(df))]
    borders = sorted(lb + rb)
    freq = [0 for _ in range(2 * len(df) - 1)]
    for i in range(2 * len(df) - 1):
        for j in range(len(df)):
            if (df.loc[j][0] - eps <= borders[i]) and (df.loc[j][0] + eps >= borders[i + 1]):
                freq[i] += 1

    moda_val = max(freq)
    moda_indexes = [i for i in range(len(freq)) if freq[i] == moda_val]
    moda = [borders[moda_indexes[0]], borders[moda_indexes[-1]]]

    print('max mu i', moda_val)
    print('moda indexes', moda_indexes)
    print('moda', moda)

    plt.axhline(y=moda_val, color='r', linestyle='--', label='moda')
    plt.plot(borders[:-1], freq)
    plt.legend()
    plt.xlabel('mV')
    plt.ylabel('mu')
    plt.show()
