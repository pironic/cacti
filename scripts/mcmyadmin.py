#!/usr/bin/python
# Written by Michael Writhe. Free to use, and copy/adjust. 
# Please leave my name associated with this code though.
# http://github.com/pironic 
import urllib, urllib2, httplib, sys, getopt, json
from urllib2 import Request, HTTPError, URLError


DEBUG = False 

opts, args = getopt.getopt(sys.argv[1:], "m:u:p:d:", ["mcma=", "user=", "password="])
mcma = 'http://your-mcmyadmin-instance/'
user = 'mcmyadminUser'
password = 'mcmyadminPass'

#get the arguments and save them to variables for ease of use.
listeners = 0
for o, v in opts:
  if o in ("-m", "--mcma"):
    mcma = str(v)
  elif o in ("-u", "--user"):
    user = str(v)
  elif o in ("-p", "--password"):
    password = str(v)
  elif o in ("-d", "--debug"):
    DEBUG = True

# set the url's we need.
url_login = mcma + 'data.json?Username='+user+'&Password='+password+'&req=login'
url_status = mcma + 'data.json?req=getstatus'

# set the headers and url that are required to authenticate... we needs the cookies!
request_auth = urllib2.Request(url_login)
request_auth.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
request_auth.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
request_auth.add_header('Referer',mcma)

try: # check the url and fetch the login data.
    response = urllib2.urlopen(request_auth)
except HTTPError, e:
    if (DEBUG):
        print 'ERROR CODE:', e.code
        print 'ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if (DEBUG):
        print 'ERROR REASON:', e.reason
    sys.exit()

request_status = urllib2.Request(url_status)
request_status.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
request_status.add_header('Cookie',response.info()['Set-Cookie'])
request_status.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')


try:    
    response = urllib2.urlopen(request_status)
    data = json.loads(response.read())
    print 'maxusers:%s users:%s cpuusage:%s maxram:%s ram:%s' % (data['maxusers'], data['users'], data['cpuusage'], data['maxram'], data['ram'])
    
    if (DEBUG):
        print 'RESPONSE:', response
        print 'URL     :', response.geturl()

        headers = response.info()
        print 'DATE    :', headers['date']
        print 'HEADERS :'
        print '---------'
        print headers

        data = response.read()
        print 'LENGTH  :', len(data)
        print 'DATA    :'
        print '---------'
        print data
except HTTPError, e:
    if (DEBUG):
        print 'ERROR CODE:', e.code
        print 'ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if (DEBUG):
        print 'ERROR REASON:', e.reason
    sys.exit()
       
        
#outstr = 'current_listeners:%s' % str(listeners)
#print outstr
