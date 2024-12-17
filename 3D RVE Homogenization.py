

## Importing ABAQUS Data and Python modules ##

from abaqus import *
from abaqusConstants import *
import __main__
import math
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import time
import os
import sys
import ctypes
import multiprocessing


CPUs=4

# mdb.ModelFromInputFile(inputFileName='E:/hypermeshtemp/testtest.inp', name=
#     'testtest')
# del mdb.models['Model-1']
# mdb.models.changeKey(fromName='testtest', toName='Model-1')
# mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='PART-1-1', 
#     toName='Part-1-1')

tolcouple=0.0011 #tol for coupling nodes

tolboundry=0.001  #tol for choosing boundry nodes

modelName = 'Model-1'
instanceName='union-1'

Nodeset = mdb.models[modelName].rootAssembly.instances[instanceName].nodes

a = mdb.models[modelName].rootAssembly
mdb.models[modelName].rootAssembly.regenerate()



## Start of sets creation ##                
j = 0
x=[]
y=[]
z=[]
c1=[]
c2=[]
c3=[]
c4=[]
c5=[]
c6=[]
c7=[]
c8=[]
Max=[]
ftedgexyz={}
btedgexyz={}
fbedgexyz={}
bbedgexyz={}
fledgexyz={}
bledgexyz={}
fredgexyz={}
bredgexyz={}
ltedgexyz={}
rtedgexyz={}
lbedgexyz={}
rbedgexyz={}
frontsxyz={}
backsxyz={}
topsxyz={}
botsxyz={}
leftsxyz={}
rightsxyz={}
frontbcxyz={}
backbcxyz={}
topbcxyz={}
botbcxyz={}
leftbcxyz={}
rightbcxyz={}
ftedge=[]
btedge=[]
fbedge=[]
bbedge=[]
fledge=[]
fredge=[]
bledge=[]
bredge=[]
ltedge=[]
lbedge=[]
rtedge=[]
rbedge=[]
fronts=[]
backs=[]
lefts=[]
rights=[]
tops=[]
bots=[]
backs=[]
frontbc=[]
backbc=[]
leftbc=[]
rightbc=[]
topbc=[]
botbc=[]
backbc=[]
errorset=[]
coc1={}
coc2={}
coc3={}
coc4={}
coc5={}
coc6={}
coc7={}
coc8={}








## Identifying RVE size ##    
for i in Nodeset:
 x.insert(j,i.coordinates[0])
 y.insert(j,i.coordinates[1])
 z.insert(j,i.coordinates[2])
 j=j+1




Max = max(x)
May = max(y)
Maz = max(z)
Mnx = min(x)
Mny = min(y)
Mnz = min(z)


## 3D model ##########################################################
                
L=abs(Max-Mnx)
H=abs(May-Mny)
W=abs(Maz-Mnz)

# Dispx = L*0.2
# Dispy = H*0.2
# Dispz = W*0.2

## Creating Ref. Points ##
for i in a.features.keys():
    if i.startswith('RP'):
        del a.features['%s' % (i)]

a.ReferencePoint(point=(Max+0.8*abs(Max-Mnx), May-0.5*(May-Mny), Maz-0.5*(Maz-Mnz)))  ## RP6: G23
a.ReferencePoint(point=(Max+0.6*abs(Max-Mnx), May-0.5*(May-Mny), Maz-0.5*(Maz-Mnz)))  ## RP5: G13
a.ReferencePoint(point=(Max+0.4*abs(Max-Mnx), May-0.5*(May-Mny), Maz-0.5*(Maz-Mnz)))  ## RP4: G12
a.ReferencePoint(point=(Max+0.2*abs(Max-Mnx), May-0.5*(May-Mny), Maz-0.5*(Maz-Mnz)))  ## RP3: Rigid body movement X-axis
a.ReferencePoint(point=(Max-0.5*(Max-Mnx), May-0.5*(May-Mny), Maz+0.2*abs(Maz-Mnz)))  ## RP2: Rigid body movement Z-axis
a.ReferencePoint(point=(Max-0.5*(Max-Mnx), May+0.2*abs(May-Mny), Maz-0.5*(Maz-Mnz)))  ## RP1: Rigid body movement Y-axis

r1 = a.referencePoints

## Naming Ref. Points ##
d=1
for i in r1.keys():
    refPoints1=(r1[i], )
    a.Set(referencePoints=refPoints1, name='RP%s' % (d))
    d=d+1
  
## Identifying boundary nodes ##

meshsens=tolboundry

for i in Nodeset:
    if (Mnx+meshsens) < i.coordinates[0] < (Max-meshsens) and (Mny+meshsens) < i.coordinates[1] < (May-meshsens) and (Mnz+meshsens) < i.coordinates[2] < (Maz-meshsens):
        continue
    if abs(i.coordinates[0]-Max)<=meshsens:
        frontbcxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[0]-Mnx)<=meshsens:
        backbcxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[2]-Maz)<=meshsens:
        leftbcxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[2]-Mnz)<=meshsens:
        rightbcxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[1]-May)<=meshsens:
        topbcxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[1]-Mny)<=meshsens:
        botbcxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[2]-Maz)<=meshsens:
        c1.insert(0,i.label)
        coc1[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[2]-Maz)<=meshsens:
        c2.insert(0,i.label)
        coc2[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[2]-Mnz)<=meshsens:
        c3.insert(0,i.label)
        coc3[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[2]-Mnz)<=meshsens:
        c4.insert(0,i.label)
        coc4[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[2]-Maz)<=meshsens:
        c5.insert(0,i.label)
        coc5[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[2]-Maz)<=meshsens:
        c6.insert(0,i.label)
        coc6[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[2]-Mnz)<=meshsens:
        c7.insert(0,i.label)
        coc7[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[2]-Mnz)<=meshsens:
        c8.insert(0,i.label)
        coc8[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[2]-Maz)>meshsens and abs(i.coordinates[2]-Mnz)>meshsens:
        ftedgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[2]-Maz)>meshsens and abs(i.coordinates[2]-Mnz)>meshsens:
        fbedgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[2]-Maz)>meshsens and abs(i.coordinates[2]-Mnz)>meshsens:
        btedgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[2]-Maz)>meshsens and abs(i.coordinates[2]-Mnz)>meshsens:
        bbedgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[2]-Maz)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens:
        fledgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[2]-Mnz)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens:
        fredgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[2]-Maz)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens:
        bledgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[2]-Mnz)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens:
        bredgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[2]-Maz)<=meshsens and abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens:
        ltedgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[2]-Maz)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens:
        lbedgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[2]-Mnz)<=meshsens and abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens:
        rtedgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[2]-Mnz)<=meshsens and abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens:
        rbedgexyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[0]-Max)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens and abs(i.coordinates[2]-Maz)>meshsens and abs(i.coordinates[2]-Mnz)>meshsens:
        frontsxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[0]-Mnx)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens and abs(i.coordinates[2]-Maz)>meshsens and abs(i.coordinates[2]-Mnz)>meshsens:
        backsxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]] 
    if abs(i.coordinates[2]-Maz)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens:
        leftsxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]	
    if abs(i.coordinates[2]-Mnz)<=meshsens and abs(i.coordinates[1]-May)>meshsens and abs(i.coordinates[1]-Mny)>meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens:
        rightsxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]   
    if abs(i.coordinates[1]-May)<=meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens and abs(i.coordinates[2]-Maz)>meshsens and abs(i.coordinates[2]-Mnz)>meshsens:
        topsxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]
    if abs(i.coordinates[1]-Mny)<=meshsens and abs(i.coordinates[0]-Max)>meshsens and abs(i.coordinates[0]-Mnx)>meshsens and abs(i.coordinates[2]-Maz)>meshsens and abs(i.coordinates[2]-Mnz)>meshsens:
        botsxyz[i.label]=[i.coordinates[0], i.coordinates[1], i.coordinates[2]]

