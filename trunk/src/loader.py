import datetime
from datetime import datetime, date
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import models

class EventLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Event',
                                   [('eventid', int),
                                    ('eventName', str),
                                    ('eventTypeDescription', str),
                                    ('eventDescription', str),
                                    ('eventStartDate', str),
                                    ('eventEndDate', str),
                                    ('location', str),
                                    ('borough', str),
                                    ('longtitude', float),
                                    ('latitude', float)
                                   ])

class StreetLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Street',
                                   [('street', str),
                                    ('zipcode', int),
                                    ('borough', str)
                                   ])

class ParkingLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Parking',
                                   [('facilityType', str),
                                    ('licenseNumber', str),
                                    ('statusEntityLicense' , str),
                                    ('licenseExpirationDate', str),
                                    ('entityName' , str),
                                    ('tradeName' , str),
                                    ('addressBldg' , str),
                                    ('addressStreetName' , str),
                                    ('akaAddress' , str),
                                    ('addressCity' , str),
                                    ('addressState' , str),
                                    ('addressZipCode', int),
                                    ('telephoneNumber', int),
                                    ('numberofSpaces', int),
                                    ('webAddress' , str),
                                    ('latitude', float),
                                    ('longtitude', float)
                                    ])

class AltParkingLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'AltParking',
                                   [('reason', str),
                                    ('date', lambda x:datetime.strptime(x,"%Y-%m-%d"))
                                   ])

class LaundromatLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Laundromat',
                                   [('camisTradeName',str),
                                    ('entityName',str),
                                    ('licenseNumber',int),
                                    ('address',str),
                                    ('longitude',float),
                                    ('latitude',float)
                                   ])

class SidewalkCafeLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'SidewalkCafe',
                                   [('licenseNumber',int),
                                    ('name',str),
                                    ('tradeTypeCamis',str),
                                    ('address',str),
                                    ('telephoneNumber',int),
                                    ('squareFootage',int),
                                    ('locationAddress',str),
                                    ('licenseExpirationDate', lambda x:datetime.strptime(x,"%Y-%m-%d")),
                                    ('latitude',float),
                                    ('longitude',float)])


class WifiSpotLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'WifiSpot',
                                   [('name',str),
                                   ('address',str),
                                   ('latitude',float),
                                   ('longitude',float)
                                   ])


loaders = [EventLoader,StreetLoader,ParkingLoader,AltParkingLoader,LaundromatLoader,SidewalkCafeLoader,WifiSpotLoader]
