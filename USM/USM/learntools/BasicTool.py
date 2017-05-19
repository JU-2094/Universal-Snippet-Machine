#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Utils:

    def create_page(self, body, name):
        file = "web%s.html" % name
        with open(file, 'wb') as f:
            f.write(body)

    def get_query(self, file):
        with open(file, 'r') as f:
            for line in f:
                yield line