from helpers.traffic import Traffic    
    
#s = parse('http://a841-dotweb01.nyc.gov/datafeeds/WeeklyTraf.xml')
#print str(s.entries[0].description)[:1000]
#t = Traffic(s.entries[0].description)

t = Traffic('Morristown, NJ', '1 Beard Street, Brooklyn, NY 11231')
a = t.relevantUpdates()
for x in a:
    print '==>> %s,\n%s' % (x[0], x[1])
