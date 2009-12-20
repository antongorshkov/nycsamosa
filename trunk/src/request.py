'''
Created on Nov 30, 2009

@author: Anton Gorshkov
'''
import sys

from geopy import geocoders
from geopy import distance
from geopy import Point
from helpers import logger
#from google.appengine.ext import db
from google.appengine.api import mail
from urllib2 import urlopen
from models.models import * #@UnusedWildImport google wants it!
import re
from datetime import date, datetime
from dateutil.relativedelta import *
from dateutil.parser import *
from feedparser import feedparser
from helpers.traffic import Traffic

#Previous Key:
#GOOGLE_KEY = 'ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA'

#Anton got this one:
GOOGLE_KEY = 'ABQIAAAAtaHRQFa02xlz0i3fu8ySPxSH7FXBwHSUoWsCAYRfqtoxAWqychQGBY8Apv9gr2X3FlFUW82d0SluZg'
YAHOO_KEY = 'u_EhiVnV34EZAxPQhoPq8dNEHGw8bUME10Hd7BYYwHZYB5irmhW90Q9d.VK_e1KB'
MILE = 0.01502 #bad bad approximation - need to calculate more precise
RANGE = MILE*0.1 #by default 5 mile 'radius', in future need to give option
EMAIL_SENDER = "nycsamosa@gmail.com"
HELP_STRING = """Welcome to nycSaMoSa! SMS for City info or make a 311 complaint. Ask about events on any day "events tomorrow", about altparking suspension dates "altparking", or wifi,cafe,parking or laundry around any location "wifi near union square" or "parking at lexington & E 54th"
"""
CONFUSION = "I'm sorry, I didn't understand you.  Please try again or reply 'HELP' for more info."
EVENTS_RSS='http://www.nycgovparks.org/xml/events_300_rss.xml'
MORE_STRING='reply \'more\' for additional listings.'

class RequestHandler(object):
    '''
    RequestHandler - handles every request
    '''

    def __init__(self, input, sender = None, attachment = [] ):
        '''
        Constructor
        '''
        logger.LogIt(input)        
        self.user_input = input
        self.address = ""
        self.sender = sender
        self.Request = GenericRequest("UNKNOWN")
        self.Request.AdditionalInfo = "input: '"+input+"'. "
        self.attachment = attachment
        self.parseIt()
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
                 #RegEx to match agains                [ ClassName        Type     ]
                 #Misc.
                 1:  [ re.compile('alternate|altpark', re.I),   "AltParking", "AltParking"],
                 2:  [ re.compile('event|happening', re.I),     "EventRequest", "EventRSS"],
                 3:  [ re.compile('traffic', re.I),             "TrafficRequest", "TrafficRSS"],
                                  
                 #Location Based
                 #re.compile('event|happenings', re.I):      [ "LocateRequest", "Event" ],
                 4:  [ re.compile('laund|cleaners', re.I),      "LocateRequest", "Laundromat"],                 
                 5:  [ re.compile('parking|park', re.I),        "LocateRequest","Parking"],
                 6:  [ re.compile('cafe|restaurant', re.I),     "LocateRequest", "SidewalkCafe"],
                 7:  [ re.compile('wifi|wireless|internet', re.I),"LocateRequest", "WifiSpot"],                                  
                                
                 #Help
                 8:  [ re.compile('\?|help', re.I),             "HelpRequest", "HELP" ],       
                 #Feedback Requests
                 9:  [ re.compile("tree", re.I),                "FeedbackRequest", "DAMAGED_TREE" ],
                 10: [ re.compile("sign", re.I),                "FeedbackRequest", "STREET_SIGN" ],
                 11: [ re.compile("light", re.I),               "FeedbackRequest", "STREET_LIGHT" ],
                 12: [ re.compile("lot", re.I),                 "FeedbackRequest", "VACANT_LOT" ],
                 13: [ re.compile("street", re.I),              "FeedbackRequest", "STREET_CONDITION" ],
                 14: [ re.compile("taxi", re.I),                "FeedbackRequest", "TAXI_LOST" ],
                 15: [ re.compile("graf", re.I),                "FeedbackRequest", "BUILD_GRAFFITI" ],
                 16: [ re.compile("broken|dirty|missing|filthy|unsafe|damaged", re.I),"FeedbackRequest", "OTHER" ],
                 }        
        query = self.user_input
        address = ""
        #We assume having @/at/around means there is an address
        AddrRegEx = re.compile("@| around | at | near |close to")
        if AddrRegEx.search(query) is not None:
            ( query, address ) = re.split(AddrRegEx,self.user_input,1)      
            
        for Rule in Rules.itervalues():                   
            if Rule[0].search(query) is not None:
                try:
                    self.LogIt("Trying to instantiate " + Rule[1])
                    req = globals()[Rule[1]](Rule[2], query, address, self.sender, self.attachment)
                    self.Request = req
                except ValueError:
                    self.Request.AdditionalInfo += str(sys.exc_info()[1])
                except:
                    self.LogIt("Failed, going for UNKNOWN" + str(sys.exc_info()[0]))
                    self.Request.AdditionalInfo += str(sys.exc_info()[1])
 
                break    #First Rule Wins!            
        
    def execute(self):
        '''
        Execute the Request.  If its a query, issue the search and store results on the object
        If its a complaint, then file the complaint
        '''
        self.Request.execute()


    def showWeb(self, more=None):
