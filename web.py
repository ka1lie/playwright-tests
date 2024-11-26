from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from dotenv import load_dotenv

# импортируем переменные из dotenv
load_dotenv()

class NeuralHTTP(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            content = open('index.html', 'rb').read()
            self.wfile.write(content)
        else:
            self.send_response(404)
    def do_POST(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
        else:
            self.send_response(501)

server = HTTPServer((os.getenv('HOST'), int(os.getenv('PORT'))), NeuralHTTP)
print("Server is running")
server.serve_forever()
server.server_close()