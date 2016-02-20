__author__ = 'Yanet'
import math
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
    file.close()
    return result_aux


#dado un path de un directorio me da una lista con todos los path de los archivos dentro del directorio
def list_paths(path):
    list_new_doc = []
    for f in os.listdir(path):
        new_path = os.path.join(path, f)
        list_new_doc.append(new_path)
    return list_new_doc


#devuelve un diccionario que tiene la probabilidad por cada clase
def probabilidad_clases(path):
    dict_clases_doc = {}
    dict_docs = {}
    total = 0
    for f in os.listdir(path):
        new_path = os.path.join(path, f)
        if os.path.isdir(new_path):
            dict_docs[f] = os.listdir(new_path)
            count_docs = len(os.listdir(new_path))
            dict_clases_doc[f] = count_docs
            total += count_docs
    for c in dict_clases_doc.keys():
        dict_clases_doc[c] = math.log10(float(dict_clases_doc[c]) / float(total))
    return dict_clases_doc, dict_docs


def words_set(path, dict_docs):
    dicc = {}
    count = 0
    for d in dict_docs['neg']:
        new_path = os.path.join(path, 'neg', d)
        f = open(new_path)
        words = [w.strip() for w in f.read().split('\n')]
        words.remove('')
        count += 1
        print(count)
        for w in words:
            if not w in dicc.keys():
                dicc[w] = {'neg': 1, 'pos': 0}
            else:
                dicc[w]['neg'] += 1
        f.close()

    for d in dict_docs['pos']:
        new_path = os.path.join(path, 'pos', d)
        f = open(new_path)
        words = [w.strip() for w in f.read().split('\n')]
        words.remove('')
        count += 1
        print(count)
        for w in words:
            if not w in dicc.keys():
                dicc[w] = {'neg': 0, 'pos': 1}
            else:
                dicc[w]['pos'] += 1
        f.close()
    return dicc


def count_words_total(dicc):
    return len(dicc.keys())


def cant_term_por_clases(dicc):
    diccionario = {'pos': 0, 'neg': 0}
    for k in dicc.keys():
        for c in dicc[k].keys():
            diccionario[c] += dicc[k][c]
    return diccionario


def cant_term_clase(dicc, term, clase):
    if not term in dicc.keys():
        return 0
    return dicc[term][clase]


def dar_respuesta(document, path_to_respuesta, clase, path):
    lista = None
    with open(os.path.join(path,document)) as f_original:
        lista= f_original.readlines()
        lista.append('\n'+clase)

    with open(os.path.join(path_to_respuesta, document), 'w') as dest:
         dest.writelines(lista)


def clasificar(path_aprendizaje, path_prediccion, path_to_respuesta, path):
    prob_clase = probabilidad_clases(path_aprendizaje)
    word_set = words_set(path_aprendizaje, prob_clase[1])
    total_set = count_words_total(word_set)
    cantidad_terminos_por_clase = cant_term_por_clases(word_set)
    for d in os.listdir(path_prediccion):
        pos = 0
        neg = 0
        max = float('-Infinity')
        clase = ''
        new_path_directory = os.path.join(path_prediccion, d)
        total_doc = len(os.listdir(new_path_directory))
        for doc in os.listdir(new_path_directory):
            new_path = os.path.join(path_prediccion, d, doc)
            f = open(new_path)
            words = [w.strip() for w in f.read().split('\n')]
            words.remove('')
            log_clases_pos = 0
            log_clases_neg = 0
            for w in words:
                p_pos = cant_term_clase(word_set, w, 'pos')
                p_neg = cant_term_clase(word_set, w, 'neg')
                if p_pos == 0:
                    log_pos = math.log10(float(p_pos + 1) / (cantidad_terminos_por_clase['pos'] + total_set + 1))
                else:
                    log_pos = math.log10(float(p_pos + 1) / (cantidad_terminos_por_clase['pos'] + total_set))
                if p_neg == 0:
                    log_neg = math.log10(float(p_neg + 1) / (cantidad_terminos_por_clase['neg'] + total_set + 1))
                else:
                    log_neg = math.log10(float(p_neg + 1) / (cantidad_terminos_por_clase['neg'] + total_set))
                log_clases_pos += log_pos
                log_clases_neg += log_neg
            if prob_clase[0]['pos'] + log_clases_pos > max:
                max = prob_clase[0]['pos'] + log_clases_pos
                clase = 'pos'
            if prob_clase[0]['neg'] + log_clases_neg > max:
                max = prob_clase[0]['neg'] + log_clases_neg
                clase = 'neg'
            if clase == 'pos':
                pos += 1
            if clase == 'neg':
                neg += 1
            dar_respuesta(doc,path_to_respuesta, clase, path)
        print('El total de documentos es: ' + str(total_doc) + ' de la carpeta: ' + d)
        print('El total de documentos positivos fue: ' + str(pos))
        print('El total de documentos negativos fue: ' + str(neg))


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


# clasificar('C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje', 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\prediccion')