#        Res_HTML = """<body style="background-image:url(http://www.google.com/sms/images/bigphone.jpg); background-repeat:no-repeat"> <div id=cellphoneDiv style="margin: 93px 0px 0px 37px; height: 218px; width: 164px; overflow: auto;"> <div id=inbox align=center style="font-family: arial; font-size: 80%;"><br></div><div id=messageBox style="font-family: arial; font-size: 80%; font-weight: bold; white-space: -moz-pre-wrap; word-wrap: break-word;">"""
        Res_HTML = """
        <html><body >
        <table border="0">
        <tr><td style="background-image:url(static/img/aaa.jpg); background-repeat:no-repeat"> 
        <div id=cellphoneDiv style="margin: 9px 20px 42px 30px; height: 203px; width: 155px; overflow: auto;"> 
            <div id=messageBox style="font-family: arial; font-size: 80%; font-weight: bold; white-space: -moz-pre-wrap; word-wrap: break-word;">
        """
        Res_HTML += self.Request.WebResults(more)
        Res_HTML += """       
        </div></div></td><td>
        <div id=mapDiv style="margin: 0px 0px 5px 37px; height: 310px; width: 310px; overflow: auto; font-family: Tahoma, sans-serif; font-size: 76%; color: #888;">
        """            
        if self.Request.img_url is not None:
            Res_HTML += "Image sent to phone:<br><img border=\"0\" src=\"%s\">" % self.Request.img_url
        Res_HTML += "</div></p></body></html>"
        return Res_HTML

    def sendMail(self, subject, more=None):        
        subject = "Re: " + subject       
        attachment = self.Request.getAttachment()
        logger.LogIt("Calling Request.MailResults(more)")
        body = self.Request.MailResults(more)        
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

    def __init__(self, type, query="", address="", sender="", attachment=[]):
        '''
        Constructor
        '''
        self.AdditionalInfo = ""
        self.LogIt("Started Constructor...")
        self.IsGeoTagged = False
        self.attachment = attachment
        self.address = address
        self.sender = sender
        self.query = query
        self.results_index = 0
        self.type = type
        self.img_url = None
        self.UserResponse = ""
        self.PreProcessQuery()
        self.geoTagIt()
        if self.validate() is not True:
            self.LogIt("Failed validation!?!?!")
            raise "Failed to Validate!"
        
    def PreProcessQuery(self):
        return True
    
    def LogIt(self, msg):
        logger.LogIt(msg)
        
    def getData(self):
        return self.address + "\n"
    
    def validate(self):
        self.LogIt("Should be returning True!")
        return True 
    
    def GetGoogleMapURL(self, results):
        markers = "&markers=color:red|label:You|"+str(self.lat)+","+str(self.lng)
        i=1
        for res in results:
            long = eval("res."+res.long())
            markers = markers + "&markers=color:blue|label:"+str(i)+"|"+str(res.latitude)+","+str(long) 
            i=i+1
        url="http://maps.google.com/maps/api/staticmap?center="+str(self.lat)+","+str(self.lng)
        url=url+"&zoom=15&size=200x200&maptype=roadmap&sensor=false&mobile=false"+markers+"&key="+GOOGLE_KEY
        return(url)
    
    def getAttachment(self):
        return []
    
    def execute(self):
        return
    
    def WebResults(self, more=None):
        return CONFUSION + " (" + self.AdditionalInfo + ")"
    
    def MailResults(self, more=None):
        return self.WebResults()
        
    def geoTagIt(self):
        if len(self.address) < 1:
            return
        
        RegEx = re.compile('New York|Manhattan|Brooklyn|Queens|Staten Island|Bronx|SI|BK|NY', re.I)
        #No Borough specified, default to New York
        if RegEx.search(self.address) is None:
            self.address += " New York"
        
        #Google likes "and" better than "&".
        self.address = self.address.replace("&", "and")
        self.address = self.address.replace("amp;", "")
                        
        g = geocoders.Google(GOOGLE_KEY)
        y = geocoders.Yahoo(YAHOO_KEY)
         
        try:
            place, (lat, lng) = g.geocode(self.address)
        except ValueError:
            try:    
                place, (lat, lng) = y.geocode(self.address)
            except:                
                return

        RegEx = re.compile("New York|NY|USA|,")
        self.place = re.sub(RegEx, "", place)        
        self.lat = lat
        self.lng = lng
        self.IsGeoTagged = True
        self.LogIt(place)
                
