import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger, StanfordTagger

from nltk import ne_chunk, pos_tag

# E/S
import os

import json

import re

# Módulos propios
import procesadoMensaje

# VARIABLES GLOBALES
#######################
data = "All work and no play makes jack dull boy. All work and no play makes jack a dull boy."
mensaje = " Me cago en en tu puta madre 0.Mierda para tu puta madre 1. Mierda para tu puta madre "
"2.Mierda para tu puta madre 3. Mierda para tu puta madre 4.Caca de la vaca, para el resto. 5. Final"
instancias = []

tokens = []
sentencias = []
# stop_words = []
palabras = []
lista_palabras = []
raices = []
lista_raices = []
mensajes = []
tags = []

nombres = []

longitud_media_tokens = 0.0
longitud_media_frases = 0.0

synonyms = []
antonyms = []

########################
## CALSES MENSAJE     ##
########################
id_foro = 16735771
nombreForo = 'nombreForo'
id_asig = 1234567
tit_hilo = 'títuloHilo'
id_hilo = 33078833
id_mensaje = '33078833_1'
id_ref_mensaje = ''
id_autor = 0
autor = 'Nombre Apellidos'
dia_semana = 'Lunes'
fecha = '00/00/00'
hora = '00:00:00'
tit_mensaje = 'título mensaje'
texto = 'texto mensaje'
caracteres = 0

mensaje1 = {'Foro': 16735771, 'ForoN': 'nombreForo', 'Asignatura': 1234567, 'Título': 'títuloHilo',
            'Hilo': 33078833,
            'Mensaje': '33078833_1', 'Responde a': '',
            'Remitente': 12345678, 'Autor': 'Nombre Apellidos', 'Día': 'Lunes', 'Fecha': '00/00/00', 'Hora': '00:00:00',
            'Título mensaje': 'título mensaje',
            'Texto mensaje': 'texto mensaje'.strip(), 'Caracteres mensaje': len('texto mensaje')
            }


# Obejto de intercambio
# Formato Mensajes de los foros
class Mensaje(object):
    id_foro = 16735771
    nombreForo = 'nombreForo'
    id_asig = 1234567
    tit_hilo = 'títuloHilo'
    id_hilo = 33078833
    id_mensaje = '33078833_1'
    id_ref_mensaje = ''
    id_autor = 0
    autor = 'Nombre Apellidos'
    dia_semana = 'Lunes'
    fecha = '00/00/00'
    hora = '00:00:00'
    tit_mensaje = 'título mensaje'
    texto = 'texto mensaje'
    caracteres = 0
    mensaje = {'Foro': id_foro, 'ForoN': nombreForo, 'Asignatura': id_asig, 'Título': tit_hilo,
               'Hilo': id_hilo,
               'Mensaje': id_mensaje, 'Responde a': id_ref_mensaje,
               'Remitente': id_autor, 'Autor': autor, 'Día': dia_semana, 'Fecha': fecha, 'Hora': hora,
               'Título mensaje': tit_mensaje,
               'Texto mensaje': texto.strip(), 'Caracteres mensaje': len(texto)
               }

    def __init__(self, mensaje):
        self.id_foro = mensaje["Foro"]
        self.nombreForo = mensaje["ForoN"]
        self.id_asig = mensaje["Asignatura"]
        self.tit_hilo = mensaje["Título"]
        self.id_hilo = mensaje["Hilo"]
        self.id_mensaje = mensaje["Mensaje"]
        self.id_ref_mensaje = mensaje["Responde a"]
        self.id_autor = mensaje["Remitente"]
        self.autor = mensaje["Autor"]
        self.dia_semana = mensaje["Día"]
        self.fecha = mensaje["Fecha"]
        self.hora = mensaje["Hora"]
        self.tit_mensaje = mensaje["Título mensaje"]
        self.texto = mensaje["Caracteres mensaje"]

        print(mensaje)

        return None

    def asignarmensaje(self, mensaje):
        self.id_foro = mensaje["Foro"]
        self.nombreForo = mensaje["ForoN"]
        self.id_asig = mensaje["Asignatura"]
        self.tit_hilo = mensaje["Título"]
        self.id_hilo = mensaje["Hilo"]
        self.id_mensaje = mensaje["Mensaje"]
        self.id_ref_mensaje = mensaje["Responde a"]
        self.id_autor = mensaje["Remitente"]
        self.autor = mensaje["Autor"]
        self.dia_semana = mensaje["Día"]
        self.fecha = mensaje["Fecha"]
        self.hora = mensaje["Hora"]
        self.tit_mensaje = mensaje["Título mensaje"]
        self.texto = mensaje["Caracteres mensaje"]

        print(self.id_foro, self.nombreForo, self.id_asig, self.tit_hilo, self.id_hilo, self.id_mensaje,
              self.id_ref_mensaje, self.id_autor, self.autor, self.dia_semana, self.fecha, self.hora, self.tit_mensaje,
              self.texto)

        pass


# Obejto de intercambio
# Formato Características de los Mensajes de los foros
class Caracteristicas(object):
    pass


# Obejto de intercambio
# Análisis de Características de los Mensajes de los foros
class Analisis(object):
    pass


# Obejto de intercambio
# Clasificación x Características de los Mensajes de los foros
class Clasificacion(object):
    pass


# Obejto de intercambio
# Clustering x Características de los Mensajes de los foros
class Clustering(object):
    pass


# OBJETOS GLOBALES
########################
# Objeto
msg = Mensaje(mensaje1)
msg.asignarmensaje(mensaje1)

# DIRECTORIO ANOTADORES #
########################
# de modelos
# de taggers java
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

# Objeto RAIZ
########################
ss = SnowballStemmer('spanish')

# Obejto POSTAGGING
########################
# Lectura desde ficheros
# del tagger java Stanford
# about the tagger: http://nlp.stanford.edu/software/tagger.shtml
# about the tagset: nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html
spanish_postagger = StanfordPOSTagger(os.path.join(dir_path, 'standford/models/spanish.tagger'),
                                      os.path.join(dir_path, 'standford/stanford-postagger.jar'), encoding='utf8')


########################
# PROCESADO Y ANALISIS
########################

# STOPWORDS
########################
# Array de stopwords personalizado
stop_words = stopwords.words('spanish')

# Añadir signos de puntuación
stop_words.append('.')
stop_words.append(':')
stop_words.append(',')
stop_words.append(';')
stop_words.append('-')
stop_words.append('"')
stop_words.append('¡')
stop_words.append('!')
stop_words.append('¡')
stop_words.append('?')
stop_words.append('&')
stop_words.append('/')
stop_words.append('(')
stop_words.append(')')
stop_words.extend(
    ('¡', '¿', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
     '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'))


