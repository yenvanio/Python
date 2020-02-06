import numpy as np

from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

import matplotlib.pyplot as plt


mat = np.array([[0.0, 1.0, 4.0, 5.0], [0.0, 0.0, 2.0, 6.0], [0.0, 0.0, 0.0, 3.0], [0.0, 0.0, 0.0, 0.0]])
dists = squareform(mat)
linkage_matrix = linkage(dists, "single")
dendrogram(linkage_matrix, labels=["A", "B", "C", "D"])
plt.title("Dendogram")
plt.show()
