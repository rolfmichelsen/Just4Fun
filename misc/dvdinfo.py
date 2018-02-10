#!/usr/bin/env python3

"""
This script will print information from DVD IFO files.  All information about the IFO file format
is from http://dvd.sourceforge.net/dvdinfo/ifo.html.
"""

import sys
from argparse import ArgumentParser

verbose = False


class Subpicture:

    extensionsDef = {
        0 : 'not specified',
        1 : 'normal',
        2 : 'large',
        3 : 'children',
        5 : 'normal captions',
        6 : 'large captions',
        7 : 'childrens captions',
        9 : 'forced',
        13 : 'director comments',
        14 : 'large director comments',
        15 : 'director comments for children'
    }

    def __init__(self, data):
        self.language = 'unknown'
        if data[0] & 0x03: self.language = str(data[2:4], encoding='ascii')
        self.extension = data[5]
        self.extensionText = self.extensionsDef.get(self.extension, 'unknown')


class VtsIfoFile:

    def __init__(self, data):
        assert type(data) is bytes
        if not data[0:12] == b'DVDVIDEO-VTS': raise Exception('Invalid file identifier')

        subpictureCnt = int.from_bytes(data[0x254:0x256], byteorder='big')
        self.subpicture = []
        for i in range(subpictureCnt):
            o = 0x256 + i*6
            self.subpicture.append(Subpicture(data[o:o+6]))


    def report(self):
        print('File type : VTS')

        if len(self.subpicture) > 0:
            print('Subpicture streams')
            for i in range(len(self.subpicture)):
                sp = self.subpicture[i]
                print('  Subpicture {0} : lang={1} ext={2} ({3})'.format(i, sp.language, sp.extensionText, sp.extension))





def IfoFactory(data):
    assert type(data) is bytes
    if data[0:12] == b'DVDVIDEO-VTS': return VtsIfoFile(data)

    print('ERROR: Unsupported file format with file id "{0}"'.format(data[0:12]), file=sys.stderr)




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
        info = IfoFactory(data)
        info.report()




if __name__ == '__main__':
    main()
