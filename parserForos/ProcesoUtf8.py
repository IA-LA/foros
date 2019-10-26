""""
Created on 09-01-2019

@author: Aitor Diaz Medina

Clase principal encargada llamar al parser y generar el archivo csv resultante

"""

import hashlib
from datetime import datetime
import numpy as numpy

# VARIABLES GLOBALES #
curso = 1900
tipo = ''
# mensajes = []
hilos = []
autores = []
asignaturas = []
foros = []

dia_semana_nombre = {
    'L': 1,
    'l': 1,
    'Lun': 1,
    'lun': 1,
    'Lunes': 1,
    'lunes': 1,
    'M': 2,
    'm': 2,
    'Mar': 2,
    'mar': 2,
    'Martes': 2,
    'martes': 2,
    'Mx': 3,
    'mx': 3,
    'Mie': 3,
    'mie': 3,
    'Miércoles': 3,
    'miércoles': 3,
    'Miercoles': 3,
    'miercoles': 3,
    'J': 4,
    'j': 4,
    'Jv': 4,
    'jv': 4,
    'Jue': 4,
    'jue': 4,
    'Jueves': 4,
    'jueves': 4,
    'V': 5,
    'v': 5,
    'Vie': 5,
    'vie': 5,
    'Viernes': 5,
    'viernes': 5,
    'S': 6,
    's': 6,
    'Sab': 6,
    'sab': 6,
    'Sábado': 6,
    'sábado': 6,
    'Sabado': 6,
    'sabado': 6,
    'D': 7,
    'd': 7,
    'Dom': 7,
    'dom': 7,
    'Domingo': 7,
    'domingo': 7,
}


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


# INICIO Añadido FJSB
# Manipulaciones
# Campos
## PARTO x CAMPOS ##
def partir_x_campo(lista, campo):
    global mensajes
    global hilos
    global autores
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
        print(val)
        if val != campo_anterior:  # NUEVA INSTANCIA x CAMPO: Hilo, Remitente o Autor,

            campo_anterior = val
            # Array repartido por 'campo'
            destino.insert(jndex, lista_destino)
            jndex = jndex + 1

            print('PARTE POR UN NUEVO CAMPO', index, jndex, val)
            lista_destino = []
            lista_destino.append(li)
        else:
            lista_destino.append(li)

    return destino


## REPARTO x CAMPOS ##
def repartir_x_campo(lista, campo):
    global mensajes
    global hilos
    global autores
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


# Arboles
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


## RECUPERACION MENSAJES DESDE FICHERO ##
# Original
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


