""""
Created on 09-01-2019

@author: Aitor Diaz Medina

Generación de vistas temporales del csv importado
"""


import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import os

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option("display.max_columns", 10)


def generar_df(input_file):
    df = pd.read_csv(input_file)
    # Anonimizado
    df['Texto mensaje'] = '(Borrado)'
    # Campo temporal
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M:%S')

    return df


def escribir_csv(df, nombre_archivo):
    df.to_csv(nombre_archivo, encoding='utf-8')
    print('Fichero CSV creado: ' + nombre_archivo)


def escribir_excel(df, nombre_archivo, nombre_hoja):
    print(nombre_archivo, nombre_hoja)
    excel = nombre_archivo + ".xlsx"
    if not os.path.isfile(excel):
        with pd.ExcelWriter(excel, datetime_format='dd/mm/yyyy', date_format='dd/mm/yyyy', time_format='hh:mm:ss') as writer:
            df.to_excel(writer, sheet_name=nombre_hoja, engine='xlsxwriter')
    else:
        with pd.ExcelWriter(excel, datetime_format='DD/MM/YYYY', date_format='DD/MM/YYYY', time_format='HH:MM:SS', mode='a') as writer:
            df.to_excel(writer, sheet_name=nombre_hoja, engine='xlsxwriter')
    print('Fichero Excel creado: ', excel)