# ## Checking number of nodes of opposite/associated sets ##
# if len(frontsxyz) != len(backsxyz):
#  print 'Warning: Number of Nodes in Front surface (fronts) not equal to number of nodes in Back surface (backs). These sets will not be created!!'
#  print '         Refer to error 06 troubleshooting in easyPBC user guide.'
#  frontsxyz={}
#  error=True
# if len(topsxyz) != len(botsxyz):
#  print 'Warning: Number of Nodes in Top surface (tops) not equal to number of nodes in Bottom surface (bots). These sets will not be created!!'
#  print '         Refer to error 06 in easyPBC user guide.'
#  topsxyz={}
#  error=True
# if len(leftsxyz) != len(rightsxyz):
#  print 'Warning: Number of Nodes in Left surface (lefts) not equal to number of nodes in Right surface (rights). These sets will not be created!!'
#  print '         Refer to error 06 in easyPBC user guide.'
#  leftsxyz={}
#  error=True
# if len(ftedgexyz) != len(btedgexyz) or len(btedgexyz) != len(bbedgexyz) or len(bbedgexyz) != len(ftedgexyz):
#  print 'Warning: Number of nodes in front-top ,back-top, back-bottom, front-bottom (ftedge, btedge, bbedge and fbedge) are not equal. These sets will not be created!!'
#  print '         Refer to error 06 in easyPBC user guide.'
#  ftedgexyz={}
#  error=True
# if len(fledgexyz) != len(bledgexyz) or len(bledgexyz) != len(bredgexyz) or len(bredgexyz) != len(fredgexyz):
#  print 'Warning: Number of nodes in front-left, back-left, back-right, front-right edge (fledge, bledge, bredge and fredge) are not equal. These sets will not be created!!'
#  print '         Refer to error 06 in easyPBC user guide.'
#  fledgexyz={}
#  error=True
# if len(ltedgexyz) != len(rtedgexyz) or len(rtedgexyz) != len(rbedgexyz) or len(rbedgexyz) != len(lbedgexyz):
#  print 'Warning: Number of nodes in left-top, right-top, right-bottom, front-bottom edge (ltedge, rtedge, rbedge and fbedge). are not equal. These sets will not be created!!'
#  print '         Refer to error 06 in easyPBC user guide.'
#  ltedgexyz={}
#  error=True
# if len(frontbcxyz) != len(backbcxyz):
#  print 'Warning: Number of Nodes in Front BC surface (frontbc) not equal to number of nodes in Back BC surface (backbc). These sets will not be created!!'
#  print '         Refer to error 06 troubleshooting in easyPBC user guide.'
#  frontbcxyz={}
#  error=True
# if len(topbcxyz) != len(botbcxyz):
#  print 'Warning: Number of Nodes in Top BC surface (topbc) not equal to number of nodes in Bottom BC surface (botbc). These sets will not be created!!'
#  print '         Refer to error 06 in easyPBC user guide.'
#  topbcxyz={}
#  error=True
# if len(leftbcxyz) != len(rightbcxyz):
#  print 'Warning: Number of Nodes in Left BC surface (leftbc) not equal to number of nodes in Right BC surface (rightbc). These sets will not be created!!'
#  print '         Refer to error 06 in easyPBC user guide.'
#  leftbcxyz={}
#  error=True

## Sorting and appending sets ##

meshsens=tolcouple

for i in frontsxyz.keys():
    for k in backsxyz.keys():
            if abs(frontsxyz[i][1] - backsxyz[k][1])<=meshsens and abs(frontsxyz[i][2] - backsxyz[k][2])<=meshsens:
                    fronts.append(i)
                    backs.append(k)

# if len(frontsxyz)!= len(fronts) or len(backsxyz)!= len(backs):
# print 'Warning: Node(s) in Front and/or Back surface (fronts and/or backs) was not imported. effected sets will not be created!!'
# print '         Refer to error 07 in easyPBC user guide and created Error set (if applicable).'
# for i, k in zip(frontsxyz.keys(),backsxyz.keys()):
#         if i not in fronts:
#                 errorset.append(i)
#         if k not in backs:
#                 errorset.append(k)
# fronts=[]
# backs=[]
# error=True                    
# if len(fronts)!=len(set(fronts)) or len(backs)!=len(set(backs)):
# print 'Warning: Node(s) in either Front or Back surface (fronts or backs) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# fronts=[]
# backs=[]
# error=True

for i in topsxyz.keys():
 for k in botsxyz.keys():
    if abs(topsxyz[i][0] - botsxyz[k][0]) <=meshsens and abs(topsxyz[i][2] - botsxyz[k][2]) <=meshsens:
        tops.append(i)
        bots.append(k)
# if len(topsxyz)!= len(tops) or len(botsxyz)!= len(bots):
# print 'Warning: Node(s) in Top and/or Bottom surface (tops and/or bots) was not imported. effected sets will not be created!!'
# print '         Refer to error 07 in easyPBC user guide and created Error set (if applicable).'
# for i, k in zip(topsxyz.keys(),botsxyz.keys()):
#         if i not in tops:
#                 errorset.append(i)
#         if k not in bots:
#                 errorset.append(k)
# tops=[]
# bots=[]
# error=True
# if len(tops)!=len(set(tops)) or len(bots)!=len(set(bots)):
# print 'Warning: Node(s) in either Top or Bottom surface (tops or bots) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# tops=[]
# bots=[]
# error=True


for i in leftsxyz.keys():
 for k in rightsxyz.keys():
    if abs(leftsxyz[i][0] - rightsxyz[k][0])<=meshsens and abs(leftsxyz[i][1] - rightsxyz[k][1]) <=meshsens:
        lefts.append(i)
        rights.append(k)
# if len(leftsxyz)!= len(lefts) or len(rightsxyz)!= len(rights):
# print 'Warning: Node(s) in Left and/or Right surface (lefts and/or rights) was not imported. effected sets will not be created!!'
# print '         Refer to error 07 in easyPBC user guide and created Error set (if applicable).'
# for i, k in zip(leftsxyz.keys(),rightsxyz.keys()):
#         if i not in lefts:
#                 errorset.append(i)
#         if k not in rights:
#                 errorset.append(k)                    
# lefts=[]
# rights=[]
# error=True                    
# if len(lefts)!=len(set(lefts)) or len(rights)!=len(set(rights)):
# print 'Warning: Node(s) in either Left or Right surface (lefts or rights) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# lefts=[]
# rights=[]
# error=True

