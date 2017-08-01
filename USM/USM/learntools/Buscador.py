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
#       https://github.com/nltk/nltk/wiki/Porting-your-code-to-NLTK-3.0
__author__="Jorge García Flores"
__date__ ="$03-abr-2011 10:05:30$"


import nltk, logging, re, time
import freeling, tempfile


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
        #grammar = nltk.parse_cfg(grammar_rules)    --Deprecated
        grammar = nltk.CFG.fromstring(grammar_rules)
        parser = nltk.ChartParser(grammar)
        #return parser.nbest_parse(tokens)          --Deprecated
        return parser.parse(tokens)


class FilterStatus:
    def __init__(self):
        self.nominal = False
        self.semantic = 0.000
        self.biographic = False
        self.vinculo_encontrado = False


class Filtro:
    def __init__(self, lista):
        self.snippets = lista
        self.seleccion = set([])

    def nominal(self, nombre):
        self._filtro_nominal = FiltroNominal(nombre)

        for s in self.snippets:
            if self._filtro_nominal.filtra(s.string):
                s.filter_status.nominal = True
        return self.snippets

    def tematico(self, tema):
        self._filtro_semantico = FiltroSemantico(tema)
        for s in self.snippets:
            # self._filtro_semantico.filtra regresa un float
            s.filter_status.semantic = self._filtro_semantico.filtra(s.string)
        return self.snippets

    def biografico(self):
        return self.snippets

    def selecciona(self):

        for s in self.snippets:
            if s.filter_status.nominal is True and s.filter_status.semantic > 0.0:
                logging.debug('main::valid nominal and semantic snippets:' + s.string)
                logging.debug('main::semantic score=' + str(s.filter_status.semantic))
                self.seleccion.add(s)
        for s in self.snippets:
            if s.filter_status.nominal is True:
                logging.debug('main::valid nominal snippets:' + s.string)
        for s in self.snippets:
            if s.filter_status.semantic > 0:
                logging.debug('main::valid semantic snippets:' + s.string)
        return self.seleccion


class FiltroSemantico:
    def __init__(self, tema):
        self._tema = tema

    def filtra(self, snippet_str):
        # Better for security delete = False
        # self._tmp_file = tempfile.NamedTemporaryFile(delete=False)
        tmp_file = tempfile.NamedTemporaryFile()
        snippet_str = self._limpia_esa(snippet_str)
        # para el CGI esto no jala
        command = UNO_ROOT + '/scripts/calculate_esa.sh "' + self._tema + '" "' + \
                  snippet_str + '" > ' + tmp_file.name + " 2>&1"
        # from a CGI we need to run calculate_esa from cgi-bin, and maybe the whole jar
        # command = 'calculate_esa.sh "' + self._tema + '" "' + \
        #                         snippet_str + '" > ' + tmp_file.name + " 2>&1"
        logging.debug('FiltroSemantico::semantic relatedness command:' + command)
        os.system(command)
        logging.info('CALCULATING SEMANTIC RELATEDNESS OF ' + self._tema + ' AGAINST:' + snippet_str)
        for line in tmp_file:
            logging.debug('FiltroSemantico::reading line ' + line)
            if re.search('ESA Similarity:', line):
                score_re = re.search('[01][,\.][0-9]+', line)
                if score_re:
                    score_str = score_re.group(0)
                    score_str = score_str.replace(',', '.')
                    logging.info('FiltroSemantico::semantic relatedness=' + score_str)
                    score = float(score_str)
                    tmp_file.close()
                    return score
        tmp_file.close()
        return 0.0

    # Función aberrante que baja a minúsculas y quita todos los signos de puntuación
    # para que research_esa lo pueda evaluar
    def _limpia_esa(self, esa_str):
        res_str = esa_str.lower()
        res_str = re.subn('[,\.:;]', ' ', res_str)[0]
        res_str = res_str.replace('"', '')
        return res_str


