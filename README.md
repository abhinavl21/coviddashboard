# coviddashboard
### COVID-19 DAILY UPDATE DASHBOARD

        Personalised covid-19 dashboard to keep you up-to-date with the latest number of cases and latest covid news in the uk and your local area. 



## How to use

-Run the web application by entering the main.py file and run the script. Click on the link below.(http://127.0.0.1:5000/)
-The web application should appear on your browser with no covid data and news data.
-You can manually trigger the updates and obtain the results immediately by ticking the given boxes(Update Covid data, Update news articles) and filling the update label
without entering any time interval.
-You can also schedule either or both updates by entering a time interval and chosing the given small boxes. A box will appear on the left hand-side confirming the process.
-News articles can be removed and scheduled updates can be cancelled by clicking on the small-cross at the top of the article box.
-The main trigger to trigger the updates is the auto-refresh! Each time there is an auto-refresh, it will look whether a job was scheduled or not.  
 If yes, either COVID API data or news will be executed

## How to test

-Use the file test_file_and_logging.py to test for the functions of the python scripts.
-You can also check the test_covid_data_handler.py and test_news_data_handling.py files.
-Logging can also be found in the test_file_and_logging.py file and by opening the test.log file.

## Configuration file
Sensitive information such as api keys, configuration information such as location, location_type and other information like image logo 
and test file can be found in a configuration file rather than in the source code so that they can be easily updated.

## Modules details:

1. ## Covid Data Handler
Installating Modules
-uk-covid19
Python 3.7+ is required to install and use this library.
To install, please run:
                       pip install uk-covid19
                       You may install the library for a specific version of Python as follows:
                       python -m pip install uk-covid19


2. ## Covid News Handling

***Installation
Get a free API Key at https://newsapi.org/register
Enter your API in config.js

  

## Built With

Python 3.7+
HTML


## APIs

Coronavirus(COVID-19) in the UK-API Service
-https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/
NewsAPI
-https://newsapi.org/


## Modules used

uk_covid19
Requests
Flask
Json
Sched
datetime

## Comments can be found all around the python scripts to help developpers to understand the code so that they can use or modify it.


## Contact

Abhinav Lodeechand
abhi_221@yahoo.com
Github account link: https://github.com/abhinavl21


## Date created

10 Decemeber 2021
