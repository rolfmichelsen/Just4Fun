#!/usr/bin/env python3
#
# Program for solving the puzzle in GC48QDA: GC-nummer puzzle.
# The program reads a file containing GCodes and finds a
# combination of GCodes that satisfies the puzzle.
#
# Written by Rolf Michelsen, 2015

import re


# Name of file containing the list of GCodes to analyze
gcodefile = 'gcodes.txt'

# List of all gcodes that will be used to find a solution to the puzzle
# Each list element miust be of type Geocache.
gcodes = []

verbose = True


class Geocache:
    """
    Class encapsulating the information about a single geocache.
    """

    def __init__(self, name, characters):
        self.name = name
        self.characters = characters





def readGcodes(filename):
    """
    Read gcodes from the named file and store them in the gcodes list.
    Invalid gcodes will be skipped with an appropriate warning in verbose
    mode.
    """
    with open(filename, 'rt') as file:
        lineNumber = 1
        for line in file:
            parseGcode(line)
            lineNumber = lineNumber + 1


def parseGcode(line):
    """
    Parse a line from the gcodes file.  If it contains a valid gcode,
    create a corresponding Geocache object and store it in the gcodes
    list.
    """
    match = re.match('GC([ABCDEFGHJKMNPQRTVWXYZ0123456789]+)\s', line)
    if match:
        gcode = match.group(1)
        characters = set(gcode)
        if len(characters) == len(gcode):
            gcodes.append(Geocache(gcode, characters))


def solve(startIndex, partialResult, characters, level):
    """
    Solve the puzzle and return the set of geocaches constituting a
    possible solution.  The result is a list of Geocache objects.
    Return None if no solution was found.
    """

    if len(characters) == 31:
        return partialResult

    while startIndex < len(gcodes):
        if verbose and level < 3:
            print('{0:3} : {1} '.format(level, startIndex))

        if len(characters & gcodes[startIndex].characters) == 0:
            # go one level down and test the next candidate
            newPartialResult = partialResult[:]
            newPartialResult.append(gcodes[startIndex])
            result = solve(startIndex+1, newPartialResult, characters | gcodes[startIndex].characters, level+1)
            if result:
                return result
        startIndex = startIndex + 1;

    return None


def main():
    print('Reading geocaches from file "{0}".'.format(gcodefile))
    readGcodes(gcodefile)
    print('Got {0} geocaches for analysis.'.format(len(gcodes)))

    result = solve(0, [], set(), 0)
    if result:
        for gc in result:
            print(gc.name)
    else:
        print('No solution found')


main()