# ESTA CLASE REPRODUCE LAS FUNCIONES DE nominal_coref.py
class FiltroNominal:
    def __init__(self, name):
        nombre = self._separa_iniciales(name)
        nombre = nombre.title()
        logging.debug('Starting FiltroNominal class for ' + nombre)
        self._name_parser = NameParser()
        self._trees = self._name_parser.parse(nombre)
        self._regex_list = self._name_variations(nombre, self._trees)
        self._limpieza = Limpieza()

    def _name_variations(self, name, trees):
        variations = []
        for tree in trees:
            if len(tree) < 2:
                return variations

            name_text = name.strip()
            nombre = tree[0]
            apellido = tree[1]
            # literal nombre, literal apellido
            s = self._literal(nombre)
            l = self._literal(apellido)
            # variations.append(name_text)
            variations = self._add_variation(s, l, variations, 'LnLa')
            # literal apellido, literal nombre
            variations = self._add_variation(l, s, variations, 'LaLn', ',? +')
            # literal sin inicial
            s = self._sin_inicial(nombre)
            l = self._sin_inicial(apellido)
            variations = self._add_variation(s, l, variations, 'SInSIa')
            # EXPANDE(nombre) PRINT(apellido)
            s = self._expande(nombre)
            l = self._literal(apellido)
            variations = self._add_variation(s, l, variations, 'EnLa')
            variations = self._add_variation(l, s, variations, 'LaEn', ',? +')
            # CONTR(nombre) PRINT(apellido)
            s = self._contrae(nombre)
            variations = self._add_variation(s, l, variations, 'CnLa')
            variations = self._add_variation(l, s, variations, 'LaCn', ',? +')
            # PRINT(nombre) CONTRAE(apellido)
            # logging.debug('****ANTES DE >>>> CaLn, len(nombre)=' +str(len(nombre))+ ', len(apellido)=' +str(len(apellido)))
            l = self._literal(nombre)
            s = self._contrae(apellido)
            variations = self._add_variation(l, s, variations, 'LnCa')
            variations = self._add_variation(s, l, variations, 'CaLn', ',? +')
            # PRINT(nombre) EXPANDE(apellido)
            s = self._expande(apellido)
            variations = self._add_variation(l, s, variations, 'LnEa')
            variations = self._add_variation(s, l, variations, 'EaLn', ',? +')
            # CONTR(nombre) CONTRAE(apellido)
            # logging.debug('antes de CnCa, len(nombre)=' +str(len(nombre))+ ', len(apellido)=' +str(len(apellido)))
            l = self._contrae(nombre)
            s = self._contrae(apellido)
            variations = self._add_variation(l, s, variations, 'CnCa')
            variations = self._add_variation(s, l, variations, 'CaCn', ',? +')
            # EXP(nombre) EXPANDE(apellido) 8
            l = self._expande(nombre)
            s = self._expande(apellido)
            variations = self._add_variation(l, s, variations, 'EnEa')
            variations = self._add_variation(s, l, variations, 'EaEn', ',? +')
            # EXP(nombre) CONTRAE(apellido) 9

            l = self._expande(nombre)
            s = self._contrae(apellido)
            variations = self._add_variation(l, s, variations, 'EnCa')
            variations = self._add_variation(s, l, variations, 'CaEn', ',? +')
            # CONTR(nombre) EXP(apellido) 10
            l = self._contrae(nombre)
            s = self._expande(apellido)
            variations = self._add_variation(l, s, variations, 'CnEa')
            variations = self._add_variation(s, l, variations, 'EaCn', ',? +')
            if len(nombre) >= 1 and len(apellido) >= 1:
                # PRINT(nombre) [inicial] #PRINT(apellido) 11
                # logging.debug('antes de LnILa, len(nombre)=' +str(len(nombre))+ ', len(apellido)=' +str(len(apellido)))
                l = self._literal(nombre)
                s = self._literal(apellido)
                variations = self._add_variation(l, s, variations, 'LnILa', ' [A-Z][\.]? ')
                # PRINT(nombre) [nombre/apodo] #PRINT(apellido) 12
                # logging.debug('antes de LnXLa, len(nombre)=' +str(len(nombre))+ ', len(apellido)=' +str(len(apellido)))
                l = self._literal(nombre)
                s = self._literal(apellido)
                variations = self._add_variation(l, s, variations, 'LnXLa', ',?[- ]+[A-Z][a-z]+ ')
                variations = self._add_variation(s, l, variations, 'LaXLn', ',?[- ]+[A-Z][a-z]+ ')

            # PRIMER(nombre) #PRIMER(apellido)
            l = self._literal(nombre[0])
            s = self._literal(apellido[0])
            variations = self._add_variation(l, s, variations, 'Ln0La0')

            logging.debug(
                '****ANTES DE >>>> Ln0Cn1La, Ln0Cn1La0Ca1 len(nombre)=' + str(len(nombre)) + ', len(apellido)=' + str(
                    len(apellido)))
            if len(nombre) > 1:
                if nombre[0].node != 'I':
                    # PRIMER(nombre) LITERAL(apellido):
                    l = self._literal(nombre[0])
                    s = self._literal(apellido)
                    variations = self._add_variation(l, s, variations, 'Ln0La')
                    if len(apellido) > 1:
                        # SEGUNDO(nombre) #PRIMER(apellido)
                        l = self._literal(nombre[1])
                        s = self._literal(apellido[0])
                        variations = self._add_variation(l, s, variations, 'Ln1La0')
                        # DOS APELLIDOS CON GUION
                        l = self._literal(apellido[0])
                        s = self._literal(apellido[1])
                        variations = self._add_variation(l, s, variations, 'La0-La1', '')
                if nombre[1].node != 'I':
                    # PRIMER(nombre) #CONTRAE(SEGUNDO(nombre)) #LITERAL(apellido)
                    l = self._literal(nombre[0])
                    m = self._contrae(nombre[1])
                    s = self._literal(apellido)
                    n = l + m
                    variations = self._add_variation(n, s, variations, 'Ln0Cn1La')
                    if len(apellido) > 1:
                        # PRIMER(nombre) #CONTRAE(SEGUNDO(nombre)) #PRIMER(apellido) #CONTRAE(2oapellido)
                        o = self._literal(apellido[0])
                        p = self._contrae(apellido[1])
                        q = o + ' ' + p
                        variations = self._add_variation(n, q, variations, 'Ln0Cn1La0Ca1')

        return variations

    def _add_variation(self, s, l, var_list, tipo='N/A', separador=' '):
        if s and l:
            variante = s.strip() + separador + l.strip()
            if variante.endswith('[ \-]+'):
                variante = variante.rstrip('[ \-]+')
            if variante.endswith('[ -]+'):
                variante = variante.rstrip('[ -]?')
            if variante not in var_list:
                var_list.append(variante)
                logging.debug('FiltroNominal::adding variation ' + variante + ' of type ' + tipo)
        return var_list

    def _expande(self, tree):
        if len(tree.pos()) > 1:
            name_buffer = ''
            for rama in tree:
                name_buffer += self._expande(rama) + ' '
            return name_buffer.strip()
        else:
            tuple = tree.pos()[0]
            if tuple[1] == 'I':
                expansion = re.sub(r'[\.\s]', '[a-z]+', tuple[0])
                return expansion
            else:
                return tuple[0]

    def _contrae(self, tree):
        # logging.debug( 'contrayendo::tree' +str(tree))
        # logging.debug( 'contrayendo::tree.node' +str(tree.node))
        if len(tree.pos()) > 1:
            name_buffer = ''
            for rama in tree:
                name_buffer += self._contrae(rama) + '[ -]?'
                # logging.debug ('contrayendo::name_buffer=' +name_buffer)
            return name_buffer.strip()
        else:
            contraccion = ''
            tuple = tree.pos()[0]
            # logging.debug( 'contrayendo::height' +str(tree.height()))
            # verificando si es un primer apellido incompresible
            if tree.node == 'AAA':
                return self._contrae_1er_apellido(tuple[0])
            elif type(tree[0]) == nltk.tree.Tree:
                if tree[0].node == 'AAA':
                    return self._contrae_1er_apellido(tuple[0])
            # logging.debug( 'contrayendo::tuple' +str(tuple))
            if tuple[1] == 'AA' and tuple[0][0].istitle():
                contraccion = tuple[0][0] + r'[\.]? '
            elif tuple[1] in ('AD', 'AG'):
                lista = tuple[0].split('[ \-]')
                for l in lista:
                    if l[0].istitle():
                        contraccion += l[0] + r'[\.]? '
                    else:
                        contraccion += l + ' '
            else:
                contraccion = tuple[0].strip()
                if contraccion.find('.') >= 0:
                    contraccion = contraccion.replace('.', '\.?')
                else:
                    contraccion += '\.?'
            return contraccion.strip()

    def _contrae_1er_apellido(self, apellido):
        if apellido.find('-'):
            apellidos = apellido.split('-')
            name_buffer = apellidos[0]
            for a in apellidos:
                if apellidos[0] != a:
                    if a[0].istitle():
                        name_buffer += ' ' + a[0] + '[\.]?'
            return name_buffer
        else:
            return apellido
        return apellido


        # Some of the functions in this module takes flags as optional parameters:
        #        I  IGNORECASE  Perform case-insensitive matching.
        # lista = tree.flatten()
        # resultado = ''
        # print tree
        # for l in lista:
        #     resultado += l + ' '
        # return resultado.strip()

    def _literal(self, tree):
        # logging.debug('literal.tree= '+str(tree))
        if len(tree.pos()) > 1:
            name_buffer = ''
            for rama in tree:
                name_buffer += self._literal(rama)
            return name_buffer
        else:
            tuple = tree.pos()[0]
            # logging.debug('literal.tuple= ' +str(tuple))
            if tree.node == 'AAA':
                return tuple[0] + '[ \-]+'
            if tuple[1] == 'I':
                # logging.debug ('entrando en if tuple[1]==I')
                ret_str = tuple[0].strip()
                if ret_str.find('.') >= 0:
                    ret_str = ret_str.replace('.', '\.?')
                    # logging.debug('after replace initial with \., ret_str=' +ret_str)
                else:
                    ret_str += '\.?'
                    # logging.debug('after replace initial without \., ret_str=' +ret_str)
                return ret_str + ' '
            else:
                return tuple[0] + ' '

    def _sin_inicial(self, tree):
        if len(tree.pos()) > 1:
            name_buffer = ''
            for rama in tree:
                name_buffer += self._sin_inicial(rama) + ' '
            return name_buffer.strip()
        else:
            tuple = tree.pos()[0]
            if tuple[1] != 'I' and tuple[0]:
                return tuple[0]
            else:
                return ''

    def _corta_nombres(self, tree):
        pass

    def filtra(self, snippet_str):
        for regex in self._regex_list:
            snippet_limpio = self._limpieza.limpia_reservados_xml(snippet_str)
            snippet_str_sin_acentos = self._limpieza.limpia_acentos(snippet_limpio)
            # error bug correction JGF: 23/01/12::
            regex = '[^A-Za-z]' + regex + '[^A-Za-z]'
            logging.debug(
                'Tree len(leaves)=' + str(len(self._trees[0].leaves())) + ' list::' + str(self._trees[0].leaves()))
            logging.debug(
                'FiltroNominal::processing name_variation: ' + regex + ' on snippet ' + snippet_str_sin_acentos)
            leaves_list = self._trees[0].leaves()
            if len(leaves_list) == 2:
                # special case for names with initial + lastname only (A Amaya)
                if len(leaves_list[0]) <= 2:
                    if re.search(regex, snippet_str_sin_acentos):
                        logging.debug('\t--->nominal correference found::' + regex)
                        return True
                elif re.search(regex, snippet_str_sin_acentos, flags=re.IGNORECASE):
                    logging.debug('\t--->nominal correference found::' + regex)
                    return True
            elif re.search(regex, snippet_str_sin_acentos, flags=re.IGNORECASE):
                logging.debug('\t--->nominal correference found::' + regex)
                return True

    def _separa_iniciales(self, nombre):
        exit_nombre = nombre
        if not exit_nombre.isupper():
            logging.debug('exit_nombre.isupper():')
            secuencia_inicial_r = re.match(u'^[A-Z]{2,}', exit_nombre)
            if secuencia_inicial_r:
                logging.debug('if secuencia_inicial_r:')
                secuencia_inicial = secuencia_inicial_r.group(0)
                exit_nombre = ''
                for c in secuencia_inicial:
                    exit_nombre = exit_nombre + ' ' + c
                exit_nombre += nombre.replace(secuencia_inicial, '')
        return exit_nombre


