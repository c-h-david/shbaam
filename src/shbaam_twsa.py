#!/usr/bin/env python
#*******************************************************************************
#shbaam_twsa.py
#*******************************************************************************

#Purpose:
#Compute Terrestrial Water Storage Anomalies from GRACE for a given shapefile.
#Given GRACE data and associated scale factors, along with a shapefile 
#referenced on a Geographic Coordinate System (i.e. longitude, latitude), this 
#script computes liquid water equivalent thickness anomaly (in cm) for every 
#time step of the GRACE data and produces a CSV time series that is spatially 
#averaged over the shapefile, as well as a netCDF time series focusing on the 
#shapefile. If the shapefile touches coastal grid cells that have NoData in the 
#GRACE scale factors, these points are ignored in the averaging.
#Author:
#Cedric H. David, 2017-2017


#*******************************************************************************
#Import Python modules
#*******************************************************************************
import sys
import os.path
import subprocess
import netCDF4
import numpy
import datetime
import fiona
import shapely.geometry
import rtree
import math
import csv


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - shb_grc_ncf
# 2 - shb_fct_ncf
# 3 - shb_pol_shp
# 4 - shb_wsa_csv
# 5 - shb_wsa_ncf


#*******************************************************************************
#Get command line arguments
#*******************************************************************************
IS_arg=len(sys.argv)
if IS_arg != 6:
     print('ERROR - 5 and only 5 arguments can be used')
     raise SystemExit(22) 

shb_grc_ncf=sys.argv[1]
shb_fct_ncf=sys.argv[2]
shb_pol_shp=sys.argv[3]
shb_wsa_csv=sys.argv[4]
shb_wsa_ncf=sys.argv[5]


#*******************************************************************************
#Print input information
#*******************************************************************************
print('Command line inputs')
print(' - '+shb_grc_ncf)
print(' - '+shb_fct_ncf)
print(' - '+shb_pol_shp)
print(' - '+shb_wsa_csv)
print(' - '+shb_wsa_ncf)


#*******************************************************************************
#Check if files exist 
#*******************************************************************************
try:
     with open(shb_grc_ncf) as file:
          pass
except IOError as e:
     print('ERROR - Unable to open '+shb_grc_ncf)
     raise SystemExit(22) 

try:
     with open(shb_fct_ncf) as file:
          pass
except IOError as e:
     print('ERROR - Unable to open '+shb_fct_ncf)
     raise SystemExit(22) 

try:
     with open(shb_pol_shp) as file:
          pass
except IOError as e:
     print('ERROR - Unable to open '+shb_pol_shp)
     raise SystemExit(22) 


#*******************************************************************************
#Read GRACE netCDF file
#*******************************************************************************
print('Read GRACE netCDF file')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Open netCDF file
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
f = netCDF4.Dataset(shb_grc_ncf, 'r')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Get dimension sizes
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
IS_grc_lon=len(f.dimensions['lon'])
print(' - The number of longitudes is: '+str(IS_grc_lon))

IS_grc_lat=len(f.dimensions['lat'])
print(' - The number of latitudes is: '+str(IS_grc_lat))

IS_grc_time=len(f.dimensions['time'])
print(' - The number of time steps is: '+str(IS_grc_time))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Get values of dimension arrays
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ZV_grc_lon=f.variables['lon']
ZV_grc_lat=f.variables['lat']
ZV_grc_time=f.variables['time']

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Get fill values
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ZS_grc_fil=netCDF4.default_fillvals['f4']
if 'RUNSF' in f.variables:
     var=f.variables['RUNSF']
     if '_FillValue' in  var.ncattrs(): 
          ZS_grc_fil=var._FillValue
          print(' - The fill value for RUNSF is: '+str(ZS_grc_fil))
     else:
          ZS_grc_fil=None
     

#*******************************************************************************
#Read scale factors netCDF file
#*******************************************************************************
print('Read scale factors netCDF file')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Open netCDF file
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
g= netCDF4.Dataset(shb_fct_ncf, 'r')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Get dimension sizes
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
IS_fct_lon=len(g.dimensions['lon'])
print(' - The number of longitudes is: '+str(IS_fct_lon))

IS_fct_lat=len(g.dimensions['lat'])
print(' - The number of latitudes is: '+str(IS_fct_lat))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Get values of dimension arrays
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ZV_fct_lon=g.variables['lon']
ZV_fct_lat=g.variables['lat']


#*******************************************************************************
#Check consistency between netCDF files
#*******************************************************************************
print('Check consistency between netCDF files')

if (IS_fct_lon != IS_grc_lon):
     print('ERROR - The number of longitudes differ')
     raise SystemExit(22) 

