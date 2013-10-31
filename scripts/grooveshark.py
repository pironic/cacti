#!/usr/bin/python
import urllib, urllib2, httplib
import sys, getopt
import re
import hashlib
from urllib2 import Request, HTTPError, URLError
from StringIO import StringIO
import gzip

DEBUG = False
SAVE = False
url_broadcast = 'http://html5.grooveshark.com/!#/writhem/broadcast'
url_app = 'http://html5.grooveshark.com/build/app.min.js'
url_api = 'https://html5.grooveshark.com/more.php'
url_scrapper = 'http://nasbox.writhem.com/monitor/grooveshark.php'
clientRevision = "20120830"
sessionID = 'notarealsessionidorsecret'
secretKey = 'efb0554935f4f1899378697f9fe90a29'
token = '525e2236b300b'
userID = 21133592
broadcastID = 'xxx'

items=dict()
md5 = hashlib.md5()

opts, args = getopt.getopt(sys.argv[1:], "d:u:b:s:", ["debug=", "userID="])
for o, v in opts:
    if o in ("-d", "--debug"):
        DEBUG = True
    if o in ("-s"):
        SAVE = True
    if o in ("-u", "--userID"):
        userID = v
    if o in ("-b") and len(v) > 5:
        broadcastID = v
if url_app == None:
    raise ValueError("bad user name, indicate user with -u <name> or --user=<name>")

# get the version number from the javascript
request = urllib2.Request(url_app)
if DEBUG:
    print 'Getting revision from url_app:',url_app
request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
request.add_header('Content-Type','application/json')
request.add_header('Accept','*/*')

try:
    response = urllib2.urlopen(request)
    data = response.read()
    
    ## capture the revision.
    regex = re.compile(r'clientRevision:"(\d+)"')
    m = regex.search(data)
    if m:
        clientRevision = m.group(1)
        if DEBUG:
            print '- DEBUG clientRevision:',clientRevision
  
                                
except HTTPError, e:
    if DEBUG:
        print '! ERROR CODE:', e.code
        #print '! ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if DEBUG:
        print '! ERROR REASON:', e.reason
    sys.exit()

# get the sessionID and generate a secretKey
request = urllib2.Request(url_broadcast)
if DEBUG:
    print 'Getting session/secretKey from url_broadcast:',url_broadcast
request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
request.add_header('Content-Type','application/json')
request.add_header('Accept','*/*')

try:
    response = urllib2.urlopen(request)
    data = response.read()
    
    ## capture the revision.
    regex = re.compile(r'sessionID":"((?:\d|[a-z])+)"')
    m = regex.search(data)
    if m:
        sessionID = m.group(1)
        md5.update(sessionID)
        secretKey = md5.hexdigest()
        if DEBUG:
            print '- DEBUG SessionID:',sessionID
            print '- DEBUG secretKey:',secretKey
                                
except HTTPError, e:
    if DEBUG:
        print '! ERROR CODE:', e.code
        #print '! ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if DEBUG:
        print '! ERROR REASON:', e.reason
    sys.exit()
    
# get the token from the id/key
request = urllib2.Request(url_api + '?getCommunicationToken')
if DEBUG:
    print 'Getting token from url_api:',url_api + '?getCommunicationToken'
request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
request.add_header('Accept','application/json')
request.add_header('Accept-Encoding','gzip,deflate')
request.add_header('Content-Type','text/plain')
request.add_header('Cookie','PHPSESSID='+sessionID)
request.add_header('Origin','http://html5.grooveshark.com')

payload = '{"header":{"client":"mobileshark","clientRevision":"20120830","privacy":0,"country":{"ID":38,"CC1":137438953472,"CC2":0,"CC3":0,"CC4":0,"DMA":0,"IPR":0},"uuid":"0EF49B00-DD49-4D01-9640-WRITHEMRADIO","session":"'+sessionID+'"},"method":"getCommunicationToken","parameters":{"secretKey":"'+secretKey+'"}}'
if DEBUG:
    print '- DEBUG payload:',payload
request.add_data(payload)

try:
    response = urllib2.urlopen(request)
    
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        # if DEBUG:
            # print '- DEBUG gzip enabled'
    else:
        data = response.read()
    
    #print 'DEBUG CommsData:',data
    
    ## capture the revision.
    regex = re.compile(r'result":"((?:\d|[a-z])+)"')
    m = regex.search(data)
    if m:
        token = m.group(1)
        if DEBUG:
            print '- DEBUG token:',token
                                
