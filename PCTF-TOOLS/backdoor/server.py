#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

Ref: https://gist.github.com/bmcculley/e716d7326d6a7b0edfd6a33feef6840e
"""
import logging
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

LOGGING_FORMAT = "%(asctime)s %(levelname)s: %(message)s"
FLAG_PATH = "/healthcheck"

class BaseServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if (self.path.startswith(FLAG_PATH)):
            #TODO process flags
            pass
        self._set_headers()
        self.wfile.write("ok".encode('utf-8'))

    def log_message(self, format, *args):
        logging.info("Source address {} ; Request {} ; Status {}".format(self.client_address[0], args[0], args[1]))

def run(server_class=HTTPServer, handler_class=BaseServer, port=18080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('HTTP server running on port %s'% port)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    logging.basicConfig(level=logging.DEBUG, filename="./logs/server_{}.log".format(time.strftime("%Y%m%d_%H%M%S")), filemode="w", format=LOGGING_FORMAT)
    logging.info("Starting server")

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
