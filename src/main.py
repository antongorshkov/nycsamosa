import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import memcache
from helpers import logger
from helpers import parser
import request
import re

#TODO: MOVE THESE to common constant files!
GOOGLE_KEY = 'ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA'
YAHOO_KEY = 'u_EhiVnV34EZAxPQhoPq8dNEHGw8bUME10Hd7BYYwHZYB5irmhW90Q9d.VK_e1KB'

#TODO: CODE REPEAT on the Static Map stuff.  Should be a single library that takes an array of markers?
#TODO: The Try Google if doesn't work, do Yahoo functionality needs to be encapsulated somewhere 
#(at least implement in the mail Handler

class MailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logger.LogIt("Received a message from: " + mail_message.sender)
        logger.LogIt("Subject: " + mail_message.subject)
        m = memcache.Client()
        plaintext = mail_message.bodies(content_type='text/plain')
        for text in plaintext:
            txtmsg = ""
            txtmsg = text[1].decode()
        
        logger.LogIt("Body is %s" % txtmsg)
        logger.LogIt("Length of body is: " + str(len(txtmsg)))        
        req = m.get(mail_message.sender)
        More_RegEx = re.compile('more|yes|next', re.I)           
        if req is not None and More_RegEx.search(txtmsg) is not None:
            req.sendMail(mail_message.subject)            
        else:
            req = request.Request(txtmsg,mail_message.sender)
            req.execute()
            req.sendMail(mail_message.subject)
    
        #Always set the Request object back to memory as it has updated info
        if not m.set(mail_message.sender, req ):
            logger.LogIt("Error storing request in memcache")
        
class MainPage(webapp.RequestHandler):
    def get(self):
        logger.LogIt("MainPage got called" )
        self.response.out.write("""
          <html><body>
              <form action="/websms" method="post">
              <input type="text" value="" name="sms" id="searchTerm" size="45" ><input type="submit" value="Send SMS to Samosa4!">
              </form></body></html>""")


class WebSMS(webapp.RequestHandler):
    def post(self):
        logger.LogIt("WebSMS post called" )
        txtQuery = parser.ParseIt(cgi.escape(self.request.get('sms')))
        req = request.Request(txtQuery)
        req.execute()
        self.response.out.write( req.showWeb() )
        m = memcache.Client()
        if not m.set("123", req, 60):
            self.response.out.write( 'Problemo using memcache!' )
        
class QuickClass(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Hello There5!<br>")
        m = memcache.Client()
        req = m.get("123")
        self.response.out.write(req.getData())
        #z = array.array('L')
        #f = open('./FASTLEXICON_3.MDF','rb')
        #print f
        #z.fromfile(f,125000)
        #print len(z)        
        #print z

#        q = MontyLingua.MontyLingua()
#        sentence = 'Show me events near 54th and 5th ave'
#        q.pp_info(q.jist(sentence))        
#        text = nltk.word_tokenize("pothole on 54th St and Lexington Ave?")
#        text_tagged = nltk.pos_tag(text)
#        print text_tagged
            
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