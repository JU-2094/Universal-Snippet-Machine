#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Todo: Special Selector for https://academic.microsoft.com/ and http://www.sciencedirect.com/ , academia.edu
# Todo: fill DB
"""
Script wich executes the spiders to storage the data. The path to the file with names must
be changed.

Todo.
how to import sql .sql 
142 y 101   Rows

Busqueda **
    Persona ** 
        Snippets

Abrir base de datos en máquina
Usar datos existentes y los de Theo
    Escribir datos 
        Hasta bloqueo
    Ampliar (combinaciones), Extraer sintagmas nominales, 
        Tema
        Instituciones
        Lugares

    Tomar en cuenta la prob de ocurrencia de un nombre
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = "Josué Fabricio Urbina González"

path = "/home/urb/PycharmProjects/unoporuno_scrapy/Test_Queries"

process = CrawlerProcess(get_project_settings())

# Spiders to be executed
process.crawl("googlespider", file=path)
process.crawl("bingspider", file=path)
process.crawl("duckspider", file=path)
process.crawl("citespider", file=path)
process.start()
