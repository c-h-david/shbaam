#!/bin/bash
#*******************************************************************************
#tst_pub_dwnl_David_etal_201x_SER.sh
#*******************************************************************************

#Purpose:
#This script downloads all the files corresponding to:
#David, Cédric H., et al. (201x)
#xxx
#DOI: xx.xxxx/xxxxxx
#This script also downloads a subset of the files from:
#Wiese, D. N., F. W. Landerer, and M. M. Watkins (2016), Quantifying and 
#reducing leakage errors in the JPL RL05M GRACE mascon solution, Water Resources
#Research, (52), 7490–7502, 
#DOI: 10.1002/2016WR019344.
#The files used are available from:
#David, Cédric H., et al. (201x)
#xxx
#DOI: xx.xxxx/xxxxxx
#and from:
#Wiese, D. N. (2015), GRACE monthly global water mass grids NETCDF RELEASE 5.0. 
#Ver. 5.0. PO.DAAC, CA, USA. Dataset accessed [YYYY-MM-DD]
#DOI: 10.5067/TEMSC-OCL05
#The script returns the following exit codes
# - 0  if all downloads are successful 
# - 22 if there was a conversion problem
# - 44 if one download is not successful
#Author:
#Cedric H. David, 2018-2018.


#*******************************************************************************
#Notes on tricks used here
#*******************************************************************************
#wget -nv -nc          --> Non-verbose (silent), No-clobber (don't overwrite) 
#tar --strip-components--> Remove leading directory components on extraction
#tar -C                --> Specify where to extract 


#*******************************************************************************
#Publication message
#*******************************************************************************
echo "********************"
echo "Downloading files from:   http://dx.doi.org/xx.xxxx/xxxxxx"
echo "                          ftp://podaac.jpl.nasa.gov/allData/tellus/L3/mascon/RL05/JPL/CRI/netcdf/"
echo "which correspond to   :   http://dx.doi.org/xx.xxxx/xxxxxx/"
echo "                          http://dx.doi.org/10.1002/2016WR019344"
echo "These files are under a Creative Commons Attribution (CC BY) license."
echo "Please cite these four DOIs if using these files for your publications."
echo "********************"


#*******************************************************************************
#Download current GRACE files
#*******************************************************************************

#-------------------------------------------------------------------------------
#Download parameters
#-------------------------------------------------------------------------------
URL="ftp://podaac.jpl.nasa.gov/allData/tellus/L3/mascon/RL05/JPL/CRI/netcdf/"

folder="../input/GRACE"

list="                                                                         \
      CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.nc                                   \
      CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.nc.md5                               \
      JPL_MSCNv01_PLACEMENT.nc                                                 \
      LAND_MASK.CRIv01.nc                                                      \
      LAND_MASK.CRIv01.nc.md5                                                  \
    "

#-------------------------------------------------------------------------------
#Download process
#-------------------------------------------------------------------------------
mkdir -p $folder
for file in $list
do
     wget -nv -nc $URL/$file -P $folder
     if [ $? -gt 0 ] ; then echo "Problem downloading $file" >&2 ; exit 44 ; fi
done

#-------------------------------------------------------------------------------
#Check downloads
#-------------------------------------------------------------------------------
cd $folder
md5sum -c CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.nc.md5                           \
          LAND_MASK.CRIv01.nc.md5
if [ $? -gt 0 ] ; then echo "Problem Checking file" >&2 ; exit 44 ; fi
cd -


#*******************************************************************************
#Download retired GRACE files
#*******************************************************************************

#-------------------------------------------------------------------------------
#Download parameters
#-------------------------------------------------------------------------------
URL="ftp://podaac.jpl.nasa.gov/allData/tellus/retired/L3/mascon/RL05/JPL/CRI/netcdf/"


folder="../input/GRACE"

list="                                                                         \
      GRCTellus.JPL.200204_201608.GLO.RL05M_1.MSCNv02CRIv02.nc                 \
      GRCTellus.JPL.200204_201608.GLO.RL05M_1.MSCNv02CRIv02.nc.md5             \
    "

#-------------------------------------------------------------------------------
#Download process
#-------------------------------------------------------------------------------
mkdir -p $folder
for file in $list
do
     wget -nv -nc $URL/$file -P $folder
     if [ $? -gt 0 ] ; then echo "Problem downloading $file" >&2 ; exit 44 ; fi
done

#-------------------------------------------------------------------------------
#Check downloads
#-------------------------------------------------------------------------------
cd $folder
md5sum -c GRCTellus.JPL.200204_201608.GLO.RL05M_1.MSCNv02CRIv02.nc.md5
cd -


#*******************************************************************************
#Download SHBAAM input files
#*******************************************************************************

#-------------------------------------------------------------------------------
#Download parameters
#-------------------------------------------------------------------------------
URL="http://rapid-hub.org/data/CI/SERVIR_STK"
folder="../input/SERVIR_STK"
list="                                                                         \
      Nepal.zip                                                                \
     "

#-------------------------------------------------------------------------------
#Download process
#-------------------------------------------------------------------------------
mkdir -p $folder
for file in $list
do
     wget -nv -nc $URL/$file -P $folder
     if [ $? -gt 0 ] ; then echo "Problem downloading $file" >&2 ; exit 44 ; fi
done


#*******************************************************************************
#Download SHBAAM output files
#*******************************************************************************

#-------------------------------------------------------------------------------
#Download parameters
#-------------------------------------------------------------------------------
URL="http://rapid-hub.org/data/CI/SERVIR_STK"
folder="../output/SERVIR_STK"
list="                                                                         \
      map_Nepal.nc                                                             \
      timeseries_Nepal.csv                                                     \
     "

#-------------------------------------------------------------------------------
#Download process
#-------------------------------------------------------------------------------
mkdir -p $folder
for file in $list
do
     wget -nv -nc $URL/$file -P $folder
     if [ $? -gt 0 ] ; then echo "Problem downloading $file" >&2 ; exit 44 ; fi
done


#*******************************************************************************
#Convert legacy files
#*******************************************************************************
unzip -nq ../input/SERVIR_STK/Nepal.zip -d ../input/SERVIR_STK/
if [ $? -gt 0 ] ; then echo "Problem converting" >&2 ; exit 22 ; fi


#*******************************************************************************
#Done
#*******************************************************************************
