import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "YOUR_TWILIO_ACCOUNT_SID"
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
from_number = "YOUR_TWILIO_PHONE_NUMBER"
to_number = "YOUR_PHONE_NUMBER"

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

will_rain = any(int(hour_data["weather"][0]["id"]) < 700 for hour_data in weather_slice)

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ.get('https_proxy')}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_=from_number,
        to=to_number
    )
    print(message.status)

# In this optimized version:
#
# The any() function is used to check if any hour within the weather slice predicts rain. It avoids unnecessary
# iterations after the first occurrence of a rainy hour.
#
# The values for OWM_Endpoint, api_key, and auth_token are fetched from environment variables using os.environ.get().
# Make sure to set these environment variables with the correct values.
#
# The from_number and to_number variables are defined at the beginning, making it easier to update the phone numbers
# when needed.
#
# The use of a list comprehension in the any() function simplifies the code and improves readability.
#
# The os.environ.get('https_proxy') call is used to retrieve the HTTPS proxy value from the environment variables.
#
# By implementing these optimizations, the code is more concise and efficient.
