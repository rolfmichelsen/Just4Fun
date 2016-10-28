#!/usr/bin/env python3

"""
Patch a geocaching GPX file to modify the geocache location.
"""

import re
import sys
from argparse import ArgumentParser

verbose = False



def getArguments():
    """
    Get command line arguments.
    """

    description = 'Patch a geocaching GPX file to modify the geocache location.'
    epilog = '''
    The patch file must contain one line per cache to be patched.  Each line contains a GC-code followed by the
    new latitude and longitude for the cache, e.g. "GCABC12 N59 12.345 E10 12.345". Empty lines are ignored.
    '''
    argParser = ArgumentParser(description=description, fromfile_prefix_chars='@', epilog=epilog)
    argParser.add_argument('gpxfile', help='Geocaching GPX file')
    argParser.add_argument('patchfile', help='GPX patch file')
    argParser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='More verbose output')
    return argParser.parse_args()



def readGpxData(gpxfile):
    """
    Read geocaching GPX data from the named file and return it as an array where each element represent
    a line in the file.
    """

    if verbose:
        print('Reading geocaching GPX data from file {0}'.format(gpxfile), file=sys.stderr)

    gpxdata = []
    linenumber = 1
    try:
        with open(gpxfile, 'rt', encoding='utf-8') as file:
            for line in file:
                gpxdata.append(line)
                linenumber += 1
    except:
        print('Error while reading line {0}'.format(linenumber), file=sys.stderr)
        raise

    if verbose:
        print('Read {0} lines'.format(len(gpxdata)), file=sys.stderr)

    return gpxdata


def writeGpxData(gpxfile, gpxdata):
    """
    Write geocaching GPX data to the named file.
    """

    if verbose:
        print('Writing geocaching GPX data to file {0}'.format(gpxfile), file=sys.stderr)

    with open(gpxfile, 'wt', encoding='utf-8') as file:
        for line in gpxdata:
            print(line, file=file, end='')

    if verbose:
        print('Wrote {0} lines'.format(len(gpxdata)), file=sys.stderr)



def convertLatitude(lat):
    """
    Convers a latitude in the format N59 10.123 to decimal format.
    """

    latitudePattern = '([NS])(\d+)\s+(\d+\.\d+)'
    m = re.search(latitudePattern, lat)
    assert(m)

    deglat = float(m.group(2)) + float(m.group(3))/60
    if m.group(1) == 'S': deglat = -deglat
    return deglat



def convertLongitude(lon):
    """
    Convers a longitude in the format E010 10.123 to decimal format.
    """

    longitudePattern = '([EW])(\d+)\s+(\d+\.\d+)'
    m = re.search(longitudePattern, lon)
    assert(m)

    deglon = float(m.group(2)) + float(m.group(3))/60
    if m.group(1) == 'W': deglon = -deglon
    return deglon



def readPatchData(patchfile):
    """
    Read GPX patch data from the named file.  The returned patch set is a map with the geocache ID as key.
    The value is a map with the following keys:
        lat     Latitude
        lon     Longitude
    Empty lines or lines starting with a '#' characters are skipped.
    """

    if verbose:
        print('Reading GPX patch set from file {0}'.format(patchfile), file=sys.stderr)

    patch = {}
    lineno = 0

    # Match lines comprising entirely of whitespace, can be safely ignored.
    ignorePattern = re.compile('^\s*$')

    # Match a GC-code followed by coordinates, eg "GC01234 N59 22.333 E10 22.333".
    geoPattern = re.compile('^(GC[A-Z0-9]+)\s+([NS]\d+\s+\d+\.\d+)\s+([EW]\d+\s+\d+\.\d+)')

    with open(patchfile, 'rt') as file:
        for line in file:
            lineno += 1
            if ignorePattern.match(line): continue
            geo = geoPattern.match(line)
            if geo:
                gccode = geo.group(1)
                lat = convertLatitude(geo.group(2))
                lon = convertLongitude(geo.group(3))
                patch[gccode] = {'lat' : lat, 'lon' : lon}
            else:
                print('ERROR: Ignoring invalid line {0}'.format(lineno), file=sys.stderr)

    if verbose:
        print('Read {0} patch entries'.format(len(patch)), file=sys.stderr)

    return patch



def patchGpx(gpx, patch):
    """
    Patch geocaching GPX data with the given patch set.  GPX data is provided as a list containing the lines
    of XML representation.
    """

    patchcount = 0
    namePattern = re.compile('^\s*<name>(GC[A-Z0-9]+)</name>')
    wptPattern = re.compile('^\s*<wpt\s+lat="([0-9]+\.[0-9]+)"\s+lon="([0-9]+\.[0-9]+)"\s*>')

    lineno = 2
    while lineno < len(gpx):
        m = namePattern.match(gpx[lineno])
        if m and m.group(1) in patch:
            if wptPattern.match(gpx[lineno-2]):
                p = patch[m.group(1)]
                gpx[lineno-2] = '  <wpt lat="{0:.5f}" lon="{1:.5f}">\n'.format(p['lat'], p['lon'])
                patchcount = patchcount + 1
                if verbose:
                    print('{0}'.format(p), file=sys.stderr)
            else:
                print('ERROR: Did not find wpt element for {0}, ignoring it'.format(p), file=sys.stderr)
        lineno += 1

    if verbose:
        print('{0} entries patched'.format(patchcount), file=sys.stderr)



def main():

    global verbose

    # Get script arguments
    args = getArguments()
    verbose = args.verbose

    gpx = readGpxData(args.gpxfile)
    patch = readPatchData(args.patchfile)
    patchGpx(gpx, patch)
    writeGpxData(args.gpxfile, gpx)



if __name__ == '__main__':
    main()
