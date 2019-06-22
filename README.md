# foros
- Foros anotados
- Nltk (frase, palabra, raíz, PoS, género, sentimiento, ant/sinónimo, lematization, n-grama)
- Modelado supervisado de agrupamiento y clasificación

# parserForos
- Fuentes foros
- Extración de información
- Características cuantitivas y cualitativas del HILO (en base a Foro, Mensaje y Autor)

# Diagrama de Clases:
          
                           
                           
                       Asignatura     
                       ==========     
                           |
         Adjutnos         Foro                                               K-medias SOM           ... 
              \           ==== \                                                 |_____|_______ ...__|
                \           |   \                                                            |                
                  \         |    \                                                           |
                    \       |     \                                                          |                  
      Características -- Mensaje -------------- [Hilo]                                   Clustering
                     /   =======  /              ====                                    ==========
                   /        |    /                 |--- Caracteristicas                      |
                 /          |   /                       ===============                      |
               /            |  /                               |_____________________________|
             /           Usuario                               |
         Texto           =======                               |
           |                                                   | 
           |_______ Analisis                                   |_________________  Clasificacion
                    ========            _________________________________________  =============
                        |              /      |                                          |
                        |             /       |                                          | 
          ______________|____________/________|                         _________________|________...__
         |        |        |        |         |                        |           |         |   |     |
     tokenizado  raices   postag  genero  sentimiento              NaïveBayes  NaïveBayes+  AD  SVM   ...
     ----------  ------   ------  ------  -----------              ---------   -----------  --  ---

## Tabla de datos
| Asinatura     | Foro          | Usuario   | Mensaje   | Hilo      |
| ------------- | :------------:| :--------:| :-------- | :--------:|
| nombre        | título        | id        | texto     | id        |
| nombre        | título        | id        | texto     | id        |
| nombre        | título        | id        | texto     | id        |
| nombre        | título        | id        | texto     | id        |
| nombre        | título        | id        | texto     | id        |