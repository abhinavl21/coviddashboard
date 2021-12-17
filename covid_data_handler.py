import csv  # CSV Library
import sched  # Scheduler
import json  # JSON Library
from uk_covid19 import Cov19API  # UK Covid19 API Library
from covid_news_handling import update_news  # News API
from datetime import datetime, timedelta
import time


# 1. Parse CSV data functionality - Read data from file
def parse_csv_data(csv_filename):
    file_in = open(csv_filename)  # Open the CSV file
    csv_read = csv.reader(file_in)  # Read the contents of the CSV file
    header = next(csv_read)  # Skip the header and move to next line

    row_contents = []  # Init row list

    for i in csv_read:
        row_contents.append(i)  # Add each row to array

    file_in.close()  # Close file and return the row contents
    return row_contents


# 2. Data processing functionality - Process CSV data
# This function will calculate 3 variables
# a.    last_7_days_cases
# b.    curr_hospital_cases
# c.    cumm_deaths
def process_covid_csv_data(covid_csv_data):
    # a. Calculate the last 7 days cases ignoring 1st entry as incomplete
    i = 0  # Init
    last_7_days_cases = 0  # Init

    # First entry is ignored, sum the 7th column for the new cases by specimen date
    while i <= 8:
        if i > 1:
            last_7_days_cases = last_7_days_cases + int(covid_csv_data[i][6])  # 7th column

        i = i + 1  # Increment index counter

    # Lookup for the current no. of hospital cases and cumm no. of deaths looping through
    # the CSV data
    i = 0  # Init
    curr_hospital_cases = ""  # Init
    cumm_deaths = ""  # Init

    for i in range(len(covid_csv_data)):
        # b. Calculate curr_hospital_cases
        if len(curr_hospital_cases) == 0:
            curr_hospital_cases = covid_csv_data[i][5]  # 6th column for hospital cases

        # c. Calculate curr_hospital_cases
        if len(cumm_deaths) == 0:
            cumm_deaths = covid_csv_data[i][4]  # 5th column for hospital cases

        # If both curr_hospital_cases and cumm_deaths are filled, no need to continue loop
        if len(curr_hospital_cases) > 0 and len(cumm_deaths) > 0:
            break

    # Return the calculated variables
    return last_7_days_cases, int(curr_hospital_cases), int(cumm_deaths)


# Access location and location_type from Config File
with open("config.json") as config_file:
    data = json.load(config_file)
    location_configFile = data["location"]
    location_type_configFile = data["location_type"]


# 3. Live data access functionality - Covid API request
# This func extracts latest COVID-19 data from an API with default values provided
def covid_API_request(location=location_configFile, location_type=location_type_configFile):
    # Init dictionary
    cov_data_dict = {}

    # Area code filter
    areaType = "areaType=" + location_type
    areaName = "areaName=" + location

    area_code_filter = [
        areaType,
        areaName
    ]

    # Structure for metrics needed
    cases_and_deaths = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDateRollingSum": "newCasesBySpecimenDateRollingSum",
    }

    # Instantiate the api
    api = Cov19API(
        filters=area_code_filter,
        structure=cases_and_deaths
        # latest_by="date"
    )

    # Do the API call to fetch the data in JSON format
    cov_data_json = api.get_json(as_string=True)

    # Data returned should be converted to dictionary format for easy manipulation
    cov_data_dict = json.loads(cov_data_json)

    # A proper data dictionary should be returned to easily map the figures
    upd_cov_data = {}  # This dictionary will be returned and contains the necessary data in the proper format

    # Current date
    myCurrDate = datetime.today().strftime('%Y-%m-%d')

    last_7_days_cases = 0
    hospital_cases = 0
    death_cases = 0

    # Calculation of figures
    i = 0
    while last_7_days_cases == 0:

        if i == 0:  # Latest data
            # Calculate latest hospital cases
            if isinstance(cov_data_dict["data"][i]["hospitalCases"], int) == True:
                hospital_cases = cov_data_dict["data"][i]["hospitalCases"]

            # Calculate latest death cases
            if isinstance(cov_data_dict["data"][i]["cumDeaths28DaysByPublishDate"], int) == True:
                death_cases = cov_data_dict["data"][i]["cumDeaths28DaysByPublishDate"]

        # Calculate Last 7 days cases
        if cov_data_dict["data"][i]["date"] != myCurrDate:  # Ignore current date for this

            if isinstance(cov_data_dict["data"][i]["newCasesBySpecimenDateRollingSum"], int) == True:  # Check if integer
                last_7_days_cases = cov_data_dict["data"][i]["newCasesBySpecimenDateRollingSum"]

        i = i + 1  # Index counter

    # Add to covid data dict and return
    upd_cov_data["last_7_days_cases"] = last_7_days_cases
    upd_cov_data["hospital_cases"] = hospital_cases
    upd_cov_data["death_cases"] = death_cases

    return upd_cov_data 


# 4. Automated updates functionality for Covid data and news - Note optional parameters
#    I tried to use this but the page was keeping on refreshing
def schedule_covid_updates(update_interval=5, update_name="COVID UPDATES", update_covid_data=False,
                           update_covid_news=False):
    # Init data
    updEvt = {}  # Init local dictionary data
    evt_covid_data_nat = None
    evt_covid_data_loc = None
    evt_covid_news_upd = None

    # If at least one condition has been met, schedule required updates
    if update_covid_data == True or update_covid_news == True:

        # Time schedule calculation for output
        mySchedTime = datetime.now() + timedelta(seconds=update_interval)

        # Instance is created
        scheduler = sched.scheduler(time.time, time.sleep)
        
        if update_covid_data == True:

            schedContent = "COVID DATA: "
            
            # 1. Schedule for LOCAL Covid data update
            # Calculate schedule time for covid data update
            curr_time = time.monotonic()
            sched_time = curr_time + update_interval

            # Event with time specified for covid Local data updates
            evt_covid_data_loc = scheduler.enterabs(sched_time, 1, covid_API_request)

            # 2. Schedule for NATIONAL Covid data update
            # Calculate schedule time for covid data update
            curr_time = time.monotonic()
            sched_time = curr_time + update_interval

            # Event with time specified for covid National data updates
            evt_covid_data_nat = scheduler.enterabs(sched_time, 2, covid_API_request, argument=("England", "nation"))

        if update_covid_news == True:

            schedContent = "COVID NEWS: "

            # 3. Schedule for Covid news update
            # Calculate schedule time for covid news update
            curr_time = time.monotonic()
            sched_time = curr_time + update_interval

            # If covid data update has been requested, we need to add a delay of 1 sec OR priority decides it
            if update_covid_data == True:
                sched_time = sched_time + 1

            # Event with time specified for covid data updates
            evt_covid_news_upd = scheduler.enterabs(sched_time, 3, update_news)

        # Add to local event dictionary
        schedContent = schedContent + "Update scheduled at " + str(mySchedTime)
        updEvt["title"] = update_name                   # Title
        updEvt["content"] = schedContent                # Content
        updEvt["evtCovidDataNat"] = evt_covid_data_nat  # Event created for Covid data national
        updEvt["evtCovidDataLoc"] = evt_covid_data_loc  # Event created for Covid data local
        updEvt["evtCovidNews"] = evt_covid_news_upd     # Event created for Covid news update

    return updEvt
