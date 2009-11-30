import urllib
import time
    
#f = open('/root/workspace/Samosa/data/streets/zips','r')
#zips = []
#for i in range(1,241):
#    s = f.readline()
#    zips.append([s[0:5],s[6:]])
#f.close()
 
zips = [['10314','Staten Island'],[' ',' ']]
    
for i in range(1,2):    
    time.sleep(1)
    u = urllib.urlopen("http://www.melissadata.com/lookups/zipstreet.asp?InData="+zips[i-1][0])
    s = u.read()
    u.close()
    end = s.find("/lookups/newstyle2009.css\" rel=\"stylesheet")
    f = open('/root/workspace/Samosa/data/streets/strs','w')
    begin,idx = 0,0
    while idx > -1:
        idx = s.find("zipstreet.asp?Step4=",begin)
        if idx > -1:
            qt = s.find('\"',idx)
            f.write(s[idx+31:qt]+'\t'+zips[i-1][0]+'\t'+zips[i-1][1]+'\n')
#            print (s[idx+31:qt]+'\t'+zips[i-1][0]+'\t'+zips[i-1][1])
            begin = qt
    f.close()
    print i,' '+zips[i-1][0]+' printed to file'