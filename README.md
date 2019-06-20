# foros
NLP (token stem), Lematization, Synonim, PoS y Sentinel
## Diagrama de Clases:
                                                                                          
                           Foro
                           ====
                            |
                            |
                            |
          Contenidos       Hilo                               K-medias    SOM    ...     
               \           ====                                  |_________|____ ... _____|
                 \          |                                                              
                   \        |                                              |
                     \      |                                              |                  
         Tipo -------- [ Mensaje ] _________  Caracteristicas          Clustering
                         =======              ===============          ==========
                            |                        |                     |
                            |                        |                     |
                            |                        |_____________________|
                         Usuario                               |
                         =======                               |
                                    Analisis  _________________|__________________  Clasificacion
                                    ========                                        =============
                                       |                                                 |
                                       |                                                 | 
                      _________________|__________________              _________________|_______...__
                     |        |        |        |         |            |           |         |        |
                tokenizado  raices   postag  genero  sentimiento   NaïveBayes  NaïveBayes+   AD  ... SVM, etc.
                ----------  ------   ------  ------  -----------   ---------   -----------   --       --
               