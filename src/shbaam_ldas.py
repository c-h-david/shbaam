#!/usr/bin/env python
#*******************************************************************************
#shbaam_ldas.py
#*******************************************************************************

#Purpose:
#Given and model name, a start date, an end date, and a folder path, this script
#downloads LDAS data from GES-DISC using the NASA EarthData credentials stored
#locally in '~/.netrc' file.
#Author:
#Cedric H. David, 2018-2018


#*******************************************************************************
#Import Python modules
#*******************************************************************************
import sys
import os.path
import datetime
import requests


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - rrr_lsm_mod
# 2 - rrr_iso_beg
# 3 - rrr_iso_end
# 4 - rrr_lsm_dir


#*******************************************************************************
#Get command line arguments
#*******************************************************************************
IS_arg=len(sys.argv)
if IS_arg != 5:
     print('ERROR - 4 and only 4 arguments can be used')
     raise SystemExit(22) 

rrr_lsm_mod=sys.argv[1]
rrr_iso_beg=sys.argv[2]
rrr_iso_end=sys.argv[3]
rrr_lsm_dir=sys.argv[4]


#*******************************************************************************
#Print input information
#*******************************************************************************
print('Command line inputs')
print('- '+rrr_lsm_mod)
print('- '+rrr_iso_beg)
print('- '+rrr_iso_end)
print('- '+rrr_lsm_dir)


#*******************************************************************************
#Check if directory exists 
#*******************************************************************************
rrr_lsm_dir=os.path.join(rrr_lsm_dir,'')
#add trailing slash if it is not there

if not os.path.isdir(rrr_lsm_dir):
     os.mkdir(rrr_lsm_dir)


#*******************************************************************************
#Check LDAS arguments
#*******************************************************************************
print('Check LDAS arguments')

if rrr_lsm_mod=='VIC' or rrr_lsm_mod=='NOAH' or rrr_lsm_mod=='MOS'             \
                      or rrr_lsm_mod=='CLM':
     print('- Model name is valid')
else:
     print('ERROR - Invalid model name')
     raise SystemExit(22) 


#*******************************************************************************
#Check temporal information
#*******************************************************************************
print('Check temporal information')

rrr_dat_beg=datetime.datetime.strptime(rrr_iso_beg,'%Y-%m-%dT%H:%M:%S')
rrr_dat_end=datetime.datetime.strptime(rrr_iso_end,'%Y-%m-%dT%H:%M:%S')

if rrr_dat_end>=rrr_dat_beg:
     print('- Beginning of interval is before end of interval')
else:
     print('ERROR - Beginning of interval is NOT before end of interval')
     raise SystemExit(22) 

rrr_dat_stp=rrr_dat_beg
IS_count=0
#Initialized when to stop downloading and the number of files to download

#-------------------------------------------------------------------------------
#If requesting monthly data
#-------------------------------------------------------------------------------
if rrr_dat_beg.day==1 and rrr_dat_beg.hour==0 and                              \
   rrr_dat_beg.minute==0 and rrr_dat_beg.second==0:
     print('- Interval starts at the top of a month')
else:
     print('ERROR - The interval does NOT start at the top of a month: '       \
           +rrr_iso_beg)
     raise SystemExit(22) 

while rrr_dat_stp<=rrr_dat_end:
     rrr_dat_stp=(rrr_dat_stp+datetime.timedelta(days=32)).replace(day=1)
     #Adding one month done by adding 32 days and replacing the day by 1
     IS_count=IS_count+1
print('- The number of files to be downloaded is: '+str(IS_count))


#*******************************************************************************
#Obtaining credentials for the server from a local file
#*******************************************************************************
print('Obtaining credentials for the server from a local file')

url='https://urs.earthdata.nasa.gov'
print('- '+url)

cred=requests.utils.get_netrc_auth(url)
print('- The credentials were obtained from ~/.netrc file')


#*******************************************************************************
#Checking that service and credentials work for one known file
#*******************************************************************************

#-------------------------------------------------------------------------------
#If requesting monthly data
#-------------------------------------------------------------------------------

print('Checking that service and credentials work for one known file')

url='https://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi'
payload={}
payload['FILENAME']='/data/GLDAS_V1/GLDAS_VIC10_M/2000/'                       \
                   +'GLDAS_VIC10_M.A200001.001.grb'
payload['FORMAT']='bmM0Lw'
payload['BBOX']='-60,-180,90,180'
payload['LABEL']='GLDAS_VIC10_M.A200001.001.grb.SUB.nc4'
payload['SHORTNAME']='GLDAS_VIC10_M'
payload['SERVICE']='L34RS_LDAS'
payload['VERSION']='1.02'
payload['DATASET_VERSION']='001'
payload['VARIABLES']='SWE,SoilM1,SoilMoist1,Canint,Canopint'
#Note, variable names change among models:
#- Noah:   SWE, SoilMoist1, Canopint
#- VIC:    SWE, SoilM1,     Canint
#- Mosaic: SWE, SoilMoist1, Canopint
#- CLM:    SWE, SoilMoist1, Canopint

