""""
Created on 15-01-2019

@author: Aitor Diaz Medina
"""

from ParserPlano import *
from Funciones import *

if __name__ == '__main__':
    nombrefichero = os.path.splitext(sys.argv[1])[0]
    print('Generando fichero CSV')
    ruta = generar_csv(nombrefichero, parserPlano(convertir_utf8(sys.argv[1]), sys.argv[2]))
    #escribir_excel(leer_archivo(ruta), nombrefichero, 'General')
    ejecutarFunciones(nombrefichero)
