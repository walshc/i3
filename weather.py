#!/usr/bin/python3

import requests
import xmltodict

url = "http://weather.yahooapis.com/forecastrss?w=2482164&u=c"
w = xmltodict.parse(requests.get(url).text)
w = w['rss']['channel']['item']['yweather:condition']

# Add unicode symbol to weather description and translate to Irish:
symbols = dict([('Cloudy', ['', 'Scamallach'] ),
               ('Mostly Cloudy', ['', 'Modartha']),
               ('Partly Cloudy', ['', 'Breacscammlach']),
               ('Fair', ['',  'Aimsir Bhreá']),
               ('Fog', ['', 'Ceo']),
               ('Showers', ['', 'Ceathanna']),
               ('Rain', ['', 'Báisteach']),
               ('Light Rain', ['', 'Báisteach Éadrom']),
               ('Light Drizzle', ['', 'Ceobhrán Éadrom']),
               ('Light Rain/Windy', ['', 'Báisteach Éadrom agus Gaofar']),
               ('Light Rain with Thunder', ['', 'Báisteach Éadrom agus Stoirm Thoirní']),
               ('Heavy Rain', ['', 'Báisteach Trom']),
               ('Thunderstorms', ['',  'Stoirm Thoirní'] ),
               ('Sunny', ['', 'Grianmhar'])])

# If weather description is in the dictionary above, get the symbol and display
# the Irish name. If not, leave out the symbol and use the English description.
try:
    symbol = symbols[w['@text']][0]
    text = symbols[w['@text']][1]
except KeyError:
    symbol = ''
    text = w['@text']

print(symbol + w['@text']  + ' ' + w['@temp'] + '°C')
#print(w['@text']  + ' ' + w['@temp'] + '°C')
