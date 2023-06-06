import numpy as np
import matplotlib.pyplot as plt
import load
import pypoman as pyp

def show_plots(data, eps, A1, B1, w1, A0, B0, w0):
    print([A1, B1])
    print(np.sum(w1))
    plt.fill_between(data.index, np.array(data) + np.array(w1) * eps, np.array(data) - np.array(w1) * eps, alpha=0.3)
    plt.plot(np.arange(0, 200), A1 + B1 * (np.arange(0, 200)), label='lsm', color='maroon', linewidth=0.5)
    plt.xlabel('n')
    plt.ylabel('мV')
    plt.show()
    plt.close()

    print(w0)
    print([A0, B0])
    print(np.sum(w0))
    plt.fill_between(data.index, np.array(data) + np.array(w0) * eps, np.array(data) - np.array(w0) * eps, color='r',
                     alpha=0.3)
    plt.fill_between(data.index, np.array(data) + eps, np.array(data) - eps, alpha=0.3)
    plt.plot(np.arange(0, 200), A0 + B0 * (np.arange(0, 200)), label='lsm', color='r', linewidth=0.5)
    plt.xlabel('n')
    plt.ylabel('мV')
    plt.show()
    plt.close()

    plt.figure()
    plt.plot(data.index, w0, linewidth=0.5, label='w0')
    plt.plot(data.index, w1, linewidth=0.5, label='w1')
    plt.legend()
    plt.xlabel('n')
    plt.ylabel('mV')
    plt.show()
    plt.close()

    plt.figure()
    plt.fill_between(data.index, np.array(data) + eps - (A1 + B1 * (np.arange(0, 200))),
                     np.array(data) - eps - (A1 + B1 * (np.arange(0, 200))), alpha=0.3)
    plt.plot([0, 199], [0, 0], label='lsm', color='r', linewidth=0.5)
    plt.xlabel('n')
    plt.ylabel('мV')
    plt.show()
    plt.close()

    plt.figure()
    plt.fill_between(data.index, np.array(data) + eps - (A0 + B0 * (np.arange(0, 200))),
                     np.array(data) - eps - (A0 + B0 * (np.arange(0, 200))), alpha=0.3)
    plt.plot([0, 199], [0, 0], label='lsm', color='r', linewidth=0.5)
    plt.xlabel('n')
    plt.ylabel('мV')
    plt.show()
    plt.close()

    A, b = [], []
    for i in range(0, len(data)):
        A.append([1, i])
        A.append([-1, -i])
        b.append(data[i] + eps)
        b.append(-data[i] + eps)
    A = np.array(A)
    b = np.array(b)
    vertices = np.array(pyp.compute_polytope_vertices(A, b))

    beta_0_min = min(vertices[:, 0])
    beta_0_max = max(vertices[:, 0])
    beta_1_min = min(vertices[:, 1])
    beta_1_max = max(vertices[:, 1])

    print(f'beta_0 in [{beta_0_min},{beta_0_max}]')
    print(f'beta_1 in [{beta_1_min},{beta_1_max}]')

    order = np.argsort(np.arctan2(vertices[:, 1] - vertices[:, 1].mean(), vertices[:, 0] - vertices[:, 0].mean()))

    plt.figure()
    plt.fill(vertices[:, 0][order], vertices[:, 1][order], edgecolor='red', color='r', alpha=0.3, linewidth=0.5)
    plt.scatter(vertices[:, 0], vertices[:, 1], color='r', s=0.5)
    plt.plot([beta_0_min, beta_0_min], [beta_1_min, beta_1_max], linewidth=0.5, color='blue')
    plt.plot([beta_0_max, beta_0_max], [beta_1_min, beta_1_max], linewidth=0.5, color='blue')
    plt.plot([beta_0_min, beta_0_max], [beta_1_min, beta_1_min], linewidth=0.5, color='blue')
    plt.plot([beta_0_min, beta_0_max], [beta_1_max, beta_1_max], linewidth=0.5, color='blue')
    plt.xlabel('beta_0')
    plt.ylabel('beta_1')
    plt.savefig('inform_set.png')
    plt.show()

    max_val, min_val = [], []
    for i in range(0, len(data)):
        minimum = 100
        maximum = 0
        for v in vertices:
            if v[0] + v[1] * i > maximum:
                maximum = v[0] + v[1] * i
            if v[0] + v[1] * i < minimum:
                minimum = v[0] + v[1] * i
        min_val.append(minimum)
        max_val.append(maximum)

    plt.figure()
    plt.fill_between(data.index, np.array(data) + eps, np.array(data) - eps, alpha=0.3)
    plt.plot(data.index, data, linewidth=0.5)
    plt.fill_between(np.arange(0, 200), np.array(min_val), np.array(max_val), color='r', alpha=0.3)
    plt.xlabel('n')
    plt.ylabel('mV')
    plt.show()
    plt.close()

    max_val_pr, min_val_pr = [], []
    for i in range(-50, 250):
        minimum = 100
        maximum = 0
        for v in vertices:
            if v[0] + v[1] * i > maximum:
                maximum = v[0] + v[1] * i
            if v[0] + v[1] * i < minimum:
                minimum = v[0] + v[1] * i
        min_val_pr.append(minimum)
        max_val_pr.append(maximum)

    plt.figure()
    plt.fill_between(data.index, np.array(data) + eps, np.array(data) - eps, alpha=0.3)
    plt.fill_between(np.arange(-50, 250), np.array(min_val_pr), np.array(max_val_pr), color='r', alpha=0.3)
    plt.plot(data.index, data, color='blue', linewidth=0.5)
    plt.xlabel('n')
    plt.ylabel('mV')
    plt.show()
    plt.close()
