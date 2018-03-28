#!/usr/bin/python3 -B

import sys
sys.dont_write_bytecode=True
from weatherIndicator import weatherIndicator
w = weatherIndicator()

f = open('/home/christoph/.cache/weather-in-bar.txt', 'w')
f.write(w.weatherInBar())
f.close()

f = open('/home/christoph/.cache/weather-notification.txt', 'w')
f.write(w.weatherNotification())
f.close()

f = open('/home/christoph/Drive/www/homepage/weather.js', 'w')
f.write(w.weatherForHomepage())
f.close()

f = open('/home/christoph/.cache/weather-conky.txt', 'w')
f.write(w.weatherForConky())
f.close()
