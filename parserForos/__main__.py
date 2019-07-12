""""
Created on 15-05-2019

@author: FJSB
"""

from ProcesoUtf8 import *
from ProcesoTxt import *
from ProcesoCsv import *
from ProcesoXlsx import *

import re

if __name__ == '__main__':

    # 2 Argumentos por línea de comandos:
    #               FICHERO         sys.argv[1]:    "D:\ruta\nombre.txt"
    #               ID-ASIGNATURA   sys.argv[2]:    "71901037"
    #   "D:\ruta\Python\ParserForos\ParserForos\foros\nombre.txt" "71901037"

    # # .TXT # #
    # Argumento 1.0: ruta + nombre
    rutaynombre = os.path.splitext(sys.argv[1])[0]
    # Argumento 1: ruta + nombre + extensión
    rutaynombreyextensionTxt = sys.argv[1]
    # Argumento 2: ID asignatura
    id_asignatura = sys.argv[2]

    # # .TXT UTF8 # #
    rutaynombreUtf8 = generar_utf8(rutaynombreyextensionTxt)

    # # PRE PROCESADO INICIO # #

    # # 1. MENSAJES # #
    print('Generando 1', rutaynombreUtf8, id_asignatura)
    # lista_de_mensajes = generar_mensajes_base(rutaynombreUtf8, id_asignatura)
    lista_de_mensajes = generar_mensajes_ampliado(rutaynombreUtf8, id_asignatura)
    lista_de_hilos = generar_hilos(lista_de_mensajes, 'Hilo')
    #lista_de_autores = generar_autores(lista_de_mensajes, lista_de_hilos, 'Autores')
    #lista_de_asignaturas = generar_asignaturas(lista_de_mensajes, lista_de_hilos, lista_de_autores, 'Asignaturas')

    partir_x_campo(lista_de_mensajes, 'Hilo')
    #repartir_x_campo(lista_de_mensajes, 'Remitente')
    # repartir_x_campo(lista_de_mensajes, 'Asignatura')
    partir_x_campo(lista_de_mensajes, 'Foro')
    generar_hilos(lista_de_mensajes, 'Hilo')

    ########################
    # exit(0)
    ########################

    # # 2. LIMPIEZA de Mensajes ([IMAGE: ] y FOROS Profesor-Tutor # #
    print('\nGenerando 1 Mensaje', re.compile('\(.*\)\,').split(lista_de_mensajes[0]['Texto mensaje']))
    ## limpiarImagenMensaje('[IMAGE:.')

    # # PRE PROCESADO FIN # #

    # # .CSV # #
    print('\nGenerando 1 .CSV', rutaynombre, lista_de_mensajes[0])
    #rutaynombreyextensionCsv = generar_csv(rutaynombre, lista_de_mensajes)
    rutaynombreyextensionCsv_mensajes = generar_csv(rutaynombre + '_mensajes', lista_de_mensajes)
    rutaynombreyextensionCsv_hilos = generar_csv(rutaynombre + '_hilos', lista_de_hilos)
    #rutaynombreyextensionCsv_autores = generar_csv(rutaynombre, lista_de_autores)
    #rutaynombreyextensionCsv_asignaturas = generar_csv(rutaynombre, lista_de_asignaturas)

    # # Pandas DATA FRAME # #
    print('\nGenerando 1 Pandas DATA FRAME del .CSV', rutaynombreyextensionCsv_mensajes)
    # pandas_df = generar_df(rutaynombreyextensionCsv)
    pandas_df_mensajes = generar_df(rutaynombreyextensionCsv_mensajes)
    pandas_df_hilos = generar_df(rutaynombreyextensionCsv_hilos)
    # pandas_df_autores = generar_df(rutaynombreyextensionCsv_autores)
    # pandas_df_asignaturas = generar_df(rutaynombreyextensionCsv_asignaturas)

    # # .XSLX # #
    print('\nGenerando 1 .XLSX', pandas_df_mensajes, rutaynombre)
    # Escribe hoja GENERAL
    # escribir_excel(pandas_df, rutaynombre, 'General')
    # Escribe hoja de características GENERAL
    escribir_excel(pandas_df_mensajes, rutaynombre + '_caracteristicas', 'Mensajes')
    escribir_excel(pandas_df_hilos, rutaynombre + '_caracteristicas', 'Hilos')
    # escribir_excel(pandas_df_autores, rutaynombre + '_caracteristicas', 'Autores')
    # escribir_excel(pandas_df_asignaturas, rutaynombre + '_caracteristicas', 'Asignaturas')

    # Genera y escribe hojas PARCIALES
    #generar_hojas_default(rutaynombre)  ## ORIGINALES

    #generar_hojas_base(rutaynombre)
    #generar_hojas_ampliada(rutaynombre)

