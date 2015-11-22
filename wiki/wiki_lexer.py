#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygments.lexer import RegexLexer, words
from pygments.token import *

class WikiLexer(RegexLexer):
    """
    Lexer for Structured Function Language.
    """
    name = 'wiki'
    tokens = {
            'root': [
                (r'\s+', Text),
                (r'/\*', Comment.Multiline),
                (words((
                    'SUMMARY', 'SEARCH', 'RANDOM',
                    'GEOSEARCH', 'QUIT', 'HELP',
                    'summary', 'search', 'random',
                    'geosearch', 'quit', 'help'),
                    suffix=r'\b'), Keyword)
                ]}
