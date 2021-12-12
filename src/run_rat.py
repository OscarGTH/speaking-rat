#!/usr/bin/env python3
"""
Program that fetches texts and speaks it aloud.
"""

import requests
import pyttsx3
import random
import time
import logging
import json
from datetime import datetime, timedelta

__author__ = "Oskari Niskanen"
__version__ = "0.1.0"
__license__ = "MIT"


engine = pyttsx3.init()  # TTS engine creation
# Slowing down the speech rate by 5%
#engine.setProperty('voice','english+f2')
engine.setProperty('rate', 130)
rate = 130
# Counter to limit api call repeating if requests fail.
api_call_count = 0
# Datetime format
formatfrom = "%Y-%m-%dT%H:%M:%S+00:00"
# Configuring logger
logging.basicConfig(level=logging.INFO)

def read_custom_phrase():
    """ Reads a random line from custom JSON file """

    logging.info("Reading custom phrase.")
    # Opening JSON file
    f = open("../phrases/phrases.json", "r")
    # Loading data into dict
    data = json.load(f)
    # Extracting random phrase from file
    phrase = data[str(random.randint(0,(len(data)-1)))]
    # Counting words
    words = phrase.split()
    word_count = len(words)
    global rate
    # Setting speech rate based on word count
    if (word_count > 100):
        rate = 160
    # Reading the phrase
    read_string(phrase, "finnish", rate)

def read_day_statistics():
    """ Reads sunrise and sunset times out loud. """

    logging.info("Reading sunset and sunrise times.")
    url = "https://api.sunrise-sunset.org/json?lat=61.49911&lng=23.78712&date=today&formatted=0"
    response = request_api(url)
    # Checking that correct key is in response
    if 'results' in response:
        sunrise_utc = response['results']['sunrise']
        sunset_utc = response['results']['sunset']

        # Converting UTC times to GMT+2
        sunrise = datetime.strptime(
            sunrise_utc, formatfrom) + timedelta(hours=2)
        sunset = datetime.strptime(sunset_utc, formatfrom) + timedelta(hours=2)

        # Extracting hours and minutes
        rise_hour = str(sunrise.hour)
        rise_minute = str(sunrise.minute)
        set_hour = str(sunset.hour)
        set_minute = str(sunset.minute)
        # Getting time of day
        rise_am_pm = sunrise.strftime("%p")
        set_am_pm = sunset.strftime("%p")

        # Constructing cohesive sentence.
        sun_statistics = ("Sun rises at " + rise_minute + "past" + rise_hour + " " + rise_am_pm +
                          " and sets at " + set_minute + " past " + set_hour + " " + set_am_pm)

        # Reading sun statistics for current day.
        read_string(sun_statistics, "english")


def read_programming_quote():
    """ Reads a computer programming quote out loud. """

    logging.info("Reading programming quote.")
    url = "https://programming-quotes-api.herokuapp.com/quotes/random"
    response = request_api(url)
    # Checking that correct key is in response
    if 'en' in response:
        read_string(response['en'], "english")


def read_inspirational_quote():
    """ Reads a famous quote out loud."""

    logging.info("Reading inspirational quote.")
    url = "https://inspiration.goprogram.ai"
    response = request_api(url)
    # Checking that correct key is in response
    if 'quote' in response:
        read_string(response['quote'], "english")


def read_joke():
    """ Reads a joke out loud. """

    logging.info("Reading joke.")
    joke_url = "https://yomomma-api.herokuapp.com/jokes"
    response = request_api(joke_url)
    # Checking that correct key is in response
    if 'joke' in response:
        read_string(response['joke'], "english")


def choose_phrase():
    """ Chooses randomly a function to call. """

    logging.info("Choosing phrase.")
    # Possible functions to call
    possible_functions = [read_inspirational_quote,
                          read_joke, read_programming_quote, read_custom_phrase, read_day_statistics]
    rand_num = random.randint(0, 4)
    # Calling random function
    possible_functions[rand_num]()


def request_api(url):
    """ Sends a request to api and returns data as JSON. """

    global api_call_count
    r = requests.get(url)
    # If status is OK, then return response as json.
    if (r.status_code == 200):
        return r.json()
    elif (api_call_count < 5):
        print("API response was not OK from " + url)
        # Else wait for 30 seconds and try again.
        time.sleep(30)
        api_call_count = api_call_count + 1
        choose_phrase()


def read_string(sentence, language, base_rate=rate):
    """ Reads a given sentence out loud. """
    # Set chosen speech language 
    engine.setProperty('voice', language+'+f2')
    # Set speech rate
    engine.setProperty('rate', base_rate)
    engine.say(sentence)
    engine.runAndWait()


def main():
    """ Main entry point of the app """

    choose_phrase()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