# ANONIMATO
########################
def anonimato(msj=mensaje, nombres=''):
    texto = msj

    #######################
    # Tratamiento TEXTO
    # Etiquetas: [(DATA|LINK|TWITGRAM|HASHTAG|MOVIL|EMAIL|DNI|ANONIMO)]
    #######################

    #
    # HTML ENTITY
    #
    # Busca entidades y los sustituye por el carácter equivalente
    import html as html

    # texto = html.unescape('Hola, cuando se concrete la fecha para &#39;APP-III&#39;, me dices, por mi parte, si me avisas con tiempo mejor&iexcl;&iexcl;  Saludos&iexcl;&iexcl;')
    texto = html.unescape(texto)

    #
    # ADJUNTOS (DOCUMENTOS, IMAGENES o EMOTICONOS)
    #
    import re

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
        # print('EMOJIS:', n_emojis)

    # Cuenta LINKS
    n_links = 0
    n_links_r = 0

    # Busca ADJUNTOS Y EMOJIS y los reemplaza por [DATA]
    if texto.find('[IMAGE:') != -1:
        # print('ADJUNTOS ENCONTRADOS: ', n_adjs)
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
        # print('LINKS ENCONTRADOS: ', n_links)

    # Busca links y los reemplaza por [LINK]
    n_links_r = len(re.findall(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        texto, re.M | re.I))
    if n_links_r != 0:
        # Reemplaza todos los LINKS (http) (sin ADJUNTOS y EMOJIS)
        texto = re.sub(
            r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
            ' [LINK] ', texto)
        # print('LINKS REEMPLAZADOS: ', n_links_r, texto)

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
        # print('EMAILS REEMPLAZADOS: ', n_emails_r, texto)
    # Busca TWITTER/TELEGRAM ID (@a) y los reemplaza por [                                                                                                                                                                                                                                                                                                ]
    n_twitters_r = len(re.findall(r'(^|[^@\w])@(\w{1,15})\b', texto, re.M | re.I))
    if n_twitters_r != 0:
        # Reemplaza todos los TWITTER/TELEGRAMS ID (@a) (sin EMAILS, LINKS, ADJUNTOS y EMOJIS)
        texto = re.sub(r'(^|[^@\w])@(\w{1,15})\b', ' [TWITGRAM] ', texto)
        # print('TWITTER/TELEGRAM ID REEMPLAZADOS: ', n_twitters_r, texto)

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
        # print('HASHTAGS REEMPLAZADOS: ', n_hashtags_r, texto)

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
        # print('MOVILES REEMPLAZADOS: ', n_moviles_r, texto)

    # Busca NUMEROS DE DNI o NIE y los reemplaza por ' [DNI] '
    # NIE: r'([X-Z]{1})([-]?)(\d{7})([-]?)([A-Z]{1})'
    # DNI: r'(\d{8})([-]?)([A-Z]{1})
    # r'(([x-zX-Z]{1})([-]?)(((\d){7,8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([-]?)([a-zA-Z]{1}))|(((\d){8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([a-zA-Z]{1})
    n_dnis_r = len(re.findall(
        r'(([x-zX-Z]{1})([-]?)(((\d){7,8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([-]?)([a-zA-Z]{1}))|(((\d){8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([a-zA-Z]{1})',
        texto, re.M | re.I))
    if n_dnis_r != 0:
        # Reemplaza todos los DNI (#a) (sin MOVILES HASHTAGS, TWITTER/TELEGRAMS, EMAILS, LINKS, ADJUNTOS y EMOJIS)
        texto = re.sub(
            r'(([x-zX-Z]{1})([-]?)(((\d){7,8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([-]?)([a-zA-Z]{1}))|(((\d){8}|((\d){1,2}\W{1,2}(\d){3}\W{1,2}(\d){3}))([-]?))([a-zA-Z]{1})',
            ' [DNI] ', texto)
        print('DNIS REEMPLAZADOS: ', n_dnis_r, texto)

    #
    # ABREVIATURAS DE NOMBRES
    #
    # Busca nombres y los sustituye por ' [ANONIMO] '

    # Busca Abreviaturas Nombres Mª, Mª., M.ª, Fco, Fco.
    #                    Apellidos Gª, Gª., G.ª
    #  y los reemplaza por ' ANONIMO ' ' Maria ' ' Francisco ' ' Garcia '
    if texto.find('Mª') != -1 or texto.find('Mª.') != -1 or texto.find('M.ª') != -1 or texto.find(
            'Gª') != -1 or texto.find('Gª.') != -1 or texto.find('G.ª') != -1:
        # or texto.find('Fco') != -1 or texto.find('Fco.') != -1 or texto.find('Fco') != -1:
        # Todas las abreviaturas
        n_abrev = len(re.findall(r'(M|m|G|g)[ .]*ª[ .]*', texto, re.M | re.I))
        # print('ABREVIATURAS ENCONTRADAS: ', n_abrev)
    # Busca ABREVIATURAS y las reemplaza por ' [ANONIMO] '
    n_abrev_r = len(re.findall(r'(M|m|G|g)[ .]*ª[ .]*', texto, re.M | re.I))
    if n_abrev_r != 0:
        # Reemplaza todos las ABREVIATURAS
        texto = re.sub(r'(M|m|G|g)[ .]*ª[ .]*', ' [ANONIMO] ', texto)
        # print('ABREVIATURAS REEMPLAZADAS: ', n_abrev_r, texto)

    #######################
    # FIN Tratamiento AMPLIADO de TEXTO \[(data|link|twitgram|anonimo|movil|email)\]
    #######################

    #######################
    # REVISAR NOMBRES AUTOR
    #######################

    # print('#######')
    # print('ESPACIAR TEXTO CON PUNTO, PUNTO Y COMA O DOS PUNTOS, ... ETC.')
    # print('#######')
    import re

    # msj = re.sub(r'\.', ' . ', msj)
    texto = re.sub(r'(\W)([.;:¿¡"*])(\w)', '\\1 \\2 \\3', texto)
    texto = re.sub(r'([¿¡])(\w)', '\\1 \\2', texto)

    #print('#######')
    #print('TEXT TOKENS')
    #print('#######')
    lista_tokens = word_tokenize(texto)
    # lista_tokens = texto.split(' ')
    texto_anonimo = '_'.join(lista_tokens)
    print('TOKEN STRIP 1', lista_tokens, texto, texto_anonimo)
    # for token in lista_tokens:
    #    print('TOKEN STRIP 1.1', token)

    # print('ELIMINAR NOMBRES APELLIDOS: ANTECESOR, AUTOR y PADRE')
    # print('#######')
    # print('pruebas')
    # print(nltk.edit_distance('Alfred', 'Aldred'), nltk.jaccard_distance(set('Alfred'), set('Aldred')))
    # print(nltk.edit_distance('Purificación', 'Puri'), nltk.jaccard_distance(set('Purificación'), set('Puri')))
    # exit(999)

    if nombres != '':
        #print("NOMBREEEEEEEE:", nombres)

        # Nombres y apellidos compuestos partidos
        nombres_c = [nombre for nombre in nombres.replace(' ', '-').split('-') if nombre]

        # Extrae la lista de los nombres
        nombres = [nombre for nombre in nombres.split(' ') if nombre] + nombres_c
        #print("NOMBREEEEEEEE C:", nombres)

        # Nombres y Apellidos compuestos
        # Bigramas
        from nltk import bigrams

        nombres_b = " ".join(["-".join(bi) if bi[0] != '' and bi[1] != '' else '' for bi in bigrams(nombres)])
        nombres_b = [nombre for nombre in nombres_b.split(' ') if nombre]

        # Nombres y apellidos compuestos con bigramas
        nombres = nombres + nombres_b
        #print("NOMBREEEEEEEE B:", nombres)

        # Quitar artículos de la lista de nombres
        # Quitar stopwords: (nombre in stop_words)
        # Quitar repetidos
        lista_nombres = set(['' if (len(nombre) < 3) or (nombre.lower() in stop_words) else nombre for nombre in nombres])

        # Quitar Tildes Castellano, Catalán, ¿¿¿ Más tildes: ( ´ ` ) ^ ¨ ???
        lista_nombres = [nombre.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('à', 'a').replace('é', 'e').replace('ì', 'i').replace('ò', 'o').replace('ù', 'u').replace('À', 'A').replace('È', 'E').replace('Ì', 'I').replace('Ò', 'O').replace('Ù', 'U') for nombre in lista_nombres]
        lista_tokens = [token.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('à', 'a').replace('é', 'e').replace('ì', 'i').replace('ò', 'o').replace('ù', 'u').replace('À', 'A').replace('È', 'E').replace('Ì', 'I').replace('Ò', 'O').replace('Ù', 'U') for token in lista_tokens]

        # print('TOKEN STRIP 1.2', lista_nombres, lista_tokens)

        lista_tokens = ['[ANONIMO]' if token in lista_nombres else token for token in lista_tokens]

        # Distancia Levenshtein       |    Distancia Jaccard
        # ---------------------       |    -----------------
        # nltk.edit_distance(w1, w2)  |    nltk.jaccard_distance(set(w1), set(w2))
        # Para tokens originales (0, 0.0) o para tokens en minúsculas (0, 0.0) de longitud inferior o igual a 3 caracteres
        # Para tokens originales (1, 0.2) o para tokens en minúsculas (1, 0.1) de longitud superior a 3 caracteres
        for nombre in lista_nombres:
            lista_tokens = ['[ANONIMO]' if (
                    # Nombres Cortos
                    ((((nltk.edit_distance(token, nombre) <= 0 and nltk.jaccard_distance(set(token), set(nombre)) <= 0.0)) or
                     ((nltk.edit_distance(token.lower(), nombre.lower()) <= 0 and nltk.jaccard_distance(set(token.lower()), set(nombre.lower())) <= 0.0)))
                     and len(token) <= 3) or
                    # Nombres Largos
                    ((((nltk.edit_distance(token, nombre) <= 0 and nltk.jaccard_distance(set(token), set(nombre)) <= 0.2)) or
                     ((nltk.edit_distance(token.lower(), nombre.lower()) <= 1 and nltk.jaccard_distance(set(token.lower()), set(nombre.lower())) <= 0.1)))
                     and len(token) > 3)) else token for token in lista_tokens]

            # print('TOKEN STRIP 1.3', lista_tokens)
        #lista_tokens = ['[ANONIMO]' if (
        #        (nltk.edit_distance(token, lista_nombres[1]) <= 1 and nltk.jaccard_distance(set(token), set(lista_nombres[1])) <= 0.2)
        #        and len(token) > 3) else token for token in lista_tokens]
        #lista_tokens = ['[ANONIMO]' if (
        #        ((nltk.edit_distance(token, nombre) <= 1 and nltk.jaccard_distance(set(token), set(nombre)) <= 0.2) for nombre in lista_nombres)
        #        and len(token) > 3) else token for token in lista_tokens]

        #lista_tokens = ['[ANONIMO]' if procesadoMensaje.distancia_combinada(token, lista_nombres[1]) <= 1.5 else token for token in lista_tokens]
        #lista_tokens = ['[ANONIMO]' if nltk.jaccard_distance(set(token), set(lista_nombres[1])) <= 0.2 else token for token in lista_tokens]
        #lista_tokens = ['[ANONIMO]' if (nltk.edit_distance(token, lista_nombres[1]) == 1 and len(nombre) == len(lista_nombres[1]) and nltk.jaccard_distance(set(token), set(lista_nombres[1])) < 0.5) else token for token in lista_tokens]

        #print("NOMBREEEEEEEE:", lista_nombres)

        # print('#######')
        # print('TEXT UNTOKENS')
        # print('#######')
        # Join the string based on ' ' delimiter
        texto_anonimo = ' '.join(lista_tokens)
        print('TOKEN STRIP 2', lista_tokens, texto, texto_anonimo)


    #######################
    # FIN REVISAR NOMBRES AUTOR
    #######################

    return texto_anonimo  # + '\n #####################################################\n' + msj


