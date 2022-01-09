import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram


def draw_dendragrame(dendrogrames):
    # отрисовывается дендрограмма
    z = list(
        [[dendrograme.num1, dendrograme.num2, dendrograme.difference, dendrograme.lvl] for dendrograme in dendrogrames])
    Z = np.array(z)
    fig = plt.figure(figsize=(10, 6))
    dn = dendrogram(Z)
    # Z = linkage(X, 'single')
    # fig = plt.figure(figsize=(2.5, 1.0))
    # dn = dendrogram(Z)
    plt.show()
