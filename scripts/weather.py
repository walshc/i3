# -*- coding: utf-8 -*-
import geocoder
import json
import locale
import os
import requests
import pandas as pd
import urllib

# forecast.io api key:
f = open('/home/christoph/.config/forecast-io-key')
key = f.readline().rstrip()
f.close()

# Get current longitude and latitude based on IP address:
ip = requests.get('http://ipinfo.io/ip').text.rstrip()
loc = geocoder.freegeoip(ip)
city = loc.locality
if city == None:
    city = geocoder.google([loc.lat, loc.lng], method='reverse').city

# Get weather info:
root_url = 'https://api.forecast.io/forecast/'
weather = requests.get(root_url + key + '/' + str(loc.lat) + ',' + str(loc.lng))
weather = json.loads(weather.text)

# Convert temperature to Celcius:
temperature = round((weather['currently']['temperature'] - 32) * 5/9)

# Get current weather condition:
condition = weather['currently']['summary']

# Translate city when approriate:
cdict = dict({'Boston': {'ga': 'Bostún'},
    'Dublin': {'ga': 'Baile Átha Cliath'}})

language = locale.getlocale()[0]
if language == 'ga_IE':
    try:
        city = cdict[city]['ga']
    except KeyError:
        city = city
elif language == 'de_DE':
    try:
        city = cdict[city]['de']
    except KeyError:
        city = city

# Get weather translation and icon:
df = pd.read_csv(os.path.expanduser('~/') + '.i3/scripts/weather.csv')
df = df[df.en == condition]

if df.shape[0] == 0:
    icon = ''
    weather = condition
else:
    icon = df.icon.values[0]
    icon = bytes(icon, 'ascii').decode('unicode-escape')
    if language == 'de_DE':
        weather = df.de.values[0]
    elif language == 'ga_IE':
        weather = df.ga.values[0]
    else:
        weather = condition

# Print output:
out = icon + '-' + city + ': ' + weather + ', ' + str(temperature) + '°C'
print(out)
