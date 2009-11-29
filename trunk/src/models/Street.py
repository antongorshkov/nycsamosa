'''
Created on Nov 29, 2009

@author: David Rytzarev
'''
from google.appengine.ext import db

class Street(db.Model):
    streetName = db.StringProperty()    
    zip = db.IntegerProperty()
    borough = db.StringProperty()