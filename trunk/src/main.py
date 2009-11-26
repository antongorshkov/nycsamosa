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
        
        message = mail.EmailMessage()
        message.sender = "daveou@gmail.com"
        message.to = mail_message.sender
        message.subject = "Re: " + mail_message.subject
#        message.body = "Got your message" + txtmsg
        body = "Results:\n"
        #txtQuery = parser.ParseIt(txtmsg)
        txtQuery = str(txtmsg)        
        results = db.query(txtQuery)
        i=1
        for res in results:
            body = body + "(" + str(i) + ") " + res.eventName + ": " + res.eventDescription + " @ " + res.location
            i=i+1 
        message.body = body
        message.send()
         
        
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
            self.out("(" + str(i) + ") " + res.eventName + ": " + res.eventDescription + " @ " + res.location + "<br>")
            i=i+1
        self.out("</div></div></body></html>")        
                
    def out(self, txt):
        self.response.out.write(txt)
        
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/websms', WebSMS),
                                      MailHandler.mapping()
                                      ],                                      
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()