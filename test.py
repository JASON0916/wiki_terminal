#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.lexers import SqlLexer
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle

sql_completer = WordCompleter(['create', 'select', 'insert', 'drop',
                                   'delete', 'from', 'where', 'table'], ignore_case=True)

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

    while True:
        text = prompt('> ', lexer=SqlLexer, completer=sql_completer,
                style=DocumentStyle, history=history)
        print('You entered:', text)
        print('GoodBye!')

if __name__ == '__main__':
    main()
