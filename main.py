# Import the necessary functions from the module
from flask import Flask, render_template, request, redirect, url_for
from covid_data_handler import covid_API_request
from covid_news_handling import update_news
from time_conversions import current_time_hhmm
import json

# Global variables
news = []
schedUpd = []

# Init
local7 = 0
national7 = 0
hospital_cases = 0
total_deaths = 0

app = Flask(__name__)


@app.route('/')
def default():
    return redirect(url_for("index"))


@app.route('/index')
def index():

    global schedUpd
    global news
    global local7
    global national7
    global hospital_cases
    global total_deaths

    # Go through each job scheduled and trigger the updates
    for item in schedUpd:
        # Check if time has passed
        if item["schedTime"] <= current_time_hhmm():

            if item["updCovData"] == True:
                # Trigger Covid data update
                latest_cov_data_local = covid_API_request()
                latest_cov_data_nation = covid_API_request("England", "nation")

                # Fill required parameters
                local7 = latest_cov_data_local["last_7_days_cases"]
                national7 = latest_cov_data_nation["last_7_days_cases"]
                hospital_cases = latest_cov_data_nation["hospital_cases"]
                total_deaths = latest_cov_data_nation["death_cases"]

            if item["updCovNews"] == True:
                # Trigger Covid news update
                if len(news) == 0:          # This ensures that closed articles will not be fetched again
                    news = update_news()

            # Finally remove the executed scheduled task
            schedUpd.remove(item)

    if request.method == "GET":
        
        # Closing of news section
        if 'notif' in request.args:
            for item in news:
                if request.args.get('notif') == item["title"]:
                    news.remove(item)

        # Scheduled updates section
        elif 'update' in request.args:
            # Fetch the different parameters in the URL
            # Update time
            upd_time = request.args.get('update')
            repeat_upd = False                         # init
            if request.args.get('repeat') == "repeat":
                repeat_upd = True
            
            # Covid data update
            if request.args.get('covid-data') == "covid-data":
                # Set to true
                upd_cov_data = True
            else:
                upd_cov_data = False
            
            # Covid news update
            if request.args.get('news') == "news":
                # Set to true
                upd_cov_news = True
            else:
                upd_cov_news = False

            # Update label
            upd_name = request.args.get('two')

            evtUpd = {}    # Init

            # It is possible that the user requested the data update immediately
            # Therefore call the APIs
            if len(upd_time) == 0 and (upd_cov_data == True or upd_cov_news == True):
                
                if upd_cov_data == True:
                    # Trigger Covid data update
                    latest_cov_data_local = covid_API_request()
                    latest_cov_data_nation = covid_API_request("England", "nation")

                    # Fill required parameters
                    local7 = latest_cov_data_local["last_7_days_cases"]
                    national7 = latest_cov_data_nation["last_7_days_cases"]
                    hospital_cases = latest_cov_data_nation["hospital_cases"]
                    total_deaths = latest_cov_data_nation["death_cases"]

                if upd_cov_news == True:
                    # Trigger Covid news update
                    if len(news) == 0:          # This ensures that closed articles will not be fetched again
                        news = update_news()
            else:
                # Schedule the updates Covid data and news independently
                if upd_cov_data == True:
                    evtUpd = job_sched(upd_name, upd_cov_data, False, upd_time)
                    schedUpd.append(evtUpd)

                    if(repeat_upd):     # Repeat
                        evtUpd = job_sched(upd_name, upd_cov_data, False, upd_time)     # Time needs to be changed!!
                        schedUpd.append(evtUpd)

                if upd_cov_news == True:
                    evtUpd = job_sched(upd_name, False, upd_cov_news, upd_time)
                    schedUpd.append(evtUpd)

                    if(repeat_upd): # Repeat
                        evtUpd = job_sched(upd_name, False, upd_cov_news, upd_time)     # Time needs to be changed!!
                        schedUpd.append(evtUpd)

        # Closing of schedule updates
        elif 'update_item' in request.args:
            # remove item from schedule list
            for item in schedUpd:
                if request.args.get('update_item') == item["title"]:
                    schedUpd.remove(item)

    # Access Image Logo from Config File
    with open("config.json") as config_file:
        data = json.load(config_file)
        myImage = data["myImage"]
    
    # Map the interface with functionality
    return render_template('index.html', title='Daily Covid-19 Update', news_articles=news[0:5], updates=schedUpd,
                           local_7day_infections=local7, national_7day_infections=national7,
                           hospital_cases=hospital_cases,
                           deaths_total=total_deaths, location="Exeter",
                           nation_location="England",image=myImage)


# Job scheduler function
def job_sched(upd_name, upd_cov_data, upd_cov_news, upd_time):

    # Init data
    updEvt = {}  # Init local dictionary data
    schedContent = ""
    if (upd_cov_data):
        schedContent = "Covid Data Update Scheduled at: " + upd_time
        updEvt["title"] = "DATA: "

    if (upd_cov_news):
        schedContent = "Covid News Update Scheduled at: " + upd_time
        updEvt["title"] = "NEWS: "
    
    updEvt["title"] = updEvt["title"] + upd_name    # Title
    updEvt["content"] = schedContent                # Content
    updEvt["updCovData"] = upd_cov_data             # Cov data upd
    updEvt["updCovNews"] = upd_cov_news             # Cov news upd
    updEvt["schedTime"] = upd_time                  # Schedule time upd

    return updEvt


if __name__ == '__main__':
    app.run()
