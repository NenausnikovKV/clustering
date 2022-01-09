# отчистка для накопления и вывода
import json

from clusterization_components_excerpts.clustering import Clustering
from clusterization_components_excerpts.element.cluster_element import ClusterElement
from clusterization_components_excerpts.cluster_gears.cluster import Cluster


from source.sentence_stage.sentence import Sentence


class ClusterSentence(ClusterElement):

    """
        Тестовый элемент - номер
    """

    def __init__(self, sentence):
        self.sentence = sentence

    def __add__(self, other):
        return ClusterSentence(self.sentence + other.sentence)

    def compare(self, other):
        return self.sentence.compare(other.sentence)

    def __repr__(self):
        return str(self.sentence)


if __name__=="__main__":


    sentence_excert1 = "Привет, это первое тестовое предложение"
    sentence_excert2 = "Следующее полностью отличное от предыдущего"
    sentence_excert3 = "Следующее полностью совпадающее от предыдущего"

    sentence1 = Sentence.initial_from_text_excerpt(sentence_excert1)
    sentence2 = Sentence.initial_from_text_excerpt(sentence_excert2)
    sentence3 = Sentence.initial_from_text_excerpt(sentence_excert3)

    started_data = [sentence1, sentence2, sentence3]
    cluster_elements =[]
    for num, element in enumerate(started_data):
        cluster_elements.append(ClusterSentence(element))

    clustering = Clustering(cluster_elements)
    clustering.do_clasterization()
    clustering.draw_dendragrame()





