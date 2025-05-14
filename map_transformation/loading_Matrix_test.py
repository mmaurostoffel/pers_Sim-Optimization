import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def plot_matrix(matrix):
    #wall, path, waypoint, marker
    colors = ["black", "white", "red"]
    cmap = ListedColormap(colors)
    plt.imshow(matrix, cmap=cmap, interpolation='nearest')
    plt.axis('off')
    plt.savefig("doc/matrix.png")
    plt.show()



matrix = np.load('doc/matrixOutput.npy', mmap_mode=None, allow_pickle=True)
print(matrix)

plot_matrix(matrix)