#!/bin/sh
#*******************************************************************************
#tst_pub_repr_David_etal_SER.sh
#*******************************************************************************

#Purpose:
#This script reproduces all SHBAAM processing steps used in the writing of:
#David, Cédric H., et al. (201x)
#xxx
#DOI: xx.xxxx/xxxxxx
#The files used are available from:
#David, Cédric H., et al. (201x)
#xxx
#DOI: xx.xxxx/xxxxxx
#The following are the possible arguments:
# - No argument: all unit tests are run
# - One unique unit test number: this test is run
# - Two unit test numbers: all tests between those (included) are run
#The script returns the following exit codes
# - 0  if all experiments are successful 
# - 22 if some arguments are faulty 
# - 99 if a comparison failed 
#Author:
#Cedric H. David, 2018-2018


#*******************************************************************************
#Publication message
#*******************************************************************************
echo "********************"
echo "Reproducing files for: http://dx.doi.org/xx.xxxx/"
echo "********************"


#*******************************************************************************
#Select which unit tests to perform based on inputs to this shell script
#*******************************************************************************
if [ "$#" = "0" ]; then
     fst=1
     lst=99
     echo "Performing all unit tests: 1-99"
     echo "********************"
fi 
#Perform all unit tests if no options are given 

if [ "$#" = "1" ]; then
     fst=$1
     lst=$1
     echo "Performing one unit test: $1"
     echo "********************"
fi 
#Perform one single unit test if one option is given 

if [ "$#" = "2" ]; then
     fst=$1
     lst=$2
     echo "Performing unit tests: $1-$2"
     echo "********************"
fi 
#Perform all unit tests between first and second option given (both included) 

if [ "$#" -gt "2" ]; then
     echo "A maximum of two options can be used" 1>&2
     exit 22
fi 
#Exit if more than two options are given 


#*******************************************************************************
#Initialize count for unit tests
#*******************************************************************************
unt=0


#*******************************************************************************
#Terrestrial water storage anomalies, Nepal
#*******************************************************************************
unt=$((unt+1))
if [ "$unt" -ge "$fst" ] && [ "$unt" -le "$lst" ] ; then
echo "Running unit test $unt/x"
run_file=tmp_run_$unt.txt
cmp_file=tmp_cmp_$unt.txt

echo "- Terrestrial water storage anomalies, Nepal"
../src/shbaam_twsa.py                                                          \
     ../input/GRACE/GRCTellus.JPL.200204_201608.GLO.RL05M_1.MSCNv02CRIv02.nc   \
     ../input/GRACE/CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.nc                     \
     ../input/SERVIR_STK/Nepal.shp                                             \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt_tst.shp                            \
     ../output/SERVIR_STK/timeseries_Nepal_tst.csv                             \
     ../output/SERVIR_STK/map_Nepal_tst.nc                                     \
     > $run_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed run: $run_file" >&2 ; exit $x ; fi

echo "- Comparing shapefiles"
./tst_cmp_shp.py                                                               \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt.shp                                \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt_tst.shp                            \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

echo "- Comparing timeseries"
./tst_cmp_csv.py                                                               \
     ../output/SERVIR_STK/timeseries_Nepal.csv                                 \
     ../output/SERVIR_STK/timeseries_Nepal_tst.csv                             \
     1e-6                                                                      \
     1e-6                                                                      \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

echo "- Comparing maps"
./tst_cmp_n3d.py                                                               \
     ../output/SERVIR_STK/map_Nepal.nc                                         \
     ../output/SERVIR_STK/map_Nepal_tst.nc                                     \
     1e-6                                                                      \
     1e-6                                                                      \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

rm -f $run_file
rm -f $cmp_file
echo "Success"
echo "********************"
fi


#*******************************************************************************
#Terrestrial water storage anomalies, FourDoabs
#*******************************************************************************
unt=$((unt+1))
if [ "$unt" -ge "$fst" ] && [ "$unt" -le "$lst" ] ; then
echo "Running unit test $unt/x"
run_file=tmp_run_$unt.txt
cmp_file=tmp_cmp_$unt.txt

