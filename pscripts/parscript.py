print "and we begin"

import requests
from bs4.diagnose import diagnose
from bs4 import BeautifulSoup

r = requests.get("http://25livepub.collegenet.com/calendars/events_all.xml")
soup = BeautifulSoup(r.content, "lxml")
entries = soup.find_all('entry')
tempent = entries
print type(entries[0])
for entry in entries:
    ladle = BeautifulSoup(entry.toString(), "lxml")
    entries.extend(ladle.find_all('title'))
