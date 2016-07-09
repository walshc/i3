# -*- coding: utf-8 -*-
import geocoder
import json
import requests

# forecast.io api key:
f = open('/home/christoph/.config/forecast-io-key')
key = f.readline().rstrip()
f.close()

# Get current longitude and latitude based on IP address:
loc = geocoder.ip(requests.get('http://ipinfo.io/ip').text.rstrip())
city = loc.locality

# Get weather info:
root_url = 'https://api.forecast.io/forecast/'
weather = requests.get(root_url + key + '/' + str(loc.lat) + ',' + str(loc.lng))
weather = json.loads(weather.text)

# Convert temperature to Celcius:
temperature = round((weather['currently']['temperature'] - 32) * 5/9)

# Get current weather condition:
condition = weather['currently']['summary']

# Translate city into Irish:
cdict = dict({'Boston': {'irish': 'Bostún'}})

try:
    cathair = cdict[city]['irish']
except KeyError:
    cathair = city

icons = dict({'Cloudy' : '\uf590', 'Fog' : '\uf591', 'Snow' : '\uf592',
    'Thunder' : '\uf593', 'Clear (Night)': '\uf594',
    'Partly Cloudy' : '\uf595', 'Rain' : '\uf596',
    'Sunny' : '\uf599'})

# Based on current condition, get icon and Irish translation:
wdict = dict({'Overcast': {'icon': icons['Cloudy'], 'irish': 'Modartha'},
    'Partly Cloudy': {'icon': icons['Partly Cloudy'],
        'irish': 'Breacscamallach'},
    'Mostly Cloudy': {'icon': icons['Cloudy'], 'irish': 'Scamallach'},
    'Scattered Clouds': {'icon': icons['Partly Cloudy'],
        'irish': 'Scamaill Scaipthe'},
    'Sunny': {'icon': icons['Sunny'], 'irish': 'Tá an ghrian ag taitneamh'},
    'Clear': {'icon': icons['Sunny'], 'irish': 'Lá breá atá ann'},
    'Light Rain': {'icon': icons['Rain'], 'irish': 'Báisteach Éadrom'},
    'Drizzle': {'icon': icons['Rain'], 'irish': 'Ceobhrán'}})

# Get an icon based on the current weather condition:
try:
    icon = wdict[condition]['icon']
except KeyError:
    icon = ''

try:
    aimsir=wdict[condition]['irish']
except KeyError:
    aimsir=condition

# Print output:
out = icon + '-' + cathair + ': ' + aimsir + ', ' + str(temperature) + '°C'
print(out)
