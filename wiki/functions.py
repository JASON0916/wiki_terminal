#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wikipedia
from termcolor import colored, cprint


class BaseManager(object):
    """BaseManager of the QueryManager, mainly to make a singleton."""
    _state = {}

    def __new__(cls, *args, **kwargs):
        ob = super(BaseManager, cls).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls._state
        return ob


class QueryManager(BaseManager):
    """Manager to manage the query send by the terminal."""

    __all__ = ['search', 'summary', 'geosearch', 'random', 'help']

    @staticmethod
    def w_print(words, words_color, key_word=[],  key_word_color='green'):
        """used to proceed the query result and print it in format."""
        if key_word is not []:
            key_word = [str(key_words).lower() for key_words in key_word]
            # for summary
            if type(words) is unicode:
                words = words.encode("utf-8").split()
            # for searchh
            elif type(words) is list:
                words = [word+'\n' for word in words]
            for ch in words:
                for times, key_words in enumerate(key_word):
                    # i claim the times to prevent print common words for
                    # more than one time
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

    def summary(self, args):
        """::summary::
        used to get summary of a word, raise errors when the word meets
        more than one wikipage
        example:
        summary apple """
        text = ''
        if not args:
            raise AssertionError(colored("function summary needs at\
                    least one argument!", "red", attrs=["bold"]))
        else:
            try:
                text = wikipedia.summary(args)
            except wikipedia.DisambiguationError as error:
                # the search term may refers to mutiple choices
                errors = [option.encode("utf-8") for option in error.options]
                message = "\"{0}\" may refer to: \n{1}"\
                        .format(error.title, '\n'.join(errors))
                raise AssertionError(colored(message, "red", attrs=["bold"]))

            if not text:
                message = 'Not found!!!'
                raise AssertionError(colored(message, "red", attrs=["bold"]))
            print self.w_print(text, "white", args, "green")

    def search(self, args):
        """::search::
        used to search for a certain word.
        example:
        1. search wikipedia -> return words refer to 'wikipedia'
        2. search wiki pedia -> return words refer to 'wiki' & 'pedia'
        3. search wiki pedia 10 -> return 10 of the results refer to 'wiki'
                & 'pedia' """
        res, key_words = [], []
        num = 0
        if len(args) < 1:
            raise AssertionError(colored("function search needs at least one argument!",
                    "red", attrs=["bold"]))
            # there may be more than 2 arguments, for example: search wiki pedia 10
        elif len(args) >= 2:
            try:
                num = int(args[-1])
            except ValueError:
                raise AssertionError("num should be a decimal number")
                res = wikipedia.search(args[0: len(args) - 1], results=num)
                key_words = args[0: len(args) - 1]
        else:
            res = wikipedia.search(args[0])
        key_words = args[0]
        self.w_print(res, "white", key_words, "green")

    def random(self, args):
        """::random::
        used to have a title even show its summary randomly.
        example:
        1. random s(or summary) -> get summary of a random keyword
        2. random -> get a random keyword"""
        if len(args) > 1:
            raise AssertionError(colored("function random has more than one argument!",
                    "red", attrs=["bold"]))
        elif len(args) == 1 and (args[0] == "s" or args[0] == 'summary'):
            title = wikipedia.random().encode("utf-8")
            cprint(title, 'blue', attrs=['bold', 'dark'])
            try:
                self.summary(title)
            except wikipedia.DisambiguationError as error:
                error(u"\"{0}\" may refer to: \n{1}".format(error.title,\
                        '\n'.join(error.options)))
        else:
            title = wikipedia.random().encode("utf-8")
            try:
                cprint(title, 'blue', attrs=['bold', 'dark'])
            except UnicodeEncodeError:
                error(colored("Unicode encode failed!", "red", attrs=["bold"]))

    def geosearch(self, args):
        """::geosearch::
        used to find out what happend at a certain location or
        in the range of radius.
        examole:
        1. geosearch 180 27 -> return event take place at 180' 27'
        2. geosearch 180 27 100 -> return event take place in 100 meters range from
                point 180' 27'"""
        global geosearch_res
        [latitude, longtitude, radius] = [0] * 3

        if len(args) < 2 or len(args) > 3:
            raise AssertionError(colored("function geosearch handle 2 or 3 arguments!",\
                    "red", attrs=["bold"]))
        elif len(args) == 2:
            [latitude, longtitude] = args[:]
        elif len(args) == 3:
            [latitude, longtitude, radius] = args[:]

        try:
            geosearch_res = wikipedia.geosearch(latitude, longtitude, radius=radius)
        except wikipedia.WikipediaException:
            raise AssertionError(colored("An unknown error occured: 'Invalid coordinate\
                    provided'. Please report it on GitHub!", "red", attrs=["bold"]))

        for res in geosearch_res:
            cprint(res + '\n', "green")

    def help(self, args):
        """::help::
        instruction of wiki_terminal
        example:
        1. help function -> how to use function
        2. help -> all the instruction desplayed"""
        if len(args) == 0:
            for func in self.__all__:
                print getattr(self, func).__doc__
        else:
            for func in args:
                print getattr(self, func).__doc__