# TOKEN
########################
def tokenizado(msj=mensaje, nombres=''):
    global tokens
    global sentencias
    global palabras
    global lista_palabras
    global longitud_media_tokens
    global longitud_media_frases
    global mensajes

    # GLOBAL
    # Array de mensajea
    mensajes.append(msj)

    lista_tokens = []
    lista_palabras = []

    from nltk.tokenize import TreebankWordTokenizer

    tokenizer = TreebankWordTokenizer()

    #print('#######')
    #print('ESPACIAR TEXTO CON PUNTO, PUNTO Y COMA O DOS PUNTOS, ... ETC.')
    #print('#######')
    import re

    #msj = re.sub(r'\.', ' . ', msj)
    msj = re.sub(r'(\W)([.;:¿¡"*])(\w)', '\\1 \\2 \\3', msj)
    msj = re.sub(r'([¿¡])(\w)', '\\1 \\2', msj)

    #print('#######')
    #print('TOKENS')
    #print('#######')
    lista_tokens = word_tokenize(msj)
    #lista_tokens2 = tokenizer.tokenize(msj)

    #print('#######')
    #print('DIVIDIR TOKENS ???????????????????????????????????')
    #print('#######')
    #lista_tokens = [token.split('.') for token in lista_tokens]
    #lista_tokens = [token[:token.index('.')] if '.' in token else token for token in lista_tokens]
    #lista_tokens = [token.split('.')[0] + ' . ' + token.split('.')[1] if '.' in token else token for token in lista_tokens]

    # REVISAR
    #print('ELIMINAR NOMBRES APELLIDOS: ANTECESOR, AUTOR y PADRE')
    #print('#######')
    #print('pruebas')
    #print(nltk.edit_distance('Alfred', 'Aldred'), nltk.jaccard_distance(set('Alfred'), set('Aldred')))
    #print(nltk.edit_distance('Purificación', 'Puri'), nltk.jaccard_distance(set('Purificación'), set('Puri')))
    #exit(999)

    if nombres != '':
        #print("NOMBREEEEEEEE:", nombres)

        # Nombres y apellidos compuestos partidos
        nombres_c = [nombre for nombre in nombres.replace(' ', '-').split('-') if nombre]

        # Extrae la lista de los nombres
        nombres = [nombre for nombre in nombres.split(' ') if nombre] + nombres_c
        #print("NOMBREEEEEEEE C:", nombres)

        # Nombres y Apellidos compuestos
        # Bigramas
        from nltk import bigrams

        nombres_b = " ".join(["-".join(bi) if bi[0] != '' and bi[1] != '' else '' for bi in bigrams(nombres)])
        nombres_b = [nombre for nombre in nombres_b.split(' ') if nombre]

        # Nombres y apellidos compuestos con bigramas
        nombres = nombres + nombres_b
        #print("NOMBREEEEEEEE B:", nombres)

        # Quitar artículos de la lista de nombres
        # Quitar stopwords: (nombre in stop_words)
        # Quitar repetidos
        lista_nombres = set(['' if (len(nombre) < 3) or (nombre.lower() in stop_words) else nombre for nombre in nombres])

        # Quitar Tildes Castellano, Catalán, ¿¿¿ Más tildes: ( ´ ` ) ^ ¨ ???
        lista_nombres = [nombre.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('à', 'a').replace('é', 'e').replace('ì', 'i').replace('ò', 'o').replace('ù', 'u').replace('À', 'A').replace('È', 'E').replace('Ì', 'I').replace('Ò', 'O').replace('Ù', 'U') for nombre in lista_nombres]
        lista_tokens = [token.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('à', 'a').replace('é', 'e').replace('ì', 'i').replace('ò', 'o').replace('ù', 'u').replace('À', 'A').replace('È', 'E').replace('Ì', 'I').replace('Ò', 'O').replace('Ù', 'U') for token in lista_tokens]

        lista_tokens = ['[ANONIMO]' if token in lista_nombres else token for token in lista_tokens]

        # Distancia Levenshtein       |    Distancia Jaccard
        # ---------------------       |    -----------------
        # nltk.edit_distance(w1, w2)  |    nltk.jaccard_distance(set(w1), set(w2))
        # Para tokens originales (0, 0.0) o para tokens en minúsculas (0, 0.0) de longitud inferior o igual a 3 caracteres
        # Para tokens originales (1, 0.2) o para tokens en minúsculas (1, 0.1) de longitud superior a 3 caracteres
        for nombre in lista_nombres:
            lista_tokens = ['[ANONIMO]' if (
                    ((((nltk.edit_distance(token, nombre) <= 0 and nltk.jaccard_distance(set(token), set(nombre)) <= 0.0)) or
                     ((nltk.edit_distance(token.lower(), nombre.lower()) <= 0 and nltk.jaccard_distance(set(token.lower()), set(nombre.lower())) <= 0.0)))
                     and len(token) <= 3) or
                    ((((nltk.edit_distance(token, nombre) <= 0 and nltk.jaccard_distance(set(token), set(nombre)) <= 0.2)) or
                     ((nltk.edit_distance(token.lower(), nombre.lower()) <= 1 and nltk.jaccard_distance(set(token.lower()), set(nombre.lower())) <= 0.1)))
                     and len(token) > 3)) else token for token in lista_tokens]
        #lista_tokens = ['[ANONIMO]' if (
        #        (nltk.edit_distance(token, lista_nombres[1]) <= 1 and nltk.jaccard_distance(set(token), set(lista_nombres[1])) <= 0.2)
        #        and len(token) > 3) else token for token in lista_tokens]
        #lista_tokens = ['[ANONIMO]' if (
        #        ((nltk.edit_distance(token, nombre) <= 1 and nltk.jaccard_distance(set(token), set(nombre)) <= 0.2) for nombre in lista_nombres)
        #        and len(token) > 3) else token for token in lista_tokens]

        #lista_tokens = ['[ANONIMO]' if procesadoMensaje.distancia_combinada(token, lista_nombres[1]) <= 1.5 else token for token in lista_tokens]
        #lista_tokens = ['[ANONIMO]' if nltk.jaccard_distance(set(token), set(lista_nombres[1])) <= 0.2 else token for token in lista_tokens]
        #lista_tokens = ['[ANONIMO]' if (nltk.edit_distance(token, lista_nombres[1]) == 1 and len(nombre) == len(lista_nombres[1]) and nltk.jaccard_distance(set(token), set(lista_nombres[1])) < 0.5) else token for token in lista_tokens]

        #print("NOMBREEEEEEEE:", lista_nombres)

    # REVISAR
    #print('MINUSCULAS')
    #print('#######')
    lista_tokens = [token.lower() for token in lista_tokens]

    # GLOBAL
    # Array de tokens
    tokens.append(lista_tokens)
    sentencias = sent_tokenize(msj)

    # 1 LONGITUD
    longitud_caracteres = len(msj)

    # 2 NUMERO
    numero_tokens = len(lista_tokens)
    numero_frases = len(sentencias)
    # Busca caracteres ALFANUMERICOS y NO ALFANUMERICOS
    if longitud_caracteres > 0:
        # Todos los [A-Z,a-Z,0-9,acentuadas y eñes]
        numero_alfanumericos = len(re.findall(r'\w', msj, re.M | re.I))
        numero_clicks = longitud_caracteres - numero_alfanumericos
        #print('ALFANUMERICOS ENCONTRADOS: ', len(msj), numero_alfanumericos, numero_clicks, msj)
    else:
        numero_alfanumericos = 0
        numero_clicks = 0

    # 3 MEDIAS
    # Pendiente de Calcular
    longitud_media_tokens = longitud_media_tokens + numero_tokens
    longitud_media_frases = longitud_media_frases + numero_frases

    #print('FRASES', sentencias)
    #print('TOKENS', lista_tokens)

    # STOPWRODS
    #print('STOPWRODS lang="es"')
    #print('#######')

    # PALABRAS = (TOKENS - STOPWORDS)
    for t in lista_tokens:
        if t not in stop_words:
            # GLOBAL
            # Array de palabras
            palabras.append(t)
            lista_palabras.append(t)
    numero_palabras = len(lista_palabras)
    numero_stop_words = numero_tokens - numero_palabras

    #print('STOPWORDS', stop_words)
    #print('PALABRAS', lista_palabras)

    #print(lista_tokens)

    return {"c": msj, "lc": longitud_caracteres, 't': lista_tokens, 'nt': numero_tokens, 'f': sentencias,
            'nf': numero_frases, 'p': lista_palabras, 'np': numero_palabras, 'ns': numero_stop_words,
            'na': numero_alfanumericos, 'nc': numero_clicks}


