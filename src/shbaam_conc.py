#!/usr/bin/env python3
#*******************************************************************************
#shbaam_conc.py
#*******************************************************************************

#Purpose:
#Given a path to a folder containing GLDAS netCDF files in subdirectories, this
#script concatenates all files into a new netCDF file in the parent folder.
#Author:
#A.J. Purdy, and Cedric H. David, 2019-2020


#*******************************************************************************
#Import Python modules
#*******************************************************************************
import os
import glob
import sys
import xarray as xr


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - fin
# 2 - fout


#*******************************************************************************
#Get command line arguments
#*******************************************************************************
IS_arg=len(sys.argv)
if IS_arg != 3:
     print('ERROR - 2 and only 2 argument can be used')
     raise SystemExit(22)

fin = sys.argv[1]
fout = sys.argv[2]


#*******************************************************************************
#Print input information
#*******************************************************************************
print('Command line inputs')
print('- ' + str(fin))


#*******************************************************************************
#Check if directory exists
#*******************************************************************************
if not os.path.isdir(fin):
     print('ERROR - Directory does not exist: '+fin)
     raise SystemExit(22)

fin=os.path.join(fin,'')
#add trailing slash if it is not there already


#*******************************************************************************
#Check number of files and corresponding model
#*******************************************************************************
print('Check number of files and corresponding model')

MODEL = fin.split('/')[fin.split('/').index('GLDAS')+1].split('_')[1][:-2]
flist = sorted(glob.glob(str(fin) + '*/*.nc4'))

print('- There are '+str(len(flist))+' files from '+MODEL)


#*******************************************************************************
#Concatenating files
#*******************************************************************************
print('Concatenating files')

def get_datespan(ds_all):
    """
    :param ds_all:
    :return: date_range a string of values to use in the filename of the model
    """
    year_start = ds_all.time.data[0].astype('datetime64[Y]').astype(int) + 1970
    year_end = ds_all.time.data[len(ds_all.time.data)-1].astype('datetime64[Y]').astype(int) + 1970
    month_start = ds_all.time.data[0].astype('datetime64[M]').astype(int) % 12 + 1
    month_end = ds_all.time.data[len(ds_all.time.data)-1].astype('datetime64[M]').astype(int) % 12 + 1
    date_range = str(year_start)+str(month_start).zfill(2)+'_'+str(year_end)+str(month_end).zfill(2)
    return date_range

ds_all = xr.merge([xr.open_dataset(f) for f in flist])
print('- Done')


#*******************************************************************************
#Creating output file
#*******************************************************************************
print('Creating output file')

ds_all.to_netcdf(fout)

print('- All monthly files from ' + MODEL + ' combined and saved to: ' + fout)


#*******************************************************************************
#End
#*******************************************************************************
