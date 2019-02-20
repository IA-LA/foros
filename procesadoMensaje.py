import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

#SENTIMIENTO POSITIVO NEGATIVO
# pondera la clasificación
def ponderarClasificación(clasificaciones):
  clasificacion = ''
  n = 0
  for c in clasificaciones:
    if(clasificaciones.count(c) > n):
      n = clasificaciones.count(c)
      clasificacion = c
    #print(c, clasificacion, clasificaciones.count(c))
  return clasificacion

# diccionario !!!!!!
def word_feats(words):
  return dict([(word, True) for word in words])

#NOMBRES DE GENERO
def gender_features3(palabra):
  return {'first_letter': palabra[0], 'last_letter': palabra[-1], 'length': len(palabra), 'ngramas': len(palabra.split(' '))}

def gender_features2(palabra):
  return {'first_letter': palabra[0], 'last_letter': palabra[-1], 'length': len(palabra)}

def gender_features1(palabra):
  return {'first_letter': palabra[0], 'last_letter': palabra[-1]}

def gender_features(word):
  return {'last_letter': word[-1]}

def sum( arg1, arg2 ):
  # Add both the parameters and return them."
  total = arg1 + arg2
  print ("Inside the function : ", total)
  return total;

data = "All work and no play makes jack dull boy. All work and no play makes jack a dull boy."
mensaje = "All work and no play makes jack dull boy. All work and no play makes jack a dull boy. Mierda para tu puta madre. Caca de la vaca, para el resto"

# TOKENIZADO
# FRASES
tokens = word_tokenize(data)
frases = sent_tokenize(data)

#1
longitudCaracteres = len(data)
numeroClicks = longitudCaracteres
#2
numeroTokens = len(tokens)
numeroFrases = len(frases)

# Pendiente de Calcular
longitudMediaTokens = 0.0
longitudMediaFrases = 0.0

print(frases)
print(tokens)

# STOPWRODS
stopWords = set(stopwords.words('spanish'))
palabras = []

for t in tokens:
  if t not in stopWords:
    palabras.append(t)

print("before __name__ procesadoMensaje guard")
#if __name__ == '__main__':
if __name__ == 'procesadoMensaje':
  print(gender_features1('main'))
  print(gender_features2('main'))
  print(gender_features3('main'))
print("after __name__ procesadoMensaje guard")