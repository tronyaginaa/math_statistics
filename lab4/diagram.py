import matplotlib.pyplot as plt

def diagram(data, epsilon, beta):
    plt.figure()
    plt.fill_between(data.index, data - epsilon, data + epsilon, alpha = 0.3)
    plt.plot(data.index, data, linewidth=0.5)
    if beta is not None:
        plt.plot([0, 199],[beta, beta], color = "r", linestyle = "--", linewidth = 0.5)
    plt.xlabel('n')
    plt.ylabel('mV')
    plt.show()

