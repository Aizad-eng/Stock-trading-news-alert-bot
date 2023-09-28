import json
from datetime import datetime, timedelta
import requests
from twilio.rest import Client

account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
client = Client(account_sid, auth_token)


STOCK_API_KEY = "YOUR_STOCK_API_KEY"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
API_KEY_NEWS = "YOUR_NEWS_API_KEY"
NEWS_URL = "https://newsapi.org/v2/top-headlines"


parameters_for_stock_api = {
    "function":"TIME_SERIES_DAILY",
    "symbol":"TSLA", #Replace it with the name of company you are interested in: Make sure the the short abbreviation is correct.
    "datatype":"json",
    "apikey":STOCK_API_KEY
}

NEWS_API_PARAMETERS = {
    "apiKey":API_KEY_NEWS,
    "country":"us",
    "category":"business",
    "q":"Tesla" #Replace it with the name of company you are interested in

}

the_day_before_yesterday = str((datetime.now()-timedelta(days=2)).date())
yesterday_date = str((datetime.now() - timedelta(days=1)).date())


todays_date = datetime.now().date() - timedelta(days=1)
response = requests.get(url = STOCK_ENDPOINT, params=parameters_for_stock_api)
response.raise_for_status()

data = response.json()
yesterday_closing_price = data["Time Series (Daily)"][yesterday_date]["4. close"]

the_day_before_yesterday_closing_price = data["Time Series (Daily)"][the_day_before_yesterday]["4. close"]


difference = round(float(yesterday_closing_price) - float(the_day_before_yesterday_closing_price), 2)
percentage_decrease = (difference / float(the_day_before_yesterday_closing_price)) * 100

if percentage_decrease < 0:
    result = f"Stocks went down by {abs(percentage_decrease):.2f}% "
else:
    result = f"Stocks went up by {abs(percentage_decrease):.2f}%"


news_response = requests.get(url=NEWS_URL, params=NEWS_API_PARAMETERS)

for article in news_response.json()["articles"]:
    message = client.messages.create(
        from_="YOUR_TWILIO_NUMBER",
        to='RECIPIENTS_NUMBER',
        body=f'{result}\n {article["title"]}'
    )

print(message.sid)