if not (ZV_fct_lon[:] == ZV_grc_lon[:]).all():
     print('ERROR - The values of longitudes differ')
     raise SystemExit(22) 

if (IS_fct_lat != IS_grc_lat):
     print('ERROR - The number of latitudes differ')
     raise SystemExit(22) 

if not (ZV_fct_lat[:] == ZV_grc_lat[:]).all():
     print('ERROR - The values of latitudes differ')
     raise SystemExit(22) 

print(' - The files are consistent')


#*******************************************************************************
#Read polygon shapefile
#*******************************************************************************
print('Read polygon shapefile')

shb_pol_lay=fiona.open(shb_pol_shp, 'r')
IS_pol_tot=len(shb_pol_lay)
print(' - The number of polygon features is: '+str(IS_pol_tot))


#*******************************************************************************
#Create spatial index for the bounds of each polygon feature
#*******************************************************************************
print('Create spatial index for the bounds of each polygon feature')

index=rtree.index.Index()
for shb_pol_fea in shb_pol_lay:
     shb_pol_fid=int(shb_pol_fea['id'])
     #the first argument of index.insert has to be 'int', not 'long' or 'str'
     shb_pol_shy=shapely.geometry.shape(shb_pol_fea['geometry'])
     index.insert(shb_pol_fid, shb_pol_shy.bounds)
     #creates an index between the feature ID and the bounds of that feature


#*******************************************************************************
#Find GRACE grid cells that intersect with polygon
#*******************************************************************************
print('Find GRACE grid cells that intersect with polygon')

IS_dom_tot=0
IV_dom_lon=[]
IV_dom_lat=[]

for JS_grc_lon in range(IS_grc_lon):
     ZS_grc_lon=ZV_grc_lon[JS_grc_lon]
     if (ZS_grc_lon > 180):
          ZS_grc_lon=ZS_grc_lon-360
          #Shift GRACE longitude range from [0;360] to [-180;180]

     for JS_grc_lat in range(IS_grc_lat):
          ZS_grc_lat=ZV_grc_lat[JS_grc_lat]
          shb_pnt_shy=shapely.geometry.Point(ZS_grc_lon,ZS_grc_lat)
          #a shapely point now exists for a given GRACE grid cell
          for shb_pol_fid in                                                 \
              [int(x) for x in list(index.intersection(shb_pnt_shy.bounds))]:
               shb_pol_fea=shb_pol_lay[shb_pol_fid]
               shb_pol_shy=shapely.geometry.shape(shb_pol_fea['geometry'])
               if (shb_pnt_shy.within(shb_pol_shy)):
                    IV_dom_lon.append(JS_grc_lon)
                    IV_dom_lat.append(JS_grc_lat)
                    IS_dom_tot=IS_dom_tot+1
 
print(' - The number of grid cells found is: '+str(IS_dom_tot))


#*******************************************************************************
#Find long-term mean for each intersecting GRACE grid cell
#*******************************************************************************
print('Find long-term mean for each intersecting GRACE grid cell')

ZV_dom_avg=[0]*IS_dom_tot
for JS_dom_tot in range(IS_dom_tot):
     JS_grc_lon=IV_dom_lon[JS_dom_tot]
     JS_grc_lat=IV_dom_lat[JS_dom_tot]
     for JS_grc_time in range(IS_grc_time):
          ZV_dom_avg[JS_dom_tot]=ZV_dom_avg[JS_dom_tot]                        \
                                +f.variables['lwe_thickness']                  \
                                            [JS_grc_time,JS_grc_lat,JS_grc_lon]
ZV_dom_avg=[x/IS_grc_time for x in ZV_dom_avg]


#*******************************************************************************
#Compute surface area of each grid cell
#*******************************************************************************
print('Compute surface area of each grid cell')

ZV_dom_sqm=[0]*IS_dom_tot
for JS_dom_tot in range(IS_dom_tot):
     JS_grc_lat=IV_dom_lat[JS_dom_tot]
     ZS_grc_lat=ZV_grc_lat[JS_grc_lat]
     ZV_dom_sqm[JS_dom_tot]=6371000*math.radians(0.5)                          \
                           *6371000*math.radians(0.5)                          \
                           *math.cos(math.radians(ZS_grc_lat))


#*******************************************************************************
#Find number of NoData points in scale factors for shapefile and area
#*******************************************************************************
print('Find number of NoData points in scale factors for shapefile and area')

