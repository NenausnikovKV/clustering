import math


class Difference:

    max_difference = 1
    @staticmethod
    def set_max_diff(max_diff):
        global max_difference
        max_difference = max_diff

    def __init__(self, cluster1, cluster2, difference):
        self.cluster1 = cluster1
        self.cluster2 = cluster2
        self.difference = difference

    def __repr__(self):
        return "{0} - {1}: {2}".format(self.cluster1, self.cluster2, self.difference)


    @classmethod
    def get_cluster_differences(cls, new_cluster, cluster_list):
        differences = []
        cluster1 = new_cluster
        for cluster2 in cluster_list:
            if cluster1 != cluster2:
                proximity = cluster1.compare(cluster2)
                dif = math.fabs(1 - proximity)
                difference = cls(cluster1=cluster1, cluster2=cluster2, difference=dif)
                differences.append(difference)
        return differences


    @classmethod
    def get_cluster_list_differences(cls, cluster_list):
        differences = []
        for cluster1 in cluster_list:
            cluster_differences = cls.get_cluster_differences(cluster1, cluster_list)
            differences.extend(cluster_differences)
        return differences


    @classmethod
    def get_differences_from_cluster_lists(cls, cluster_list1, cluster_list2):
        differences = []
        for cluster1 in cluster_list1:
            for cluster2 in cluster_list2:
                if cluster1 != cluster2:
                    proximity = cluster1.element.get_difference(cluster2.element)
                    dif = math.fabs(1-proximity)
                    difference = cls(cluster1=cluster1, cluster2=cluster2, difference=dif)
                    differences.append(difference)
        return differences







    @staticmethod
    def remove_differences_contain_cluster(differences, cluster):
        index = 0
        while index < differences.__len__():
            difference = differences[index]
            cluster1 = difference.cluster1
            cluster2 = difference.cluster2
            if any([cluster == cluster1, cluster == cluster2]):
                differences.pop(index)
                index -= 1
            index += 1
        return differences


