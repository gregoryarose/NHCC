# NHCC
NHCC Rider and Grading database
Steps to use:

Windows:

If not already installed, install python:

	[from command prompt] >	pip3 install python3

set up cosmos-sdk:

    git clone https://github.com/jixjia/cosmos-sdk.git - (more info if needed at https://github.com/jixjia/cosmos-sdk)


    pip3 install -r requirements.txt (if not found, make sure you are in the directory that contains the cosmos-sdk folder)
	pip3 install Jinja2

Add your Cosmos DB Endpoint and Primary Key to the cosmosdb_credential.py file (get these from Greg Rose)



ON MAC:

If not already installed, install python:

	[from terminal] >	pip3 install python3

git clone https://github.com/jixjia/cosmos-sdk.git

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python3 get-pip.py

pip install -r requirements.txt

pip3 install Jinja2

Add your Cosmos DB Endpoint and Primary Key to the cosmosdb_credential.py file (get these from Greg Rose)
