#! /bin/env python3
#
# Simple HTTP server for testing purposes.
#
# The server handles GET requests by returning a JSON object containing the
# request string and all request headers.

import http.server
import json
import sys
from argparse import ArgumentParser



class RequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """
        Handle client GET requests.
        """
        response = {}

        # Capture the URL request
        response["request"] = self.requestline

        # Capture all header fields
        headers = {}
        for (key, header) in self.headers.items():
            headers[key] = header
        response["headers"] = headers

        # Return the response
        self.send_response(200, "OK")
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response, sort_keys=True, indent=4).encode("utf-8"))


def getArguments():
    """
    Get command line arguments.
    """

    description = "Simple HTTP server for testing."
    epilog = '''
    The server handles GET requests by returning a JSON object containing the request URL and
    all request header fields.
    '''
    argParser = ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars='@')
    argParser.add_argument('port', type=int, nargs='?', help='Server port')
    return argParser.parse_args()


def main():
    args = getArguments()

    if not args.port:
        print("ERROR: A server port must be specified with the --port argument.", file=sys.stderr)

    port = args.port

    print("Starting HTTP server on port {}".format(port))
    serverAddress = ("", port)
    server = http.server.HTTPServer(serverAddress , RequestHandler)
    server.serve_forever()




if __name__ == '__main__':
    main()
