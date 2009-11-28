'''
Created on Nov 28, 2009

@author: Anton Gorshkov
'''
from google.appengine.ext import db

class Event(db.Model):
    eventid = db.IntegerProperty()    
    eventName = db.StringProperty()    
    eventTypeDescription = db.StringProperty()
    eventDescription = db.StringProperty()
    eventStartDate = db.StringProperty()    
    eventEndDate = db.StringProperty()        
    location = db.StringProperty()    
    borough = db.StringProperty()
    latitude = db.FloatProperty()    
    longtitude = db.FloatProperty()
    distance = db.FloatProperty()