# RAIZ
########################
def enraizado(pal=lista_palabras):
    global raices
    global lista_raices

    #print('#######')
    #print('RAICES lang="es"')
    #print('#######')

    # Extrae raices
    lista_raices = []
    for p in lista_palabras:
        r = ss.stem(p)
        raices.append(r)
        lista_raices.append(r)
    numero_raices = len(lista_raices)

    # Elimina duplicados
    lista_raices_distintas = []
    # [x.append(i) for i in s if i not in x]
    [lista_raices_distintas.append(raiz) for raiz in lista_raices if raiz not in lista_raices_distintas]
    numero_raices_distintas = len(lista_raices_distintas)

    # print('IDIOMAS', SnowballStemmer.languages)
    #print('RAICES', lista_raices, lista_raices_distintas)

    return {'r': lista_raices, 'nr': numero_raices, 'rd': lista_raices_distintas, 'nrd': numero_raices_distintas}


# POSTAGGING
########################
def postag_EN():

    print('#######')
    print('POSTAGGING A/B/C')
    print('#######')

    # A
    # English Palabras
    print('POSTAGGING A lang="en"')
    print('Palabras')
    print('#######')
    pos = nltk.pos_tag(palabras)
    print(pos)
    for p in palabras:
        print(p, palabras.index(p))

    # B
    # English Sentencias
    print('POSTAGGING B lang="en"')
    print('Sentencias')
    print('#######')
    lista_tags = []
    for sentencia in sentencias:
        lista_tags = lista_tags + nltk.pos_tag(nltk.word_tokenize(sentencia))

    for word in lista_tags:
        if 'NNP' in word[1]:
            print(word)

    return {0}


