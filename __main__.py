import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from nltk.tag.stanford import StanfordPOSTagger, StanfordNERTagger, StanfordTagger

from nltk import ne_chunk, pos_tag

# E/S
import os

# Módulos propios
import procesadoMensaje

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
    tit_mensaje= 'título mensaje'
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

        print(self.id_foro, self.nombreForo, self.id_asig, self.tit_hilo, self.id_hilo, self.id_mensaje, self.id_ref_mensaje, self.id_autor, self.autor, self.dia_semana, self.fecha, self.hora, self.tit_mensaje, self.texto)

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


import json
# Objeto
msg = Mensaje(mensaje1)
msg.asignarmensaje(mensaje1)
print('AAAAAAAAAAAAAAAAAAAAAA', mensaje1)

# de modelos
# de taggers java
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

data = "All work and no play makes jack dull boy. All work and no play makes jack a dull boy."
mensaje = " Mierda para tu puta madre 1.Mierda para tu puta madre 2. Mierda para tu puta madre 3. Mierda para tu puta madre 3. Caca de la vaca, para el resto"
tokens = []
sentencias = []
stopWords = []
palabras = []


# TOKENIZADO
# FRASES
def tokenizado():
  print('TOKENS')
  print('#######')

  tokens = word_tokenize(mensaje)
  sentencias = sent_tokenize(mensaje)

  #1
  longitudCaracteres = len(mensaje)
  numeroClicks = longitudCaracteres
  #2
  numeroTokens = len(tokens)
  numeroFrases = len(sentencias)

  # Pendiente de Calcular
  longitudMediaTokens = 0.0
  longitudMediaFrases = 0.0

  print('FRASES', sentencias)
  print('TOKENS', tokens)

  #STOPWRODS
  print('STOPWRODS lang="es"')
  print('#######')
  stopWords = stopwords.words('spanish')

  # Añadir signos de puntuación
  stopWords.append('.')
  stopWords.append(':')
  stopWords.append(',')
  stopWords.append(';')
  stopWords.append('-')
  stopWords.append('"')
  stopWords.append('¡')
  stopWords.append('!')
  stopWords.append('¡')
  stopWords.append('?')
  stopWords.append('&')
  stopWords.append('/')
  stopWords.append('(')
  stopWords.append(')')
  stopWords.extend(('¡', '¿', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
                    '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'))

  # PAABRAS = TOKENS sin STOPWORDS
  for t in tokens:
    if t not in stopWords:
      palabras.append(t)

  print('STOPWORDS', stopWords)
  print('PALABRAS', palabras)

  return {0}


#RAICES
########################
def raices():
  print('RAICES lang="es"')
  print('#######')
  ss = SnowballStemmer('spanish')
  raices = []

  for p in palabras:
    raices.append(ss.stem(p))

  print('IDIOMAS', SnowballStemmer.languages)
  print('RAICES', raices)

  return {0}


#POSTAG
########################
def postag():
  # A
  print('TAGGING A lang="en"')
  print('#######')
  for p in palabras:
      print(p, pos_tag(palabras))

  # B English
  print('TAGGING B lang="en"')
  print('#######')
  posTag = []
  for sentencia in sentencias:
    posTag = posTag + nltk.pos_tag(nltk.word_tokenize(sentencia))

  for word in posTag:
    if 'NNP' in word[1]:
      print(word)

  # C Spanish
  print('TAGGING C lang="es"')
  print('#######')

  # Lectura desde ficheros
  # del tagger java Stanford

  # about the tagger: http://nlp.stanford.edu/software/tagger.shtml
  # about the tagset: nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html
  spanish_postagger = StanfordPOSTagger(os.path.join(dir_path, 'standford/models/spanish.tagger'), os.path.join(dir_path, 'standford/stanford-postagger.jar'), encoding='utf8')

  posTag = []
  for sentencia in sent_tokenize(mensaje):
    posTag = posTag + spanish_postagger.tag(word_tokenize(sentencia))

  print('POSTAG', posTag)
  nombres = []
  for wordTag in posTag:
    if 'n' in wordTag[1]:
      nombres.append(wordTag)

  print('NOMBRES', nombres)

  return {0}


########################
#CLASIFICACION Y CULSTER
########################


