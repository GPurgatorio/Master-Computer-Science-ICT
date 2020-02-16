# Standard library imports...
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import socket
from threading import Thread

# Third-party imports...
import requests


class MockServerRequestHandler(BaseHTTPRequestHandler):
    NEW_PATTERN = re.compile(r'^/(new|delete)$')

    # Status response code
    _status_code = requests.codes.ok
    # Body response JSON
    _body_response = json.dumps([])

    def do_POST(self):
        if re.search(self.NEW_PATTERN, self.path):
            # Add response status code.
            self.send_response(self._status_code)

            # Add response headers.
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            # Add response content.
            response_content = self._body_response
            self.wfile.write(response_content.encode('utf-8'))
            return

    def do_DELETE(self):
        if re.search(self.NEW_PATTERN, self.path):
            # Add response status code.
            self.send_response(self._status_code)

            # Add response headers.
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            # Add response content.
            response_content = self._body_response
            self.wfile.write(response_content.encode('utf-8'))
            return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
