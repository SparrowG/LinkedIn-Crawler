#! /usr/bin/python
 
class person_searchobj():
  """this object is used for the google search and the final person object"""
 
  def __init__ (self, givenname="", familyname="", title="", organization="", location=""):
    """
    given name could be a title in this case, does not matter in terms of google
    but then may have to change for the final person object
    """
    #"name" is their actual name, unlike givenName and family name which are linkedin names
    self.name = ""
    self.givenName = givenname
    self.familyName = familyname
    self.title = title
    self.organization = organization
    self.location = location
 
    #this is retrieved by GoogleQueery
    self.url = ""
 
  def goog_printstring(self):
    """return the google print string used for queries"""
    retrstr = "site:linkedin.com "
    for i in  [self.givenName, self.familyName, self.title, self.organization, self.location]:
      if i != "":
        retrstr += '"' + i +'" '
    return retrstr
 
  def __repr__(self):
    """Overload __repr__ for easy printing. Mostly for debugging"""
    return (self.name + "\n" +
            "------\n"
            "GivenName: " + self.givenName + "\n" +
            "familyName:" + self.familyName + "\n" +
            "Title:" + self.title + "\n" +
            "Organization:" + self.organization + "\n" +
            "Location" + self.location + "\n" +
            "URL:" + self.url + "\n\n")

