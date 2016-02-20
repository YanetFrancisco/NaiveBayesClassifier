__author__ = 'Yanet'

import os
from nltk.tokenize import TreebankWordTokenizer, RegexpTokenizer


# elimina las stopwords de un texto
def eiminar_stopwords(words):
    a = open('english.txt')
    result = []
    english_stops = []
    for f in a:
        result.append(f)
    tokenizer = TreebankWordTokenizer()
    for s in result:
        tokenizer = RegexpTokenizer("[\w']+")
        temp = tokenizer.tokenize(s)
        english_stops += temp
    resultado = []
    from nltk.stem import PorterStemmer
    stemmer = PorterStemmer()
    for w in words:
        if not w in english_stops:
            resultado.append(stemmer.stem(w))
    return resultado


def crear_dicc_doc_term(path):
    result = []
    result_aux = []
    file = open(path)
    for f in file:
        result.append(f)
    tokenizer = TreebankWordTokenizer()
    for s in result:
        tokenizer = RegexpTokenizer("[\w']+")
        temp = tokenizer.tokenize(s)
        words = temp
        result_aux += eiminar_stopwords(words)
    return result_aux


def cleaner_text(path, clase, to_path):
    for f in os.listdir(path):
        new_path = os.path.join(path, f)
        words = crear_dicc_doc_term(new_path)
        o = open(to_path + clase + '\\' + f, 'w')
        for w in words:
            o.write(w + '\n')
        o.close()


# cleaner_text('D:\\Corpus\\aprendizaje\\neg', 'neg', 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje\\')
# cleaner_text('D:\\Corpus\\aprendizaje\\pos', 'pos', 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje\\')

# cleaner_text('D:\\Corpus\\prediccion\\neg', 'neg', 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\prediccion\\')
# cleaner_text('D:\\Corpus\\prediccion\\pos', 'pos', 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\prediccion\\')
