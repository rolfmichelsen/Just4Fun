#!/usr/bin/env python3

"""
Performs simple frequency analysis of input text.
"""

import sys
from argparse import ArgumentParser



def frequencyAnalysis(text, alpha=False):
    """
    Return a frequency analysis of characters in the input text.  Returns a map where the key is the character
    and the value is the occurrence count in the text.
    """
    
    frequency = {}
    for ch in text:
        if alpha and not ch.isalpha(): continue
        if ch.isspace(): ch = ' '
        f = frequency.get(ch, 0)
        frequency[ch] = f + 1
    return frequency



def outputReport(frequency):
    """
    Output character frequency counts.  The input is a map with characters as keys and occurrence count as value.
    """

    charsTotal = sum(frequency.values())
    charMax = max(frequency.values())

    freq = sorted(zip(frequency.values(), frequency.keys()), reverse=True)
    for (count, character) in freq:
        print('{0:2} : {1:>3} {2:>8.2f}% {3}'.format(character, count, count*100.0/charsTotal, '*'*int(count*60/charMax)))



def getArguments():
    """
    Get command line arguments.
    """

    description = 'Output frequency analysis of input text.'
    epilog = '''
    Read a text from standard input and provide a report on the occurrence frequency of each character.
    All whitespace characters are normalized to a space before computing frequencies.
    Hint: Use @<filename> to read command line arguments from a file.
    '''
    argParser = ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars='@')
    argParser.add_argument('--alpha', dest='alpha', action='store_true', help='Only consider alphabetical characters')
    argParser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='more verbose output')
    return argParser.parse_args()




def main():
    args = getArguments()

    text = sys.stdin.read()
    frequency = frequencyAnalysis(text, alpha=args.alpha)
    outputReport(frequency)


if __name__ == '__main__':
    main()