# NOMBRES/GENERO
########################
def genero():
  from nltk.corpus import names

  print('NOMBRES')
  print('#######')

  # Load data and training
  names = ([(name, 'male') for name in names.words('male.txt')] +
           [(name, 'female') for name in names.words('female.txt')])
  print(names)

  # Leer datos y entrenar el modelo
  fileH = open(os.path.join(dir_path, 'nombres\\male.txt'), 'r')
  fileM = open(os.path.join(dir_path, 'nombres\\female.txt'), 'r')

  #Listado de nombres N-gramas para búsqueda directa
  strHombres = []
  strMujeres = []
  strHombres = fileH.read()
  strMujeres = fileM.read()

  #print(fileM.readline().capitalize())

  fileH = open(os.path.join(dir_path, 'nombres\\male.txt'), 'r')
  fileM = open(os.path.join(dir_path, 'nombres\\female.txt'), 'r')

  #Array de par (género, nombre 1-grama)
  nombres1grama = ([(name.lower().capitalize(), 'male') for name in word_tokenize(fileH.read())] +
             [(name.lower().capitalize(), 'female') for name in word_tokenize(fileM.read())])

  fileH = open(os.path.join(dir_path, 'nombres\\male.txt'), 'r')
  fileM = open(os.path.join(dir_path, 'nombres\\female.txt'), 'r')

  #Array de nombres N-gramas para entrenamiento del modelo
  hombres = []
  mujeres = []
  for line in fileH:
    hombres.append(line.replace("\n", "").lower())
  for line in fileM:
    mujeres.append(line.replace("\n", "").lower())

  #Array de par (género, nombre N-grama)
  nombresNgrama = ([(name, 'male') for name in hombres] +
             [(name, 'female') for name in mujeres])

  #print(nombres1grama, nombresNgrama)

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

  generoNombres = [(nombre, classifier1.classify(procesadoMensaje.gender_features2(word_tokenize(nombre)[0])), strHombres.count(nombre.upper()), strMujeres.count(nombre.upper())) for nombre in listaNombres]
  print(generoNombres)
  generoNombres = [(nombre, classifier2.classify(procesadoMensaje.gender_features2(word_tokenize(nombre)[0])), strHombres.count(nombre.upper()), strMujeres.count(nombre.upper())) for nombre in listaNombres]
  print(generoNombres)
  generoNombres = [(nombre, classifier3.classify(procesadoMensaje.gender_features2(word_tokenize(nombre)[0])), strHombres.count(nombre.upper()), strMujeres.count(nombre.upper())) for nombre in listaNombres]
  print(generoNombres)

  return {0}

