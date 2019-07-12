# foros
- Foros anotados (Corpus)
- PLN: Nltk (a nivel de frase, palabra, raíz, PoS, género, sentimiento, ant/sinónimo, lematization, n-gramas)
- Aprendizaje Automático: modelado supervisado de agrupamiento y clasificación

# parserForos
- Fuentes foros
- Extración de información (RI)
- Extracción de características cuantitivas y cualitativas del HILO (en base a Asignatura, Foro, Mensaje y Autor)

# Diagrama de Clases:
          
                           
                           
                       Asignatura     
                       ==========     
                           |
         Adjutnos         Foro                                               K-medias SOM           ... 
              \           ==== \                                                 |_____|_______ ...__|
                \           |   \                                                            |                
                  \         |    \                                                           |
                    \       |     \                                                          |                  
      Características -- Mensaje __\____________ [Hilo] ________                          Clustering
                     /   =======   /              ====          |                         ==========
                   /        |     /                      Caracteristicas                      |
                 /          |    /                       ===============                      |
               /            |   /                               |                             |
             /           Usuario                                |                             |
         Texto           =======                     Aprendizaje Automático __________________|
           |                                         ======================              |
           |_______ Analisis NLP                                                         |
                    ============                    _______________________________ Clasificacion
                        |                          /      |                         =============
                        |                         /       |                              | 
          ______________|_______________________ /________|                         _____|_____________________...__
         |   |     |    |           |           |         |                        |           |         |   |     |
     token  raíz  PoS  Freq.D.  Topic Mod.   genero  sentimiento              NaïveBayes  NaïveBayes+  AD  SVM   ...
     -----  ----  ---  -------  ---------    ------  -----------

## Tabla de datos base
| Asignatura    | Foro          | Usuario   | Mensaje   | Hilo      |
| ------------: | --------------| :--------:| --------- | :--------:|
| nombre        | título        | id        | texto     | id        |
| nombre        | título        | id        | texto     | id        |
| nombre        | título        | id        | texto     | id        |
| nombre        | título        | id        | texto     | id        |
| nombre        | título        | id        | texto     | id        |