#!/usr/bin/env python
#*******************************************************************************
#tst_cmp_n3d.py
#*******************************************************************************

#Purpose:
#Compare netCDF files.
#Author:
#Cedric H. David, 2018-2018


#*******************************************************************************
#Prerequisites
#*******************************************************************************
import sys
import netCDF4
import math
import numpy


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - rrr_ncf_file1
# 2 - rrr_ncf_file2
#(3)- relative tolerance 
#(4)- absolute tolerance 


#*******************************************************************************
#Get command line arguments
#*******************************************************************************
IS_arg=len(sys.argv)
if IS_arg < 3 or IS_arg > 5:
     print('ERROR - A minimum of 2 and a maximum of 4 arguments can be used')
     raise SystemExit(22) 

rrr_ncf_file1=sys.argv[1]
rrr_ncf_file2=sys.argv[2]
if IS_arg > 3:
     ZS_rtol=float(sys.argv[3])
else:
     ZS_rtol=float(0)
if IS_arg > 4:
     ZS_atol=float(sys.argv[4])
else:
     ZS_atol=float(0)
     

#*******************************************************************************
#Print current variables
#*******************************************************************************
print('Comparing netCDF files')
print('1st netCDF file               :'+rrr_ncf_file1)
print('2nd netCDF file               :'+rrr_ncf_file2)
print('Relative tolerance            :'+str(ZS_rtol))
print('Absolute tolerance            :'+str(ZS_atol))
print('-------------------------------')


#*******************************************************************************
#Test if input files exist
#*******************************************************************************
try:
     with open(rrr_ncf_file1) as file:
          pass
except IOError as e:
     print('Unable to open '+rrr_ncf_file1)
     raise SystemExit(22) 

try:
     with open(rrr_ncf_file2) as file:
          pass
except IOError as e:
     print('Unable to open '+rrr_ncf_file2)
     raise SystemExit(22) 


#*******************************************************************************
#Read and compare netCDF files
#*******************************************************************************

#-------------------------------------------------------------------------------
#Open files and get dimensions
#-------------------------------------------------------------------------------
f1 = netCDF4.Dataset(rrr_ncf_file1, "r")

if 'lon' in f1.dimensions:
     IS_lon1=len(f1.dimensions['lon'])
elif 'Lon' in f1.dimensions:
     IS_lon1=len(f1.dimensions['Lon'])
else:
     print('ERROR - Neither lon nor Lon are dimensions in: '+rrr_ncf_file1) 
     raise SystemExit(99) 

if 'lat' in f1.dimensions:
     IS_lat1=len(f1.dimensions['lat'])
elif 'Lat' in f1.dimensions:
     IS_lat1=len(f1.dimensions['Lat'])
else:
     print('ERROR - Neither lat nor Lat are dimensions in: '+rrr_ncf_file1) 
     raise SystemExit(99) 

if 'time' in f1.dimensions:
     IS_time1=len(f1.dimensions['time'])
elif 'Time' in f1.dimensions:
     IS_time1=len(f1.dimensions['Time'])
else:
     print('ERROR - Neither time nor Time are dimensions in: '+rrr_ncf_file1) 
     raise SystemExit(99) 

if 'lwe_thickness' in f1.variables:
     rrr_ncf_var1='lwe_thickness'
else:
     print('ERROR - lwe_thickness is not a variable in: '+rrr_ncf_file1) 
     raise SystemExit(99) 

f2 = netCDF4.Dataset(rrr_ncf_file2, "r")

if 'lon' in f2.dimensions:
     IS_lon2=len(f2.dimensions['lon'])
elif 'Lon' in f2.dimensions:
     IS_lon2=len(f2.dimensions['Lon'])
else:
     print('ERROR - Neither lon nor Lon are dimensions in: '+rrr_ncf_file2) 
     raise SystemExit(99) 

if 'lat' in f2.dimensions:
     IS_lat2=len(f2.dimensions['lat'])
elif 'Lat' in f2.dimensions:
     IS_lat2=len(f2.dimensions['Lat'])
else:
     print('ERROR - Neither lat nor Lat are dimensions in: '+rrr_ncf_file2) 
     raise SystemExit(99) 

if 'time' in f2.dimensions:
     IS_time2=len(f2.dimensions['time'])
elif 'Time' in f2.dimensions:
     IS_time2=len(f2.dimensions['Time'])
else:
     print('ERROR - Neither time nor Time are dimensions in: '+rrr_ncf_file2) 
     raise SystemExit(99) 

if 'lwe_thickness' in f2.variables:
     rrr_ncf_var2='lwe_thickness'
else:
     print('ERROR - lwe_thickness is not a variable in: '+rrr_ncf_file2) 
     raise SystemExit(99) 


#-------------------------------------------------------------------------------
#Compare file sizes and variable names
#-------------------------------------------------------------------------------
if IS_lon1==IS_lon2:
     IS_lon=IS_lon1
     print('Common number of longitudes   :'+str(IS_lon))
else:
     print('ERROR - The number of longitudes differs: '                        \
           +str(IS_lon1)+' <> '+str(IS_lon2))
     raise SystemExit(99) 

