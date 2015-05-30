# coding:utf-8
__author__ = 'cm'
from optparse import OptionParser
from wiki_functions import *


def main():
    usage = colored("%prog [options] arg", 'green', attrs=['bold', 'underline'])
    parser = OptionParser(usage, add_help_option=True)

    # '\n' seems to be useless, which needs to be fixed.
    parser.add_option("-s", "--summary", action="callback", callback=wiki_summary,
                      help="wiki the summary for the word.\n"
                           "Usage: wiki -s(--summary) query.\n"
                           "query: the issue you wiki for")

    parser.add_option("-S", "--search", action="callback", callback=wiki_search,
                      help="Do a Wikipedia search for query. "
                           "Usage: wiki -S(--search) query num(default=10) suggestion(default=false)\n"
                            "query: the issue you search for\n"
                            "num: the maxmimum number of results returned, numbers only")

    parser.add_option("-r", "--random", action="callback", callback=wiki_random,
                      help="Get a list of random Wikipedia article titles.\n"
                            "Usage: wiki -r(--random) s/summary(if you want to get the summary about it)")

    parser.add_option("-g", "--geosearch", action="callback", callback=wiki_geosearch,
                      help="Do a wikipedia geo search for latitude and longitude using.\n"
                            "Usage: wiki -g(--geosearch) latitude longitude (radius)"
                            "latitude & longitude: location of the article.\n"
                            "radius: Search radius in meters. The value must be between 10 and 10000")

    (options, args) = parser.parse_args()
    parser.disable_interspersed_args()

if __name__ == '__main__':
    main()