def distribucion_temporal_dias_semana(input_file, export_file):
    df = generar_df(input_file)

    # Poblema formato Fechas y Horas
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    # Fin Poblema formato Fechas y Horas

    # ordenar dataframe
    sorted_df = df.sort_values(by='Fecha').set_index("Mensaje", drop=False)
    sorted_df['Día'] = pd.Categorical(sorted_df['Día'],
                                      ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
    # agrupar por día
    df_dias = sorted_df.groupby('Día')
    df_def = df_dias.size().reset_index(name='Total')
    # print(df_def)

    # Gráfico
    # plt.figure()
    # print(df_def.plot(kind='bar', rot=45, fontsize=10))
    # plt.show(block=True)

    # Generar csv
    # df_def.to_csv('export/dias_semana.csv', index=False)
    escribir_excel(df_def, export_file, 'Temporal días')
    return df_def


def distribucion_temporal_fechas(input_file, export_file):
    df = generar_df(input_file)

    # Poblema formato Fechas y Horas
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    # Fin Poblema formato Fechas y Horas

    # Problema del formato de Fechas
    df['Fecha'] = df['Fecha'].dt.date

    #oredenar por Fecha
    sorted_df = df.sort_values(by='Fecha')

    df_fechas = sorted_df.set_index(["Fecha", "Mensaje"]).count(level="Fecha")

    index = pd.date_range(sorted_df['Fecha'].min(), sorted_df['Fecha'].max(), freq='D')
    # reindex the DataFrame
    df_reindexed = df_fechas.reindex(index)

    df_def = df_reindexed.loc[:, 'Foro']

    df_def2 = df_def.to_frame()
    # cambiar nombre de la columna del dataframe
    df_def2.columns = ['Total']
    # cambiar NaN por 0 y pasar a tipo integer
    df_def2 = df_def2.fillna(0)
    df_def2['Total'] = df_def2['Total'].astype(np.int64)
    # poner la fecha de indice del dataframe
    df_def2.index.names = ['Fecha']

    # print(df_def2)

    # Gráfico
    # plt.figure()
    # print(df_def2.plot(kind='bar', fontsize=4))
    # plt.show(block=True)

    # Generar el csv
    # escribir_csv(df_def2, 'export/fechas.csv')
    escribir_excel(df_def2, export_file, 'Temporal fechas')
    return df_def2


def distribucion_temporal_rango_horas(input_file, export_file):
    df = generar_df(input_file)

    # Poblema formato Fechas y Horas
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    # Fin Poblema formato Fechas y Horas

    # sorted_df = df.sort_values(by='Fecha')
    # index = pd.date_range(sorted_df['Fecha'].min(), sorted_df['Fecha'].max(), freq='D')

    # Problema del formato de Fechas
    df['Fecha'] = df['Fecha'].dt.date

    # Agrupa Horas por Fecha
    df_rango_horas = df.groupby([df.Fecha, df.Día, pd.Grouper(key='Hora', freq='4H')]).size()
    print(df_rango_horas)

    # df_reindexed = df_rango_horas.reindex(index)
    # print(df_reindexed)

    df_rango_horas_def = df_rango_horas.unstack()
    df_rango_horas_def.columns = ['de 0:00 a 4:00', 'de 4:00 a 8:00', 'de 8:00 a 12:00', 'de 12:00 a 16:00', 'de 16:00 a 20:00', 'de 20:00 a 24:00']
    df_rango_horas_def = df_rango_horas_def.fillna(0)
    df_rango_horas_def = df_rango_horas_def.astype(np.int64)

    # print(df_rango_horas_def)

    # escribir_csv(df_rango_horas_def, 'export/rango_horas.csv')
    escribir_excel(df_rango_horas_def, export_file, 'Temporal Rango horas')
    return df_rango_horas_def


def distribucion_personas_dias(input_file, export_file):
    df = generar_df(input_file)

    # Poblema formato Fechas y Horas
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    # Fin Poblema formato Fechas y Horas

    # ordenar por fecha y los dias de la semana
    sorted_df = df.sort_values(by='Fecha').set_index("Mensaje", drop=False)
    sorted_df['Día'] = pd.Categorical(sorted_df['Día'],
                                      ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
    # agrupar por remitente y dia de la semana
    df_rango_semanas = sorted_df.groupby([sorted_df.Autor, sorted_df.Remitente, sorted_df.Día]).size()  # .reset_index(name='count')
    df_rango_semanas_def = df_rango_semanas.unstack()

    # cambiar a integer y NaN por 0s
    df_rango_semanas_def = df_rango_semanas_def.fillna(0)
    df_rango_semanas_def = df_rango_semanas_def.astype(np.int64)

    # print(df_rango_semanas_def)
    # escribir_csv(df_rango_semanas_def, 'export/personas_dias_semana.csv')
    # escribir_excel(df_rango_semanas_def, export_file, 'Personas días')
    return df_rango_semanas_def


def distribucion_personas_horas(input_file, export_file):
    df = generar_df(input_file)

    # Poblema formato Fechas y Horas
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    # Fin Poblema formato Fechas y Horas

    # agrupar por remitente y rango de horas
    df_personas_rango_horas = df.groupby([df.Autor, df.Remitente, pd.Grouper(key='Hora', freq='4H')]).size()  # .reset_index(name='count')
    df_def = df_personas_rango_horas.unstack()
    df_def.columns = ['de 0:00 a 4:00', 'de 4:00 a 8:00', 'de 8:00 a 12:00', 'de 12:00 a 16:00', 'de 16:00 a 20:00', 'de 20:00 a 24:00']

    # cambiar a integer y NaN por 0s
    df_def = df_def.fillna(0)
    df_def = df_def.astype(np.int64)

    # print(df_def)
    # escribir_csv(df_def, 'export/personas_horas.csv')
    # escribir_excel(df_def, export_file, 'Personas horas')
    return df_def


def distribucion_personas_dias_horas(input_file, export_file):
    df_personas_dias = distribucion_personas_dias(input_file, export_file)
    df_personas_horas = distribucion_personas_horas(input_file, export_file)

    # print(df_personas_dias)
    # print(df_personas_horas)
    # print(df_personas_dias.info(), df_personas_horas.info())
    df = pd.merge(df_personas_horas, df_personas_dias, on=['Remitente', 'Autor'])

    # print(df)
    # escribir_csv(df, 'export/personas_horas_dias.csv')
    escribir_excel(df_personas_dias, export_file, 'Personas dias')
    escribir_excel(df_personas_horas, export_file, 'Personas horas')
    escribir_excel(df, export_file, 'Personas horas días')
    return df


def distribucion_personas_semanas(input_file, export_file):
    df = generar_df(input_file)

    # Poblema formato Fechas y Horas
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Hora'] = pd.to_datetime(df['Hora'])
    # Fin Poblema formato Fechas y Horas

    df = df.sort_values(by=['Fecha'], ascending=True)

    df_personas_semanas = df.groupby([df.Autor, df.Remitente, pd.Grouper(key='Date', sort=True, freq='W-MON')]).size()
    # print(df_personas_semanas)

    df_personas_semanas = df_personas_semanas.sort_values()
    df_def = df_personas_semanas.unstack()
    df_def = df_def.fillna(0)
    df_def = df_def.astype(np.int64)
    # print(df_def)

    # Generar el csv
    # escribir_csv(df_def2, 'export/personas_semanas.csv')
    # ruta_excel = os.path.splitext(input_file)[0]
    escribir_excel(df_def, export_file, 'Personas semanas')
    return df_def


# INICIO añadido FJSB
def df_personas_mensajes_fechas_diff(input_file, export_file):
    df = generar_df(input_file)
    # print(df)

    df_ = df.groupby([df.Autor, df.Remitente, df.Date, (df.sort_values(by=['Autor', 'Date']).rename(columns={'Date': 'Diff'}).Diff.diff().astype('timedelta64', copy=False).clip(lower=0)), pd.Grouper(key='Autor')]).size()
    print(df_)

    #exit('ACABOSE')

    df_def = df_.unstack()
    df_def = df_def.fillna(0)
    df_def = df_def.astype(np.int64)
    # print(df_def)

    # Generar el csv
    # escribir_csv(df_def, 'export/hilos_horas.csv')

    # Hoja de Excel
    escribir_excel(df_def, export_file, 'Personas mensajes diff')
    return df_def


def df_personas_mensajes_hilos_fechas_diff(input_file, export_file):
    df = generar_df(input_file)
    # print(df)

    df_ = df.groupby([df.Autor, df.Remitente, df.Hilo, df.Date, (df.sort_values(by=['Autor', 'Hilo', 'Date']).rename(columns={'Date': 'Diff'}).Diff.diff()), pd.Grouper(key='Autor')]).size()
    print(df_)

    df_def = df_.unstack()
    df_def = df_def.fillna(0)
    df_def = df_def.astype(np.int64)
    # print(df_def)

    # Hoja de Excel
    escribir_excel(df_def, export_file, 'Personas mensajes hilos diff')
    return df_def


def df_personas_participacion(input_file, export_file):
    df = generar_df(input_file)
    # print(df)

    df_ = df.groupby(['Autor', 'Remitente']).size().sort_values(ascending=False, na_position='last')
    print(df_)

    df_def = df_
    # print(df_def)

    # Dibujar Gráficas
    #import matplotlib.pyplot as plt

    #In[2]: plt.close('all')
    #In[8]: plt.figure()

    #In[9]: df.plot
    # Fin Dibujar Gráficas

    # Hoja de Excel
    escribir_excel(df_def, export_file, 'Personas participación')
    return df_def


def df_personas_pruebas(input_file, export_file):
    df = generar_df(input_file)

    #print(df)
    #df.sort_values(by=['Autor', 'Remitente', 'Fecha', 'Hora'], ascending=[True, True, True, True])

    #df.sort_values(by=['Autor', 'Remitente', 'Date'], ascending=[True, True, True])
    print(df)
    #df.sort_values(by='Date')
    #df_personas_dias_mensaje = df.groupby([df.Autor, df.Remitente, df.Fecha, pd.Grouper(key='Date', freq='60s')]).size()
    #df_personas_dias_mensaje = df.groupby([df.Autor, df.Remitente, df.Date, (df.Date.diff()).dt.seconds, pd.Grouper(key='Autor')]).size()
    df_personas_dias_mensaje = df.groupby(['Autor', 'Remitente']).size()
    #df_personas_dias_mensaje['Date'] = (df_personas_dias_mensaje['Date'].diff(periods=-1)).dt.days
    #df_personas_dias_mensaje.rename(columns={'Date': 'Date', 'Date': 'DateDiff'})

    #df_personas_dias_mensaje['Diff'] = (df['Date'].diff()).dt.days

    #df_personas_dias_mensaje=df_personas_dias_mensaje.assign('Diff', df_personas_dias_mensaje['Date'].diff()).dt.seconds)
    #import matplotlib.pyplot as plt
    #df_personas_dias_mensaje.plot()
    print("PRUEBASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    print(df_personas_dias_mensaje)

    #df_personas_dias_mensaje_diff = df_personas_dias_mensaje.groupby([df_personas_dias_mensaje.Autor, df_personas_dias_mensaje.Remitente, (df_personas_dias_mensaje['Date'].diff()).dt.seconds])

    #print(df_personas_dias_mensaje_diff)

    #df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    #df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    #df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M:%S')
    #df['Diff'] = (df['Date'].diff()).dt.days

    df_def = df_personas_dias_mensaje
    #df_def = df_personas_dias_mensaje.unstack()
    #df_def.columns = ['Autor', 'Remitente', 'Date', 'Diferencia', 'Autor']
    #df_def = df_def.fillna(0)
    #df_def = df_def.astype(np.int64)
    # print(df_def)

    # Generar el csv
    # escribir_csv(df_def2, 'export/personas_semanas.csv')
    # ruta_excel = os.path.splitext(input_file)[0]
    escribir_excel(df_def, export_file, 'Personas pruebas')
    exit(1)
    return df_def
# FIN Añadido FJSB


def distribucion_hilos_horas(input_file, export_file):
    df = generar_df(input_file)

    # Poblema formato Fechas y Horas
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    # Fin Poblema formato Fechas y Horas

    # agrupar por hilos y rango de horas
    # Problema del formato de Fechas y horas
    df = df.replace(np.nan, '', regex=True)

    #df['Hora'] = df['Hora'].dt.time
    #df['Hora'] = df['Hora'].astype('timedelta64[s]')

    df1 = df[df['Responde a'] == '']

    df_hilos_rango_horas = df1.groupby([pd.Grouper(key='Hora', freq='4H')]).size()
    # print(df_hilos_rango_horas)
    # print(df_hilos_rango_horas.to_frame().info())

    df_def = df_hilos_rango_horas.to_frame(name='Total').reset_index()

    df_def['Hora'] = df_def['Hora'].dt.time
    #df_def.rename(columns={'0': 'Total'})
    #df_def.columns = [['Hora', 'Total']]
    # print(df_def)

    # Generar el csv
    # escribir_csv(df_def, 'export/hilos_horas.csv')
    escribir_excel(df_def, export_file, 'Hilos horas')
    return df_def


# INICIO Añadido FJSB
def df_hilos_pruebas(input_file, export_file):
    df = generar_df(input_file)

    # agrupar por hilos y rango de horas
    # print(df.info())
    df = df.replace(np.nan, '', regex=True)
    df1 = df[df['Responde a'] == '']
    print(df1)
    df_ = df1.groupby([pd.Grouper(key='Hora', freq='4H')], ).size()
    # print(df_)
    # print(df_.to_frame().info())
    df_def = df_.to_frame()
    df_def.columns = [['Total']]
    # print(df_def)

    # Generar el csv
    # escribir_csv(df_def, 'export/hilos_horas.csv')
    escribir_excel(df_def, export_file, 'Hilos horas pruebas')
    return df_def
# FIN Añadido FJSB


def generar_hojas_default(nombrearchivo):
    csv = nombrearchivo + '.csv'

    #Temporal
    distribucion_temporal_dias_semana(csv, nombrearchivo)
    distribucion_temporal_fechas(csv, nombrearchivo)
    distribucion_temporal_rango_horas(csv, nombrearchivo)

    #Personas
    distribucion_personas_dias_horas(csv, nombrearchivo)
    distribucion_personas_semanas(csv, nombrearchivo)

    #hilos
    distribucion_hilos_horas(csv, nombrearchivo)


# INICIO Añadido FJSB
def generar_hojas_base(nombrearchivo):
    csv = nombrearchivo + '.csv'
    nombrearchivo = nombrearchivo + '_base'

    #Temporal
    distribucion_temporal_dias_semana(csv, nombrearchivo)
    distribucion_temporal_fechas(csv, nombrearchivo)
    distribucion_temporal_rango_horas(csv, nombrearchivo)

    #Personas
    distribucion_personas_dias_horas(csv, nombrearchivo)
    distribucion_personas_semanas(csv, nombrearchivo)

    #hilos
    distribucion_hilos_horas(csv, nombrearchivo)


def generar_hojas_ampliada(nombrearchivo):
    csv = nombrearchivo + '.csv'
    nombrearchivo = nombrearchivo + '_ampliado'

    # AMPLIADOS INICIO
    df_personas_mensajes_fechas_diff(csv, nombrearchivo)
    df_personas_mensajes_hilos_fechas_diff(csv, nombrearchivo)
    df_personas_participacion(csv, nombrearchivo)
    # df_personas_pruebas(csv, nombrearchivo)
    # FIN AMPLIADOS

    # hilos
    # df_hilos_pruebas(csv, nombrearchivo)
# FIN Añadido FJSB

