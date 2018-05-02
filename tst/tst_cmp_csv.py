#!/usr/bin/env python
#*******************************************************************************
#tst_cmp_csv.py
#*******************************************************************************

#Purpose:
#Compare csv files.
#Author:
#Cedric H. David, 2015-2018


#*******************************************************************************
#Prerequisites
#*******************************************************************************
import sys
import csv


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - csv_file1
# 2 - csv_file2
#(3)- relative tolerance 
#(4)- absolute tolerance 


#*******************************************************************************
#Get command line arguments
#*******************************************************************************
IS_arg=len(sys.argv)
if IS_arg < 3 or IS_arg > 5:
     print('ERROR - A minimum of 2 and a maximum of 4 arguments can be used')
     raise SystemExit(22) 

csv_file1=sys.argv[1]
csv_file2=sys.argv[2]
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
print('Comparing CSV files')
print('1st CSV file                  :'+csv_file1)
print('2nd CSV file                  :'+csv_file2)
print('Relative tolerance            :'+str(ZS_rtol))
print('Absolute tolerance            :'+str(ZS_atol))
print('-------------------------------')


#*******************************************************************************
#Test if input files exist
#*******************************************************************************
try:
     with open(csv_file1) as file:
          pass
except IOError as e:
     print('Unable to open '+csv_file1)
     raise SystemExit(22) 

try:
     with open(csv_file2) as file:
          pass
except IOError as e:
     print('Unable to open '+csv_file2)
     raise SystemExit(22) 


#*******************************************************************************
#Read all files
#*******************************************************************************
ZM_csv1=[]
IS_col1=0
with open(csv_file1) as csv_file:
     reader=csv.reader(csv_file,dialect='excel')
     for row in reader:
          row=filter(lambda x: x!='',row)
          #Removes the empty strings created by csv.reader for trailing commas
          for JS_col in range(len(row)):
               try:
                    row[JS_col]=int(row[JS_col])
               except ValueError:
                    try:
                         row[JS_col]=float(row[JS_col])
                    except ValueError:
                         row[JS_col]=str(row[JS_col])
          ZM_csv1.append(row)
IS_row1=len(ZM_csv1)
IS_col1=len(row)

for row in ZM_csv1:
     if len(row) != IS_col1:
     #Check that the number of columns is always the same
          print('ERROR - Inconsistent number of columns in '+csv_file1)
          raise SystemExit(22) 

ZM_csv2=[]
IS_col2=0
with open(csv_file2) as csv_file:
     reader=csv.reader(csv_file,dialect='excel')
     for row in reader:
          row=filter(lambda x: x!='',row)
          #Removes the empty strings created by csv.reader for trailing commas
          for JS_col in range(len(row)):
               try:
                    row[JS_col]=int(row[JS_col])
               except ValueError:
                    try:
                         row[JS_col]=float(row[JS_col])
                    except ValueError:
                         row[JS_col]=str(row[JS_col])
          ZM_csv2.append(row)
IS_row2=len(ZM_csv2)
IS_col2=len(row)

for row in ZM_csv2:
     if len(row) != IS_col2:
     #Check that the number of columns is always the same
          print('ERROR - Inconsistent number of columns in '+csv_file2)
          raise SystemExit(22) 


#*******************************************************************************
#Compare file sizes 
#*******************************************************************************
if IS_row1==IS_row2:
     IS_row=IS_row1
     print('Common number of rows: '+str(IS_row))
else:
     print('ERROR - The number of rows are different: '                        \
           +str(IS_row1)+' <> '+str(IS_row2))
     raise SystemExit(99) 

if IS_col1==IS_col2:
     IS_col=IS_col1
     print('Common number of columns: '+str(IS_col))
else:
     print('ERROR - The number of columns are different: '                     \
           +str(IS_col1)+' <> '+str(IS_col2))
     raise SystemExit(99) 

print('-------------------------------')


#*******************************************************************************
#Compute differences 
#*******************************************************************************
ZS_rdif_max=float(0)
ZS_adif_max=float(0)
for JS_row in range(IS_row):
     for JS_col in range(IS_col):
          if type(ZM_csv1[JS_row][JS_col]) is str:
               if ZM_csv1[JS_row][JS_col].strip()                              \
                ==ZM_csv2[JS_row][JS_col].strip():
                    ZS_adif=0
                    ZS_rdif=0
               else:
                    print('ERROR!!! in comparison of strings: '+               \
                           ZM_csv1[JS_row][JS_col]+' differs from '+           \
                           ZM_csv2[JS_row][JS_col])
                    raise SystemExit(99) 
          else:
               ZS_adif=abs(ZM_csv1[JS_row][JS_col]-ZM_csv2[JS_row][JS_col])
               #Absolute difference computed
               if ZS_adif == 0:
                    ZS_rdif=0
               else:
                    ZS_rdif=2*ZS_adif/                                         \
                            abs(ZM_csv1[JS_row][JS_col]+ZM_csv2[JS_row][JS_col])
               #Relative difference computed
          if ZS_adif > ZS_adif_max:
               ZS_adif_max=ZS_adif
          #Maximum absolute difference updated
          if ZS_rdif > ZS_rdif_max:
               ZS_rdif_max=ZS_rdif
          #Maximum relative difference updated

print('Max relative difference       :'+str(ZS_rdif_max))
print('Max absolute difference       :'+str(ZS_adif_max))
print('-------------------------------')


#*******************************************************************************
#Compare csv files
#*******************************************************************************
if ZS_rdif_max > ZS_rtol:
     print('Unacceptable rel. difference!!!')
     print('-------------------------------')
     raise SystemExit(99) 

if ZS_adif_max > ZS_atol:
     print('Unacceptable abs. difference!!!')
     print('-------------------------------')
     raise SystemExit(99) 

print('CSV files similar!!!')
print('Passed all tests!!!')
print('-------------------------------')


#*******************************************************************************
#End
#*******************************************************************************
