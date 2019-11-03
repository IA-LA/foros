import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# PARTE TEXTO EN TOKENS HASTA 72(n) CARACTERES
def parte_texto(texto, n):
    texto_partido = ''
    contador = 0
    for index, c in enumerate(texto):
        if contador >= n and c == ' ':
            texto_partido += c + '\n'
            contador = 0
        else:
            texto_partido += c
            contador += 1
    return texto_partido

# DISTANCIA ENTRE TERMINOS
def distancia_combinada(token_a, token_b):
    # VOCALES ['a', 'á', 'e', 'é', 'i', 'í', 'o', 'ó', 'u', 'ú']
    vocal = ['a', 'e', 'i', 'o', 'u']
    vocal_acentuada = ['á', 'é', 'í', 'ó', 'ú']
    # VOCALES QWERTY ['a', '', 'e', '', '', '', 'i', 'o', 'u']
    # CONSONANTES ['b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    consonante = ['b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    # CONSONANTES QWERTY ['q', 'w', '', 'r', 't', 'y', '', '', '', 'p']
    consonante_acentuada = []
    token1 = token_a.lower()
    token2 = token_b.lower()
    levenshtein = nltk.edit_distance(token1, token2)
    jaccard = nltk.jaccard_distance(set(token1), set(token2))

    # PARA PALABRAS SEMEJANTES
    similaridad = 0.0 # if anterior o posterior
    c1_ant = ''
    c2_ant = ''
    semejanza = 0.0
    if abs(len(token1) - len(token2)) <= 1:
        # VOCALES
        for c1, c2 in zip(token1, token2):
            if c1 in vocal or c1 in vocal_acentuada:
                if c2 in vocal or c2 in vocal_acentuada:
                    # print("VOCALES", c1, c2)
                    # DISTANCIA EN EL TECLADO QWERTY
                    # DISTANCIA TECLADO ASDF G H JKLÑ´Ç
                    if c1 in vocal:
                        if c2 in vocal:
                            # print("\tNO ACENTUADAS", vocal.index(c1)-vocal.index(c2))
                            semejanza += abs(vocal.index(c1)-vocal.index(c2))
                        else:
                            # print("\tNO ACENTUADA", vocal.index(c1)-vocal_acentuada.index(c2))
                            semejanza += abs(vocal.index(c1)-vocal_acentuada.index(c2))
                        # DIVERGENCIA DISLEXICA
                        if c1 == c2_ant and c2 == c1_ant:
                            similaridad += 1
                    elif c1 in vocal_acentuada:
                        if c2 in vocal_acentuada:
                            # print("\tACENTUADAS", vocal_acentuada.index(c1)-vocal_acentuada.index(c2))
                            semejanza += abs(vocal_acentuada.index(c1)-vocal_acentuada.index(c2))
                        else:
                            # print("\tACENTUADA", vocal_acentuada.index(c1)-vocal.index(c2))
                            semejanza += abs(vocal_acentuada.index(c1)-vocal.index(c2))
                        # DIVERGENCIA DISLEXICA
                        if c1 == c2_ant and c2 == c1_ant:
                            similaridad += 1
                else:
                    # print("VOCAL DIVERGENCIA", c1, c2, c1_ant, c2_ant)
                    # DIVERGENCIA DISLEXICA
                    if c1 == c2_ant and c2 == c1_ant:
                        similaridad += 1
            # CONSONANTES
            if c1 in consonante or c1 in consonante_acentuada:
                if c2 in consonante or c2 in consonante_acentuada:
                    # print("CONSONANTES", c1, c2)
                    # DISTANCIA EN EL TECLADO QWERTY
                    # DISTANCIA TECLADO ASDF G H JKLÑ´Ç
                    if c1 in consonante:
                        if c2 in consonante:
                            # print("\tNO ACENTUADAS", consonante.index(c1)-consonante.index(c2))
                            semejanza += abs(consonante.index(c1)-consonante.index(c2))
                        else:
                            # print("\tNO ACENTUADA", consonante.index(c1)-consonante_acentuada.index(c2))
                            semejanza += abs(consonante.index(c1)-consonante_acentuada.index(c2))

                        # DIVERGENCIA DISLEXICA
                        if c1 == c2_ant and c2 == c1_ant:
                            similaridad += 1
                    elif c1 in consonante_acentuada:
                        if c2 in consonante_acentuada:
                            # print("\tACENTUADAS", consonante_acentuada.index(c1)-consonante_acentuada.index(c2))
                            semejanza += abs(consonante_acentuada.index(c1)-consonante_acentuada.index(c2))
                        else:
                            # print("\tACENTUADA", consonante_acentuada.index(c1)-consonante.index(c2))
                            semejanza += abs(consonante_acentuada.index(c1)-consonante.index(c2))
                        # DIVERGENCIA DISLEXICA
                        if c1 == c2_ant and c2 == c1_ant:
                            similaridad += 1
                else:
                    # print("CONSONANTE DIVERGENCIA", c1, c2, c1_ant, c2_ant)
                    # DIVERGENCIA DISLEXICA
                    if c1 == c2_ant and c2 == c1_ant:
                        similaridad += 1
            # Actualiza caracteres anteriores
            c1_ant = c1
            c2_ant = c2

    # print("CONSTANTE DE SIMILARIDAD : ", similaridad/100)
    # print("CONSTANTE DE SEMEJANZA   : ", semejanza/100)

    # POTENCIA LAS FALTAS DE ORTOGRAFIA EN LAS TILDES (con len())
    # Y LOS ERRORES POR DISLEXIA (CON TODAS LAS LETRAS BIEN ESCRITAS con 2^Jaccard)
    # DISTANCIAS     Longitud      Levenshtein      Jaccard         (Rodríguez)
    # DISTANCIAS 0.05130164500296486    1       0.2                 (Rodriguez)
    # DISTANCIAS 1.0                    2       0.0                 (Rodírguez)
    # DISTANCIAS 1.0                    2       0.0                 (Rodrígeuz)
    # DISTANCIAS 1.031051372218805      1       0.1111111111111111  (Rodrguez)
    # DISTANCIAS 1.031051372218805      1       0.1111111111111111  (Rodíguez)
    # DISTANCIAS 1.051301645002965      2       0.2                 (Rodígiuez)
    # DISTANCIAS 3.0                    4       0.0                 (Rodírgeuz)

    if len(token1) > 4 and len(token2) > 4:
        distancia = abs(abs(len(token1)-len(token2)) + levenshtein + jaccard -
                        (2**jaccard) + (-similaridad/100 + semejanza/100)/0.125)
    else:
        distancia = abs(abs(len(token1) - len(token2)) + levenshtein + jaccard)

    return distancia