# Ampliados
def generar_mensajes_ampliado(ruta, id_asig, curso_asig, tipo, clase=''):
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
        n_mensajes = 0

        # Atributos Base
        id_foro = ""
        # id_asignatura = 12345678
        nombre_foro = ""
        id_hilo = ""
        tit_hilo = ""
        clase_hilo = ''
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

        # Atributos Texto
        var_token = {}
        var_raiz = {}
        var_pos = {}

        # Nombres
        nombre_padre = ''
        nombre_antecesor = ''
        nombre_sucesor = ''

        #from datetime import datetime

        for index, linea in enumerate(lineas):

            if linea.startswith('Foro: '):
                #print(linea.partition('Foro: ')[2])
                nombre_foro = linea.partition('Foro: ')[2]
                ## Foro
                ## ID = HASH('Título Foro' + 'Date')
                # Hash(FORO)
                # con Fecha añadida para hacerlo único
                id_foro = int(hashlib.sha1(nombre_foro.encode('utf-8') + str(datetime.now()).encode('utf-8')).hexdigest(), 16) % (10 ** 8)

            elif linea.startswith('Mensajes de la conversación: '):
                tit_hilo = linea.partition('Mensajes de la conversación: ')[2]
                ## Hilo
                ## ID = HASH('Título del 1er Mensaje del  Hilo' + 'Date')
                # Hash(HILO)
                # con Fecha añadida para hacerlo único
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
                id_autor = int(hashlib.sha1(autor.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
                ## Autor anónimo
                #autor = id_autor

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
                    # Tratamiento AMPLIADO de TEXTO \[(data|link|twitgram|anonimo|movil|email)\]
                    #######################

                    #
                    # HTML ENTITY
                    #
                    # Busca entidades y los sustituye por el carácter equivalente
                    import html as html

                    #texto = html.unescape('Hola, cuando se concrete la fecha para &#39;APP-III&#39;, me dices, por mi parte, si me avisas con tiempo mejor&iexcl;&iexcl;  Saludos&iexcl;&iexcl;')
                    texto = html.unescape(texto)

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
                        print()
                        #print('EMOJIS:', n_emojis)

                    # Cuenta LINKS
                    n_links = 0
                    n_links_r = 0

                    # Busca ADJUNTOS Y EMOJIS y los reemplaza por [DATA]
                    if texto.find('[IMAGE:') != -1:
                        #print('ADJUNTOS ENCONTRADOS: ', n_adjs)
                        # Busca [IMAGE:
                        regex = re.search(r'(\[IMAGE: .*\])', texto, re.M | re.I)
                        if regex != None:
                            # Reemplaza todos los ADJUNTOS Y EMOJIS [IMAGE:] por [DATA] Ampliación: poner tipo [DATA:XXX]
                            texto = re.sub(r'(\[IMAGE: .*\])', ' [DATA] ', texto)
                            # print(regex.group(1))
                            # print(texto)
                            # exit(12345567890)

                    # Busca LINKS (ya eliminados ADJUNTOS y EMOJIS)
                    if texto.find('http') != -1:
                        # Todos los http
                        n_links = len(re.findall(r'(http)', texto, re.M | re.I))
                        #print('LINKS ENCONTRADOS: ', n_links)

                    # Busca links y los reemplaza por [LINK]
                    n_links_r = len(re.findall(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', texto, re.M | re.I))
                    if n_links_r != 0:
                        # Reemplaza todos los LINKS (http) (sin ADJUNTOS y EMOJIS)
                        texto = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', ' [LINK] ', texto)
                        #print('LINKS REEMPLAZADOS: ', n_links_r, texto)

                    # Cuenta ARROBAS, HASHTAG Y MOVILES
                    n_arrobas = 0
                    n_emails_r = 0
                    n_twiters_r = 0
                    n_hashtags = 0
                    n_hashtagr_r = 0
                    n_moviles = 0
                    n_moviles_r = 0
                    n_abrev = 0
                    n_abrev_r = 0

                    # Busca ARROBAS y los reemplaza por [EMAIL] o [TWITGRAM]
                    if texto.find('@') != -1:
                        # Todos los email, twitter o telegram id
                        n_arrobas = len(re.findall(r'(@)', texto, re.M | re.I))
                        # print('ARROBAS ENCONTRADAS: ', n_arrobas)
                    # Busca EMAILS y los reemplaza por [EMAIL]
                    n_emails_r = len(re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', texto, re.M | re.I))
                    if n_emails_r != 0:
                        # Reemplaza todos los EMAILS (a@a.a) (sin LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', ' [EMAIL] ', texto)
                        #print('EMAILS REEMPLAZADOS: ', n_emails_r, texto)
                    # Busca TWITTER/TELEGRAM ID (@a) y los reemplaza por [                                                                                                                                                                                                                                                                                                ]
                    n_twitters_r = len(re.findall(r'(^|[^@\w])@(\w{1,15})\b', texto, re.M | re.I))
                    if n_twitters_r != 0:
                        # Reemplaza todos los TWITTER/TELEGRAMS ID (@a) (sin EMAILS, LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'(^|[^@\w])@(\w{1,15})\b', ' [TWITGRAM] ', texto)
                        #print('TWITTER/TELEGRAM ID REEMPLAZADOS: ', n_twitters_r, texto)

                    # Busca HASHTAGS (#) y los reemplaza por ' [HASHTAG] '
                    # r'#(\w+)'
                    if texto.find('#') != -1:
                        # Todos los hashtags
                        n_hashtags = len(re.findall(r'(#)', texto, re.M | re.I))
                        # print('HASHTAGS ENCONTRADAS: ', n_hashtags)
                    # Busca HASHTAGS ID y los reemplaza por [HASHTAG]
                    n_hashtags_r = len(re.findall(r'(^|[^#\w])#(\w{1,15})\b', texto, re.M | re.I))
                    if n_hashtags_r != 0:
                        # Reemplaza todos los HASHTAGS (#a) (sin TWITTER/TELEGRAMS, EMAILS, LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'(^|[^#\w])#(\w{1,15})\b', ' [HASHTAG] ', texto)
                        #print('HASHTAGS REEMPLAZADOS: ', n_hashtags_r, texto)

                    # Busca NUMEROS DE MOVIL y los reemplaza por ' [MOVIL] ' DE LOS GRUPOS DE TELEGRAM/WHATSAPP
                    # r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}'
                    if texto.find('6') != -1 or texto.find('7') != -1:
                        # Todos los móviles
                        n_moviles = len(re.findall(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', texto, re.M | re.I))
                        # print('MOVILES ENCONTRADOS: ', n_moviles)
                    # Busca MOVILES y los reemplaza por [MOVIL]
                    n_moviles_r = len(re.findall(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', texto, re.M | re.I))
                    if n_moviles_r != 0:
                        # Reemplaza todos los MOVILES (#a) (sin HASHTAGS, TWITTER/TELEGRAMS, EMAILS, LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', ' [MOVIL] ', texto)
                        #print('MOVILES REEMPLAZADOS: ', n_moviles_r, texto)

                    #
                    # ABREVIATURAS DE NOMBRES
                    #
                    # Busca nombres y los sustituye por ' [ANONIMO] '

                    # Busca Abreviaturas Nombres Mª, Mª., M.ª, Fco, Fco.
                    #                    Apellidos Gª, Gª., G.ª
                    #  y los reemplaza por ' ANONIMO ' ' Maria ' ' Francisco ' ' Garcia '
                    if texto.find('Mª') != -1 or texto.find('Mª.') != -1 or texto.find('M.ª') != -1 or texto.find('Gª') != -1 or texto.find('Gª.') != -1 or texto.find('G.ª') != -1:
                        # or texto.find('Fco') != -1 or texto.find('Fco.') != -1 or texto.find('Fco') != -1:
                        # Todas las abreviaturas
                        n_abrev = len(re.findall(r'(M|m|G|g)[ .]*ª[ .]*', texto, re.M | re.I))
                        #print('ABREVIATURAS ENCONTRADAS: ', n_abrev)
                    # Busca ABREVIATURAS y las reemplaza por ' [ANONIMO] '
                    n_abrev_r = len(re.findall(r'(M|m|G|g)[ .]*ª[ .]*', texto, re.M | re.I))
                    if n_abrev_r != 0:
                        # Reemplaza todos las ABREVIATURAS
                        texto = re.sub(r'(M|m|G|g)[ .]*ª[ .]*', ' [ANONIMO] ', texto)
                        #print('ABREVIATURAS REEMPLAZADAS: ', n_abrev_r, texto)

                    #######################
                    # FIN Tratamiento AMPLIADO de TEXTO \[(data|link|twitgram|anonimo|movil|email)\]
                    #######################

                    ###################
                    # ANÁLISIS de TEXTO x MENSAJE
                    ###################
                    from procesadoGeneral import tokenizado
                    from procesadoGeneral import enraizado
                    from procesadoGeneral import postag
                    from procesadoGeneral import cluster

                    #
                    # ANÁLISIS del TEXTO MENSAJE
                    #
                    print('TOKENIZADO MENSAJE')
                    #print('TOKENIZADO MENSAJE(', len(mensajes), ') ASIG(', id_asig, ') TIPO(', tipo, '): ', nombre_antecesor + ' ' + nombre_sucesor + ' ' + nombre_padre)
                    var_token = tokenizado(texto.strip(), nombre_antecesor + ' ' + nombre_sucesor + ' ' + nombre_padre)
                    #print('TOKENIZADO MENSAJE(', len(mensajes), '). ')
                    #print('TOKENIZADO MENSAJE')
                    #print('TOKENIZADO MENSAJE(', n_mensajes_hilo, '): ', var_token)

                    #print('RAICES MENSAJE')
                    print('RAICES MENSAJE(', len(mensajes), ') ASIG(', id_asig, ') TIPO(', tipo, '): ')
                    var_raiz = enraizado()
                    #print('RAICES MENSAJE(', len(mensajes), '). ')
                    #print('RAICES MENSAJE')
                    #print('RAICES MENSAJE(', var_token, '): ', var_raiz)

                    #print('POSTAG MENSAJE')
                    # print('POSTAG MENSAJE(', len(mensajes), ') ASIG(', id_asig, ') TIPO(', tipo, '): ')
                    #var_pos = postag(texto.strip())
                    #print('POSTAG MENSAJE(', len(mensajes), '). ')
                    #print('POSTAG MENSAJE')
                    #print('POSTAG MENSAJE(', len(mensajes), '): ', var_pos)

                    #print('CLUSTER MENSAJE')
                    # print('CLUSTER MENSAJE(', len(mensajes), ') ASIG(', id_asig, ') TIPO(', tipo, '): ')
                    #var_clu = cluster()
                    #print('CLUSTER MENSAJE')
                    #print('CLUSTER MENSAJE: ', var_clu)

                    # exit(999)

                    #
                    # ANÁLISIS del TITULO DEL TEXTO ????????????????????????????????????????????????????????????????????
                    #

                    # exit(999)

                    #
                    # TOPIC MODELLING, t-SNE, Spectral Clusterin de un MENASJE ?????????????????????????????????????????
                    #

                    # exit(999)

                    #
                    # CLUSTERING de MENASJE
                    #
                    #var_clu = cluster()
                    #print('CLUSTER MENSAJE: ', var_clu)

                    # exit(999)

                    #
                    # POSICIONES EN HILO
                    #
                    # INICIAL
                    if id_ref_mensaje == '':

                        # Padre-Hijo
                        nombre_padre = autor

                        # Antecesor-Sucesor
                        nombre_antecesor = nombre_sucesor
                        nombre_sucesor = autor

                    # RESPUESTAS
                    else:

                        # Padre-Hijo

                        # Antecesor-Sucesor
                        nombre_antecesor = nombre_sucesor
                        nombre_sucesor = autor

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
                    #from datetime import datetime

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
                        date_ph = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") -
                                      date_padre).total_seconds()  # (fecha + ' ' + hora) - date_padre

                        # Antecesor-Sucesor en segundos
                        date_as = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") -
                                      date_antecesor).total_seconds()  # (fecha + ' ' + hora) - date_antecesor

                        date_antecesor = datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")  # fecha + ' ' + hora

                        # 1er Mensaje
                        if len(mensajes) == 0:
                            print()
                            #print(date_ph, date_as)

                    # DISTANCIA AL ORIGEN #
                    # Permite ordenar por fecha de forma directa #
                    date_origen = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                        '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds()

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

                    #print()

                    # Actualización Nº Mensajes RESPUESTA del Hilo
                    n_mensajes_hilo = n_mensajes_hilo + 1

                    ########################
                    # Derfinición de MENSAJE (ampliado)
                    ########################
                    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor, autor, dia_semana, fecha, tit_mensaje, texto]
                    if tipo == 'cluster':
                        mensaje = {
                            # BASE #
                            'Asignatura': int(id_asig),
                            'Foro': id_foro,
                            #'Nombre foro': nombre_foro,
                            'Caracteres foro': len(nombre_foro),
                            'Hilo': id_hilo,
                            #'Título': tit_hilo,
                            'Caracteres hilo': len(tit_hilo),
                            #'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                            'Remitente': id_autor, 'Autor': id_autor,
                            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                            'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta,
                            'Terminal': terminal,
                            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                            'Día': int(dia_semana_nombre[dia_semana]),
                            #'Fecha': fecha, 'Hora': hora,
                            'Date': abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                                  '01/09/2010 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
                            'Distancia PH': int(date_ph), 'Distancia AS': int(date_as), 'Distancia OO': int(date_origen),
                            # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                            'Diferencia PH': size_ph, 'Diferencia AS': size_as, 'Diferencia OO': len(nombre_foro) + len(tit_hilo) + len(tit_mensaje) + len(texto),
                            #'Título mensaje': tit_mensaje,
                            'Caracteres título mensaje': len(tit_mensaje),
                            #'Texto mensaje': texto.strip(),
                            'Caracteres texto mensaje': len(texto),
                            # ANÁLISIS de TEXTO
                            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                            #'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                            "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                            # .SnowballStemmer("spanish").stem,
                            #'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                            'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                            'Cantidad de Información': var_raiz.get('nrd')/var_token.get('nt') if var_token.get('nt') != 0 else 0,
                            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                            #'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                            # PoS: # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                            'Curso': int(curso),
                        }
                    elif tipo == 'clasificador':
                        # Recoge CLASES anotadas
                        if isinstance(clase[len(mensajes)], str): #numpy.isnan(clase[len(mensajes)]):
                            clase_hilo = clase[len(mensajes)]
                        mensaje = {
                            # BASE #
                            'Clase': clase_hilo,
                            'Asignatura': int(id_asig),
                            'Foro': id_foro,
                            #'Nombre foro': nombre_foro,
                            'Caracteres foro': len(nombre_foro),
                            'Hilo': id_hilo,
                            #'Título': tit_hilo,
                            'Caracteres hilo': len(tit_hilo),
                            #'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                            'Remitente': id_autor, 'Autor': id_autor,
                            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                            'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta,
                            'Terminal': terminal,
                            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                            'Día': int(dia_semana_nombre[dia_semana]),
                            #'Fecha': fecha, 'Hora': hora,
                            'Date': abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                                  '01/09/2010 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
                            'Distancia PH': int(date_ph), 'Distancia AS': int(date_as), 'Distancia OO': int(date_origen),
                            # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                            'Diferencia PH': size_ph, 'Diferencia AS': size_as, 'Diferencia OO': len(nombre_foro) + len(tit_hilo) + len(tit_mensaje) + len(texto),
                            #'Título mensaje': tit_mensaje,
                            'Caracteres título mensaje': len(tit_mensaje),
                            #'Texto mensaje': texto.strip(),
                            'Caracteres texto mensaje': len(texto),
                            # ANÁLISIS de TEXTO
                            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                            #'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                            "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                            # .SnowballStemmer("spanish").stem,
                            #'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                            'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                            'Cantidad de Información': var_raiz.get('nrd')/var_token.get('nt') if var_token.get('nt') != 0 else 0,
                            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                            #'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                            # PoS: # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                            'Curso': int(curso),
                        }
                    else:  # General
                        mensaje = {
                            # BASE #
                            'Asignatura': int(id_asig),
                            'Foro': id_foro, 'Nombre foro': nombre_foro, 'Caracteres foro': len(nombre_foro),
                            'Hilo': id_hilo, 'Título': tit_hilo, 'Caracteres hilo': len(tit_hilo),
                            'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                            'Remitente': id_autor, 'Autor': autor,
                            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                            'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
                            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                            'Día': dia_semana,
                            'Fecha': fecha, 'Hora': hora, 'Date': fecha + ' ' + hora,
                            'Distancia PH': int(date_ph), 'Distancia AS': int(date_as), 'Distancia OO': int(date_origen),
                            # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                            'Título mensaje': tit_mensaje, 'Caracteres título mensaje': len(tit_mensaje),
                            'Texto mensaje': texto.strip(), 'Caracteres texto mensaje': len(texto),
                            'Diferencia PH': size_ph, 'Diferencia AS': size_as, 'Diferencia OO': len(nombre_foro) + len(tit_hilo) + len(tit_mensaje) + len(texto),
                            # ANÁLISIS de TEXTO
                            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                            # {"c": msj, "lc": longitud_caracteres, 't': lista_tokens, 'nt': numero_tokens, 'f': sentencias,
                            #             'nf': numero_frases, 'p': lista_palabras, 'np': numero_palabras, 'ns': numero_stop_words}
                            'Tokens': var_token.get('t'),  # Anotación revisores externos y Revisión de los Nombres anónimos
                            # 'Frases': var_token.get('f'),  # Revisión del los Nombres no anónimos
                            #'Tokens': var_token,
                            # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                            "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                            # .SnowballStemmer("spanish").stem,
                            'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                            'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                            'Cantidad de Información': var_raiz.get('nrd')/var_token.get('nt') if var_token.get('nt') != 0 else 0,
                            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                            # 'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                            # PoS: # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                            'Curso': int(curso),
                        }

                    mensajes.append(mensaje)

                    # Limpia variables
                    texto = ""
                    autor = ""
                    # print(linea)

            if lineas[index - 1].startswith('Título: '):
                estado = 'MENSAJE'

            if estado == 'MENSAJE':
                texto = texto + ' ' + linea

    return mensajes


# Anónimos
def generar_mensajes_anonimo(ruta, id_asig, curso_asig, tipo, clase=''):
    global mensajes

    print('#######')
    print('MENSAJES')
    print('#######')

    lineas_anonimas = []
    curso = curso_asig
    with open(ruta, 'r', encoding='utf8') as f:
        lineas = f.readlines()
        lineas = [l.strip('\n') for l in lineas]
        mensajes = []
        # mensaje = []
        n_mensajes = 0

        # Atributos Base
        id_foro = ""
        # id_asignatura = 12345678
        nombre_foro = ""
        id_hilo = ""
        tit_hilo = ""
        clase_hilo = ''
        id_mensaje = ""
        id_ref_mensaje = ""
        id_autor = ""
        autor = ""
        fecha = ""
        dia_semana = ""
        tit_mensaje = ""
        texto = ""
        estado = 'FIN_MENSAJE'
        contador_lineas_titulo = 1
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

        # Atributos Texto
        var_token = {}
        var_raiz = {}
        var_pos = {}

        # Nombres
        nombre_padre = ''
        nombre_antecesor = ''
        nombre_sucesor = ''

        #from datetime import datetime

        for index, linea in enumerate(lineas):

            print(linea)
            # Controla Títulos de Hilo y Mensaje de más de una línea
            if estado == 'TITULO_LARGO':
                # Títulos de +1 línea:
                # Revisa la siguiente línea por si el título ocupa dos o + líneas
                if not lineas[index + 1].startswith('_______________________________________________________________________________'):
                    estado = 'TITULO_LARGO'
                    tit_hilo = tit_hilo + ' ' + linea
                    contador_lineas_titulo += 1
                else:
                    estado = 'MENSAJE'
                    tit_hilo = tit_hilo + ' ' + linea
                    # contador_lineas_titulo = 1

            elif linea.startswith('Foro: '):
                #print(linea.partition('Foro: ')[2])
                nombre_foro = linea.partition('Foro: ')[2]
                ## Foro
                ## ID = HASH('Título Foro' + 'Date')
                # Hash(FORO)
                # con Fecha añadida para hacerlo único
                id_foro = int(hashlib.sha1(nombre_foro.encode('utf-8') + str(datetime.now()).encode('utf-8')).hexdigest(), 16) % (10 ** 8)

                # Anonimato:
                ############
                #linea = linea.replace(linea.partition('Foro: ')[2], str(id_foro), 1)

            # Título de Hilo
            elif linea.startswith('Mensajes de la conversación: '):

                # Inicializa contador con el Nuevo Hilo
                if contador_lineas_titulo > 1:
                    contador_lineas_titulo = 1

                # Títulos de +1 línea:
                # Revisa la siguiente línea por si el título ocupa dos o + líneas
                if not lineas[index + 1].startswith('_______________________________________________________________________________'):
                    estado = 'TITULO_LARGO'
                    contador_lineas_titulo += 1

                tit_hilo = linea.partition('Título: ')[2]

                ## Hilo
                ## ID = HASH('Título del 1er Mensaje del  Hilo' + 'Date')
                # Hash(HILO)
                # con Fecha añadida para hacerlo único
                id_hilo = int(hashlib.sha1(tit_hilo.encode('utf-8') + str(datetime.now()).encode('utf-8')).hexdigest(), 16) % (10 ** 8)

                # Anonimato:
                ############
                #linea = linea.replace(linea.partition('Mensajes de la conversación: ')[2], str(id_foro), 1)

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
                #autor = id_autor

                # Anonimato:
                ############
                linea = linea.replace(linea.partition('Enviado por: ')[2].partition(" el")[0], str(id_autor), 1)

                fecha = linea.partition(" el ")[2].strip()
                if not lineas[index + 1].startswith('Título: '):
                    # print('bien, estado: ' + estado)
                    fecha = fecha + " " + lineas[index + 1]
                    # print(fecha)
                # else:
                #    print('bien : ' + fecha)
                # print(fecha)

            # Título de Mensaje
            elif linea.startswith('Título: '):
                # print(lineas[lineas.index(linea)-1])
                # if not lineas[lineas.index(linea)-1].startswith('Enviado por: '):
                #   fecha = fecha.strip() + ' ' + lineas[lineas.index(linea)-1].strip()
                #  print(lineas[lineas.index(linea)-1], fecha)
                # print(linea)

                # Títulos de +1 línea:
                # Revisa la siguiente línea por si el título ocupa dos líneas
                if not lineas[index + 1].startswith('_______________________________________________________________________________'):
                    estado = 'TITULO_LARGO'
                    #tit_hilo = linea.partition('Título: ')[2] + lineas[index + 1]

                #if mensaje_no == "1":
                #    tit_hilo = linea.partition('Título: ')[2]

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
                    # Tratamiento AMPLIADO de TEXTO \[(data|link|twitgram|anonimo|movil|email)\]
                    #######################

                    #
                    # HTML ENTITY
                    #
                    # Busca entidades y los sustituye por el carácter equivalente
                    import html as html

                    #texto = html.unescape('Hola, cuando se concrete la fecha para &#39;APP-III&#39;, me dices, por mi parte, si me avisas con tiempo mejor&iexcl;&iexcl;  Saludos&iexcl;&iexcl;')
                    texto = html.unescape(texto)

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
                        print()
                        #print('EMOJIS:', n_emojis)

                    # Cuenta LINKS
                    n_links = 0
                    n_links_r = 0

                    # Busca ADJUNTOS Y EMOJIS y los reemplaza por [DATA]
                    if texto.find('[IMAGE:') != -1:
                        #print('ADJUNTOS ENCONTRADOS: ', n_adjs)
                        # Busca [IMAGE:
                        regex = re.search(r'(\[IMAGE: .*\])', texto, re.M | re.I)
                        if regex != None:
                            # Reemplaza todos los ADJUNTOS Y EMOJIS [IMAGE:] por [DATA] Ampliación: poner tipo [DATA:XXX]
                            texto = re.sub(r'(\[IMAGE: .*\])', ' [DATA] ', texto)
                            # print(regex.group(1))
                            # print(texto)
                            # exit(12345567890)

                    # Busca LINKS (ya eliminados ADJUNTOS y EMOJIS)
                    if texto.find('http') != -1:
                        # Todos los http
                        n_links = len(re.findall(r'(http)', texto, re.M | re.I))
                        #print('LINKS ENCONTRADOS: ', n_links)

                    # Busca links y los reemplaza por [LINK]
                    n_links_r = len(re.findall(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', texto, re.M | re.I))
                    if n_links_r != 0:
                        # Reemplaza todos los LINKS (http) (sin ADJUNTOS y EMOJIS)
                        texto = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', ' [LINK] ', texto)
                        #print('LINKS REEMPLAZADOS: ', n_links_r, texto)

                    # Cuenta ARROBAS, HASHTAG Y MOVILES
                    n_arrobas = 0
                    n_emails_r = 0
                    n_twiters_r = 0
                    n_hashtags = 0
                    n_hashtagr_r = 0
                    n_moviles = 0
                    n_moviles_r = 0
                    n_abrev = 0
                    n_abrev_r = 0

                    # Busca ARROBAS y los reemplaza por [EMAIL] o [TWITGRAM]
                    if texto.find('@') != -1:
                        # Todos los email, twitter o telegram id
                        n_arrobas = len(re.findall(r'(@)', texto, re.M | re.I))
                        # print('ARROBAS ENCONTRADAS: ', n_arrobas)
                    # Busca EMAILS y los reemplaza por [EMAIL]
                    n_emails_r = len(re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', texto, re.M | re.I))
                    if n_emails_r != 0:
                        # Reemplaza todos los EMAILS (a@a.a) (sin LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', ' [EMAIL] ', texto)
                        #print('EMAILS REEMPLAZADOS: ', n_emails_r, texto)
                    # Busca TWITTER/TELEGRAM ID (@a) y los reemplaza por [                                                                                                                                                                                                                                                                                                ]
                    n_twitters_r = len(re.findall(r'(^|[^@\w])@(\w{1,15})\b', texto, re.M | re.I))
                    if n_twitters_r != 0:
                        # Reemplaza todos los TWITTER/TELEGRAMS ID (@a) (sin EMAILS, LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'(^|[^@\w])@(\w{1,15})\b', ' [TWITGRAM] ', texto)
                        #print('TWITTER/TELEGRAM ID REEMPLAZADOS: ', n_twitters_r, texto)

                    # Busca HASHTAGS (#) y los reemplaza por ' [HASHTAG] '
                    # r'#(\w+)'
                    if texto.find('#') != -1:
                        # Todos los hashtags
                        n_hashtags = len(re.findall(r'(#)', texto, re.M | re.I))
                        # print('HASHTAGS ENCONTRADAS: ', n_hashtags)
                    # Busca HASHTAGS ID y los reemplaza por [HASHTAG]
                    n_hashtags_r = len(re.findall(r'(^|[^#\w])#(\w{1,15})\b', texto, re.M | re.I))
                    if n_hashtags_r != 0:
                        # Reemplaza todos los HASHTAGS (#a) (sin TWITTER/TELEGRAMS, EMAILS, LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'(^|[^#\w])#(\w{1,15})\b', ' [HASHTAG] ', texto)
                        #print('HASHTAGS REEMPLAZADOS: ', n_hashtags_r, texto)

                    # Busca NUMEROS DE MOVIL y los reemplaza por ' [MOVIL] ' DE CONTACTO O GRUPOS DE TELEGRAM/WHATSAPP
                    # r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}'
                    if texto.find('6') != -1 or texto.find('7') != -1:
                        # Todos los móviles
                        n_moviles = len(re.findall(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', texto, re.M | re.I))
                        # print('MOVILES ENCONTRADOS: ', n_moviles)
                    # Busca MOVILES y los reemplaza por [MOVIL]
                    n_moviles_r = len(re.findall(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', texto, re.M | re.I))
                    if n_moviles_r != 0:
                        # Reemplaza todos los MOVILES (#a) (sin HASHTAGS, TWITTER/TELEGRAMS, EMAILS, LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', ' [MOVIL] ', texto)
                        #print('MOVILES REEMPLAZADOS: ', n_moviles_r, texto)

                    # Busca NUMEROS DE DNI o NIE y los reemplaza por ' [DNI] '
                    # NIE: r'([X-Z]{1})([-]?)(\d{7})([-]?)([A-Z]{1})'
                    # DNI: r'(\d{8})([-]?)([A-Z]{1})
                    # r'(([x-zX-Z]{1})([-]?)(((\d){7,8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([-]?)([a-zA-Z]{1}))|(((\d){8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([a-zA-Z]{1})
                    n_dnis_r = len(re.findall(r'(([x-zX-Z]{1})([-]?)(((\d){7,8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([-]?)([a-zA-Z]{1}))|(((\d){8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([a-zA-Z]{1})', texto, re.M | re.I))
                    if n_dnis_r != 0:
                        # Reemplaza todos los DNI (#a) (sin MOVILES HASHTAGS, TWITTER/TELEGRAMS, EMAILS, LINKS, ADJUNTOS y EMOJIS)
                        texto = re.sub(r'(([x-zX-Z]{1})([-]?)(((\d){7,8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([-]?)([a-zA-Z]{1}))|(((\d){8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([a-zA-Z]{1})', ' [DNI] ', texto)
                        print('DNIS REEMPLAZADOS: ', n_dnis_r, texto)

                    #
                    # ABREVIATURAS DE NOMBRES
                    #
                    # Busca nombres y los sustituye por ' [ANONIMO] '

                    # Busca Abreviaturas Nombres Mª, Mª., M.ª, Fco, Fco.
                    #                    Apellidos Gª, Gª., G.ª
                    #  y los reemplaza por ' ANONIMO ' ' Maria ' ' Francisco ' ' Garcia '
                    if texto.find('Mª') != -1 or texto.find('Mª.') != -1 or texto.find('M.ª') != -1 or texto.find('Gª') != -1 or texto.find('Gª.') != -1 or texto.find('G.ª') != -1:
                        # or texto.find('Fco') != -1 or texto.find('Fco.') != -1 or texto.find('Fco') != -1:
                        # Todas las abreviaturas
                        n_abrev = len(re.findall(r'(M|m|G|g)[ .]*ª[ .]*', texto, re.M | re.I))
                        #print('ABREVIATURAS ENCONTRADAS: ', n_abrev)
                    # Busca ABREVIATURAS y las reemplaza por ' [ANONIMO] '
                    n_abrev_r = len(re.findall(r'(M|m|G|g)[ .]*ª[ .]*', texto, re.M | re.I))
                    if n_abrev_r != 0:
                        # Reemplaza todos las ABREVIATURAS
                        texto = re.sub(r'(M|m|G|g)[ .]*ª[ .]*', ' [ANONIMO] ', texto)
                        #print('ABREVIATURAS REEMPLAZADAS: ', n_abrev_r, texto)

                    #######################
                    # FIN Tratamiento AMPLIADO de TEXTO \[(data|link|twitgram|anonimo|movil|email)\]
                    #######################

                    ###################
                    # ANÁLISIS de TEXTO x MENSAJE
                    ###################
                    from procesadoGeneral import tokenizado
                    from procesadoGeneral import enraizado
                    from procesadoGeneral import postag
                    from procesadoGeneral import cluster

                    #
                    # ANÁLISIS del TEXTO MENSAJE
                    #
                    #print('TOKENIZADO MENSAJE')
                    print('TOKENIZADO MENSAJE(', len(mensajes), ') ASIG(', id_asig, ') TIPO(', tipo, '): ', nombre_antecesor + ' ' + nombre_sucesor + ' ' + nombre_padre)
                    # var_token = {'t': 0, 'lc': 0, 'nt': 0, 'nf': 0, 'np': 0, 'ns': 0}
                    var_token = tokenizado(texto.strip(), nombre_antecesor + ' ' + nombre_sucesor + ' ' + nombre_padre)
                    #print('TOKENIZADO MENSAJE(', len(mensajes), '). ')
                    #print('TOKENIZADO MENSAJE')
                    #print('TOKENIZADO MENSAJE(', n_mensajes_hilo, '): ', var_token)

                    #print('RAICES MENSAJE')
                    print('RAICES MENSAJE(', len(mensajes), ') ASIG(', id_asig, ') TIPO(', tipo, '): ')
                    var_raiz = enraizado()
                    #print('RAICES MENSAJE(', len(mensajes), '). ')
                    #print('RAICES MENSAJE')
                    #print('RAICES MENSAJE(', var_token, '): ', var_raiz)

                    #print('POSTAG MENSAJE')
                    # print('POSTAG MENSAJE(', len(mensajes), ') ASIG(', id_asig, ') TIPO(', tipo, '): ')
                    #var_pos = postag(texto.strip())
                    #print('POSTAG MENSAJE(', len(mensajes), '). ')
                    #print('POSTAG MENSAJE')
                    #print('POSTAG MENSAJE(', len(mensajes), '): ', var_pos)

                    #print('CLUSTER MENSAJE')
                    # print('CLUSTER MENSAJE(', len(mensajes), ') ASIG(', id_asig, ') TIPO(', tipo, '): ')
                    #var_clu = cluster()
                    #print('CLUSTER MENSAJE')
                    #print('CLUSTER MENSAJE: ', var_clu)

                    # exit(999)

                    #
                    # ANÁLISIS del TITULO DEL TEXTO ????????????????????????????????????????????????????????????????????
                    #

                    # exit(999)

                    #
                    # TOPIC MODELLING, t-SNE, Spectral Clusterin de un MENASJE ?????????????????????????????????????????
                    #

                    # exit(999)

                    #
                    # CLUSTERING de MENASJE
                    #
                    #var_clu = cluster()
                    #print('CLUSTER MENSAJE: ', var_clu)

                    # exit(999)

                    #
                    # POSICIONES EN HILO
                    #
                    # INICIAL
                    if id_ref_mensaje == '':

                        # Padre-Hijo
                        nombre_padre = autor

                        # Antecesor-Sucesor
                        nombre_antecesor = nombre_sucesor
                        nombre_sucesor = autor

                    # RESPUESTAS
                    else:

                        # Padre-Hijo

                        # Antecesor-Sucesor
                        nombre_antecesor = nombre_sucesor
                        nombre_sucesor = autor

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
                    #from datetime import datetime

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
                        date_ph = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") -
                                      date_padre).total_seconds()  # (fecha + ' ' + hora) - date_padre

                        # Antecesor-Sucesor en segundos
                        date_as = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") -
                                      date_antecesor).total_seconds()  # (fecha + ' ' + hora) - date_antecesor

                        date_antecesor = datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")  # fecha + ' ' + hora

                        # 1er Mensaje
                        if len(mensajes) == 0:
                            print()
                            #print(date_ph, date_as)

                    # DISTANCIA AL ORIGEN #
                    # Permite ordenar por fecha de forma directa #
                    date_origen = abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                        '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds()

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

                    #print()

                    # Actualización Nº Mensajes RESPUESTA del Hilo
                    n_mensajes_hilo = n_mensajes_hilo + 1

                    ########################
                    # Derfinición de MENSAJE (ampliado)
                    ########################
                    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor, autor, dia_semana, fecha, tit_mensaje, texto]
                    if tipo == 'cluster':
                        mensaje = {
                            # BASE #
                            'Asignatura': int(id_asig),
                            'Foro': id_foro,
                            #'Nombre foro': nombre_foro,
                            'Caracteres foro': len(nombre_foro),
                            'Hilo': id_hilo,
                            #'Título': tit_hilo,
                            'Caracteres hilo': len(tit_hilo),
                            #'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                            'Remitente': id_autor, 'Autor': id_autor,
                            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                            'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta,
                            'Terminal': terminal,
                            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                            'Día': int(dia_semana_nombre[dia_semana]),
                            #'Fecha': fecha, 'Hora': hora,
                            'Date': abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                                  '01/09/2010 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
                            'Distancia PH': int(date_ph), 'Distancia AS': int(date_as), 'Distancia OO': int(date_origen),
                            # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                            'Diferencia PH': size_ph, 'Diferencia AS': size_as, 'Diferencia OO': len(nombre_foro) + len(tit_hilo) + len(tit_mensaje) + len(texto),
                            #'Título mensaje': tit_mensaje,
                            'Caracteres título mensaje': len(tit_mensaje),
                            #'Texto mensaje': texto.strip(),
                            'Caracteres texto mensaje': len(texto),
                            # ANÁLISIS de TEXTO
                            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                            #'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                            "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                            # .SnowballStemmer("spanish").stem,
                            #'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                            'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                            'Cantidad de Información': var_raiz.get('nrd')/var_token.get('nt') if var_token.get('nt') != 0 else 0,
                            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                            #'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                            # PoS: # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                            'Curso': int(curso),
                        }
                    elif tipo == 'clasificador':
                        # Recoge CLASES anotadas
                        if isinstance(clase[len(mensajes)], str): #numpy.isnan(clase[len(mensajes)]):
                            clase_hilo = clase[len(mensajes)]
                        mensaje = {
                            # BASE #
                            'Clase': clase_hilo,
                            'Asignatura': int(id_asig),
                            'Foro': id_foro,
                            #'Nombre foro': nombre_foro,
                            'Caracteres foro': len(nombre_foro),
                            'Hilo': id_hilo,
                            #'Título': tit_hilo,
                            'Caracteres hilo': len(tit_hilo),
                            #'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                            'Remitente': id_autor, 'Autor': id_autor,
                            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                            'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta,
                            'Terminal': terminal,
                            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                            'Día': int(dia_semana_nombre[dia_semana]),
                            #'Fecha': fecha, 'Hora': hora,
                            'Date': abs(datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                                  '01/09/2010 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
                            'Distancia PH': int(date_ph), 'Distancia AS': int(date_as), 'Distancia OO': int(date_origen),
                            # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                            'Diferencia PH': size_ph, 'Diferencia AS': size_as, 'Diferencia OO': len(nombre_foro) + len(tit_hilo) + len(tit_mensaje) + len(texto),
                            #'Título mensaje': tit_mensaje,
                            'Caracteres título mensaje': len(tit_mensaje),
                            #'Texto mensaje': texto.strip(),
                            'Caracteres texto mensaje': len(texto),
                            # ANÁLISIS de TEXTO
                            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                            #'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                            "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                            # .SnowballStemmer("spanish").stem,
                            #'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                            'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                            'Cantidad de Información': var_raiz.get('nrd')/var_token.get('nt') if var_token.get('nt') != 0 else 0,
                            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                            #'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                            # PoS: # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                            'Curso': int(curso),
                        }
                    else:  # General
                        mensaje = {
                            # BASE #
                            'Asignatura': int(id_asig),
                            'Foro': id_foro, 'Nombre foro': nombre_foro, 'Caracteres foro': len(nombre_foro),
                            'Hilo': id_hilo, 'Título': tit_hilo, 'Caracteres hilo': len(tit_hilo),
                            'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                            'Remitente': id_autor, 'Autor': autor,
                            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                            'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
                            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                            'Día': dia_semana,
                            'Fecha': fecha, 'Hora': hora, 'Date': fecha + ' ' + hora,
                            'Distancia PH': int(date_ph), 'Distancia AS': int(date_as), 'Distancia OO': int(date_origen),
                            # DIFERENCIAS Padre-Hijo Antecesor-Sucesor
                            'Título mensaje': tit_mensaje, 'Caracteres título mensaje': len(tit_mensaje),
                            'Texto mensaje': texto.strip(), 'Caracteres texto mensaje': len(texto),
                            'Diferencia PH': size_ph, 'Diferencia AS': size_as, 'Diferencia OO': len(nombre_foro) + len(tit_hilo) + len(tit_mensaje) + len(texto),
                            # ANÁLISIS de TEXTO
                            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                            # {"c": msj, "lc": longitud_caracteres, 't': lista_tokens, 'nt': numero_tokens, 'f': sentencias,
                            #             'nf': numero_frases, 'p': lista_palabras, 'np': numero_palabras, 'ns': numero_stop_words}
                            'Tokens': var_token.get('t'),  # Anotación revisores externos y Revisión de los Nombres anónimos
                            # 'Frases': var_token.get('f'),  # Revisión del los Nombres no anónimos
                            #'Tokens': var_token,
                            # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                            "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                            # .SnowballStemmer("spanish").stem,
                            'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                            'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                            'Cantidad de Información': var_raiz.get('nrd')/var_token.get('nt') if var_token.get('nt') != 0 else 0,
                            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                            # 'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                            # PoS: # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                            'Curso': int(curso),
                        }

                    mensajes.append(mensaje)


                    # Anonimato:
                    ############
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + str(mensaje['Texto mensaje']) + "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
                    #linea = texto
                    #lineas_anonimas.append(texto + '\n')

                    # Limpia variables
                    texto = ""
                    autor = ""
                    # print(linea)

            if lineas[index - 1].startswith('Título: '):
                estado = 'MENSAJE'

            if estado == 'MENSAJE':
                texto = texto + ' ' + linea

            else:
                if linea.startswith('_______________________________________________________________________________'):
                    estado = 'MENSAJE'

            lineas_anonimas.append(linea+'\n')

    print(lineas_anonimas)
    with open(ruta.split('utf8')[0] + '_anonimo.txt', 'w', encoding='utf8') as f_destino:
        f_destino.writelines(lineas_anonimas)

    return mensajes


## PROCESADO MENSAJES ##
def generar_mensajes(mensajes, campo, ruta, id_asig, curso_asig, tipo):

    print('#######')
    print('MENSAJES')
    print('#######')
    mensajes = []
    curso = curso_asig

    # Variables Globales
    mensaje = {}
    # Interruptores
    msj_previo = 0

    # Totales
    n_msj = 0

    # PARA CADA MENSAJE #
    for index, mensaje in enumerate(mensajes):
        if mensaje['Mensaje'] != msj_previo:
            n_msj += 1
            msj_previo = mensaje['Mensaje']

    ########################
    # Derfinición de MENSAJE (ampliado)
    ########################
    # mensaje=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor, autor, dia_semana, fecha, tit_mensaje, texto]
    if tipo == 'excel':
        mensaje = {}
    elif tipo == 'cluster':
        mensaje = {}
    elif tipo == 'clasificador':
        mensaje = {}
    else:
        mensaje = {}

    mensajes.append(mensaje)

    return mensajes


## PROCESADO HILOS ##
def generar_hilos(mensajes, campo, curso_asig, tipo, clase=''):
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
        #print("well, it WASN'T defined after all!")
        id_hilo_anterior = 0
        cambia_subhilo = 1
    else:
        #print("sure, it was defined.")
        id_hilo_anterior = 0
        cambia_subhilo = 1
    # Fin excepción

    # Variables Globales
    autores_previos = []
    foro_previo = 0
    clase_hilo = ''

    # Totales
    n_mensajes = 0
    n_autores = 0
    n_hilos = 0
    n_foros = 0
    n_subhilos = 0
    n_auto_respuestas = 0
    longitud = 0  # Tamaño texto
    distancia = 0  # Duración

    # 'Distancia PH': int(date_ph), 'Distancia AS': int(date_as), 'Distancia OO': int(date_origen),
    # 'Diferencia PH': size_ph, 'Diferencia AS': size_as, 'Diferencia OO': len(nombre_foro) + len(tit_hilo) + len(tit_mensaje) + len(texto),
    longitud_hilo = 0
    distancia_hilo = 0
    longitud_00 = 0
    distancia_00 = 0

    # ACUMULADOS ANÁLISIS TEXTO
    lc = 0
    nt = 0
    nf = 0
    np = 0
    ns = 0
    nr = 0
    nrd = 0
    nn = 0
    nnd = 0
    nv = 0
    nvd = 0
    # 'Cantidad de Información': var_raiz.get('nrd') / var_token.get('nt') if var_token.get('nt') != 0 else 0,
    cdi = 0
    # ACUMULADOS ADJUNTOS
    n_adjs = 0
    t_adj = 0
    n_emojis = 0
    n_links = 0

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
    # Atributos Texto
    var_token = {}
    var_raiz = {}
    var_pos = {}

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

        # Recoge CLASES anotadas
        if tipo == 'clasificador' and isinstance(clase[index], str):  # numpy.isnan(clase[len(mensajes)]):
            clase_hilo = clase[index]

        # ACUMULADOS ANÁLISIS TEXTO
        lc += mensaje['lc']
        nt += mensaje['nt']
        nf += mensaje['nf']
        np += mensaje['np']
        ns += mensaje['ns']
        nr += mensaje['nr']
        nrd += mensaje['nrd']
        #nn += mensaje['nn']
        #nnd += mensaje['nnd']
        #nv += mensaje['nv']
        #nvd += mensaje['nvd']
        # ACUMULADOS ADJUNTOS
        n_adjs += mensaje['Adjuntos']
        t_adj += mensaje['Tamaño adjuntos']
        n_emojis += mensaje['Emojis']
        n_links += mensaje['Links']

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
                    #print(index, id_hilo, 'Nuevo SUBHILOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO', respuesta, n_subhilos)
                    cambia_subhilo = cambia_subhilo * -1
                    # Cuenta las Ramificaciones del hilo principal (-1,1)
                    if respuesta != 1 and respuesta != -1:
                        n_subhilos += 1
                    n_mensajes_medio_subhilo = 1
                # MENSAJE MISMO SUBHILO #
                else:
                    #print(index, id_hilo, 'Mensaje de tipo respuesta') # ,'Mensaje de tipo respuesta del mismo subhilo', respuesta)
                    n_mensajes_medio_subhilo += 1
                    # ULTIMO MENSAJE DEL HILO Y del último SUBHILO del HILO
                    #########################
                    if terminal == -1:
                        print('ULTIMO MENSAJE HILO: (', len(mensajes), ') HILO(', n_hilos, ') MSJ(', n_mensajes, '): ')
                        #print(index, id_hilo, 'Mensaje de tipo respuesta último del hilo')
            # MENSAJE NO RESPUESTA #
            else:
                n_hilos += 1

        # MENSAJE CABECERA HILO (INICIALIZAR) #
        # NUEVO HILO (INICIALIZAR) #
        ############################
        else:
            #print(index, id_hilo, 'Nuevo HILOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO', respuesta)

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
            import numpy as numpy

            # TIEMPO
            # PH
            # CALCULAR TIEMPOS #
            media_tiempos_ph = numpy.mean(lista_tiempos_previos_ph)
            mediana_tiempos_ph = numpy.median(lista_tiempos_previos_ph)
            # Excepción:
            try:
                # MODA
                #print("MODA_T:", len(contador_tiempos_previos_ph), max(contador_tiempos_previos_ph))
                max_tiempos_ph = max(lista_tiempos_previos_ph)
                min_tiempos_ph = min(lista_tiempos_previos_ph)

                (_, idx, counts) = numpy.unique(lista_tiempos_previos_ph, return_index=True, return_counts=True)
                index_np = idx[numpy.argmax(counts)]
                moda_tiempos_ph = lista_tiempos_previos_ph[index_np]

                #print("MODA_T:", moda_tiempos_ph)

            except NameError:
                #print("well, it WASN'T defined after all! (MODA_T)")
                moda_tiempos_ph = 0
            else:
                #print("sure, it was defined. (MODA_T)")
                moda_tiempos_ph = moda_tiempos_ph
            # Fin excepción
            rango_tiempos_ph = sorted(lista_tiempos_previos_ph)[len(lista_tiempos_previos_ph)-1] - sorted(lista_tiempos_previos_ph)[0]
            #print("MediaTph: ", media_tiempos_ph)
            #print("MedianaTph: ", mediana_tiempos_ph)
            #print("ModaTph: ", moda_tiempos_ph)
            #print("RangoTph: ", rango_tiempos_ph)

            # AS
            # CALCULAR TIEMPOS #
            media_tiempos = numpy.mean(lista_tiempos_previos)
            mediana_tiempos = numpy.median(lista_tiempos_previos)
            # Excepción:
            try:
                # MODA
                #print("MODA_T:", len(contador_tiempos_previos), max(contador_tiempos_previos))
                max_tiempos = max(lista_tiempos_previos)
                min_tiempos = min(lista_tiempos_previos)

                (_, idx, counts) = numpy.unique(lista_tiempos_previos, return_index=True, return_counts=True)
                index_np = idx[numpy.argmax(counts)]
                moda_tiempos = lista_tiempos_previos[index_np]

                #print("MODA_T:", moda_tiempos)

            except NameError:
                #print("well, it WASN'T defined after all! (MODA_T)")
                moda_tiempos = 0
            else:
                #print("sure, it was defined. (MODA_T)")
                moda_tiempos = moda_tiempos
            # Fin excepción
            rango_tiempos = sorted(lista_tiempos_previos)[len(lista_tiempos_previos)-1] - sorted(lista_tiempos_previos)[0]
            #print("MediaT: ", media_tiempos)
            #print("MedianaT: ", mediana_tiempos)
            #print("ModaT: ", moda_tiempos)
            #print("RangoT: ", rango_tiempos)

            # TAMAÑO
            la_longitud = mensaje['Caracteres texto mensaje']
            # INICIALIZAR LONGITUDES #
            media_longitudes = numpy.mean(lista_longitudes_previas)
            mediana_longitudes = numpy.median(lista_longitudes_previas)
            # Excepción:
            try:
                # MODA
                #print("MODA_L:", len(contador_longitudes_previas), max(contador_longitudes_previas))
                max_longitudes = max(lista_longitudes_previas)
                min_longitudes = min(lista_longitudes_previas)

                (_, idx, counts) = numpy.unique(lista_longitudes_previas, return_index=True, return_counts=True)
                index_np = idx[numpy.argmax(counts)]
                moda_longitudes = lista_longitudes_previas[index_np]

                #print("MODA_L:", moda_longitudes)

            except NameError:
                #print("well, it WASN'T defined after all! (MODA_L)")
                moda_longitudes = 0
            else:
                #print("sure, it was defined. (MODA_L)")
                moda_longitudes = moda_longitudes
            # Fin excepción
            rango_longitudes = sorted(lista_longitudes_previas)[len(lista_longitudes_previas)-1] - sorted(lista_longitudes_previas)[0]
            #print("MediaL: ", media_longitudes)
            #print("MedianaL: ", mediana_longitudes)
            #print("ModaL: ", moda_longitudes)
            #print("RangoL: ", rango_longitudes)

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
            if tipo == 'cluster':

                ###################
                # ANÁLISIS de TEXTOS x HILO
                ###################
                from procesadoGeneral import tokenizado
                from procesadoGeneral import enraizado
                from procesadoGeneral import postag
                from procesadoGeneral import cluster

                #
                # ANÁLISIS de los TEXTOS de un HILO
                #
                # var_token = tokenizado(textos_mensajes.strip())
                # print('TOKENIZADO HILOS')
                # print('TOKENIZADO(', n_mensajes, '): ', var_token)

                # var_raiz = enraizado()
                # print('RAICES HILOS')
                # print('RAICES: ', var_raiz)

                # print('POSTAG HILO(', n_hilos, '): ')
                # var_pos = postag(textos_mensajes.strip())
                # print('POSTAG HILO(', n_hilos, '): ', var_pos)

                # var_clu = cluster()
                # print('CLUSTER: ', var_clu)

                # exit(999)

                #
                # ANÁLISIS de TITULO/S DE LOS TEXTOS de un HILO ????????????????????????????????????????????????????????????
                #

                #
                # TOPIC MODELLING, t-SNE, Spectral Clusterin de un HILO ????????????????????????????????????????????????????
                #

                hilo = {
                    # BASE #
                    # MENSAJES #
                    'Asignatura': int(mensaje['Asignatura']),
                    #'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
                    'Caracteres foro': mensaje['Caracteres foro'],
                    #'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'],
                    'Caracteres hilo': mensaje['Caracteres hilo'],
                    'N autores': n_autores,
                    'N foro': n_foros,
                    'N hilo': n_hilos,
                    'N mensajes': n_mensajes,
                    'N auto-respuestas': n_auto_respuestas,
                    'N subhilos': n_subhilos,
                    # MENSAJES x SUBHILO
                    'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
                    #    'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                    #    'Remitente': id_autor, 'Autor': autor,
                    # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                    #    'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
                    # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                    #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                    'Date': abs(datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                        '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
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
                    #'Título mensaje': titulos_mensajes,
                    'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los títulos
                    #'Texto mensaje': textos_mensajes.strip(),
                    'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los textos
                    # ANÁLISIS de TEXTO
                    # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                    #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                    #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                    "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
                    # .SnowballStemmer("spanish").stem,
                    #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                    #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                    'nr': nr, 'nrd': nrd,
                    # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                    #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                    #'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                    # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
                    'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                    'Curso': int(curso),
                }
            elif tipo == 'clasificador':
                hilo = {
                    # BASE #
                    # MENSAJES #
                    'Clase': clase_hilo,
                    'Asignatura': int(mensaje['Asignatura']),
                    #'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
                    'Caracteres foro': mensaje['Caracteres foro'],
                    #'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'],
                    'Caracteres hilo': mensaje['Caracteres hilo'],
                    'N autores': n_autores,
                    'N foro': n_foros,
                    'N hilo': n_hilos,
                    'N mensajes': n_mensajes,
                    'N auto-respuestas': n_auto_respuestas,
                    'N subhilos': n_subhilos,
                    # MENSAJES x SUBHILO
                    'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
                    #    'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                    #    'Remitente': id_autor, 'Autor': autor,
                    # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                    #    'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
                    # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                    #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                    'Date': abs(datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                        '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
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
                    #'Título mensaje': titulos_mensajes,
                    'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los títulos
                    #'Texto mensaje': textos_mensajes.strip(),
                    'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los textos
                    # ANÁLISIS de TEXTO
                    # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                    #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                    #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                    "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
                    # .SnowballStemmer("spanish").stem,
                    #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                    #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                    'nr': nr, 'nrd': nrd,
                    # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                    #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                    #'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                    # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
                    'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                    'Curso': int(curso),
                }
            else:  # General
                hilo = {
                    # BASE #
                    # MENSAJES #
                    'Asignatura': mensaje['Asignatura'],
                    'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
                    'Caracteres foro': mensaje['Caracteres foro'],
                    'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'], 'Caracteres hilo': mensaje['Caracteres hilo'],
                    'N autores': n_autores,
                    'N foro': n_foros,
                    'N hilo': n_hilos,
                    'N mensajes': n_mensajes,
                    'N auto-respuestas': n_auto_respuestas,
                    'N subhilos': n_subhilos,
                    # MENSAJES x SUBHILO
                    'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
                    #    'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
                    'Remitente': autores_previos[0], 'Autor': autores_previos[0],
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
                    'Título mensaje': titulos_mensajes,
                    'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los títulos
                    'Texto mensaje': textos_mensajes.strip(),
                    'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los textos
                    # ANÁLISIS de TEXTO
                    # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                    #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                    #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                    "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
                    # .SnowballStemmer("spanish").stem,
                    #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                    #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                    'nr': nr, 'nrd': nrd,
                    # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                    #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                    #'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                    # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
                    'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                    'Curso': int(curso),
                }

            # INICIALIZAR AUTORES #
            autores_previos = []
            # INICIALIZAR CONTADORES HILO #
            longitud = 0
            n_mensajes = 0
            distancia = 0

            # ACUMULADOS ANÁLISIS TEXTO
            lc = 0
            nt = 0
            nf = 0
            np = 0
            ns = 0
            nr = 0
            nrd = 0
            nn = 0
            nnd = 0
            nv = 0
            nvd = 0
            # ACUMULADOS ADJUNTOS
            n_adjs = 0
            t_adj = 0
            n_emojis = 0
            n_links = 0

            # AÑADIR HILO #
            hilos.append(hilo)

        ########################
        # CIERRE DEL ARRAY HILOS
        ########################
        # print(hilos)

    ########################
    # Derfinición ULTIMO HILO
    ########################
    # hilo = [tit_hilo, id_hilo, dia_semana, fecha, n_mensajes, n_autores, n_subhilos, n_auto_respuestas, longitud, distancia, longitud_media, distancia_media]
    if tipo == 'cluster':

        ###################
        # ANÁLISIS de TEXTOS x HILO
        ###################
        from procesadoGeneral import tokenizado
        from procesadoGeneral import enraizado
        from procesadoGeneral import postag
        from procesadoGeneral import cluster

        #
        # ANÁLISIS de los TEXTOS de un HILO
        #
        # var_token = tokenizado(textos_mensajes.strip())
        # print('TOKENIZADO HILOS')
        # print('TOKENIZADO(', n_mensajes, '): ', var_token)

        # var_raiz = enraizado()
        # print('RAICES HILOS')
        # print('RAICES: ', var_raiz)

        # print('POSTAG HILO(', n_hilos, '): ')
        # var_pos = postag(textos_mensajes.strip())
        # print('POSTAG HILO(', n_hilos, '): ', var_pos)

        # var_clu = cluster()
        # print('CLUSTER: ', var_clu)

        # exit(999)

        #
        # ANÁLISIS de TITULO/S DE LOS TEXTOS de un HILO ????????????????????????????????????????????????????????????
        #

        #
        # TOPIC MODELLING, t-SNE, Spectral Clusterin de un HILO ????????????????????????????????????????????????????
        #

        hilo = {
            # BASE #
            # MENSAJES #
            'Asignatura': int(mensaje['Asignatura']),
            # 'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
            'Caracteres foro': mensaje['Caracteres foro'],
            # 'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'],
            'Caracteres hilo': mensaje['Caracteres hilo'],
            'N autores': n_autores,
            'N foro': n_foros,
            'N hilo': n_hilos,
            'N mensajes': n_mensajes,
            'N auto-respuestas': n_auto_respuestas,
            'N subhilos': n_subhilos,
            # MENSAJES x SUBHILO
            'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
            #    'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
            #    'Remitente': id_autor, 'Autor': autor,
            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
            #    'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
            #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
            'Date': abs(datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
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
            # 'Título mensaje': titulos_mensajes,
            'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,
        # Espacios en blanco de separacion de los títulos
            # 'Texto mensaje': textos_mensajes.strip(),
            'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,
        # Espacios en blanco de separacion de los textos
            # ANÁLISIS de TEXTO
            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
            #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
            #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
            "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
            # .SnowballStemmer("spanish").stem,
            #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
            #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
            'nr': nr, 'nrd': nrd,
            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
            #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
            # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
            # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
            'Curso': int(curso),
        }
    elif tipo == 'clasificador':
        hilo = {
            # BASE #
            # MENSAJES #
            'Clase': clase_hilo,
            'Asignatura': int(mensaje['Asignatura']),
            #'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
            'Caracteres foro': mensaje['Caracteres foro'],
            #'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'],
            'Caracteres hilo': mensaje['Caracteres hilo'],
            'N autores': n_autores,
            'N foro': n_foros,
            'N hilo': n_hilos,
            'N mensajes': n_mensajes,
            'N auto-respuestas': n_auto_respuestas,
            'N subhilos': n_subhilos,
            # MENSAJES x SUBHILO
            'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
            #    'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
            #    'Remitente': id_autor, 'Autor': autor,
            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
            #    'Inicial': inicial, 'Respuesta': respuesta, 'Auto-respuesta': auto_respuesta, 'Terminal': terminal,
            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
            #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
            'Date': abs(datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
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
            #'Título mensaje': titulos_mensajes,
            'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los títulos
            #'Texto mensaje': textos_mensajes.strip(),
            'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los textos
            # ANÁLISIS de TEXTO
            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
            #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
            #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
            "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
            # .SnowballStemmer("spanish").stem,
            #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
            #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
            'nr': nr, 'nrd': nrd,
            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
            #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
            #'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
            # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
            'Curso': int(curso),
        }
    else:  # General
        hilo = {
            # BASE #
            # MENSAJES #
            'Asignatura': mensaje['Asignatura'],
            'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
            'Caracteres foro': mensaje['Caracteres foro'],
            'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'], 'Caracteres hilo': mensaje['Caracteres hilo'],
            'N autores': n_autores,
            'N foro': n_foros,
            'N hilo': n_hilos,
            'N mensajes': n_mensajes,
            'N auto-respuestas': n_auto_respuestas,
            'N subhilos': n_subhilos,
            # MENSAJES x SUBHILO
            'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
            #    'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
            'Remitente': autores_previos[0], 'Autor': autores_previos[0],
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
            'Título mensaje': titulos_mensajes,
            'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,
        # Espacios en blanco de separacion de los títulos
            'Texto mensaje': textos_mensajes.strip(),
            'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,
        # Espacios en blanco de separacion de los textos
            # ANÁLISIS de TEXTO
            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
            #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
            #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
            "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
            # .SnowballStemmer("spanish").stem,
            #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
            #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
            'nr': nr, 'nrd': nrd,
            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
            #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
            # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
            # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
            'Curso': int(curso),
        }
    # AÑADIR ULTIMO HILO #
    hilos.append(hilo)

    return hilos


## PROCESADO USUARIOS ##
def generar_autores(mensajes, hilos, campo, curso_asig, tipo, clase=''):
    global autores

    print('#######')
    print('AUTORES')
    print('#######')
    autores = []
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
        #print("well, it WASN'T defined after all!")
        id_autor_anterior = 0
        cambia_autor = 1
    else:
        #print("sure, it was defined.")
        id_autoranterior = 0
        cambia_autor = 1
    # Fin excepción

    # Variables Globales
    autores_previos = []
    hilos_previos = []
    foros_previos = []
    asignaturas_previas = []
    autor_previo = 0
    nombre_autor_previo = ''
    foro_previo = 0
    hilo_previo = 0
    clase_hilo = ''
    asignatura_previa = 0

    # Totales
    n_mensajes = 0
    n_autores = 0
    n_hilos = 0
    n_subhilos = 0
    n_foros = 0
    n_asig = 0
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

    # ACUMULADOS ANÁLISIS TEXTO
    lc = 0
    nt = 0
    nf = 0
    np = 0
    ns = 0
    nr = 0
    nrd = 0
    nn = 0
    nnd = 0
    nv = 0
    nvd = 0
    # ACUMULADOS ADJUNTOS
    n_adjs = 0
    t_adj = 0
    n_emojis = 0
    n_links = 0

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

        # X AUTOR
        id_autor = mensaje[campo]
        nombre_autor = mensaje['Autor']
        if id_autor != autor_previo:

            # SI ES EL PRIMER MENSAJE DEL PRIMER AUTOR INICIAL
            if autor_previo == 0:
                # Actualiza el valor para poder usar el ID
                autor_previo = id_autor
                nombre_autor_previo = nombre_autor

            # SI ES EL PRIMER MENSAJE DE UN AUTOR INTERMEDIO
            # Y SI FUE EL ULTIMO MENSAJE DEL AUTOR ANTERIOR
            # Y SI ES EL UNICO MENSAJE DEL ULTIMO AUTOR
            # CONTABILIZA LAS VARIABLES DEL AUTOR PREVIO E INICIALIZA LAS DEL ACTUAL
            else:
                # DISTANCIAS datetime.strptime(fecha + ' ' + hora, "%d/%m/%Y %H:%M:%S")
                #
                #from datetime import datetime
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
                import numpy as numpy

                # TIEMPO
                # PH
                # CALCULAR TIEMPOS #
                if lista_tiempos_previos_ph != []:
                    # PH
                    media_tiempos_ph = numpy.mean(lista_tiempos_previos_ph)
                    mediana_tiempos_ph = numpy.median(lista_tiempos_previos_ph)
                    max_tiempos_ph = max(lista_tiempos_previos_ph)
                    min_tiempos_ph = min(lista_tiempos_previos_ph)
                    (_, idx, counts) = numpy.unique(lista_tiempos_previos_ph, return_index=True, return_counts=True)
                    index_np = idx[numpy.argmax(counts)]
                    moda_tiempos_ph = lista_tiempos_previos_ph[index_np]
                    rango_tiempos_ph = sorted(lista_tiempos_previos_ph)[len(lista_tiempos_previos_ph)-1] - sorted(lista_tiempos_previos_ph)[0]
                if lista_tiempos_previos_as != []:
                    # AS
                    media_tiempos_as = numpy.mean(lista_tiempos_previos_as)
                    mediana_tiempos_as = numpy.median(lista_tiempos_previos_as)
                    max_tiempos_as = max(lista_tiempos_previos_as)
                    min_tiempos_as = min(lista_tiempos_previos_as)
                    (_, idx, counts) = numpy.unique(lista_tiempos_previos_as, return_index=True, return_counts=True)
                    index_np = idx[numpy.argmax(counts)]
                    moda_tiempos_as = lista_tiempos_previos_as[index_np]
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
                if tipo == 'cluster':

                    ###################
                    # ANÁLISIS de TEXTOS x AUTOR
                    ###################
                    from procesadoGeneral import tokenizado
                    from procesadoGeneral import enraizado
                    from procesadoGeneral import postag
                    from procesadoGeneral import cluster

                    #
                    # ANÁLISIS de los TEXTOS de un AUTOR
                    #
                    # var_token = tokenizado(textos_mensajes.strip())
                    # print('TOKENIZADO AUTOR')
                    # print('TOKENIZADO AUTOR(', n_mensajes, '): ', var_token)

                    # var_raiz = enraizado()
                    # print('RAICES AUTOR')
                    # print('RAICES AUTOR: ', var_raiz)

                    # print('POSTAG AUTOR(', n_autores, '): ')
                    # var_pos = postag(textos_mensajes.strip())
                    # print('POSTAG AUTOR(', n_autores, '): ', var_pos)

                    # var_clu = cluster()
                    # print('CLUSTER: ', var_clu)

                    # exit(999)

                    #
                    # ANÁLISIS de TITULO/S DE LOS TEXTOS de un HILO ????????????????????????????????????????????????????????????
                    #

                    #
                    # TOPIC MODELLING, t-SNE, Spectral Clusterin de un HILO ????????????????????????????????????????????????????
                    #

                    autor = {
                        # BASE #
                        # MENSAJES #
                        'Asignatura': int(mensaje['Asignatura']),
                        # 'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
                        # 'Caracteres foro': mensaje['Caracteres foro'],
                        # 'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'], 'Caracteres hilo': mensaje['Caracteres hilo'],
                        'N autores': n_autores,
                        'N asignaturas': n_asig,
                        'N foros': n_foros,
                        'N hilos': n_hilos,
                        'N mensajes': n_mensajes,
                        #'N auto-respuestas': n_auto_respuestas,
                        #'N subhilos': n_subhilos,
                        # MENSAJES x SUBHILO
                        #'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
                        #'Mensaje': mensaje['Mensaje'], 'Responde a': mensaje['Responde a'],
                        # AUTOR ANTERIOR
                        'Remitente': autor_previo, 'Autor': id_autor,
                        # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
                        'Iniciales': n_iniciales, 'Respuestas': n_respuestas,
                        'Auto-respuestas': n_auto_respuestas, 'Terminales': n_terminales,
                        # DISTANCIAS Padre-Hijo Antecesor-Sucesor
                        #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
                        'Date': abs(datetime.strptime(date, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                            '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
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
                        #'Título mensaje': titulos_mensajes,
                        'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los títulos
                        #'Texto mensaje': textos_mensajes.strip(),
                        'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los textos
                        # ANÁLISIS de TEXTO
                        # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                        #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                        #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                        "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
                        # .SnowballStemmer("spanish").stem,
                        #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                        #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                        'nr': nr, 'nrd': nrd,
                        # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                        #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                        #'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                        # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
                        'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                        'Curso': int(curso),
                    }
                elif tipo == 'clasificador':
                    if isinstance(clase[index], str): #numpy.isnan(clase[len(mensajes)]):
                        clase_hilo = clase[index]
                    autor = {}
                else:  # General
                    autor = {
                        # BASE #
                        # MENSAJES #
                        'Asignatura': mensaje['Asignatura'],
                        # 'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
                        # 'Caracteres foro': mensaje['Caracteres foro'],
                        # 'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'], 'Caracteres hilo': mensaje['Caracteres hilo'],
                        'N autores': n_autores,
                        'N asignaturas': n_asig,
                        'N foros': n_foros,
                        'N hilos': n_hilos,
                        'N mensajes': n_mensajes,
                        # 'N auto-respuestas': n_auto_respuestas,
                        # 'N subhilos': n_subhilos,
                        # MENSAJES x SUBHILO
                        # 'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
                        # 'Mensaje': mensaje['Mensaje'], 'Responde a': mensaje['Responde a'],
                        # AUTOR ANTERIOR
                        'Remitente': autor_previo, 'Autor': nombre_autor_previo,
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
                        # 'MediaL': media_longitudes,
                        # 'MedianaL': mediana_longitudes,
                        # 'ModaL': moda_longitudes,
                        # 'RangoL': rango_longitudes,
                        'Título mensaje': titulos_mensajes,
                        'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los títulos
                        'Texto mensaje': textos_mensajes.strip(),
                        'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,  # Espacios en blanco de separacion de los textos
                        # ANÁLISIS de TEXTO
                        # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
                        #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
                        #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
                        "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
                        # .SnowballStemmer("spanish").stem,
                        #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
                        #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
                        'nr': nr, 'nrd': nrd,
                        # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
                        #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
                        #    'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
                        # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
                        'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
                        'Curso': int(curso),
                    }

                # PRIMER MENSAJE AUTOR #
                # INICIALIZAR MENSAJES #
                n_mensajes = 0
                # INICIALIZAR AUTORES #
                autores_previos = []
                n_autores += 1
                autor_previo = id_autor
                nombre_autor_previo = nombre_autor
                # INICIALIZAR HILOS #
                hilos_previos = []
                # INICIALIZAR FOROS #
                foros_previos = []
                # INICIALIZAR ASIGNATURAS #
                asignaturas_previas = []

                # INICIALIZAR CONTADORES AUTOR #
                n_foros = 0
                n_hilos = 0
                n_asig = 0

                # INICIADOR, RESPONDEDOR Y TERMINADOR
                n_iniciales = 0
                n_respuestas = 0
                n_auto_respuestas = 0
                n_terminales = 0

                # INICIALIZAR DISTANCIAS/TIEMPOS
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

                # INICIALIZAR TAMAÑO/LONGITUD
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
                #
                # ACUMULADOS ANÁLISIS TEXTO
                lc = 0
                nt = 0
                nf = 0
                np = 0
                ns = 0
                nr = 0
                nrd = 0
                nn = 0
                nnd = 0
                nv = 0
                nvd = 0
                # ACUMULADOS ADJUNTOS
                n_adjs = 0
                t_adj = 0
                n_emojis = 0
                n_links = 0
                #
                # TEXTOS
                titulos_mensajes = mensaje['Título mensaje']
                textos_mensajes = mensaje['Texto mensaje']

                # AÑADIR AUTOR #
                autores.append(autor)

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
        #from datetime import datetime

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
            datetime.strptime(date, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds()

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
        # ACUMULADOS ANÁLISIS TEXTO #
        lc += mensaje['lc']
        nt += mensaje['nt']
        nf += mensaje['nf']
        np += mensaje['np']
        ns += mensaje['ns']
        nr += mensaje['nr']
        nrd += mensaje['nrd']
        #nn += mensaje['nn']
        #nnd += mensaje['nnd']
        #nv += mensaje['nv']
        #nvd += mensaje['nvd']
        # ACUMULADOS ADJUNTOS #
        n_adjs += mensaje['Adjuntos']
        t_adj += mensaje['Tamaño adjuntos']
        n_emojis += mensaje['Emojis']
        n_links += mensaje['Links']
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
        foro = mensaje['Foro']
        # FOROS DISTINTOS #
        if foro not in foros_previos:
            foros_previos.append(foro)
            n_foros += 1
        if foro != foro_previo:
            foro_previo = foro

        # X ASIGNATURA
        asignatura = mensaje['Asignatura']
        # ASIGNATURAS DISTINTAS #
        if asignatura not in asignaturas_previas:
            asignaturas_previas.append(hilo)
        if asignatura != asignatura_previa:
            n_asig += 1
            asignatura_previa = asignatura

    ########################
    # CIERRE DEL ARRAY AUTORES
    ########################
    # print(autores)

    ########################
    # Derfinición ULTIMO AUTOR
    ########################
    # autor = [tit_hilo, id_hilo, dia_semana, fecha, n_mensajes, n_autores, n_subhilos, n_auto_respuestas, longitud, distancia, longitud_media, distancia_media]
    if tipo == 'cluster':

        ###################
        # ANÁLISIS de TEXTOS x AUTOR
        ###################
        from procesadoGeneral import tokenizado
        from procesadoGeneral import enraizado
        from procesadoGeneral import postag
        from procesadoGeneral import cluster

        #
        # ANÁLISIS de los TEXTOS de un AUTOR
        #
        # var_token = tokenizado(textos_mensajes.strip())
        # print('TOKENIZADO AUTOR')
        # print('TOKENIZADO AUTOR(', n_mensajes, '): ', var_token)

        # var_raiz = enraizado()
        # print('RAICES AUTOR')
        # print('RAICES AUTOR: ', var_raiz)

        # print('POSTAG AUTOR(', n_autores, '): ')
        # var_pos = postag(textos_mensajes.strip())
        # print('POSTAG AUTOR(', n_autores, '): ', var_pos)

        # var_clu = cluster()
        # print('CLUSTER: ', var_clu)

        # exit(999)

        #
        # ANÁLISIS de TITULO/S DE LOS TEXTOS de un HILO ????????????????????????????????????????????????????????????
        #

        #
        # TOPIC MODELLING, t-SNE, Spectral Clusterin de un HILO ????????????????????????????????????????????????????
        #

        autor = {
            # BASE #
            # MENSAJES #
            'Asignatura': int(mensaje['Asignatura']),
            # 'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
            # 'Caracteres foro': mensaje['Caracteres foro'],
            # 'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'], 'Caracteres hilo': mensaje['Caracteres hilo'],
            'N autores': n_autores,
            'N asignaturas': n_asig,
            'N foros': n_foros,
            'N hilos': n_hilos,
            'N mensajes': n_mensajes,
            # 'N auto-respuestas': n_auto_respuestas,
            # 'N subhilos': n_subhilos,
            # MENSAJES x SUBHILO
            # 'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
            # 'Mensaje': mensaje['Mensaje'], 'Responde a': mensaje['Responde a'],
            # AUTOR ANTERIOR
            'Remitente': autor_previo, 'Autor': id_autor,
            # TIPO INICIAL, TERMINAL, RESPUESTA Y AUTO-RESPUESTA
            'Iniciales': n_iniciales, 'Respuestas': n_respuestas,
            'Auto-respuestas': n_auto_respuestas, 'Terminales': n_terminales,
            # DISTANCIAS Padre-Hijo Antecesor-Sucesor
            #    'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
            'Date': abs(datetime.strptime(date, "%d/%m/%Y %H:%M:%S") - datetime.strptime(
                '01/09/' + curso + ' 00:00:00', "%d/%m/%Y %H:%M:%S")).total_seconds(),
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
            # 'MediaL': media_longitudes,
            # 'MedianaL': mediana_longitudes,
            # 'ModaL': moda_longitudes,
            # 'RangoL': rango_longitudes,
            # 'Título mensaje': titulos_mensajes,
            'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,
        # Espacios en blanco de separacion de los títulos
            # 'Texto mensaje': textos_mensajes.strip(),
            'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,
        # Espacios en blanco de separacion de los textos
            # ANÁLISIS de TEXTO
            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
            #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
            #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
            "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
            # .SnowballStemmer("spanish").stem,
            #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
            #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
            'nr': nr, 'nrd': nrd,
            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
            #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
            # 'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
            # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
            'Curso': int(curso),
        }
    elif tipo == 'clasificador':
        if isinstance(clase[index], str):  # numpy.isnan(clase[len(mensajes)]):
            clase_hilo = clase[index]
        autor = {}
    else:  # General
        autor = {
            # BASE #
            # MENSAJES #
            'Asignatura': mensaje['Asignatura'],
            # 'Foro': mensaje['Foro'], 'Nombre foro': mensaje['Nombre foro'],
            # 'Caracteres foro': mensaje['Caracteres foro'],
            # 'Hilo': mensaje['Hilo'], 'Título': mensaje['Título'], 'Caracteres hilo': mensaje['Caracteres hilo'],
            'N autores': n_autores,
            'N asignaturas': n_asig,
            'N foros': n_foros,
            'N hilos': n_hilos,
            'N mensajes': n_mensajes,
            # 'N auto-respuestas': n_auto_respuestas,
            # 'N subhilos': n_subhilos,
            # MENSAJES x SUBHILO
            # 'Mensajes medios por subhilo': n_mensajes_medio_subhilo,
            # 'Mensaje': mensaje['Mensaje'], 'Responde a': mensaje['Responde a'],
            # AUTOR ANTERIOR
            'Remitente': autor_previo, 'Autor': nombre_autor_previo,
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
            # 'MediaL': media_longitudes,
            # 'MedianaL': mediana_longitudes,
            # 'ModaL': moda_longitudes,
            # 'RangoL': rango_longitudes,
            'Título mensaje': titulos_mensajes,
            'Caracteres títulos mensajes': len(titulos_mensajes) - n_mensajes - 1,
        # Espacios en blanco de separacion de los títulos
            'Texto mensaje': textos_mensajes.strip(),
            'Caracteres texto mensajes': len(textos_mensajes) - n_mensajes - 1,
        # Espacios en blanco de separacion de los textos
            # ANÁLISIS de TEXTO
            # 'nltk.tokenize.sent_tokenize', .corpus.stopwords,
            #    'Tokens': var_token,  # {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero de stopwords}
            #    "lc": var_token.get('lc'), 'nt': var_token.get('nt'), 'nf': var_token.get('nf'), 'np': var_token.get('np'), 'ns': var_token.get('ns'),
            "lc": lc, 'nt': nt, 'nf': nf, 'np': np, 'ns': ns,
            # .SnowballStemmer("spanish").stem,
            #    'Raices': var_raiz,  # {'nr': numero_raices, 'nrd': numero_raices_distintas(Cantidad de información)}
            #    'nr': var_raiz.get('nr'), 'nrd': var_raiz.get('nrd'),
            'nr': nr, 'nrd': nrd,
            # 'nltk.tokenize.word_tokenize, .corpus.stopwords, .SnowballStemmer("spanish").stem, .tag.stanford',
            #    'Postag': var_pos,  # {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}
            #    'nn': var_pos.get('nn'), 'nv': var_pos.get('nv'), 'nnd': var_pos.get('nnd'), 'nvd': var_pos.get('nvd'),
            # PoS: # 'nn': nn, 'nv': nv, 'nnd': nnd, 'nvd': nvd,
            'Adjuntos': n_adjs, 'Tamaño adjuntos': t_adj, 'Emojis': n_emojis, 'Links': n_links,
            'Curso': int(curso),
        }
    # AÑADIR ULTIMO AUTOR #
    autores.append(autor)

    return autores

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

    return autores


## PROCESADO FOROS ##
def generar_foros(mensajes, hilos, autores, campo, curso_asig, tipo):
    global foros

    print('#######')
    print('FOROS')
    print('#######')
    foros = []
    curso = curso_asig
    #

    # Variables Globales
    foro = {}
    # Interruptores
    foro_previo = 0

    # Totales
    n_foros = 0

    # PARA CADA MENSAJE #
    for index, mensaje in enumerate(mensajes):
        if mensaje['Foro'] != foro_previo:
            n_foros += 1
            foro_previo = mensaje['Foro']

        ########################
        # Derfinición de FORO
        ########################
        # foro=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor, autor, dia_semana, fecha, tit_mensaje, texto]
        if tipo == 'excel':
            foro = {}
        elif tipo == 'cluster':
            foro = {}
        elif tipo == 'clasificador':
            foro = {}
        else:
            foro = {}

        foros.append(foro)

        ########################
        # CIERRE DEL ARRAY FOROS
        ########################
        # print(foros)

    ########################
    # Derfinición ULTIMO FORO
    ########################
    # foro=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor, autor, dia_semana, fecha, tit_mensaje, texto]
    if tipo == 'excel':
        foro = {}
    elif tipo == 'cluster':
        foro = {}
    elif tipo == 'clasificador':
        foro = {}
    else:
        foro = {}

    return foros


## PROCESADO ASIGNATURAS ##
def generar_asignaturas(mensajes, hilos, autores, foros, campo, curso_asig, tipo):
    global asignaturas

    print('#######')
    print('ASIGNATURAS')
    print('#######')
    asignaturas = []
    curso = curso_asig
    #

    # Variables Globales
    asignatura = {}
    # Interruptores
    asig_previa = 0

    # Totales
    n_asig = 0

    # PARA CADA MENSAJE #
    for index, mensaje in enumerate(mensajes):
        if mensaje['Asignatura'] != asig_previa:
            n_asig += 1
            asig_previa = mensaje['Asignatura']

        ########################
        # Derfinición de ASIGNATURA
        ########################
        # asignatura=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor, autor, dia_semana, fecha, tit_mensaje, texto]
        if tipo == 'excel':
            asignatura = {}
        elif tipo == 'cluster':
            asignatura = {}
        elif tipo == 'clasificador':
            asignatura = {}
        else:
            asignatura = {}

        asignaturas.append(asignatura)

        ########################
        # CIERRE DEL ARRAY ASIGNATURAS
        ########################
        # print(asignaturas)

    ########################
    # Derfinición ULTIMA ASIGNATURA
    ########################
    # asignatura=[tit_hilo, id_hilo, id_mensaje, id_ref_mensaje, id_autor, autor, dia_semana, fecha, tit_mensaje, texto]
    if tipo == 'excel':
        asignatura = {}
    elif tipo == 'cluster':
        asignatura = {}
    elif tipo == 'clasificador':
        asignatura = {}
    else:
        asignatura = {}

    asignaturas.append(asignatura)

    return asignaturas
