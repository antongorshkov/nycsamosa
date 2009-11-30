import re

def shrinker(string):
    string=' '+string.lower()+' '
    
    string = re.sub(' street ',' st ',string)
    string = re.sub(' avenue ',' ave ',string)
    string = re.sub(' east ',' e ',string)
    string = re.sub(' west ',' w ',string)
    string = re.sub(' north ',' n ',string)
    string = re.sub(' south ',' s ',string)
    string = re.sub(' boulevard ',' blvd ',string)
    string = re.sub(' road ',' rd ',string)
    string = re.sub(' drive ',' dr ',string)
    string = re.sub(' parkway ',' pkwy ',string)
    string = re.sub('\s+',' ',string)
    string = string.strip()
    
    print string
    

   
#    east2,west2,blvd2,street2,avenue2,road2,drive2 = -1,-1,-1,-1,-1,-1,-1
#    east1 = string.lower().find("east")
#    if east1 > -1:
#        east2 = string.lower().find("east",east1+1)
#    west1 = string.lower().find("west")
#    if west1 > -1:
#        west2 = string.lower().find("west",west1+1)
#    blvd1 = string.lower().find("boulevard")
#    if blvd1 > -1:
#        blvd2 = string.lower().find("boulevard",blvd1+1)
#    street1 = string.lower().find("street")    
#    if street1 > -1:
#        street2 = string.lower().find("street",street1+1)
#    avenue1 = string.lower().find("avenue")    
#    if avenue1 > -1:
#        avenue2 = string.lower().find("avenue",avenue1+1)
#    road1 = string.lower().find("road")    
#    if road1 > -1:
#        road2 = string.lower().find("road",road1+1)
#    drive1 = string.lower().find("drive")    
#    if drive1 > -1:
#        drive2 = string.lower().find("drive",drive1+1)
#
#    print east1,west1,street1,avenue1,blvd1,road1,drive1,':::',east2,west2,street2,avenue2,blvd2,road2,drive2
    
    