if IS_lat1==IS_lat2:
     IS_lat=IS_lat1
     print('Common number of latitudes    :'+str(IS_lat))
else:
     print('ERROR - The number of latitudes differs: '                         \
           +str(IS_lat1)+' <> '+str(IS_lat2))
     raise SystemExit(99) 

if IS_time1==IS_time2:
     IS_time=IS_time1
     print('Common number of time steps   :'+str(IS_time))
else:
     print('ERROR - The number of time steps differs: '                        \
           +str(IS_time1)+' <> '+str(IS_time2))
     raise SystemExit(99) 

if rrr_ncf_var1==rrr_ncf_var2:
     rrr_ncf_var=rrr_ncf_var1
     print('Common variable name          :'+rrr_ncf_var)
else:
     print('ERROR - The variable names differ: '                               \
           +rrr_ncf_var1+' <> '+rrr_ncf_var1)
     raise SystemExit(99) 

print('-------------------------------')

#-------------------------------------------------------------------------------
#Compare coordinate values if they exist in both files
#-------------------------------------------------------------------------------
if 'lon' in f1.variables:
     ZV_lon1=f1.variables['lon']
elif 'Lon' in f1.variables:
     ZV_lon1=f1.variables['Lon']

if 'lon' in f2.variables:
     ZV_lon2=f2.variables['lon']
elif 'Lon' in f2.variables:
     ZV_lon2=f2.variables['Lon']

if 'ZV_lon1' in locals() and 'ZV_lon2' in locals():
     #This makes sure that both variables actually exist before comparing them
     if numpy.array_equal(ZV_lon1[:],ZV_lon2[:]):
          print('The longitudes are the same')
     else:
          print('ERROR: The longitudes differ')
          raise SystemExit(99) 

if 'lat' in f1.variables:
     ZV_lat1=f1.variables['lat']
elif 'Lat' in f1.variables:
     ZV_lat1=f1.variables['Lat']

if 'lat' in f2.variables:
     ZV_lat2=f2.variables['lat']
elif 'Lat' in f2.variables:
     ZV_lat2=f2.variables['Lat']

if 'ZV_lat1' in locals() and 'ZV_lat2' in locals():
     #This makes sure that both variables actually exist before comparing them
     if numpy.array_equal(ZV_lat1[:],ZV_lat2[:]):
          print('The latitudes are the same')
     else:
          print('ERROR: The latitudes differ')
          raise SystemExit(99) 

print('-------------------------------')

#-------------------------------------------------------------------------------
#Compute differences 
#-------------------------------------------------------------------------------
ZS_rdif_max=0
ZS_adif_max=0

for JS_time in range(IS_time):
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#initializing
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
     ZS_rdif=0
     ZS_adif=0

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#Reading values
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
     ZM_Var_1=f1.variables[rrr_ncf_var][JS_time,:]
     ZM_Var_2=f2.variables[rrr_ncf_var][JS_time,:]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#Checking that the locations of NoData are the same
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
     ZM_mask1=numpy.logical_not(numpy.ma.getmaskarray(ZM_Var_1))
     ZM_mask2=numpy.logical_not(numpy.ma.getmaskarray(ZM_Var_2))
     if numpy.array_equal(ZM_mask1,ZM_mask2):
          ZM_mask=ZM_mask1
     else:
          print('ERROR - The locations of NoData differ')
          raise SystemExit(99) 

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#Comparing difference values
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
     #Tried computations with regular Python lists but this makes is very slow.
     #Also tried using map(operator.sub,V,W) or [x-y for x,y in zip(V,W)]
     #But this still results in slow computations.
     #The best performance seems to be with Numpy.
     ZM_dVar_abs=numpy.absolute(ZM_Var_1-ZM_Var_2)
     ZS_adif_max=max(numpy.max(ZM_dVar_abs),ZS_adif_max)

     ZS_rdif=numpy.sum(numpy.multiply(ZM_dVar_abs,ZM_dVar_abs,where=ZM_mask))  \
            /numpy.sum(numpy.multiply(ZM_Var_1,ZM_Var_1,where=ZM_mask))
     #Using the mask helps avoid the 'overflow' warning at runtime by performing
     #operations only for values that are not masked
     ZS_rdif=math.sqrt(ZS_rdif)
     ZS_rdif_max=max(ZS_rdif,ZS_rdif_max)


#*******************************************************************************
#Print difference values and comparing values to tolerance
#*******************************************************************************
print('Max relative difference       :'+'{0:.2e}'.format(ZS_rdif_max))
print('Max absolute difference       :'+'{0:.2e}'.format(ZS_adif_max))
print('-------------------------------')

if ZS_rdif_max > ZS_rtol:
     print('Unacceptable rel. difference!!!')
     print('-------------------------------')
     raise SystemExit(99) 

if ZS_adif_max > ZS_atol:
     print('Unacceptable abs. difference!!!')
     print('-------------------------------')
     raise SystemExit(99) 

print('netCDF files similar!!!')
print('-------------------------------')


#*******************************************************************************
#End
#*******************************************************************************