class LocateRequest(GenericRequest):
    '''
    LocateRequest - handles requests to find entities
    '''

    def validate(self):
        if len(self.address) < 1:
            raise ValueError("Missing Address")
        
        return self.IsGeoTagged
    
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
        
    def WebResults(self, more=None):
        Res_HTML = "Results near %s:<br>" % self.place
        results = self.SearchResults[self.results_index:self.results_index+5]        
        url = self.GetGoogleMapURL(results)
        for res in results:
            Res_HTML += "(%s) %s<br>" % (self.results_index+1,res.description())
            self.results_index+=1
        self.img_url = url
        Res_HTML += MORE_STRING
        return Res_HTML
    
    def MailResults(self, more=None):        
        body = "Results near %s:\n" % self.place
        results = self.SearchResults[self.results_index:self.results_index+5]
        for res in results:
            body += "%s. %s\n" % (self.results_index+1,res.description())
            self.results_index += 1
        body += "Reply 'more' for additional results."
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

    def WebResults(self, more=None, line_break="<br>"):
        body = "Upcoming Alternate Parking Holidays:\n"
        results = self.SearchResults[self.results_index:self.results_index+5]
        for res in results:
            body = body + "(" + str(self.results_index+1) + ") " + res.date.strftime("%m/%d/%y") + " - " + res.reason + line_break
            self.results_index += 1
        body += "Reply 'more' for additional results."            
        return body            
    
    def MailResults(self, more=None):        
        return self.WebResults(None, "\n")

class HelpRequest(GenericRequest):
    '''
    HelpRequest - handles requests for Help
    '''
    def WebResults(self, more=None):
        return HELP_STRING
    
class FeedbackRequest(GenericRequest):
    '''
    FeedbackRequest - handles feedback
    '''
    
    '''
    Parse the feedback and store in the database.
    Include User / Location / Feedback Type / Feedback Date / Photo
    '''
    def execute(self):
        feedback = Feedback()
        feedback.feedback_type = self.type
        feedback.address = self.address
        feedback.latitude = self.lat
        feedback.longitude = self.lng
        feedback.user_input = self.query
        feedback.contact = self.sender
        feedback.date = datetime.now()
        if len(self.attachment) > 1:
            feedback.attach_name = self.attachment[0]
            feedback.attach = self.attachment[1]
        self.LogIt("About to submit Feedback!")
        feedback.put()
        
    def MailResults(self, more=None, line_break="\n"):
        return "Thank you for your feedback! You can visit http://nycsamosa.appspot.com/dashboard to see it.(loc:%s)" % self.place
    
    def WebResults(self, more=None):
        return "Thank you for your feedback! You can visit our <a href=http://nycsamosa.appspot.com/dashboard target=\"_blank\">Dashboard</a> to see it.(loc:%s)" % self.place

