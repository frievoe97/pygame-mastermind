from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# IP-Adresse und Port für den Server
server_ip = "127.0.0.1"
server_port = 8080

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_POST(self):
        # Verarbeiten der HTTP POST-Anfrage
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data)

        # Beispielhafte Verarbeitung der Anfrage
        response_data = {
            "gameid": request_data.get("gameid"),
            "gamerid": request_data.get("gamerid"),
            "positions": request_data.get("positions"),
            "colors": request_data.get("colors"),
            "value": "Response to the request",
        }

        # Senden der Antwort
        self._set_response()
        self.wfile.write(json.dumps(response_data).encode())

# Starten des Servers
def run_server(server_ip, server_port):
    server_address = (server_ip, server_port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server gestartet auf {}:{}".format(server_ip, server_port))
    httpd.serve_forever()

if __name__ == "__main__":
    run_server(server_ip, server_port)