print('- Requesting a subset of GLDAS_VIC10_M.A200001.001.grb')
s=requests.session()
s.max_redirects=200
r=s.get(url, params=payload, auth=cred)
s.close()
#Downloads data from:
#https://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi
#     ?FILENAME=/data/GLDAS_V1/GLDAS_VIC10_M/2000/
#     GLDAS_VIC10_M.A200001.001.grb
#     &FORMAT=bmM0Lw
#     &BBOX=-60,-180,90,180
#     &LABEL=GLDAS_VIC10_M.A200001.001.grb.SUB.nc4
#     &SHORTNAME=GLDAS_VIC10_M
#     &SERVICE=L34RS_LDAS
#     &VERSION=1.02
#     &DATASET_VERSION=001
#     &VARIABLES=SoilM1,SWE
#requests.get() actually downloads the file into memory and also saves some
#associated download metadata
if r.ok:
     print('- The request was successful')
else:
     print('ERROR - Status code '+str(r.status_code))
     raise SystemExit(22)


#*******************************************************************************
#Downloading all files
#*******************************************************************************
print('Downloading all files')

#-------------------------------------------------------------------------------
#Creating a networking session and assigning associated credentials
#-------------------------------------------------------------------------------
print('- Creating a networking session and assigning associated credentials')

s=requests.Session()
s.max_redirects=200
s.auth=cred

     
#-------------------------------------------------------------------------------
#If requesting monthly data
#-------------------------------------------------------------------------------

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Initializing URL and payload
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print('- Initializing URL and payload')

url='https://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/OTF/HTTP_services.cgi'
payload={}
payload['FILENAME']='/data/GLDAS_V1/GLDAS_VIC10_M/2000/'                       \
                   +'GLDAS_VIC10_M.A200001.001.grb'
payload['FORMAT']='bmM0Lw'
payload['BBOX']='-60,-180,90,180'
payload['LABEL']='GLDAS_VIC10_M.A200001.001.grb.SUB.nc4'
payload['SHORTNAME']='GLDAS_VIC10_M'
payload['SERVICE']='L34RS_LDAS'
payload['VERSION']='1.02'
payload['DATASET_VERSION']='001'
payload['VARIABLES']='SWE,SoilM1,SoilMoist1,Canint,Canopint'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Looping over all files
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print('- Looping over all files')

rrr_dat_cur=rrr_dat_beg
for JS_count in range(IS_count):
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     #Determine current datetime and various date strings
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     YS_yr=rrr_dat_cur.strftime('%Y')
     YS_mo=rrr_dat_cur.strftime('%m')
     YS_da=rrr_dat_cur.strftime('%d')
     YS_hr=rrr_dat_cur.strftime('%H')
     YS_dy=rrr_dat_cur.strftime('%j')
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     #Generate file name
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     payload['FILENAME']='/data/GLDAS_V1/GLDAS_'+rrr_lsm_mod+'10_M/'           \
                        +YS_yr+'/'                                             \
                        +'GLDAS_'+rrr_lsm_mod+'10_M.A'+YS_yr+''+YS_mo          \
                        +'.001.grb'
     payload['LABEL']   ='GLDAS_'+rrr_lsm_mod+'10_M.A'+YS_yr+''+YS_mo          \
                        +'.001.grb.SUB.nc4'
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     #Create directory if it doesn't exist
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     YS_dir='GLDAS_'+rrr_lsm_mod+'10_M/'+YS_yr+'/'
     if not os.path.isdir(rrr_lsm_dir+YS_dir):
          os.makedirs(rrr_lsm_dir+YS_dir)
     #Update directory name and make sure it exists
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     #Place request if file does not already exist, and check it is ok
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     if os.path.isfile(rrr_lsm_dir+YS_dir+payload['LABEL']):
          print(' . Skipping '+payload['LABEL'])
     else:
          print(' . Downloading '+payload['LABEL'])
          r=s.get(url, params=payload)
          if not r.ok:
               print('ERROR - status code '+str(r.status_code)+                \
                     'returned when downloading '+payload['FILENAME'])
               raise SystemExit(22)
          YS_name=r.headers['content-disposition']
          YS_name=YS_name.replace('attachment; filename=','')
          YS_name=YS_name.replace('"','')
          #The file name is extracted directly from requests.get() results
          open(rrr_lsm_dir+YS_dir+YS_name, 'wb').write(r.content)
          #The file is written on local disk
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     #Increment current datetime
     # - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + - + -
     rrr_dat_cur=(rrr_dat_cur+datetime.timedelta(days=32)).replace(day=1)
     
#-------------------------------------------------------------------------------
#Closing the networking session
#-------------------------------------------------------------------------------
print('- Closing the networking session')

s.close()


#*******************************************************************************
#End
#*******************************************************************************
