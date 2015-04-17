# coding:utf-8
__author__ = 'cm'
import wikipedia
import re
from termcolor import colored, cprint


def wiki_summary(option, opt_str, value, parser):
    if len(parser.rargs) == 0:
        parser.error("option -s requires an argument.")
    else:
        print '\n'+"=="*15+"result"+"=="*15+'\n'
        try:
            text = wikipedia.summary(parser.rargs)
            text = re.sub('\.', '\n\n', text)
            print text
            print '\n'+"=="*15+"end"+"=="*15+'\n'
        except wikipedia.DisambiguationError as error:
            # the search term may refers to mutiple choices
            parser.error(u"\"{0}\" may refer to: \n{1}".format(error.title, '\n'.join(error.options)))


def wiki_search(option, opt_str, value, parser):
    res = []
    if len(parser.rargs) > 2 or len(parser.rargs) < 1:
        parser.error("option -S has more than two arguments!")
    elif len(parser.rargs) == 2:
        try:
            num = int(parser.rargs[1])+1
            res = wikipedia.search(parser.rargs[0], results=num)
        except ValueError:
            parser.error("num should be a decimal number")
    else:
        res = wikipedia.search(parser.rargs[0])
    print '\n'+"=="*15+"results"+"=="*15+'\n'
    for x in res:
        try:
            print x.encode() + '\n'
        except UnicodeEncodeError:
            pass


def wiki_random(option, opt_str, value, parser):
    length = len(parser.rargs)
    global title
    if length > 1:
        parser.error("option -r has more than one argument!")
    elif length == 1:
        if parser.rargs[0] == "s" or parser.rargs[0] == 'summary':
            title = wikipedia.random()
            cprint(title, 'blue', attrs=['bold', 'dark'])
        print '\n'+"=="*15+"result"+"=="*15+'\n'
        try:
            text = wikipedia.summary(title)
            text = re.sub(title, colored(title, 'green', attrs=['bold', 'underline']), text)
            text = re.sub('\.', '\n\n', text)
            print text
        except wikipedia.DisambiguationError as error:
            parser.error(u"\"{0}\" may refer to: \n{1}".format(error.title, '\n'.join(error.options)))
        print '\n'+"=="*15+"end"+"=="*15+'\n'
    else:
        title = wikipedia.random().encode()
        try:
            cprint(title, 'blue', attrs=['bold', 'dark'])
        except UnicodeEncodeError:
            pass