ZM_grc_scl=g.variables['scale_factor'][:,:]
IS_dom_msk=0
ZS_sqm=0
for JS_dom_tot in range(IS_dom_tot):
     JS_grc_lon=IV_dom_lon[JS_dom_tot]
     JS_grc_lat=IV_dom_lat[JS_dom_tot]
     if (ZM_grc_scl.mask[JS_grc_lat,JS_grc_lon]):
          IS_dom_msk=IS_dom_msk+1
     else:
          ZS_sqm=ZS_sqm+ZV_dom_sqm[JS_dom_tot]

print(' - The number of NoData points found is: '+str(IS_dom_msk))
print(' - The area (m2) for the domain is: '+str(ZS_sqm))


#*******************************************************************************
#Compute total terrestrial water storage anomaly timeseries
#*******************************************************************************
print('Compute total terrestrial water storage anomaly timeseries')

ZV_wsa=[]
for JS_grc_time in range(IS_grc_time):
     ZS_wsa=0
     for JS_dom_tot in range(IS_dom_tot):
          JS_grc_lon=IV_dom_lon[JS_dom_tot]
          JS_grc_lat=IV_dom_lat[JS_dom_tot]
          ZS_dom_sqm=ZV_dom_sqm[JS_dom_tot]
          ZS_dom_avg=ZV_dom_avg[JS_dom_tot]
          if (ZM_grc_scl.mask[JS_grc_lat,JS_grc_lon]):
               ZS_dom_scl=0
          else:
               ZS_dom_scl=ZM_grc_scl[JS_grc_lat,JS_grc_lon]
          ZS_dom_wsa=( f.variables['lwe_thickness']                            \
                                  [JS_grc_time,JS_grc_lat,JS_grc_lon]          \
                      -ZS_dom_avg                                    )/100     \
                    *  ZS_dom_scl                                              \
                    *  ZS_dom_sqm
                    #The division by 100 is to go from cm to m in GRACE data.
          ZS_wsa=ZS_wsa+ZS_dom_wsa
     ZV_wsa.append(100*ZS_wsa/ZS_sqm)


#*******************************************************************************
#Determine time strings
#*******************************************************************************
print('Determine time strings')
shb_dat_str=datetime.datetime.strptime('2002-01-01T00:00:00',                \
                                         '%Y-%m-%dT%H:%M:%S')

YV_grc_time=[]
for JS_grc_time in range(IS_grc_time):
     shb_dat_dlt=datetime.timedelta(days=ZV_grc_time[JS_grc_time])
     YS_grc_time=(shb_dat_str+shb_dat_dlt).strftime('%m/%d/%Y')
     YV_grc_time.append(YS_grc_time)


#*******************************************************************************
#Write shb_wsa_csv
#*******************************************************************************
print('Write shb_wsa_csv')

with open(shb_wsa_csv, 'wb') as csvfile:
     #csvwriter = csv.writer(csvfile, dialect='excel', quotechar="'",           \
     #                       quoting=csv.QUOTE_NONNUMERIC)
     csvwriter = csv.writer(csvfile, dialect='excel')
     for JS_grc_time in range(IS_grc_time):
          IV_line=[YV_grc_time[JS_grc_time],ZV_wsa[JS_grc_time]] 
          csvwriter.writerow(IV_line) 


#*******************************************************************************
#Write shb_wsa_ncf
#*******************************************************************************
print('Write shb_wsa_ncf')

#-------------------------------------------------------------------------------
#Create netCDF file
#-------------------------------------------------------------------------------
print('- Create netCDF file')

h = netCDF4.Dataset(shb_wsa_ncf, 'w', format="NETCDF3_CLASSIC")

time = h.createDimension("time", None)
lat = h.createDimension("lat", IS_grc_lat)
lon = h.createDimension("lon", IS_grc_lon)
nv = h.createDimension("nv", 2)

time = h.createVariable("time","i4",("time",))
time_bnds = h.createVariable("time_bnds","i4",("time","nv",))
lat = h.createVariable("lat","f4",("lat",))
lon = h.createVariable("lon","f4",("lon",))
lwe_thickness = h.createVariable("lwe_thickness","f4",("time","lat","lon",),   \
                                 fill_value=ZS_grc_fil)
crs = h.createVariable("crs","i4")

#-------------------------------------------------------------------------------
#Metadata in netCDF global attributes
#-------------------------------------------------------------------------------
print('- Populate global attributes')

dt=datetime.datetime.utcnow()
dt=dt.replace(microsecond=0)
#Current UTC time without the microseconds 
vsn=subprocess.Popen('../version.sh',stdout=subprocess.PIPE).communicate()
vsn=vsn[0]
vsn=vsn.rstrip()
#Version of SHBAAM

h.Conventions='CF-1.6'
h.title=''
h.institution=''
h.source='SHBAAM: '+vsn+', GRACE: '+os.path.basename(shb_grc_ncf)             \
                      +', Scale factors: '+os.path.basename(shb_fct_ncf)
