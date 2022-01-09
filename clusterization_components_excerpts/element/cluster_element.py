from abc import abstractmethod


class ClusterElement:
    """
    Интерфейс для элемента кластера
    """

    @abstractmethod
    def __add__(self, other):
        pass


    @abstractmethod
    def compare(self, other):
        pass

