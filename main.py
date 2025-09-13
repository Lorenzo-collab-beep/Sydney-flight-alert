import datetime
import time
import amadeus
import flight_data
import notifier

SLEEP_TIME = 1
DAY_TO_CHECK = 3

date_start = datetime.datetime.today()
date_end = date_start + datetime.timedelta(days=DAY_TO_CHECK)

cheaper_flight_list = []

while date_start < date_end:

    temp_cheaper_flight = amadeus.request_cheapest_flight(date_start.strftime("%Y-%m-%d"))

    if temp_cheaper_flight is not None:
        cheaper_flight_list.append(temp_cheaper_flight)

    date_start += datetime.timedelta(days=1)
    time.sleep(SLEEP_TIME)


cheaper_flight = flight_data.pic_cheapest_flight(cheaper_flight_list)

if cheaper_flight is not None:
    mail_message = (f"Found {len(cheaper_flight_list)} flights in {DAY_TO_CHECK} days from today\n"
                    f"Here the cheaper one:\n\n{str(cheaper_flight)}")

    notifier.send_email(mail_message)

