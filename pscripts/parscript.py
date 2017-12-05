print "and we begin"

class event:
    def __init__(self):
        self.__name = "nameplaceholder"
        self.__description = "contentplaceholder"
        self.__time = "timeplaceholder"
        self.__date = "dateplaceholder"
        self.__location = "locationplaceholder"



from bs4 import BeautifulSoup
import requests
f = requests.get("http://25livepub.collegenet.com/calendars/events_all.xml") #grabs the xml from 25live
#f = open("events.xml", "r") #Opens a local document. events.xml is a shortened version of the larger events doc
soup = BeautifulSoup(f.text, "lxml") #creates soup of the xml



entries = soup.find_all('entry') #creates a list of all the entry tags from the xml
print type(entries[0]), "\n" #prints the first entry
print entries[0].prettify(), "\n" #prints the first entry out
print entries[0].find('content').prettify(), "\n" #prints the first content tag in the first entry



titles = []
for item in entries:
    titles.append(item.find('title').string)
#this iterates through the entries and puts each event's title into a list
print titles, "\n"



for item in entries:
    print item.find('content').prettify(), "\n"
