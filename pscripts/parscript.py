print "and we begin"

import requests
from bs4.diagnose import diagnose
from bs4 import BeautifulSoup

#r = requests.get("http://25livepub.collegenet.com/calendars/events_all.xml")
f = open("events.xml", "r")

soup = BeautifulSoup(f.read(), "lxml")
entries = soup.find_all('entry')
print type(entries[0]), "\n"
print entries[0].prettify(), "\n"
print entries[0].find('content').prettify(), "\n"

titles = []
for item in entries:
    ladle = BeautifulSoup(unicode(item.string), "lxml")
    titles = ladle.find_all('title')

print titles
