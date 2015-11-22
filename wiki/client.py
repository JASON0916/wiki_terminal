#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.style import Style
from pygments.token import Token
from wiki_lexer import WikiLexer
from pygments.styles.default import DefaultStyle
from functions import QueryManager

wiki_completer = WordCompleter([
                            'summary',
                            'search',
                            'random',
                            'geosearch',
                            'quit',
                            'help'
                            ], meta_dict={
                                'summary': 'used to get summary of a word',
                                'search': 'used to search for a certain word.',
                                'random': 'used to have a title even show \
                                        its summary randomly.',
                                'geosearch': 'used to find out what happend\
                                        at a certain location or in the\
                                        range of radius.'
                                }, ignore_case=True)


class DocumentStyle(Style):
        styles = {
                Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
                Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
                Token.Menu.Completions.ProgressButton: 'bg:#003333',
                Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
                }
        styles.update(DefaultStyle.styles)


def main():
    history = InMemoryHistory()
    manager = QueryManager()
    while True:
        try:
            input = prompt('>>> ', lexer=WikiLexer, completer=wiki_completer,
                     style=DocumentStyle, history=history,
                     display_completions_in_columns=True)

            if not input or input.lower() == 'quit':
                print 'See you.'
                break
            else:
                func, args = input.split()[0], input.split()[1:]
            try:
                getattr(manager, func)(args)
            except AttributeError as error:
                print 'No function: %s' %func

        except KeyboardInterrupt as stop:
            print 'See you.'
            break



if __name__ == '__main__':
    main()
