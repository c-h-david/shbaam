#!/usr/bin/env python


#*******************************************************************************
#shbaam_ldas_anoms.py
#*******************************************************************************

#Purpose:
# Given a filepath to a GLDAS concatenated file, and a shapefile with a geographic (Lat,Lon)
# coordinate reference system,  this script computes water storage anomalies within
# a shapefile's footprint.
# Outputs include: a csv file AND a netcdf file for the subset area

#Author:
# A.J. Purdy, 2019
# Modified from C.H. David  shbaam_twsa.py
# Modified from UCI Fall 2018 CS Class: Tong, Alaya, Gonzalez, Yamamoto

#*******************************************************************************
#Import Python modules
#*******************************************************************************
import sys
from netCDF4 import Dataset, num2date, date2num
import fiona
import shapely.geometry
import shapely.prepared
import rtree
import math
import numpy
import csv
import datetime
import xarray as xr

#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - concatenated GLDAS data in netcdf format
# 2 - shapefile of format '.shp'
# 3 - output shapefile of GLDAS coordinates for region of interest
# 4 - output csv file time series of region mean anomalies
# 5 - output (3-dimensional) netcdf file of GLDAS anomalies

#*******************************************************************************
#Get command line arguments
#*******************************************************************************
fin = sys.argv[1:]

#*******************************************************************************
#Print input information
#*******************************************************************************
print('Command line inputs')
print(' - '+fin[0])
print(' - '+fin[1])
print(' - '+fin[2])
print(' - '+fin[3])
print(' - '+fin[4])

#*******************************************************************************
#Check crs of input shapefile
#*******************************************************************************
# read polygon shapefile

polygon = fiona.open(fin[1], 'r')
if 'PROJCS' in polygon.crs_wkt:
    print('ERRROR the coordinate reference system of ' + fin[1] + ' is incompatible with shbaam')
    print('\tSet the crs of ' + fin[1] + ' to a compatable crs')
    print('\tThese include: EPSG:4326, EPSG:4269, or EPSG: 4267')
    raise SystemExit(22)
elif 'GEOGCS' not in polygon.crs_wkt:
    print('ERROR the coordinate reference system of ' + fin[1] + ' is not defined')
    print('\tSet the crs of ' + fin[1] + ' to a compatable crs')
    print('\tThese include: EPSG:4326, EPSG:4269, or EPSG: 4267')
    raise SystemExit(22)

# the other way to do this check is to evaluate poly.crs
# if (polygon.crs['init'] != 'epsg:4326): EPSG:4269 : (EPSG: 4267):

# *******************************************************************************
def createPointShp(input_shp, output_shp, num_lon, num_lat, lons, lats):
    '''
    Create a point with all GLDAS grid cells
    '''
    point_driver = input_shp.driver
    point_crs = input_shp.crs

    point_schema = {'geometry': 'Point',
                 'properties': {'lon' : 'float',
                                'lat' : 'float',
                                'lon_index': 'int:4',
                                'lat_index': 'int:4',
                                }}

    with fiona.open( output_shp, 'w', driver=point_driver, crs=point_crs, schema=point_schema) as pf:
       for lon_index in range(num_lon):
            longitude = lons[lon_index]

            for lat_index in range(num_lat):
                latitude = lats[lat_index]

                pf_property = { 'lon': longitude, 'lat': latitude,
                                'lon_index': lon_index, 'lat_index': lat_index,}
                pf_geometry = shapely.geometry.mapping(
                            shapely.geometry.Point((longitude, latitude)))
                pf.write({
                           'properties': pf_property,
                           'geometry': pf_geometry,
                         })

    print('Success -- created a new shapefile')

def createRtreeIndex(pf):
    idx = rtree.index.Index()
    for point in pf:
        point_id = int(point['id'])
        point_bounds = shapely.geometry.shape(point['geometry']).bounds
        idx.insert(point_id, point_bounds)
    print('Success -- created rtree')
    return idx

def findInterest(pol, pf, idx):
    total = 0
    interest_lon = []
    interest_lat = []

    for polygon in pol:
        polygon_geo = shapely.geometry.shape(polygon['geometry'])
        prepared_polygon = shapely.prepared.prep( polygon_geo )
        for pf_id in [int(i) for i in list(idx.intersection(polygon_geo.bounds))]:
            point = pf[pf_id]
            point_bounds = shapely.geometry.shape(point['geometry'])
            if prepared_polygon.contains(point_bounds):
                #print('cell:', pf_id)
                interest_lon.append( (point['properties']['lon_index'], point['properties']['lon']) )
                interest_lat.append( (point['properties']['lat_index'], point['properties']['lat']) )
                total += 1

    print('The total cells found: ' + str(total) )
    print('The longitude of the cells: ' + str([i[1] for i in interest_lon]) )
    print('The lattitude of the cells: '+ str([i[1] for i in interest_lat]) )
    return total, interest_lon, interest_lat

