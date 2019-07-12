""""
Created on 09-01-2019

@author: Aitor Diaz Medina

Clase principal encargada llamar al parser y generar el archivo csv resultante

"""

import hashlib

# VARIABLES GLOBALES #
# mensajes = []
hilos = []
usuarios = []
asignaturas = []

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


def generar_mensajes_ampliado(ruta, id_asig):
    global mensajes

    print('#######')
    print('MENSAJES')
    print('#######')
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
            # ULTIMO MENSAJE DE CADA HILO: CIERRE DE HILO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            elif linea.startswith('----------------------------------------------------------------------') or \
                    linea.startswith('==============================================================================='):
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
                    print('EMOJIS:', n_emojis)

                    # Cuenta LINKS
                    n_links = 0
                    n_links_r = 0

                    # Busca ADJUNTOS Y EMOJIS
                    if texto.find('[IMAGE:'):
                        print('ADJUNTOS ENCONTRADOS: ', n_adjs)
                        # Busca [IMAGE:
                        regex = re.search(r'(\[IMAGE: .*\])', texto, re.M | re.I)
                        if regex != None:
                            # Reemplaza todos los ADJUNTOS Y EMOJIS [IMAGE: por [DATA:XXX]
                            texto = re.sub(r'(\[IMAGE: .*\])', '[DATA]', texto)
                            print(regex.group(1))
                            print(texto)
                            # exit(12345567890)

                    # Busca LINKS (eliminados ADJUNTOS y EMOJIS)
                    if texto.find('http'):
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
                        date_ph = abs(date_padre - date_padre).total_seconds()
                        # Antecesor-Sucesor en segundos
                        date_as = abs(date_padre - date_padre).total_seconds()

                        date_antecesor = datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")  # fecha + ' ' + hora

                    # RESPUESTAS
                    else:

                        # Padre-Hijo en días
                        date_ph = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - date_padre).total_seconds()  # (fecha + ' ' + hora) - date_padre

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

                    #
                    # ANÁLISIS de TEXTO
                    #
                    from procesadoGeneral import tokenizado
                    from procesadoGeneral import enraizado
                    from procesadoGeneral import postag

                    var_token = tokenizado(texto.strip())
                    print('TOKENIZADO(', n_mensajes_hilo, '): ', var_token)

                    var_raiz = enraizado()
                    print('RAICES: ', var_raiz)

                    # var_pos = postag(texto.strip())
                    # print('PoStag: ', var_pos)

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
                        'Distancia PH': date_ph, 'Distancia AS': date_as,
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
                        'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links
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


## REPARTO x CAMPOS ##
def partir_x_campo(lista, campo):
    global mensajes
    global hilos
    global usuarios
    global asignaturas

    print('#######')
    print('CAMPO')
    print('#######')
    destino = []
    # Valor inicial del CAMPO de partición
    # y del campo anterior
    campo_anterior = lista[0].get(campo)
    #

    print(lista)
    jndex = 0
    for index, li in enumerate(lista):
        val = li.get(campo)
        print(val)
        if val != campo_anterior:  # NUEVA INSTANCIA x CAMPO: Hilo, Remitente o Autor, Asignatura
            campo_anterior = val
            jndex = jndex + 1
            print(index, jndex)
        destino.insert(jndex, li)

    print(destino[3])
    return destino


## REPARTO x CAMPOS ##
def repartir_x_campo(lista, campo):
    global mensajes
    global hilos
    global usuarios
    global asignaturas

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


