print "and we begin"

import requests
from bs4 import BeautifulSoup
#import urllib
#print page.read()
#page = urllib.urlopen("http://25livepub.collegenet.com/calendars/events_all.xml")
r = requests.get("http://25livepub.collegenet.com/calendars/events_all.xml")
soup = BeautifulSoup(r.content, "xml")
print soup.prettify()
#soup.find_all("entry")
