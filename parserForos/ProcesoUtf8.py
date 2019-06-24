""""
Created on 09-01-2019

@author: Aitor Diaz Medina

Clase principal encargada llamar al parser y generar el archivo csv resultante

"""

import hashlib

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


## PROCESADO MENSAJES ##
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
                id_foro = int(hashlib.sha1(nombre_foro.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensajes de la conversación: '):
                tit_hilo = linea.partition('Mensajes de la conversación: ')[2]
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
                ## Autor
                ## id = HASH(''Nombres Apellidos)
                autor = linea.partition('Enviado por: ')[2].partition(" el")[0]
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


def generar_mensajes_ampliado(ruta, id_asig):
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
        # n_c_
        # n_
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

        hilo = 1

        # Atributos Textuales

        for index, linea in enumerate(lineas):

            if linea.startswith('Foro: '):
                print(linea.partition('Foro: ')[2])
                nombre_foro = linea.partition('Foro: ')[2]
                id_foro = int(hashlib.sha1(nombre_foro.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensajes de la conversación: '):
                tit_hilo = linea.partition('Mensajes de la conversación: ')[2]
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
                ## Autor
                ## id = HASH(''Nombres Apellidos)
                autor = linea.partition('Enviado por: ')[2].partition(" el")[0]
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

                    #######################
                    # Tratamiento AMPLIADO
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
                    print('EMOJIS:', n_emojis)

                    # Cuenta LINKS
                    n_links = 0

                    # Busca ADJUNTOS Y EMOJIS
                    if texto.find('[IMAGE:'):
                        print('ADJUNTOS ENCONTRADOS: ', n_adjs)
                        # Busca [IMAGE:
                        regex = re.search(r'(\[IMAGE: .*\])', texto, re.M | re.I)
                        if regex != None:
                            # Replace all [IMAGE:
                            texto = re.sub(r'(\[IMAGE: .*\])', '[DATA: .XXX]', texto)
                            print(regex.group(1))
                            print(texto)
                            # exit(12345567890)

                    # Busca LINKS (eliminados ADJUNTOS y EMOJIS)
                    if texto.find('http'):
                        n_links = len(re.findall(r'(http)', texto, re.M | re.I))
                        print('LINKS ENCONTRADOS: ', n_links)

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
                        date_ph = abs(date_padre - date_padre)
                        # Antecesor-Sucesor en segundos
                        date_as = abs(date_padre - date_padre).total_seconds()

                        date_antecesor = datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")  # fecha + ' ' + hora

                    # RESPUESTAS
                    else:

                        # Padre-Hijo en días
                        date_ph = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - date_padre)  # (fecha + ' ' + hora) - date_padre

                        # Antecesor-Sucesor en segundos
                        date_as = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - date_antecesor).total_seconds()  # (fecha + ' ' + hora) - date_antecesor

                        date_antecesor = datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")  # fecha + ' ' + hora

                        # 1er Mensaje
                        if len(mensajes) == 0:
                            print(date_ph, date_as)

                    #
                    # TIPOS MENSAJE (INICIAL, RESPUESTA o TERMINAL)
                    #

                    # Tipos x posición
                    # INICIAL
                    if id_ref_mensaje == '':

                        # Define PADRE HILO
                        # controla si son auto-respuestas o participantes distintos
                        try:
                            padre_hilo = padre_hilo
                            padre_hilo = id_autor
                        except NameError:
                            padre_hilo = id_autor

                        inicial = 0
                        respuesta = 0  # 'inicial'
                        auto_respuesta = 0  # 'no'
                        terminal = 0  # 'sinrespuesta'

                        # Redefine TERMINAL
                        # si un menssaje es Inicial
                        # revisa los anteriores (-1,-2,-3,-4,...)
                        # anotándoles como Terminal
                        try:
                            n_mensajes_hilo = n_mensajes_hilo
                        except NameError:
                            n_mensajes_hilo = 0

                        for i in range(0, n_mensajes_hilo, 1):
                            # Mensaje único del hilo
                            # 0 'sinrespuesta'
                            mensajes[len(mensajes) - (i+1)]['Terminal'] = -i

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

                        # Mensaje RESPUESTA del Hilo
                        n_mensajes_hilo = n_mensajes_hilo + 1

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
                        'Distancia PH': date_ph, 'Distancia AS': date_as,
                        # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                        'Título mensaje': tit_mensaje, 'Caracteres título mensaje': len(tit_mensaje),
                        'Diferncia PH': size_ph, 'Diferencia AS': size_as,
                        # ANALISIS de TEXTO
                        'Texto mensaje': texto.strip(), 'Caracteres texto mensaje': len(texto),
                        'Frases':  'nltk.tokenize.sent_tokenize',
                        'Palabras': 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                        'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links
                    }
                    mensajes.append(mensaje)
                    ## Limpia variables
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
                    mensaje = {'Foro': id_foro, 'Nombre foro': nombre_foro, 'Asignatura': id_asig, 'Título': tit_hilo,
                               'Hilo': id_hilo,
                               'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                               'Remitente': id_autor, 'Autor': autor, 'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                               'Date': fecha + ' ' + hora,
                               'Título mensaje': tit_mensaje,
                               'Texto mensaje': texto.strip(), 'Caracteres texto mensaje': len(texto)}
                    mensajes.append(mensaje)
                    texto = ""
                    autor = ""
                    # print(linea)

            if lineas[index - 1].startswith('Título: '):
                estado = 'MENSAJE'

            if estado == 'MENSAJE':
                texto = texto + ' ' + linea

    return mensajes


## PROCESADO HILOS ##
def generar_hilos(ruta, id_asig):
    hilos = []
    return hilos


## PROCESADO USUARIOS ##
def generar_usuarios(ruta, id_asig):
    usuarios = []
    return usuarios
# FIN Añadido FJSB