echo "- Terrestrial water storage anomalies, FourDoabs"
../src/shbaam_twsa.py                                                          \
     ../input/GRACE/GRCTellus.JPL.200204_201608.GLO.RL05M_1.MSCNv02CRIv02.nc   \
     ../input/GRACE/CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.nc                     \
     ../input/SERVIR_STK/FourDoabs.shp                                         \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt_tst.shp                            \
     ../output/SERVIR_STK/timeseries_FourDoabs_tst.csv                         \
     ../output/SERVIR_STK/map_FourDoabs_tst.nc                                 \
     > $run_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed run: $run_file" >&2 ; exit $x ; fi

echo "- Comparing shapefiles"
./tst_cmp_shp.py                                                               \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt.shp                                \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt_tst.shp                            \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

echo "- Comparing timeseries"
./tst_cmp_csv.py                                                               \
     ../output/SERVIR_STK/timeseries_FourDoabs.csv                             \
     ../output/SERVIR_STK/timeseries_FourDoabs_tst.csv                         \
     1e-6                                                                      \
     1e-6                                                                      \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

echo "- Comparing maps"
./tst_cmp_n3d.py                                                               \
     ../output/SERVIR_STK/map_FourDoabs.nc                                     \
     ../output/SERVIR_STK/map_FourDoabs_tst.nc                                 \
     1e-6                                                                      \
     1e-6                                                                      \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

rm -f $run_file
rm -f $cmp_file
echo "Success"
echo "********************"
fi


#*******************************************************************************
#Terrestrial water storage anomalies, NorthWestBD
#*******************************************************************************
unt=$((unt+1))
if [ "$unt" -ge "$fst" ] && [ "$unt" -le "$lst" ] ; then
echo "Running unit test $unt/x"
run_file=tmp_run_$unt.txt
cmp_file=tmp_cmp_$unt.txt

echo "- Terrestrial water storage anomalies, NorthWestBD"
../src/shbaam_twsa.py                                                          \
     ../input/GRACE/GRCTellus.JPL.200204_201608.GLO.RL05M_1.MSCNv02CRIv02.nc   \
     ../input/GRACE/CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.nc                     \
     ../input/SERVIR_STK/NorthWestBD.shp                                       \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt_tst.shp                            \
     ../output/SERVIR_STK/timeseries_NorthWestBD_tst.csv                       \
     ../output/SERVIR_STK/map_NorthWestBD_tst.nc                               \
     > $run_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed run: $run_file" >&2 ; exit $x ; fi

echo "- Comparing shapefiles"
./tst_cmp_shp.py                                                               \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt.shp                                \
     ../output/SERVIR_STK/GRCTellus.JPL.pnt_tst.shp                            \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

echo "- Comparing timeseries"
./tst_cmp_csv.py                                                               \
     ../output/SERVIR_STK/timeseries_NorthWestBD.csv                           \
     ../output/SERVIR_STK/timeseries_NorthWestBD_tst.csv                       \
     1e-6                                                                      \
     1e-6                                                                      \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

echo "- Comparing maps"
./tst_cmp_n3d.py                                                               \
     ../output/SERVIR_STK/map_NorthWestBD.nc                                   \
     ../output/SERVIR_STK/map_NorthWestBD_tst.nc                               \
     1e-6                                                                      \
     1e-6                                                                      \
     > $cmp_file
x=$? && if [ $x -gt 0 ] ; then echo "Failed comparison: $cmp_file" >&2 ; exit $x ; fi

rm -f $run_file
rm -f $cmp_file
echo "Success"
echo "********************"
fi


#*******************************************************************************
#Clean up
#*******************************************************************************
rm -f ../output/SERVIR_STK/*_tst.*


#*******************************************************************************
#End
#*******************************************************************************
echo "Passed all tests!!!"
echo "********************"
