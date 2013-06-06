#!/usr/bin/python
import urllib, urllib2, httplib, sys, getopt
from urllib2 import Request, HTTPError, URLError
import xml.etree.ElementTree as ET

DEBUG = False

opts, args = getopt.getopt(sys.argv[1:], "x:d:", ["xml=", "debug="])
url = 'http://nasbox.writhem.com/monitor/varnishstat.xml.php'
for o, v in opts:
    if o in ("-x", "--xml"):
        url = str(v)
    elif o in ("-d", "--debug"):
        DEBUG = True

request = urllib2.Request(url)
request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
try:
    response = urllib2.urlopen(request)
    root = ET.fromstring(response.read())
except HTTPError, e:
    if (DEBUG):
        print 'ERROR CODE:', e.code
        print 'ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if (DEBUG):
        print 'ERROR REASON:', e.reason
    sys.exit()
  
req = 0
hit = 0
miss = 0
# for stat in root:
for r in range(0, len(root)):
    for n in range(0, len(root[0])):
        if (root[r][n].tag == 'name'):
            name = root[r][n].text
        elif (root[r][n].tag == 'value'):
            value = root[r][n].text
    if (name == 'client_req'):
        req = int(value)
    if (name == 'cache_hitpass'):
        hit = int(value)
    if (name == 'cache_miss'):
        miss = int(value)
     
try: # divide by your mom errors... check for it.
    hitrate = round(hit / (hit + miss) * 100, 1)
except ZeroDivisionError, e:
    if (DEBUG):
        print 'MATH ERROR:', e
    hitrate = 0

outstr = 'varnish_requests:%s varnish_hitrate:%s varnish_hits:%.0f varnish_misses:%.0f' % (str(req), str(hitrate), hit, miss)
print outstr