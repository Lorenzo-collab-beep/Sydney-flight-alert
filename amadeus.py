import requests
from flight_data import FlightData

API_KEY = "QAxXH02pYbUqYLiu4W95HoXG6LYfjYvr"
API_SECRET = "lA0vszPEsvgO9LwE"

MAX_FLIGHTS_PER_DAY = 5
MAX_PRICE = 800
MILAN_CODE = "MIL"
SYDNEY_CODE = "SYD"

def get_token() -> str:
    payload = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url="https://test.api.amadeus.com/v1/security/oauth2/token", data=payload,
                             headers=headers)
    response.raise_for_status()

    return f"Bearer {response.json().get("access_token")}"


def request_flight_list(departure_date : str) -> requests.Response or None:
    try:
        params = {
            "originLocationCode" : MILAN_CODE,
            "destinationLocationCode" : SYDNEY_CODE,
            "departureDate" : departure_date,
            "adults" : 1,
            "nonStop": "false",
            "currencyCode" : "EUR",
            "maxPrice" : MAX_PRICE,
            "max" : MAX_FLIGHTS_PER_DAY
        }

        headers = {
            "Authorization": get_token()
        }

        response = requests.get(url="https://test.api.amadeus.com/v2/shopping/flight-offers", params=params,
                                headers=headers)
        response.raise_for_status()

        return response

    except Exception as e:
        print(f"Flight request failed do to: {e}")
        return None


def request_cheapest_flight(departure_date : str) -> FlightData or None:
    data = request_flight_list(departure_date)

    if data is None:
        print(f"{departure_date}: no response data")
        return None

    json_data = data.json()
    flight_list = json_data.get("data", [])

    #print(json_data)

    if not flight_list:
        print(f"{departure_date}: no flights data")
        return None

    def build_flight_data(flight):
        try:
            segments_list = []
            for segment in flight["itineraries"][0]["segments"]:
                segments_list.append(f"From: {segment["departure"]["iataCode"]} To: {segment["arrival"]["iataCode"]}")

            return FlightData(
                flight["price"]["grandTotal"],
                flight["price"]["currency"],
                segments_list,
                flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            )
        except (KeyError, IndexError, ValueError) as e:
            print(f"Skipping flight due to error: {e}")
            return None

    cheapest_flight = build_flight_data(flight_list[0])

    for f in flight_list[1:]:
        current_flight = build_flight_data(f)
        if current_flight and current_flight.get_price() < cheapest_flight.get_price():
            cheapest_flight = current_flight

    return cheapest_flight