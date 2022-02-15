<p align="center">
  <img src="https://jixjiastorage.blob.core.windows.net/blog-resources/cosmos-sdk-for-python/title.jpg">
</p>

# Python SDK for Azure Cosmos DB

I designed this utility to help simplify interacting with Azure Cosmos DB using Python. The repo contains following features:

1. Classes for supporting common CRUD operations
2. Sample driver program showing how to use this SDK

## How-To

1. Provision an Azure Cosmos DB service from [Azure Portal](http://portal.azure.com)
2. Clone this repo `git clone https://github.com/jixjia/cosmos-sdk.git`
3. Install dependencies with `pip install -r requirements.txt`
4. Add your **Cosmos DB Endpoint** and **Primary Key** to the `cosmosdb_credential.py` file:

```python
# Cosmos DB config
cosmosdb_config = {
    'ENDPOINT': '<YOUR_COSMOS_ENDPOINT>',
    'PRIMARYKEY': '<YOUR_PRIMARY_KEY>'
}
```

You can find credential information from the **Keys** section of your Cosmos DB instance on Azure Portal:
<p align="center">
  <img src="https://jixjiastorage.blob.core.windows.net/blog-resources/cosmos-sdk-for-python/1.png">
</p>


5. Run driver program `python program.py` for a demo of this utility. It will perform followings:
   - Create a new Cosmos database
   - Create a new database collection (also known as container)
   - Add sample data into it
   - Query items using SQL-like syntax (SQL API)
   - Delete selected items

:warning: *You will need the Cosmos DB provisioned in order to run this DEMO program*

## Tutorial
Refer to this [blog article](https://jixjia.com/python-sdk-for-cosmosdb/) for more examples of easy-to-use tutorials

