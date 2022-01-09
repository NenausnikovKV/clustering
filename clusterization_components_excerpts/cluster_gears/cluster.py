import copy
from collections import namedtuple
from operator import attrgetter

from clusterization_components_excerpts.element.cluster_element import ClusterElement
from clusterization_components_excerpts.cluster_gears.difference import Difference

Dendrograme = namedtuple("Dendrograme", ["num1", "num2", "difference", "lvl"])


class Cluster(ClusterElement):
    """
    Кластер и методы взаимодействия
    """


    max_difference = 1
    @staticmethod
    def set_max_diff(max_diff):
        global max_difference
        max_difference = max_diff

    def __init__(self, element, num, stage_number):
        """
        Создание кластера всегда начинается с одного элемента
        """
        self.elements = [element]
        self.general_element = element
        # порядковый номер
        self.num = num
        # номер по структуре для строительства дендрограммы
        self.stage_number = stage_number

    def __add__(self, other):
        result = copy.deepcopy(self)
        result.elements.extend(other.elements)
        result.general_element = self.general_element + other.general_element
        result.stage_number = self.stage_number+other.stage_number
        return result

    def __repr__(self):
        return "num - " + str(self.num) + " element - " + str(self.general_element) + "  stage - " + str(self.stage_number)

    def cut_off(self):
        """уменьшаем количество связей для виво ключевого элемента"""
        self.general_element.cut_off()

    def set_num(self, num):
        self.num = num

    def compare(self, other):
        return self.general_element.compare(other.general_element)

    @staticmethod
    def combine(cluster1, cluster2, new_num):
        new_cluster = cluster1 + cluster2
        new_cluster.set_num(num=new_num)
        return new_cluster

    @staticmethod
    def add_cluster(general_cluster, b, differences):
        new_differences = Difference.get_cluster_differences(b, [general_cluster])
        differences.extend(new_differences)
        b.append(general_cluster)
        return b, differences

    @staticmethod
    def do_clustering(clusters, max_diff = Difference.max_difference):
        # определяем разницу между кластером и всеми другими
        differences = Difference.get_cluster_list_differences(clusters)

        clustering_length = len(clusters)
        num = 0
        while differences.__len__() > 0:

            # print(num)
            num += 1

            differences = sorted(differences, key=attrgetter('difference'))
            min_diff = differences[0]
            if min_diff.difference > max_diff:
                break

            # удаляем из общей структруы минимально отличающииеся кластеры
            clusters.remove(min_diff.cluster1)
            clusters.remove(min_diff.cluster2)

            # удаляем из связе минимально отличающииеся клстеры
            differences = Difference.remove_differences_contain_cluster(differences, min_diff.cluster1)
            differences = Difference.remove_differences_contain_cluster(differences, min_diff.cluster2)

            # добавляем в общую структуру совокупный элемент
            new_cluster = Cluster.combine(min_diff.cluster1, min_diff.cluster2, new_num=clustering_length)
            clusters.append(new_cluster)
            new_differences = Difference.get_cluster_differences(new_cluster, clusters)
            differences.extend(new_differences)
            clustering_length += 1
        return clusters

    @staticmethod
    def remove_clusters(min_difference, difference_list,):

        Difference.remove_differences_contain_cluster(difference_list, min_difference.cluster1)
        Difference.remove_differences_contain_cluster(difference_list, min_difference.cluster2)

        return difference_list
