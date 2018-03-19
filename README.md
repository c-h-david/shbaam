# SHBAAM
[![License (3-Clause BSD)](https://img.shields.io/badge/license-BSD%203--Clause-yellow.svg)](https://github.com/c-h-david/shbaam/blob/master/LICENSE)

[![Build Status](https://travis-ci.org/c-h-david/shbaam.svg?branch=master)](https://travis-ci.org/c-h-david/shbaam)

[![Build Status](https://ci.appveyor.com/api/projects/status/github/c-h-david/shbaam?branch=master&svg=true)](https://ci.appveyor.com/project/c-h-david/shbaam)

Satellite Hydrology Bits Analysis And Mapping (SHBAAM) is a Python and bash 
shell toolbox that combines many repetitive pre and post-processing tasks that 
are common to studying the studying the terrestrial water cycle with satellite 
data. 

Such tasks include the preparation of files corresponding to:

- Terrestrial Water Storage Anomaly using GRACE data

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
