import requests

# IP-Adresse und Port des Servers
server_ip = "127.0.0.1"
server_port = 8080

# URL für die HTTP POST-Anfrage
url = f"http://{server_ip}:{server_port}/api/endpoint"

# JSON-Daten, die an den Server gesendet werden sollen (Beispiel)
data = {
    "gameid": 123,
    "gamerid": "player1",
    "positions": 4,
    "colors": 6,
    "value": ""
}

def validate_response(response_data):
    """
    Validiert die Antwort gegen das JSON-Schema.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://htwberlin.com/ssr/superhirnserver/move_schema.json",
        "title": "Move",
        "_comment": "Farbkodierung= 1=Rot, 2=Grün, 3=Gelb, 4=Blau, 5=Orange, 6=Braun, 7=Weiss (Bewertung bzw. Spielfarbe), 8=Schwarz (Bewertung bzw. Spielfarbe)",
        "gameid": {
          "description": "The Id of a certain game. 0 if you want to start a new game.",
          "type": "integer"
        },
        "gamerid": {
          "description": "The Id (String) of of the gamer. Freely selectable at the beginning of the game.",
          "type": "string"
        },
        "positions": {
          "description": "How many positions (>=1, <=9) does the pattern to be guessed have?. Selectable at the beginning of the game.",
          "type": "integer"
        },
        "colors": {
        "description": "What is the maximum number of different colors (>=1, <=8) in the pattern to be guessed?. Selectable at the beginning of the game.",
        "type": "integer"
        },
        "value": {
        "description": "Either the attempt to be evaluated (request to the server) or the evaluation (response from the server). Empty String at game start.",
        "type": "string"
        },
        "required": [ "gameid", "gamerid", "positions", "colors", "value"]
    }

    # Hier sollte die Validierung mit dem JSON-Schema stattfinden
    # Verwenden Sie beispielsweise die `jsonschema`-Bibliothek
    # Rückgabe True, wenn das JSON-Schema gültig ist, andernfalls False
    return True

def process_response(response_data):
    """
    Verarbeitet die gültige Antwort.
    """
    # Führen Sie hier die gewünschten Operationen mit den Daten der Antwort durch
    print("Antwort erhalten:", response_data)

def handle_invalid_response(response_data):
    """
    Behandelt den Fall einer ungültigen Antwort.
    """
    print("Ungültige Antwort erhalten:", response_data)

def handle_failed_request(status_code):
    """
    Behandelt den Fall einer fehlgeschlagenen Anfrage.
    """
    print("Fehlerhafte Anfrage:", status_code)

# Senden der HTTP POST-Anfrage mit den JSON-Daten
response = requests.post(url, json=data)

# Überprüfen des Statuscodes der Antwort
if response.status_code == 200:
    # Die Anfrage war erfolgreich
    response_data = response.json()  # JSON-Daten aus der Antwort extrahieren
    # Validieren der Antwort gegen das JSON-Schema und weitere Verarbeitung
    if validate_response(response_data):
        # Die Antwort hat das erwartete JSON-Schema
        process_response(response_data)
    else:
        # Die Antwort hat ein ungültiges JSON-Schema
        handle_invalid_response(response_data)
else:
    # Die Anfrage war nicht erfolgreich
    handle_failed_request(response.status_code)
