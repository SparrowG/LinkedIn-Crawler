#! /usr/bin/python
 
#class to make google queries
#must masquerade as a legitimate browser
#Using this violates Google ToS
 
import httplib
import urllib
import sys
import HTMLParser
import re
 
#class is basically fed a google url for linkedin for the
#sole purpose of getting a linkedin link
class GoogleQueery(HTMLParser.HTMLParser):
  def __init__(self, goog_url):
    HTMLParser.HTMLParser.__init__(self)
    self.linkedinurl = []
    query = urllib.urlencode({"q": goog_url})
    conn = httplib.HTTPConnection("www.google.com")
    headers = self.getHeaders()
    conn.request("GET", "/search?hl=en&"+query, headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    self.feed(data)
    self.get_num_results(data)
    conn.close()
 
  #this is necessary because google wants to be mean and 403 based on... not sure
  #but it seems  I must look like a real browser to get a 200
  def getHeaders(self, browser="chromium"):
    #if browser == "random":
      #TODO randomize choice
    #ubuntu firefox spoof
    if browser == "ubuntuFF":
      headers = {
        "Host": "www.google.com",
        "User-Agent": "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language" : "en-us,en;q=0.5",
        "Accept-Charset" : "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Keep-Alive" : "300",
        "Proxy-Connection" : "keep-alive"
        }
    elif browser == "chromium":
      headers = {
        "Host": "www.google.com",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.5 Safari/533.2",
        "Referer": "http://www.google.com/",
        "Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
        "Avail-Dictionary": "FcpNLYBN",
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
      }
    elif browser == "ie":
      headers = {
        "Host": "www.google.com",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
        "Referer": "http://www.google.com/",
        "Accept": "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
      }
    return headers
 
  def get_num_results(self, data):
    index = re.search("<b>1<\/b> - <b>[\d]+<\/b> of [\w]*[ ]?<b>([\d,]+)", data)
    try:
      self.numResults = int(index.group(1).replace(",", ""))
    except:
      self.numResults = 0
      if not "- did not match any documents. " in data:
        print "Warning: numresults parsing problem"
        print "setting number of results to 0"
 
  def handle_starttag(self, tag, attrs):
    try:
      if tag == "a" and ((("linkedin.com/pub/" in attrs[0][1])
                    or  ("linkedin.com/in" in attrs[0][1]))
                    and ("http://" in attrs[0][1])
                    and ("search?q=cache" not in attrs[0][1])
                    and ("/dir/" not in attrs[0][1])):
        self.linkedinurl.append(attrs[0][1])
        #print self.linkedinurl
      #perhaps add a google cache option here in the future
    except IndexError:
      pass
 
#for testing
if __name__ == "__main__":
  #url = "site:linkedin.com \"PROJECT ADMINISTRATOR at CAT INL QATAR W.L.L.\" \"Qatar\""
  m = GoogleQueery(url)