for i in frontbcxyz.keys():
 for k in backbcxyz.keys():
    if abs(frontbcxyz[i][1] - backbcxyz[k][1])<=meshsens and abs(frontbcxyz[i][2] - backbcxyz[k][2])<=meshsens:
        frontbc.append(i)
        backbc.append(k)
# if len(frontbcxyz)!= len(frontbc) or len(backbcxyz)!= len(backbc):
# print 'Warning: Node(s) in Front BC and/or Back BC surface (frontbc and/or backbc) was not imported. effected sets will not be created!!'
# print '         Refer to error 07 in easyPBC user guide and created Error set (if applicable).'
# for i, k in zip(frontbcxyz.keys(),backbcxyz.keys()):
#         if i not in frontbc:
#                 errorset.append(i)
#         if k not in backbc:
#                 errorset.append(k)
# frontbc=[]
# backbc=[]
# error=True
# if len(frontbc)!=len(set(frontbc)) or len(backbc)!=len(set(backbc)):
# print 'Warning: Node(s) in either Front BC or Back BC surface (frontbc or backbc) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# frontbc=[]
# backbc=[]
# error=True


for i in topbcxyz.keys():
 for k in botbcxyz.keys():
    if abs(topbcxyz[i][0] - botbcxyz[k][0]) <=meshsens and abs(topbcxyz[i][2] - botbcxyz[k][2]) <=meshsens:
        topbc.append(i)
        botbc.append(k)
# if len(topbcxyz)!= len(topbc) or len(botbcxyz)!= len(botbc):
# print 'Warning: Node(s) in Top BC and/or Bottom BC surface (topbc and/or botbc) was not imported. effected sets will not be created!!'
# print '         Refer to error 07 in easyPBC user guide and created Error set (if applicable).'
# for i, k in zip(topbcxyz.keys(),botbcxyz.keys()):
#         if i not in topbc:
#                 errorset.append(i)
#         if k not in botbc:
#                 errorset.append(k)
# topbc=[]
# botbc=[]
# error=True
# if len(topbc)!=len(set(topbc)) or len(botbc)!=len(set(botbc)):
# print 'Warning: Node(s) in either Top BC or Bottom BC surface (topbc or botbc) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# topbc=[]
# botbc=[]
# error=True


for i in leftbcxyz.keys():
 for k in rightbcxyz.keys():
    if abs(leftbcxyz[i][0] - rightbcxyz[k][0])<=meshsens and abs(leftbcxyz[i][1] - rightbcxyz[k][1]) <=meshsens:
        leftbc.append(i)
        rightbc.append(k)
# if len(leftbcxyz)!= len(leftbc) or len(rightbcxyz)!= len(rightbc):
# print 'Warning: Node(s) in Left BC and/or Right BC surface (lefts and/or rights) was not imported. effected sets will not be created!!'
# print '         Refer to error 07 in easyPBC user guide and created Error set (if applicable).'
# for i, k in zip(leftbcxyz.keys(),rightbcxyz.keys()):
#         if i not in leftbc:
#                 errorset.append(i)
#         if k not in rightbc:
#                 errorset.append(k)            
# leftbc=[]
# rightbc=[]
# error=True
# if len(leftbc)!=len(set(leftbc)) or len(rightbc)!=len(set(rightbc)):
# print 'Warning: Node(s) in either Left BC or Right BC surface (leftbc or rightbc) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# leftbc=[]
# rightbc=[]
# error=True


for i in ftedgexyz.keys():
 for k in btedgexyz.keys():
    if abs(ftedgexyz[i][1] - btedgexyz[k][1])<=meshsens and abs(ftedgexyz[i][2] - btedgexyz[k][2])<=meshsens:
        ftedge.append(i)
        btedge.append(k)
for i in btedge:
 for k in bbedgexyz.keys():
    if abs(btedgexyz[i][0] - bbedgexyz[k][0]) <=meshsens and abs(btedgexyz[i][2] - bbedgexyz[k][2]) <=meshsens:
        bbedge.append(k)    
for i in bbedge:
 for k in fbedgexyz.keys():
    if abs(bbedgexyz[i][1] - fbedgexyz[k][1]) <=meshsens and abs(bbedgexyz[i][2] - fbedgexyz[k][2]) <=meshsens:
        fbedge.append(k) 
# if len(ftedge)!=len(set(ftedge)) or len(btedge)!=len(set(btedge)) or len(bbedge)!=len(set(bbedge)) or len(fbedge)!=len(set(fbedge)):
# print 'Warning: Node(s) in either front-top, back-top, back-bottom and front-bottom edge(ftedge, btedge, bbedge and fbedge) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# ftedge=[]
# btedge=[]
# bbedg=[]
# fbedge=[]
# error==True
# if len(ftedgexyz)!= len(ftedge) or len(btedgexyz)!= len(btedge) or len(bbedgexyz)!= len(bbedge) or len(fbedgexyz)!= len(fbedge):
# print 'Warning: Node(s) in front-top, back-top, back-bottom and front-bottom edge(ftedge, btedge, bbedge and fbedge) were not imported. these sets will not be created!!'
# print '         Refer to error 07 in easyPBC user guide and created Error set (if applicable).'
# ftedge=[]
# btedge=[]
# bbedg=[]
# fbedge=[]
# error=True

for i in ltedgexyz.keys():
 for k in rtedgexyz.keys():
    if abs(ltedgexyz[i][0] - rtedgexyz[k][0])<=meshsens and abs(ltedgexyz[i][1] - rtedgexyz[k][1])<=meshsens:
        ltedge.append(i)
        rtedge.append(k)
for i in rtedge:
 for k in rbedgexyz.keys():
    if abs(rtedgexyz[i][0] - rbedgexyz[k][0])<=meshsens and abs(rtedgexyz[i][2] - rbedgexyz[k][2])<=meshsens:
        rbedge.append(k)    
for i in rbedge:
 for k in lbedgexyz.keys():
    if abs(rbedgexyz[i][0] - lbedgexyz[k][0])<=meshsens and abs(rbedgexyz[i][1] - lbedgexyz[k][1])<=meshsens:
        lbedge.append(k) 

# if len(ltedge)!=len(set(ltedge)) or len(rtedge)!=len(set(rtedge)) or len(rbedge)!=len(set(rbedge)) or len(lbedge)!=len(set(lbedge)):
# print 'Warning: Node(s) in either front-top, back-bottom and front-bottom edge(ltedge, rtedge, rbedge and lbedge) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# ltedge=[]
# rtedge=[]
# rbedg=[]
# lbedge=[]
# error=True