## PROCESADO HILOS ##
def generar_hilos(mensajes, campo):
    global hilos

    print('#######')
    print('HILOS')
    print('#######')
    hilos = []
    # Valor inicial del CAMPO de partición
    # anterior = mensajes[0].get(campo)

    # Excepción:
    # Si la variable 'id_hilo_anterior' no exite la inicializa
    # Si la variable 'cambia_subhilo' no exite la inicializa (vale 1: si es el mismo subhilo, vale -1: si cambia el subhilo)
    try:
        id_hilo_anterior
        # interruptor de cambio de hilo #
        cambia_subhilo
    except NameError:
        print("well, it WASN'T defined after all!")
        id_hilo_anterior = mensajes[0].get(campo)
        cambia_subhilo = 1
    else:
        print("sure, it was defined.")
    #

    # Variables Globales
    autores_previos = []
    # Totales
    n_mensajes = 0
    n_autores = 0
    n_subhilos = 0
    n_auto_respuestas = 0
    longitud = 0  # Tamaño texto
    distancia = 0  # Duración
    longitud_media = 0.0  # Tamaño
    distancia_media = 0.0  # Duración

    # Medias
    n_mensajes_medio_subhilo = 0

    # Cuantitativos
    mensaje_mas_respondido_del_hilo = "¿CUÁL SERÁ?"
    autor_mas_respondedor_del_hilo = "¿CUÁL SERÁ?"

    # PARA CADA MENSAJE #
    for index, mensaje in enumerate(mensajes):
        id_hilo = mensaje[campo]
        respuesta = mensaje['Respuesta']
        auto_respuesta = mensaje['Auto-respuesta']
        autor = mensaje['Remitente']
        # ULTIMO MENSAJE DEL HILO
        terminal = mensaje['Terminal']
        # LONGITUD #
        longitud += mensaje['Caracteres texto mensaje']
        # Nº MENSAJES #
        n_mensajes += 1
        # AUTORES DISTINTOS #
        if autor not in autores_previos:
            autores_previos.append(autor)
            n_autores += 1
        # AUTO-RESPUESTAS DEL HILO DE MENSAJES
        if auto_respuesta != 0:
            n_auto_respuestas += 1

        # MENSAJES DEL MISMO HILO
        if id_hilo_anterior == id_hilo:
            # MENSAJES RESPUESTA #
            if respuesta != 0:
                # DISTANCIA
                distancia += 1

                # MENSAJE Nuevo SUBHILO
                if cambia_subhilo * respuesta < 0:
                    print(index, id_hilo, 'Nuevo SUBHILOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO', respuesta, n_subhilos)
                    cambia_subhilo = cambia_subhilo * -1
                    n_subhilos += 1
                    n_mensajes_medio_subhilo += -(terminal)

                # MENSAJES MISMO HILO #
                else:
                    print(index, id_hilo, 'Mensaje de tipo respuesta') # ,'Mensaje de tipo respuesta del mismo subhilo', respuesta)
                    # ULTIMO MENSAJE DEL HILO
                    if terminal == -1:
                        # LONGITUD MEDIA #
                        longitud_media += longitud/n_mensajes
                        # DISTANCIA y DISTANCIA MEDIA #
                        distancia = mensaje['Distancia PH']
                        distancia_media += distancia/n_mensajes
                        # MENSAJES x SUBHILO
                        n_mensajes_medio_subhilo = n_mensajes_medio_subhilo/n_mensajes

        # MENSAJE CABECERA HILO #
        # CAMBIO DE HILO #
        else:
            print(index, id_hilo, 'Nuevo HILOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO', respuesta)
            id_hilo_anterior = id_hilo
            # ULTIMO MENSAJE DEL HILO

        if terminal == -1:
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
                'Núnero mensajes': n_mensajes,
                'Núnero auto-respuestas': n_auto_respuestas,
                'Núnero subhilos': n_subhilos,
                #    'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                #    'Remitente': id_autor, 'Autor': autor,
                # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                #    'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
                # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                'Date': mensaje['Fecha'] + ' ' + mensaje['Hora'],
                #    'Distancia PH': date_ph, 'Distancia AS': date_as,
                # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                #    'Título mensaje': tit_mensaje, 'Caracteres título mensaje': len(tit_mensaje),
                #    'Texto mensaje': texto.strip(), 'Caracteres texto mensaje': len(texto),
                #    'Diferencia PH': size_ph, 'Diferencia AS': size_as,
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
                #    'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links
            }
            # INICIALIZAR AUTORES #
            autores_previos = []
            # INICIALIZAR CONTADORES HILO #
            longitud = 0
            n_mensajes = 0

            # AÑADIR HILO #
            hilos.append(hilo)

    print(hilos)
    return hilos


## PROCESADO USUARIOS ##
def generar_usuarios(mensajes, hilos, campo):
    global usuarios

    print('#######')
    print('USUARIOS')
    print('#######')
    usuarios = []
    #
    return usuarios


## PROCESADO ASIGNATURAS ##
def generar_asignaturas(mensajes, hilos, usuarios, campo):
    global asignaturas

    print('#######')
    print('ASIGNATIRAS')
    print('#######')
    asignaturas = []
    #
    return asignaturas

# FIN Añadido FJSB