def postag(msj=mensaje):
    global tags

    # C
    # Spanish Mensaje
    print('#######')
    print('POSTAGGING C lang="es"')
    print('#######')

    lista_tags = []

    # tokenizado()
    # Si no se ha llamado tokenizado() previamente
    print('#######')
    print('DIVIDIR TOKENS CON PUNTO, PUNTO Y COMA O DOS PUNTOS, ... ETC.')
    print('#######')
    import re

    msj = re.sub(r'(\W)([.;:¿"*])(\w)', '\\1 \\2 \\3', msj)

    # Minúsculas
    #for sentencia in sent_tokenize(msj.lower()):
    for sentencia in sent_tokenize(msj):
        # X token
        tag = spanish_postagger.tag(word_tokenize(sentencia))
        # X frase
        # tag = spanish_postagger.tag_sents(sentencia)
        tags.append(tag)
        lista_tags = lista_tags + tag

    # PoS TAG RAICES (no funciona demasiado bien, mezcla y confunde verbos y nombrea)
    # lista_tags = spanish_postagger.tag(lista_raices)

    print('POSTAG', lista_tags)
    nombres = []
    for word_tag in lista_tags:
        if 'n' in word_tag[1]:
            nombres.append(word_tag)
    numero_nombres = len(nombres)

    verbos = []
    for word_tag in lista_tags:
        if 'v' in word_tag[1]:
            verbos.append(word_tag)
    numero_verbos = len(verbos)

    # Elimina duplicados
    lista_tags_distintas = []
    # [x.append(i) for i in s if i not in x]
    [lista_tags_distintas.append(tag) for tag in lista_tags if tag not in lista_tags_distintas]

    print('POSTAG DISTINTAS', lista_tags_distintas)
    nombres_distintos = []
    for word_tag in lista_tags_distintas:
        if 'n' in word_tag[1]:
            nombres_distintos.append(word_tag)
    numero_nombres_distintos = len(nombres_distintos)

    verbos_distintos = []
    for word_tag in lista_tags_distintas:
        if 'v' in word_tag[1]:
            verbos_distintos.append(word_tag)
    numero_verbos_distintos = len(verbos_distintos)

    print('NOMBRES', nombres, nombres_distintos)
    print('VERBOS', verbos, verbos_distintos)

    return {'n': nombres, 'nn': numero_nombres, 'v': verbos, 'nv': numero_verbos, 'nd': nombres_distintos,
            'nnd': numero_nombres_distintos, 'vd': verbos_distintos, 'nvd': numero_verbos_distintos}


