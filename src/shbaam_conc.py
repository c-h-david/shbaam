#!/usr/bin/env python

#*******************************************************************************
#shbaam_conc.py
#*******************************************************************************

#Purpose:
#Given a folder path with list of files, this script
#concatenates all files from a GLDAS model and then removes the downloaded indidual subset files stored in the same folder
#Author:
#A.J. Purdy, 2019


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


#*******************************************************************************
#Get command line arguments
#*******************************************************************************
fin = sys.argv[1:]

#*******************************************************************************
#Print input information
#*******************************************************************************
print('Command line inputs')
print('- ' + str(fin[0]))
flist = sorted(glob.glob(str(fin[0]) + '*/*.nc4'))

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


MODEL = fin[0].split('/')[fin[0].split('/').index('GLDAS')+1].split('_')[1][:-2]

print('There are '+str(len(flist))+' files from '+MODEL)
ds_all = xr.merge([xr.open_dataset(f) for f in flist])
OUT_DIR = '/'.join(fin[0].split('/')[0:fin[0].split('/').index('GLDAS')+1])+'/'

out_fname = flist[0].split('/')[-1].split('.')[0] + '.A' + get_datespan(ds_all) + '.nc'
ds_all.to_netcdf(OUT_DIR + out_fname)

print('all monthly files from ' + MODEL + ' combined and saved to:\n\t' + OUT_DIR + out_fname)

