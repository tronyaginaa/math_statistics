import matplotlib.pyplot as plt

def plot(data):
    for d in data:
        x = range(1, d.values[:, 0].size + 1)
        y = d.values[:, 0]

        for i in range(len(x) - 1):
            plt.plot([x[i], x[i + 1]], [y[i], y[i]], color='blue')

    plt.xlabel('n')
    plt.ylabel('mV')
    plt.show()