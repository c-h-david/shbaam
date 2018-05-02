#!/usr/bin/env python
#*******************************************************************************
#tst_cmp_shp.py
#*******************************************************************************

#Purpose:
#Compare two shapefiles. The geometries are first checked, then all the 
#attributes of the first file are checked within the second file.
#Author:
#Cedric H. David, 2016-2018


#*******************************************************************************
#Prerequisites
#*******************************************************************************
import sys
import fiona


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - shb_old_shp
# 2 - shb_new_shp


#*******************************************************************************
#Get command line arguments
#*******************************************************************************
IS_arg=len(sys.argv)
if IS_arg != 3 :
     print('ERROR - 2 and only 2 arguments can be used')
     raise SystemExit(22) 

shb_old_shp=sys.argv[1]
shb_new_shp=sys.argv[2]
   

#*******************************************************************************
#Print current variables
#*******************************************************************************
print('Command line inputs')
print('- '+shb_old_shp)
print('- '+shb_new_shp)


#*******************************************************************************
#Test if input files exist
#*******************************************************************************
try:
     with open(shb_old_shp) as file:
          pass
except IOError as e:
     print('Unable to open '+shb_old_shp)
     raise SystemExit(22) 

try:
     with open(shb_new_shp) as file:
          pass
except IOError as e:
     print('Unable to open '+shb_new_shp)
     raise SystemExit(22) 


#*******************************************************************************
#Open shb_old_shp
#*******************************************************************************
print('Open shb_old_shp')

shb_old_lay=fiona.open(shb_old_shp, 'r')

IS_old_tot=len(shb_old_lay)
print('- The number of features is: '+str(IS_old_tot))

YV_old_prp=shb_old_lay.schema['properties'].keys()
print('- The number of attributes is: '+str(len(YV_old_prp)))


#*******************************************************************************
#Open shb_new_shp
#*******************************************************************************
print('Open shb_new_shp')

shb_new_lay=fiona.open(shb_new_shp, 'r')

IS_new_tot=len(shb_new_lay)
print('- The number of features is: '+str(IS_new_tot))

YV_new_prp=shb_new_lay.schema['properties'].keys()
print('- The number of attributes is: '+str(len(YV_new_prp)))


#*******************************************************************************
#Compare number of features
#*******************************************************************************
print('Compare number of features')
if IS_old_tot==IS_new_tot:
     print('- The numbers of features are the same')
else:
     print('ERROR - The numbers of features are different: '                   \
           +str(IS_old_tot)+' <> '+str(IS_new_tot))
     raise SystemExit(99) 


#*******************************************************************************
#Compare content of shapefiles
#*******************************************************************************
print('Compare content of shapefiles')

for JS_old_tot in range(IS_old_tot):
     #--------------------------------------------------------------------------
     #Extract the properties and geometry for the current feature of old file
     #--------------------------------------------------------------------------
     shb_old_fea=shb_old_lay[JS_old_tot]
     shb_old_prp=shb_old_fea['properties']
     shb_old_geo=shb_old_fea['geometry']

     #--------------------------------------------------------------------------
     #Extract the properties and geometry for the current feature of new file
     #--------------------------------------------------------------------------
     shb_new_fea=shb_new_lay[JS_old_tot]
     shb_new_prp=shb_new_fea['properties']
     shb_new_geo=shb_new_fea['geometry']
     
     #--------------------------------------------------------------------------
     #Compare geometry
     #--------------------------------------------------------------------------
     if shb_old_geo!=shb_new_geo:
          print('ERROR - The geometries of features are different for index: ' \
                +str(JS_old_tot))
          raise SystemExit(99) 

     #--------------------------------------------------------------------------
     #Compare attributes
     #--------------------------------------------------------------------------
     for YS_old_prp in YV_old_prp:
          if shb_old_prp[YS_old_prp]!=shb_new_prp[YS_old_prp]:
               print('ERROR - The attributes of features are different for '+  \
                     'index: '+str(JS_old_tot)+', attribute: '+str(JS_old_att))
            
print('Success!!!')


#*******************************************************************************
#End
#*******************************************************************************
