#!/usr/bin/python
import urllib, urllib2, httplib, sys, getopt, json
from urllib2 import Request, HTTPError, URLError

DEBUG = False

opts, args = getopt.getopt(sys.argv[1:], "a:u:p:", ["api=", "user=", "password="])
api = 'http://nasbox.writhem.com/power/api.php'
user = 'admin'
password = 'poop'

for o, v in opts:
  if o in ("-x", "--api"):
    api = str(v)
  elif o in ("-u", "--user"):
    user = str(v)
  elif o in ("-p", "--password"):
    password = str(v)

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, api, user, password)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
try:
  response = opener.open(api)
  if (DEBUG):
    print response
except HTTPError, e:
    if (DEBUG):
        print 'ERROR CODE:', e.code
        print 'ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if (DEBUG):
        print 'ERROR REASON:', e.reason
    sys.exit()
    
current = 0.0;
temp = 0.0;
outlet1 = -1;
outlet2 = -1;
outlet3 = -1;
outlet4 = -1;
outlet5 = -1;
outlet6 = -1;
outlet7 = -1;
outlet8 = -1;

try:    
    data = json.loads(response.read())
    for k in data:
    
        try:
            current = k['Current']
        except: 
            current = current
            
        try:
            temp = k['Temp']
        except: 
            temp = temp
            
        try:
            for l in k['Outlets']:
                if l['ID'] == '1':
                    if l['Status'] == "Off":
                        outlet1 = 0
                    else:
                        outlet1 = 1
                if l['ID'] == '2':
                    if l['Status'] == 'Off':
                        outlet2 = 0
                    else:
                        outlet2 = 1
                if l['ID'] == '3':
                    if l['Status'] == 'Off':
                        outlet3 = 0
                    else:
                        outlet3 = 1
                if l['ID'] == '4':
                    if l['Status'] == 'Off':
                        outlet4 = 0
                    else:
                        outlet4 = 1
                if l['ID'] == '5':
                    if l['Status'] == 'Off':
                        outlet5 = 0
                    else:
                        outlet5 = 1
                if l['ID'] == '6':
                    if l['Status'] == 'Off':
                        outlet6 = 0
                    else:
                        outlet6 = 1
                if l['ID'] == '7':
                    if l['Status'] == 'Off':
                        outlet7 = 0
                    else:
                        outlet7 = 1
                if l['ID'] == '8':
                    if l['Status'] == 'Off':
                        outlet8 = 0
                    else:
                        outlet8 = 1
        except: 
            outlet1 = outlet1
        
    print 'current:%s temp:%s outlet1:%s outlet2:%s outlet3:%s outlet4:%s outlet5:%s outlet6:%s outlet7:%s outlet8:%s ' % (current, temp, outlet1, outlet2, outlet3, outlet4, outlet5, outlet6, outlet7, outlet8)
    
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
    
    
# if DEBUG:
  # import syslog
  # outstr += "(%s)" % response
  # syslog.syslog(outstr)

