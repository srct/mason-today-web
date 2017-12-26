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


#this just seems like useless junk everytime they pop up it's always false or always true for the given condition 
def cleancontent(str):
    str = str.replace("Publish event on the Calendar?: TRUE \n" , "")
    str = str.replace("Performing any medical procedures?: FALSE \n" , "")
    str = str.replace("Parking Needed?: FALSE \n" , "")

    #this is here because there's always a \n at the end and it's pissing me off and is getting in the way
    str = str[0:len(str) - 1]
    return str

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
    entry_content = cleancontent(entry_content) 


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
    
    if (#see (A) above
    entry_detailes[0][0:6] == "Monday" or 
    entry_detailes[0][0:7] == "Tuesday" or 
    entry_detailes[0][0:9] == "Wednesday" or 
    entry_detailes[0][0:8] == "Thursday" or 
    entry_detailes[0][0:6] == "Friday" or
    entry_detailes[0][0:8] == "Saturday" or 
    entry_detailes[0][0:6] == "Sunday" or 
    entry_detailes[0][0:7] == "Ongoing"):
        #See (B)
        if len(entry_detailes) == 1:
            location = "no location"
            date = entry_detailes[0]
            description = "no description"
        #see (C)
        elif len(entry_detailes) == 2:
            location = "no location"
            date = entry_detailes[0]
            description = entry_detailes[1]
        #This extra case was made because one entry had the description split into two by a 
        #newline so it registered as two descriptions making the length = 3
        elif len(entry_detailes) == 3:  
            location = "no location"
            date = entry_detailes[0]
            description = entry_detailes[1] + " " + entry_detailes[2]
        #this will print if the code has failed to account for something in detailes, but it works as of December 26th 2017
        else:
            print "wut, this hsouldn't print plz halp,"     

    elif(#see (D) above
    entry_detailes[1][0:6] == "Monday" or 
    entry_detailes[1][0:7] == "Tuesday" or 
    entry_detailes[1][0:9] == "Wednesday" or 
    entry_detailes[1][0:8] == "Thursday" or 
    entry_detailes[1][0:6] == "Friday" or 
    entry_detailes[1][0:8] == "Saturday" or 
    entry_detailes[1][0:6] == "Sunday" or 
    entry_detailes[1][0:7] == "Ongoing"):
        #See (E)
        if len(entry_detailes) == 2:
            location = entry_detailes[0]
            date = entry_detailes[1]
            description = "no description given"
        #See (F)
        elif len(entry_detailes) == 3:
            location = entry_detailes[0]
            date = entry_detailes[1]
            description = entry_detailes[2]
        #This extra case was made because one entry had the description split into two by a 
        #newline so it registered as two descriptions making the length = 3
        elif  len(entry_detailes) == 4:
            location = entry_detailes[0]
            date = entry_detailes[1]
            description = entry_detailes[2] + " " + entry_detailes[3]
        #this will print if the code has failed to account for something in detailes
        else:
            print "wut, this hsouldn't print plz halp"
    #this will print if the above if statements failed to find the date block
    else:
        print "if this prints there is something wrong please don't show up"
    
    print "-----------------------------------------------------------------------------"
    print location
    print date
    print description
    print "----------------------------------------------------------------------------"
    












#everything in the house is fuzzy 