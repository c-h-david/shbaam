# SHBAAM
[![License (3-Clause BSD)](https://img.shields.io/badge/license-BSD%203--Clause-yellow.svg)](https://github.com/c-h-david/shbaam/blob/master/LICENSE)

[![Build Status](https://travis-ci.org/c-h-david/shbaam.svg?branch=master)](https://travis-ci.org/c-h-david/shbaam)

[![Build Status](https://ci.appveyor.com/api/projects/status/github/c-h-david/shbaam?branch=master&svg=true)](https://ci.appveyor.com/project/c-h-david/shbaam)

[![Docker Build](https://img.shields.io/docker/automated/chdavid/shbaam.svg)](https://hub.docker.com/r/chdavid/shbaam/)

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

### Install packages
The beauty of Docker is that there is **no need to install anymore packages**.
SHBAAM is ready to go! To run it, just use:

```
$ docker run --rm --name shbaam -it chdavid/shbaam
```

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

## Installation on MacOS
This document was written and tested on a machine with a **clean** image of
MacOS High Sierra (Version 10.13.4) installed.

Note that the experienced users may find more up-to-date installation
instructions in
[.travis.yml](https://github.com/c-h-david/shbaam/blob/master/.travis.yml).

### Download SHBAAM
First, make sure that `brew` is installed:

```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Second, make sure that `git` is installed:

```
$ which git
/usr/bin/git
```

Then download SHBAAM:

```
$ git clone https://github.com/c-h-david/shbaam
```

Finally, enter the SHBAAM directory:

```
$ cd shbaam/
```

### Install Homebrew packages
Software packages for Homebrew are summarized in
[requirements.brw](https://github.com/c-h-david/shbaam/blob/master/requirements.brw)
and can be installed with `brew`. All packages can be installed at once using:

```
$ brew reinstall $(grep -v -E '(^#|^$)' requirements.brw)
```

> Alternatively, one may install the Hoembrew packages listed in
> [requirements.brw](https://github.com/c-h-david/shbaam/blob/master/requirements.brw)
> one by one, for example:
>
> ```
> $ brew reinstall python@2
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
> $ sudo pip install numpy==1.9.3
> ```

## Testing on MacOS
Testing scripts are currently under development.

Note that the experienced users may find more up-to-date testing instructions
in
[.travis.yml](https://github.com/c-h-david/shbaam/blob/master/.travis.yml).

## Installation on Windows 10
This document was written and tested on a machine with a **clean** image of
Windows 10, 64-bit, installed. The following instructions were prepared for
Windows **PowerShell** which shall be run in **administrator mode**.

Note that the experienced users may find more up-to-date installation
instructions in
[.appveyor.yml](https://github.com/c-h-david/shbaam/blob/master/.appveyor.yml).

### Download SHBAAM
First, make sure that `choco` is installed:

```
PS C:\> Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

Second, make sure that `git` is installed:

```
PS C:\> choco install git
```

Then download SHBAAM:

```
PS C:\> git clone https://github.com/c-h-david/shbaam
```

Finally, enter the SHBAAM directory:

```
PS C:\> cd shbaam\
```

### Install Chocolatey packages
Software packages for Chocolatey are summarized in
[requirements.cho](https://github.com/c-h-david/shbaam/blob/master/requirements.cho)
and can be installed with `choco`. All packages can be installed at once using:

```
PS C:\> choco install --no-progress ((gc requirements.cho) -notmatch '^#' -match '\S')
```

> Alternatively, one may install the Chocolatey packages listed in
> [requirements.cho](https://github.com/c-h-david/shbaam/blob/master/requirements.cho)
> one by one, for example:
>
> ```
> PS C:\> choco install miniconda
> ```
>
> Note that by default, `wget` in is aliased to the PowerShell
> `Invoke-WebRequest`, and one may to remove this alias before installing
> `wget`:
>
> ```
> PS C:\> rm Alias:wget
> ```

The Chocolatey installation of `conda`  does not update the environment
variables, so the following action must be taken:

```
PS C:\> $ENV:PATH="C:\\ProgramData\\MiniConda2;C:\\ProgramData\\MiniConda2\\Scripts;$ENV:PATH"
```

The Chocolatey installation of `git`  does not update the environment
variables to give access to `bash` and `sh`, so the following action must be
taken:

```
C:\> $ENV:PATH="C:\\Program Files\\Git\\bin;$ENV:PATH"
```

### Install Anaconda packages
Python packages from the Anaconda Package Repository are summarized in
[requirements.cnd](https://github.com/c-h-david/shbaam/blob/master/requirements.cnd)
and can be installed with `conda`. All packages can be installed at once using:

```
PS C:\> conda install -y -q -c anaconda --file requirements.cnd
```

> Alternatively, one may install the Anaconda packages listed in
> [requirements.cnd](https://github.com/c-h-david/shbaam/blob/master/requirements.cnd)
> one by one, for example:
>
> ```
> PS C:\> conda install -y -q -c anaconda numpy
> ```

## Testing on Windows 10
Testing scripts are currently under development.

Note that the experienced users may find more up-to-date testing instructions
in
[.appveyor.yml](https://github.com/c-h-david/shbaam/blob/master/.appveyor.yml).
