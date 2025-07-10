"""Utils module for parsing teh command line"""
#
# Imports
#

from argparse import ArgumentParser

#
# Methods
#


def setup_parser() -> ArgumentParser:

    parser: ArgumentParser = ArgumentParser(description="(Naive-)Pattern matcher over a text file.")

    parser.add_argument("-f", "--file", help="Input text file in UTF-8 encoding.", default="divina_commedia.txt")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Ignore case when matching patterns.")
    parser.add_argument("patterns", nargs="+", help="Pattern(s) to search for in the file.")
    return parser
