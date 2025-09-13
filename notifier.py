import smtplib
import dotenv
import os

dotenv.load_dotenv()

APP_MAIL = os.getenv("APP_MAIL")
APP_PWD = os.getenv("APP_PWD")

PERS_MAIL = os.getenv("PERS_MAIL")

def send_email(letter_body : str):
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()  # secure the connection (tls)

    connection.login(user=APP_MAIL, password=APP_PWD)
    message = f"Subject: Sydney Alert: Best Price Notifier\n\n{letter_body}"
    print(message)
    connection.sendmail(from_addr=APP_MAIL, to_addrs=PERS_MAIL, msg=message.encode("utf-8"))
    connection.close()
