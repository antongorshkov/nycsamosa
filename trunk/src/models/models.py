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
    longtitude = db.FloatProperty()
    latitude = db.FloatProperty()
        
class Street(db.Model):
    street = db.StringProperty()    
    zipcodes = db.IntegerProperty()
    borough = db.StringProperty()


