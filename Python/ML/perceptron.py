import sys

import numpy as np

input = sys.argv[1]
output = sys.argv[2]

debug = False

data = np.genfromtxt(input, delimiter=',')
op_file = open(output, 'w')

if debug:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    plt.ion()
    plt.scatter(data[:, 0], data[:, 1], c=data[:, 2])
    ax.set_xlim([data[:, 0].min(), data[:, 0].max()])
    ax.set_ylim([data[:, 1].min(), data[:, 0].max()])
    line, = plt.plot([], [], '-')
    # plt.show()
    xs = np.linspace(0, 16)

w1 = w2 = b = 0
flag = True
n = len(data)

while flag:
    flag = False
    for i in range(n):
        x1, x2, y = data[i, :]
        f = 1 if w1 * x1 + w2 * x2 + b > 0 else -1
        if f != y:
            w1 += x1 * y
            w2 += x2 * y
            b += y
            flag = True
    print(w1, 22, b, sep=',', file=op_file)
    if debug:
        if w2 == 0:
            ys = np.linspace(-20, 20)
            xs = -b / w1 * np.ones((len(ys),))
        else:
            ys = - (w1 * xs + b) / w2
        # plt.clf()
        # plt.scatter(data[:, 0], data[:, 1], c=data[:, 2])
        # print(xs)
        line.set_xdata(xs)
        line.set_ydata(ys)
        # plt.draw()
        # plt.show()
        plt.pause(0.01)
        # time.sleep(0.05)

# plt.pause(3)
op_file.close()
