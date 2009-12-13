'''
Created on Dec 7, 2009

@author: David Rytzarev
'''

import urllib
import string
from feedparser.feedparser import * 
from helpers.googlemaps import GoogleMaps
import re


class Traffic():
    s,userOrig,userDest = '','',''
    
    def __init__(self,user1,user2):
        self.userOrig,self.userDest = user1,user2
        v = urllib.urlopen("http://a841-dotweb01.nyc.gov/datafeeds/WeeklyTraf.xml").read()
        self.s = v[:v.find('<pubDate>',v.find('</pubDate>'))]
        gmaps = GoogleMaps('ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA')
        directions = gmaps.directions(self.userOrig,self.userDest)
        
        #self.s = s        
    def betweenTags(self,str,begin,tag1,tag2):
        idx1 = str.find(tag1,begin)
        if idx1 == -1:
            return '',-1
        idx2 = str.find(tag2,idx1)
        return str[idx1+len(tag1):idx2],idx2
    
    def getUpdates(self):
        updates = []
        begin = 0
        head1 = '&lt;p&gt;'
        #head1 = '<p><span class="blue">'
        head2 = ':'
        #head2 = ':</span>'
        body2 = '&lt;/p&gt;'
        num = string.count(self.s,head1)
        for i in range(0,num):
            head,begin = self.betweenTags(self.s, begin, head1, head2)
            if(head.find('ridlock') == -1):
                body,begin = self.betweenTags(self.s, begin, head2+' ', body2)
                updates.append([head,body])
        return updates

    def googleSet(self):
        shrunk = ['St','Ave','Blvd','Pkwy','Rd','Dr','Pl','Expy','Hwy','Ln','<b>E ','<b>W ','<b>N ','<b>S ','/<wbr/>',' N</b>',' S</b>',' W</b>',' E</b>']
        expanded = ['Street','Avenue','Boulevard','Parkway','Road','Drive','Place','Expressway','Highway','Lane','<b>East ','<b>West ','<b>North ','<b>South ','</b> <b>',' North</b>',' South</b>',' West</b>',' East</b>']
        gmaps = GoogleMaps('ABQIAAAAAnMK37-crb-IVXX2SNmBOhStP4HpWo52j4u-OwfYEqnsxFY73BSpaiVrjhMtwbsCCfu2NkyPhj6myA')
        directions = gmaps.directions(self.userOrig,self.userDest)
        stepStream = ''
        for step in directions['Directions']['Routes'][0]['Steps']:
            stepStream += step['descriptionHtml']
        for i,j in zip(shrunk,expanded):
            stepStream = stepStream.replace(i,j)
        streets,begin = [],0
        while begin > -1:
            street,begin = self.betweenTags(stepStream, begin, '<b>', '</b>')
            if (street != '' and street != 'southeast' and street != 'northeast' and street != 'southwest' and 
                street != 'northeast' and street != 'left' and street != 'right' and street != 'north' and 
                street != 'south' and street != 'west' and street != 'east'):
                streets.append(street)
        return streets
    
    def relevantUpdates(self):
        shrunk = ['St','Ave','Blvd','Pkwy','Rd','rd','Dr','Pl','Expy','Hwy','Ln','E','W','N','S','Jan','Feb','Mar','Apr','Jun','Jul','Aug','Sep','Oct','Nov','Dec','apch','dir','passgr','rehab','constr','due','Sun','Mon','Tue','Wed','Thu','Fri','Sat','veh','btw',' & ','constr','rehab','inspect','maint','resurfacing','']
        expanded = ['Street','Avenue','Boulevard','Parkway','Road','road','Drive','Place','Expressway','Highway','Lane','East','West','North','South','January','February','March','April','June','July','August','September','October','November','December','approach','direction','passenger','rehabilitation','construction','to facilitate','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','vehicles','between',' and ','construction activity', 'rehabilitation activity','inspection activity','maintenance activity','resurfacing activity','the ']
        r = []
        strts = self.googleSet()
        updts = self.getUpdates()
        for u in updts:
            for s in strts:
                if u[0].find(s) > -1:
                    u[1] = u[1].replace('&amp;amp;', '&')
                    u[1] = u[1].replace('&lt;br /&gt;', '')
                    u[1] = u[1].replace('&lt;strong&gt;', '')
                    u[1] = u[1].replace('&lt;/strong&gt;', '')
                    for i,j in zip(expanded,shrunk):
                        u[0] = u[0].replace(i,j)
                        u[1] = u[1].replace(i,j)
                    r.append(u)
        return r