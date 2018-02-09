#!/usr/bin/env python3

"""
This script will print information from DVD IFO files.  All information about the IFO file format
is from http://dvd.sourceforge.net/dvdinfo/ifo.html.
"""

import sys
from argparse import ArgumentParser

verbose = False


class VtsIfoFile:

    def __init__(self, data):
        assert type(data) is bytes
        if not data[0:11] == b'DVDVIDEO-VTS': raise Exception('Invalid file identifier')

        subpictureCnt = int.from_bytes(data[254:255], byteorder='big')
        print('Number of subpicture streams : {0}'.format(subpictureCount))





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

    with open(inputFile, 'rb') as f:
        print('Reading file {0}'.format(inputFile))
        data = f.read()
        info = VtsIfoFile(data)




if __name__ == '__main__':
    main()
