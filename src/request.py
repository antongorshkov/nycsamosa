'''
Created on Nov 30, 2009

@author: Anton Gorshkov
'''

from geopy import geocoders
from geopy import distance
from geopy import Point
from helpers import logger
from google.appengine.ext import db
from google.appengine.api import mail
from urllib2 import urlopen

GOOGLE_KEY = 'ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA'
YAHOO_KEY = 'u_EhiVnV34EZAxPQhoPq8dNEHGw8bUME10Hd7BYYwHZYB5irmhW90Q9d.VK_e1KB'
MILE = 0.01502 #bad bad approximation - need to calculate more precise
RANGE = MILE*0.1 #by default 5 mile 'radius', in future need to give option
EMAIL_SENDER = "daveou@gmail.com"

class Request(object):
    '''
    Request Object stores user request and any additional information about request.
    '''

    def __init__(self, input, sender = None ):
        '''
        Constructor
        '''
        logger.LogIt(input)        
        self.user_input = input
        self.parseIt()
        self.geoTagIt()
        self.sender = sender
                
    def show(self):
        print(self.user_input)
        print(self.query_type)
        print(self.place)
        print(self.lat, self.lng)
    
    def parseIt(self):
        #TODO Parsing logic to extract everything (address, type of query, etc)
        self.address = self.user_input
        self.query_type = 'EVENT'
    
    def geoTagIt(self):        
        g = geocoders.Google(GOOGLE_KEY)
        y = geocoders.Yahoo(YAHOO_KEY) 
        try:
            place, (lat, lng) = g.geocode(self.address)
        except ValueError:    
            place, (lat, lng) = y.geocode(self.address)
        self.place = place
        self.lat = lat
        self.lng = lng
    
    
    def execute(self):
        '''
        Execute the Request.  If its a query, issue the search and store results on the object
        If its a complaint, then file the complaint
        '''
        lng_min = self.lng - RANGE
        lng_max = self.lng + RANGE
        lat_min = self.lat - RANGE
        lat_max = self.lat + RANGE
        self.LogIt("lng_min: " + str(lng_min))
        self.LogIt("lng_min: " + str(lng_max))   
        self.LogIt("lat_min: " + str(lat_min))
        self.LogIt("lat_min: " + str(lat_max))
        
        #    Can't query by two parameters, so only querying on one and then doing distance calculation
        #    This is not good.  Need GeoHash based algorithm instead.
        query = db.GqlQuery("SELECT * FROM Event WHERE longtitude > :lomin AND longtitude < :lomax", 
                            lomin=lng_min, lomax=lng_max )
        #    query = db.GqlQuery("SELECT * FROM Event WHERE longtitude > :lomin AND longtitude < :lomax"
        #                    "AND latitude > :lamin AND latitude < :lamax",
        #                    lomin=lng_min, lomax=lng_max, lamin=lat_min, lamax=lat_max)
         
        ret_results = []
        for result in query:
            p1 = Point(result.latitude, result.longtitude)
            p2 = Point(self.lat, self.lng) 
            result.distance = distance.distance(p1, p2).miles
            ret_results.append( result )
        
        def compare(a, b):
            return cmp(a.distance, b.distance)
        
        ret_results.sort(compare)
        
        self.SearchResults = ret_results

    def showWeb(self):
        Res_HTML = """<body style="background-image:url(http://www.google.com/sms/images/bigphone.jpg); background-repeat:no-repeat"> <div id=cellphoneDiv style="margin: 93px 0px 0px 37px; height: 218px; width: 164px; overflow: auto;"> <div id=inbox align=center style="font-family: arial; font-size: 80%;"><br></div><div id=messageBox style="font-family: arial; font-size: 80%; font-weight: bold; white-space: -moz-pre-wrap; word-wrap: break-word;">"""                      
        results = self.SearchResults[0:5]
        url = self.GetGoogleMapURL(results)
        #TODO: we need to maintain proper counter - use result array index somehow?
        i=1       
        for res in results:
            Res_HTML += "(" + str(i) + ") " + res.eventName + ": " + res.eventDescription + " @ " + res.location + "(" + str(res.distance) + " miles)<br>"            
            i=i+1        
        Res_HTML += "</div></div><br><br><br><p><img border=\"0\" src=\""
        Res_HTML += url
        Res_HTML += "\"/></p></body></html>"
        return(Res_HTML)

    def sendMail(self, subject):        
        subject = "Re: " + subject
        body = "Results:\n"
        results = self.SearchResults[0:5]
        i=1
        for res in results:
            body = body + "(" + str(i) + ") " + res.eventName + ": " + res.eventDescription + " @ " + res.location 
            i=i+1
        url = self.GetGoogleMapURL(results)                
        logger.LogIt("URL is: " + url)
        filehandle = urlopen(url)              
        mail.send_mail(sender=EMAIL_SENDER,
                       to=self.sender,
                       subject=subject,
                       body=body,
                       attachments=[("pic.png", filehandle.read())]
                       )
    
    def GetGoogleMapURL(self, results):
        markers = "&markers=color:red|label:You|"+str(self.lat)+","+str(self.lng)
        i=1
        for res in results:
            markers = markers + "&markers=color:blue|label:"+str(i)+"|"+str(res.latitude)+","+str(res.longtitude) 
            i=i+1
        url="http://maps.google.com/maps/api/staticmap?center="+str(self.lat)+","+str(self.lng)
        url=url+"&zoom=14&size=512x512&maptype=roadmap&sensor=false"+markers+"&key="+GOOGLE_KEY
        return(url)
        
    def LogIt(self, msg):
        logger.LogIt(msg)