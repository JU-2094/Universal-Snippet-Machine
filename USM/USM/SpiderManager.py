#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Todo: Special Selector for https://academic.microsoft.com/ and http://www.sciencedirect.com/ , academia.edu
# Todo: fill DB
# Todo Adaptar al codigo de Theo con json
# Todo Hacer filtros para los features

"""
Script wich executes the spiders to storage the data. The query to the file with names must
be changed.


142 y 101 , 129  Rows in tables    
"""
"""
gazet -> Lista de palabras
Si está contenida 

Name -> Parser de la grámatica para hacer combinaciones

Features
        - Nombre presente  
                - Usando one-hot encoded
                compresión. artículo Jorge
        - Lugar
                -one-hot       
                Lugar de méxico y de Francia
        - Tema
                -Jorge            match  ...  ???
        - Organizaciones
        
        NOTE: Google -> with 4 seconds realizes is a bot
        -------------------------------------------------------------
        Todo 
        Learn about this
        LSTM Long short time memory  neural network

        Filtro nominal
                Filtro semantico
                        LSTM

        Add  what has been search in the dump data... because fuck it         
        
        ---------------
        
        U - Ver que modulos usar para el LSTM...
        
        Repetir el experimento de JAPTAL'2012 con lstm en ves de svm 
                . Probar acc. de filtro nominal                 - H = Jorge
                . mejoras de antiguo clasificador.      Freeling. 
                        . entidades nombradas
                        . topónimos             
                        rapido que no tome hrs
                . intentar la ultima versión de freeling        -U, H
                . juegos de datos:
                        . los mismos en JAPTAL'2012
                        . corpus conacyt fernando
        ---
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = "Josué Fabricio Urbina González"

query = "select up.id,up.busqueda_id,up.name,up.geo,up.orgs,up.topics " \
        "from unoporuno_busqueda as ub join unoporuno_persona as up " \
        "where (ub.id=142 or ub.id=101 or ub.id=129) and ub.id=up.busqueda_id;"

process = CrawlerProcess(get_project_settings())

# Spiders to be executed
process.crawl("googlespider", source=query)
process.crawl("bingspider", source=query)
process.crawl("duckspider", source=query)
process.crawl("citespider", source=query)
process.start()
