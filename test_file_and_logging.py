# Import the necessary functions from the module
from covid_data_handler import parse_csv_data, process_covid_csv_data, covid_API_request, schedule_covid_updates
from covid_news_handling import news_API_request, update_news
import json
import logging

# Access Log file from Config File
with open("config.json") as config_file:
    data = json.load(config_file)
    testfile = data["TestFile"]

# Logging
logging.basicConfig(filename=testfile,level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')

# Test for CSV data parsing
data = parse_csv_data('nation_2021-10-28.csv')
print(data)
logging.info(data)

# Test for Data processing
last_7_days_cases, curr_hospital_cases, cumm_deaths = process_covid_csv_data(data)
print("Number of cases in the last 7 days:", last_7_days_cases)
print("Number of hospital cases:", curr_hospital_cases)
print("Cumulative number of deaths:", cumm_deaths)
logging.info(process_covid_csv_data(data))

# Test for Live data access
latest_cov_data = covid_API_request("England", "nation")
print(latest_cov_data)
logging.info(latest_cov_data)
latest_cov_data_exeter = covid_API_request()
print(latest_cov_data_exeter)
logging.info(latest_cov_data_exeter)


# Test for News data access
latest_covid_news = news_API_request()
print(latest_covid_news)
logging.info(latest_covid_news)

# Test for Automated updates - covid data and covid news
# A nested dictionary is used as a global variable
updates = {}
print("Init: ", updates)

updates = []
# The scheduled updates will return a dictionary, then this dictionary will be added to the global nested dictionary.
# Sched Event 1
evtUpd = schedule_covid_updates(20, "COVID UPDATE 1", True, True)
updates.append(evtUpd)
##
evtUpd = schedule_covid_updates(50, "COVID UPDATE 2", True)
updates.append(evtUpd)
##
evtUpd = schedule_covid_updates(70, "COVID UPDATE 3", True)
updates.append(evtUpd)
##
for update in updates:
    print(update["title"])
    print(update["content"])
    print("==========================")




# TEST FOR COVID NEWS UPDATE
news_articles = update_news()

for news in news_articles:
    print(news["title"])
    print(news["content"])
    print("=============================================")
