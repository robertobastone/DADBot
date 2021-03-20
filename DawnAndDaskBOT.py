################################################### INTRO

author = 'Roberto Bastone '

version = 1.00

######################### LIBRARIES #########################

import tweepy # TWIITER INTEGRATION
import credentials # GET CREDENTIALS
import requests # CALL GET
from datetime import datetime, timezone # GET TIME
from dateutil.parser import parse as parse_date #CONVERT UNICODE INTO DATETIME
import sys # better management of the exceptions

# timezone
utc = "+00:00" 
# thanking
thanking_site = 'https://sunrise-sunset.org/api'
thanking_hashtags = "\n #Python #pythonlearning"
thanking_message = ". This bot was made thanks to " + thanking_site + " and Tweepy." + thanking_hashtags

##### GENERATING GET REQUEST
base_url = 'https://api.sunrise-sunset.org/json?'
latitude = 'lat=40.8518&'
longitude = 'lng=14.2681&'
date = 'date=today&'
timeFormat = 'formatted=0'

# CALLING SERVICE
resp = requests.get(base_url+latitude+longitude+date+timeFormat)

# MANAGING RESPONSE
if resp.status_code != 200:
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
else:
    jsonResponse = resp.json()
    sunrise = parse_date(jsonResponse['results']['sunrise']).time()
    sunset = parse_date(jsonResponse['results']['sunset']).time()
    main_message = "Today, in Napoli (Italia), the sun will rise at " + str(sunrise) + utc + " and the sun will set at " + str(sunset) + utc

##### GENERATING TWITTER REQUEST
# Authenticate to Twitter
auth = tweepy.OAuthHandler(credentials.consumer_key,credentials.consumer_secret)
auth.set_access_token(credentials.access_key,credentials.access_token)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
    api.update_status(main_message + thanking_message)
except Exception as e:
    print("The following exception was catched: " + str(e))
