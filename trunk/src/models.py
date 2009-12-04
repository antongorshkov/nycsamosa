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

class WifiSpot(db.Model):
    name = db.StringProperty()
    address = db.StringProperty()
    latitude = db.FloatProperty()
    longitude = db.FloatProperty()
    