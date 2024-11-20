from http.server import HTTPServer, BaseHTTPRequestHandler
from main import result

HOST = "127.0.0.1"
PORT = 8080

class NeuralHTTP(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("HELLO", "utf-8"))


server = HTTPServer((HOST, PORT), NeuralHTTP)
print("Server is running")
server.serve_forever()
server.server_close()