def sentimiento():
    #ANALISIS EDL SENTIMIENTO
    ########################
    import nltk.classify.util
    from nltk.classify import NaiveBayesClassifier

    print('SENTINEL lang = ES')
    print('###################')

    fileP = open(os.path.join(dir_path, 'sentimiento\\positive.txt'), 'r', encoding='utf-8')
    fileN = open(os.path.join(dir_path, 'sentimiento\\negative.txt'), 'r', encoding='utf-8')
    fileL = open(os.path.join(dir_path, 'sentimiento\\neutral.txt'), 'r', encoding='utf-8')

    #Array de términos positivos/negativos N-gramas para entrenamiento del modelo
    positivos = []
    negativos = []
    neutros = []

    #positivos = fileP.read()
    #negativos = fileN.read()

    for line in fileP:
      #positivos.append(line.replace(" ", "_").replace("\n", "").lower())
      positivos.append(line.replace(" ", "_").replace("\n", "").lower())
    for line in fileN:
      negativos.append(line.replace(" ", "_").replace("\n", "").lower())
    for line in fileL:
      neutros.append(line.replace(" ", "_").replace("\n", "").lower())

    #print(positivos, negativos)

    #Array de par (género, nombre N-grama) lang=es
    positivos.extend([':)', ':-)', ';-)', 'También', 'Tambien', 'Y', 'O', 'Alguien', 'Algo', 'Siempre', 'Alguno', 'Alguna', 'Algunos', 'Algunas', 'Algún', 'Algun', 'También demasiado', 'Tambien demasiado', 'Alguna cosa', ':)', ':)'])
    negativos.extend([':(', ':-(', ';-(', 'Tampoco', 'Ni', 'Nadie', 'Nada', 'Nunca', 'Ninguno', 'Ninguna', ':(', ':-(', ';(', ';-('])
    #neutros.extend([])

    stopWords = stopwords.words('spanish')
    # Añadir signos de puntuación
    stopWords.extend(('¡', '¿', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'))

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
    #positive_features_ES = [(procesadoMensaje.word_feats(pos), 'pos') for pos in positive_vocab_ES]
    #negative_features_ES = [(procesadoMensaje.word_feats(neg), 'neg') for neg in negative_vocab_ES]
    #neutral_features_ES = [(procesadoMensaje.word_feats(neu), 'neu') for neu in neutral_vocab_ES]

    positive_features_ES = [(procesadoMensaje.word_feats(pos.lower()), 'positive') for pos in positive_vocab_ES]
    negative_features_ES = [(procesadoMensaje.word_feats(neg.lower()), 'negative') for neg in negative_vocab_ES]
    neutral_features_ES = [(procesadoMensaje.word_feats(neu.lower()), 'neutral') for neu in neutral_vocab_ES]

    #positive_features_ES = [(procesadoMensaje.word_feats(ss.stem(pos.lower())), 'pos') for pos in positive_vocab_ES]
    #negative_features_ES = [(procesadoMensaje.word_feats(ss.stem(neg.lower())), 'neg') for neg in negative_vocab_ES]
    #neutral_features_ES = [(procesadoMensaje.word_feats(ss.stem(neu.lower())), 'neu') for neu in neutral_vocab_ES]

    #train_set_ES = positive_features_ES + negative_features_ES + neutral_features_ES
    train_set_ES = positive_features_ES + negative_features_ES

    print('SENTINEL ANALISIS lang = ES', positive_features_ES, positive_vocab_ES, neutral_features_ES)

    # SENTINEL lang = en
    ####################

    print('SENTINEL lang = EN')
    print('###################')

    #Array de tokens (termino 1-grama) lang=en
    positive_vocab = ['awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)']
    negative_vocab = ['bad', 'terrible', 'useless', 'hate', ':(']
    neutral_vocab = ['movie', 'the', 'sound', 'was', 'is', 'actors', 'did', 'know', 'words', 'not']

    # Características par (token, 'pos/neg/neu') de entrenamiento del modelo
    positive_features = [(procesadoMensaje.word_feats(pos.lower()), 'pos') for pos in positive_vocab]
    negative_features = [(procesadoMensaje.word_feats(neg.lower()), 'neg') for neg in negative_vocab]
    neutral_features = [(procesadoMensaje.word_feats(neu.lower()), 'neu') for neu in neutral_vocab]

    #train_set = positive_features + negative_features + neutral_features
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
    spanish_postagger = StanfordPOSTagger(os.path.join(dir_path, 'standford/models/spanish.tagger'), os.path.join(dir_path, 'standford/stanford-postagger.jar'), encoding='utf8')

    posTag = []
    for sentencia in sent_tokenize(sentence.lower()):
      posTag = posTag + spanish_postagger.tag(word_tokenize(sentencia))

    print('POSTAG', posTag)
    nombres = []
    for wordTag in posTag:
      if 'nc' in wordTag[1]:
        nombres.append(wordTag)

    print('NOMBRES', nombres)

    from nltk.tokenize import RegexpTokenizer

    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(sentence)

    #words = sentence.split(' ')
    for word in words:
      #classResult_ES = classifier_ES.classify(procesadoMensaje.word_feats(ss.stem(word.lower())))
      classResult1_ES = classifier1_ES.classify(procesadoMensaje.word_feats(word.lower()))
      classResult2_ES = classifier2_ES.classify(procesadoMensaje.word_feats(word.lower()))
      classResult3_ES = classifier3_ES.classify(procesadoMensaje.word_feats(word.lower()))

      classResult_ES = procesadoMensaje.ponderarClasificación([classResult1_ES, classResult2_ES, classResult3_ES])

      if ((word.lower() not in stopWords) and (word.lower() not in nombres[0])) or (word.lower() in 'no') or (word.lower() in 'sí'):
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
        print(word,'neg')
      if classResult == 'pos':
        pos = pos + 1
        print(word,'pos')

    print('Positive EN: ' + str(float(pos) / len(words)))
    print('Negative EN: ' + str(float(neg) / len(words)))

    return 0


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

synonyms = []
antonyms = []

for syn in wordnet.synsets("big"):
  for lemma in syn.lemmas():
    synonyms.append(lemma.name())
    for anton in lemma.antonyms():
      antonyms.append(anton.name())

print(synonyms)
print(antonyms)

print('WORDNET 3.0 lang="es"')
print('#######', dir_path)
from nltk.corpus.reader import XMLCorpusReader

#reader = XMLCorpusReader(os.path.join(dir_path + '\wordnet3'), '.*\.xml')
reader = XMLCorpusReader(os.path.join(dir_path + '\wordnet3'), 'wn_synset.xml')

print(nltk.corpus.gutenberg.fileids())
print(nltk.corpus.wordnet.fileids())
print(nltk.corpus.wordnet.words())
#print(nltk.corpus.wordnet.sents())
print(reader.fileids())
#print(reader.words('wn_synset.xml'))
print(reader.words())


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

print("before __name__ guard")

if __name__ == '__main__':
  print('FRASES Y TOKENS')
  print('STOPWRODS')
  # tokenizado()

  print('RAICES')
  # raices()

  print('POS-TAG')
  # postag()

  print('NOMBRES/GENERO')
  # genero()

  print('SENTIMIENTO')
  # sentimiento()

  print('SINONIMOS')
  print('LEMAS')

print("after __name__ guard")