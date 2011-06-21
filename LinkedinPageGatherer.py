#!/usr/bin/python
 
import urllib
import urllib2
import sys
import time
import copy
import pickle
import math
 
from person_searchobj import person_searchobj
from LinkedinHTMLParser import LinkedinHTMLParser
from GoogleQueery import GoogleQueery
 
#TODO add a test function that tests the website format for easy diagnostics when HTML changes
#TODO use HTMLParser like a sane person
class LinkedinPageGatherer:
  """
  class that generates the initial linkeding queeries using the company name
  as a search parameter. These search strings will be searched using google
  to obtain additional information (these limited initial search strings usually lack
  vital info like names)
  """
  def __init__(self, login, password, maxsearch=100,
               totalresultpercent=.7, maxskunk=100,**kwargs):
    """
    login and password are params for a valid linkedin account
    maxsearch is the number of results - linkedin limit unpaid accounts to 100
    totalresultpercent is the number of results this script will try to find
    maxskunk is the number of searches this class will attempt before giving up
    """
    #list of person_searchobj
    query=''
    for k,v in kwargs.items():
        query+="&"+k+"="+v
    self.people_searchobj = []
    self.login = login
    self.password = password
    self.fullurl = ("http://www.linkedin.com/search?search="+query, "&page_num=", "1")
    self.opener = self.linkedin_login()
    #for the smart_people_adder
    self.searchSpecific = []
    #can only look at 100 people at a time. Parameters used to narrow down queries
    self.total_results = self.get_num_results()
    self.maxsearch = maxsearch
    self.totalresultpercent = totalresultpercent
    #self.extraparameters = {"locationinfo" : [], "titleinfo" : [], "locationtitle" : [] }
    #extraparameters is a simple stack that adds keywords to restrict the search
    self.extraparameters = []
    #TODO can only look at 100 people at a time - like to narrow down queries
    #and auto grab more
    currrespercent = 0.0
    skunked = 0
    currurl = self.fullurl[0] + self.fullurl[1]
    extraparamindex = 0
    

 
    while currrespercent < self.totalresultpercent and skunked <= maxskunk:
      numresults = self.get_num_results(currurl)
      save_num = len(self.people_searchobj)
 
      print "-------"
      print "currurl", currurl
      print "percentage", currrespercent
      print "skunked", skunked
      print "numresults", numresults
      print "save_num", save_num
     
      if self.total_results == 0:
        print "No matches found" 
        return
      for i in range (1, int(min(math.ceil(self.maxsearch/10), math.ceil(numresults/10)))+1):
        #function adds to self.people_searchobj
        print "currurl" + currurl + str(i)
        self.return_people_links(currurl + str(i))
      currrespercent = float(len(self.people_searchobj))/self.total_results
      if save_num == len(self.people_searchobj):
        skunked += 1
      for i in self.people_searchobj:
        pushTitles = [("title", gName) for gName in i.givenName.split()]
        #TODO this could be inproved for more detailed results, etc, but keeping it simple for now
        pushKeywords = [("keywords", gName) for gName in i.givenName.split()]
        pushTotal = pushTitles[:] + pushKeywords[:]
        #append to extraparameters if unique
        self.push_search_parameters(pushTotal)
      print "parameters", self.extraparameters
      #get a new url to search for, if necessary
      #use the extra params in title, "keywords" parameters
      try:
        refineel = self.extraparameters[extraparamindex]
        extraparamindex += 1
        currurl = self.fullurl[0] + "&" + refineel[0] + "=" + refineel[1] + self.fullurl[1]
      except IndexError:
        break
 
  """
  #TODO: This idea is fine, but we should get names first to better distinguish people
  #also maybe should be moved
  def smart_people_adder(self):
    #we've already done a basic search, must do more
    if "basic" in self.searchSpecific:
  """
  def return_people_links(self, linkedinurl):
    req = urllib2.Request(linkedinurl)
    fd = self.opener.open(req)
    pagedata = ""
    while 1:
      data = fd.read(2056)
      pagedata = pagedata + data
      if not len(data):
        break
    #print pagedata
    self.parse_page(pagedata)
 
  def parse_page(self, page):
    thesePeople = LinkedinHTMLParser()
    page=page.replace('<![if (!IE)|(lt IE 9)]>', '')
    page=page.replace('<![endif]>', '')
    thesePeople.feed(page)
    for newperson in thesePeople.personArray:
      unique = True
      for oldperson in self.people_searchobj:
        #if all these things match but they really are different people, they
        #will likely still be found as unique google results
        if (oldperson.givenName == newperson.givenName and
            oldperson.familyName == newperson.familyName and
            oldperson.title == newperson.title and
            oldperson.location == oldperson.location):
              unique = False
              break
      if unique:
        self.people_searchobj.append(newperson)
  """
    print "======================="
    for person in self.people_searchobj:
      print person.goog_printstring()
  """
 
  #return the number of results, very breakable
  def get_num_results(self, url=None):
    #by default return total in company
    if url is None:
      fd = self.opener.open(self.fullurl[0] )
    else:
      fd = self.opener.open(url)
    data = fd.read()
    fd.close()
    with open("out","w") as f:
        f.write(data)
    searchstr = "<p class=\"summary keywords\">"
    sindex = data.find(searchstr) + len(searchstr)
    eindex = data.find("</strong>", sindex)
    val=int((data[sindex:eindex].strip().strip("<strong>").replace(",", "").strip()))
    return(val)
 
  #returns an opener object that contains valid cookies
  def linkedin_login(self):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)
    #login page
    fd = opener.open("https://www.linkedin.com/secure/login?trk=hb_signin")
    data = fd.read()
    fd.close()
    #csrf 'prevention' login value
    searchstr = """<input type="hidden" name="csrfToken" value="ajax:"""
    sindex = data.find(searchstr) + len(searchstr)
    eindex = data.find('"', sindex)
    params = urllib.urlencode(dict(csrfToken="ajax:-"+data[sindex:eindex],
                              session_key=self.login,
                              session_password=self.password,
                              session_login="Sign+In",
                              session_rikey=""))
    #need the second request to get the csrf stuff, initial cookies
    request = urllib2.Request("https://www.linkedin.com/secure/login")
    request.add_header("Host", "www.linkedin.com")
    request.add_header("Referer", "https://www.linkedin.com/secure/login?trk=hb_signin")
    time.sleep(1.5)
    fd = opener.open(request, params)
    data = fd.read()
    if "<div id=\"header\" class=\"guest\">" in data:
      print "Linkedin authentication faild. Please supply a valid linkedin account"
      sys.exit(1)
    else:
      print "Linkedin authentication Successful"
    fd.close()
    return opener
 
  def push_search_parameters(self, extraparam):
    uselesswords = [ "for", "the", "and", "at", "in"]
    for pm in extraparam:
      pm = (pm[0], pm[1].strip().lower())
      if (pm not in self.extraparameters) and (pm[1] not in uselesswords) and pm != None:
        self.extraparameters.append(pm)
 
class LinkedinTotalPageGather(LinkedinPageGatherer):
  """
  Overhead class that generates the person_searchobjs, using GoogleQueery
  """
  def __init__(self, login, password, **kwargs):
    LinkedinPageGatherer.__init__(self, login, password, **kwargs)
    extraPeople = []
    for person in self.people_searchobj:
      mgoogqueery = GoogleQueery(person.goog_printstring())
      #making the assumption that each pub url is a unique person
      count = 0
      for url in mgoogqueery.linkedinurl:
        #grab the real name from the url
        begindex = url.find("/pub/") + 5
        endindex = url.find("/", begindex)
        if count == 0:
          person.url = url
          person.name = url[begindex:endindex]
        else:
          extraObj = copy.deepcopy(person)
          extraObj.url = url
          extraObj.name = url[begindex:endindex]
          extraPeople.append(extraObj)
        count += 1
      print person
    print "Extra People"
    for person in extraPeople:
      print person
      self.people_searchobj.append(person)
 
if __name__ == "__main__":
  #args are email and password for linkedin
  if len(sys.argv) == 3:
    pass
  my = LinkedinTotalPageGather(sys.argv[1], sys.argv[2], company='artoo')
  my
