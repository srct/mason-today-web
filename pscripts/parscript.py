#print "and we begin"

from bs4 import BeautifulSoup
import requests

eventDict = {}

class Event:
    def __init__(self, entryTag): #where var entryTag is a specific event tag
        self.__name = entryTag.find('title').string
        self.__description = entryTag.find('content').string
        self.__time = "timeplaceholder"
        self.__date = "dateplaceholder"
        self.__location = "locationplaceholder"

    def __str__(self):
        return self.__name + ": " + self.__description + "\n\n"

    def addDescript(description):
        self.__description = description

    def addTime(time):
        self.__time = time

    def addDate(date):
        self.__date = date

    def addLocation(location):
        self.__location = location

def cleanup(str):
    str = str.replace("&amp;", "&")
    str = str.replace("&nbsp;", " ")
    str = str.replace("&ndash;", "-")
    str = str.replace("&lt;", "<")
    str = str.replace("&gt;", ">")
    str = str.replace("<br/>", "\n")
    return str


#this gets rid of the given things that all of them say false or true. It doesn't seem useful and it's just easier to ignore just get rid of it
def cleancontent(str):
    str = str.replace("Publish event on the Calendar?: TRUE \n" , "")
    str = str.replace("Performing any medical procedures?: FALSE \n" , "")
    str = str.replace("Parking Needed?: FALSE \n" , "")
    str = str[0:len(str) - 1]#this is here because there's always a \n at the end and it's pissing me off and is getting in the way
    return str

xmldoc = requests.get("http://25livepub.collegenet.com/calendars/events_all.xml") #grabs the xml from 25live
#xmldoc = open("events.xml", "r") #Opens a local document. events.xml is a shortened version of the larger events doc

xmldoc = cleanup(xmldoc.text)
#print xmldoc
soup = BeautifulSoup(xmldoc, "lxml") #creates soup of the xml
#print soup.prettify(), "\n\n"

#creates a list of all the entry tags from the xml
entries = soup.findAll('entry')

counter = 0



#indexs an entry in the list of entries 
for entry in entries:

    #pulls up an entry in the list of entries, finds the title tag and .text deletes all xml tags and returns just the text
    entry_title = entry.title.text
    #print entry_title
    #print ""

    print "---------------------------------------------------start -----------------------------------------------------"
    entry_content = entry.content.text

    #check clearcontent function

    #makes it easy to find as things may be unevenly spaced 
    entry_content = entry_content.replace("\n\n\n" , "\n")
    entry_content = entry_content.replace("\n\n" , "\n")
    entry_content = cleancontent(entry_content) 

    entry_detailes = entry_content.split("\n")

    if (
    entry_detailes[0][0:6] == "Monday" or 
    entry_detailes[0][0:7] == "Tuesday" or 
    entry_detailes[0][0:9] == "Wednesday" or 
    entry_detailes[0][0:8] == "Thursday" or 
    entry_detailes[0][0:6] == "Friday" or 
    entry_detailes[0][0:8] == "Saturday" or 
    entry_detailes[0][0:6] == "Sunday" or 
    entry_detailes[0][0:7] == "Ongoing"):
        if len(entry_detailes) == 2:
            location = "no location"
            date = entry_detailes[0]
            description = entry_detailes[1]
        elif len(entry_detailes) == 1:
            location = "no location"
            date = entry_detailes[0]
            description = "no description"
        else:
            print "wut, this hsouldn't print plz halp, they probably changed the xml or something and means we need to update but if it work we should just ship it"
            
    elif(
    entry_detailes[1][0:6] == "Monday" or 
    entry_detailes[1][0:7] == "Tuesday" or 
    entry_detailes[1][0:9] == "Wednesday" or 
    entry_detailes[1][0:8] == "Thursday" or 
    entry_detailes[1][0:6] == "Friday" or 
    entry_detailes[1][0:8] == "Saturday" or 
    entry_detailes[1][0:6] == "Sunday" or 
    entry_detailes[1][0:7] == "Ongoing"):
        if len(entry_detailes) == 2:
            location = entry_detailes[0]
            date = entry_detailes[1]
            description = "no description given"
        elif len(entry_detailes) == 3:
            location = entry_detailes[0]
            date = entry_detailes[1]
            description = entry_detailes[2]
        else:
            print "wut, this hsouldn't print plz halp, they probably changed the xml or something and means we need to update but if it work we should just ship it"
    print counter
    print len(entry_detailes)

    if counter == 36:
        print entry_detailes#idk what going on with entry 36, drama department doin something weird and it shouldn't work but it does idk


    counter += 1
    print location
    print date
    print description



#27

'''

#just use as needed
content = entries[37].content.text
content = content.replace("\n\n" , "\n")
content = content.replace("\n\n\n" , "\n")
#content = cleancontent(content)
content = cleancontent(content)
#print content


detailes = content.split("\n")

print detailes[0]
print detailes[1]
print detailes[2]


'''