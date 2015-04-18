# coding:utf-8
__author__ = 'cm'
import wikipedia
import re
from termcolor import colored, cprint


# three formal parameter not used but added for the sake of optparse
def wiki_summary(option, opt_str, value, parser):
    length = len(parser.rargs)
    if length == 0:
        parser.error(colored("option -s needs at least one argument!", "red", attrs=["bold"]))
    else:
        print '\n'+"=="*15+"result"+"=="*15+'\n'
        try:
            text = wikipedia.summary(parser.rargs)
            text = re.sub('\.', '\n\n', text)
            print text
            print '\n'+"=="*16+"end"+"=="*16+'\n'
        except wikipedia.DisambiguationError as error:
            # the search term may refers to mutiple choices
            parser.error(u"\"{0}\" may refer to: \n{1}".format(error.title, '\n'.join(error.options)))


def wiki_search(option, opt_str, value, parser):
    res = []
    length = len(parser.rargs)
    if length < 1:
        parser.error(colored("option -S needs at least one argument!", "red", attrs=["bold"]))
    # there may be more than 2 arguments, for example: wiki -S wiki pedia 10
    elif length >= 2:
        try:
            global num
            num = int(parser.rargs[-1])
        except ValueError:
            parser.error("num should be a decimal number")
        res = wikipedia.search(parser.rargs[0: length-1], results=num)
    else:
        res = wikipedia.search(parser.rargs[0])
    print '\n'+"=="*15+"results"+"=="*15+'\n'
    for x in res:
        try:
            print x.encode() + '\n'
        except UnicodeEncodeError:
            pass
    print '\n'+"=="*16+"end"+"=="*16+'\n'


def wiki_random(option, opt_str, value, parser):
    length = len(parser.rargs)
    global title
    if length > 1:
        parser.error(colored("option -r has more than one argument!", "red", attrs=["bold"]))
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
        print '\n'+"=="*16+"end"+"=="*16+'\n'
    else:
        title = wikipedia.random().encode()
        try:
            cprint(title, 'blue', attrs=['bold', 'dark'])
        except UnicodeEncodeError:
            pass


def wiki_geosearch(option, opt_str, value, parser):
    length = len(parser.rargs)
    global geosearch_res
    if length < 2:
        parser.error(colored("option -g needs at least 2 arguments!", "red", attrs=["bold"]))
    elif length > 3:
        parser.error(colored("option -g can't handle more than 3 arguments!", "red", attrs=["bold"]))
    elif length == 2:
        [latitude, longtitude] = parser.rargs
        print '\n'+"=="*15+"result"+"=="*15+'\n'
        try:
            geosearch_res = wikipedia.geosearch(latitude, longtitude)
        except wikipedia.WikipediaException:
            parser.error(colored("An unknown error occured: 'Invalid coordinate provided'. Please report it on GitHub!",
                                 "red", attrs=["bold"]))
        for res in geosearch_res:
            cprint(res+'\n', "green")
        print '\n'+"=="*16+"end"+"=="*16+'\n'
    else:
        [latitude, longtitude, radius] = parser.rargs
        try:
            geosearch_res = wikipedia.geosearch(latitude, longtitude, radius=radius)
        except wikipedia.WikipediaException:
            parser.error(colored("An unknown error occured: 'Invalid coordinate provided'. Please report it on GitHub!",
                                 "red", attrs=["bold"]))
        print '\n'+"=="*15+"result"+"=="*15+'\n'
        for res in geosearch_res:
            cprint(res+'\n', "green")
        print '\n'+"=="*16+"end"+"=="*16+'\n'