###########################
# CLASIFICACIONES Y CULSTER
###########################
# CULSTER
########################
def cluster(ins=instancias):
    from nltk.cluster import em
    from nltk.cluster import gaac
    from nltk.cluster import kmeans
    from nltk.cluster import util

    print('#######')
    print('CLUSTER')
    print('#######')

    em.demo()
    gaac.demo()
    kmeans.demo()

    try:
        import numpy as np
    except ImportError:
        pass

    print(util.cosine_distance(np.array([0.5, 0.5, 0.5]), np.array([1, 1, 1])))
    print(util.euclidean_distance(np.array([0.1, 0.1, 0.1]), np.array([1, 1, 1])))

    class AttributeDict(dict):
        __getattr__ = dict.__getitem__
        __setattr__ = dict.__setitem__

    #ins = AttributeDict(ins)
    for item in enumerate(ins):
        print()
        #print(item)
        #print(getattr(item, 'Nº autores'))

    # Recorre dict ins=intancias
    #colocando sólo valores en el vector
    vector = []
    vectores = []
    for i, item in enumerate(ins):
        vector = [v for v in item.values()]
        vectores.append(vector)
        #for key, value in item.items():
        #    print(key, value)
        #print(getattr(item, 'Nº autores'))

    print(vectores[0])

    # Pribando las distancias
    util.euclidean_distance(np.array(vectores[1]), np.array(vectores[0]))

    #vectors = [np.array(f) for f in ins]
    #vectors = [np.array(f.items()) for f in ins]
    #vectors = [np.array(f.keys()) for f in ins]
    #vectors = [np.array(f.values()) for f in ins]

    vectors = [np.array(f) for f in vectores]

    print()
    print(vectors[0])
    #exit(1)

    # test k-means using the euclidean distance metric, 2 means and repeat
    # clustering 10 times with random seeds
    clusterer = kmeans.KMeansClusterer(4, util.euclidean_distance, repeats=10)
    clusters = clusterer.cluster(vectors, True)
    print('Clustered:', vectors)
    print('As:', clusters)
    print('Means:', clusterer.means())
    print()

    # test the GAAC clusterer with 4 clusters
    clusterer = gaac.GAAClusterer(4)
    clusters = clusterer.cluster(vectors, True)

    print('Clusterer:', clusterer)
    print('Clustered:', vectors)
    print('As:', clusters)
    print()

    return 0

    # test the EM clusterer
    #mediasID = [[0, 1, 1, 1, 96170, 96170, 0, 1, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 218, 0.0, 0, 0, 11, 215, 2019], [0, 1, 1, 1, 96170, 96170, 0, 1, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 218, 0.0, 0, 0, 11, 215, 2019], [0, 1, 1, 1, 96170, 96170, 0, 1, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 218, 0.0, 0, 0, 11, 215, 2019], [0, 1, 1, 1, 96170, 96170, 0, 1, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 218, 0.0, 0, 0, 11, 215, 2019]]
    #mediasID = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0, 0, 0, 0, 0],
    #          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.0, 1.0, 1, 1, 1, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1.0, 1.0, 1.0, 1.0, 1, 1.0, 1, 1, 1, 1, 1],
    #          [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2.0, 2.0, 2, 2, 2, 2, 2.0, 2.0, 2.0, 2.0, 2, 2, 2.0, 2.0, 2.0, 2.0, 2, 2.0, 2, 2, 2, 2, 2],
    #          [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3.0, 3.0, 3, 3, 3, 3, 3.0, 3.0, 3.0, 3.0, 3, 3, 3.0, 3.0, 3.0, 3.0, 3, 3.0, 3, 3, 3, 3, 3]]
    #medias = [[0, 1, 1, 1, 0, 1, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 218, 0.0, 0, 0, 11, 215, 2019], [0, 1, 1, 1, 0, 1, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 218, 0.0, 0, 0, 11, 215, 2019], [0, 1, 1, 1, 0, 1, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 218, 0.0, 0, 0, 11, 215, 2019], [0, 1, 1, 1, 0, 1, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 218, 0.0, 0, 0, 11, 215, 2019]]
    medias = [[0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1.0, 1.0, 1, 1, 1, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1.0, 1.0, 1.0, 1.0, 1, 1.0, 1, 1, 1, 1, 1],
              [2, 2, 2, 2, 2, 2, 2, 2, 2.0, 2.0, 2, 2, 2, 2, 2.0, 2.0, 2.0, 2.0, 2, 2, 2.0, 2.0, 2.0, 2.0, 2, 2.0, 2, 2, 2, 2, 2],
              [3, 3, 3, 3, 3, 3, 3, 3, 3.0, 3.0, 3, 3, 3, 3, 3.0, 3.0, 3.0, 3.0, 3, 3, 3.0, 3.0, 3.0, 3.0, 3, 3.0, 3, 3, 3, 3, 3]]
    clusterer = em.EMClusterer(medias, bias=0.1)
    clusters = clusterer.cluster(vectors, True, trace=True)

    print('Clustered:', vectors)
    print('As:       ', clusters)
    print()

    return 0


###########################
# CLASIFICACIONES
########################
def clasificador(ins=instancias):
    return 0


# GENERO
########################
def genero(listaNombres=nombres):
    from nltk.corpus import names

    print('#######')
    print('NOMBRES')
    print('#######')

    # Load data and training
    names = ([(name, 'male') for name in names.words('male.txt')] +
             [(name, 'female') for name in names.words('female.txt')])
    print(names)

    # Leer datos y entrenar el modelo
    fileH = open(os.path.join(dir_path, 'nombres\\male.txt'), 'r')
    fileM = open(os.path.join(dir_path, 'nombres\\female.txt'), 'r')

    # Listado de nombres N-gramas para búsqueda directa
    strHombres = []
    strMujeres = []
    strHombres = fileH.read()
    strMujeres = fileM.read()

    # print(fileM.readline().capitalize())

    fileH = open(os.path.join(dir_path, 'nombres\\male.txt'), 'r')
    fileM = open(os.path.join(dir_path, 'nombres\\female.txt'), 'r')

    # Array de par (género, nombre 1-grama)
    nombres1grama = ([(name.lower().capitalize(), 'male') for name in word_tokenize(fileH.read())] +
                     [(name.lower().capitalize(), 'female') for name in word_tokenize(fileM.read())])

    fileH = open(os.path.join(dir_path, 'nombres\\male.txt'), 'r')
    fileM = open(os.path.join(dir_path, 'nombres\\female.txt'), 'r')

    # Array de nombres N-gramas para entrenamiento del modelo
    hombres = []
    mujeres = []
    for line in fileH:
        hombres.append(line.replace("\n", "").lower())
    for line in fileM:
        mujeres.append(line.replace("\n", "").lower())

    # Array de par (género, nombre N-grama)
    nombresNgrama = ([(name, 'male') for name in hombres] +
                     [(name, 'female') for name in mujeres])

    # print(nombres1grama, nombresNgrama)

    # Nombres ESPAÑOLES
    featuresetsES1 = [(procesadoMensaje.gender_features3(n), g) for (n, g) in nombres1grama]
    print('GENERO', featuresetsES1)
    featuresetsES2 = [(procesadoMensaje.gender_features3(n), g) for (n, g) in nombres1grama]
    print('GENERO', featuresetsES2)

    # Nombres Anglosajones
    featuresetsEN1 = [(procesadoMensaje.gender_features3(n), g) for (n, g) in names]
    print('GENERO', featuresetsEN1)

    classifier1 = nltk.NaiveBayesClassifier.train(featuresetsES1)
    classifier2 = nltk.classify.positivenaivebayes.NaiveBayesClassifier.train(featuresetsES1)
    classifier3 = nltk.classify.decisiontree.DecisionTreeClassifier.train(featuresetsES1)

    # Predicción
    listaNombres = ['José', 'Pepe', 'Laura', 'Tanis', 'Josefa María', 'Romualdo', 'Pío María Bonifacio', 'José María',
                    'María José', 'Loreto', 'Lourdes', 'Pilar', 'Carmen', 'Isabel', 'Cristofer', 'Jake', 'Santal',
                    'Chantal']

    generoNombres = [(nombre, classifier1.classify(procesadoMensaje.gender_features2(word_tokenize(nombre)[0])),
                      strHombres.count(nombre.upper()), strMujeres.count(nombre.upper())) for nombre in listaNombres]
    print(generoNombres)
    generoNombres = [(nombre, classifier2.classify(procesadoMensaje.gender_features2(word_tokenize(nombre)[0])),
                      strHombres.count(nombre.upper()), strMujeres.count(nombre.upper())) for nombre in listaNombres]
    print(generoNombres)
    generoNombres = [(nombre, classifier3.classify(procesadoMensaje.gender_features2(word_tokenize(nombre)[0])),
                      strHombres.count(nombre.upper()), strMujeres.count(nombre.upper())) for nombre in listaNombres]
    print(generoNombres)

    return {0}


