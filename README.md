# foros
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
                      _________________|__________________              _________________|______________________...
                     |        |        |        |         |            |                 |                  |
                tokenizado  raices   postag  genero  sentimiento   NaïveBayes       NaïveBayes+             AD  ... SVM, etc.
                ----------  ------   ------  ------  -----------   ---------        -----------             --               