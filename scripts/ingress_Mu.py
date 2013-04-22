#!/usr/bin/python
import sys, getopt
import urllib2
import simplejson as json
import pprint

DEBUG = False
url = None

opts, args = getopt.getopt(sys.argv[1:], "k:d:", ["key=", "debug="])
for o, v in opts:
    if o in ("-k", "--key"):
        url = 'http://ingress.writhem.com/api/?key=' + str(v) + '&table=view_mu'
    elif o in ("-d", "--debug"):
        DEBUG = True
if url == None:
    raise ValueError("bad api key, indicate user with -k <value> or --key=<value>")
if DEBUG:
    print 'url is set to: %s' % (url)
    
req = urllib2.Request(url, None, {'user-agent':'Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'})

opener = urllib2.build_opener()
f = opener.open(req)
content = f.read()
j = json.loads(content)

outstr = ''  
for k in range(0, 2):
    
    # outstr = outstr + '{0}:{1} '.format('id', j[k]['guid'])
    # outstr = outstr + '{0}:{1} '.format('name', j[k]['name'])
    outstr = outstr + '{0}:{1} '.format(j[k]['name'] + '-capturedMU', j[k]['capturedMU'])
    outstr = outstr + '{0}:{1} '.format(j[k]['name'] + '-liberatedMU', j[k]['liberatedMU'])
    outstr = outstr + '{0}:{1} '.format(j[k]['name'] + '-currentMU', j[k]['currentMU'])
print outstr