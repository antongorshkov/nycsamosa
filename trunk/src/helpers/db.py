'''
Created on Nov 24, 2009

@author: Anton Gorshkov
'''
from google.appengine.ext import db

class Event(db.Model):
    borough = db.StringProperty(required=False)
    eventDescription = db.StringProperty(required=False)
    eventEndDate = db.StringProperty(required=False)
    eventName = db.StringProperty(required=False)
    eventStartDate = db.StringProperty(required=False)
    eventTypeDescription = db.StringProperty(required=False)
    eventid = db.IntegerProperty()
    location = db.StringProperty(required=False)
    
def query(search):
    query = Event.all()
    results = [];
    for result in query:
        if search.lower() in result.location.lower():
            results.append( result )
    return( results )