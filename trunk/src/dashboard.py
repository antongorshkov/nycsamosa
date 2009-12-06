'''
Created on Dec 5, 2009

@author: Anton Gorshkov
'''

#Anton got this one:
GOOGLE_KEY = 'ABQIAAAAtaHRQFa02xlz0i3fu8ySPxSH7FXBwHSUoWsCAYRfqtoxAWqychQGBY8Apv9gr2X3FlFUW82d0SluZg'
YAHOO_KEY = 'u_EhiVnV34EZAxPQhoPq8dNEHGw8bUME10Hd7BYYwHZYB5irmhW90Q9d.VK_e1KB'

#ANTON's Yahoo Key
YAHOO_KEY = 'rfaEY5HV34FgMWkBkyLlbKKizvfDlkRnZb7sBWE4u7HtfedNUmB10QOvfFYQop3b'

from pymaps.pymaps import Map, PyMap, Icon # import the libraries
from models.models import *

def getDashBoard():
    return showmap2()

#Yahoo!
def showmap2():
    res = """  
<html>
<head>
<style type="text/css">
#map{
height: 75%;
width: 100%;
}
</style>
</head>
<body>
<div id="map"></div>

<script type="text/javascript" src="http://api.maps.yahoo.com/ajaxymap?v=3.8&appid=rfaEY5HV34FgMWkBkyLlbKKizvfDlkRnZb7sBWE4u7HtfedNUmB10QOvfFYQop3b"></script>
<script type="text/javascript">
    // Create a map object
    var map = new YMap(document.getElementById('map'));

    // Add map type control
    map.addTypeControl();  
    map.addZoomLong();  
    map.addPanControl();  

    function createYahooMarker(lat, lng, marker_html) {
        var myMarker = new YMarker(new YGeoPoint( lat,lng ));
        YEvent.Capture(myMarker,EventsList.MouseClick, function() { myMarker.openSmartWindow(marker_html) });
        return myMarker;
    }
    // Set map type to either of: YAHOO_MAP_SAT, YAHOO_MAP_HYB, YAHOO_MAP_REG
    map.setMapType(YAHOO_MAP_REG);
"""
    query = Feedback.all()
    
    #myMarker = new YMarker(new YGeoPoint( 40.6515882,-73.9330429 ));
    #marker_html = "Hey There! <br><img width=200 height=200 src=http://nycsamosa.appspot.com/image?key=aglueWNzYW1vc2FyEAsSCEZlZWRiYWNrGNuKBAw>"
    #YEvent.Capture(myMarker,EventsList.MouseClick, function() { myMarker.openSmartWindow(marker_html) }); 
    #map.addOverlay(myMarker);
        
    for result in query:            
        if result.attach_name is not None:
            img_url = "http://nycsamosa.appspot.com/image?key=%s" % result.key()
            marker_html = "%s <br> <img width=200 height=200 src=%s>" % (result.user_input, img_url) 
            #res += "\tmyMarker = new YMarker(new YGeoPoint( %s,%s ), new YImage('%s',new YSize(20,20),new YCoordPoint(0,0)));\n" % (result.latitude, result.longitude, img_url)
        else:
            marker_html = "%s" % result.user_input
            
        #res += "\tmyMarker = new YMarker(new YGeoPoint( %s,%s ));\n" % (result.latitude, result.longitude)
        #res += "YEvent.Capture(myMarker,EventsList.MouseClick, function() { myMarker.openSmartWindow('%s') });\n" % marker_html
        #res += "\tmyMarker.openSmartWindow( \"%s\" );\n" % result.user_input
        #res += "\tmap.addOverlay(myMarker);\n"
        #http://nycsamosa.appspot.com/image?key=aglueWNzYW1vc2FyEAsSCEZlZWRiYWNrGMGDBAw
        res += "\tmap.addOverlay(createYahooMarker(%s,%s,'%s'));" %  (result.latitude, result.longitude, marker_html)
        
    res += """    
    //myPoint = new YGeoPoint( 40.5856189,-73.9565551 );
    //myMarker = new YMarker(myPoint);
    //myMarker.openSmartWindow( "tree" );
    //map.addOverlay(myMarker);
    //myMarker = new YMarker(new YGeoPoint( 40.7388327,-73.9852212 )));
    //myMarker.openSmartWindow( "messy tree" );
    //map.addOverlay(myMarker);
    

    //var currentGeoPoint = new YGeoPoint( 40.5856189, -73.9565551 );
    //var marker = new YMarker( currentGeoPoint );
    //marker.addLabel( "Test" );
    //marker.openSmartWindow( "Hey There!" );  
    //map.addMarker(marker);
    //map.addOverlay(marker);  

    // Display the map centered on a geocoded location
    map.drawZoomAndCenter("New York", 6);
</script>
</body>
</html>
"""  
    return res

#Google + PyMaps
def showmap():

    # Create a map - pymaps allows multiple maps in an object
    tmap = Map()
    tmap.zoom = 12

    # Latitude and lognitude - see the getcords function
    # to see how we convert from traditional D/M/S to the DD type
    # used by Googel Maps
    
    query = Feedback.all()
    
    icon = Icon("Test")
    for result in query:            
        point = (result.latitude, result.longitude, result.user_input, icon.id)
        tmap.setpoint(point)
        
    lat = 40.5856189 
    long = -73.9565551
            
    tmap.center = (lat,long)

    # Put your own googl ekey here
    gmap = PyMap(key=GOOGLE_KEY, maplist=[tmap])
    gmap.addicon(icon)

    # pymapjs exports all the javascript required to build the map!
    mapcode = gmap.pymapjs()

    # Do what you want with it - pass it to the template or print it!
    res = """
    <body onload="load()" onunload="GUnload()">        
    <div id="map" style="width: 760px; height: 460px"></div>
    </body> 
    """     
    return res + mapcode