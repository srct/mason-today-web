print "and we begin"

from bs4 import BeautifulSoup
import requests

class Event:
    def __init__(self, entryTag): #where var entryTag is a specific event tag
        self.__name = entryTag.find('title').string
        self.__description = entryTag.find('content').string
        self.__time = "timeplaceholder"
        self.__date = "dateplaceholder"
        self.__location = "locationplaceholder"

    def __str__(self):
        return self.__name + ": " + self.__description + "\n\n"

def cleanup(str):
    str = str.replace("&amp;", "&")
    str = str.replace("&nbsp;", " ")
    str = str.replace("&ndash;", "-")
    str = str.replace("&lt;", "<")
    str = str.replace("&gt;", ">")
    str = str.replace("<br/>", "\n")
    return str


xmldoc = requests.get("http://25livepub.collegenet.com/calendars/events_all.xml") #grabs the xml from 25live
#xmldoc = open("events.xml", "r") #Opens a local document. events.xml is a shortened version of the larger events doc

xmldoc = cleanup(xmldoc.text)
print xmldoc
soup = BeautifulSoup(xmldoc, "lxml") #creates soup of the xml
print soup.prettify(), "\n\n"


entries = soup.find_all('entry') #creates a list of all the entry tags from the xml
#print type(entries[0]), "\n" #prints the first entry
#print entries[0].prettify(), "\n" #prints the first entry out
#print entries[0].find('content').prettify(), "\n" #prints the first content tag in the first entry



#for item in entries:
#    print item.find('content').string, "\n\n"