# ANALISIS EDL SENTIMIENTO
########################
def sentimiento():
    import nltk.classify.util
    from nltk.classify import NaiveBayesClassifier

    # SENTINEL lang = es
    ####################

    print('#######')
    print('SENTINEL lang = ES')
    print('###################')

    fileP = open(os.path.join(dir_path, 'sentimiento\\positive.txt'), 'r', encoding='utf-8')
    fileN = open(os.path.join(dir_path, 'sentimiento\\negative.txt'), 'r', encoding='utf-8')
    fileL = open(os.path.join(dir_path, 'sentimiento\\neutral.txt'), 'r', encoding='utf-8')

    # Array de términos positivos/negativos N-gramas para entrenamiento del modelo
    positivos = []
    negativos = []
    neutros = []

    # positivos = fileP.read()
    # negativos = fileN.read()

    for line in fileP:
        # positivos.append(line.replace(" ", "_").replace("\n", "").lower())
        positivos.append(line.replace(" ", "_").replace("\n", "").lower())
    for line in fileN:
        negativos.append(line.replace(" ", "_").replace("\n", "").lower())
    for line in fileL:
        neutros.append(line.replace(" ", "_").replace("\n", "").lower())

    # print(positivos, negativos)

    # Array de par (género, nombre N-grama) lang=es
    positivos.extend(
        [':)', ':-)', ';-)', 'También', 'Tambien', 'Y', 'O', 'Alguien', 'Algo', 'Siempre', 'Alguno', 'Alguna',
         'Algunos', 'Algunas', 'Algún', 'Algun', 'También demasiado', 'Tambien demasiado', 'Alguna cosa', ':)', ':)'])
    negativos.extend(
        [':(', ':-(', ';-(', 'Tampoco', 'Ni', 'Nadie', 'Nada', 'Nunca', 'Ninguno', 'Ninguna', ':(', ':-(', ';(', ';-('])
    # neutros.extend([])

    stopWords = stopwords.words('spanish')
    # Añadir signos de puntuación
    stopWords.extend(('¡', '¿', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';',
                      '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'))

    # Añadir pronombres, preposiciones y demás vocabulario sin significación
    stopWords.extend(['ser', 'estar'])
    neutros.extend(stopWords)
    print(stopWords)

    positive_vocab_ES = positivos
    negative_vocab_ES = negativos
    neutral_vocab_ES = neutros

    print(positive_vocab_ES, negative_vocab_ES, neutral_vocab_ES)

    ss = SnowballStemmer('spanish')

    # Características par (token, 'pos/neg/neu') de entrenamiento del modelo
    # positive_features_ES = [(procesadoMensaje.word_feats(pos), 'pos') for pos in positive_vocab_ES]
    # negative_features_ES = [(procesadoMensaje.word_feats(neg), 'neg') for neg in negative_vocab_ES]
    # neutral_features_ES = [(procesadoMensaje.word_feats(neu), 'neu') for neu in neutral_vocab_ES]

    positive_features_ES = [(procesadoMensaje.word_feats(pos.lower()), 'positive') for pos in positive_vocab_ES]
    negative_features_ES = [(procesadoMensaje.word_feats(neg.lower()), 'negative') for neg in negative_vocab_ES]
    neutral_features_ES = [(procesadoMensaje.word_feats(neu.lower()), 'neutral') for neu in neutral_vocab_ES]

    # positive_features_ES = [(procesadoMensaje.word_feats(ss.stem(pos.lower())), 'pos') for pos in positive_vocab_ES]
    # negative_features_ES = [(procesadoMensaje.word_feats(ss.stem(neg.lower())), 'neg') for neg in negative_vocab_ES]
    # neutral_features_ES = [(procesadoMensaje.word_feats(ss.stem(neu.lower())), 'neu') for neu in neutral_vocab_ES]

    # train_set_ES = positive_features_ES + negative_features_ES + neutral_features_ES
    train_set_ES = positive_features_ES + negative_features_ES

    print('SENTINEL ANALISIS lang = ES', positive_features_ES, positive_vocab_ES, neutral_features_ES)

    # SENTINEL lang = en
    ####################

    print('SENTINEL lang = EN')
    print('###################')

    # Array de tokens (termino 1-grama) lang=en
    positive_vocab = ['awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)']
    negative_vocab = ['bad', 'terrible', 'useless', 'hate', ':(']
    neutral_vocab = ['movie', 'the', 'sound', 'was', 'is', 'actors', 'did', 'know', 'words', 'not']

    # Características par (token, 'pos/neg/neu') de entrenamiento del modelo
    positive_features = [(procesadoMensaje.word_feats(pos.lower()), 'pos') for pos in positive_vocab]
    negative_features = [(procesadoMensaje.word_feats(neg.lower()), 'neg') for neg in negative_vocab]
    neutral_features = [(procesadoMensaje.word_feats(neu.lower()), 'neu') for neu in neutral_vocab]

    # train_set = positive_features + negative_features + neutral_features
    train_set = positive_features + negative_features

    print('SENTINEL ANALISIS lang = EN', positive_features, negative_features, neutral_features)

    # Clasificadores
    # ES
    classifier1_ES = NaiveBayesClassifier.train(train_set_ES)
    classifier2_ES = nltk.classify.positivenaivebayes.NaiveBayesClassifier.train(train_set_ES)
    classifier3_ES = nltk.classify.decisiontree.DecisionTreeClassifier.train(train_set_ES)
    # EN
    classifier = NaiveBayesClassifier.train(train_set)

    # Predict ES
    neg = 0
    pos = 0
    sentence_ES_P = "Impresionante película, también me ha gustado"
    sentence_ES_N = "Mala película, no me ha gustado"

    sentence = sentence_ES_N

    # C Spanish
    print('POSTAGGING C lang="es"')
    print('#######')

    # Lectura desde ficheros
    # del tagger java Stanford

    # about the tagger: http://nlp.stanford.edu/software/tagger.shtml
    # about the tagset: nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html
    spanish_postagger = StanfordPOSTagger(os.path.join(dir_path, 'standford/models/spanish.tagger'),
                                          os.path.join(dir_path, 'standford/stanford-postagger.jar'), encoding='utf8')

    lista_tags = []
    for sentencia in sent_tokenize(sentence.lower()):
        lista_tags = lista_tags + spanish_postagger.tag(word_tokenize(sentencia))

    print('POSTAG', lista_tags)
    nombres = []
    for wordTag in lista_tags:
        if 'nc' in wordTag[1]:
            nombres.append(wordTag)

    print('NOMBRES', nombres)

    from nltk.tokenize import RegexpTokenizer

    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(sentence)

    # words = sentence.split(' ')
    for word in words:
        # classResult_ES = classifier_ES.classify(procesadoMensaje.word_feats(ss.stem(word.lower())))
        classResult1_ES = classifier1_ES.classify(procesadoMensaje.word_feats(word.lower()))
        classResult2_ES = classifier2_ES.classify(procesadoMensaje.word_feats(word.lower()))
        classResult3_ES = classifier3_ES.classify(procesadoMensaje.word_feats(word.lower()))

        classResult_ES = procesadoMensaje.ponderarClasificacion([classResult1_ES, classResult2_ES, classResult3_ES])

        if ((word.lower() not in stopWords) and (word.lower() not in nombres[0])) or (word.lower() in 'no') or (
                word.lower() in 'sí'):
            if classResult_ES == 'neutral':
                pos = pos + 1
                print(word, 'neutral', ss.stem(word))
            if classResult_ES == 'negative':
                neg = neg + 1
                print(word, 'negative', ss.stem(word))
            if classResult_ES == 'positive':
                pos = pos + 1
                print(word, 'positive', ss.stem(word))

    print('Positive ES: ' + str(float(pos) / len(words)))
    print('Negative ES: ' + str(float(neg) / len(words)))

    # Predict EN
    neg = 0
    pos = 0

    sentence = "Awesome movie, I liked it"

    words = sentence.split(' ')
    for word in words:
        classResult = classifier.classify(procesadoMensaje.word_feats(word))
        if classResult == 'neg':
            neg = neg + 1
            print(word, 'neg')
        if classResult == 'pos':
            pos = pos + 1
            print(word, 'pos')

    print('Positive EN: ' + str(float(pos) / len(words)))
    print('Negative EN: ' + str(float(neg) / len(words)))

    return 0


