from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
from dotenv import load_dotenv
import json
import time
import os

# импортируем переменные из dotenv
load_dotenv()

checker_status = [{"status": "N/A"}]


class _RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps(checker_status).encode('utf-8'))

    def do_POST(self):
        global checker_status
        checker_status = []
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        checker_status.append(message)
        self._set_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

    def do_OPTIONS(self):
        # Send allow-origin header for preflight POST XHRs.
        self.send_response(HTTPStatus.NO_CONTENT.value)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()


def run_server():
    server_address = (os.getenv('HOST'), int(os.getenv('PORT')))
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()