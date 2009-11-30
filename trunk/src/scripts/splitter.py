
#12402

allstrs = []
f1 = open('/root/workspace/SamosaSVNGoogle/data/streets','r')
for i in range(0,12402):
    allstrs.append(f1.readline())
f1.close()

for j in range(0,12402):
    f = open('/root/workspace/SamosaSVNGoogle/data/s'+str(j)+'.csv','w')
    for k in range(0,248):
        f.write(allstrs[j*4+k])
#        allstrs[j*4+k]
    f.close()
    
    