# ANT/SINONIMOS
########################
def sinonimos():
    print('#######')
    print('ANT/SINONIMOS lang="en"')
    print('#######')

    from nltk.corpus import wordnet

    try:
        syn = wordnet.synsets("big")
        print(syn[0].definition())
        print(syn[0].lemmas())
        print(syn[0].lemmas()[0].antonyms())
        print(syn[0].examples())
    except NameError:
        print("well, it WASN'T defined after all!")
    else:
        print("sure, it was defined.")

    for syn in wordnet.synsets("big"):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            for anton in lemma.antonyms():
                antonyms.append(anton.name())

    print(synonyms)
    print(antonyms)

    print('WORDNET 3.0 lang="es"')
    print('#######', dir_path)
    from nltk.corpus.reader import XMLCorpusReader, XMLCorpusView, CategorizedCorpusReader
    import glob

    reader = XMLCorpusReader(os.path.join(dir_path + '\wordnet3'), '.*\.xml')
    # reader = XMLCorpusReader(os.path.join(dir_path + '\wordnet3'), 'wn_synset.xml')

    # viewer = XMLCorpusView(os.path.join(dir_path + '\wordnet3'), '.*\.xml')[0]

    print(nltk.corpus.gutenberg.fileids())
    print(nltk.corpus.wordnet.synsets)
    print(nltk.corpus.wordnet.fileids())
    print(nltk.corpus.wordnet.words())
    # print(nltk.corpus.wordnet.sents())
    files = glob.glob(dir_path + '\wordnet3/*.xml')
    sentences = []
    dir = ''
    fi = ''
    i = 0
    for file in files:
        if i > 0 and i % 500 == 0:
            print("%d/%d files loaded, #-sentences: %d, #-file: %s" %
                  (i, len(files), len(sentences), file.split(dir_path + '\wordnet3')[1].split('\\')))
        dir = dir_path + '\wordnet3'
        fi = file.split(dir)[1][1:]
        reader = XMLCorpusReader(dir, fi)
        print(reader.words(), fi)
        sentences.extend(nltk.sent_tokenize(" ".join(reader.words())))
        i += 1

    # READER
    print(reader.fileids())
    print(sentences)

    # print(reader.words('wn_synset.xml'))
    # print(reader.words())

    # VIEWER
    # print(viewer)

    return 0


# LEMAS
########################
def lemas():
    print('#######')
    print('LEMAS lang="en"')
    print('#######')
    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()
    for s in synonyms:
        print(lemmatizer.lemmatize(s))
    for a in antonyms:
        print(lemmatizer.lemmatize(a))

    print(lemmatizer.lemmatize('playing', pos="v"))

    print(lemmatizer.lemmatize('playing', pos="n"))

    print(lemmatizer.lemmatize('playing', pos="a"))

    print(lemmatizer.lemmatize('playing', pos="r"))

    print('#######')
    print('NGRAMAS lang="en"')
    print('#######')
    from nltk.util import ngrams
    text = "Hi How are you? i am fine and you"
    token = nltk.word_tokenize(text)

    bigrams = ngrams(token, 2)
    biarray = [bi for bi in bigrams]
    print('BIARRAY:', biarray)
    for bi in bigrams:
        print('BIGRAMAS:', bi)

    trigrams = ngrams(token, 3)

    print('TRIGRAMAS:', next(trigrams))

    fourgrams = ngrams(token, 4)

    print('CUATRIGRAMAS:', next(fourgrams))

    return 0
