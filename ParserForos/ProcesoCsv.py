""""
Created on 15-05-2019

@author: FJSB

Genera el archivo csv

"""

import csv


def generar_csv(nombre_txt, lista_mensajes):

    ruta_csv = nombre_txt + '.csv'
    keys = lista_mensajes[0].keys()

    print('Generando 3', nombre_txt, lista_mensajes[0], ruta_csv)

    with open(ruta_csv, 'w', encoding='utf8') as output_file:  # Just use 'w' mode in 3.x
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(lista_mensajes)

    print('Generando 3', ruta_csv, keys)

    print('Fichero CSV general creado: ' + ruta_csv)

    return ruta_csv