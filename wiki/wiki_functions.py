# coding:utf-8
__author__ = 'cm'
from termcolor import colored, cprint
from wikipedia import summary, DisambiguationError, \
    search, random, geosearch, WikipediaException


# decorators
def print_start_end(func):
    def temp(*args, **kwargs):
        temp_name = func.__name__
        print '\n'+"=="*15+temp_name+"=="*15+'\n'
        ret = func(*args, **kwargs)
        print '\n'+"=="*16+"end"+"=="*16+'\n'
        return ret
    return temp


# three formal parameter not used but added for the sake of optparse
@print_start_end
def wiki_summary(option, opt_str, value, parser):
    """
    used to get summary of a word, raise errors when the word meets more than one wikipage
    """
    text = ''
    length = len(parser.rargs)
    if length == 0:
        parser.error(colored("option -s needs at least one argument!", "red", attrs=["bold"]))
    else:
        try:
            text = summary(parser.rargs)

        except DisambiguationError as error:
            # the search term may refers to mutiple choices
            errors = [error.encode("utf-8") for error in error.options]
            message = "\"{0}\" may refer to: \n{1}".format(error.title, '\n'.join(errors))
            parser.error(colored(message, "red", attrs=["bold"]))
            exit(1)

        # there is always a "None" at last, can't solve that problem.
        print w_print(text, "white", parser.rargs, "green")
        with open('history.txt', 'a') as history_file:
            history_file.writelines(parser.rargs[0]+'\n')


@print_start_end
def wiki_search(option, opt_str, value, parser):
    """
    used to search for a certain word.
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
            exit(1)
        res = search(parser.rargs[0: length-1], results=num)
        key_words = parser.rargs[0: length-1]
    else:
        res = search(parser.rargs[0])
        key_words = parser.rargs[0]

    w_print(res, "white", key_words, "green")
    with open('history.txt', 'a') as history_file:
        history_file.writelines(parser.rargs[0]+'\n')


@print_start_end
def wiki_random(option, opt_str, value, parser):
    """
    used to have a title even show its summary randomly.
    """
    length = len(parser.rargs)
    if length > 1:
        parser.error(colored("option -r has more than one argument!", "red", attrs=["bold"]))
    elif length == 1 and (parser.rargs[0] == "s" or parser.rargs[0] == 'summary'):
        title = random().encode("utf-8")
        cprint(title, 'blue', attrs=['bold', 'dark'])
        try:
            text = summary(title)
            w_print(text, "white", title.split(), "green")
        except DisambiguationError as error:
            parser.error(u"\"{0}\" may refer to: \n{1}".format(error.title, '\n'.join(error.options)))
            exit(1)
    else:
        title = random().encode("utf-8")
        try:
            cprint(title, 'blue', attrs=['bold', 'dark'])
        except UnicodeEncodeError:
            parser.error(colored("Unicode encode failed!", "red", attrs=["bold"]))
            exit(1)


@print_start_end
def wiki_geosearch(option, opt_str, value, parser):
    """
    used to find out what happend at a certain location or in the range of radius
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
        exit(1)
    for res in geosearch_res:
        cprint(res+'\n', "green")


@print_start_end
def wiki_history(option, opt_str, value, parser):
    """
    used to show history and query the word in it again.
    """
    length = len(parser.rargs)
    if length > 1:
        parser.error(colored("option -h can't handle more than 1 arguments!", "red", attrs=["bold"]))
    elif length == 0:
        with open('history.txt', 'r+') as history_file:
            for nums, lines in enumerate(history_file):
                print nums+1, lines
    else:
        number = int(parser.rargs[0])
        with open('history.txt', 'r+') as history_file:
            lines = history_file.readlines()
            if len(lines) < number:
                parser.error(colored("number too big!!!", "red", attrs=["bold"]))
            try:
                text = summary(lines[number-1])
                w_print(text, "white", lines[number-1], "green")
            except DisambiguationError as error:
                # the search term may refers to mutiple choices
                errors = [error.encode("utf-8") for error in error.options]
                message = "\"{0}\" may refer to: \n{1}".format(error.title, '\n'.join(errors))
                parser.error(colored(message, "red", attrs=["bold"]))
                exit(1)
            # there is always a "None" at last, can't solve that problem.


def wiki_clear_history(option, opt_str, value, parser):
    """
    clear the history log
    """
    import os
    os.remove('history.txt')
    new_his = open('history.txt', 'w')
    new_his.close()


def w_print(words, words_color, key_word=[],  key_word_color='green'):
    """
    used to proceed the text received and then print it.
    """
    if key_word is not []:
        key_word = [str(key_words).lower() for key_words in key_word]
        if type(words) is unicode:
            # prepared for wiki_summary
            words = words.encode("utf-8").split()
        elif type(words) is list:
            # prepared for wiki_search
            words = [word+'\n' for word in words]
        for ch in words:
            for times, key_words in enumerate(key_word):
                # i claim the times to prevent print common words for more than one time
                if key_words in ch.lower():
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