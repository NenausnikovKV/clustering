import math

from clusterization_components_excerpts.clustering import Clustering
from clusterization_components_excerpts.element.cluster_element import ClusterElement


class ClusterNumber(ClusterElement):

    """
        Тестовый элемент - номер
    """

    def __init__(self, num=0):
        self.num = num

    def __add__(self, other):
        return ClusterNumber(self.num + other.num)

    def compare(self, other):
        return math.fabs(self.num - other.num)

    def __repr__(self):
        return str(self.num)


if __name__=="__main__":

    started_data = [1, 2, 3, 4, 110, 65, 70, 71]
    started_data = (element/100 for element in started_data)
    cluster_elements =[]
    for num, element in enumerate(started_data):
        cluster_elements.append(ClusterNumber(element))

    clustering = Clustering(cluster_elements)
    clustering.do_clasterization()
    clustering.draw_dendragrame()