# PROBLEMS, function unicode
# class Limpieza:
#     def __init__(self):
#         # TODO: support propper UTF-8 with NLTK!!!
#
#         self._re_a = re.compile(u'[áâàä]')
#         self._re_e = re.compile(u'[éèêëě]')
#         self._re_i = re.compile(u'[íïîì]')
#         self._re_o = re.compile(u'[óòôöø]')
#         self._re_u = re.compile(u'[úùüû]')
#         self._re_n = re.compile(u'[ñ]')
#         self._re_c = re.compile(u'[ç]')
#         self._re_y = re.compile(u'[ỳýÿŷÿ]')
#         self._re_beta = re.compile(u'[ß]')
#         self._re_A = re.compile(u'[ÁÀÄÂÅ]')
#         self._re_E = re.compile(u'[ÉÈÊË]')
#         self._re_I = re.compile(u'[ÍÌÏÎ]')
#         self._re_O = re.compile(u'[ÓÒÔÖØ]')
#         self._re_U = re.compile(u'[ÚÙÛÜ]')
#         self._re_N = re.compile(u'[Ñ]')
#         self._re_C = re.compile(u'[Ç]')
#         self._re_S = re.compile(u'[Š]')
#
#     def limpia_acentos(self, linea):
#         linea_u = unicode(linea, 'utf-8')
#
#         linea_u = self._re_a.subn('a', linea_u)[0]
#         linea_u = self._re_e.subn('e', linea_u)[0]
#         linea_u = self._re_i.subn('i', linea_u)[0]
#         linea_u = self._re_o.subn('o', linea_u)[0]
#         linea_u = self._re_u.subn('u', linea_u)[0]
#         linea_u = self._re_n.subn('n', linea_u)[0]
#         linea_u = self._re_c.subn('c', linea_u)[0]
#         linea_u = self._re_y.subn('y', linea_u)[0]
#         linea_u = self._re_beta.subn('ss', linea_u)[0]
#         linea_u = self._re_A.subn('A', linea_u)[0]
#         linea_u = self._re_E.subn('E', linea_u)[0]
#         linea_u = self._re_I.subn('I', linea_u)[0]
#         linea_u = self._re_O.subn('O', linea_u)[0]
#         linea_u = self._re_U.subn('U', linea_u)[0]
#         linea_u = self._re_N.subn('N', linea_u)[0]
#         linea_u = self._re_C.subn('C', linea_u)[0]
#         linea_u = self._re_S.subn('S', linea_u)[0]
#
#         linea_a = linea_u.encode('ascii', 'ignore')
#         return linea_a
#
#     def limpia_reservados_xml(self, linea):
#         r = linea.replace('&apos;', "'")
#         r = r.replace('&lt;', "<")
#         r = r.replace('&gt;', ">")
#         r = r.replace('&quot;', '"')
#         r = r.replace('&amp;', "&")
#         return r
