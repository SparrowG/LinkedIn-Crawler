#! /usr/bin/python
 
#this should probably be put in LinkedinPageGatherer.py
 
import HTMLParser
 
from person_searchobj import person_searchobj
 
class LinkedinHTMLParser(HTMLParser.HTMLParser):
  """
  subclass of HTMLParser specifically for parsing Linkedin names to person_searchobjs
  requires a call to .feed(data), stored data in the personArray
  """
  def __init__(self):
    HTMLParser.HTMLParser.__init__(self)
    self.personArray = []
    self.personIndex = -1
    self.inGivenName = False
    self.inFamilyName = False
    self.inTitle = False
    self.inLocation = False
 
  def handle_starttag(self, tag, attrs):
    try:
      if tag == "li" and attrs[0][0] == "class" and ("vcard" in attrs[0][1]):
        self.personIndex += 1
        self.personArray.append(person_searchobj())
      if attrs[0][1] == "given-name" and self.personIndex >=0:
        self.inGivenName = True
      elif attrs[0][1] == "family-name" and self.personIndex >= 0:
        self.inFamilyName = True
      elif tag == "dd" and attrs[0][1] == "title" and self.personIndex >= 0:
        self.inTitle = True
      elif tag == "span" and attrs[0][1] == "location" and self.personIndex >= 0:
        self.inLocation = True
    except IndexError:
      pass
 
  def handle_endtag(self, tag):
    if tag == "span":
      self.inGivenName = False
      self.inFamilyName = False
      self.inLocation = False
    elif tag == "dd":
      self.inTitle = False
 
  def handle_data(self, data):
    if self.inGivenName:
      self.personArray[self.personIndex].givenName = data.strip()
    elif self.inFamilyName:
      self.personArray[self.personIndex].familyName = data.strip()
    elif self.inTitle:
      self.personArray[self.personIndex].title = data.strip()
    elif self.inLocation:
      self.personArray[self.personIndex].location = data.strip()
 
#for testing - use a file since this is just a parser
if __name__ == "__main__":
  import sys
  file = open ("test.htm")
  df = file.read()
  parser = LinkedinHTMLParser()
  parser.feed(df)
  print "================"
  for person in parser.personArray:
    print person.goog_printstring()
  file.close()
