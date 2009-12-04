'''
Created on Nov 30, 2009

@author: Anton Gorshkov
'''

from geopy import geocoders
from geopy import distance
from geopy import Point
from helpers import logger
#from google.appengine.ext import db
from google.appengine.api import mail
from urllib2 import urlopen
from models.models import * #@UnusedWildImport google wants it!
import re
from datetime import date

GOOGLE_KEY = 'ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA'
YAHOO_KEY = 'u_EhiVnV34EZAxPQhoPq8dNEHGw8bUME10Hd7BYYwHZYB5irmhW90Q9d.VK_e1KB'
MILE = 0.01502 #bad bad approximation - need to calculate more precise
RANGE = MILE*0.1 #by default 5 mile 'radius', in future need to give option
EMAIL_SENDER = "nycsamosa@gmail.com"
HELP_STRING = """Welcome to Samosa!
You can get info about all of city services and more. Use the following convention:
cafes@union square, new york
events @ 85 Broadway
laundry @ 10004
You can also search for Wifi, Parking
'altpark' for alternate parking rules
You can also search for wifi, parking.  You can ask for Alternate Parking rules!  
"""

class RequestHandler(object):
    '''
    RequestHandler - handles every request
    '''

    def __init__(self, input, sender = None ):
        '''
        Constructor
        '''
        logger.LogIt(input)        
        self.user_input = input
        self.address = ""
        self.Request = GenericRequest("UNKNOWN")
        self.parseIt()
        self.Request.geoTagIt()
        self.sender = sender
        self.logSelf()
                
    def show(self):
        print(self.user_input)
        #print(self.type)
        #print(self.place)
        #print(self.lat, self.lng)
    
    def logSelf(self):
        self.LogIt(self.getData())
            
    def getData(self):
        data = self.user_input + "\n" + self.Request.getData() + "\n"
        return(data)
       
    def parseIt(self):       
        #Rules will be applied in order(i think?), first rule wins!
        Rules = {
                 re.compile('event|happenings', re.I): LocateRequest("Event"),
                 re.compile('laund|cleaners', re.I): LocateRequest("Laundromat"),
                 re.compile('alternate|altpark', re.I): AltParking("AltParking"),                 
                 re.compile('parking|park', re.I): LocateRequest("Parking"),
                 re.compile('cafe|restaurant', re.I): LocateRequest("SidewalkCafe"),
                 re.compile('wifi|wireless|internet', re.I): LocateRequest("WifiSpot"),                 
                 re.compile('\?|help', re.I): HelpRequest("HELP"),
                 }        
        #We assume having @ means there is an address
        if "@" in self.user_input:        
            ( self.query, self.address ) = self.user_input.split("@",1)   
        else:            
            self.query = self.user_input
            
        for RegEx, Request in Rules.iteritems():                   
            if RegEx.search(self.query) is not None:
                self.Request = Request
                self.Request.address = self.address
                self.Request.query = self.query 
                break                               #First Rule Wins!            
       
    def execute(self):
        '''
        Execute the Request.  If its a query, issue the search and store results on the object
        If its a complaint, then file the complaint
        '''
        self.Request.execute()


    def showWeb(self):
        Res_HTML = """<body style="background-image:url(http://www.google.com/sms/images/bigphone.jpg); background-repeat:no-repeat"> <div id=cellphoneDiv style="margin: 93px 0px 0px 37px; height: 218px; width: 164px; overflow: auto;"> <div id=inbox align=center style="font-family: arial; font-size: 80%;"><br></div><div id=messageBox style="font-family: arial; font-size: 80%; font-weight: bold; white-space: -moz-pre-wrap; word-wrap: break-word;">"""
        Res_HTML += self.Request.WebResults()                      
        Res_HTML += "\"/></p></body></html>"
        return Res_HTML

    def sendMail(self, subject):        
        subject = "Re: " + subject       
        #TODO: Need to handle cases when requested typeslice is bigger then results!
        attachment = self.Request.getAttachment()
        body = self.Request.MailResults()        
        if len(attachment):
            mail.send_mail(sender=EMAIL_SENDER,to=self.sender,subject=subject,body=body,attachments=attachment)
        else:
            mail.send_mail(sender=EMAIL_SENDER,to=self.sender,subject=subject,body=body)
        
    def LogIt(self, msg):
        logger.LogIt(msg)

