import datetime
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
                                    ('zipcodes', int),
                                    ('borough', str)
                                   ])

loaders = [EventLoader,StreetLoader]
