import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger, StanfordTagger

from nltk import ne_chunk, pos_tag

# E/S
import os

import json

# Módulos propios
import procesadoMensaje

# VARIABLES GLOBALES
#######################
data = "All work and no play makes jack dull boy. All work and no play makes jack a dull boy."
mensaje = " Me cago en en tu puta madre 0.Mierda para tu puta madre 1. Mierda para tu puta madre "
"2.Mierda para tu puta madre 3. Mierda para tu puta madre 4.Caca de la vaca, para el resto. 5. Final"

tokens = []
sentencias = []
# stop_words = []
palabras = []
lista_palabras = []
raices = []
lista_raices = []
mensajes = []
tags = []

longitud_media_tokens = 0.0
longitud_media_frases = 0.0

synonyms = []
antonyms = []


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
print('AAAAAAAAAAAAAAAAAAAAAA', mensaje1)

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


# TOKEN
########################
def tokenizado(msj=mensaje):
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

    print('#######')
    print('TOKENS')
    print('#######')
    lista_tokens = word_tokenize(msj)
    # GLOBAL
    # Array de tokens
    tokens.append(lista_tokens)
    sentencias = sent_tokenize(msj)

    # 1 LONGITUD
    longitud_caracteres = len(msj)
    numero_clicks = longitud_caracteres

    # 2 NUMERO
    numero_tokens = len(lista_tokens)
    numero_frases = len(sentencias)

    # 3 MEDIAS
    # Pendiente de Calcular
    longitud_media_tokens = longitud_media_tokens + numero_tokens
    longitud_media_frases = longitud_media_frases + numero_frases

    print('FRASES', sentencias)
    print('TOKENS', lista_tokens)

    # STOPWRODS
    print('STOPWRODS lang="es"')
    print('#######')
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

    # PALABRAS = (TOKENS - STOPWORDS)
    for t in lista_tokens:
        if t not in stop_words:
            # GLOBAL
            # Array de palabras
            palabras.append(t)
            lista_palabras.append(t)
    numero_palabras = len(lista_palabras)
    numero_stop_words = numero_tokens - numero_palabras

    print('STOPWORDS', stop_words)
    print('PALABRAS', lista_palabras)

    return {"lc": longitud_caracteres, 'nt': numero_tokens, 'nf': numero_frases, 'np': numero_palabras, 'ns': numero_stop_words}


# RAIZ
########################
def enraizado(pal=lista_palabras):
    global raices
    global lista_raices

    print('#######')
    print('RAICES lang="es"')
    print('#######')

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
    print('RAICES', lista_raices, lista_raices_distintas)

    return {'nr': numero_raices, 'nrd': numero_raices_distintas}


# POSTAGGING
########################
def postag_EN():

    print('#######')
    print('TAGGING A/B/C')
    print('#######')

    # A
    # English Palabras
    print('TAGGING A lang="en"')
    print('Palabras')
    print('#######')
    pos = nltk.pos_tag(palabras)
    print(pos)
    for p in palabras:
        print(p, palabras.index(p))

    # B
    # English Sentencias
    print('TAGGING B lang="en"')
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
    print('TAGGING C lang="es"')
    print('#######')

    lista_tags = []
    # Si no se ha llamado tokenizado() previamente
    for sentencia in sent_tokenize(msj):
        tag = spanish_postagger.tag(word_tokenize(sentencia))
        # tag = spanish_postagger.tag_sents(sentencia)
        tags.append(tag)
        lista_tags = lista_tags + tag

    # PoS TAG RAICES (no funciona demasiado bien, confunde verbos y nombrea)
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

    return {'nn': numero_nombres, 'nv': numero_verbos, 'nnd': numero_nombres_distintos, 'nvd': numero_verbos_distintos}


########################
# CLASIFICACIONES Y CULSTERIZACIONES
########################


# GENERO
########################
def genero():
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
    print('TAGGING C lang="es"')
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

        classResult_ES = procesadoMensaje.ponderarClasificación([classResult1_ES, classResult2_ES, classResult3_ES])

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