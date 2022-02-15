# NHCC

# Developer: Gregory Rose (gregory.rose@optusnet.com.au)

NHCC Rider and Grading database

Steps to use:


Windows:

from command promt
> git clone https://github.com/gregoryarose/NHCC.git


If not already installed, install python:
> pip3 install python3
> pip3 install Jinja2
> cd NHCC
> pip3 install -r requirements.txt 

set up cosmos-sdk:

from windows file explorer navigate to NHCC folder 

Add your Cosmos DB Endpoint and Primary Key to the cosmosdb_credential.py file (contact Greg Rose for the keys)

ON MAC:

If not already installed, install python:

	[from terminal] >	pip3 install python3

git clone https://github.com/jixjia/cosmos-sdk.git

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python3 get-pip.py

pip install -r requirements.txt

pip3 install Jinja2

Add your Cosmos DB Endpoint and Primary Key to the cosmosdb_credential.py file (get these from Greg Rose)
