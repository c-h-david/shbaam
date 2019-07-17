# SHBAAM
[![License (3-Clause BSD)](https://img.shields.io/badge/license-BSD%203--Clause-yellow.svg)](https://github.com/c-h-david/shbaam/blob/master/LICENSE)

[![Build Status](https://travis-ci.org/c-h-david/shbaam.svg?branch=master)](https://travis-ci.org/c-h-david/shbaam)

[![Docker Build](https://img.shields.io/docker/cloud/build/chdavid/shbaam.svg)](https://hub.docker.com/r/chdavid/shbaam/)

Satellite Hydrology Bits Analysis And Mapping (SHBAAM) is a Python and bash 
shell toolbox that combines many repetitive pre and post-processing tasks that 
are common to studying the studying the terrestrial water cycle with satellite 
data. 

Such tasks include the preparation of files corresponding to:

- Terrestrial Water Storage Anomaly using GRACE data

## Installation with Docker
Installing SHBAAM is **by far the easiest with Docker**. This document was
written and tested using
[Docker Community Edition](https://www.docker.com/community-edition#/download)
which is available for free and can be installed on a wide variety of operating
systems. To install it, follow the instructions in the link provided above.

Note that the experienced users may find more up-to-date installation
instructions in
[Dockerfile](https://github.com/c-h-david/shbaam/blob/master/Dockerfile).

### Download SHBAAM
Downloading SHBAAM with Docker can be done using:

```
$ docker pull chdavid/shbaam
```

### Run SHBAAM
The beauty of Docker is that there is **no need to install anymore packages**.
SHBAAM is ready to go! To run it, just use:

```
$ docker run --rm -it chdavid/shbaam
```

Or, if you'd like to run the Jupyter tutorial instead, you should first start
with:

```
$ docker run --rm -it -p 8888:8888 chdavid/shbaam jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

You'll see that two URLs will be suggested, for example:

```
    Copy and paste one of these URLs:
        http://(0123456789ab or 127.0.0.1):8888/?token=0123456789abcdefghijklmnopqrstuvwxyz0123456789ab
```

You then just need to extract one of the suggested URLs, and paste it in the
address bar of your internet browser. Note that the URLs are randomly generated
each time for security reasons. With the example above, you would use:
`http://127.0.0.1:8888/?token=0123456789abcdefghijklmnopqrstuvwxyz0123456789ab`
to access the Jupyter dashboard from your internet browser. Finally, click on
`TUTORIAL.ipynb` within the Jupyter dashboard.

## Testing with Docker
Testing scripts are currently under development.

Note that the experienced users may find more up-to-date testing instructions
in
[.docker.test.yml](https://github.com/c-h-david/shbaam/blob/master/.docker.test.yml).

## Installation on Ubuntu
This document was written and tested on a machine with a **clean** image of 
[Ubuntu 14.04.0 Desktop 64-bit](http://old-releases.ubuntu.com/releases/14.04.0/ubuntu-14.04-desktop-amd64.iso)
installed, *i.e.* **no update** was performed, and **no upgrade** either.

Note that the experienced users may find more up-to-date installation 
instructions in
[.travis.yml](https://github.com/c-h-david/shbaam/blob/master/.travis.yml).

### Download SHBAAM
First, make sure that `git` is installed: 

```
$ sudo apt-get install -y git
```

Then download SHBAAM:

```
$ git clone https://github.com/c-h-david/shbaam
```

Finally, enter the SHBAAM directory:

```
$ cd shbaam/
```

### Install APT packages
Software packages for the Advanced Packaging Tool (APT) are summarized in 
[requirements.apt](https://github.com/c-h-david/shbaam/blob/master/requirements.apt)
and can be installed with `apt-get`. All packages can be installed at once using:

```
$ sudo apt-get install -y $(grep -v -E '(^#|^$)' requirements.apt)
```

> Alternatively, one may install the APT packages listed in 
> [requirements.apt](https://github.com/c-h-david/shbaam/blob/master/requirements.apt)
> one by one, for example:
>
> ```
> $ sudo apt-get install -y python-pip
>```

### Install Python packages
Python packages from the Python Package Index (PyPI) are summarized in 
[requirements.pip](https://github.com/c-h-david/shbaam/blob/master/requirements.pip)
and can be installed with `pip`. All packages can be installed at once using:

```
$ sudo pip install -r requirements.pip
```

> Alternatively, one may install the PyPI packages listed in 
> [requirements.pip](https://github.com/c-h-david/shbaam/blob/master/requirements.pip)
> one by one, for example:
>
> ```
> $ sudo pip install numpy==1.7.0
> ```

## Testing on Ubuntu
Testing scripts are currently under development.

Note that the experienced users may find more up-to-date testing instructions 
in
[.travis.yml](https://github.com/c-h-david/shbaam/blob/master/.travis.yml).

