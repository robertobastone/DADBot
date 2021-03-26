######################### LIBRARIES #########################

import tweepy # TWIITER INTEGRATION
import time # sleep time between executions
import requests # CALL GET
from datetime import datetime # GET TIME
from dateutil.parser import parse as parse_date #CONVERT UNICODE INTO DATETIME
import pytz # change time zone
import sys # better management of the exceptions
import os
from os import environ # help heroku use credentials

# timezone
cet = pytz.timezone('Europe/Rome')

# sleepTime
sleepTime = 60*60*24 # 1 day
sleepTimeRetry = 60*30 # 1/2 hour

# thanking
thanking_site = 'https://sunrise-sunset.org/api'
thanking_hashtags = "\n #Python #pythonlearning"
thanking_message = ". This tweet is auto-generated by a Python bot I created using Tweepy. The hours displayed here come from " + thanking_site + "." + thanking_hashtags

##### GENERATING GET REQUEST
base_url = 'https://api.sunrise-sunset.org/json?'
latitude = 'lat=40.8518&' # Napoli, Campania, Italia
longitude = 'lng=14.2681&'
date = 'date=today&'
timeFormat = 'formatted=0'

# CALLING SERVICE
def callSunriseSunsetApi():
    try:
        resp = requests.get(base_url+latitude+longitude+date+timeFormat)
        # MANAGING RESPONSE
        if resp.status_code != 200:
            print('GET tasks status: {}'.format(resp.status_code))
        else:
            print('GET tasks status {}'.format(resp.status_code))
            jsonResponse = resp.json()['results']
            sunrise = getSunriseSunsetTimeString(jsonResponse['sunrise'],'sunrise')
            sunset = getSunriseSunsetTimeString(jsonResponse['sunset'],'sunset')
            main_message = str(datetime.now().date().strftime('Today %d %b %Y')) + ", in Napoli, the sun " + sunrise + " and the sun " + str(sunset)
            return main_message
    except Exception as e:
        print("callSunriseSunsetApi - The following exception was catched: " + str(e))
        return "KO"

def callTwitter(main_message):
    ##### GENERATING TWITTER REQUEST
    CONSUMER_KEY = environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = environ['TWITTER_CONSUMER_SECRET']
    ACCESS_KEY = environ['TWIITER_ACCESS_KEY']
    ACCESS_SECRET = environ['TWITTER_ACCESS_SECRET']
    # Authenticate to Twitter: via environment variables
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    api = tweepy.API(auth)
    try:
        if api.verify_credentials() == False:
            print("The user credentials are invalid.")
        else:
            print("The user credentials are valid.")
            tweeting = api.update_status(main_message + thanking_message)
            print("Tweeting: " + str(tweeting))
    except Exception as e:
        print("callTwitter - The following exception was catched: " + str(e))
        print("callTwitter - we have to wait")
        time.sleep(sleepTimeRetry)
        print("callTwitter - the wait is over")
        callTwitter(main_message)

def getSunriseSunsetTimeString(datetime_sun,event_sun):
    try:
        datetime_item = parse_date(datetime_sun).astimezone(cet)
        now = datetime.now().astimezone(cet).time()
        time_item = datetime_item.time()
        if event_sun == 'sunrise':
            action_item = "rose at " if now > time_item else "will rise at "
        elif event_sun == 'sunset':
            action_item = "set at " if now > time_item else "will set at "
        else:
            action_item = 0
        timezone_item = datetime_item.tzname()
        string_sun = action_item + str(time_item) + ' ' + str(timezone_item)
        return string_sun
    except Exception as e:
        print("getSunriseSunsetTimeString - The following exception was catched: " + str(e))


try:
    while True:
        print("Starting... DADbot")
        main_message = callSunriseSunsetApi()
        print("Message is... " + main_message)
        if main_message != "KO":
            callTwitter(main_message)
            print("Tweeting completed... DADbot")
        time.sleep(sleepTime)
except Exception as e:
    print("main - The following exception was catched: " + str(e))
