""""
Created on 22-01-2019

@author: Aitor Diaz Medina

Generación de archivos de texto por cada mensaje del csv importado
"""

import pandas as pd
import os
import sys


def leer_archivo(input_file):
    df = pd.read_csv(input_file)
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    return df


def generar_archivos_cuerpo_default(input_file):
    df = leer_archivo(input_file)
    eleccion = ""
    while eleccion != '1' and eleccion != '2' and eleccion != '3':
        print('Opciones: ')
        print('1. Separar por foros.')
        print('2. Separar por hilos.')
        print('3. No separar.')

        eleccion = input()

    raiz = 'asig' + str(df.loc[0, 'Asignatura'])
    if not os.path.exists(raiz):
        os.makedirs(raiz)

    if eleccion == '1':
        for index, row in df.iterrows():
            hilo = str(row['Hilo'])
            directory = raiz + '/' + hilo
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(directory + "/" + row['Mensaje'] + ".txt", "w") as text_file:
                print(f"" + row['Texto mensaje'], file=text_file)
    elif eleccion == '2':
        for index, row in df.iterrows():
            foro = str(row['Foro'])
            hilo = str(row['Hilo'])
            directory = raiz + '/' + foro + '/' + hilo
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(directory + "/" + row['Mensaje'] + ".txt", "w") as text_file:
                print(f"" + row['Texto mensaje'], file=text_file)
    else:
        for index, row in df.iterrows():
            directory = raiz
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(directory + "/" + row['Mensaje'] + ".txt", "w") as text_file:
                print(f"" + row['Texto mensaje'], file=text_file)

    print('Creados ficheros en carpeta ' + raiz)


def generar_archivos_cuerpo(input_file):
    df = leer_archivo(input_file)
    eleccion = ""
    while eleccion != '1' and eleccion != '2' and eleccion != '3':
        print('Opciones: ')
        print('1. Separar por foros.')
        print('2. Separar por hilos.')
        print('3. No separar.')

        eleccion = input()

    raiz = 'asig' + str(df.loc[0, 'Asignatura'])
    if not os.path.exists(raiz):
        os.makedirs(raiz)

    if eleccion == '2':
        for index, row in df.iterrows():
            hilo = str(row['Hilo'])
            directory = raiz + '/' + hilo
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(directory + "/" + row['Mensaje'] + ".txt", "w") as text_file:
                print(f"" + row['Texto mensaje'], file=text_file)
    elif eleccion == '1':
        for index, row in df.iterrows():
            foro = str(row['Foro'])
            hilo = str(row['Hilo'])
            directory = raiz + '/' + foro + '/' + hilo
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(directory + "/" + row['Mensaje'] + ".txt", "w") as text_file:
                print(f"" + row['Texto mensaje'], file=text_file)
    elif eleccion == '3':
        for index, row in df.iterrows():
            directory = raiz
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(directory + "/" + row['Mensaje'] + ".txt", "w") as text_file:
                print(f"" + row['Texto mensaje'], file=text_file)

    print('Creados ficheros en carpeta ' + raiz)


if __name__ == '__main__':
    generar_archivos_cuerpo(sys.argv[1])
