#!/usr/bin/python
import urllib, urllib2, httplib
import sys, getopt
import re
from urllib2 import Request, HTTPError, URLError

DEBUG = False
url_current = 'http://wx.ca/'
url_almanac = 'http://weather.gc.ca/almanac/almanac_e.html?id=yyc'
items=dict()

opts, args = getopt.getopt(sys.argv[1:], "d:", ["debug="])
for o, v in opts:
    if o in ("-d", "--debug"):
        DEBUG = True
if url_current == None:
    raise ValueError("bad user name, indicate user with -u <name> or --user=<name>")

request = urllib2.Request(url_current)
request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
try:
    response = urllib2.urlopen(request)
    data = response.read()

    ## capture the temperature.
    regex = re.compile(r'Temperature<\/td>[^"]*class="value"(?:>| colspan="2">)((?:\d|\.){1,4})<\/td>')
    m = regex.search(data)
    if m:
        items.update({'Temperature':float(m.group(1).replace(",",""))})
        
    ## capture the wind.
    regex = re.compile(r'Wind<\/td>[^"]*class="value">((?:.|\.){2,3})<\/td>[^\d]*(\d)*<\/td>[^\d]*(\d)*<\/td>')
    m = regex.search(data)
    if m:
        WindDirections = {'N':1,
            'NNE':1.5,
            'NE':2,
            'ENE':2.5,
            'E':3,
            'ESE':3.5,
            'SE':4,
            'SSE':4.5,
            'S':5,
            'SSW':5.5,
            'SW':6,
            'WSW':6.5,
            'W':7,
            'WNW':7.5,
            'NW':8,
            'NNW':8.5,
            'N':9}
        items.update({'WindDirection':float(WindDirections[m.group(1).replace(",","")])})
        items.update({'WindSpeedLow':float(m.group(2).replace(",",""))})
        items.update({'WindSpeedHigh':float(m.group(3).replace(",",""))})
        items.update({'WindSpeedAvg':((float(m.group(3).replace(",","")) + float(m.group(2).replace(",",""))) / 2)})
        
    ## capture the baro pressure.
    regex = re.compile(r'Pressure<\/td>[^"]*class="value"(?:>| colspan="2">)((?:\d|\.){2,5})<\/td>')
    m = regex.search(data)
    if m:
        items.update({'BaroPressure':float(m.group(1).replace(",",""))})
        
    ## capture the precipitation.
    regex = re.compile(r'Precipitation<\/td>[^"]*class="value"(?:>| colspan="2">)((?:\d|\.){2,5})<\/td>')
    m = regex.search(data)
    if m:
        items.update({'Precipitation':float(m.group(1).replace(",",""))})
        
    ## capture the lightning strike count.
    regex = re.compile(r'Lightning<\/td>[^"]*class="value"(?:>| colspan="2">)((?:\d|\.){1,4})<\/td>')
    m = regex.search(data)
    if m:
        items.update({'Lightning':float(m.group(1).replace(",",""))})
        
                
except HTTPError, e:
    if DEBUG:
        print 'ERROR CODE:', e.code
        #print 'ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if DEBUG:
        print 'ERROR REASON:', e.reason
    sys.exit()
  
request = urllib2.Request(url_almanac)
request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
try:
    response = urllib2.urlopen(request)
    data = response.read()

    ## capture the avg_max_temp.
    regex = re.compile(r'Average Maximum Temperature[^\d]*((?:\d|\.|-){1,4})')
    m = regex.search(data)
    if m:
        items.update({'hist_avg_max_temp':float(m.group(1).replace(",",""))})
        
    ## capture the max_temp.
    regex = re.compile(r'Highest Temperature [^>]*[^\d]*((?:\d|\.|-){1,4})')
    m = regex.search(data)
    if m:
        items.update({'hist_max_temp':float(m.group(1).replace(",",""))})
        
    ## capture the avg_min_temp.
    regex = re.compile(r'Average Minimum Temperature[^\d]*((?:\d|\.|-){1,4})')
    m = regex.search(data)
    if m:
        items.update({'hist_avg_min_temp':float(m.group(1).replace(",",""))})
        
    ## capture the min_temp.
    regex = re.compile(r'Lowest Temperature [^>]*[^\d]*"(?:header\d| )*">((?:\d|\.|-){1,6})')
    m = regex.search(data)
    if m:
        items.update({'hist_min_temp':float(m.group(1).replace(",",""))})
        
    ## capture the hist_freq_precip.
    regex = re.compile(r'Frequency of Precipitation[^\d]*((?:\d|\.|-){1,4})')
    m = regex.search(data)
    if m:
        items.update({'hist_freq_precip':float(m.group(1).replace(",",""))})
        
    ## capture the max_precip.
    regex = re.compile(r'Greatest Precipitation [^>]*[^\d]*"(?:header\d{1,2}| )*">((?:\d|\.|-){1,6})')
    m = regex.search(data)
    if m:
        items.update({'hist_max_precip':float(m.group(1).replace(",",""))})
        
    ## capture the max_rain.
    regex = re.compile(r'Greatest Rainfall [^>]*[^\d]*"(?:header\d{1,2}| )*">((?:\d|\.|-){1,6})')
    m = regex.search(data)
    if m:
        items.update({'hist_max_rain':float(m.group(1).replace(",",""))})
        
    ## capture the max_snowfall.
    regex = re.compile(r'Greatest Snowfall [^>]*[^\d]*"(?:header\d{1,2}| )*">((?:\d|\.|-){1,6})')
    m = regex.search(data)
    if m:
        items.update({'hist_max_snowfall':float(m.group(1).replace(",",""))})
        
    ## capture the max_snowfall.
    regex = re.compile(r'Most Snow on the Ground [^>]*[^\d]*"(?:header\d{1,2}| )*">((?:\d|\.|-){1,6})')
    m = regex.search(data)
    if m:
        items.update({'hist_max_snowOnGround':float(m.group(1).replace(",",""))})
        
                
except HTTPError, e:
    if DEBUG:
        print 'ERROR CODE:', e.code
        #print 'ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if DEBUG:
        print 'ERROR REASON:', e.reason
    sys.exit()
  
outstr = u''  
for k, v in sorted(items.items()):
    outstr = outstr + u'{0}:{1} '.format(k, v)
print outstr
