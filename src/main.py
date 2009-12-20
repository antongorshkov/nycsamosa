import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import db
from google.appengine.api import memcache
from helpers import logger
from helpers import parser
from dashboard import *
import request
import re


#TODO: MOVE THESE to common constant files!
#Previous one:
#GOOGLE_KEY = 'ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA'

#Anton got this one:
GOOGLE_KEY = 'ABQIAAAAtaHRQFa02xlz0i3fu8ySPxSH7FXBwHSUoWsCAYRfqtoxAWqychQGBY8Apv9gr2X3FlFUW82d0SluZg'
YAHOO_KEY = 'u_EhiVnV34EZAxPQhoPq8dNEHGw8bUME10Hd7BYYwHZYB5irmhW90Q9d.VK_e1KB'

class MailHandler(InboundMailHandler):
    def goodDecode(self, encodedPayload):
        encoding = encodedPayload.encoding
        payload = encodedPayload.payload
        if encoding and encoding.lower() != '7bit':
            payload = payload.decode(encoding)
        return payload

    def receive(self, mail_message):
        logger.LogIt("Received a message from: " + mail_message.sender)
        ########################################################################  BEGIN Modified by Dima (adding try/except)
        try: logger.LogIt("Subject: " + mail_message.subject)
        except: logger.LogIt("Subject: None")
        ########################################################################  END Modified by Dima        
        attachment = []
        pic = None
        logger.LogIt( str(mail_message.bodies))
        image = mail_message.bodies(content_type='image/jpeg')
        for i in image:
            pic = i[1]
        
        if pic is not None:
            attachment = ("hey!",db.Blob(self.goodDecode(pic)))
                                    
        plaintext = mail_message.bodies(content_type='text/plain')
        txtmsg = ""
        for text in plaintext:
            txtmsg = ""
            txtmsg = text[1].decode()
        txtmsg = txtmsg.split("\n")[0]
        logger.LogIt("Body is %s" % txtmsg)
        logger.LogIt("Length of body is: " + str(len(txtmsg)))
        m = memcache.Client()
        req = m.get(mail_message.sender)
        More_RegEx = re.compile('more|yes|next', re.I)           
        if req is not None and More_RegEx.search(txtmsg) is not None:
            logger.LogIt("This is a MORE Request!")
            req.sendMail(mail_message.subject,txtmsg)            
        else:
            req = request.RequestHandler(txtmsg,mail_message.sender,attachment)
            req.execute()
            req.sendMail(mail_message.subject)
    
        #Always set the Request object back to memory as it has updated info
        if not m.set(mail_message.sender, req ):
            logger.LogIt("Error storing request in memcache")
        
class MainPage(webapp.RequestHandler):
    def get(self):
        logger.LogIt("MainPage got called from ip: %s of type %s" % (self.request.remote_addr, type(self.request.remote_addr)) )
        self.response.out.write("""
          <html><body>
              <form action="/websms" method="get">
              <input type="text" value="" name="sms" id="searchTerm" size="45" ><input type="submit" value="Send SMS to Samosa4!">
              </form></body></html>""")

#TODO: DRY in WebSMS and MailHandler - one function!!!
class WebSMS(webapp.RequestHandler):
    def get(self):
        ip = self.request.remote_addr
        logger.LogIt("WebSMS post called from ip: %s" % ip )
        txtQuery = parser.ParseIt(cgi.escape(self.request.get('sms')))
        m = memcache.Client()
        req = m.get(ip)
        More_RegEx = re.compile('more|yes|next', re.I)           
        if req is not None and More_RegEx.search(txtQuery) is not None:
            self.response.out.write( req.showWeb(txtQuery) )            
        else:
            req = request.RequestHandler(txtQuery,"Web Request")
            req.execute()
            self.response.out.write( req.showWeb() )
        
        #Always set the Request object back to memory as it has updated info
        if not m.set(ip, req ):
            logger.LogIt("Error storing request in memcache")
        
class DashboardClass(webapp.RequestHandler):
    def get(self):  
        self.response.out.write(getDashBoard())

class ImageClass(webapp.RequestHandler):
    def get(self):
        key_str = self.request.get('key')
        key = db.Key(key_str)
        res = db.get(key)
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(res.attach)

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/websms', WebSMS),
                                      ('/dashboard', DashboardClass),
                                      ('/image', ImageClass),                                      
                                      MailHandler.mapping()
                                      ],                                      
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
