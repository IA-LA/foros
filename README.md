# foros
NLP (token stem), Lematization, Synonim, PoS y Sentinel
## Diagrama de Clases:
          
                           Foro
                           ====
                            |
                            |
                            |
         Contenidos        Hilo __________                    K-medias    SOM          ... 
               \           ====           |                      |_________|___ ... ____|
                 \          |       Caracteristicas                        |                
                   \        |       ===============                        |
                     \      |             |                                |                  
         Tipo -------- [ Mensaje ]        |                            Clustering
                     /   =======          |                            ==========
                   /        |             |                                |
                 /          |             |                                |
               /            |             |________________________________|
             /           Usuario                               |
         Texto           =======                               |
           |                                                   | 
           |_______ Analisis                                   |__________________  Clasificacion
                    ========                                                        =============
                        |                                                                |
                        |                                                                | 
          ____________________________________                          _________________|________...__
         |        |        |        |         |                        |           |         |         |
     tokenizado  raices   postag  genero  sentimiento              NaïveBayes  NaïveBayes+   AD  ...  SVM, etc.
     ----------  ------   ------  ------  -----------              ---------   -----------   --       ---