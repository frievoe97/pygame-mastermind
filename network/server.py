import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
sys.path.insert(0, '..')

from logic.general_logic import calculate_pins

IP_ADDRESS = "127.0.0.1"
PORT = 8005

all_codes = {}


def generate_secret_code(positions, colors):
    random_string = ""
    for _ in range(positions):
        random_string += str(random.randint(1, colors))
    return random_string


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            json_data = json.loads(post_data)

            required_keys = ["gameid", "gamerid", "positions", "colors", "value"]
            if not all(key in json_data for key in required_keys):
                raise ValueError("Ungültige JSON-Daten")
        except (json.JSONDecodeError, ValueError) as e:
            self._set_response(400)
            response = {
                "error": str(e)
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        gameid = json_data.get("gameid")
        positions = json_data.get("positions")
        colors = json_data.get("colors")
        gamerid = json_data.get("gamerid")
        value = None

        if gameid == 0 or not gameid in all_codes:
            gameid = random.randint(1, 10000)
            all_codes[gameid] = generate_secret_code(positions, colors)
            value = ""
            print("Solution:", all_codes[gameid])
        else:
            print("Use exicsting gameid")
            code = all_codes[gameid]
            guess = json_data.get("value")
            print("Guess: ", guess)
            black_pins, white_pins = calculate_pins(list(code), list(guess))
            value = '7' * white_pins + '8' * black_pins
            print("White Pins:", white_pins)
            print("Black Pins:", black_pins)

        response = {
            "gameid": gameid,
            "gamerid": gamerid,
            "positions": positions,
            "colors": colors,
            "value": value,
        }

        print("Solution: ", all_codes[gameid])

        self._set_response()
        self.wfile.write(json.dumps(response).encode("utf-8"))


def run_server():
    server_address = (IP_ADDRESS, PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server läuft auf {}:{}".format(IP_ADDRESS, PORT))
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
