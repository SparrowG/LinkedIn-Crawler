import urllib
import urllib2
import sys

from LinkedinPageGatherer import *

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)
gsoc_url="http://www.google-melange.com/gsoc/projects/list/google/gsoc2011"
req = urllib2.Request(gsoc_url)
fd=opener.open(req)
pagedata=fd.read()
fd.close()
    
with open("list", "w") as fd:
    fd.write(pagedata)

