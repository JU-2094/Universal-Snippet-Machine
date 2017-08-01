#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql as sql

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