class GenericRequest(object):
    '''
    GenericRequest - base request object.
    '''

    def __init__(self, type):
        '''
        Constructor
        '''
        self.address = ""
        self.results_index = 0
        self.type = type
        
    def LogIt(self, msg):
        logger.LogIt(msg)
        
    def getData(self):
        return self.address + "\n" 
    
    def GetGoogleMapURL(self, results):
        markers = "&markers=color:red|label:You|"+str(self.lat)+","+str(self.lng)
        i=1
        for res in results:
            long = eval("res."+res.long())
            markers = markers + "&markers=color:blue|label:"+str(i)+"|"+str(res.latitude)+","+str(long) 
            i=i+1
        url="http://maps.google.com/maps/api/staticmap?center="+str(self.lat)+","+str(self.lng)
        url=url+"&zoom=14&size=512x512&maptype=roadmap&sensor=false"+markers+"&key="+GOOGLE_KEY
        return(url)
    
    def getAttachment(self):
        return []
    
    def execute(self):
        return
    
    def WebResults(self):
        return "I didn't get you!?  Try 'HELP' for more info."
    
    def MailResults(self):
        return self.WebResults()
        
    def geoTagIt(self):
        if len(self.address) < 1:
            return
                        
        g = geocoders.Google(GOOGLE_KEY)
        y = geocoders.Yahoo(YAHOO_KEY)
         
        try:
            place, (lat, lng) = g.geocode(self.address)
        except ValueError:    
            place, (lat, lng) = y.geocode(self.address)
        self.place = place
        self.lat = lat
        self.lng = lng
                
class LocateRequest(GenericRequest):
    '''
    LocateRequest - handles requests to find entities
    '''

    def execute(self):
        lng_min = self.lng - RANGE
        lng_max = self.lng + RANGE
        lat_min = self.lat - RANGE
        lat_max = self.lat + RANGE
        self.LogIt("lng_min: " + str(lng_min))
        self.LogIt("lng_max: " + str(lng_max))   
        self.LogIt("lat_min: " + str(lat_min))
        self.LogIt("lat_max: " + str(lat_max))
        
        #TODO: Probably best to query by date alone and then just store all results since we're outputing them 5 at a time
        #    Can't query by two parameters, so only querying on one and then doing distance calculation
        #    This is not good.  Need GeoHash based algorithm instead.
        #obj = eval(str(self.type)+"()")
        #select = "SELECT * FROM " + self.type + " WHERE "+ obj.long() +" > :lomin AND " + obj.long() + " < :lomax";
        query = eval( self.type + ".all()" )
        
        ##ORIGINAL QUERY
        #select = "SELECT * FROM " + self.type + " WHERE latitude > :lamin AND latitude < :lamax";
        #query = db.GqlQuery(select, lamin=lat_min, lamax=lat_max )
        
        #    query = db.GqlQuery("SELECT * FROM Event WHERE longtitude > :lomin AND longtitude < :lomax"
        #                    "AND latitude > :lamin AND latitude < :lamax",
        #                    lomin=lng_min, lomax=lng_max, lamin=lat_min, lamax=lat_max)
         
        self.LogIt(str(query))
        ret_results = []
        for result in query:
            long = eval("result."+result.long())
            p1 = Point(result.latitude, long)
            p2 = Point(self.lat, self.lng) 
            result.distance = distance.distance(p1, p2).miles
            ret_results.append( result )
        
        def compare(a, b):
            return cmp(a.distance, b.distance)
        
        ret_results.sort(compare)
        
        self.SearchResults = ret_results[0:25]
        
    def WebResults(self):
        Res_HTML = ""
        results = self.SearchResults[0:5]
        url = self.GetGoogleMapURL(results)
        #TODO: we need to maintain proper counter - use result array index somehow?
        i=1       
        for res in results:
            Res_HTML += "(" + str(i) + ") " + res.description() +"<br>"            
            i=i+1        
        Res_HTML += "</div></div><br><br><br><p><img border=\"0\" src=\""
        Res_HTML += url
        return Res_HTML
    
    def MailResults(self):
        body = "Results:\n"
        results = self.SearchResults[self.results_index:self.results_index+5]
        for res in results:
            body = body + "(" + str(self.results_index+1) + ") " + res.description()
            self.results_index += 1
        return body
    
    def getAttachment(self):
        results = self.SearchResults[self.results_index:self.results_index+5]
        url = self.GetGoogleMapURL(results)
        logger.LogIt("URL is: " + url)                        
        filehandle = urlopen(url)      
        attachment = [("pic.png", filehandle.read())]
        return attachment         

class AltParking(GenericRequest):
    '''
    InfoRequest - handles requests to get some information
    '''
    def execute(self):
        query = db.GqlQuery("SELECT * FROM AltParking WHERE date >= :today ORDER BY date ASC", today=date.today() )
        
        self.LogIt(str(query))
        ret_results = []
        for result in query:
            ret_results.append( result )        
        self.SearchResults = ret_results[0:100]

    def WebResults(self, line_break="<br>"):
        body = "Upcoming Alternate Parking Holidays:\n"
        results = self.SearchResults[self.results_index:self.results_index+5]
        for res in results:
            body = body + "(" + str(self.results_index+1) + ") " + res.date.strftime("%m/%d/%y") + " - " + res.reason + line_break
            self.results_index += 1
        return body            
    
    def MailResults(self):
        return self.WebResults("\n")

class HelpRequest(GenericRequest):
    '''
    HelpRequest - handles requests for Help
    '''
    def WebResults(self):
        return HELP_STRING