# -*- coding: utf-8 -*-

import boto3

def handler(event, context):

    try:

        dynamodb = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url="http://localhost:8000")
        #dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
        """
        table = dynamodb.create_table(
        TableName='Menu',
        KeySchema=[
            {
                'AttributeName': 'menu_id',
                'KeyType': 'HASH'
            }        
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'menu_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
        )
        """

        table = dynamodb.Table('Menu')

        table.put_item(Item=event)

        return "200 OK"
        

    except:

        return "500 Error"


    e = event.get('menu_id')
    pi = event.get('store_name')
    return e
