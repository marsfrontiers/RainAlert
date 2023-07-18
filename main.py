# Note! For the code to work you need to replace all the placeholders with
# Your own details. e.g. account_sid, lat/lon, from/to phone numbers.

import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("c8bc8e4c1c966a37ece0e35ecfe02a33")
account_sid = "AC24f1f4883e5ea5aa54f57fc22b0fedce"
auth_token = os.environ.get("7e32685b0cbbdcad6f6a43914e87fb09")

weather_params = {
    "lat": 25.442190,
    "lon": 81.840919,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_='+12542496791',
        to='+918896927066'
    )
    print(message.status)
