__author__ = 'Yanet'
import pre_procesing_text
import algorithm
import knn


# print('Por favor tenga mucha paciencia (muchaaaaaaaaaaaaaaaaaaa) para esperar por la respuesta de estos algoritmos, ')
# print('puede disfrutar usted mientras tanto de una buena pelicula, le recomiendo "The Guardians of the Galaxy"')

#Prepocesamiento a el Corpus de entrenamiento
# pre_procesing_text.cleaner_text('D:\\Corpus\\aprendizaje\\neg', 'neg', 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje\\')
# pre_procesing_text.cleaner_text('D:\\Corpus\\aprendizaje\\pos', 'pos', 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje\\')


path = 'D:\\Corpus\\respuesta' #Este es el path a modificar por el profesor
path_to_prediccion = 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\prediccion\\'
path_to_aprendizaje = 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\aprendizaje'
path_to_respuesta_nb = 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\respuesta_nb'
path_to_respuesta_knn = 'C:\\Users\\Yanet\\PycharmProjects\\naive_bayes_class\\respuesta_knn'

#Preprocesamiento a el Corpus a predecir su clase
pre_procesing_text.cleaner_text(path, 'test', path_to_prediccion)

#Clasificacion con Naive Bayes
algorithm.clasificar(path_to_aprendizaje, path_to_prediccion, path_to_respuesta_nb, path)

#Clasificacion con KNN
knn.clasificar(path_to_aprendizaje, path_to_prediccion, path_to_respuesta_knn, path)


print('Muchas Gracias')

# import os
# f = open('D\\a.txt', 'w')
# f.write('hola')