# if len(ltedgexyz)!= len(ltedge) or len(rtedgexyz)!= len(rtedge) or len(rbedgexyz)!= len(rbedge) or len(lbedgexyz)!= len(lbedge):
# print 'Warning: Node(s) in left-top, right-top, right-bottom, left-bottom edge (ltedge, rtedge, rbedge and lbedge) were not imported. these sets will not be created!!'
# print '         Refer to error 07 in easyPBC user guide and created Error set (if applicable).'
# ltedge=[]
# rtedge=[]
# rbedg=[]
# lbedge=[]
# error=True

for i in fledgexyz.keys():
 for k in bledgexyz.keys():
    if abs(fledgexyz[i][1] - bledgexyz[k][1])<=meshsens and abs(fledgexyz[i][2] - bledgexyz[k][2])<=meshsens:
        fledge.append(i)
        bledge.append(k)
for i in bledge:
 for k in bredgexyz.keys():
    if abs(bledgexyz[i][0] - bredgexyz[k][0])<=meshsens and abs(bledgexyz[i][1] - bredgexyz[k][1])<=meshsens:
        bredge.append(k)    
for i in bredge:
 for k in fredgexyz.keys():
    if abs(bredgexyz[i][1] - fredgexyz[k][1])<=meshsens and abs(bredgexyz[i][2] - fredgexyz[k][2])<=meshsens:
        fredge.append(k) 

# if len(fledge)!=len(set(fledge)) or len(bledge)!=len(set(bledge)) or len(bredge)!=len(set(bredge)) or len(fredge)!=len(set(fredge)):
# print 'Warning: Node(s) in either front-left, back-left, back-right and front-right edge(fledge, bledge, bredge and fredge) being linked with more than one opposite node. effected sets will not be created!!'
# print '         Refer to error 08 in easyPBC user guide.'
# fledge=[]
# bledge=[]
# bredg=[]
# fredge=[]
# error=True
# if len(fledgexyz)!= len(fledge) or len(bledgexyz)!= len(bledge) or len(bredgexyz)!= len(bredge) or len(fredgexyz)!= len(fredge):
# print 'Warning: Node(s) in front-left, back-left, back-right and front-right edge (fledge, bledge, bredge and fredge) were not imported. these sets will not be created!!'
# print '         Refer to error 07 in easyPBC user user guide.'
# fledge=[]
# bledge=[]
# bredg=[]
# fredge=[]
# error=True

## Creating ABAQUS sets ##
a.SetFromNodeLabels(name='c1', nodeLabels=((instanceName,c1),))
a.SetFromNodeLabels(name='c2', nodeLabels=((instanceName,c2),))
a.SetFromNodeLabels(name='c3', nodeLabels=((instanceName,c3),))
a.SetFromNodeLabels(name='c4', nodeLabels=((instanceName,c4),))
a.SetFromNodeLabels(name='c5', nodeLabels=((instanceName,c5),))
a.SetFromNodeLabels(name='c6', nodeLabels=((instanceName,c6),))
a.SetFromNodeLabels(name='c7', nodeLabels=((instanceName,c7),))
a.SetFromNodeLabels(name='c8', nodeLabels=((instanceName,c8),))
a.SetFromNodeLabels(name='ftedge', nodeLabels=((instanceName,ftedge),))
a.SetFromNodeLabels(name='fbedge', nodeLabels=((instanceName,fbedge),))
a.SetFromNodeLabels(name='btedge', nodeLabels=((instanceName,btedge),))
a.SetFromNodeLabels(name='bbedge', nodeLabels=((instanceName,bbedge),))
a.SetFromNodeLabels(name='fledge', nodeLabels=((instanceName,fledge),))
a.SetFromNodeLabels(name='fredge', nodeLabels=((instanceName,fredge),))
a.SetFromNodeLabels(name='bledge', nodeLabels=((instanceName,bledge),))
a.SetFromNodeLabels(name='bredge', nodeLabels=((instanceName,bredge),))
a.SetFromNodeLabels(name='ltedge', nodeLabels=((instanceName,ltedge),))
a.SetFromNodeLabels(name='lbedge', nodeLabels=((instanceName,lbedge),))
a.SetFromNodeLabels(name='rtedge', nodeLabels=((instanceName,rtedge),))
a.SetFromNodeLabels(name='rbedge', nodeLabels=((instanceName,rbedge),))
a.SetFromNodeLabels(name='fronts', nodeLabels=((instanceName,fronts),))
a.SetFromNodeLabels(name='backs', nodeLabels=((instanceName,backs),))
a.SetFromNodeLabels(name='lefts', nodeLabels=((instanceName,lefts),))
a.SetFromNodeLabels(name='rights', nodeLabels=((instanceName,rights),))
a.SetFromNodeLabels(name='tops', nodeLabels=((instanceName,tops),))
a.SetFromNodeLabels(name='bots', nodeLabels=((instanceName,bots),))
a.SetFromNodeLabels(name='frontbc', nodeLabels=((instanceName,frontbc),))
a.SetFromNodeLabels(name='backbc', nodeLabels=((instanceName,backbc),))
a.SetFromNodeLabels(name='leftbc', nodeLabels=((instanceName,leftbc),))
a.SetFromNodeLabels(name='rightbc', nodeLabels=((instanceName,rightbc),))
a.SetFromNodeLabels(name='topbc', nodeLabels=((instanceName,topbc),))
a.SetFromNodeLabels(name='botbc', nodeLabels=((instanceName,botbc),))
print ('------ End of Sets Creation ------')

## Extracting model mass ##
prop=mdb.models[modelName].rootAssembly.getMassProperties()
mass=prop['mass']

a = mdb.models[modelName].rootAssembly
Nodeset = mdb.models[modelName].rootAssembly.instances[instanceName].nodes
mdb.models[modelName].StaticStep(name='Step-1', previous='Initial')
mdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'E', 'EE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 'EVOL'))

## Creating single-node ABAQUS sets ##                

