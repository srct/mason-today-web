#print "and we begin"

from bs4 import BeautifulSoup
from datetime import date, time
import requests

eventDict = {}

DaysOfWeek = {
    "Sunday" : 0,
    "Monday" : 1,
    "Tuesday" : 2,
    "Wednesday" : 3,
    "Thursday" : 4,
    "Friday" : 5,
    "Saturday" : 6,
}


notProvide = "Not not provided"
counter = 0

class Event:
    def __init__(self, entryTag): #where var entryTag is a specific event tag
        self.__name = entryTag.find('title').string
        self.__description = entryTag.find('content').string
        self.__time = "timeplaceholder"
        self.__date = "dateplaceholder"
        self.__location = "locationplaceholder"
        self.__timehour = "00"
        self.__timemin = "00"
        self.__day = "null day"

    def __str__(self):
        return self.__name + ": " + self.__description + "\n\n"

    def setDescription(description):
        self.__description = description

    def setTime(time):
        self.__time = time

    def setDate(date):
        self.__date = date

    def setLocation(location):
        self.__location = location

    def setTimehour(timehour):
        self.__timehour = timehour

    def setTimeminute(timemin):
        self.__timemin = timemin

    def setDay(day):
        self.__day = day

def cleanup(str):
    str = str.replace("&amp;", "&")
    str = str.replace("&nbsp;", " ")
    str = str.replace("&ndash;", "-")
    str = str.replace("&lt;", "<")
    str = str.replace("&gt;", ">")
    str = str.replace("<br/>", "\n")
    str = str.replace("Publish event on the Calendar?: TRUE \n" , "")
    str = str.replace("Performing any medical procedures?: FALSE \n" , "")
    str = str.replace("Parking Needed?: FALSE \n" , "")
    str = str[0:len(str) - 1]
    return str


#this just seems like useless junk everytime they pop up it's always false or always true for the given condition 
def cleancontent(str):
    str = str.replace("Publish event on the Calendar?: TRUE \n" , "")
    str = str.replace("Performing any medical procedures?: FALSE \n" , "")
    str = str.replace("Parking Needed?: FALSE \n" , "")

    #this is here because there's always a \n at the end and it's pissing me off and is getting in the way
    str = str[0:len(str) - 1]
    return str

class eventException:

    def __init__(self,message):
        self.__message = message
        self.__exceptionlist = []

    def __str__(self):
        return self.__exceptionlist
    


xmldoc = requests.get("http://25livepub.collegenet.com/calendars/events_all.xml") #grabs the xml from 25live
#xmldoc = open("events.xml", "r") #Opens a local document. events.xml is a shortened version of the larger events doc

xmldoc = cleanup(xmldoc.text)
#print xmldoc
soup = BeautifulSoup(xmldoc, "lxml") #creates soup of the xml
#print soup.prettify(), "\n\n"



#creates a list of all the entry tags from the xml
entries = soup.findAll('entry')


#indexs an entry in the list of entries 
for entry in entries:

    #pulls up an entry in the list of entries, finds the title tag and .text deletes all xml tags and returns just the text as a string
    entry_title = entry.title.text

    entry_content = entry.content.text


    #makes it easy to find as things may be unevenly spaced 
    entry_content = entry_content.replace("\n\n\n" , "\n")
    entry_content = entry_content.replace("\n\n" , "\n")

    #check clearcontent function
    entry_content = cleanup(entry_content) #we might just get rid of this one

    #each piece of content may is seperated by a newline, entry_detailes creates a list 
    entry_detailes = entry_content.split("\n")


    #in entry detailes list normally the conditions go as follow
    #[0] is the location
    #[1] is the date
    #[2] is the description

    #either conditions follows
    #[0] is date 

    #[0] is location
    #[1] is date 

    #[0] is date
    #[1] is description
 
    #sometimes the location or description is not given; however, the location always goes before date and
    #the description always follows the date. The date is always present. See examples above
    
    #(A) if the location is not given then the date must be index [0]
    #(B) if the length of the list = 1 and date is index [0] --> location not given & description is not given              
    #(C) if the length of the list = 2 and date is index [0] --> location not given but description is given at [1]         
    
    #(D) if the location is given then the date must be index [1]       
    #(E) if the length of the list = 2 and date is index [1] --> location is given at [0] but description is not given      
    #(F) if the length of the list = 3 and date is index [1] --> location is given at [0] and description is given at [2]   
    

    #the two if statements finds the date string. The date string always starts with 
    #Monday Tuesday Wednesday Thursday Friday Saturday Sunday or Ongoing and the date 
    #is always on either [0] or [1]
    
    #see (A) above
    if entry_detailes[0].split(",")[0] in DaysOfWeek:
        #See (B)
        if len(entry_detailes) == 1:
            location = notProvide
            entry.location = "no location"
            date = entry_detailes[0]
            description = notProvide
        #see (C)
        elif len(entry_detailes) == 2:
            location = notProvide
            date = entry_detailes[0]
            description = entry_detailes[1]
        #This extra case was made because one entry had the description split into two by a 
        #newline so it registered as two descriptions making the length = 3
        elif len(entry_detailes) == 3:  
            location = notProvide
            date = entry_detailes[0]
            description = entry_detailes[1] + " " + entry_detailes[2]
        #this will print if the code has failed to account for something in detailes, but it works as of December 26th 2017
        else:
            raise eventException("failed to account for detail in entry_detailes when date element is index 0 on entry_detailes list")


    #see (D) above
    elif entry_detailes[1].split(",")[0] in DaysOfWeek:
        #See (E)
        if len(entry_detailes) == 2:
            location = entry_detailes[0]
            date = entry_detailes[1]
            description = notProvide
        #See (F)
        elif len(entry_detailes) == 3:
            location = entry_detailes[0]
            date = entry_detailes[1]
            description = entry_detailes[2]
        #This extra case was made because one entry had the description split into two by a 
        #newline so it registered as two descriptions making the length = 3
        elif len(entry_detailes) == 4:
            location = entry_detailes[0]
            date = entry_detailes[1]
            description = entry_detailes[2] + " " + entry_detailes[3]
        #this will print if the code has failed to account for something in detailes
        else:
            raise eventException("failed to account for detail in entry_detailes when date element is index 1 on entry_detailes list")
    #this will print if the above if statements failed to find the date block
    else:
        raise eventException("failed to find and account for date element in entry_detailes list")
   

     
    if "Fairfax Campus" in location:
        location = location.split(", Fairfax Campus")
        campus = "Fairfax"
    elif "Arlington Campus" in location:
        location = location.split(", Arlington Campus")
        campus = "Arlington"
    else:
        location = [location]


    date = date.split(",")
    day = date[0]
    time = date[3][1:]
    date = date[1][1:] + "," + date[2]
    date = date.split(" ")
    month = date[0]
    monthday = date[1][:(len(date[1]) - 1)]
    year = date[2]


    print "-----------------------------------------------------------------------------"
    print location
    print day
    print month
    print monthday
    print year
    print time
    print description
    print "----------------------------------------------------------------------------"
    











#everything in the house is fuzzy, stupid dogs were acting like pollinators, if that's how you even spell it

