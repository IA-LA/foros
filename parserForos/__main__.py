""""
Created on 15-05-2019

@author: FJSB
"""

from ProcesoParametros import *
from ProcesoUtf8 import *
from ProcesoTxt import *
from ProcesoCsv import *
from ProcesoXlsx import *

import re

if __name__ == '__main__':

    ficheros = filtrar_parametros(sys.argv)

    # PARA CADA FICHERO #
    for index, fichero in enumerate(ficheros):

        # Maneja Dict as Object
        class AttributeDict(dict):
            def __getattr__(self, name):
                if name in self:
                    return self[name]
                raise AttributeError(name)

        fichero = AttributeDict(fichero)

        # # .TXT UTF8 # #
        rutaynombreUtf8 = generar_utf8(fichero.rutaynombreyextensionTxt)

        # # PRE PROCESADO INICIO # #

        # # 1. MENSAJES # #
        print('Generando 1', rutaynombreUtf8, fichero.id_asignatura)
        # lista_de_mensajes = generar_mensajes_base(rutaynombreUtf8, id_asignatura)
        lista_de_mensajes = generar_mensajes_ampliado(rutaynombreUtf8, fichero.id_asignatura)
        lista_de_hilos = generar_hilos(lista_de_mensajes, 'Hilo')
        lista_de_autores = generar_autores(lista_de_mensajes, lista_de_hilos, 'Remitente')
        #lista_de_asignaturas = generar_asignaturas(lista_de_mensajes, lista_de_hilos, lista_de_autores, 'Asignaturas')

        # # PARTICIONES # #
        # info = partir_x_campo(lista_de_mensajes, 'Mensaje')
        # repartir_x_campo(lista_de_mensajes, 'Remitente')
        # repartir_x_campo(lista_de_mensajes, 'Asignatura')
        info = partir_x_campo(lista_de_mensajes, 'Foro')
        print(info[2])
        print(info[3])

        ########################
        #exit(0)
        ########################

        # # ARBOLES # #
        # generar_arbol_default(info[0], 'Mensaje',  'Respuesta')
        generar_arbol_default(info[0], 'Mensaje', 'Responde a')
        # generar_arbol(info[0], 'Mensaje', 'Responde a', 0)
        generar_arbol(info[0], 'Mensaje', 'Respuesta', 0)
        ########################
        # exit(0)
        ########################


        # # 2. LIMPIEZA de Mensajes ([IMAGE: ] y FOROS Profesor-Tutor # #
        print('\nGenerando 1 Mensaje', re.compile('\(.*\)\,').split(lista_de_mensajes[0]['Texto mensaje']))
        ## limpiarImagenMensaje('[IMAGE:.')

        # # PRE PROCESADO FIN # #

        # # .CSV # #
        print('\nGenerando 1 .CSV', fichero.rutaynombre, lista_de_mensajes[0])
        #rutaynombreyextensionCsv = generar_csv(rutaynombre, lista_de_mensajes)
        rutaynombreyextensionCsv_mensajes = generar_csv(fichero.rutaynombre + '_mensajes', lista_de_mensajes)
        rutaynombreyextensionCsv_hilos = generar_csv(fichero.rutaynombre + '_hilos', lista_de_hilos)
        rutaynombreyextensionCsv_autores = generar_csv(fichero.rutaynombre + '_autores', lista_de_autores)
        #rutaynombreyextensionCsv_asignaturas = generar_csv(fichero.rutaynombre + '_asignaturas', lista_de_asignaturas)

        # # Pandas DATA FRAME # #
        print('\nGenerando 1 Pandas DATA FRAME del .CSV', rutaynombreyextensionCsv_mensajes)
        # pandas_df = generar_df(rutaynombreyextensionCsv)
        pandas_df_mensajes = generar_df(rutaynombreyextensionCsv_mensajes)
        pandas_df_hilos = generar_df(rutaynombreyextensionCsv_hilos)
        pandas_df_autores = generar_df(rutaynombreyextensionCsv_autores)
        # pandas_df_asignaturas = generar_df(rutaynombreyextensionCsv_asignaturas)

        # # .XSLX # #
        print('\nGenerando 1 .XLSX', pandas_df_mensajes, fichero.rutaynombre)
        # Escribe hoja GENERAL
        # escribir_excel(pandas_df, rutaynombre, 'General')
        # Escribe hoja de características GENERAL
        escribir_excel(pandas_df_mensajes, fichero.rutaynombre + '_caracteristicas', 'Mensajes')
        escribir_excel(pandas_df_hilos, fichero.rutaynombre + '_caracteristicas', 'Hilos')
        escribir_excel(pandas_df_autores, fichero.rutaynombre + '_caracteristicas', 'Autores')
        # escribir_excel(pandas_df_asignaturas, fichero.rutaynombre + '_caracteristicas', 'Asignaturas')

        # Genera y escribe hojas PARCIALES
        #generar_hojas_default(fichero.rutaynombre)  ## ORIGINALES

        #generar_hojas_base(fichero.rutaynombre)
        #generar_hojas_ampliada(fichero.rutaynombre)

