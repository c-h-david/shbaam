#*******************************************************************************
#Dockerfile
#*******************************************************************************

#Purpose:
#This file describes the operating system prerequisites for SHBAAM, and is used
#by the Docker software.
#Author:
#Cedric H. David, 2018-2020


#*******************************************************************************
#Usage
#*******************************************************************************
#docker build -t shbaam:myimage -f Dockerfile .          #Create image
#docker run --rm --name shbaam_mycontainer     \
#           -it shbaam:myimage                           #Run image in container
#docker run --rm --name shbaam_mycontainer     \
#           -v $PWD/input:/home/shbaam/input   \
#           -v $PWD/output:/home/shbaam/output \
#           -it shbaam:myimage                           #Run and map volumes
#docker save -o shbaam_myimage.tar shbaam:myimage        #Save a copy of image
#docker load -i shbaam_myimage.tar                       #Load a saved image
#docker commit containerID shbaam:myimage2               #Save image from contID
#docker start -a -i containerID                          #Restart a container


#*******************************************************************************
#Operating System
#*******************************************************************************
FROM debian:stretch-slim


#*******************************************************************************
#Copy files into Docker image (this ignores the files listed in .dockerignore)
#*******************************************************************************
WORKDIR /home/shbaam/
COPY . . 


#*******************************************************************************
#Operating System Requirements
#*******************************************************************************
RUN  apt-get update && \
     apt-get install -y --no-install-recommends $(grep -v -E '(^#|^$)' requirements.apt) && \
     rm -rf /var/lib/apt/lists/*


#*******************************************************************************
#Python requirements
#*******************************************************************************
ADD https://bootstrap.pypa.io/get-pip.py .
RUN python3 get-pip.py --no-cache-dir \
    `grep 'pip==' requirements.pip` \
    `grep 'setuptools==' requirements.pip` \
    `grep 'wheel==' requirements.pip` && \
    rm get-pip.py

RUN pip3 install --no-cache-dir -r requirements.pip


#*******************************************************************************
#Intended (default) command at execution of image (not used during build)
#*******************************************************************************
CMD  /bin/bash


#*******************************************************************************
#End
#*******************************************************************************