except HTTPError, e:
    if DEBUG:
        print '! ERROR CODE:', e.code
        #print '! ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if DEBUG:
        print '! ERROR REASON:', e.reason
    sys.exit()
    
#get broadcast stats
request = urllib2.Request(url_api + '?getUsersActiveBroadcast')
if DEBUG:
    print 'Getting broadcast data from url_api:',url_api + '?getUsersActiveBroadcast'
request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
request.add_header('Content-Type','application/json')
request.add_header('Cookie','ismobile=no;PHPSESSID='+sessionID)

payload = '{"header":{"client":"mobileshark","clientRevision":"'+clientRevision+'","privacy":0,"country":{"ID":38,"CC1":137438953472,"CC2":0,"CC3":0,"CC4":0,"DMA":0,"IPR":0},"uuid":"0EF49B00-DD49-4D01-9640-WRITHEMRADIO","session":"'+sessionID+'","token":"'+token+'"},"method":"getUsersActiveBroadcast","parameters":{"userID":'+userID+'}}'
request.add_data(payload)

if DEBUG:
    print '- DEBUG payload:', payload

try:
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        # if DEBUG:
            # print '- DEBUG gzip enabled'
    else:
        data = response.read()
    
    if DEBUG:
        print '- DEBUG code:',response.code
        print '- DEBUG data:',data
        
    ## make sure its valid return
    regex = re.compile(r'"result":(false)')
    m = regex.search(data)
    if m:
        #get broadcast stats
        request = urllib2.Request(url_api + '?broadcastStatusPoll')
        if DEBUG:
            print 'Getting broadcast data from url_api:',url_api + '?getUsersActiveBroadcast'
        request.add_header('User-agent','Cacti-Python AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')
        request.add_header('Content-Type','application/json')
        request.add_header('Cookie','ismobile=no;PHPSESSID='+sessionID)

        payload = '{"header":{"client":"mobileshark","clientRevision":"'+clientRevision+'","privacy":0,"country":{"ID":38,"CC1":137438953472,"CC2":0,"CC3":0,"CC4":0,"DMA":0,"IPR":0},"uuid":"0EF49B00-DD49-4D01-9640-WRITHEMRADIO","session":"'+sessionID+'","token":"'+token+'"},"method":"broadcastStatusPoll","parameters":{"broadcastID":"'+broadcastID+'"}}'
        request.add_data(payload)

        if DEBUG:
            print '- DEBUG payload:', payload

        try:
            response = urllib2.urlopen(request)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO( response.read())
                f = gzip.GzipFile(fileobj=buf)
                data = f.read()
                # if DEBUG:
                    # print '- DEBUG gzip enabled'
            else:
                data = response.read()
            
            if DEBUG:
                print '- DEBUG code:',response.code
                print '- DEBUG data:',data
        except HTTPError, e:
            if DEBUG:
                print '! ERROR CODE:', e.code
                #print '! ERROR DATA:', e.read()
            sys.exit()
        except URLError, e:
            if DEBUG:
                print '! ERROR REASON:', e.reason
            sys.exit()

    ## capture stuff
    regex = re.compile(r'"listenersCount":"(\d+)"')
    m = regex.search(data)
    if m:
        items.update({'listenerCount':m.group(1)})
        if DEBUG: 
            print '- DEBUG listenerCount:',m.group(1)

    ## capture stuff
    regex = re.compile(r'"IsPlaying":"(\d)"')
    m = regex.search(data)
    if m:
        items.update({'isPlaying':m.group(1)})        
        
except HTTPError, e:
    if DEBUG:
        print '! ERROR CODE:', e.code
        #print '! ERROR DATA:', e.read()
    sys.exit()
except URLError, e:
    if DEBUG:
        print '! ERROR REASON:', e.reason
    sys.exit()
    
#save details to scrapper api
if SAVE:
    md5 = hashlib.md5()
    md5.update(userID)
    request = urllib2.Request(url_scrapper + '?key='+md5.hexdigest() + '&bcID=' + broadcastID)
    if DEBUG:
        print 'Saving broadcast data to url_scrapper:',url_scrapper + '?key='+md5.hexdigest()
    request.add_data(data)
    try:
        response = urllib2.urlopen(request)
        if DEBUG:
            print '- DEBUG lastresponse:',response.read()
        
    except HTTPError, e:
        if DEBUG:
            print '! ERROR CODE:', e.code
            #print '! ERROR DATA:', e.read()
    except URLError, e:
        if DEBUG:
            print '! ERROR REASON:', e.reason

  
outstr = u''  
for k, v in sorted(items.items()):
    outstr = outstr + u'{0}:{1} '.format(k, v)
print outstr
