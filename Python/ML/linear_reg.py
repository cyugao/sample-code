import sys
import numpy as np
from numpy.linalg import norm
from mpl_toolkits.mplot3d import Axes3D

input = sys.argv[1]
output = sys.argv[2]

alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.2]

debug = True

rawdata = np.genfromtxt(input, delimiter=',')
x, y, z = rawdata[:, 0], rawdata[:, 1], rawdata[:, 2]
op_file = open(output, 'w')

if debug:
    import matplotlib.pyplot as plt

    fig = plt.figure()
    import matplotlib

    # matplotlib.get_backend()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(x.min() - 1, x.max() + 1)
    ax.set_ylim(y.min() - 1, y.max() + 1)
    ax.set_zlim(z.min() - 1, z.max() + 1)
    ax.scatter(x, y, z)
    # plt.show()
    xs = np.linspace(x.min(), x.max())
    ys = np.linspace(y.min(), y.max())

n, p = rawdata.shape

X = rawdata[:, :-1]
X = (X - X.mean(axis=0)) / X.std(axis=0)
X = np.concatenate((np.ones((n, 1)), X), axis=1)
Y = rawdata[:, [-1]]

# plt.pause(3)
iter_times = 100
beta = np.zeros((p, 1))

for alpha in alphas:
    rss_list = []
    for i in range(iter_times):
        Z = np.dot(X, beta)
        diff = Z - Y
        beta -= alpha * np.dot(X.T, diff) / n
        # rss = np.sum(diff ** 2) if np.max(diff) < 1e100 else 1e100
        # rss_list.append(rss)
    if debug:
        plt.clf()
        plt.plot(rss_list, '-')
        plt.pause(0.1)
    print(alpha, iter_times, beta[0, 0], beta[1, 0], beta[2, 0], sep=',', file=op_file)
plt.pause(3)
op_file.close()
