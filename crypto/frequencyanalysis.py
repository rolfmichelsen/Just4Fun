#! /usr/bin/env python3
#
# See https://github.com/rolfmichelsen/Just4Fun for latest
# version, licensing terms and more.
#
# © Rolf Michelsen, 2018.  All rights reserved.

"""
Frequency analysis of input text.
"""

import sys
from argparse import ArgumentParser

verbose = False


def analyseFrequencies(text, order=1):
    """
    Return a frequency analysis of the input text.
    """
    if order < 1: raise(Exception)
    frequency = {}
    textlen = len(text)
    if textlen < order: return frequency
    ngram = text[0:order-1]
    pos = order - 1
    while pos < textlen:
        ngram = (ngram + text[pos])[-order:]
        pos = pos + 1
        if ngram in frequency:
            frequency[ngram] = frequency[ngram] + 1
        else:
            frequency[ngram] = 1
    return frequency


def getText(inputfile):
    """
    Read all data from a named file, or from standard input if inputfile is None.  Return
    the read data.
    """
    text = None
    if inputfile:
        if verbose: print("Reading text from file {}".format(inputfile), file=sys.stderr)
        with open(inputfile, 'rt') as f:
            text = f.read()
    else:
        if verbose: print("Reading text from standard input", file=sys.stderr)
        text = sys.stdin.read()
    return text


def normalizeTextCase(text):
    """
    Normalize the text casing.
    """
    return text.lower()


def normalizeTextWhitespace(text):
    result = ""
    for ch in text:
        if ch.isspace(): ch = " "
        result = result + ch
    return result


def getArguments():
    """
    Get command line arguments.
    """

    description = "Output frequency analysis of input text."
    epilog = None
    argParser = ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars="@")
    argParser.add_argument("inputfile", action="store", nargs="?", help="name of file containing text to analyse")
    argParser.add_argument("--ngram", action = "store", help = "analyze ngrams of given size")
    argParser.add_argument("--nocase", action = "store_true", help = "ignore casing in input text")
    argParser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="verbose output")
    return argParser.parse_args()


def printReport(freq):
    for ngram in freq.keys():
        print("{0} : {1}".format(ngram, freq[ngram]))


def main():
    global verbose
    args = getArguments()
    verbose = args.verbose
    ngram = int(args.ngram) if args.ngram else 1

    text = getText(args.inputfile)
    if args.nocase: text = normalizeTextCase(text)
    text = normalizeTextWhitespace(text)
    freq = analyseFrequencies(text, order=ngram)
    printReport(freq)





if __name__ == '__main__':
    main()

