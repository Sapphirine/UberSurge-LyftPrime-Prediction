from __future__ import print_function  # Python 2/3 compatibility

import ConfigParser

import boto3

# access config information
config = ConfigParser.RawConfigParser()
config.read('config.cfg')

# get access to dynomodb
dynamodb = boto3.resource('dynamodb', region_name=config.get('dynamo', 'region_name'),
                          endpoint_url=config.get('dynamo', 'endpoint_url'))


# for the use to delete the database
def delete_database(table):
    try:
        table.delete()
    except Exception:
        raise Exception


# create a dynamodb table
def create_database(table_name):
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'time',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("Table %s is creating" % table_name)
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    print("Table status: %s" % table.table_status)
    return table


# access the database table
def get_table(table_name):
    return dynamodb.Table(table_name)


# wrapper function to insert item into table, data format specified
def insert(table, item):
    response = table.put_item(Item=item)
