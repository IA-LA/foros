""""
Created on 09-01-2019

@author: Aitor Diaz Medina

Clase principal encargada llamar al parser y generar el archivo csv resultante

"""

import hashlib
from ConvertirUTF8 import *


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
    # for msj in mensajes:
    #    print(msj)


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

        # Atributos Frecuentistas
        # n_c_
        # n_
        inicial = 1
        respuesta = 0
        terminal = 0

        # Atributos Textuales

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
                    mensaje_no = linea.partition('Mensaje no. ')[2].partition(' (Respuesta a no. ')[0]
                    id_mensaje = str(id_hilo) + "_" + mensaje_no
                    id_ref_mensaje = str(id_hilo) + "_" + respuesta

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
                    mensaje = {'Foro': id_foro, 'ForoN': nombreForo, 'Asignatura': id_asig, 'Título': tit_hilo,
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
                    mensaje = {'Foro': id_foro, 'ForoN': nombreForo, 'Asignatura': id_asig, 'Título': tit_hilo,
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
    # for msj in mensajes:
    #    print(msj)


def generar_mensajes_ampliada(ruta, id_asig):
    with open(ruta, 'r', encoding='utf8') as f:
        lineas = f.readlines()
        lineas = [l.strip('\n') for l in lineas]
        mensajes = []
        # mensaje = []

        # Atributos Base
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

        # Atributos Frecuentistas
        # n_c_
        # n_
        inicial = 1
        respuesta = 0
        terminal = 0

        # Atributos Textuales

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
                    mensaje_no = linea.partition('Mensaje no. ')[2].partition(' (Respuesta a no. ')[0]
                    id_mensaje = str(id_hilo) + "_" + mensaje_no
                    id_ref_mensaje = str(id_hilo) + "_" + respuesta

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

                    # Tipos x posición
                    if id_ref_mensaje == "":
                        inicial = 1
                        respuesta = 0
                        # ????????????????????????????????????????????????????????????????
                        terminal = 0  # Necesita llevar la cuenta de los mensajes del hilo
                    else:
                        inicial = 0
                        respuesta = 1
                        # ????????????????????????????????????????????????????????????????
                        terminal = 0  # Necesita llevar la cuenta de los mensajes del hilo

                    import re

                    def tratamiento(item):
                        print(item)
                        return item

                    # Archivos Adjuntos y enlaces
                    # Cuenta ADJUNTOS: las [IMAGE: '' ...]
                    n_adjs = len(re.findall(r'(\[IMAGE: \'\'.*\])', texto, re.M | re.I))
                    t_adj = ''
                    if n_adjs > 0:
                        t_adj = 'KB [IMAGE:.*])'

                    # Cuenta EMOJI: las [IMAGE: '.+' ...]
                    n_emojis = len(re.findall(r'(\[IMAGE: \'.+\'.*\])', texto, re.M | re.I))
                    print('EMOJIS:', n_emojis)

                    # Busca IMAGENES
                    if texto.find('[IMAGE:'):
                        print('IMAGENES ENCONTRADAS: ', texto.find('[IMAGE:'))
                        # Busca [IMAGE:
                        regex = re.search(r'(\[IMAGE: .*\])', texto, re.M | re.I)
                        if regex != None:
                            # Replace all [IMAGE:
                            texto = re.sub(r'(\[IMAGE: .*\])', '[DATA: .XXX]', texto)
                            print(regex.group(1))
                            print(texto)
                            # exit(12345567890)

                    # Busca LINKS
                    if texto.find('http'):
                        print('LINKS ENCONTRADAS: ', texto.find('http'))
                        n_links = len(re.findall(r'(http)', texto, re.M | re.I))

                    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor,autor,  dia_semana, fecha, tit_mensaje, texto]
                    mensaje = {'Foro': id_foro, 'ForoN': nombreForo, 'Caracteres foro': len(nombreForo),
                               'Asignatura': id_asig, 'Título': tit_hilo, 'Caracteres hilo': len(tit_hilo),
                               'Hilo': id_hilo,
                               'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                               'Inicial': inicial, 'Contestación': respuesta, 'Terminal': terminal,
                               # cuando un menssaje es Iniciador el anterior es Terminal
                               'Remitente': id_autor, 'Autor': autor, 'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                               'Date': fecha + ' ' + hora,
                               'Título mensaje': tit_mensaje, 'Caracteres título': len(tit_mensaje),
                               'Texto mensaje': texto.strip(), 'Caracteres mensaje': len(texto),
                               'n_adj': n_adjs, 't_adj': t_adj, 'n_emojis': n_emojis, 'n_links': n_links}
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
                    mensaje = {'Foro': id_foro, 'ForoN': nombreForo, 'Asignatura': id_asig, 'Título': tit_hilo,
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
    # for msj in mensajes:
    #    print(msj)
# FIN Añadido FJSB

