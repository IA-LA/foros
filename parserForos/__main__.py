""""
Created on 15-05-2019

@author: FJSB
"""

from ProcesoParametros import *
from ProcesoUtf8 import *
from ProcesoTxt import *
from ProcesoCsv import *
from ProcesoXlsx import *

lista_de_mensajes_global = []
lista_de_hilos_global = []
lista_de_autores_global = []

lista_de_mensajes_global_cluster = []
lista_de_hilos_global_cluster = []
lista_de_autores_global_cluster = []

lista_de_mensajes_global_clasificador = []
lista_de_hilos_global_clasificador = []
lista_de_autores_global_clasificador = []

if __name__ == '__main__':

    # FILTRA LOS PARAMETROS (de línea de comandos)
    ficheros = filtrar_parametros(sys.argv)
    #print(ficheros)
    #exit(999)

    ###########
    # PRUEBAS #
    ###########
    #print(sys.float_info)
    #print(sys.maxsize)
    #print(ficheros[0]['ruta'], ficheros[0]['rutaynombre'])
    #pandas_df_mensajes = {}
    #pandas_df_mensajes = leer_excel(ficheros[0]['ruta'] + 'anotados\\1\\Foros_Alvaro_Anotados_default', 'General')
    #print(pandas_df_mensajes['Anotado'].to_numpy()[0])
    #if os.path.isfile(ficheros[0]['rutaynombre'] + '_Anotados.xlsx'):
    #    pandas_df_mensajes_clase = leer_excel(ficheros[0]['rutaynombre'] + '_Anotados', 'General')
    #    print(pandas_df_mensajes_clase['Anotado'].to_numpy()[756], len(pandas_df_mensajes_clase['Anotado'].to_numpy()))
    #exit(999)

    pandas_df_mensajes_clase = []

    # PARA CADA FICHERO #
    for index, fichero in enumerate(ficheros):

        # Maneja Dict as Object
        class AttributeDict(dict):
            def __getattr__(self, name):
                if name in self:
                    return self[name]
                raise AttributeError(name)

        fichero = AttributeDict(fichero)

        ###########################################
        # LOCAL
        ###########################################

        # # .TXT UTF8 # #
        rutaynombreUtf8 = generar_utf8(fichero.rutaynombreyextensionTxt)

        # # PRE PROCESADO INICIO # #

        # # 1. MENSAJES # #
        print('Generando 1.JSON')
        #print('Generando 1.JSON', rutaynombreUtf8, fichero.id_asignatura)

        # # JSON WEKA
        # lista_de_mensajes = generar_mensajes_base(rutaynombreUtf8, id_asignatura)
        lista_de_mensajes_anonimos = generar_mensajes_anonimo(rutaynombreUtf8, fichero.id_asignatura, fichero.ano, '')
        lista_de_mensajes = generar_mensajes_ampliado(rutaynombreUtf8, fichero.id_asignatura, fichero.ano, '')
        lista_de_hilos = generar_hilos(lista_de_mensajes, 'Hilo', fichero.ano, '')
        lista_de_autores = generar_autores(lista_de_mensajes, lista_de_hilos, 'Remitente', fichero.ano, '')
        #lista_de_foros = generar_asignaturas(lista_de_mensajes, lista_de_hilos, lista_de_autores, 'Foro', fichero.ano, '')
        #lista_de_asignaturas = generar_asignaturas(lista_de_mensajes, lista_de_hilos, lista_de_autores, lista_de_foros 'Asignaturas', fichero.ano, '')

        # # JSON WEKA GLOBAL
        # (acumulado mensajes, hilos y ) # #
        lista_de_mensajes_global += lista_de_mensajes
        lista_de_hilos_global += lista_de_hilos
        # (y autores) se hace al final con el acumulado #
        #lista_de_autores_global += lista_de_autores

        # # JSON WEKA CLUSTER
        # (sin Títulos ni Textos) # #
        #lista_de_mensajes_cluster = generar_mensajes_ampliado(rutaynombreUtf8, fichero.id_asignatura, fichero.ano, 'cluster')
        #lista_de_hilos_cluster = generar_hilos(lista_de_mensajes, 'Hilo', fichero.ano, 'cluster')
        #lista_de_autores_cluster = generar_autores(lista_de_mensajes, lista_de_hilos, 'Remitente', fichero.ano, 'cluster')

        # # JSON WEKA GLOBAL CLUSTER
        # (acumulado mensajes, hilos y ) # #
        #lista_de_mensajes_global_cluster += lista_de_mensajes_cluster
        #lista_de_hilos_global_cluster += lista_de_hilos_cluster
        # (y autores) se hace al final con el acumulado #
        #lista_de_autores_global_cluster += lista_de_autores_cluster

        # # JSON WEKA CLASIFICADOR
        # (sin Títulos ni Textos y con la clase) #
        # SI EXISTE FICHERO ANOTADO CON LA CLASE '_Anotados.xlsx' # #
        if os.path.isfile(fichero.rutaynombre + '_Anotados.xlsx'):
            pandas_df_mensajes_clase = leer_excel(fichero.rutaynombre + '_Anotados', 'General')
            #print(pandas_df_mensajes_clase['Anotado'].to_numpy()[2], len(pandas_df_mensajes_clase['Anotado'].to_numpy()))

            lista_de_mensajes_clasificador = generar_mensajes_ampliado(rutaynombreUtf8, fichero.id_asignatura, fichero.ano, 'clasificador', pandas_df_mensajes_clase['Anotado'].to_numpy())
            lista_de_hilos_clasificador = generar_hilos(lista_de_mensajes, 'Hilo', fichero.ano, 'clasificador', pandas_df_mensajes_clase['Anotado'].to_numpy())
            #lista_de_autores_clasificador = generar_autores(lista_de_mensajes, lista_de_hilos, 'Remitente', fichero.ano, 'clasificador', pandas_df_mensajes_clase['Anotado'].to_numpy())

            # # JSON WEKA GLOBAL CLASIFICADOR
            # (acumulado mensajes, hilos y ) # #
            lista_de_mensajes_global_clasificador += lista_de_mensajes_clasificador
            lista_de_hilos_global_clasificador += lista_de_hilos_clasificador
            # (y autores) se hace al final con el acumulado #
            #lista_de_autores_global_clasificador += lista_de_autores_clasificador

            # # .CSV WEKA CLASIFICADOR
            # (sin Títulos ni Textos y con la clase) #
            rutaynombreyextensionCsv_mensajes_clasificador = generar_csv(fichero.rutaynombre + '_mensajes_clasificador',
                                                                         lista_de_mensajes_clasificador)
            rutaynombreyextensionCsv_hilos_clasificador = generar_csv(fichero.rutaynombre + '_hilos_clasificador',
                                                                      lista_de_hilos_clasificador)
            #rutaynombreyextensionCsv_autores_clasificador = generar_csv(fichero.rutaynombre + '_autores_clasificador',
            #                                                            lista_de_autores_clasificador)

            # ANOTADOS {T,O,T/O} y {O,T,T/O}
            pandas_df_mensajes_anotados = generar_df(rutaynombreyextensionCsv_mensajes_clasificador)
            pandas_df_autores_anotados = generar_df(rutaynombreyextensionCsv_hilos_clasificador)

            escribir_excel(pandas_df_mensajes_anotados, fichero.rutaynombre + '_anotados_auto', 'Mensajes')
            escribir_excel(pandas_df_autores_anotados, fichero.rutaynombre + '_anotados_auto', 'Hilos')

        ###################
        # ANÁLISIS de TEXTO
        ###################
        from procesadoGeneral import tokenizado
        from procesadoGeneral import enraizado
        from procesadoGeneral import postag
        from procesadoGeneral import cluster

        #var_token = tokenizado(texto.strip())
        #print('TOKENIZADO(', n_mensajes_hilo, '): ', var_token)

        #var_raiz = enraizado()
        #print('RAICES: ', var_raiz)

        #var_pos = postag(texto.strip())
        #print('POSTAG: ', var_pos)

        #exit(999)

        #
        # ANÁLISIS del TITULO DEL TEXTO ????????????????????????????????????????????????????????????????????
        #
        #

        # exit(999)

        #
        # TOPIC MODELLING, t-SNE, Spectral Clusterin de un MENASJE ?????????????????????????????????????????
        #
        #

        # exit(999)

        ###################
        # CLÚSTER de TEXTO
        ###################

        #var_clu = cluster(lista_de_autores_cluster)
        #print('CLUSTER: ', var_clu)

        #exit(999)

        # # PARTICIONES # #
        # info = partir_x_campo(lista_de_mensajes, 'Mensaje')
        # repartir_x_campo(lista_de_mensajes, 'Remitente')
        # repartir_x_campo(lista_de_mensajes, 'Asignatura')
        #info = partir_x_campo(lista_de_mensajes, 'Foro')
        #print(info[2])
        #print(info[3])

        ########################
        #exit(0)
        ########################

        # # ARBOLES # #
        # generar_arbol_default(info[0], 'Mensaje',  'Respuesta')
        #generar_arbol_default(info[0], 'Mensaje', 'Responde a')
        # generar_arbol(info[0], 'Mensaje', 'Responde a', 0)
        #generar_arbol(info[0], 'Mensaje', 'Respuesta', 0)
        ########################
        #exit(0)
        ########################


        # # 2. LIMPIEZA de Mensajes ([IMAGE: ] y FOROS Profesor-Tutor # #
        # print('\nGenerando 1 Mensaje', re.compile('\(.*\)\,').split(lista_de_mensajes[0]['Texto mensaje']))
        # # limpiarImagenMensaje('[IMAGE:.')

        # # PRE PROCESADO FIN # #

        # # .CSV # #
        print('\nGenerando 1 .CSV')
        # print('\nGenerando 1 .CSV', fichero.rutaynombre, lista_de_mensajes[0])
        # rutaynombreyextensionCsv = generar_csv(rutaynombre, lista_de_mensajes)
        rutaynombreyextensionCsv_mensajes = generar_csv(fichero.rutaynombre + '_mensajes', lista_de_mensajes)
        rutaynombreyextensionCsv_hilos = generar_csv(fichero.rutaynombre + '_hilos', lista_de_hilos)
        rutaynombreyextensionCsv_autores = generar_csv(fichero.rutaynombre + '_autores', lista_de_autores)
        #rutaynombreyextensionCsv_asignaturas = generar_csv(fichero.rutaynombre + '_asignaturas', lista_de_asignaturas)

        # # .CSV WEKA CLUSTER
        # (sin Títulos ni Textos) # #
        #rutaynombreyextensionCsv_mensajes_cluster = generar_csv(fichero.rutaynombre + '_mensajes_cluster', lista_de_mensajes_cluster)
        #rutaynombreyextensionCsv_hilos_cluster = generar_csv(fichero.rutaynombre + '_hilos_cluster', lista_de_hilos_cluster)
        #rutaynombreyextensionCsv_autores_cluster = generar_csv(fichero.rutaynombre + '_autores_cluster', lista_de_autores_cluster)

        # # Pandas DATA FRAME # #
        print('\nGenerando 1 Pandas DATA FRAME del .CSV')
        #print('\nGenerando 1 Pandas DATA FRAME del .CSV', rutaynombreyextensionCsv_mensajes)
        # pandas_df = generar_df(rutaynombreyextensionCsv)
        pandas_df_mensajes = generar_df(rutaynombreyextensionCsv_mensajes)
        pandas_df_hilos = generar_df(rutaynombreyextensionCsv_hilos)
        pandas_df_autores = generar_df(rutaynombreyextensionCsv_autores)
        # pandas_df_asignaturas = generar_df(rutaynombreyextensionCsv_asignaturas)

        # # .XSLX # #
        print('\nGenerando 1 .XLSX')
        #print('\nGenerando 1 .XLSX', pandas_df_mensajes, pandas_df_hilos, pandas_df_autores, fichero.rutaynombre)
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

    ###########################################
    # GLOBAL
    ###########################################
    if ficheros != []:
        print('GLOBAL MENSJAES')
        #print('GLOBAL M', lista_de_mensajes_global)
        print()
        print('GLOBAL HIKOS')
        #print('GLOBAL H', lista_de_hilos_global)
        print()
        print('GLOBAL AUTORES')
        #print('GLOBAL A', lista_de_autores_global)

        # # JSON WEKA GLOBAL
        # (acumulado autores) # #
        lista_de_autores_global += generar_autores(lista_de_mensajes_global, lista_de_hilos_global, 'Remitente', ficheros[0]['ano'], '')

        # # JSON WEKA GLOBAL CLUSTER
        # (acumulado mensajes, hilos, autores sin Títulos ni Textos) # #
        #lista_de_autores_global_cluster += generar_autores(lista_de_mensajes_global, lista_de_hilos_global, 'Remitente', ficheros[0]['ano'], 'cluster')

        # # .CSV WEKA GLOBAL
        # (Sin Títulos ni Textos) # #
        rutaynombreyextensionCsv_mensajes_global = generar_csv(ficheros[0]['ruta'] + 'acu_mensajes_global', lista_de_mensajes_global)
        rutaynombreyextensionCsv_hilos_global = generar_csv(ficheros[0]['ruta'] + 'acu_hilos_global', lista_de_hilos_global)
        rutaynombreyextensionCsv_autores_global = generar_csv(ficheros[0]['ruta'] + 'acu_autores_global', lista_de_autores_global)

        # # .CSV WEKA GLOBAL CLUSTER
        # (Sin Títulos ni Textos) # #
        #rutaynombreyextensionCsv_mensajes_global_cluster = generar_csv(ficheros[0]['ruta'] + 'acu_mensajes_global_cluster', lista_de_mensajes_global_cluster)
        #rutaynombreyextensionCsv_hilos_global_cluster = generar_csv(ficheros[0]['ruta'] + 'acu_hilos_global_cluster', lista_de_hilos_global_cluster)
        #rutaynombreyextensionCsv_autores_global_cluster = generar_csv(ficheros[0]['ruta'] + 'acu_autores_global_cluster', lista_de_autores_global_cluster)

        # # .CSV WEKA GLOBAL CLASIFICADOR
        # (Sin Títulos ni Textos y con la clase) #
        # SI EXISTE FICHERO ANOTADO CON LA CLASE '_Anotados.xlsx' # #
        if len(pandas_df_mensajes_clase) != 0:
            rutaynombreyextensionCsv_mensajes_global_clasificador = generar_csv(ficheros[0]['ruta'] + 'acu_mensajes_global_clasificador', lista_de_mensajes_global_clasificador)
            rutaynombreyextensionCsv_hilos_global_clasificador = generar_csv(ficheros[0]['ruta'] + 'acu_hilos_global_clasificador', lista_de_hilos_global_clasificador)
            #rutaynombreyextensionCsv_autores_global_clasificador = generar_csv(ficheros[0]['ruta'] + 'acu_autores_global_clasificador', lista_de_autores_global_clasificador)