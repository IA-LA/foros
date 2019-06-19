""""
Created on 15-01-2019

@author: Aitor Diaz Medina
"""

from ParserPlano import *
from Funciones import *
import re

if __name__ == '__main__':

    rutafichero = os.path.splitext(sys.argv[1])[0]

    print('Generando 1', os.path.splitext(sys.argv[1])[0], sys.argv[1], sys.argv[2])
    lista_de_mensajes = parserPlano(convertir_utf8(sys.argv[1]), sys.argv[2])

    ## LIMPIEZA de Mensajes ([IMAGE: ] y FOROS Profesor-Tutor ##
    print('\nGenerando 1 Mensaje', re.compile('\(.*\)\,').split(lista_de_mensajes[0]['Texto mensaje']))
    ## limpiarImagenMensaje('[IMAGE:.')

    ## .CSV ##
    print('\nGenerando 1 .CSV', os.path.splitext(sys.argv[1])[0], parserPlano(convertir_utf8(sys.argv[1]), sys.argv[2])[0])
    ruta = generar_csv(rutafichero, parserPlano(convertir_utf8(sys.argv[1]), sys.argv[2]))

    ## .XSL ##
    print('\nGenerando 1 .XLS', ruta)
    # QUITADO EJECUCION-RAPIDA
    escribir_excel(leer_archivo(ruta), rutafichero, 'General')

    ejecutarFunciones(rutafichero)
