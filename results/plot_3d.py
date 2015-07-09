
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def plot_3d(data, indices):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    plt.show()
