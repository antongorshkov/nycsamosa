'''
Created on Nov 24, 2009

@author: Anton Gorshkov
'''
from google.appengine.ext import db
from geopy import geocoders
from geopy import distance
from geopy import Point
from helpers import logger
from models import Event
    
GOOGLE_KEY = 'ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA'
YAHOO_KEY = 'u_EhiVnV34EZAxPQhoPq8dNEHGw8bUME10Hd7BYYwHZYB5irmhW90Q9d.VK_e1KB'
 
def query(search):
    mile = 0.01502 #bad bad approximation - need to calculate more precise
    range = mile*0.1 #by default 5 mile 'radius', in future need to give option
    g = geocoders.Google(GOOGLE_KEY)
    y = geocoders.Yahoo(YAHOO_KEY) 

    try:
        place, (lat, lng) = g.geocode(search)
    except ValueError:    
        logger.LogIt("Google errored, lets try yahoo")
        place, (lat, lng) = y.geocode(search)
        
    lng_min = lng - range
    lng_max = lng + range
    lat_min = lat - range
    lat_max = lat + range
    logger.LogIt("lng_min: " + str(lng_min))
    logger.LogIt("lng_min: " + str(lng_max))   
    logger.LogIt("lat_min: " + str(lat_min))
    logger.LogIt("lat_min: " + str(lat_max))
    
#    Can't query by two parameters, so only querying on one and then doing distance calculation
#    This is not good.  Need GeoHash based algorithm instead.
    query = db.GqlQuery("SELECT * FROM Event WHERE longtitude > :lomin AND longtitude < :lomax", 
                        lomin=lng_min, lomax=lng_max )
#    query = db.GqlQuery("SELECT * FROM Event WHERE longtitude > :lomin AND longtitude < :lomax"
#                    "AND latitude > :lamin AND latitude < :lamax",
#                    lomin=lng_min, lomax=lng_max, lamin=lat_min, lamax=lat_max)
     
    ret_results = []
    for result in query:
        p1 = Point(result.latitude, result.longtitude)
        p2 = Point(lat, lng) 
        result.distance = distance.distance(p1, p2).miles
        ret_results.append( result )
    
    def compare(a, b):
        return cmp(a.distance, b.distance)
    
    ret_results.sort(compare)
       
    return( ret_results[0:5] ) 
        
    #1. Build a box of 5 mile radius
    #2. Search within the box
    #3. Iterate over results, calculating distance of each one
    #4. Sort by Distance and return first 3
    
#    query = Event.all()