h.history='date created: '+dt.isoformat()+'+00:00'
h.references='https://github.com/c-h-david/shbaam/'
h.comment=''
h.featureType='timeSeries'

#-------------------------------------------------------------------------------
#Metadata in netCDF variable attributes
#-------------------------------------------------------------------------------
print('- Copy existing variable attributes')

if 'time' in f.variables:
     var=f.variables['time']
     if 'standard_name' in  var.ncattrs(): time.standard_name=var.standard_name
     if 'long_name' in var.ncattrs(): time.long_name=var.long_name
     if 'units' in var.ncattrs(): time.units=var.units
     if 'axis' in var.ncattrs(): time.axis=var.axis
     if 'calendar' in var.ncattrs(): time.calendar=var.calendar
     if 'bounds' in var.ncattrs(): time.bounds=var.bounds

if 'lat' in f.variables:
     var=f.variables['lat']
     if 'standard_name' in  var.ncattrs(): lat.standard_name=var.standard_name
     if 'long_name' in  var.ncattrs(): lat.long_name=var.long_name
     if 'units' in  var.ncattrs(): lat.units=var.units
     if 'axis' in  var.ncattrs(): lat.axis=var.axis

if 'lon' in f.variables:
     var=f.variables['lon']
     if 'standard_name' in  var.ncattrs(): lon.standard_name=var.standard_name
     if 'long_name' in  var.ncattrs(): lon.long_name=var.long_name
     if 'units' in  var.ncattrs(): lon.units=var.units
     if 'axis' in  var.ncattrs(): lon.axis=var.axis

if 'lwe_thickness' in f.variables: 
     var=f.variables['lwe_thickness']
     if 'standard_name' in var.ncattrs(): lwe_thickness.standard_name=var.standard_name
     if 'long_name' in var.ncattrs(): lwe_thickness.long_name=var.long_name
     if 'units' in var.ncattrs(): lwe_thickness.units=var.units
     if 'units' in var.ncattrs(): lwe_thickness.coordinates=var.coordinates
     if 'grid_mapping' in var.ncattrs(): lwe_thickness.grid_mapping=var.grid_mapping
     if 'cell_methods' in var.ncattrs(): lwe_thickness.cell_methods=var.cell_methods

if 'crs' in f.variables: 
     var=f.variables['crs']
     if 'grid_mapping_name' in var.ncattrs(): crs.grid_mapping_name=var.grid_mapping_name
     if 'semi_major_axis' in var.ncattrs(): crs.semi_major_axis=var.semi_major_axis
     if 'inverse_flattening' in var.ncattrs(): crs.inverse_flattening=var.inverse_flattening

print('- Modify CRS variable attributes')
lwe_thickness.grid_mapping='crs'
crs.grid_mapping_name='latitude_longitude'
crs.semi_major_axis='6378137'
crs.inverse_flattening='298.257223563' 
#These are for the WGS84 spheroid

#-------------------------------------------------------------------------------
#Populate static data
#-------------------------------------------------------------------------------
print('- Populate static data')

lon[:]=ZV_grc_lon[:]
lat[:]=ZV_grc_lat[:]
#Coordinates

#-------------------------------------------------------------------------------
#Populate dynamic data
#-------------------------------------------------------------------------------
print('- Populate dynamic data')

for JS_dom_tot in range(IS_dom_tot):
     JS_grc_lon=IV_dom_lon[JS_dom_tot]
     JS_grc_lat=IV_dom_lat[JS_dom_tot]
     ZS_dom_avg=ZV_dom_avg[JS_dom_tot]
     if (ZM_grc_scl.mask[JS_grc_lat,JS_grc_lon]):
          ZS_dom_scl=0
     else:
          ZS_dom_scl=ZM_grc_scl[JS_grc_lat,JS_grc_lon]
     for JS_grc_time in range(IS_grc_time):
          lwe_thickness[JS_grc_time,JS_grc_lat,JS_grc_lon]=                    \
            f.variables['lwe_thickness'][JS_grc_time,JS_grc_lat,JS_grc_lon]    \
            -ZS_dom_avg

time[:]=f.variables['time'][:]


#*******************************************************************************
#Close netCDF files
#*******************************************************************************
print('Close netCDF files')

f.close()
g.close()
h.close()


#*******************************************************************************
#Check some computations
#*******************************************************************************
print('Check some computations')

print('- Average of time series: '+str(numpy.average(ZV_wsa)))
print('- Maximum of time series: '+str(numpy.max(ZV_wsa)))
print('- Minimum of time series: '+str(numpy.min(ZV_wsa)))


#*******************************************************************************
#End
#*******************************************************************************
