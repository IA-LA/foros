""""
Created on 09-01-2019

@author: Aitor Diaz Medina

Clase principal encargada llamar al parser y generar el archivo csv resultante

"""

import hashlib

# VARIABLES GLOBALES #
curso = 1900
# mensajes = []
hilos = []
usuarios = []
asignaturas = []
foros = []

def month_string_to_number(string):
    m = {
        'ene': 1,
        'feb': 2,
        'mar': 3,
        'abr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'ago': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dic': 12
    }
    s = string.strip()[:3].lower()

    out = m[s]
    return out


## RECUPERACION MENSAJES DESDE FICHERO ##
def generar_mensajes_default(ruta, id_asig):
    with open(ruta, 'r', encoding='utf8') as f:
        lineas = f.readlines()
        lineas = [l.strip('\n') for l in lineas]
        mensajes = []
        # mensaje = []
        id_foro = ""
        # id_asignatura = 12345678
        nombreForo = ""
        id_hilo = ""
        tit_hilo = ""
        id_mensaje = ""
        id_ref_mensaje = ""
        id_autor = ""
        autor = ""
        fecha = ""
        dia_semana = ""
        tit_mensaje = ""
        texto = ""
        estado = 'FIN_MENSAJE'

        for index, linea in enumerate(lineas):

            if linea.startswith('Foro: '):
                print(linea.partition('Foro: ')[2])
                nombreForo = linea.partition('Foro: ')[2]
                id_foro = int(hashlib.sha1(nombreForo.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensajes de la conversación: '):
                tit_hilo = linea.partition('Mensajes de la conversación: ')[2]
                id_hilo = int(hashlib.sha1(tit_hilo.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensaje no. '):
                if ' (Respuesta a no. ' in linea:
                    respuesta = linea.partition(' (Respuesta a no. ')[2].partition(")")[0]
                    no_mensaje = linea.partition('Mensaje no. ')[2].partition(' (Respuesta a no. ')[0]
                    id_mensaje = str(id_hilo) + "_" + no_mensaje
                    id_ref_mensaje = str(id_hilo) + "_" + respuesta

                else:
                    no_mensaje = linea.partition('Mensaje no. ')[2]
                    id_mensaje = str(id_hilo) + "_" + no_mensaje
                    id_ref_mensaje = ""
                # print(no_mensaje)

            elif linea.startswith('Enviado por: '):
                autor = linea.partition('Enviado por: ')[2].partition(" el")[0]
                id_autor = int(hashlib.sha1(autor.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
                fecha = linea.partition(" el ")[2].strip()
                if not lineas[index + 1].startswith('Título: '):
                    # print('bien, estado: ' + estado)
                    fecha = fecha + " " + lineas[index + 1]
                    # print(fecha)
                # else:
                #    print('bien : ' + fecha)
                # print(fecha)

            elif linea.startswith('Título: '):
                # print(lineas[lineas.index(linea)-1])
                # if not lineas[lineas.index(linea)-1].startswith('Enviado por: '):
                #   fecha = fecha.strip() + ' ' + lineas[lineas.index(linea)-1].strip()
                #  print(lineas[lineas.index(linea)-1], fecha)
                # print(linea)
                if no_mensaje == "1":
                    tit_hilo = linea.partition('Título: ')[2]
                tit_mensaje = linea.partition('Título: ')[2]

            elif linea.startswith('----------------------------------------------------------------------'):
                estado = 'FIN_MENSAJE'
                if autor:
                    fecha_parser = fecha.split(' ')
                    dia_semana = fecha_parser[0]
                    fecha = fecha_parser[1] + "/" + str(month_string_to_number(fecha_parser[2])) + "/" + fecha_parser[3]
                    hora = fecha_parser[4]
                    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor,autor,  dia_semana, fecha, tit_mensaje, texto]
                    mensaje = {'Foro': id_foro, 'ForoN': nombreForo, 'Asignatura': id_asig, 'Título': tit_hilo,
                               'Hilo': id_hilo,
                               'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                               'Remitente': id_autor, 'Autor': autor, 'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                               'Título mensaje': tit_mensaje,
                               'Texto mensaje': texto.strip(), 'Caracteres mensaje': len(texto)}
                    mensajes.append(mensaje)
                    texto = ""
                    autor = ""

                    # print(linea)
            elif linea.startswith('==============================================================================='):
                estado = 'FIN_MENSAJE'
                if autor:
                    fecha_parser = fecha.split(' ')
                    dia_semana = fecha_parser[0]
                    fecha = fecha_parser[1] + "/" + str(month_string_to_number(fecha_parser[2])) + "/" + fecha_parser[3]
                    hora = fecha_parser[4].strip()
                    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor,autor,  dia_semana, fecha, tit_mensaje, texto]
                    mensaje = {'Foro': id_foro, 'ForoN': nombreForo, 'Asignatura': id_asig, 'Título': tit_hilo,
                               'Hilo': id_hilo,
                               'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                               'Remitente': id_autor, 'Autor': autor, 'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                               'Título mensaje': tit_mensaje,
                               'Texto mensaje': texto.strip(), 'Caracteres mensaje': len(texto)}
                    mensajes.append(mensaje)
                    texto = ""
                    autor = ""
                    # print(linea)

            if lineas[index - 1].startswith('Título: '):
                estado = 'MENSAJE'

            if estado == 'MENSAJE':
                texto = texto + ' ' + linea

    return mensajes


# INICIO Añadido FJSB
# Base
def generar_mensajes_base(ruta, id_asig):
    with open(ruta, 'r', encoding='utf8') as f:
        lineas = f.readlines()
        lineas = [l.strip('\n') for l in lineas]
        mensajes = []
        # mensaje = []

        # Atributos Base
        id_foro = ""
        # id_asignatura = 12345678
        nombre_foro = ""
        id_hilo = ""
        tit_hilo = ""
        id_mensaje = ""
        id_ref_mensaje = ""
        id_autor = ""
        autor = ""
        fecha = ""
        dia_semana = ""
        tit_mensaje = ""
        texto = ""
        estado = 'FIN_MENSAJE'

        for index, linea in enumerate(lineas):

            if linea.startswith('Foro: '):
                print(linea.partition('Foro: ')[2])
                nombre_foro = linea.partition('Foro: ')[2]
                ## Foro
                ## ID = HASH('Título Foro' + 'Date')
                # Hash(FORO)
                id_foro = int(hashlib.sha1(nombre_foro.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensajes de la conversación: '):
                tit_hilo = linea.partition('Mensajes de la conversación: ')[2]
                ## Hilo
                ## ID = HASH('Título del 1er Mensaje del  Hilo' + 'Date')
                # Hash(HILO)
                id_hilo = int(hashlib.sha1(tit_hilo.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensaje no. '):
                if ' (Respuesta a no. ' in linea:
                    respuesta_no = linea.partition(' (Respuesta a no. ')[2].partition(")")[0]
                    mensaje_no = linea.partition('Mensaje no. ')[2].partition(' (Respuesta a no. ')[0]
                    id_mensaje = str(id_hilo) + "_" + mensaje_no
                    id_ref_mensaje = str(id_hilo) + "_" + respuesta_no

                else:
                    mensaje_no = linea.partition('Mensaje no. ')[2]
                    id_mensaje = str(id_hilo) + "_" + mensaje_no
                    id_ref_mensaje = ""
                # print(mensaje_no)

            elif linea.startswith('Enviado por: '):
                autor = linea.partition('Enviado por: ')[2].partition(" el")[0]
                ## Autor
                ## ID = HASH('Nombres Apellidos' + 'Date')
                # Hash(AUTOR)
                id_autor = int(hashlib.sha1(autor.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
                ## Autor anónimo
                autor = id_autor

                fecha = linea.partition(" el ")[2].strip()
                if not lineas[index + 1].startswith('Título: '):
                    # print('bien, estado: ' + estado)
                    fecha = fecha + " " + lineas[index + 1]
                    # print(fecha)
                # else:
                #    print('bien : ' + fecha)
                # print(fecha)

            elif linea.startswith('Título: '):
                # print(lineas[lineas.index(linea)-1])
                # if not lineas[lineas.index(linea)-1].startswith('Enviado por: '):
                #   fecha = fecha.strip() + ' ' + lineas[lineas.index(linea)-1].strip()
                #  print(lineas[lineas.index(linea)-1], fecha)
                # print(linea)
                if mensaje_no == "1":
                    tit_hilo = linea.partition('Título: ')[2]
                tit_mensaje = linea.partition('Título: ')[2]

            elif linea.startswith('----------------------------------------------------------------------'):
                estado = 'FIN_MENSAJE'
                if autor:
                    fecha_parser = fecha.split(' ')
                    dia_semana = fecha_parser[0]
                    fecha = fecha_parser[1] + "/" + str(month_string_to_number(fecha_parser[2])) + "/" + fecha_parser[3]
                    hora = fecha_parser[4]
                    ########################
                    # Derfinición de MENSAJE (base)
                    ########################
                    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor,autor,  dia_semana, fecha, tit_mensaje, texto]
                    mensaje = {'Foro': id_foro, 'ForoN': nombre_foro, 'Asignatura': id_asig, 'Título': tit_hilo,
                               'Hilo': id_hilo,
                               'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                               'Remitente': id_autor, 'Autor': autor, 'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                               'Date': fecha + ' ' + hora,
                               'Título mensaje': tit_mensaje,
                               'Texto mensaje': texto.strip(), 'Caracteres mensaje': len(texto)}
                    mensajes.append(mensaje)
                    texto = ""
                    autor = ""
            elif linea.startswith('==============================================================================='):
                estado = 'FIN_MENSAJE'
                if autor:
                    fecha_parser = fecha.split(' ')
                    dia_semana = fecha_parser[0]
                    fecha = fecha_parser[1] + "/" + str(month_string_to_number(fecha_parser[2])) + "/" + fecha_parser[3]
                    hora = fecha_parser[4].strip()
                    ########################
                    # Derfinición de MENSAJE (base)
                    ########################
                    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor,autor,  dia_semana, fecha, tit_mensaje, texto]
                    mensaje = {'Foro': id_foro, 'ForoN': nombre_foro, 'Asignatura': id_asig, 'Título': tit_hilo,
                               'Hilo': id_hilo,
                               'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                               'Remitente': id_autor, 'Autor': autor, 'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                               'Date': fecha + ' ' + hora,
                               'Título mensaje': tit_mensaje,
                               'Texto mensaje': texto.strip(), 'Caracteres mensaje': len(texto)}
                    mensajes.append(mensaje)
                    texto = ""
                    autor = ""
                    # print(linea)

            if lineas[index - 1].startswith('Título: '):
                estado = 'MENSAJE'

            if estado == 'MENSAJE':
                texto = texto + ' ' + linea

    return mensajes


# Ampliadas
def generar_mensajes_ampliado(ruta, id_asig, curso_asig):
    global mensajes

    print('#######')
    print('MENSAJES')
    print('#######')

    curso = curso_asig

    with open(ruta, 'r', encoding='utf8') as f:
        lineas = f.readlines()
        lineas = [l.strip('\n') for l in lineas]
        mensajes = []
        # mensaje = []

        # Atributos Base
        id_foro = ""
        # id_asignatura = 12345678
        nombre_foro = ""
        id_hilo = ""
        tit_hilo = ""
        id_mensaje = ""
        id_ref_mensaje = ""
        id_autor = ""
        autor = ""
        fecha = ""
        dia_semana = ""
        tit_mensaje = ""
        texto = ""
        estado = 'FIN_MENSAJE'
        mensaje_no = ''

        # Atributos Frecuentistas
        # Mensaje
        size_padre = 0
        size_antecesor = 0
        size_ph = 0
        size_as = 0

        date_padre = ''
        date_antecesor = ''
        date_ph = ''
        date_ph = ''

        padre_hilo = 0
        n_mensajes_hilo = 0
        inicial = 0
        respuesta = 0
        auto_respuesta = 0
        terminal = 0

        hilo = 0

        # Hilo

        # Atributos Textuales
        var_token = {}
        var_raiz = {}
        var_pos = {}

        from datetime import datetime

        for index, linea in enumerate(lineas):

            if linea.startswith('Foro: '):
                print(linea.partition('Foro: ')[2])
                nombre_foro = linea.partition('Foro: ')[2]
                ## Foro
                ## ID = HASH('Título Foro' + 'Date')
                # Hash(FORO)
                id_foro = int(hashlib.sha1(nombre_foro.encode('utf-8') + str(datetime.now()).encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensajes de la conversación: '):
                tit_hilo = linea.partition('Mensajes de la conversación: ')[2]
                ## Hilo
                ## ID = HASH('Título del 1er Mensaje del  Hilo' + 'Date')
                # Hash(HILO)
                id_hilo = int(hashlib.sha1(tit_hilo.encode('utf-8') + str(datetime.now()).encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensaje no. '):
                if ' (Respuesta a no. ' in linea:
                    respuesta_no = linea.partition(' (Respuesta a no. ')[2].partition(")")[0]
                    mensaje_no = linea.partition('Mensaje no. ')[2].partition(' (Respuesta a no. ')[0]
                    id_mensaje = str(id_hilo) + "_" + mensaje_no
                    id_ref_mensaje = str(id_hilo) + "_" + respuesta_no

                else:
                    mensaje_no = linea.partition('Mensaje no. ')[2]
                    id_mensaje = str(id_hilo) + "_" + mensaje_no
                    id_ref_mensaje = ""
                # print(mensaje_no)

            elif linea.startswith('Enviado por: '):
                autor = linea.partition('Enviado por: ')[2].partition(" el")[0]
                ## Autor
                ## ID = HASH('Nombres Apellidos' + 'Date')
                # Hash(AUTOR)
                id_autor = int(hashlib.sha1(autor.encode('utf-8') + str(datetime.now()).encode('utf-8')).hexdigest(), 16) % (10 ** 8)
                ## Autor anónimo
                autor = id_autor

                fecha = linea.partition(" el ")[2].strip()
                if not lineas[index + 1].startswith('Título: '):
                    # print('bien, estado: ' + estado)
                    fecha = fecha + " " + lineas[index + 1]
                    # print(fecha)
                # else:
                #    print('bien : ' + fecha)
                # print(fecha)

            elif linea.startswith('Título: '):
                # print(lineas[lineas.index(linea)-1])
                # if not lineas[lineas.index(linea)-1].startswith('Enviado por: '):
                #   fecha = fecha.strip() + ' ' + lineas[lineas.index(linea)-1].strip()
                #  print(lineas[lineas.index(linea)-1], fecha)
                # print(linea)
                if mensaje_no == "1":
                    tit_hilo = linea.partition('Título: ')[2]
                tit_mensaje = linea.partition('Título: ')[2]

            # MENSAJE 79 caracteres
            # '-------------------------------------------------------------------------------'
            # HILO 79 caracteres
            # '_______________________________________________________________________________'
            # ULTIMO MENSAJE DE CADA HILO: CIERRE DE HILO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # HILO 70 caracteres
            elif linea.startswith('----------------------------------------------------------------------') or \
                    linea.startswith('==============================================================================='):
                    # FORO 79 caracteres
                estado = 'FIN_MENSAJE'
                if autor:
                    fecha_parser = fecha.split(' ')
                    dia_semana = fecha_parser[0]
                    fecha = fecha_parser[1] + "/" + str(month_string_to_number(fecha_parser[2])) + "/" + fecha_parser[3]
                    hora = fecha_parser[4]

                    #######################
                    # Tratamiento AMPLIADO de TEXTO
                    #######################

                    #
                    # ADJUNTOS (DOCUMENTOS, IMAGENES o EMOTICONOS)
                    #

                    import re

                    def tratamiento(item):
                        print(item)
                        return item

                    # Busca archivos Adjuntos y enlaces
                    # Cuenta ADJUNTOS: las [IMAGE: '' ...]
                    imagenes = re.findall(r'(\[IMAGE: \'\'.*\])', texto, re.M | re.I)
                    n_adjs = len(imagenes)
                    t_adj = 0
                    if n_adjs > 0:
                        for imagen in imagenes:
                            t_adj = t_adj + len(imagen)
                    else:
                        t_adj = 0  # '0KB [IMAGE:.*])'

                    # Cuenta EMOJI: las [IMAGE: '.+' ...]
                    n_emojis = len(re.findall(r'(\[IMAGE: \'.+\'.*\])', texto, re.M | re.I))
                    if n_emojis > 0:
                        print('EMOJIS:', n_emojis)

                    # Cuenta LINKS
                    n_links = 0
                    n_links_r = 0

                    # Busca ADJUNTOS Y EMOJIS
                    if texto.find('[IMAGE:') != -1:
                        print('ADJUNTOS ENCONTRADOS: ', n_adjs)
                        # Busca [IMAGE:
                        regex = re.search(r'(\[IMAGE: .*\])', texto, re.M | re.I)
                        if regex != None:
                            # Reemplaza todos los ADJUNTOS Y EMOJIS [IMAGE:] por [DATA] Ampliación: poner tipo [DATA:XXX]
                            texto = re.sub(r'(\[IMAGE: .*\])', '[DATA]', texto)
                            print(regex.group(1))
                            print(texto)
                            # exit(12345567890)

                    # Busca LINKS (eliminados ADJUNTOS y EMOJIS)
                    if texto.find('http') != -1:
                        # Todos los http
                        n_links = len(re.findall(r'(http)', texto, re.M | re.I))
                        print('LINKS ENCONTRADOS: ', n_links)

                    # Busca links
                    n_links_r = len(re.findall(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', texto, re.M | re.I))
                    if n_links_r != 0:
                        # Reemplaza todos los LINKS (http) (sin ADJUNTOS y EMOJIS)
                        texto = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '[LINK]', texto)
                        print('LINKS REEMPLAZADOS: ', n_links_r, texto)

                    #
                    # DIFERENCIAS (len(nombre_foro) + len(tit_hilo) + len(tit_mensaje) + len(texto))
                    #

                    # INICIAL
                    if id_ref_mensaje == '':

                        size_padre = len(tit_mensaje) + len(texto)

                        # Padre-Hijo
                        size_ph = 0

                        # Antecesor-Sucesor
                        size_as = 0

                        size_antecesor = len(tit_mensaje) + len(texto)

                    # RESPUESTAS
                    else:

                        # Padre-Hijo
                        size_ph = (len(tit_mensaje) + len(texto)) - size_padre

                        # Antecesor-Sucesor
                        size_as = (len(tit_mensaje) + len(texto)) - size_antecesor

                        size_antecesor = len(tit_mensaje) + len(texto)

                    #
                    # DISTANCIAS  datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")
                    #
                    from datetime import datetime

                    # INICIAL
                    if id_ref_mensaje == '':

                        date_padre = datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")  # fecha + ' ' + hora

                        # Padre-Hijo en días
                        date_ph = abs(date_padre - date_padre).total_seconds()  # Valor 0
                        # Antecesor-Sucesor en segundos
                        date_as = abs(date_padre - date_padre).total_seconds()  # Valor 0

                        date_antecesor = datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")  # fecha + ' ' + hora

                    # RESPUESTA
                    else:

                        # Padre-Hijo en días
                        date_ph = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - date_padre).total_seconds()  # (fecha + ' ' + hora) - date_padre

                        # Antecesor-Sucesor en segundos
                        date_as = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - date_antecesor).total_seconds()  # (fecha + ' ' + hora) - date_antecesor

                        date_antecesor = datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")  # fecha + ' ' + hora

                        # 1er Mensaje
                        if len(mensajes) == 0:
                            print(date_ph, date_as)

                    # DISTANCIA AL ORIGEN #
                    # Permite ordenar por fecha de forma directa #
                    date_origen = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - datetime.strptime('01/01/2017 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds()

                    #
                    # TIPOS MENSAJE (INICIAL, RESPUESTA o TERMINAL)
                    #

                    # Tipos x posición
                    # INICIAL
                    if id_ref_mensaje == '':

                        # Define PADRE HILO
                        # controla si son auto-respuestas o participantes distintos

                        # Excepción:
                        # Si la variable 'padre_hilo' no exite la inicializa
                        try:
                            padre_hilo = padre_hilo
                            padre_hilo = id_autor
                        except NameError:
                            padre_hilo = id_autor

                        inicial = 1
                        respuesta = 0  # 'inicial'
                        auto_respuesta = 0  # 'no'
                        terminal = 0  # 'sinrespuesta'

                        # Redefine TERMINAL
                        # si un menssaje es Inicial
                        # revisa los anteriores (-1,-2,-3,-4,...)
                        # anotándoles como Terminal

                        # Excepción:
                        # Si la variable 'n_mensajes_hilo' no exite la inicializa
                        try:
                            n_mensajes_hilo = n_mensajes_hilo
                        except NameError:
                            n_mensajes_hilo = 1

                        for i in range(1, n_mensajes_hilo, 1):
                            # Mensaje único del hilo
                            # 0 'sinrespuesta'
                            mensajes[len(mensajes) - i]['Terminal'] = -i

                        # Mensaje INICIAL del Hilo
                        n_mensajes_hilo = 1
                        hilo = 1

                    # RESPUESTA o TERMINAL
                    # id_ref_mensaje != ''
                    else:
                        inicial = n_mensajes_hilo
                        # HILO
                        # AUTO-RESPUESTA
                        auto_respuesta = 0
                        if padre_hilo == id_autor:
                            auto_respuesta = 1  # 'autorespuesta', "rectificación", "agradecimiento"
                        # SUBHILO
                        if int(id_mensaje.split('_')[1]) - int(id_ref_mensaje.split('_')[1]) != 1:
                            subpadre = id_ref_mensaje.split('_')[1]
                            if respuesta > 0:  # & int(subpadre) != respuesta:
                                respuesta = - int(subpadre)
                                hilo = - int(subpadre)  # "subhilos 1,2,3,4,..."
                            else:
                                respuesta = int(subpadre)
                                hilo = int(subpadre)  # "subhilos 1,2,3,4,..."
                        else:
                            respuesta = hilo  # "subhilos 1,2,3,4,..."
                        # TERMINAL
                        terminal = 0  # 'posible'

                    ###################
                    # ANÁLISIS de TEXTO
                    ###################
                    from procesadoGeneral import tokenizado
                    from procesadoGeneral import enraizado
                    from procesadoGeneral import postag

                    #var_token = tokenizado(texto.strip())
                    #print('TOKENIZADO(', n_mensajes_hilo, '): ', var_token)

                    #var_raiz = enraizado()
                    #print('RAICES: ', var_raiz)

                    # var_pos = postag(texto.strip())
                    # print('POSTAG: ', var_pos)

                    # exit(9999999)

                    #
                    # ANÁLISIS de TITULO DE EXTO ??????????????????????????????????????????????????????????????????????
                    #

                    # Actualización Nº
                    # Mensaje RESPUESTA del Hilo
                    n_mensajes_hilo = n_mensajes_hilo + 1

                    ########################
                    # Derfinición de MENSAJE (ampliado)
                    ########################
                    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor,autor,  dia_semana, fecha, tit_mensaje, texto]
                    mensaje = {
                        # BASE #
                        'Asignatura': id_asig,
                        'Foro': id_foro, 'Nombre foro': nombre_foro, 'Caracteres foro': len(nombre_foro),
                        'Hilo': id_hilo, 'Título': tit_hilo, 'Caracteres hilo': len(tit_hilo),
                        'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                        'Remitente': id_autor, 'Autor': autor,
                        # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                        'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
                        # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                        'Día': dia_semana, 'Fecha': fecha, 'Hora': hora, 'Date': fecha + ' ' + hora,
                        'Distancia PH': date_ph, 'Distancia AS': date_as, 'Distancia OO': date_origen,
                        # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                        'Título mensaje': tit_mensaje, 'Caracteres título mensaje': len(tit_mensaje),
                        'Texto mensaje': texto.strip(), 'Caracteres texto mensaje': len(texto),
                        'Diferencia PH': size_ph, 'Diferencia AS': size_as,
                        # ANÁLISIS de TEXTO
                        # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                        'Tokens':  var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras}
                        "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                        # .SnowballStemmer("spanish").stem,
                        'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas}
                        'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                        # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                        'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                        'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                        'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                        'Curso': curso,
                    }
                    mensajes.append(mensaje)

                    ## Limpia variables
                    texto = ""
                    autor = ""
                    # print(linea)

            if lineas[index - 1].startswith('Título: '):
                estado = 'MENSAJE'

            if estado == 'MENSAJE':
                texto = texto + ' ' + linea

    return mensajes


## PARTO x CAMPOS ##
def partir_x_campo(lista, campo):
    global mensajes
    global hilos
    global usuarios
    global asignaturas
    global foros

    print('#######')
    print('CAMPO')
    print('#######')
    destino = []
    lista_destino = []
    # Valor inicial del CAMPO de partición
    # y del campo anterior
    campo_anterior = lista[0].get(campo)
    #

    print(lista)
    jndex = 0
    for index, li in enumerate(lista):
        val = li.get(campo)
        # print(val)
        if val != campo_anterior:  # NUEVA INSTANCIA x CAMPO: Hilo, Remitente o Autor,

            campo_anterior = val
            # Array repartido por 'campo'
            destino.insert(jndex, lista_destino)
            jndex = jndex + 1

            # print('PARTE POR UN NUEVO CAMPO', index, jndex, val)
            lista_destino = []
            lista_destino.append(li)
        else:
            lista_destino.append(li)

    return destino


## REPARTO x CAMPOS ##
def repartir_x_campo(lista, campo):
    global mensajes
    global hilos
    global usuarios
    global asignaturas
    global foros

    print('#######')
    print('CAMPO')
    print('#######')
    indice = {}
    destino = []
    destino2d = []
    campo_anterior = lista[0].get(campo)
    #

    print(lista)
    jndex = 0
    for index, li in enumerate(lista):
        val = li.get(campo)
        print(val)

        destino2d['jo'] = 1


    print(destino2d)
    return destino2d


## PROCESADO MENSAJES ##
def generar_mensajes(mensajes, campo, ruta, id_asig, curso_asig):

    print('#######')
    print('MENSAJES')
    print('#######')

    curso = curso_asig

    return mensajes


## PROCESADO HILOS ##
def generar_hilos(mensajes, campo, curso_asig):
    global hilos

    print('#######')
    print('HILOS')
    print('#######')
    hilos = []
    curso = curso_asig
    # Valor inicial del CAMPO de partición
    # anterior = mensajes[0].get(campo)

    # Excepción:
    # Si la variable 'id_hilo_anterior' no exite la inicializa
    # Si la variable 'cambia_subhilo' no exite la inicializa (vale 1: si es el mismo subhilo, vale -1: si cambia el subhilo)
    try:
        # ID de hilo
        id_hilo_anterior
        # interruptor de cambio de hilo #
        cambia_subhilo = 1
    except NameError:
        print("well, it WASN'T defined after all!")
        id_hilo_anterior = 0
        cambia_subhilo = 1
    else:
        print("sure, it was defined.")
        id_hilo_anterior = 0
        cambia_subhilo = 1
    # Fin excepción

    # Variables Globales
    autores_previos = []
    foro_previo = 0

    # Totales
    n_mensajes = 0
    n_autores = 0
    n_hilos = 0
    n_foros = 0
    n_subhilos = 0
    n_auto_respuestas = 0
    longitud = 0  # Tamaño texto
    distancia = 0  # Duración

    # Fecha
    fecha = ''

    # Medias, moda, mediana y rango
    # TIEMPOS
    contador_tiempo = 0
    # PH
    lista_tiempos_previos_ph = []
    tiempos_previos_ph = []
    contador_tiempos_previos_ph = []
    max_tiempos_ph = 0
    min_tiempos_ph = 0
    # AS
    lista_tiempos_previos = []
    tiempos_previos = []
    contador_tiempos_previos = []
    max_tiempos = 0
    min_tiempos = 0
    # TAMAÑOS
    contador_longitud = 0
    #
    lista_longitudes_previas = []
    longitudes_previas = []
    contador_longitudes_previas = []
    max_longitudes = 0
    min_longitudes = 0

    n_mensajes_medio_subhilo = 0
    longitud_media = 0.0  # Tamaño
    distancia_media = 0.0  # Duración

    # Texto
    textos_mensajes = ''
    titulos_mensajes = ''

    # Cuantitativos
    # Cualitativos
    mensaje_mas_respondido_del_hilo = "¿CUÁL SERÁ?"
    autor_mas_respondedor_del_hilo = "¿CUÁL SERÁ?"

    # PARA CADA MENSAJE #
    for index, mensaje in enumerate(mensajes):

        # X FORO
        if mensaje['Foro'] != foro_previo:
            n_foros += 1
            foro_previo = mensaje['Foro']

        # X MENSAJE
        id_hilo = mensaje[campo]
        respuesta = mensaje['Respuesta']
        auto_respuesta = mensaje['Auto-respuesta']
        autor = mensaje['Remitente']
        # ETIQUETA ULTIMO MENSAJE DEL HILO
        terminal = mensaje['Terminal']

        # Nº MENSAJES #
        n_mensajes += 1

        # AUTORES DISTINTOS #
        if autor not in autores_previos:
            autores_previos.append(autor)
            n_autores += 1

        # AUTO-RESPUESTAS DEL HILO DE MENSAJES
        if auto_respuesta != 0:
            n_auto_respuestas += 1

        # MENSAJES MISMO HILO (ACTUALIZAR) #
        ####################################
        if id_hilo == id_hilo_anterior:

            # ESTADISTICAS (ACTUALIZAR) #
            # Media, Moda, Mediana y Rango
            #
            # TIEMPO
            # PH
            el_tiempo_ph = mensaje['Distancia PH']
            lista_tiempos_previos_ph.append(el_tiempo_ph)
            # SI TIEMPOS DISTINTOS #
            if el_tiempo_ph not in tiempos_previos_ph:
                # Array de valores
                tiempos_previos_ph.append(el_tiempo_ph)
                # Array de índices de tiempos
                contador_tiempos_previos_ph.insert(tiempos_previos_ph.index(el_tiempo_ph), 1)
            else:
                # Obtener ordinal del tiempo #
                contador_tiempo_ph = contador_tiempos_previos_ph[tiempos_previos_ph.index(el_tiempo_ph)]
                # Array de índices de tiempos
                contador_tiempos_previos_ph.insert(tiempos_previos_ph.index(el_tiempo_ph), contador_tiempo_ph + 1)

            # AS
            el_tiempo = mensaje['Distancia AS']
            lista_tiempos_previos.append(el_tiempo)
            # SI TIEMPOS DISTINTOS #
            if el_tiempo not in tiempos_previos:
                # Array de valores
                tiempos_previos.append(el_tiempo)
                # Array de índices de tiempos
                contador_tiempos_previos.insert(tiempos_previos.index(el_tiempo), 1)
            else:
                # Obtener ordinal del tiempo #
                contador_tiempo = contador_tiempos_previos[tiempos_previos.index(el_tiempo)]
                # Array de índices de tiempos
                contador_tiempos_previos.insert(tiempos_previos.index(el_tiempo), contador_tiempo + 1)

            # TAMAÑO
            la_longitud = mensaje['Caracteres texto mensaje']
            lista_longitudes_previas.append(la_longitud)
            # SI LONGITUDES DISTINTAS #
            if la_longitud not in longitudes_previas:
                # Array de valores
                longitudes_previas.append(la_longitud)
                # Array de índices de longitudes
                contador_longitudes_previas.insert(longitudes_previas.index(la_longitud), 1)
            else:
                # Obtener ordinal de la longitud #
                contador_longitud = contador_longitudes_previas[longitudes_previas.index(la_longitud)]
                # Array de índices de longitudes
                contador_longitudes_previas.insert(longitudes_previas.index(la_longitud), contador_longitud + 1)

            # LONGITUD #
            longitud += mensaje['Caracteres texto mensaje']

            # TEXTOS #
            titulos_mensajes += ' ' + mensaje['Título mensaje']
            textos_mensajes += ' ' + mensaje['Texto mensaje']

            # MENSAJES RESPUESTA #
            if respuesta != 0:
                # MENSAJE NUEVO SUBHILO
                if cambia_subhilo * respuesta < 0:
                    print(index, id_hilo, 'Nuevo SUBHILOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO', respuesta, n_subhilos)
                    cambia_subhilo = cambia_subhilo * -1
                    # Cuenta las Ramificaciones del hilo principal (-1,1)
                    if respuesta != 1 and respuesta != -1:
                        n_subhilos += 1
                    n_mensajes_medio_subhilo = 1
                # MENSAJE MISMO SUBHILO #
                else:
                    print(index, id_hilo, 'Mensaje de tipo respuesta') # ,'Mensaje de tipo respuesta del mismo subhilo', respuesta)
                    n_mensajes_medio_subhilo += 1
                    # ULTIMO MENSAJE DEL HILO Y del último SUBHILO del HILO
                    #########################
                    if terminal == -1:
                        print(index, id_hilo, 'Mensaje de tipo respuesta último del hilo')
            # MENSAJE NO RESPUESTA #
            else:
                n_hilos += 1

        # MENSAJE CABECERA HILO (INICIALIZAR) #
        # NUEVO HILO (INICIALIZAR) #
        ############################
        else:
            print(index, id_hilo, 'Nuevo HILOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO', respuesta)

            # CONTADOR HILOS
            n_hilos += 1

            # ID HILO
            id_hilo_anterior = id_hilo

            # INICIALIZAR CONTADORES #
            n_auto_respuestas = 0
            n_subhilos = 0
            longitud = mensaje['Caracteres texto mensaje']  # Tamaño texto
            distancia = 0  # Duración
            n_autores = 1

            titulos_mensajes = mensaje['Título mensaje']
            textos_mensajes = mensaje['Texto mensaje']

            fecha = mensaje['Fecha'] + ' ' + mensaje['Hora']

            # ESTADISTICAS (INICIALIZAR) #
            # Media, Moda, Mediana y Rango
            #
            # TIEMPO
            # PH
            el_tiempo_ph = mensaje['Distancia PH']
            # INICIALIZAR TIEMPOS #
            lista_tiempos_previos_ph = []
            tiempos_previos_ph = []
            contador_tiempos_previos_ph = []
            # Array de tiempos
            lista_tiempos_previos_ph.append(el_tiempo_ph)
            # Array de valores
            tiempos_previos_ph.append(el_tiempo_ph)
            # Array de índices de tiempos
            contador_tiempos_previos_ph.insert(tiempos_previos_ph.index(el_tiempo_ph), 1)

            # AS
            el_tiempo = mensaje['Distancia AS']
            # INICIALIZAR TIEMPOS #
            lista_tiempos_previos = []
            tiempos_previos = []
            contador_tiempos_previos = []
            # Array de tiempos
            lista_tiempos_previos.append(el_tiempo)
            # Array de valores
            tiempos_previos.append(el_tiempo)
            # Array de índices de tiempos
            contador_tiempos_previos.insert(tiempos_previos.index(el_tiempo), 1)

            # TAMAÑO
            la_longitud = mensaje['Caracteres texto mensaje']
            # INICIALIZAR LONGITUDES #
            lista_longitudes_previas = []
            longitudes_previas = []
            contador_longitudes_previas = []
            # Array longitudes
            lista_longitudes_previas.append(la_longitud)
            # Array de valores
            longitudes_previas.append(la_longitud)
            # Array de índices de longitudes
            contador_longitudes_previas.insert(longitudes_previas.index(la_longitud), 1)

        # ULTIMO MENSAJE DEL HILO (CERRAR y CALCULAR) #
        # (de un único mensaje o de múltiples mensajes) #
        #################################################
        if terminal == -1:

            # ESTADISTICAS (CERRAR y CALCULAR) #
            # Media, Moda, Mediana y Rango
            #
            import numpy as np

            # TIEMPO
            # PH
            # CALCULAR TIEMPOS #
            media_tiempos_ph = np.mean(lista_tiempos_previos_ph)
            mediana_tiempos_ph = np.median(lista_tiempos_previos_ph)
            # Excepción:
            try:
                # MODA
                print("MODA_T:", len(contador_tiempos_previos_ph), max(contador_tiempos_previos_ph))
                max_tiempos_ph = max(contador_tiempos_previos_ph)
                min_tiempos_ph = min(contador_tiempos_previos_ph)

                (_, idx, counts) = np.unique(lista_tiempos_previos_ph, return_index=True, return_counts=True)
                index = idx[np.argmax(counts)]
                moda_tiempos_ph = lista_tiempos_previos_ph[index]

                print("MODA_T:", moda_tiempos_ph)

            except NameError:
                print("well, it WASN'T defined after all! (MODA_T)")
                moda_tiempos_ph = 0
            else:
                print("sure, it was defined. (MODA_T)")
                moda_tiempos_ph = moda_tiempos_ph
            # Fin excepción
            rango_tiempos_ph = sorted(lista_tiempos_previos_ph)[len(lista_tiempos_previos_ph)-1] - sorted(lista_tiempos_previos_ph)[0]
            print("MediaTph: ", media_tiempos_ph)
            print("MedianaTph: ", mediana_tiempos_ph)
            print("ModaTph: ", moda_tiempos_ph)
            print("RangoTph: ", rango_tiempos_ph)

            # AS
            # CALCULAR TIEMPOS #
            media_tiempos = np.mean(lista_tiempos_previos)
            mediana_tiempos = np.median(lista_tiempos_previos)
            # Excepción:
            try:
                # MODA
                print("MODA_T:", len(contador_tiempos_previos), max(contador_tiempos_previos))
                max_tiempos = max(contador_tiempos_previos)
                min_tiempos = min(contador_tiempos_previos)

                (_, idx, counts) = np.unique(lista_tiempos_previos, return_index=True, return_counts=True)
                index = idx[np.argmax(counts)]
                moda_tiempos = lista_tiempos_previos[index]

                print("MODA_T:", moda_tiempos)

            except NameError:
                print("well, it WASN'T defined after all! (MODA_T)")
                moda_tiempos = 0
            else:
                print("sure, it was defined. (MODA_T)")
                moda_tiempos = moda_tiempos
            # Fin excepción
            rango_tiempos = sorted(lista_tiempos_previos)[len(lista_tiempos_previos)-1] - sorted(lista_tiempos_previos)[0]
            print("MediaT: ", media_tiempos)
            print("MedianaT: ", mediana_tiempos)
            print("ModaT: ", moda_tiempos)
            print("RangoT: ", rango_tiempos)

            # TAMAÑO
            la_longitud = mensaje['Caracteres texto mensaje']
            # INICIALIZAR LONGITUDES #
            media_longitudes = np.mean(lista_longitudes_previas)
            mediana_longitudes = np.median(lista_longitudes_previas)
            # Excepción:
            try:
                # MODA
                print("MODA_L:", len(contador_longitudes_previas), max(contador_longitudes_previas))
                max_longitudes = max(contador_longitudes_previas)
                min_longitudes = min(contador_longitudes_previas)

                (_, idx, counts) = np.unique(lista_longitudes_previas, return_index=True, return_counts=True)
                index = idx[np.argmax(counts)]
                moda_longitudes = lista_longitudes_previas[index]

                print("MODA_L:", moda_longitudes)

            except NameError:
                print("well, it WASN'T defined after all! (MODA_L)")
                moda_longitudes = 0
            else:
                print("sure, it was defined. (MODA_L)")
                moda_longitudes = moda_longitudes
            # Fin excepción
            rango_longitudes = sorted(lista_longitudes_previas)[len(lista_longitudes_previas)-1] - sorted(lista_longitudes_previas)[0]
            print("MediaL: ", media_longitudes)
            print("MedianaL: ", mediana_longitudes)
            print("ModaL: ", moda_longitudes)
            print("RangoL: ", rango_longitudes)

            # LONGITUD MEDIA #
            longitud_media = longitud / n_mensajes

            # DISTANCIA y DISTANCIA MEDIA #
            distancia = mensaje['Distancia PH']
            distancia_media = distancia / n_mensajes

            # MENSAJES x SUBHILO
            if n_subhilos != 0:
                n_mensajes_medio_subhilo = n_mensajes / n_subhilos
            else:
                n_mensajes_medio_subhilo = 0

            ########################
            # Derfinición de HILO
            ########################
            # hilo = [tit_hilo, id_hilo, dia_semana, fecha, n_mensajes, n_autores, n_subhilos, n_auto_respuestas, longitud, distancia, longitud_media, distancia_media]
            hilo = {
                # BASE #
                # MENSAJES #
                'Asignatura': mensaje['Asignatura'],
                'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
                'Caracteres foro': mensaje['Caracteres foro'],
                'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'], 'Caracteres hilo': mensaje['Caracteres hilo'],
                'Nº autores': n_autores,
                'Nº foro': n_foros,
                'Nº hilo': n_hilos,
                'Nº mensajes': n_mensajes,
                'Nº auto-respuestas': n_auto_respuestas,
                'Nº subhilos': n_subhilos,
                # MENSAJES x SUBHILO
                'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
                #    'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                #    'Remitente': id_autor, 'Autor': autor,
                # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                #    'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
                # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                'Date': fecha,
                # DISTANCIA y DISTANCIA MEDIA #
                'Distancia': distancia,
                'Distancia / Mensajes': distancia_media,
                #    'Distancia PH': date_ph
                'Distancia MaxTph': max_tiempos_ph,
                'Distancia MinTph': min_tiempos_ph,
                'MediaTph': media_tiempos_ph,
                'MedianaTph': mediana_tiempos_ph,
                'ModaTph': moda_tiempos_ph,
                'RangoTph': rango_tiempos_ph,
                #    'Distancia AS': date_as,
                'Distancia MaxTas': max_tiempos,
                'Distancia MinTs': min_tiempos,
                'MediaTas': media_tiempos,
                'MedianaTas': mediana_tiempos,
                'ModaTas': moda_tiempos,
                'RangoTas': rango_tiempos,
                # DIFERENCIAS TAMAÑO Padre-Hijo Antecesor-Sucesor
                'Longitud': longitud,
                'Longitud media': longitud_media,
                'Longitud Max': max_longitudes,
                'Longitud Min': min_longitudes,
                'MediaL': media_longitudes,
                'MedianaL': mediana_longitudes,
                'ModaL': moda_longitudes,
                'RangoL': rango_longitudes,
                'Títulos mensajes': titulos_mensajes, 'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los títulos
                'Textos mensajes': textos_mensajes.strip(), 'Caracteres textos mensajes': len(textos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los textos
                # ANÁLISIS de TEXTO
                # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                #    'Tokens': var_token,
                # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras}
                #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'),
                #    'ns': var_token.get('ns'),
                # .SnowballStemmer("spanish").stem,
                #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas}
                #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                #    'Postag': var_pos,
                # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                #    'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                #    'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                'Curso': curso,
            }

            # INICIALIZAR AUTORES #
            autores_previos = []
            # INICIALIZAR CONTADORES HILO #
            longitud = 0
            n_mensajes = 0
            distancia = 0

            # AÑADIR HILO #
            hilos.append(hilo)

    # print(hilos)
    return hilos


## ARBOLES ##
def generar_arbol_default(lista, etiqueta, campo):
    from anytree import Node, RenderTree, AsciiStyle

    # NODO RAIZ #
    raiz = Node(etiqueta)
    nodo_anterior = raiz

    # Valor inicial de la RAIZ
    valor = 0
    valor_anterior = valor
    valores_previos = []
    nodos_previos = []

    # PARA CADA NODO HOJA #
    for index, elemento in enumerate(lista):
        valor = elemento.get(campo)

        if valor != 0 or valor != '':
            if valor != valor_anterior:
                # NODOS DISTINTOS #
                if valor not in valores_previos:
                    nodo = Node(valor, parent=nodo_anterior)
                    valores_previos.append(valor)
                    # Array de nosos
                    nodos_previos.insert(valores_previos.index(valor), nodo)

                else:
                    # Obtener ordinal del nodo #
                    nodo = Node(valor, parent=nodos_previos[valores_previos.index(valor)])

        else:
            nodo = Node(valor, parent=raiz)

        # print(nodo_anterior)
        valor_anterior = valor
        nodo_anterior = nodo

    # Preview
    for pre, fill, node in RenderTree(raiz, style=AsciiStyle()):
        print("%s%s" % (pre, node.name))

    # Export PNG (Graphviz)
    from anytree.exporter import DotExporter
    # graphviz needs to be installed for the next line!
    #DotExporter(arbol).to_picture("arbol.png")

    return raiz


def generar_arbol(lista, etiqueta, campo, valor_raiz):
    from anytree import Node, RenderTree, AsciiStyle

    # NODO RAIZ #
    raiz = Node(etiqueta)
    nodo_anterior = raiz

    # Valor inicial de la RAIZ
    valor = 0
    valor_anterior = valor
    valores_previos = []
    nodos_previos = []

    # PARA CADA NODO HOJA #
    for index, elemento in enumerate(lista):
        valor = elemento.get(campo)
        valor_etiqueta = elemento.get(etiqueta)
        # Nodo NO Raíz
        if valor != valor_raiz:
            # Nodos no anidados
            if valor != valor_anterior:
                # NODOS DISTINTOS #
                if valor not in valores_previos:
                    nodo = Node(valor_etiqueta, parent=nodo_anterior)
                    # Array de valores
                    valores_previos.append(valor_etiqueta)
                    # Array de nodos objetos
                    nodos_previos.insert(valores_previos.index(valor_etiqueta), nodo)

                else:
                    # Obtener ordinal del nodo #
                    nodo = Node(valor_etiqueta, parent=nodos_previos[valores_previos.index(valor_etiqueta)])
            else:
                nodo = Node(valor_etiqueta, parent=nodo_anterior)
        else:
            nodo = Node(valor_etiqueta, parent=raiz)

        # NODO PREVIO
        # print(nodo_anterior)
        valor_anterior = valor
        nodo_anterior = nodo

    # Preview
    for pre, fill, node in RenderTree(raiz, style=AsciiStyle()):
        print("%s%s" % (pre, node.name))

    # Export PNG (Graphviz)
    from anytree.exporter import DotExporter
    # graphviz needs to be installed for the next line!
    DotExporter(raiz).to_dotfile("tree.dot")
    # ERROR: FileNotFoundError: [WinError 2] El sistema no puede encontrar el archivo especificado
    # DotExporter(raiz).to_picture("tree.png")

    return raiz


## PROCESADO USUARIOS ##
def generar_autores(mensajes, hilos, campo, curso_asig):
    global usuarios

    print('#######')
    print('AUTORES')
    print('#######')
    usuarios = []
    curso = curso_asig
    #

    # Excepción:
    # Si la variable 'id_autor_anterior' no exite, la inicializa
    # Si la variable 'cambia_autor' no exite, la inicializa (vale 1: si es el mismo autor, vale -1: si cambia el autor)
    try:
        # ID de autor
        id_autor_anterior
        # interruptor de cambio de autor #
        cambia_autor = 1
    except NameError:
        print("well, it WASN'T defined after all!")
        id_autor_anterior = 0
        cambia_autor = 1
    else:
        print("sure, it was defined.")
        id_autoranterior = 0
        cambia_autor = 1
    # Fin excepción

    # Variables Globales
    autores_previos = []
    hilos_previos = []
    autor_previo = 0
    foro_previo = 0
    hilo_previo = 0

    # Totales
    n_mensajes = 0
    n_autores = 0
    n_hilos = 0
    n_foros = 0
    n_subhilos = 0
    # INICIADOR, RESPONDEDOR Y TERMINADOR
    n_iniciales = 0
    n_respuestas = 0
    n_auto_respuestas = 0
    n_terminales = 0
    # TIEMPO/DISTANCIA
    longitud = 0  # Tamaño texto

    distancia = 0  # Duración
    date = 0
    date_diff = 0
    date_ph = 0
    date_as = 0
    date_antecesor = 0

    # Fecha
    fecha = ''

    # Medias, moda, mediana y rango
    # TIEMPO/DISTANCIA
    distancia_media = 0.0  # Duración
    distancia_media_ph = 0.0
    media_tiempos_ph = 0.0
    mediana_tiempos_ph = 0.0
    moda_tiempos_ph = 0.0
    rango_tiempos_ph = 0.0
    distancia_media_as = 0.0
    media_tiempos_as = 0.0
    mediana_tiempos_as = 0.0
    moda_tiempos_as = 0.0
    rango_tiempos_as = 0.0
    contador_tiempo = 0
    # DIFF
    lista_tiempos_previos = []
    tiempos_previos = []
    contador_tiempos_previos = []
    max_tiempos = 0
    min_tiempos = 0
    # PH
    lista_tiempos_previos_ph = []
    tiempos_previos_ph = []
    contador_tiempos_previos_ph = []
    max_tiempos_ph = 0
    min_tiempos_ph = 0
    # AS
    lista_tiempos_previos_as = []
    tiempos_previos_as = []
    contador_tiempos_previos_as = []
    max_tiempos_as = 0
    min_tiempos_as = 0

    # TAMAÑO/LONGITUD
    longitud_media = 0.0  # Tamaño
    contador_longitud = 0
    #
    lista_longitudes_previas = []
    longitudes_previas = []
    contador_longitudes_previas = []
    max_longitudes = 0
    min_longitudes = 0

    n_mensajes_medio_subhilo = 0

    # Texto
    textos_mensajes = ''
    titulos_mensajes = ''

    # Cuantitativos
    # Cualitativos
    mensaje_mas_respondido_del_hilo = "¿CUÁL SERÁ?"
    autor_mas_respondedor_del_hilo = "¿CUÁL SERÁ?"

    # Orena por Autores
    lista_mensajes = sorted(mensajes, key=lambda objeto: objeto['Remitente'])

    ############################
    # Ordena por Autores y Fecha (para crear la lista de autores por mensaje escrito)
    ############################
    lista_mensajes_fecha = sorted(lista_mensajes, key=lambda o: (o['Remitente'], o['Distancia OO']))

    # PARA CADA MENSAJE #
    for index, mensaje in enumerate(lista_mensajes_fecha):

        # FECHA (Date)
        date = mensaje['Fecha'] + ' ' + mensaje['Hora']

        # X MENSAJE
        n_mensajes += 1
        # INICIADOR, RESPONDEDOR Y TERMINADOR
        # ETIQUETA PRIMER MENSAJE DE HILO
        inicial = mensaje['Inicial']
        if inicial == 1:
            n_iniciales += 1
        # ETIQUETA MENSAJE INTERMEDIO DE HILO
        respuesta = mensaje['Respuesta']
        if respuesta == 1 or respuesta == -1:
            n_respuestas += 1
        auto_respuesta = mensaje['Auto-respuesta']
        if auto_respuesta == 1:
            n_auto_respuestas += 1
        # ETIQUETA ULTIMO MENSAJE DE HILO
        terminal = mensaje['Terminal']
        if terminal == -1:
            n_terminales += 1
        #
        # DISTANCIAS  datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")
        from datetime import datetime

        date_origen = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")  # date = fecha + ' ' + hora

        # MENSAJE INICIAL O PRIMER AUTOR
        if date_antecesor == 0 or inicial == 1:

            # Antecesor-Sucesor en segundos
            date_diff = abs(date_origen - date_origen).total_seconds()  # Valor 0

            date_antecesor = date_origen  # fecha + ' ' + hora

        # SEGUNDO O POSTERIOR MENSAJE AUTOR
        else:

            # Antecesor-Sucesor en segundos
            date_diff = abs(date_origen - date_antecesor).total_seconds()  # (fecha + ' ' + hora) - date_antecesor

            date_antecesor = date_origen  # fecha + ' ' + hora
        #
        # DISTANCIA #
        distancia += date_diff
        # DISTANCIA AL ORIGEN #
        # Permite ordenar por fecha de forma directa #
        date_origen = abs(
            datetime.strptime(date, "%d/%m/%Y %H:%M:%S") - datetime.strptime('01/01/2017 00:00:00',
                                                                                           "%d/%m/%Y %H:%M:%S")).total_seconds()

        # print('LISTAS ', lista_tiempos_previos, lista_tiempos_previos_ph, lista_tiempos_previos_as)
        #
        # TIEMPO #
        if date_diff != 0:
            # DIFF
            el_tiempo = date_diff
            # Array de tiempos
            lista_tiempos_previos.append(el_tiempo)
            # Array de valores
            tiempos_previos.append(el_tiempo)
            # Array de índices de tiempos
            contador_tiempos_previos.insert(tiempos_previos.index(el_tiempo), 1)
        if mensaje['Distancia PH'] != 0:
            # PH
            el_tiempo_ph = mensaje['Distancia PH']
            # Array de tiempos
            lista_tiempos_previos_ph.append(el_tiempo_ph)
            # Array de valores
            tiempos_previos_ph.append(el_tiempo_ph)
            # Array de índices de tiempos
            contador_tiempos_previos_ph.insert(tiempos_previos_ph.index(el_tiempo_ph), 1)
        if mensaje['Distancia AS'] != 0:
            # AS
            el_tiempo = mensaje['Distancia AS']
            # Array de tiempos
            lista_tiempos_previos_as.append(el_tiempo)
            # Array de valores
            tiempos_previos_as.append(el_tiempo)
            # Array de índices de tiempos
            contador_tiempos_previos_as.insert(tiempos_previos_as.index(el_tiempo), 1)
        #
        # LONGITUD #
        longitud += mensaje['Caracteres texto mensaje']
        if mensaje['Caracteres texto mensaje'] != 0:
            # TAMAÑO
            la_longitud = mensaje['Caracteres texto mensaje']
            # Array longitudes
            lista_longitudes_previas.append(la_longitud)
            # Array de valores
            longitudes_previas.append(la_longitud)
            # Array de índices de longitudes
            contador_longitudes_previas.insert(longitudes_previas.index(la_longitud), 1)
        #
        # TEXTOS #
        titulos_mensajes += ' ' + mensaje['Título mensaje']
        textos_mensajes += ' ' + mensaje['Texto mensaje']

        # X HILO
        hilo = mensaje['Hilo']
        # HILOS DISTINTOS #
        if hilo not in hilos_previos:
            hilos_previos.append(hilo)
            n_hilos += 1
        if hilo != hilo_previo:
            hilo_previo = hilo

        # X FORO
        if mensaje['Foro'] != foro_previo:
            n_foros += 1
            foro_previo = mensaje['Foro']

        # X AUTOR
        id_autor = mensaje[campo]
        if id_autor != autor_previo:

            # SI PRIMER MENSAJE Y PRIMER AUTOR
            if autor_previo == 0:
                autor_previo = id_autor
            # SI ULTIMO MENSAJE AUTOR PREVIO
            else:
                # DISTANCIAS
                #
                date_antecesor = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")  # date = fecha + ' ' + hora
                # DISTANCIA MEDIA MAX MIN #
                if lista_tiempos_previos != []:
                    # DIFF
                    distancia_media = distancia / n_mensajes - 1
                    max_tiempos = max(lista_tiempos_previos)
                    min_tiempos = min(lista_tiempos_previos)

                # ESTADISTICAS (CERRAR y CALCULAR) #
                # Media, Moda, Mediana y Rango
                #
                import numpy as np

                # TIEMPO
                # PH
                # CALCULAR TIEMPOS #
                if lista_tiempos_previos_ph != []:
                    # PH
                    media_tiempos_ph = np.mean(lista_tiempos_previos_ph)
                    mediana_tiempos_ph = np.median(lista_tiempos_previos_ph)
                    max_tiempos_ph = max(lista_tiempos_previos_ph)
                    min_tiempos_ph = min(lista_tiempos_previos_ph)
                    (_, idx, counts) = np.unique(lista_tiempos_previos_ph, return_index=True, return_counts=True)
                    index = idx[np.argmax(counts)]
                    moda_tiempos_ph = lista_tiempos_previos_ph[index]
                    rango_tiempos_ph = sorted(lista_tiempos_previos_ph)[len(lista_tiempos_previos_ph)-1] - sorted(lista_tiempos_previos_ph)[0]
                if lista_tiempos_previos_as != []:
                    # AS
                    media_tiempos_as = np.mean(lista_tiempos_previos_as)
                    mediana_tiempos_as = np.median(lista_tiempos_previos_as)
                    max_tiempos_as = max(lista_tiempos_previos_as)
                    min_tiempos_as = min(lista_tiempos_previos_as)
                    (_, idx, counts) = np.unique(lista_tiempos_previos_as, return_index=True, return_counts=True)
                    index = idx[np.argmax(counts)]
                    moda_tiempos_as = lista_tiempos_previos_as[index]
                    rango_tiempos_as = sorted(lista_tiempos_previos_as)[len(lista_tiempos_previos_as)-1] - sorted(lista_tiempos_previos_as)[0]

                # LONGITUD MEDIA MAX MIN #
                longitud_media = longitud / n_mensajes
                if longitudes_previas != []:
                    max_longitudes = max(longitudes_previas)
                    min_longitudes = min(longitudes_previas)

            ########################
            # Derfinición de AUTOR
            ########################
            # autor = [tit_hilo, id_hilo, dia_semana, fecha, n_mensajes, n_autores, n_subhilos, n_auto_respuestas, longitud, distancia, longitud_media, distancia_media]
            autor = {
                # BASE #
                # MENSAJES #
                'Asignatura': mensaje['Asignatura'],
                # 'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
                # 'Caracteres foro': mensaje['Caracteres foro'],
                # 'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'], 'Caracteres hilo': mensaje['Caracteres hilo'],
                'Nº autores': n_autores,
                'Nº foros': n_foros,
                'Nº hilos': n_hilos,
                'Nº mensajes': n_mensajes,
                #'Nº auto-respuestas': n_auto_respuestas,
                #'Nº subhilos': n_subhilos,
                # MENSAJES x SUBHILO
                #'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
                #'Mensaje': mensaje['Mensaje'], 'Responde a': mensaje['Responde a'],
                'Remitente': id_autor, 'Autor': autor_previo,
                # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                'Iniciales': n_iniciales, 'Respuestas': n_respuestas,
                'Auto-respuestas': n_auto_respuestas, 'Terminales': n_terminales,
                # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                'Date': date,
                # DISTANCIA y DISTANCIA MEDIA #
                'Distancia': distancia,
                'Distancia / Mensajes': distancia_media,
                'Distancia Max': max_tiempos,
                'Distancia Min': min_tiempos,
                #    'Distancia PH': date_ph
                'Distancia MaxTph': max_tiempos_ph,
                'Distancia MinTph': min_tiempos_ph,
                'MediaTph': media_tiempos_ph,
                'MedianaTph': mediana_tiempos_ph,
                'ModaTph': moda_tiempos_ph,
                'RangoTph': rango_tiempos_ph,
                #    'Distancia AS': date_as,
                'Distancia MaxTas': max_tiempos_as,
                'Distancia MinTs': min_tiempos_as,
                'MediaTas': media_tiempos_as,
                'MedianaTas': mediana_tiempos_as,
                'ModaTas': moda_tiempos_as,
                'RangoTas': rango_tiempos_as,
                # DIFERENCIAS TAMAÑO Padre-Hijo Antecesor-Sucesor
                'Longitud': longitud,
                'Longitud media': longitud_media,
                'Longitud Max': max_longitudes,
                'Longitud Min': min_longitudes,
                #'MediaL': media_longitudes,
                #'MedianaL': mediana_longitudes,
                #'ModaL': moda_longitudes,
                #'RangoL': rango_longitudes,
                'Títulos mensajes': titulos_mensajes, 'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los títulos
                'Textos mensajes': textos_mensajes.strip(), 'Caracteres textos mensajes': len(textos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los textos
                # ANÁLISIS de TEXTO
                # ANÁLISIS de TEXTO
                # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                #    'Tokens': var_token,
                # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras}
                #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'),
                #    'ns': var_token.get('ns'),
                # .SnowballStemmer("spanish").stem,
                #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas}
                #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                #    'Postag': var_pos,
                # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                #    'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                #    'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                'Curso': curso,
            }

            # PRIMER MENSAJE AUTOR #
            # INICIALIZAR MENSAJES #
            n_mensajes = 0
            # INICIALIZAR AUTORES #
            autores_previos = []
            n_autores += 1
            autor_previo = id_autor
            # INICIALIZAR HILOS #
            hilos_previos = []

            # INICIALIZAR CONTADORES AUTOR #
            n_mensajes = 1
            n_foros = 1
            n_hilos = 1

            # INICIADOR, RESPONDEDOR Y TERMINADOR
            n_iniciales = 0
            n_respuestas = 0
            n_auto_respuestas = 0
            n_terminales = 0

            # DISTANCIAS/TIEMPOS
            longitud = 0
            distancia = 0
            max_tiempos = 0
            min_tiempos = 0
            # INICIALIZAR TIEMPOS DIFF #
            lista_tiempos_previos = []
            tiempos_previos = []
            contador_tiempos_previos = []
            # INICIALIZAR TIEMPOS PH #
            lista_tiempos_previos_ph = []
            tiempos_previos_ph = []
            contador_tiempos_previos_ph = []
            # INICIALIZAR TIEMPOS AS #
            lista_tiempos_previos_as = []
            tiempos_previos_as = []
            contador_tiempos_previos_as = []

            # TAMAÑO/LONGITUD
            contador_longitud = 0
            #
            lista_longitudes_previas = []
            longitudes_previas = []
            contador_longitudes_previas = []
            max_longitudes = 0
            min_longitudes = 0

            n_mensajes_medio_subhilo = 0
            longitud_media = 0.0  # Tamaño
            distancia_media = 0.0  # Duración
            distancia_media_ph = 0.0  # Duración
            distancia_media_as = 0.0  # Duración
            #
            # TIEMPO #
            if date_diff != 0:
                # DIFF
                el_tiempo = date_diff
                # INICIALIZAR TIEMPOS #
                lista_tiempos_previos = []
                tiempos_previos = []
                contador_tiempos_previos = []
                # Array de tiempos
                lista_tiempos_previos.append(el_tiempo)
                # Array de valores
                tiempos_previos.append(el_tiempo)
                # Array de índices de tiempos
                contador_tiempos_previos.insert(tiempos_previos.index(el_tiempo), 1)
            if mensaje['Distancia PH'] != 0:
                # PH
                el_tiempo_ph = mensaje['Distancia PH']
                # INICIALIZAR TIEMPOS #
                lista_tiempos_previos_ph = []
                tiempos_previos_ph = []
                contador_tiempos_previos_ph = []
                # Array de tiempos
                lista_tiempos_previos_ph.append(el_tiempo_ph)
                # Array de valores
                tiempos_previos_ph.append(el_tiempo_ph)
                # Array de índices de tiempos
                contador_tiempos_previos_ph.insert(tiempos_previos_ph.index(el_tiempo_ph), 1)
            if mensaje['Distancia AS'] != 0:
                # AS
                el_tiempo = mensaje['Distancia AS']
                # INICIALIZAR TIEMPOS #
                lista_tiempos_previos_as = []
                tiempos_previos_as = []
                contador_tiempos_previos_as = []
                # Array de tiempos
                lista_tiempos_previos_as.append(el_tiempo)
                # Array de valores
                tiempos_previos_as.append(el_tiempo)
                # Array de índices de tiempos
                contador_tiempos_previos_as.insert(tiempos_previos_as.index(el_tiempo), 1)
                #
                # LONGITUD #
                longitud += mensaje['Caracteres texto mensaje']
            if mensaje['Caracteres texto mensaje'] != 0:
                # TAMAÑO
                la_longitud = mensaje['Caracteres texto mensaje']
                # INICIALIZAR LONGITUDES #
                lista_longitudes_previas = []
                longitudes_previas = []
                contador_longitudes_previas = []
                # Array longitudes
                lista_longitudes_previas.append(la_longitud)
                # Array de valores
                longitudes_previas.append(la_longitud)
                # Array de índices de longitudes
                contador_longitudes_previas.insert(longitudes_previas.index(la_longitud), 1)

            # TEXTOS
            titulos_mensajes = mensaje['Título mensaje']
            textos_mensajes = mensaje['Texto mensaje']

            # AÑADIR AUTOR #
            usuarios.append(autor)

    return usuarios

    #import operator
    #lista_mensajes_fecha = sorted(lista_mensajes, key=operator.itemgetter('Remitente', 'Fecha'))

    #lista_mensajes_fecha = sorted(lista_mensajes, key=lambda objeto: (objeto['Remitente'], objeto['Fecha']))

    #lista_mensajes_fecha = sorted([(e['Remitente'], e['Date'], e) for e in mensajes], reverse=True)

    # sort edges: primary key=length, secondary key=start index.
    # (and filter out the token edges)
    #edges = sorted([(e.length(), e.start(), e) for e in self])
    #edges = [e for (_, _, e) in edges]

    for i in range(0, 20, 1):
        print(lista_mensajes[i]['Remitente'], lista_mensajes[i]['Date'], lista_mensajes[i])

    print('------------------')

    for i in range(0, 20, 1):
        print(lista_mensajes_fecha[i]['Remitente'], lista_mensajes_fecha[i]['Date'], lista_mensajes_fecha[i])

    from anytree import Node, RenderTree

    udo = Node("Raíz")
    lui = Node("Lui", parent=udo)
    marc = Node("Marc", parent=udo)
    print(udo)
    lian = Node("Lian", parent=marc)
    dan = Node("Dan", parent=udo)
    joe = Node("Joe", parent=dan)
    print(joe)
    for pre, fill, node in RenderTree(udo):
        print("%s%s" % (pre, node.name))

    from anytree.dotexport import RenderTreeGraph
    from anytree.exporter import DotExporter
    # graphviz needs to be installed for the next line!
    RenderTreeGraph(udo).to_dotfile("udo.dot")
    #DotExporter(udo).to_picture("udo.png")

    return usuarios


## PROCESADO FOROS ##
def generar_foros(mensajes, hilos, autores, campo, curso_asig):
    global foros

    print('#######')
    print('FOROS')
    print('#######')
    foros = []
    curso = curso_asig
    #

    # Variables Globales
    # Interruptores
    foro_previo = 0

    # Totales
    n_foros = 0

    # PARA CADA MENSAJE #
    for index, mensaje in enumerate(mensajes):
        if mensaje['Foro'] != foro_previo:
            n_foros += 1
            foro_previo = mensaje['Foro']

    return foros


## PROCESADO ASIGNATURAS ##
def generar_asignaturas(mensajes, hilos, autores, foros, campo, curso_asig):
    global asignaturas

    print('#######')
    print('ASIGNATURAS')
    print('#######')
    asignaturas = []
    curso = curso_asig
    #

    return asignaturas
