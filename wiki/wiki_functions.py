# coding:utf-8
__author__ = 'cm'
from termcolor import colored, cprint
from wikipedia import summary, DisambiguationError, \
    search, random, geosearch, WikipediaException


# three formal parameter not used but added for the sake of optparse
def wiki_summary(option, opt_str, value, parser):
    """
    used to get summary of a word, raise errors when the word meets more than one wikipage
    :param option:
    :param opt_str:
    :param value:
    :param parser:
    :return:
    """
    text = ''
    length = len(parser.rargs)
    if length == 0:
        parser.error(colored("option -s needs at least one argument!", "red", attrs=["bold"]))
    else:
        print '\n'+"=="*15+"result"+"=="*15+'\n'
        try:
            text = summary(parser.rargs)

        except DisambiguationError as error:
            # the search term may refers to mutiple choices
            errors = [error.encode("utf-8") for error in error.options]
            message = "\"{0}\" may refer to: \n{1}".format(error.title, '\n'.join(errors))
            parser.error(colored(message, "red", attrs=["bold"]))

        # there is always a "None" at last, can't solve that problem.
        print w_print(text, "white", parser.rargs, "green")
        print '\n'+"=="*16+"end"+"=="*16+'\n'


def wiki_search(option, opt_str, value, parser):
    """
    used to search for a certain word.
    :param option:
    :param opt_str:
    :param value:
    :param parser:
    :return:
    """
    res = []
    key_words = []
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
        res = search(parser.rargs[0: length-1], results=num)
        key_words = parser.rargs[0: length-1]
    else:
        res = search(parser.rargs[0])
        key_words = parser.rargs[0]

    print '\n'+"=="*15+"results"+"=="*15+'\n'
    w_print(res, "white", key_words, "green")
    print '\n'+"=="*16+"end"+"=="*16+'\n'


def wiki_random(option, opt_str, value, parser):
    """
    used to have a title even show its summary randomly.
    :param option:
    :param opt_str:
    :param value:
    :param parser:
    :return:
    """
    length = len(parser.rargs)
    if length > 1:
        parser.error(colored("option -r has more than one argument!", "red", attrs=["bold"]))
    elif length == 1 and (parser.rargs[0] == "s" or parser.rargs[0] == 'summary'):
        title = random().encode("utf-8")
        cprint(title, 'blue', attrs=['bold', 'dark'])
        print '\n'+"=="*15+"result"+"=="*15+'\n'
        try:
            text = summary(title)
            w_print(text, "white", title.split(), "green")
        except DisambiguationError as error:
            parser.error(u"\"{0}\" may refer to: \n{1}".format(error.title, '\n'.join(error.options)))
        print '\n'+"=="*16+"end"+"=="*16+'\n'
    else:
        title = random().encode("utf-8")
        try:
            cprint(title, 'blue', attrs=['bold', 'dark'])
        except UnicodeEncodeError:
            parser.error(colored("Unicode encode failed!", "red", attrs=["bold"]))


def wiki_geosearch(option, opt_str, value, parser):
    """
    used to find out what happend at a certain location or in the range of radius
    :param option:
    :param opt_str:
    :param value:
    :param parser:
    :return:
    """
    length = len(parser.rargs)
    global geosearch_res
    [latitude, longtitude, radius] = [0]*3

    if length < 2:
        parser.error(colored("option -g needs at least 2 arguments!", "red", attrs=["bold"]))
    elif length > 3:
        parser.error(colored("option -g can't handle more than 3 arguments!", "red", attrs=["bold"]))
    elif length == 2:
        [latitude, longtitude] = parser.rargs[:]
    else:
        [latitude, longtitude, radius] = parser.rargs[:]

    try:
        geosearch_res = geosearch(latitude, longtitude, radius=radius)
    except WikipediaException:
        parser.error(colored("An unknown error occured: 'Invalid coordinate provided'. Please report it on GitHub!",
                             "red", attrs=["bold"]))
    print '\n'+"=="*15+"result"+"=="*15+'\n'
    for res in geosearch_res:
        cprint(res+'\n', "green")
    print '\n'+"=="*16+"end"+"=="*16+'\n'


def w_print(words, words_color, key_word=[],  key_word_color='green'):
    """
    used to proceed the text received and then print it.
    :param words:
    :param words_color:
    :param key_word:
    :param key_word_color:
    :return:
    """
    if key_word is not []:
        key_word = [str(key_words).lower() for key_words in key_word]
        for ch in words.encode("utf-8").split():
            for times, key_words in enumerate(key_word):
                # i claim the times to prevent print common words for more than one time
                if ch.lower().startswith(key_words) or ch.lower().endswith(key_words):
                    print colored(ch, key_word_color, attrs=['bold', 'underline']),
                    break
                if times == len(key_word) - 1:
                    print colored(ch, words_color),
            if ch.endswith('.'):
                print '\n'
    else:
        for ch in [words.encode("utf-8")]:
            if ch == '.':
                print "\n"
            else:
                print colored(ch, words_color),
