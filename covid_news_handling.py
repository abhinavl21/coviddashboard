import requests  # API requests library
from datetime import datetime  # Date and time
import json


# 1. Fetch latest covid news using news API
def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    # Access Api Key from Config File
    with open("config.json") as config_file:
        data = json.load(config_file)
        apikey = data["myAPIKey"]

    # Storing Api Key from Config File into variable
    myApiKey = apikey

    # Today's date
    myDate = datetime.today().strftime('%Y-%m-%d')

    # Build URL
    my_req_url = "https://newsapi.org/v2/everything?q=" + covid_terms + "&from=" + myDate + "&sortBy=popularity&" +\
                 "apiKey=" + myApiKey

    url = my_req_url
    response = requests.get(url)

    return response.json()  # Return version


# 2. Process news_api_request and return data structure for articles
def update_news(covid_terms="Covid COVID-19 coronavirus"):
    # Fetch latest news from API
    newsResponse = news_API_request(covid_terms)

    # Keep articles in a list
    list_articles = []
    list_articles = newsResponse["articles"]

    return list_articles
