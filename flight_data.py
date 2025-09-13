
class FlightData:

    def __init__(self, price : str, currency : str, segment_list : list[str], out_date : str):

        self._price = price
        self._currency = currency
        self._segments_list = segment_list
        self._out_date = out_date

    def get_price(self) -> float:
        return float(self._price)

    def __str__(self):
        return str(f"Price: {self._price} {self._currency}\n{self._segments_list}\nOut Date: {self._out_date}\n\n")


def pic_cheapest_flight(flight_data_list : list[FlightData]) -> FlightData or None:
    if flight_data_list is None:
        print("flights data list is empty")
        return None

    cheapest_flight = flight_data_list[0]

    for flight in flight_data_list[1:]:
        if flight.get_price() < cheapest_flight.get_price():
            cheapest_flight = flight

    return cheapest_flight





