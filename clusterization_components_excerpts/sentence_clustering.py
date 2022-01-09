# отчистка для накопления и вывода
import json
from collections import defaultdict
from operator import attrgetter

from clusterization_components_excerpts.element.VivoSentence import VivoSentence
from clusterization_components_excerpts.element.cluster_element import ClusterElement
from clusterization_components_excerpts.cluster_gears.cluster import Cluster
from graph_representation.vivo import Vivo
from source.sentence_stage.sentence import Sentence


def read_input_data():
    input_= dict()
    name = "bubbles"
    sentence_dict = {name: []}
    file_address = "in/bubble_sentences/bubbles"
    with open(file_address, "r", encoding="utf-8") as file:
        for line in file:
            sentence_dict[name].append(line.strip())
    input_["sentence_dict"] = sentence_dict
    return input_



def get_vivo_sentences(sentence_texts):
    #  подгатавливаем элементы для кластеризации - элемент (sentence)
    #  и его описание для сравнения (синтаксчическое древо vivos)
    vivo_sentences = []
    for sentence_text in sentence_texts:
        if sentence_text == "":
            continue
        sentence = Sentence.initial_from_text_excerpt(sentence_text.replace("\n", " "))
        # подмешиваем к предложениям интерфес элемента кластеризации
        vivo = Vivo(nodes={hash(word.text):word.text for word in sentence.word_list})
        vivo_sentence = VivoSentence(sentence=sentence, vivo=vivo)
        vivo_sentences.append(vivo_sentence)
    return vivo_sentences

def write_sentence_clusters(directory, file_name, clusters):
    cluster_text = ""
    for cluster in clusters:
        cluster_text = cluster_text + cluster.general_element.sentence.text
        cluster_text = cluster_text + "\n \n ------------------------------------------------------- \n \n"
    address = directory + "\\" + file_name
    with open(address, "w", encoding="utf-8") as f:
        f.write(cluster_text)

def cluster_sentences(categories_sentence_texts, max_diff=0.0, out_directory="out\\cluster\\cluster_categories\\"):
    """
    Кластеризация предложений внутри категорий
    """

    # считываем блоки предложений относящихся к соответствующим им категориям

    #  для каждой категории рассматриваем
    for category, component_text in categories_sentence_texts.items():
        # if category != "common_data":
        #     continue
        print(f"раассматриваем категорию - {category}")

        # лингвистический анализ строк текста
        # if isinstance(component_text, str):
        #     sentence_texts = [sentence for sentence in component_text.split("\n") if sentence != ""]
        # else:
        #     sentence_texts = component_text
        sentence_texts = component_text
        vivo_sentences = get_vivo_sentences(sentence_texts)
        relations = sorted(vivo_sentences[0].vivo.relations.values(), key=attrgetter("text"))
        # заврачиваем подготовленные элементы в кластеры
        clusters = [Cluster(vivo_sentences[num], num, stage_number=1) for num, item in enumerate(vivo_sentences)]

        # выполняем кластеризация
        clusters = Cluster.do_clustering(clusters, max_diff)

        # запись результатов в файл
        write_sentence_clusters(directory=out_directory, file_name=category, clusters=clusters)


def simplify_components(components):
    "компоненты могут содеражть несколько разорванных отрывков. Длоя кластеризации сводим их как независимые предложения"
    simple_components = defaultdict(list)
    for category, excerts in components.items():
        for excert in excerts:
            simple_components[category].extend(excert)
    return simple_components

if __name__ == "__main__":

    input_data = read_input_data()
    components = input_data["sentence_dict"]

    # переводим отрывки компоенета в тексте в независисые строки
    # components = simplify_components(components)

    # это оказалось не нужно
    # category_sentences = defaultdict(list)
    # for category_name, excerts in components.items():
    #     for excert in excerts:
    #         sentences = NatashaSent.divide_text_to_sentence_plain_texts(excert)
    #         assert len(sentences)==1, "hello"
    #         category_sentences[category_name].extend(sentences)

    out_directory = ("out/data_clusters/")
    cluster_sentences(components, max_diff=0.9, out_directory=out_directory)