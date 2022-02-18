# !/usr/bin/python
# A web scraper for scrobbling WMFO shows to last.fm
# By Tyler Calabrese

# Notes: You will need your last.fm API key and username in 

# Used GeeksforGeeks Scrape Tables From any website using Python

import argparse
import sys, os
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from dateutil.parser import parse
from datetime import *
import time

from dotenv import load_dotenv

import pylast

url = 'https://www.wmfo.org'

def rows_from_url(url):
    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.add_argument("--headless")
    driver = webdriver.Firefox(options=firefoxOptions)
    driver.get(url)

    return driver.find_elements(By.XPATH, '//tr')


# track should be a table row element
def extract_track(track):
    spintimestr = track.find_element(By.XPATH, './/td[@class="spin-time"]/a').text
    spintime = parse(spintimestr, default=datetime.now())
    spinunixtime = int(spintime.timestamp())

    artist = track.find_element(By.XPATH, './/span[@class="artist"]').text
    title = track.find_element(By.XPATH, './/span[@class="song"]').text
    try:
        album = track.find_element(By.XPATH, './/span[@class="release"]').text
    except NoSuchElementException:
        album = ''

    return {"timestamp":spinunixtime, "artist": artist, "title": title,
            "album": album}


def choose_to_send(track, network):
   promptstr =  "scrobble " + track["title"] + " by " + track["artist"]
   promptstr +=  "? y/n "
   choice = input(promptstr)
   if choice == 'y': send_scrobble(track, network)


def send_scrobble(track, network):
    print("scrobbling ", track)
    if track == '':
        network.scrobble(artist=track["artist"], title=track["title"],
                         timestamp=track["timestamp"])
    else:
        network.scrobble(artist=track["artist"], title=track["title"],
                         timestamp=track["timestamp"], album=track["album"])
    print("done.")


def setup_lastfm():
    load_dotenv()
    API_KEY = os.environ.get("API_KEY")
    API_SECRET = os.environ.get("API_SECRET")
    USERNAME = os.environ.get("USERNAME")
    HASHED_PASS = os.environ.get("HASHED_PASS")
    return pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=USERNAME,
        password_hash=HASHED_PASS
    )


def main():
    print("getting songs from", url)
    rows = rows_from_url(url)

    tracks = list(map(extract_track, rows))

    promptstr =  "found " + str(len(tracks)) + " tracks. "
    promptstr += "s to scrobble all, p to pick tracks to scrobble, "
    promptstr += "or c to cancel. "
    choice = input(promptstr)

    if choice == 's' or choice == 'p':
        last_fm_net = setup_lastfm()
    if choice == 's':
        for track in tracks: send_scrobble(track,  last_fm_net)
    if choice == 'p':
        for track in tracks: choose_to_send(track, last_fm_net)
    if choice == 'c':
        print('Canceling. Nothing will be scrobbled.')

if __name__ == '__main__':
    main()

