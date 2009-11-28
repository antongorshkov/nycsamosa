#A simple comment to test SVN commits

import cgi
import email

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import mail
from helpers import logger
from helpers import parser
from helpers import db
from geopy import geocoders
#from urllib import urlencode
from urllib2 import urlopen

class MailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logger.LogIt("Received a message from: " + mail_message.sender)
        logger.LogIt("Subject: " + mail_message.subject)
        
        plaintext = mail_message.bodies(content_type='text/plain')
        for text in plaintext:
            txtmsg = ""
            txtmsg = text[1].decode()
        
        logger.LogIt("Body is %s" % txtmsg)
        logger.LogIt("Length of body is: " + str(len(txtmsg)))        
        
        sender = "daveou@gmail.com"        
        subject = "Re: " + mail_message.subject
#        message.body = "Got your message" + txtmsg
        body = "Results:\n"
        #txtQuery = parser.ParseIt(txtmsg)
        txtQuery = str(txtmsg)        
        results = db.query(txtQuery)
        i=1
        #REMOVE FROM HERE! DRY!!!!!
        api_key = "ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA"
        g = geocoders.Google(api_key)  
        place, (lat, lng) = g.geocode(txtQuery)    
        markers = "&markers=color:red|label:You|"+str(lat)+","+str(lng)
        for res in results:
            body = body + "(" + str(i) + ") " + res.eventName + ": " + res.eventDescription + " @ " + res.location
            markers = markers + "&markers=color:blue|label:"+str(i)+"|"+str(res.latitude)+","+str(res.longtitude) 
            i=i+1
        url="http://maps.google.com/maps/api/staticmap?center="+str(lat)+","+str(lng)
        url=url+"&zoom=14&size=512x512&maptype=roadmap&sensor=false"+markers+"&key="+api_key
        logger.LogIt("URL is: " + url)
        filehandle = urlopen(url)              
        mail.send_mail(sender=sender,
                       to=mail_message.sender,
                       subject=subject,
                       body=body,
                       attachments=[("pic.png", filehandle.read())]
                       )
         
        
class MainPage(webapp.RequestHandler):
    def get(self):
        logger.LogIt("MainPage got called" )
        self.response.out.write("""
          <html><body>
              <form action="/websms" method="post">
              <input type="text" value="" name="sms" id="searchTerm" size="45" ><input type="submit" value="Send SMS to Samosa!">
              </form></body></html>""")


class WebSMS(webapp.RequestHandler):
    def post(self):
        logger.LogIt("WebSMS post called" )
        self.out("""<body style="background-image:url(http://www.google.com/sms/images/bigphone.jpg); background-repeat:no-repeat"> <div id=cellphoneDiv style="margin: 93px 0px 0px 37px; height: 218px; width: 164px; overflow: auto;"> <div id=inbox align=center style="font-family: arial; font-size: 80%;"><br></div><div id=messageBox style="font-family: arial; font-size: 80%; font-weight: bold; white-space: -moz-pre-wrap; word-wrap: break-word;">""")
        txtQuery = parser.ParseIt(cgi.escape(self.request.get('sms')))        
        results = db.query(txtQuery)
        i=1
        for res in results:
            self.out("(" + str(i) + ") " + res.eventName + ": " + res.eventDescription + " @ " + res.location + "(" + str(res.distance) + " miles)<br>")
            i=i+1
        self.out("</div></div></body></html>")        
                
    def out(self, txt):
        self.response.out.write(txt)
        
class QuickClass(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Hello There2!<br>")
        logger.LogIt("Q get called" )
        url = "http://maps.google.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=14&size=512x512&maptype=roadmap\&markers=color:blue|label:S|40.702147,-74.015794&markers=color:green|label:G|40.711614,-74.012318&markers=color:red|label:C|40.718217,-73.998284&sensor=false&key=ABQIAAAAzr2EBOXUKnm_jVnk0OJI7xSsTL4WIgxhMZ0ZK_kHjwHeQuOD4xQJpBVbSrqNn69S6DOTv203MQ5ufA"
        filehandle = urlopen(url)              
        mail.send_mail(sender="daveou@gmail.com",
                       to="6467338252@mms.att.net",
                       subject="Test Sending Google Image",
                       body=";)",
                       attachments=[("pic.png", filehandle.read())]
                       )
            
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/websms', WebSMS),
                                      ('/q', QuickClass),                                      
                                      MailHandler.mapping()
                                      ],                                      
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()