import math
from operator import attrgetter

import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from clusterization_components_excerpts.cluster_gears.cluster import Cluster, Dendrograme
from clusterization_components_excerpts.cluster_gears.difference import Difference

class Clustering:

    """
        Процесс кластеризации
    """

    def __init__(self, elements):
        self.clusters = self._get_start_clusters(elements)
        self.differences = self._get_cluster_list_differences(self.clusters)
        self.dendrograms = list()

    def _get_start_clusters(self, data_list):
        """
            Заворачиваем начальне элементы в кластеры.
            На данном этапе каждый элемент сам по себе явялется кластером с номером уровня равным единице.
        """
        clusters = []
        # т.к. эти элементы еще не разу не объединялись - онинаходятся на первом уровне дендрограммы
        dendrograms_level = 1
        for num, element in enumerate(data_list):
            cluster = Cluster(element, num, dendrograms_level)
            clusters.append(cluster)
        return clusters

    def _get_cluster_differences(self, new_cluster, cluster_list):
        differences = []
        cluster1 = new_cluster
        for cluster2 in cluster_list:
            if cluster1 != cluster2:
                proximity = cluster1.compare(cluster2)
                dif = math.fabs(1 - proximity)
                difference = Difference(cluster1=cluster1, cluster2=cluster2, difference=dif)
                differences.append(difference)
        return differences

    def _get_cluster_list_differences(self, cluster_list):
        differences = []
        for cluster1 in cluster_list:
            cluster_differences = self._get_cluster_differences(cluster1, cluster_list)
            differences.extend(cluster_differences)
        return differences

    def do_clasterization(self, max_difference = Difference.max_difference):

        stage_number = len(self.clusters)
        num = 0
        while self.differences.__len__() > 0:

            num += 1

            self.differences = sorted(self.differences, key=attrgetter('difference'))
            min_diff = self.differences[0]
            if min_diff.difference > max_difference:
                break

            cluster1 = min_diff.cluster1
            cluster2 = min_diff.cluster2

            # добавляем в общую структуру совокупный элемент
            new_cluster = Cluster.combine(cluster1, cluster2, new_num=stage_number)
            self.clusters.append(new_cluster)
            # удаляем из общей структруы минимально отличающииеся элементы
            self.clusters.remove(cluster1)
            self.clusters.remove(cluster2)

            new_differences = Difference.get_cluster_differences(new_cluster, self.clusters)
            self.differences.extend(new_differences)
            # удаляем разницы содержащие удаленные кластеры
            self.differences = Difference.remove_differences_contain_cluster(self.differences, cluster1)
            self.differences = Difference.remove_differences_contain_cluster(self.differences, cluster2)
            self.dendrograms.append(Dendrograme(num1=cluster1.num, num2=cluster2.num, difference=min_diff.difference,
                                                lvl=new_cluster.stage_number))

            stage_number += 1

    def draw_dendragrame(self):
        # отрисовывается дендрограмма
        z = list([[dendrograme.num1, dendrograme.num2, dendrograme.difference, dendrograme.lvl] for dendrograme in
             self.dendrograms])
        Z = np.array(z)
        fig = plt.figure(figsize=(10, 6))
        dn = dendrogram(Z)
        # Z = linkage(X, 'single')
        # fig = plt.figure(figsize=(2.5, 1.0))
        # dn = dendrogram(Z)
        plt.show()


