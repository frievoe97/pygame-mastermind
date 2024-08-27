import requests
import json

IP_ADDRESS = "141.45.36.52"
PORT = 5001

IP_ADDRESS = "127.0.0.1"
PORT = 8001


def send_request(gameid, gamerid, positions, colors, value):
    """
    Sends a request to a server with the provided data.

    Args:
        gameid (int): The game ID.
        gamerid (str): The player's name.
        positions (int): The number of positions.
        colors (int): The number of colors.
        value (str): The value.

    Returns:
        int: The updated game ID.

    Raises:
        requests.exceptions.RequestException: If there is an error during the request.
    """

    global response
    url = "http://{}:{}".format(IP_ADDRESS, PORT)

    data = {
        "gameid": gameid,
        "gamerid": gamerid,
        "positions": positions,
        "colors": colors,
        "value": value
    }

    headers = {"Content-Type": "application/json"}

    try:
        # Send POST request to the server
        # print(json.dumps(data))
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response_data = response.json()
        response.raise_for_status()

        if response.status_code == 200:
            print("Request sent successfully.")
            print("Sent data:", json.dumps(data))

            # Extract response data
            gameid = response_data.get("gameid", gameid)
            gamerid = response_data["gamerid"]
            positions = response_data["positions"]
            colors = response_data["colors"]
            value = response_data["value"]

            print("Received data:", response_data)
            print("gameid:", gameid)
            print("gamerid:", gamerid)
            print("positions:", positions)
            print("colors:", colors)
            print("value:", value)
            print("")

            return gameid, value

    except requests.exceptions.RequestException as e:
        print("Error sending the request:", str(e))
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 400:
            response_data = e.response.json()
            error_message = response_data.get("error")
            if error_message:
                print("Server error message:", error_message)

    return gameid, value


# Example usage
gameid = 52342485
gamerid = "Friedrich"
positions = 6
colors = 8
value = "123456"

# Send multiple requests
gameid = send_request(322, gamerid, positions, colors, "111111")
# gameid = send_request(gameid, gamerid, positions, colors, value)
# gameid = send_request(gameid, gamerid, positions, colors, value)
# gameid = send_request(gameid, gamerid, positions, colors, value)
# gameid = send_request(gameid, gamerid, positions, colors, value)
# gameid = send_request(gameid, gamerid, positions, colors, value)