for i,k in zip(tops,bots):
    a.SetFromNodeLabels(name='tops%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='bots%s' % (k), nodeLabels=((instanceName,[k]),))




for i,k in zip(fronts,backs):
    a.SetFromNodeLabels(name='fronts%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='backs%s' % (k), nodeLabels=((instanceName,[k]),))




for i,k in zip(lefts,rights):
    a.SetFromNodeLabels(name='lefts%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='rights%s' % (k), nodeLabels=((instanceName,[k]),))





for i,k,j,l in zip(ftedge,btedge,bbedge,fbedge):
    a.SetFromNodeLabels(name='ftedge%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='btedge%s' % (k), nodeLabels=((instanceName,[k]),))
    a.SetFromNodeLabels(name='bbedge%s' % (j), nodeLabels=((instanceName,[j]),))
    a.SetFromNodeLabels(name='fbedge%s' % (l), nodeLabels=((instanceName,[l]),))




for i,k,j,l in zip(fledge,bledge,bredge,fredge):
    a.SetFromNodeLabels(name='fledge%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='bledge%s' % (k), nodeLabels=((instanceName,[k]),))
    a.SetFromNodeLabels(name='bredge%s' % (j), nodeLabels=((instanceName,[j]),))
    a.SetFromNodeLabels(name='fredge%s' % (l), nodeLabels=((instanceName,[l]),))





for i,k,j,l in zip(ltedge,lbedge,rbedge,rtedge):
    a.SetFromNodeLabels(name='ltedge%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='lbedge%s' % (k), nodeLabels=((instanceName,[k]),))
    a.SetFromNodeLabels(name='rbedge%s' % (j), nodeLabels=((instanceName,[j]),))
    a.SetFromNodeLabels(name='rtedge%s' % (l), nodeLabels=((instanceName,[l]),))




for i,k in zip(topbc,botbc):
    a.SetFromNodeLabels(name='topbc%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='botbc%s' % (k), nodeLabels=((instanceName,[k]),))




for i,k in zip(frontbc,backbc):
    a.SetFromNodeLabels(name='frontbc%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='backbc%s' % (k), nodeLabels=((instanceName,[k]),))





for i,k in zip(leftbc,rightbc):
    a.SetFromNodeLabels(name='leftbc%s' % (i), nodeLabels=((instanceName,[i]),))
    a.SetFromNodeLabels(name='rightbc%s' % (k), nodeLabels=((instanceName,[k]),))

print ('------ End of Creating single-node ABAQUS sets ------')

## Creating constraints  ##
                       
for i in mdb.models[modelName].constraints.keys():
        del mdb.models[modelName].constraints[i]

for i,k in zip(tops,bots):
    mdb.models[modelName].Equation(name='G-1-tops-bots%s'%i, terms=((1.0, 'tops%s'%i, 1), (-1.0, 'bots%s'%k, 1),(-1.0, 'RP4', 1)))
for i,k in zip(tops,bots):
    mdb.models[modelName].Equation(name='G-2-tops-bots%s'%i, terms=((1.0, 'tops%s'%i, 2), (-1.0, 'bots%s'%k, 2),(-1.0, 'RP1', 2)))
for i,k in zip(tops,bots):
    mdb.models[modelName].Equation(name='G-3-tops-bots%s'%i, terms=((1.0, 'tops%s'%i, 3), (-1.0, 'bots%s'%k, 3),(-1.0, 'RP6', 3)))

   
for i,k in zip(lefts,rights):
    mdb.models[modelName].Equation(name='G-1-lefts-rights%s'%i, terms=((1.0, 'lefts%s'%i, 1), (-1.0, 'rights%s'%k, 1),(-1.0, 'RP5', 1)))
for i,k in zip(lefts,rights):
    mdb.models[modelName].Equation(name='G-2-lefts-rights%s'%i, terms=((1.0, 'lefts%s'%i, 2), (-1.0, 'rights%s'%k, 2),(-1.0, 'RP6', 2)))
for i,k in zip(lefts,rights):
    mdb.models[modelName].Equation(name='G-3-lefts-rights%s'%i, terms=((1.0, 'lefts%s'%i, 3), (-1.0, 'rights%s'%k, 3),(-1.0, 'RP2', 3)))

for i,k in zip(fronts,backs):
    mdb.models[modelName].Equation(name='G-1-fronts-backs%s'%i, terms=((1.0, 'fronts%s'%i, 1), (-1.0, 'backs%s'%k, 1),(-1.0, 'RP3', 1)))
for i,k in zip(fronts,backs):
    mdb.models[modelName].Equation(name='G-2-fronts-backs%s'%i, terms=((1.0, 'fronts%s'%i, 2), (-1.0, 'backs%s'%k, 2),(-1.0, 'RP4', 2)))
for i,k in zip(fronts,backs):
    mdb.models[modelName].Equation(name='G-3-fronts-backs%s'%i, terms=((1.0, 'fronts%s'%i, 3), (-1.0, 'backs%s'%k, 3),(-1.0, 'RP5', 3)))


mdb.models[modelName].Equation(name='G-1-c12', terms=((1.0, 'c6', 1), (-1.0, 'c2', 1),(1.0, 'RP4', 1)))
mdb.models[modelName].Equation(name='G-1-c23', terms=((1.0, 'c2', 1), (-1.0, 'c3', 1),(-1.0, 'RP5', 1)))
mdb.models[modelName].Equation(name='G-1-c34', terms=((1.0, 'c3', 1), (-1.0, 'c4', 1),(1.0, 'RP3', 1)))
mdb.models[modelName].Equation(name='G-1-c45', terms=((1.0, 'c4', 1), (-1.0, 'c8', 1),(-1.0, 'RP4', 1)))
mdb.models[modelName].Equation(name='G-1-c56', terms=((1.0, 'c8', 1), (-1.0, 'c5', 1),(1.0, 'RP5', 1)))
mdb.models[modelName].Equation(name='G-1-c67', terms=((1.0, 'c5', 1), (-1.0, 'c1', 1),(1.0, 'RP4', 1)))
mdb.models[modelName].Equation(name='G-1-c78', terms=((1.0, 'c1', 1), (-1.0, 'c7', 1),(-1.0, 'RP3', 1),(-1.0, 'RP4', 1),(-1.0, 'RP5', 1)))

    
mdb.models[modelName].Equation(name='G-2-c12', terms=((1.0, 'c6', 2), (-1.0, 'c2', 2),(1.0, 'RP1', 2)))
mdb.models[modelName].Equation(name='G-2-c23', terms=((1.0, 'c2', 2), (-1.0, 'c3', 2),(-1.0, 'RP6', 2)))
mdb.models[modelName].Equation(name='G-2-c34', terms=((1.0, 'c3', 2), (-1.0, 'c4', 2),(1.0, 'RP4', 2)))
mdb.models[modelName].Equation(name='G-2-c45', terms=((1.0, 'c4', 2), (-1.0, 'c8', 2),(-1.0, 'RP1', 2)))
mdb.models[modelName].Equation(name='G-2-c56', terms=((1.0, 'c8', 2), (-1.0, 'c5', 2),(1.0, 'RP6', 2)))
mdb.models[modelName].Equation(name='G-2-c67', terms=((1.0, 'c5', 2), (-1.0, 'c1', 2),(1.0, 'RP1', 2)))
mdb.models[modelName].Equation(name='G-2-c78', terms=((1.0, 'c1', 2), (-1.0, 'c7', 2),(-1.0, 'RP1', 2),(-1.0, 'RP4', 2),(-1.0, 'RP6', 2)))


mdb.models[modelName].Equation(name='G-3-c12', terms=((1.0, 'c6', 3), (-1.0, 'c2', 3),(1.0, 'RP6', 3)))
mdb.models[modelName].Equation(name='G-3-c23', terms=((1.0, 'c2', 3), (-1.0, 'c3', 3),(-1.0, 'RP2', 3)))
mdb.models[modelName].Equation(name='G-3-c34', terms=((1.0, 'c3', 3), (-1.0, 'c4', 3),(1.0, 'RP5', 3)))
mdb.models[modelName].Equation(name='G-3-c45', terms=((1.0, 'c4', 3), (-1.0, 'c8', 3),(-1.0, 'RP6', 3)))
mdb.models[modelName].Equation(name='G-3-c56', terms=((1.0, 'c8', 3), (-1.0, 'c5', 3),(1.0, 'RP2', 3)))
mdb.models[modelName].Equation(name='G-3-c67', terms=((1.0, 'c5', 3), (-1.0, 'c1', 3),(1.0, 'RP6', 3)))
mdb.models[modelName].Equation(name='G-3-c78', terms=((1.0, 'c1', 3), (-1.0, 'c7', 3),(-1.0, 'RP2', 3),(-1.0, 'RP5', 3),(-1.0, 'RP6', 3)))
 

for i,k,j,l in zip(ftedge,btedge,bbedge,fbedge):
    mdb.models[modelName].Equation(name='G-1-ftedge-btedge%s'%i, terms=((1.0, 'ftedge%s'%i, 1), (-1.0, 'btedge%s'%k, 1),(-1.0, 'RP3', 1)))
    mdb.models[modelName].Equation(name='G-1-btedge-bbedge%s'%k, terms=((1.0, 'btedge%s'%k, 1), (-1.0, 'bbedge%s'%j, 1),(-1.0, 'RP4', 1)))
    mdb.models[modelName].Equation(name='G-1-bbedge-fbedge%s'%j, terms=((1.0, 'bbedge%s'%j, 1), (-1.0, 'fbedge%s'%l, 1),(1.0, 'RP3', 1)))
for i,k,j,l in zip(ftedge,btedge,bbedge,fbedge):
    mdb.models[modelName].Equation(name='G-2-ftedge-btedge%s'%i, terms=((1.0, 'ftedge%s'%i, 2), (-1.0, 'btedge%s'%k, 2),(-1.0, 'RP4', 2)))
    mdb.models[modelName].Equation(name='G-2-btedge-bbedge%s'%k, terms=((1.0, 'btedge%s'%k, 2), (-1.0, 'bbedge%s'%j, 2),(-1.0, 'RP1', 2)))
    mdb.models[modelName].Equation(name='G-2-bbedge-fbedge%s'%j, terms=((1.0, 'bbedge%s'%j, 2), (-1.0, 'fbedge%s'%l, 2),(1.0, 'RP4', 2)))
for i,k,j,l in zip(ftedge,btedge,bbedge,fbedge):
    mdb.models[modelName].Equation(name='G-3-ftedge-btedge%s'%i, terms=((1.0, 'ftedge%s'%i, 3), (-1.0, 'btedge%s'%k, 3),(-1.0, 'RP5', 3)))
    mdb.models[modelName].Equation(name='G-3-btedge-bbedge%s'%k, terms=((1.0, 'btedge%s'%k, 3), (-1.0, 'bbedge%s'%j, 3),(-1.0, 'RP6', 3)))
    mdb.models[modelName].Equation(name='G-3-bbedge-fbedge%s'%j, terms=((1.0, 'bbedge%s'%j, 3), (-1.0, 'fbedge%s'%l, 3),(1.0, 'RP5', 3)))


for i,k,j,l in zip(fledge,bledge,bredge,fredge):
    mdb.models[modelName].Equation(name='G-1-fledge-bledge%s'%i, terms=((1.0, 'fledge%s'%i, 1), (-1.0, 'bledge%s'%k, 1),(-1.0, 'RP3', 1)))
    mdb.models[modelName].Equation(name='G-1-bledge-bredge%s'%k, terms=((1.0, 'bledge%s'%k, 1), (-1.0, 'bredge%s'%j, 1),(-1.0, 'RP5', 1)))
    mdb.models[modelName].Equation(name='G-1-bredge-fredge%s'%j, terms=((1.0, 'bredge%s'%j, 1), (-1.0, 'fredge%s'%l, 1),(1.0, 'RP3', 1)))
for i,k,j,l in zip(fledge,bledge,bredge,fredge):
    mdb.models[modelName].Equation(name='G-2-fledge-bledge%s'%i, terms=((1.0, 'fledge%s'%i, 2), (-1.0, 'bledge%s'%k, 2),(-1.0, 'RP4', 2)))
    mdb.models[modelName].Equation(name='G-2-bledge-bredge%s'%k, terms=((1.0, 'bledge%s'%k, 2), (-1.0, 'bredge%s'%j, 2),(-1.0, 'RP6', 2)))
    mdb.models[modelName].Equation(name='G-2-bredge-fredge%s'%j, terms=((1.0, 'bredge%s'%j, 2), (-1.0, 'fredge%s'%l, 2),(1.0, 'RP4', 2)))
for i,k,j,l in zip(fledge,bledge,bredge,fredge):
    mdb.models[modelName].Equation(name='G-3-fledge-bledge%s'%i, terms=((1.0, 'fledge%s'%i, 3), (-1.0, 'bledge%s'%k, 3),(-1.0, 'RP5', 3)))
    mdb.models[modelName].Equation(name='G-3-bledge-bredge%s'%k, terms=((1.0, 'bledge%s'%k, 3), (-1.0, 'bredge%s'%j, 3),(-1.0, 'RP2', 3)))
    mdb.models[modelName].Equation(name='G-3-bredge-fredge%s'%j, terms=((1.0, 'bredge%s'%j, 3), (-1.0, 'fredge%s'%l, 3),(1.0, 'RP5', 3)))
    

for i,k,j,l in zip(ltedge,lbedge,rbedge,rtedge):
    mdb.models[modelName].Equation(name='G-1-ltedge-lbedge%s'%i, terms=((1.0, 'ltedge%s'%i, 1), (-1.0, 'lbedge%s'%k, 1),(-1.0, 'RP4', 1)))
    mdb.models[modelName].Equation(name='G-1-lbtedge-rbedge%s'%k, terms=((1.0, 'lbedge%s'%k, 1), (-1.0, 'rbedge%s'%j, 1),(-1.0, 'RP5', 1)))
    mdb.models[modelName].Equation(name='G-1-rbedge-rtbedge%s'%j, terms=((1.0, 'rbedge%s'%j, 1), (-1.0, 'rtedge%s'%l, 1),(1.0, 'RP4', 1)))                                    
for i,k,j,l in zip(ltedge,lbedge,rbedge,rtedge):
    mdb.models[modelName].Equation(name='G-2-ltedge-lbedge%s'%i, terms=((1.0, 'ltedge%s'%i, 2), (-1.0, 'lbedge%s'%k, 2),(-1.0, 'RP1', 2)))
    mdb.models[modelName].Equation(name='G-2-lbtedge-rbedge%s'%k, terms=((1.0, 'lbedge%s'%k, 2), (-1.0, 'rbedge%s'%j, 2),(-1.0, 'RP6', 2)))
    mdb.models[modelName].Equation(name='G-2-rbedge-rtbedge%s'%j, terms=((1.0, 'rbedge%s'%j, 2), (-1.0, 'rtedge%s'%l, 2),(1.0, 'RP1', 2)))
for i,k,j,l in zip(ltedge,lbedge,rbedge,rtedge):
    mdb.models[modelName].Equation(name='G-3-ltedge-lbedge%s'%i, terms=((1.0, 'ltedge%s'%i, 3), (-1.0, 'lbedge%s'%k, 3),(-1.0, 'RP6', 3)))
    mdb.models[modelName].Equation(name='G-3-lbtedge-rbedge%s'%k, terms=((1.0, 'lbedge%s'%k, 3), (-1.0, 'rbedge%s'%j, 3),(-1.0, 'RP2', 3)))
    mdb.models[modelName].Equation(name='G-3-rbedge-rtbedge%s'%j, terms=((1.0, 'rbedge%s'%j, 3), (-1.0, 'rtedge%s'%l, 3),(1.0, 'RP6', 3)))

print ('------ End of equations Creation ------')

## C11: C11 to C61 ##
                        
for i in mdb.models[modelName].loads.keys():
        del mdb.models[modelName].loads[i]


for i in mdb.models[modelName].boundaryConditions.keys():
        del mdb.models[modelName].boundaryConditions[i]


region = a.sets['RP1']
mdb.models[modelName].DisplacementBC(name='C11-1', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP2']
mdb.models[modelName].DisplacementBC(name='C11-2', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP3']
mdb.models[modelName].DisplacementBC(name='C11-3', createStepName='Step-1', 
    region=region, u1=1, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP4']
mdb.models[modelName].DisplacementBC(name='C11-4', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP5']
mdb.models[modelName].DisplacementBC(name='C11-5', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP6']
mdb.models[modelName].DisplacementBC(name='C11-6', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

regionDef=mdb.models[modelName].rootAssembly.sets['c1']
mdb.models[modelName].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Step-1', variables=('RT', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

import os, glob

mdb.Job(name='job-C11', model= modelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=CPUs, numDomains=CPUs, numGPUs=0)
mdb.jobs['job-C11'].submit(consistencyChecking=OFF)

mdb.jobs['job-C11'].waitForCompletion()



#-----------------------------------------------------------------------------------------------------------------
## C22: C12 to C62 ##

for i in mdb.models[modelName].loads.keys():
        del mdb.models[modelName].loads[i]


for i in mdb.models[modelName].boundaryConditions.keys():
        del mdb.models[modelName].boundaryConditions[i]


region = a.sets['RP1']
mdb.models[modelName].DisplacementBC(name='C22-1', createStepName='Step-1', 
    region=region, u1=0, u2=1, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP2']
mdb.models[modelName].DisplacementBC(name='C22-2', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP3']
mdb.models[modelName].DisplacementBC(name='C22-3', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP4']
mdb.models[modelName].DisplacementBC(name='C22-4', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP5']
mdb.models[modelName].DisplacementBC(name='C22-5', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP6']
mdb.models[modelName].DisplacementBC(name='C22-6', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

regionDef=mdb.models[modelName].rootAssembly.sets['c1']
mdb.models[modelName].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Step-1', variables=('RT', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

import os, glob

mdb.Job(name='job-C22', model= modelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=CPUs, numDomains=CPUs, numGPUs=0)
mdb.jobs['job-C22'].submit(consistencyChecking=OFF)

mdb.jobs['job-C22'].waitForCompletion()







## C33: C13 to C63 ########################----------------------------------------------------------------------------

for i in mdb.models[modelName].loads.keys():
        del mdb.models[modelName].loads[i]


for i in mdb.models[modelName].boundaryConditions.keys():
        del mdb.models[modelName].boundaryConditions[i]


region = a.sets['RP1']
mdb.models[modelName].DisplacementBC(name='C33-1', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP2']
mdb.models[modelName].DisplacementBC(name='C33-2', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=1, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP3']
mdb.models[modelName].DisplacementBC(name='C33-3', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP4']
mdb.models[modelName].DisplacementBC(name='C33-4', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP5']
mdb.models[modelName].DisplacementBC(name='C33-5', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP6']
mdb.models[modelName].DisplacementBC(name='C33-6', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

regionDef=mdb.models[modelName].rootAssembly.sets['c1']
mdb.models[modelName].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Step-1', variables=('RT', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

import os, glob

mdb.Job(name='job-C33', model= modelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=CPUs, numDomains=CPUs, numGPUs=0)
mdb.jobs['job-C33'].submit(consistencyChecking=OFF)

mdb.jobs['job-C33'].waitForCompletion()



## C44: C14 to C64 ##---------------------------------------------------


for i in mdb.models[modelName].loads.keys():
        del mdb.models[modelName].loads[i]


for i in mdb.models[modelName].boundaryConditions.keys():
        del mdb.models[modelName].boundaryConditions[i]


region = a.sets['RP1']
mdb.models[modelName].DisplacementBC(name='C44-1', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP2']
mdb.models[modelName].DisplacementBC(name='C44-2', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP3']
mdb.models[modelName].DisplacementBC(name='C44-3', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP4']
mdb.models[modelName].DisplacementBC(name='C44-4', createStepName='Step-1', 
    region=region, u1=0.5, u2=0.5, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP5']
mdb.models[modelName].DisplacementBC(name='C44-5', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP6']
mdb.models[modelName].DisplacementBC(name='C44-6', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

regionDef=mdb.models[modelName].rootAssembly.sets['c1']
mdb.models[modelName].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Step-1', variables=('RT', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

import os, glob

mdb.Job(name='job-C44', model= modelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=CPUs, numDomains=CPUs, numGPUs=0)
mdb.jobs['job-C44'].submit(consistencyChecking=OFF)

mdb.jobs['job-C44'].waitForCompletion()





# C55: C15 to C65 ####################

for i in mdb.models[modelName].loads.keys():
        del mdb.models[modelName].loads[i]


for i in mdb.models[modelName].boundaryConditions.keys():
        del mdb.models[modelName].boundaryConditions[i]


region = a.sets['RP1']
mdb.models[modelName].DisplacementBC(name='C55-1', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP2']
mdb.models[modelName].DisplacementBC(name='C55-2', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP3']
mdb.models[modelName].DisplacementBC(name='C55-3', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP4']
mdb.models[modelName].DisplacementBC(name='C55-4', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP5']
mdb.models[modelName].DisplacementBC(name='C55-5', createStepName='Step-1', 
    region=region, u1=0.5, u2=0, u3=0.5, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP6']
mdb.models[modelName].DisplacementBC(name='C55-6', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

regionDef=mdb.models[modelName].rootAssembly.sets['c1']
mdb.models[modelName].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Step-1', variables=('RT', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

import os, glob

mdb.Job(name='job-C55', model= modelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=CPUs, numDomains=CPUs, numGPUs=0)
mdb.jobs['job-C55'].submit(consistencyChecking=OFF)

mdb.jobs['job-C55'].waitForCompletion()




## C66: C61 to C66 ############################

for i in mdb.models[modelName].loads.keys():
        del mdb.models[modelName].loads[i]


for i in mdb.models[modelName].boundaryConditions.keys():
        del mdb.models[modelName].boundaryConditions[i]


region = a.sets['RP1']
mdb.models[modelName].DisplacementBC(name='C66-1', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP2']
mdb.models[modelName].DisplacementBC(name='C66-2', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP3']
mdb.models[modelName].DisplacementBC(name='C66-3', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP4']
mdb.models[modelName].DisplacementBC(name='C66-4', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


region = a.sets['RP5']
mdb.models[modelName].DisplacementBC(name='C66-5', createStepName='Step-1', 
    region=region, u1=0, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['RP6']
mdb.models[modelName].DisplacementBC(name='C66-6', createStepName='Step-1', 
    region=region, u1=0, u2=0.5, u3=0.5, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

regionDef=mdb.models[modelName].rootAssembly.sets['c1']
mdb.models[modelName].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Step-1', variables=('RT', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

import os, glob

mdb.Job(name='job-C66', model= modelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=CPUs, numDomains=CPUs, numGPUs=0)
mdb.jobs['job-C66'].submit(consistencyChecking=OFF)

mdb.jobs['job-C66'].waitForCompletion()

###  gathering data ################################################
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import os
import numpy as np
### saving data to the files###########################
for t in range(1,7):
	x='\job-C' + str(t)+str(t) + '.odb'
	path = os.getcwd()
	o3 = session.openOdb(name='%s' % (path+x))
	odb = session.odbs['%s' % (path+x)]
	session.viewports['Viewport: 1'].setValues(displayedObject=o3)
	dtm = session.odbs['%s' % (path+x)].rootAssembly.datumCsyses['ASSEMBLY_UNION-1_ORI-1']
	session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(	transformationType=USER_SPECIFIED, datumCsys=dtm)
	odbName=session.viewports[session.currentViewportName].odbDisplay.name
	session.fieldReportOptions.setValues(printTotal=OFF, printMinMax=OFF)
	filename='stress-C' + str(t)+str(t) + '.rpt'
	session.writeFieldReport(fileName=filename, append=OFF,sortItem='Element Label', odb=odb, step=0, frame=1,outputPosition= ELEMENT_CENTROID , variable=(('S', INTEGRATION_POINT, (( COMPONENT, 'S11'), (COMPONENT, 'S22'), (COMPONENT, 'S33'), (COMPONENT, 'S12'), (COMPONENT, 'S13'), (COMPONENT, 'S23'), )), ), stepFrame=SPECIFY)
################################################    
x='\job-C66.odb'
path = os.getcwd()
odb =  odb = session.odbs['%s' % (path+x)]
session.fieldReportOptions.setValues(printTotal=OFF)
session.writeFieldReport(fileName='elvol.rpt', append=OFF, 
    sortItem='Element Label', odb=odb, step=0, frame=1, 
    outputPosition=WHOLE_ELEMENT, variable=(('EVOL', WHOLE_ELEMENT), ), 
    stepFrame=SPECIFY)
### reading data###############################################################################
f=open('elvol.rpt', "r")
vol = {}
for line in f:
    if line != '\n':  
      splitLine = line.split()
      if splitLine[0].isdigit():
         vol[int(splitLine[0])]=[float(splitLine[1])]

  
###################################################################
f=open('stress-C11.rpt', "r")
stress11 = {}
for line in f:
  if line != '\n': 
    splitLine = line.split()
    if splitLine[0].isdigit():
        stress11[int(splitLine[0])]=[float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4]),float(splitLine[5]),float(splitLine[6])]



###################################################################
f=open('stress-C22.rpt', "r")
stress22 = {}
for line in f:
  if line != '\n': 
    splitLine = line.split()
    if splitLine[0].isdigit():
        stress22[int(splitLine[0])]=[float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4]),float(splitLine[5]),float(splitLine[6])]


###################################################################
f=open('stress-C33.rpt', "r").readlines()[19:]
stress33 = {}
for line in f:
  if line != '\n': 
    splitLine = line.split()
    if splitLine[0].isdigit():
        stress33[int(splitLine[0])]=[float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4]),float(splitLine[5]),float(splitLine[6])]



###################################################################
f=open('stress-C44.rpt', "r").readlines()[19:]
stress44 = {}
for line in f:
    if line != '\n':
        splitLine = line.split()
        if splitLine[0].isdigit():
            stress44[int(splitLine[0])]=[float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4]),float(splitLine[5]),float(splitLine[6])]


###################################################################
f=open('stress-C55.rpt', "r").readlines()[19:]
stress55 = {}
for line in f:
    if line != '\n':
        splitLine = line.split()
        if splitLine[0].isdigit():
            stress55[int(splitLine[0])]=[float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4]),float(splitLine[5]),float(splitLine[6])]


###################################################################
f=open('stress-C66.rpt', "r").readlines()[19:]
stress66 = {}
for line in f:
    if line != '\n':
        splitLine = line.split()
        if splitLine[0].isdigit():
            stress66[int(splitLine[0])]=[float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4]),float(splitLine[5]),float(splitLine[6])]

##calculating##################################
totalvol=0
for i in vol.keys():
    totalvol=totalvol+vol[i][0]

#######################################################
C = np.zeros((6,6))
for t in range(0,6):
    for i in stress11.keys():
      C[t][0]=C[t][0]+ stress11[i][t]*vol[i][0]
    
#######################################################

for t in range(0,6):
    for i in stress22.keys():
      C[t][1]=C[t][1]+ stress22[i][t]*vol[i][0]

#######################################################

for t in range(0,6):
    for i in stress33.keys():
      C[t][2]=C[t][2]+ stress33[i][t]*vol[i][0]

#######################################################

for t in range(0,6):
    for i in stress44.keys():
      C[t][3]=C[t][3]+ stress44[i][t]*vol[i][0]

#######################################################

for t in range(0,6):
    for i in stress55.keys():
      C[t][4]=C[t][4]+ stress55[i][t]*vol[i][0]

#######################################################

for t in range(0,6):
    for i in stress66.keys():
      C[t][5]=C[t][5]+ stress66[i][t]*vol[i][0]      



#############################################



C=C/(L*H*W)

ss = np.linalg.inv(C)

E11 = 1/ss[0,0]
E22 = 1/ss[1,1]
E33 = 1/ss[2,2]

V12 = -E11*ss[1,0]
V21 = -E22*ss[0,1]
V13 = -E11*ss[2,0]
V31 = -E33*ss[0,2]
V23 = -E22*ss[2,1]
V32 = -E33*ss[1,2]

G12 = 1/ss[3,3]
G13 = 1/ss[4,4]
G23 = 1/ss[5,5]


ayz=2*C[3,3]/(((C[1,1]+C[2,2])/2)-C[1,2])
y11=(C[0,0]+C[1,1]+C[2,2])/3
y12=(C[0,1]+C[1,2]+C[2,0])/3
y44=(C[3,3]+C[4,4]+C[5,5])/3
a=2*y44/(y11-y12)

  
###..............................

print ('E11=%s MPa' % (E11))
print ('E22=%s MPa' % (E22))
print ('E33=%s MPa' % (E33))


print ('V12=%s ratio' % (V12))
print ('V21=%s ratio' % (V21))
print ('V13=%s ratio' % (V13))
print ('V31=%s ratio' % (V31))
print ('V23=%s ratio' % (V23))
print ('V32=%s ratio' % (V32))


print ('G12=%s MPa' % (G12))
print ('G13=%s MPa' % (G13))
print ('G23=%s MPa' % (G23))

print ('Alpha=%s' % (a))
