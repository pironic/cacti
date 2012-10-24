#!/usr/bin/python
import urllib, urllib2, httplib, sys, getopt, re from urllib2 import Request, HTTPError, URLError import xml.etree.ElementTree as ET DEBUG = False opts, args 
= getopt.getopt(sys.argv[1:], "u:d:", ["usr=", "debug="]) url = None for o, v in opts:
    if o in ("-u", "--user"):
        url = 'http://raptr.com/' + str(v) + '/about'
    elif o in ("-d", "--debug"):
        DEBUG = True if url == None:
    raise Exception("bad user name, indicate user with -u <name> or --user=<name>")
    
request = urllib2.Request(url) request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1') try:
    response = urllib2.urlopen(request)
    data = response.read()
    
    items=dict()
    
    ## capture the game count.
    regex = re.compile(r'\\/games\\">(.*) games<\\/a>')
    m = regex.search(data)
    if m:
        items.update({'games':int(m.group(1).replace(",",""))})
        
    ## capture the game hours.
    regex = re.compile(r'\\/games\\">.*\\/games\\">(.*) hours tracked<\\/a>')
    m = regex.search(data)
    if m:
        items.update({'hours':int(m.group(1).replace(",",""))})
        
    ## capture the achievements.
    regex = re.compile(r'\\/achievements\\">(.*) achievements<\\/a>')
    m = regex.search(data)
    if m:
        items.update({'achievements':int(m.group(1).replace(",",""))})
        
except HTTPError, e:
    if (DEBUG):
        print 'ERROR CODE:', e.code
        #print 'ERROR DATA:', e.read()
    sys.exit() except URLError, e:
    if (DEBUG):
        print 'ERROR REASON:', e.reason
    sys.exit()
  
outstr = u'' for k, v in sorted(items.items()):
    outstr = outstr + u'{0}:{1} '.format(k, v)
print outstr
