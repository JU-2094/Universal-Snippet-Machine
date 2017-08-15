#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Todo: Special Selector for https://academic.microsoft.com/ and http://www.sciencedirect.com/ , academia.edu
# Todo: fill DB
# Todo Adaptar al codigo de Theo con json

# Todo Freeling, when detecting the language check if all configuration files exits

# Todo: GoogleSearch spider, check for CITE , sometimes is not complete
"""
Script wich executes the spiders to storage the data. The query to the file with names must
be changed.


142 y 101 , 129  Rows in tables    
        
"""
"""
        
        NOTE: Google -> with 4 seconds realizes is a bot
        -------------------------------------------------------------
        Todo 
        Learn about this
        LSTM Long short time memory  neural network

        Filtro nominal
                Filtro semantico
                        LSTM
        
        ---------------
        
        U - Instalación de keras, para LSTM, done
        
        Repetir el experimento de JAPTAL'2012 con lstm en ves de svm 
                . Probar acc. de filtro nominal                 - H = Jorge
                . mejoras de antiguo clasificador.      Freeling. 
                        . entidades nombradas
                        . topónimos             
                        rapido que no tome hrs
                . activar el NER classifier freeling        -U.  DONE
                . juegos de datos:
                        . los mismos en JAPTAL'2012
                        . corpus conacyt fernando
                
        SLACK viernes 7 Julio
                a las 11 @jorge
                
                        
        checar unoporuno_svm_person_classification
            testing set 101,   uruguayos
            
            aprendizaje
            748
            142 For scientometric_corrected - 477,  aprendizaje
            
        
            
        ---
        
        
        Para el filtro nominal es la 119
        
        
        TODO
        
        - get snippets from web search of all Fernando
        with nominal filter
        EXCEL
        
        
        -PENDING THE LSTM WITH THE SEMANTIC FILTER
                
                -how to vectorize the snippets
                -skipgram, CBOW, etc?
                
                
                -LSTM
                Using---        Keras
                
                testing 50 personas
                trainning lo demás
        
                
        csv or json or database
        
        
        todo 
        adapt everything so it could be a function
        generate_query(name,"words..")
        
        take the keywords list and plup paste it
        
        create more queries with the nominal filter     ..?
        
        put the engine searcher - and number
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = "Josué Fabricio Urbina González"

query = "select up.id,up.busqueda_id,up.name,up.geo,up.orgs,up.topics " \
        "from unoporuno_busqueda as ub join unoporuno_persona as up " \
        "where (ub.id=142 or ub.id=101 or ub.id=129) and ub.id=up.busqueda_id;"
path_file1 = "/home/urb/PycharmProjects/unoporuno_scrapy/USM/USM/Data/Data_1996_2005_9308.csv"
path_file2 = "/home/urb/PycharmProjects/unoporuno_scrapy/USM/USM/Data/Data_Junio_1996_4851.csv"

process = CrawlerProcess(get_project_settings())

# Spiders to be executed
# Example for using the query
# todo adaptar lo de vlady

process.crawl("googlespider", source=query)
process.crawl("bingspider", source=query)
process.crawl("duckspider", source=query)
process.crawl("citespider", source=query)
process.start()

#process.crawl("googlespider", source=path_file1, type="1")
#process.start()