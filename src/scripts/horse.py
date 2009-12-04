import httplib, re, time

from shrinker import *


class locator:

    def foo(startRow,numRows,fn):
        f = open('/root/workspace/Samosa/data/'+fn,'r')
        intersections = []
        for i in range(startRow):
            f.readline()
        for i in range(startRow,startRow+numRows):
            s = f.readline()
            tok1 = s.find(' between ')
            tok2 = s.find(' and ')
            tok3 = s.find(',')
            tok4 = s.find('\t')
            if(tok2 == -1 and tok3 == -1):
                tok5 = tok4
            elif(tok2 == -1):
                tok5 = tok3
            elif(tok3 == -1):
                tok5 = tok2
            else:
                tok5 = min(tok2,tok3)
            street1 = s[0:tok1].strip()
            street2 = s[tok1+9:tok5].strip()
            borough = s[s.find('\t')+1:s.find('\n')]
            intersections.append([street1,street2,borough])
        f.close()
        return intersections
        
    def goo(string2DArray):
        conn = httplib.HTTPConnection("maps.google.com")
        apiKey = "ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA"
        googleData = []
        count = 1
        for r in string2DArray:
            if(count%5 == 0):
                time.sleep(1)
            street = r[0]+'+and+'+ r[1]
            borough = r[2]
            param = "/maps/geo?q="+street+",+"+borough+",+ny&output=json&sensor=false&key="+apiKey
#            param = "/maps/geo?q=8+AVENUE+and+WEST+14+STREET,+manhattan,+NY&output=json&sensor=false&key=ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA"
            conn.request("GET", param)
            response = conn.getresponse()
            #print response.status, response.reason 
            if(response.reason == 'OK'):
                r = response.read()
                googleData.append(r)
            count = count + 1
        conn.close()
        return googleData
    
    def extractCoordinates(googleData):
        points = []
        for d in googleData:
            tok1 = d.find('coordinates')
            tok2 = d.find('coordinates', tok1+10)
            if tok2 != -1: 
                tok3 = d.find('coordinates', tok2+10)
            else:
                tok3 = -1
            p1 = [d[tok1+16:tok1+27],d[tok1+29:tok1+39]]
            if tok2 != -1:
                p2 = [d[tok2+16:tok2+27],d[tok2+29:tok2+39]]
            else:
                p2 = None
            if tok3 != -1:
                p3 = [d[tok3+16:tok3+27],d[tok3+29:tok3+39]]
            else:
                p3 = None
            points.append([p1,p2,p3])
        return points
    
    def replaceSpaces(string2DArray):
        for x in string2DArray:
            x[0] = re.sub('\s+','+',x[0])
            x[1] = re.sub('\s+','+',x[1])

######### BEGIN  
# 
 
    
#
#def loc(street,city,state,zipc):
#    engine, date = 1, ""  #1 = Google, 2 = Yahoo
#    if(engine == 1):
#        conn = httplib.HTTPConnection("maps.google.com")
#        apiKey = "ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA"
#        param = "/maps/geo?q="+street+",+"+city+",+"+state+",+"+zipc+"&output=json&sensor=false&key="+apiKey
#        conn.request("GET", param)
#    if(engine == 2):
#        conn = httplib.HTTPConnection("local.yahooapis.com")
#        param = "/MapsService/V1/geocode?appid=u_EhiVnV34EZAxPQhoPq8dNEHGw8bUME10Hd7BYYwHZYB5irmhW90Q9d.VK_e1KB"
#        conn.request("POST", param+"&street="+street+"&city="+city+"&state="+state)
#    response = conn.getresponse()
#    print response.status, response.reason
#    if(response.reason == 'OK'):
#        data = response.read()
#        print data
#        coords = extractCoordinates(data)
#        print coords
#    conn.close()
#    return coords

    
    
#    replaceSpaces(ints)
#    for q in ints:
#        print q[0],q[1],q[2]
#    googleData = goo(ints)
#    points = extractCoordinates(googleData)
#    counter=1
#    count1 = 0
#    count2 = 0
#    count3 = 0
#    for p,q in zip(points,ints):
#        print q[0]+'+and+'+q[1],',',q[2],'\t',p[0][0],'\t',p[0][1]
#        count1 = count1 + 1
#        if p[1] != None: 
#            print '\t','\t','\t',p[1][0],'\t',p[1][1]
#            count2 = count2 + 1
#        if p[2] != None:
#            print '\t','\t','\t',p[2][0],'\t',p[2][1]
#            count3 = count3 + 1
#        counter = counter + 1
#
#    print count1,count2,count3
    
  
#g = geocoders.Google(GOOGLE_KEY)
#y = geocoders.Yahoo(YAHOO_KEY)
#
#try:
#    place, (lat, lng) = g.geocode(search)
#except ValueError:    
#    place, (lat, lng) = y.geocode(search)
    
    