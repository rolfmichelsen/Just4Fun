#! /bin/env python3
#
# Simple HTTP server for testing purposes.

import http.server
import sys
from argparse import ArgumentParser



class RequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.requestline)
        for (key, header) in self.headers.items():
            print("{} : {}".format(key, header))
        print("---")

        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(b"Thanks for all the fish...")



def getArguments():
    """
    Get command line arguments.
    """

    description = "Simple HTTP server for testing."
    epilog = '''
    '''
    argParser = ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars='@')
    argParser.add_argument('port', type=int, nargs='?', help='Server port')
    return argParser.parse_args()


def main():
    args = getArguments()
    port = args.port

    print("Starting HTTP server on port {}".format(port))
    serverAddress = ("", port)
    server = http.server.HTTPServer(serverAddress , RequestHandler)
    server.serve_forever()




if __name__ == '__main__':
    main()