# SENTIMIENTO POSITIVO NEGATIVO
# pondera la clasificación
def ponderarClasificacion(clasificaciones):
    clasificacion = ''
    n = 0
    for c in clasificaciones:
        if(clasificaciones.count(c) > n):
            n = clasificaciones.count(c)
            clasificacion = c
        # print(c, clasificacion, clasificaciones.count(c))
    return clasificacion


# diccionario !!!!!!
def word_feats(words):
    return dict([(word, True) for word in words])


# NOMBRES DE GENERO
def gender_features3(palabra):
    return {'first_letter': palabra[0], 'last_letter': palabra[-1],
            'length': len(palabra), 'ngramas': len(palabra.split(' '))}


def gender_features2(palabra):
    return {'first_letter': palabra[0], 'last_letter': palabra[-1], 'length': len(palabra)}


def gender_features1(palabra):
    return {'first_letter': palabra[0], 'last_letter': palabra[-1]}


def gender_features(word):
    return {'last_letter': word[-1]}


def sum(arg1, arg2):
  # Add both the parameters and return them."
  total = arg1 + arg2
  print ("Inside the function : ", total)
  return total


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
# if __name__ == '__main__':
if __name__ == 'procesadoMensaje':
    print(gender_features1('main'))
    print(gender_features2('main'))
    print(gender_features3('main'))
print("after __name__ procesadoMensaje guard")
