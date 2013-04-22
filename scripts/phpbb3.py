#!/usr/bin/python
import urllib, urllib2, httplib
import sys, getopt
import re
from urllib2 import Request, HTTPError, URLError

DEBUG = False
url = None

opts, args = getopt.getopt(sys.argv[1:], "u:d:", ["url=", "debug="])
for o, v in opts:
    if o in ("-u", "--url"):
        url = str(v) + "/viewonline.php?sg=1"
    elif o in ("-d", "--debug"):
        DEBUG = True
if url == None:
    raise ValueError("bad url; indicate the forum url with -u <name> or --user=<name>")

request = urllib2.Request(url)
request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
try:
    response = urllib2.urlopen(request)
    data = response.read()
    
    if DEBUG:
       print "OUTPUT:",data
    items=dict()

    ## capture the online counts.
    regex = re.compile(r'<h2>There (?:are|is) (\d) registered user(?:|s) and (\d) hidden user(?:|s) online</h2>[.\r\n]*<p>There (?:are|is) (\d+) guest user(?:|s) online')
    m = regex.search(data)
    if m:
        count_registered = int(m.group(1).replace(",",""))
        items.update({'registered':count_registered})
        items.update({'hidden':int(m.group(2).replace(",",""))})
        items.update({'guests':int(m.group(3).replace(",",""))})
		
    ## modify the online counts with bot data.
    count_bots = 0
    color_bots = '9E8DA7'
    regex = re.compile(r'(?:style="color:(?:| )#(#?[0-9A-Fa-f]{6})(?:;|)" class="username-coloured">|<td>(Guest)</td>)')
    for m in regex.finditer(data):
        # print str(m.group(1))
        if str(m.group(1)) == color_bots:
            count_bots += 1
            count_registered += -1
    items.update({'bots':count_bots})
    items.update({'registered':count_registered})

    ## capture the total counts.
    regex = re.compile(r'Total members <strong>(\d+)</strong> Total posts <strong>(\d+)</strong> Total topics <strong>(\d+)</strong>')
    m = regex.search(data)
    if m:
        items.update({'members':int(m.group(1).replace(",",""))})
        items.update({'posts':int(m.group(2).replace(",",""))})
        items.update({'topics':int(m.group(3).replace(",",""))})
        
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