def findAvg(var, total, interest_lon, interest_lat, time_steps):
    #var: the nc4.variables that you want to get for average such as swe..
    print('--Find long-term mean for each intersecting GLDAS grid cell--')
    avg = [0.0] * total
    for cell_index in range(total):
        lon_index = interest_lon[cell_index][0]
        lat_index = interest_lat[cell_index][0]
        for time in range(time_steps):
            avg[cell_index] = avg[cell_index] + var[time, lat_index, lon_index]

    avg = [i / time_steps for i in avg]
    print('--long-term mean:' + str(avg)+'--')
    return avg

def calculateSurfaceArea(total, num_lat, interest_lat, lon_step, lat_step):
    areas = [0] * total
    for cell_index in range(total):
        areas[ cell_index ] = 6371000*math.radians(lat_step) \
                                    *6371000*math.radians(lon_step)\
                                    *math.cos(math.radians(interest_lat[cell_index][1]))
    print('area for each interest cell: ' + str(areas))
    return areas

def sum_SM_by_depth(dataset):
    if 'SoilMoist' in dataset.data_vars:
        tot_sm = dataset.SoilMoist.sum(dim='depth')
        tot_sm.attrs['units'] = 'kg/m2'
        dataset['SMTa'] = tot_sm
        dataset = dataset.drop(['SoilMoist','depth_bnds'])
        print('Soil moisture summed by depth for anomaly time sereis')
    else:
        print('ERROR - No soil moisture data available. Please check input dataset.')
        raise SystemExit(22)
    return dataset

def anomalyTimeseries(var, var_factor, avg, time_steps, total, interest_lon, interest_lat, areas):
    print('Compute storage anomaly timeseries')
    anomalies = []
    total_area = sum(areas)
    print(total_area)
    for time in range(time_steps):
        anomaly_in_time = 0
        for cell_index in range(total):
            lon_index = interest_lon[cell_index][0]
            lat_index = interest_lat[cell_index][0]
            area = areas[cell_index]
            long_term_mean = avg[cell_index]
            anomaly_in_area = (var[time, lat_index, lon_index] - long_term_mean) / var_factor * area
            # print(anomaly_in_area)
            if numpy.isnan(anomaly_in_area):
                anomaly_in_time += 0
            else:
                anomaly_in_time += anomaly_in_area
        # 100 changes the units of anomaly in time / total area from m to cm to be the same as grace
        anomalies.append(100 * anomaly_in_time / total_area)

    avgT = numpy.mean(anomalies)
    maxT = numpy.max(anomalies)
    minT = numpy.min(anomalies)
    print('- Average of time series: '+str(avgT))
    print('- Maximum of time series: '+str(maxT))
    print('- Minimum of time series: '+str(minT))

    return anomalies


def outputCSV(output_file, fieldnames, times, anomalies_dict):
    with open(output_file, mode='w') as csvfile:
        writer = csv.DictWriter(csvfile, dialect='excel', fieldnames=fieldnames)
        dates = times #createTimes(times)
        writer.writeheader()
        for i in range(len(dates)):
            d = dict()
            d[fieldnames[0]] = dates[i]
            for j in range(1, len(fieldnames)):
                d[fieldnames[j]] = anomalies_dict[fieldnames[j]][i]
            writer.writerow(d)
    csvfile.close()
    print('Success -- creating csv file')

