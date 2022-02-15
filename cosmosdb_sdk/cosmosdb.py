'''
Author:         Jixin Jia (Gin)
Date:           20-Jan-2020
Version:        1.0

This utility is designed to streamline interactign with Azure Cosmos DB using Python. 
It contains following features:

(1) Classes for supporting common CRUD operations
(2) Sample driver program showcasing how to use this SDK
'''

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
from .cosmos_credential import cosmosdb_config
from logging import getLogger
logger = getLogger(__name__)


class CosmosDB():
    def __init__(self, database_id, container_id):

        # Initialize the Cosmos client
        self.client = cosmos_client.CosmosClient(
            url_connection=cosmosdb_config['ENDPOINT'],
            auth={'masterKey': cosmosdb_config['PRIMARYKEY']}
        )

        '''
        This utility will create the specified database and container 
        if they don't exist already
        '''

        # Define database link
        self.database_link = 'dbs/' + database_id
        try:
            db = self.client.ReadDatabase(self.database_link)
            logger.info('Initiated DB ->', db)

        except errors.HTTPFailure as e:
            if e.status_code == 404:
                print('The database \'{0}\' DOES NOT exist.'.format(
                    database_id))

                self.create_database(database_id)
                db = self.client.ReadDatabase(self.database_link)
                print(
                    '[Info] Successfully created {0} -> {1}'.format(database_id, db))

            else:
                raise errors.HTTPFailure(e.status_code)

        except Exception as e:
            raise e

        # Define container link
        self.container_link = self.database_link + \
            '/colls/' + container_id

        try:
            container = self.client.ReadContainer(
                self.container_link, options=None)
            logger.info('Initiated Container ->', container)

        except errors.HTTPFailure as e:
            if e.status_code == 404:
                print('The container \'{0}\' DOES NOT exist.'.format(
                    container_id))

                self.create_container(container_id)
                container = self.client.ReadContainer(
                    self.container_link, options=None)
                print(
                    '[Info] Successfully created {0} -> {1}'.format(container_id, container))

            else:
                raise errors.HTTPFailure(e.status_code)

        except Exception as e:
            raise e

    def default_options(self):
        options = {
            'enableCrossPartitionQuery': True,
            'maxItemCount': -1,  # optimized for auto document pagination
        }
        return options

    # Create a database
    def create_database(self, database):
        try:
            return self.client.CreateDatabase({'id': database})

        except errors.HTTPFailure as e:
            if e.status_code == 409:
                print('[Info] A database with id \'{0}\' ALREADY exists'.format(
                    self.database_link))
            else:
                raise errors.HTTPFailure(e.status_code)

        except Exception as e:
            raise e

    # Create a container
    def create_container(self, container):
        try:
            container_definition = {
                'id': container,
                'indexingPolicy': {
                    'indexingMode': 'consistent',  # consistent or lazy
                    'automatic': True,
                    'includedPaths': [{
                        'path': '/*',
                        'indexes': [{
                            'kind': 'Range',
                            'dataType': 'Number',
                            'precision': -1
                        }, {
                            'kind': 'Range',
                            'dataType': 'String',
                            'precision': -1
                        }, {
                            'kind': 'Spatial',
                            'dataType': 'Point'
                        }
                        ]}],
                    'excludedPaths': [{
                        'path': '/\'_etag\'/?'
                    }]
                },
                'partitionKey': {
                    'paths': [
                        '/partitionKey'
                    ],
                    'kind': 'Hash',
                }
            }

            options = {
                'offerThroughput': 400  # range from 400 to 1 million
            }

            return self.client.CreateContainer(self.database_link, container_definition, options)

        except errors.CosmosError as e:
            if e.status_code == 409:
                logger.error('A collection with id \'{0}\' ALREADY exists'.format(
                    self.container_link))
            else:
                raise errors.HTTPFailure(e.status_code)
        except Exception as e:
            raise e

    # Create and add an item to the container
    def create_item(self, item):
        # query = {
        #     'query': 'SELECT * FROM c WHERE c.id = "{0}"'.format(item['id'])
        # }

        try:
            output = self.client.CreateItem(self.container_link, item)
            # results = list(self.client.QueryItems(
            #     self.container_link, query, self.default_options()))
            print('[Info] Successfully created item {}'.format(item['id']))
            return output

        except errors.HTTPFailure as e:
            if e.status_code == 404:
                print('[Create] A collection with id \'{0}\' DOES NOT exist'.format(
                    self.container_link))
            elif e.status_code == 409:
                logger.error(
                    '[Create]  A Item with id \'{0}\' already exists'.format(item['id']))
            else:
                raise errors.HTTPFailure(e.status_code)
        except Exception as e:
            raise e

    # Upsert a item from the container
    def upsert_item(self, item):
        try:
            result = self.client.UpsertItem(
                self.container_link, item, self.default_options())
            print('[Info] Successfully updated item {}'.format(item['id']))
            return result
        except errors.HTTPFailure as e:
            if e.status_code == 404:
                print('[Upsert] A collection with id \'{0}\' DOES NOT exist'.format(
                    self.container_link))
            else:
                raise errors.HTTPFailure(e.status_code)
        except Exception as e:
            raise e

    # Read all documents in a container (collection)
    def list_items(self):
        try:
            itemList = list(self.client.ReadItems(
                self.container_link, {'maxItemCount': 50}))

            logger.info('[Info] Found {0} documents'.format(
                itemList.__len__()))

            for item in itemList:
                logger.info(item)
            return itemList
        except errors.HTTPFailure as e:
            if e.status_code == 404:
                print('[Read] A collection with id \'{0}\' DOES NOT exist'.format(
                    self.container_link))
            else:
                raise errors.HTTPFailure(e.status_code)
        except Exception as e:
            raise e

    # Execute custom query to fetch data
    def query_item(self, query_syntax):
        query = {'query': query_syntax}
        try:
            results = list(self.client.QueryItems(
                self.container_link, query, self.default_options()))
            return results
        except errors.HTTPFailure as e:
            if e.status_code == 404:
                print('[Query] A collection with id \'{0}\' DOES NOT exist'.format(
                    self.container_link))
            else:
                raise errors.HTTPFailure(e.status_code)
        except Exception as e:
            raise e

    def delete_item(self, document_id):
        query = {
            'query': 'SELECT * FROM c WHERE c.id = "{0}"'.format(document_id)
        }
        try:
            results = self.client.QueryItems(
                self.container_link, query, self.default_options())

            for result in list(results):
                options = self.default_options()
                options['partitionKey'] = result['partitionKey']
                doc_link = self.container_link + '/docs/' + result['id']
                output = self.client.DeleteItem(doc_link, options)
                print('[Info] Successfully deleted item {}'.format(result['id']))
            return output

        except errors.HTTPFailure as e:
            if e.status_code == 404:
                print('[Delete] A collection with id \'{0}\' DOES NOT exist'.format(
                    self.container_link))
            else:
                raise errors.HTTPFailure(e.status_code)
        except Exception as e:
            raise e
