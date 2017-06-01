#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Todo: Special Selector for https://academic.microsoft.com/ and http://www.sciencedirect.com/ , academia.edu
# Todo: fill DB
# Todo: adapt all the spiders to storage the id of person
"""
Script wich executes the spiders to storage the data. The query to the file with names must
be changed.

Todo.
how to import sql .sql 
142 y 101 , 129  Rows

Busqueda **
    Persona ** 
        Snippets

Abrir base de datos en máquina
Usar datos existentes y los de Theo
    Escribir datos BLOQUEA CON 2 [s], seguir probando
        Hasta bloqueo
    Ampliar (combinaciones), Extraer sintagmas nominales, 
    
    Extraer en la tabla persona
        Tema
        Instituciones
        Lugares


    Tomar en cuenta la prob de ocurrencia de un nombre
    Extraer del censo los nombres y sacar prob.
    
    
    id  -- busqueda
        id -- persona
            hacer combinaciones de datos
            aplicar filtro
            guardar en db
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = "Josué Fabricio Urbina González"

query = "select up.id,up.busqueda_id,up.name,up.geo,up.orgs,up.topics " \
        "from unoporuno_busqueda as ub join unoporuno_persona as up " \
        "where (ub.id=142 or ub.id=101 or ub.id=129) and ub.id=up.busqueda_id;"

process = CrawlerProcess(get_project_settings())

# Spiders to be executed
process.crawl("googlespider", file=query)
process.crawl("bingspider", file=query)
process.crawl("duckspider", file=query)
process.crawl("citespider", file=query)
process.start()
