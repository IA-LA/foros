
  *Una institución académica, una universidad, se puede juzgar por la forma en que trata a sus alumnos. **— Anónimo

**INDICE DE CONTENIDOS**
1. Introducción
2. Estado del Arte
3. Sistema
4. Experimento
  4.1. Definición de requisitos
  4.2. Análisis de requisitos
  4.3. Diseño
  4.4. Implementación y Pruebas
  4.5. Puesta en producción
5. Resultados y Evaluación
6. Conclusiones
7. Bibliografía

# Foros
  NLP (token stem), Lematization, Synonim, PoS y Sentinel
## Diagrama de Clases:
                                                                                          
                                                                                |_________|_________| 
                                                                                          |                  
    [ Mensaje ] ______________________________________  Caracteristicas                   |
      =======                                           ===============               Clustering
                                                               |                      ==========
                                                               |                           |
                                                               |___________________________|
                                                               |
                                                               |
                                    Analisis  _________________|__________________  Clasificacion
                                    ========                                        =============
                      _________________|__________________              _________________|________...
                     |        |        |        |         |            |           |          |
                tokenizado  raices   postag  genero  sentimiento   NaïveBayes  NaïveBayes+    AD  ... SVM, etc.
                ----------  ------   ------  ------  -----------   ---------   -----------    --               
