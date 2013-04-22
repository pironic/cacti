#!/usr/bin/python
import urllib, urllib2, httplib, sys, getopt
from xml.dom.minidom import parse, parseString

DEBUG = False

opts, args = getopt.getopt(sys.argv[1:], "x:m:u:p:", ["xml=", "mount=", "user=", "password="])
xml = 'http://radio.overviewer.org/admin/stats.xml'
mount = '/writhem.mp3'
user = 'admin'
password = 'poop'

listeners = 0
for o, v in opts:
  if o in ("-x", "--xml"):
    xml = str(v)
  elif o in ("-m", "--mount"):
    mount = str(v)
  elif o in ("-u", "--user"):
    user = str(v)
  elif o in ("-p", "--password"):
    password = str(v)

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, xml, user, password)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
try:
  file_obj = opener.open(xml)
  dom = parseString(file_obj.read())
  for element in dom.getElementsByTagName('icestats'):
    source = element.getElementsByTagName('source')
    for n in range(1, len(source)):
      if (source[n].getAttribute('mount') == mount):
       listeners = source[n].getElementsByTagName('listeners')[0].firstChild.data
except IOError, e:
  listeners =  "Error: %s" % e
        
if (listeners == 1):
  strCurrentListeners = "1 Current Listener"
else:
  strCurrentListeners = "%s Current Listeners" % str(listeners)

outstr = 'current_listeners:%s' % str(listeners)
print outstr
if DEBUG:
  import syslog
  outstr += "(%s)" % file_obj
  syslog.syslog(outstr)

