#!/bin/sh
#*******************************************************************************
#version.sh
#*******************************************************************************

#Purpose:
#This script allows determining the version of SHBAAM that is being used, but 
#only if git is installed and if the SHBAAM git repository is present.  
#Otherwise 'unknown' is used.  
#Author:
#Cedric H. David, 2017-2018


#*******************************************************************************
#Check if a program exists and perform tasks
#*******************************************************************************
if command -v git > /dev/null 2>&1; then
     #git is installed
     if git rev-parse --git-dir > /dev/null 2>&1; then
          #this is a git repository
          git describe --always
     else
          #this is not a git repository
          echo "unknown, NOT a git repository"
     fi
else
     #git is not installed
     echo "unknown, git NOT installed"
fi


#*******************************************************************************
#end
#*******************************************************************************
