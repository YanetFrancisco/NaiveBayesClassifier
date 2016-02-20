__author__ = 'Yanet'
import math
import os
from nltk.tokenize import TreebankWordTokenizer, RegexpTokenizer


def extraer_vocabulario(path_aprendizaje):
    vocabulario = set()
    for d in os.listdir(path_aprendizaje):
        new_path = os.path.join(path_aprendizaje, d)
        for doc in os.listdir(new_path):
            f = open(os.path.join(new_path, doc))
            words = [w.strip() for w in f.read().split('\n')]
            words.remove('')
            for w in words:
                 vocabulario.add(w)
            f.close()
    print(len(vocabulario))
    return vocabulario


def dicc_doc_clases(path, c):
    dict_docs = {}
    new_path = os.path.join(path, c)
    for f in os.listdir(new_path):
        dict_docs[f] = []
    return dict_docs


def dicc_vectores_por_doc(path_aprendizaje, vocabulario):
    dicc_neg = dicc_doc_clases(path_aprendizaje, 'neg')
    dicc_pos = dicc_doc_clases(path_aprendizaje, 'pos')
    print('calculo los diccionarios')
    neg = 0
    pos = 0
    for d in dicc_neg.keys():
        neg += 1
        print(neg)
        new_path = os.path.join(path_aprendizaje, 'neg', d)
        f = open(new_path)
        words = [w.strip() for w in f.read().split('\n')]
        words.remove('')
        for v in vocabulario:
            count = 0
            for w in words:
                if w == v:
                    count += 1
            dicc_neg[d].append(count)
        f.close()

    for d in dicc_pos.keys():
        pos += 1
        print(pos)
        new_path = os.path.join(path_aprendizaje, 'pos', d)
        f = open(new_path)
        words = [w.strip() for w in f.read().split('\n')]
        words.remove('')
        for v in vocabulario:
            count = 0
            for w in words:
                if w == v:
                    count += 1
            dicc_pos[d].append(count)
        f.close()
    return dicc_neg, dicc_pos


def distancia_euclidiana(dicc_term, vector_doc):
    dicc_resultante = []
    for d in dicc_term.keys():
        distancia = 0
        for c in range(len(dicc_term[d])):
            distancia += math.pow((dicc_term[d][c] - vector_doc[c]), 2)
        dicc_resultante.append(math.sqrt(distancia))
    dicc_resultante.sort()
    result = dicc_resultante[0:5]
    return result


def vector_a_clasificar(path, vocabulario):
    vector = []
    f = open(path)
    words = [w.strip() for w in f.read().split('\n')]
    words.remove('')
    for v in vocabulario:
        count = 0
        for w in words:
            if w == v:
                count += 1
        vector.append(count)
    f.close()
    return vector


def clase_mas_cercana(distancia_neg, distancia_pos):
    aux = []
    for i in range(5):
        if(min(distancia_neg) < min(distancia_pos)):
            aux.append('neg')
            distancia_neg.remove(min(distancia_neg))
        else:
            aux.append('pos')
            distancia_pos.remove(min(distancia_pos))
    neg = 0
    pos = 0
    for c in aux:
        if c == 'neg':
            neg += 1
        else:
            pos += 1
    if pos > neg:
        return 'pos'
    else:
        return 'neg'


def dar_respuesta(document, path_to_respuesta, clase, path):
    lista = None
    with open(os.path.join(path,document)) as f_original:
        lista= f_original.readlines()
        lista.append('\n'+clase)

    with open(os.path.join(path_to_respuesta, document), 'w') as dest:
         dest.writelines(lista)


def clasificar(path_aprendizaje, path_prediccion, path_to_respuesta, path):
    vocabulario = extraer_vocabulario(path_aprendizaje)
    dicc_neg, dicc_pos = dicc_vectores_por_doc(path_aprendizaje, vocabulario)
    for d in os.listdir(path_prediccion):
        pos = 0
        neg = 0
        new_path = os.path.join(path_prediccion, d)
        for doc in os.listdir(new_path):
            document = os.path.join(new_path, doc)
            vector = vector_a_clasificar(document, vocabulario)
            dicc_distancia_neg = distancia_euclidiana(dicc_neg, vector)
            dicc_distancia_pos = distancia_euclidiana(dicc_pos, vector)
            clase = clase_mas_cercana(dicc_distancia_neg, dicc_distancia_pos)
            if clase == 'pos':
                pos += 1
            else:
                neg += 1
            dar_respuesta(doc, path_to_respuesta, clase, path)
        print('El total de documentos es: ' + str(len(os.listdir(new_path))) + ' de la carpeta: ' + d)
        print('El total de documentos positivos fue: ' + str(pos))
        print('El total de documentos negativos fue: ' + str(neg))




# vocabulario = extraer_vocabulario('C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje')
# dicc_vectores_por_doc('C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje', vocabulario)
# clasificar('C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje', 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\prediccion')