class EventRequest(GenericRequest):
    '''
    EventRequest - handle RSS Events
    '''
    
    def execute(self):
        def ParseDate(dt):
            TODAY = date.today()
            WordDates = {   'today'     : TODAY, 
                            'tomorrow'  : TODAY+relativedelta(days=+1),
                            'monday'    : TODAY+relativedelta(weekday=MO),
                            'tuesday'   : TODAY+relativedelta(weekday=TU),
                            'wednesday' : TODAY+relativedelta(weekday=WE),
                            'thursday'  : TODAY+relativedelta(weekday=TH),
                            'friday'    : TODAY+relativedelta(weekday=FR),
                            'saturday'  : TODAY+relativedelta(weekday=SA),
                            'sunday'    : TODAY+relativedelta(weekday=SU),                                
            }
            dt = dt.lower()
            real_date = None
            try:
                real_date = WordDates[dt]
                real_date = datetime(real_date.year, real_date.month, real_date.day)
            except:
                try:
                    real_date = parse(dt)
                except:
                    return
            
            return real_date
        
        #Continiously try to remove first word until you can find a date
        def ParseInput(inp):
            dt = ParseDate(inp)
            if dt is None:
                spl = inp.split(" ", 1)
                if len(spl) > 1:
                    return ParseInput(spl[1])
                else:
                    return None
            else:
                return dt
        
        dt = ParseInput(self.query)
        if dt is None:
            dt = date.today()
            dt = datetime(dt.year, dt.month, dt.day)
        self.event_date = dt    
        d = feedparser.parse(EVENTS_RSS)
        self.LogIt("Looking for events on %s" % dt)
        ret_results = []
        for e in d.entries:
            event_date = parse(e.startdate)
            if event_date == dt:
                ret_results.append( e )
        
        self.LogIt("Found %s events " % len(ret_results))
        self.SearchResults = ret_results[0:25]
        
    def WebResults(self, more=None, line_break="<br>"):
        return self.MailResults(more, line_break)
        
    def MailResults(self, more=None, line_break="\n"):        
        #Display back (with option to ask for details!)
        #Lets see if its a detail request
        self.LogIt("Inside MailResults... more: %s" % more)        
        if more is not None:
            num = None
            RegEx = re.compile("[0-9]+")            
            found = RegEx.search(more)
            if found is not None:
                num = int(found.group(0))
                
            if num is not None:
                desc = self.SearchResults[num-1].description
                if line_break == "\n":
                    desc = desc.replace("</p>","\n")
                    RegEx = re.compile('<.*?>', re.I)
                    desc = re.sub(RegEx, "", desc)
                return desc
        body = "Events on %s:%s" % (self.event_date.strftime("%m/%d/%y"),line_break)

        results = self.SearchResults[self.results_index:self.results_index+5]
        for res in results:
            body = body + str(self.results_index+1) + ". " + res.title + line_break
            self.results_index += 1
        
        if self.results_index>len(self.SearchResults)-1:
            body += "End of Results."
        else:
            body += "Reply 'more' for additional results or 'more 1' for details on #1 ."            
        return body

class TrafficRequest(GenericRequest):
    '''
    TrafficRequest - handle Traffic
    '''

    def PreProcessQuery(self):
        inp = self.query
        inp = inp.replace("traffic","")
        inp = inp.replace("from","")
        res = inp.split(" to ",1)
        if len(res) != 2:
            raise ValueError("Need two addresses in the form \"address1\" to \"address2\"")
        else:
            (self.from_addr,self.to_addr) = res
    
    def validate(self):
        try:
            self.traffic = Traffic(self.from_addr,self.to_addr)
            return True
        except:
            raise ValueError("Failed to get Traffic info.") 
            
    def execute(self):
        self.SearchResults = self.traffic.relevantUpdates()

#TODO: DRY! Same as in previous class.
    def WebResults(self, more=None, line_break="<br>"):
        return self.MailResults(more, line_break)
        
    def MailResults(self, more=None, line_break="\n"):        
        if more is not None:
            num = None
            RegEx = re.compile("[0-9]+")            
            found = RegEx.search(more)
            if found is not None:
                num = int(found.group(0))
                
            if num is not None:
                return self.SearchResults[num-1][0]+ ":" + line_break + self.SearchResults[num-1][1]

        body = "Traffic updates on your route:%s" % line_break
        results = self.SearchResults[self.results_index:self.results_index+10]
        for res in results:
            body = body + str(self.results_index+1) + ". " + res[0] + line_break
            self.results_index += 1
        if self.results_index>len(self.SearchResults)-1:
            body += "End of Results."
        else:
            body += "Reply 'more' for additional results or 'more 1' for details on #1 ."    
        return body
