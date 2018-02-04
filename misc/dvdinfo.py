#!/usr/bin/env python3

import sys
from argparse import ArgumentParser

verbose = False


class VtsIfoFile:
    
    def __init__(self, data):
        






def getArguments():
    """
    Get command line arguments.
    """

    description = 'Print information from DVD IFO files'
    argParser = ArgumentParser(description=description, fromfile_prefix_chars='@')
    argParser.add_argument('file', help='DVD IFO file')
    argParser.add_argument('--verbose', dest='verbose', action='store_true', help='More verbose output')
    return argParser.parse_args()


def main():
    global verbose
    args = getArguments()
    verbose = args.verbose
    inputFile = args.file



if __name__ == '__main__':
    main()
