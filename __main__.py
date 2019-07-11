# Módulos propios
from procesadoGeneral import *

print("before __name__ guard")

## PROGRAMA PRINCIPAL ##
########################
if __name__ == '__main__':

    print('FRASES Y TOKENS')
    print('STOPWRODS')
    tokenizado()

    print('RAICES')
    enraizado()

    print('POS-TAG')
    postag()

    print('NOMBRES/GENERO')
    # genero()

    print('SENTIMIENTO')
    # sentimiento()

    print('SINONIMOS')
    # sinonimos()
    print('LEMAS')
    # lemas()

print("after __name__ guard")
