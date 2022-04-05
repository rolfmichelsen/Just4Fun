#! /usr/bin/env python3
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
        self.handleRequest()


    def do_POST(self):
        """
        Handle client POST request
        """
        self.handleRequest()


    def handleRequest(self):
        request = self.captureRequest()
        self.logRequest(request)
        self.outputResponse(request)



    def captureRequest(self):
        request = {}

        # Capture the request method and URL
        request["method"] = self.command
        request["request"] = self.requestline

        # Capture request headers
        headers = {}
        for (key, header) in self.headers.items():
            headers[key] = header
        request["headers"] = headers

        # Capture request body
        contentLength = int(request["headers"]["Content-Length"])
        if contentLength > 0:
            request["body"] = str(self.rfile.read(contentLength), "utf-8")
        else:
            request["body"] = ""

        return request


    def outputResponse(self, response):
        """
        Output response
        """
        self.send_response(200, "OK");
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response, sort_keys=True, indent=4).encode("utf-8"))


    def logRequest(self, request):
        print(request["request"], file=sys.stderr)
        print("\nHeaders:", file=sys.stderr)
        headers = request["headers"]
        for (name, value) in headers.items():
            print("  {0} : {1}".format(name, value), file=sys.stderr)
        print("\nBody", file=sys.stderr)
        print(request["body"], file=sys.stderr)
        print("----\n", file=sys.stderr)




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
        return

    port = args.port

    print("Starting HTTP server on port {}".format(port))
    serverAddress = ("", port)
    server = http.server.HTTPServer(serverAddress , RequestHandler)
    server.serve_forever()




if __name__ == '__main__':
    main()
