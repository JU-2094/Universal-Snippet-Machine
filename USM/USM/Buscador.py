#/usr/bin/env python
# -*- coding: utf8 -*-
##
## Copyright (c) 2010-2012 Jorge J. García Flores, LIMSI/CNRS

## This file is part of Unoporuno.

##     Unoporuno is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.

##     Unoporuno is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with Unoporuno.  If not, see <http://www.gnu.org/licenses/>.
##
#      This program is part of CIDESAL.incubator.iteration 1
#
#      The goal is to read name, theme, organization and places of a person from
#       an XML file, to search its information in Google or Yahoo and to
#       filter the result snippets according to the following criteria:
#           : nominal: the snippet correspond to the possible variations of the person's name
#           : thematic: the snippet's topic correspond to the theme and organization topics
#           : biographic: the snippet's source document might containt biographica information \
#                about the person
#
__author__="Jorge García Flores"
__date__ ="$03-abr-2011 10:05:30$"


import nltk


class NameParser:
    def __init__(self):
        self.grammar_head = """
    NC -> N A
    N -> N I
    N -> N AA
    N -> I
    N -> AA
    N -> AG
    N -> AA AD
    A -> AAA
    A -> AAA AA
    A -> AAA AD
    A -> AAA AG
    A -> AAA I
    AAA -> AA
    AAA -> AG
    AAA -> AD
    """
        self.name_tokenizer_regex = r'(Mc[A-Z][a-z]+|O\'[A-Z][a-z]+|[Dd]e\s[Ll]a\s[A-Z][a-z]+|-[Dd]e-[A-Z][a-z]+|[A-Z][a-z]+-[A-Z][a-z]+|[Dd]e\s[Ll]a\s[A-Z][a-z]+|[Vv][oa]n\s[A-Z][a-z]+|[Dd]e[l]?\s[A-Z][a-z]+|[A-Z][\.\s]{1,1}|[A-Z][a-z]+|[Dd]e\s[Ll]os\s[A-Z][a-z]+)'

        self.regexp_tagger_list = [(r'([A-Z][a-z]+-[A-Z][a-z]+|-[Dd]e-[A-Z][a-z]+)', 'AG'),
                                   (r'[A-Z][a-z]+', 'AA'),
                                   (r'[A-Z][\.\s]{1,1}', 'I'),
                                   (
                                   r'([A-Z][a-z]+-[A-Z][a-z]+|[Dd]e\s[Ll]a\s[A-Z][a-z]+|[Vv][oa]n\s[A-Z][a-z]+|[Dd]e[l]?\s[A-Z][a-z]+|[Dd]e\s[Ll]os\s[A-Z][a-z]+)',
                                   'AD'),
                                   (r'(Mc[A-Z][a-z]+|O\'[A-Z][a-z]+)', 'AA')]

        self.tokenizer = nltk.RegexpTokenizer(self.name_tokenizer_regex)
        self.tagger = nltk.RegexpTagger(self.regexp_tagger_list)

    def parse(self, name):
        tokens = self.tokenizer.tokenize(name)
        tag_tokens = self.tagger.tag(tokens)
        terminals = ''
        for ts in tag_tokens:
            terminals += ts[1] + " -> " + "'" + ts[0] + "'" + "\n    "
        grammar_rules = self.grammar_head + terminals
        grammar = nltk.parse_cfg(grammar_rules)
        parser = nltk.ChartParser(grammar)
        return parser.nbest_parse(tokens)
