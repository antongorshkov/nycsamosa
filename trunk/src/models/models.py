from google.appengine.ext import db

class GenericResult():
    description = ""
    def description(self):
        return self.description
    
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
    distance = db.FloatProperty()
    def description(self):
        return "%s: %s @ %s (%.1g miles)" % (self.eventName,self.eventDescription,self.location,self.distance)
#        return self.eventName + ": " + self.eventDescription + " @ " + self.location + "(" + str(self.distance) + " miles)"
#        Res_HTML += "(%s) %s (%.1g miles)<br>" % (self.results_index+1,res.description(),res.distance)
    def long(self):
        return "longtitude"
       
class Street(db.Model):
    street = db.StringProperty()   
    zipcode = db.IntegerProperty()
    borough = db.StringProperty()   

class Parking(db.Model):
    facilityType = db.StringProperty()
    licenseNumber = db.StringProperty()
    statusEntityLicense = db.StringProperty()
    licenseExpirationDate = db.StringProperty()
    entityName = db.StringProperty()
    tradeName = db.StringProperty()
    addressBldg = db.StringProperty()
    addressStreetName = db.StringProperty()
    akaAddress = db.StringProperty()
    addressCity = db.StringProperty()
    addressState = db.StringProperty()
    addressZipCode = db.IntegerProperty()
    telephoneNumber = db.IntegerProperty()
    numberofSpaces = db.IntegerProperty()
    webAddress = db.StringProperty()
    latitude = db.FloatProperty()
    longtitude = db.FloatProperty()
    distance = db.FloatProperty()
    
    def description(self):
        return self.entityName + "@" + self.webAddress
    
    def long(self):
        return "longtitude" 

class AltParking(db.Model):
    reason = db.StringProperty()
    date = db.DateTimeProperty()
   
class Laundromat(db.Model):
    camisTradeName = db.StringProperty()
    entityName = db.StringProperty()
    licenseNumber = db.IntegerProperty()
    address = db.StringProperty()
    longitude = db.FloatProperty()
    latitude = db.FloatProperty()
    distance = db.FloatProperty()
    
    def description(self):
        return self.entityName + "@" + self.address
    
    def long(self):
        return "longitude"    
   
class SidewalkCafe(db.Model):
    licenseNumber = db.IntegerProperty()
    name = db.StringProperty()
    tradeTypeCamis = db.StringProperty()
    address = db.StringProperty()
    telephoneNumber = db.IntegerProperty()
    squareFootage = db.IntegerProperty()
    locationAddress = db.StringProperty()
    licenseExpirationDate = db.DateTimeProperty()
    latitude = db.FloatProperty()
    longitude = db.FloatProperty()
    distance = db.FloatProperty()
    
    def description(self):
        return self.name + "@" + self.address
    
    def long(self):
        return "longitude"

class WifiSpot(db.Model):
    address = db.StringProperty()
    latitude = db.FloatProperty()
    longitude = db.FloatProperty()
    name = db.StringProperty()
    
    def description(self):
        return self.name + "@" + self.address
    
    def long(self):
        return "longitude"

class Feedback(db.Model):
    feedback_type = db.StringProperty
    address = db.StringProperty()
    latitude = db.FloatProperty()
    longitude = db.FloatProperty()
    user_input = db.StringProperty()
    contact = db.StringProperty()
    date = db.DateTimeProperty()
    attach_name =  db.StringProperty()
    attach = db.BlobProperty()