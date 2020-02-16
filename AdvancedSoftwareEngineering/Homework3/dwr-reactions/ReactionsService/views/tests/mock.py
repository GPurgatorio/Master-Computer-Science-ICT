# Standard library imports...
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import socket
from threading import Thread

# Third-party imports...
import requests


class MockServerRequestHandler(BaseHTTPRequestHandler):
    NEW_PATTERN = re.compile(r'/stories/users/')
    def do_GET(self):
        if re.search(self.NEW_PATTERN, self.path):
            # Add response status code.
            self.send_response(requests.codes.ok)

            # Add response headers.
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            # Add response content.
            result = [{
                    "author_id": 1, 
                    "date": "Mon, 25 Nov 2019 15:49:00 GMT",
                    "figures": "#ciao#",
                    "id": 1,
                    "is_draft": False,
                    "text": "ciao"
                }, {
                    "author_id": 1,
                    "date": "Mon, 25 Nov 2019 15:50:00 GMT",
                    "figures": "#ok#",
                    "id": 3,
                    "is_draft": False,
                    "text": "ok"
            }]

            response_content = json.dumps(result)
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