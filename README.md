# NHCC

# Developer: Gregory Rose (gregory.rose@optusnet.com.au)

NHCC Rider and Grading database

Steps to use:


Windows:


If not already installed, install python:

NOTE: When the install window comes up, tick the box to add "Add Python 3.10 to PATH"
	
	https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe

If not already installed, install git:

	https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-64-bit.exe

Download NHCC files from GIT:

from command prompt
> git clone https://github.com/gregoryarose/NHCC.git

Confirm location of NHCC folder, should be C:\users\[your username]\NHCC


Install required packages:
>cd NHCC

> pip3 install -r requirements.txt 

 
*************************************************************************************

ON MAC:

Git is probably installed - to check, open terminal and enter the below command:

    $ git --version  

The above command will display the installed version of Git.

Output:

git version 2.24.0 (Apple Git-66)

If you do not have installed it already, then it will ask you to install it.

https://sourceforge.net/projects/git-osx-installer/files/latest/download


After git is installed:
from terminal 
> git clone https://github.com/gregoryarose/NHCC.git

If not already installed, install python:

https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe

from terminal:

> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
> python3 get-pip.py
> cd NHCC
> pip3 install -r requirements.txt


********************************************************************************


Run the programme:

For Windows, there is a shortcut in the NHCC folder "NHCC Rider Grading"

Double click this  - it may not correctly point to your installation.  If it doesn't you can run manually from the command prompt 
C:\Users\grego> cd NHCC

C:\Users\grego\NHCC> python3 NHCCRiderHistory.py. (substitute "grego" with your home directory name)


For Mac, double click NHCC.sh - again if the link fails use "Terminal" as follows:

gregoryrose@Gregorys-Air % cd nhcc

gregoryrose@Gregorys-Air nhcc % python3 NHCCRiderHistory.py