def outputNC(output_file, ds, total, interest_lon, interest_lat, time_steps, var_list, avg_dict):
    print('Writing new nc4 file')
    nc4_out = Dataset(output_file, 'w', format='NETCDF4')
    time = nc4_out.createDimension("time", None)
    lat = nc4_out.createDimension("lat", len(ds.lat.data))
    lon = nc4_out.createDimension("lon", len(ds.lon.data))

    # copying dimentions
    time = nc4_out.createVariable("time", "i4", ("time",))
    days = []
    for i in ds.time.data:
        year = int(str(i).split('T')[0].split('-')[0])
        month = int(str(i).split('T')[0].split('-')[1])
        day = int(str(i).split('T')[0].split('-')[1])
        dt = datetime.datetime(year, month, day) - datetime.datetime(2002, 1, 1)
        days.append(dt.days)
    days = numpy.array(days)
    time[:] = days
    lat = nc4_out.createVariable("lat", "f4", ("lat",))
    lat[:] = ds.lat.data[:]
    lon = nc4_out.createVariable("lon", "f4", ("lon",))
    lon[:] = ds.lon.data[:]
    crs = nc4_out.createVariable("crs", "i4")

    if 'time' in ds.variables:
        var = ds['time']
        if 'standard_name' in var.attrs:
            time.standard_name = var.standard_name
        if 'long_name' in var.attrs:
            time.long_name = "time"
        if 'units' not in var.attrs:
            time.units = "days since 2002-01-01 00:00:00 UTC"
        if 'axis' in var.attrs:
            time.axis = var.axis
        if 'calendar' not in var.attrs:
            time.calendar = "gregorian"
        if 'bounds' in var.attrs:
            time.bounds = var.bounds

    if 'lat' in ds.variables:
        var = ds['lat']
        if 'standard_name' in var.attrs:
            lat.standard_name = var.standard_name
        if 'long_name' in var.attrs:
            lat.long_name = var.long_name
        if 'units' in var.attrs:
            lat.units = var.units
        if 'axis' in var.attrs:
            lat.axis = var.axis

    if 'lon' in ds.variables:
        var = ds['lon']
        if 'standard_name' in var.attrs:
            lon.standard_name = var.standard_name
        if 'long_name' in var.attrs:
            lon.long_name = var.long_name
        if 'units' in var.attrs:
            lon.units = var.units
        if 'axis' in var.attrs:
            lon.axis = var.axis

    #copying variables
    for (name, value) in ds.data_vars.items():
        nc4_vars = nc4_out.createVariable(name, value.dtype, value.dims)
        nc4_vars.setncatts(ds[name].attrs)

    dt = datetime.datetime.utcnow()
    dt = dt.replace(microsecond=0)
    nc4_out.Conventions='CF-1.6'
    nc4_out.title=''
    nc4_out.institution=''
    nc4_out.history='date created: '+ dt.isoformat() +'+00:00'
    nc4_out.references='https://github.com/c-h-david/shbaam/'
    nc4_out.comment=''
    nc4_out.featureType='timeSeries'

    for var in var_list:
        nc4_out[var][:, :, :] = numpy.nan
        for i in range(total):
            lon_index, lat_index = interest_lon[i][0], interest_lat[i][0]
            long_term_mean = avg_dict[var][i]
            for time in range(time_steps):
                nc4_out[var][time,lat_index,lon_index] = ds[var][time, lat_index, lon_index] - long_term_mean

    nc4_out.close()
    print("Success -- creating nc4 file\n")

if __name__ == "__main__":
    files = sys.argv[1:]
    """
    files[0]: concatenated netCDF4 file
    files[1]: given shapefile ('../input/SERVIR_STK/Nepal.shp')
    files[2]: output shapefile with all grid cells from nc4
    files[3]: output csv file
    files[4]: output nc file
    """

    #open netCDF4 file
    print(files[0])
    ds = xr.open_dataset(files[0])
    num_lon = ds.lon.shape[0]
    num_lat = ds.lat.shape[0]
    time_steps = ds.time.shape[0]

    lons = ds.lon.data
    lats = ds.lat.data
    times = ds.time.data

    lon_step = abs(lons[1] - lons[0])
    lat_step = abs(lats[1] - lats[0])
    ds = sum_SM_by_depth(ds)

    all_vars = []
    for varname in ds.data_vars:
        all_vars.append(varname)

    unit_factors = {"mm": 1000, "kg/m2": 1000, "kg/m^2": 1000, "cm": 100, "dm": 10, "m": 1, "km": .001}

    #read polygon shapefile
    polygon = fiona.open(files[1], 'r')
    point_file = files[2]
    createPointShp(polygon, point_file, num_lon, num_lat, lons, lats)

    #open newly created point_file
    pf = fiona.open(point_file, 'r')

    #create spatial index for the bounds of each point
    idx = createRtreeIndex(pf)
    total_interest, interest_lon, interest_lat = findInterest(polygon, pf, idx)

    #calculate surface area for each interest cell
    areas = calculateSurfaceArea(total_interest, num_lat, interest_lat, lon_step, lat_step)
    var_list = all_vars
    avg_dict = dict()
    anomalies_dict = dict()

    #write anomalies to netcdf file, mask all other data points as nan
    for var in var_list:
        print(var)
        vals = ds[var].data
        var_factor = unit_factors[ds[var].units]
        avg = findAvg(vals, total_interest, interest_lon, interest_lat, time_steps)
        anomalies = anomalyTimeseries(vals, var_factor, avg, time_steps, total_interest, interest_lon, interest_lat, areas)
        avg_dict[var] = avg
        anomalies_dict[var] = anomalies

    output_csv = files[3]
    fieldname = ['date'] + var_list
    outputCSV(output_csv, fieldname, times, anomalies_dict)
    output_nc = files[4]
    outputNC(output_nc, ds, total_interest, interest_lon, interest_lat, time_steps, var_list, avg_dict)
    polygon.close()
    pf.close()

    print('Script complete')
