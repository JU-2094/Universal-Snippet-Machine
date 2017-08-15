#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql as sql
import pandas as pd
import math

__author__ = "Josué Fabricio Urbina González"


class Utils:

    user = "root"
    pswd = "876123jo"
    name_db = "conacyt"
    host_db = "localhost"

    def create_page(self, body, name):
        file = "web%s.html" % name
        with open(file, 'wb') as f:
            f.write(body)

    # def get_query(self, file):
    #     with open(file, 'r') as f:
    #         for line in f:
    #             yield line

    def make_combination(self, values):
        name = values[0]
        for x in values[1:]:
            for v in x.split(";"):
                if v != "":
                    val = name + ", " + v
                    yield(val)

    def get_query(self, query):
        # search in database with this query and do the permutations
        db = sql.Connect(self.host_db, self.user, self.pswd, self.name_db)
        cursor = db.cursor()

        try:
            cursor.execute(query)
        except:
            db.rollback()
        results = cursor.fetchall()
        db.close()

        for row in results:
            id = row[0]
            vals = row[2:]
            for search in self.make_combination(vals):
                yield (id, vals, search)

    def exec_query(self, query):
        db = sql.Connect(self.host_db, self.user, self.pswd, self.name_db)
        cursor = db.cursor()

        try:
            cursor.execute(query)
        except:
            db.rollback()
        results = cursor.fetchall()
        db.close()
        return results

    def read_csv(self, file):
        return pd.read_csv(file)

    def get_query_csv(self, df):
        l = df.index.values
        for i in range(1, len(l)):
            id = df.loc[l[i], 'REGISTRO']
            name = df.loc[l[i], 'NOMBRE']
            for search in self.make_combination_csv(df, l[i]):
                yield (id, name, search)

    def make_combination_csv(self, df, index):
        # REGISTRO, NOMBRE, PAÍS, NOMBRE_COMPLETO_INSTITUCION, NOMBRE CORTO, ÁREA, DISCIPLINA,
        # SUBDISCIPLINA
        name = df.loc[index, 'NOMBRE']
        country = df.loc[index, 'PAÍS']
        org_l = df.loc[index, 'NOMBRE_COMPLETO_INSTITUCION']
        org_s = df.loc[index, 'NOMBRE CORTO']
        spec = df.loc[index, 'ÁREA']
        disc = df.loc[index, 'DISCIPLINA']
        subdisc = df.loc[index, 'SUBDISCIPLINA']

        search = []
        search.append(name)
        search.append(name + ", "+country)
        search.append(name + ", "+org_l)
        search.append(name + ", "+org_s)
        search.append(name + ", "+spec)
        if type(disc) is not float:
            search.append(name + ", "+disc)
        search.append(name + ", "+subdisc)

        for s in search:
            yield s

    def get_query_param(self, src):

        id = src[0]
        attr = src[1]

        search = src[1]
        return id, attr, search
