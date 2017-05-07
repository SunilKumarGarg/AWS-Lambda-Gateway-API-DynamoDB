# -*- coding: utf-8 -*-

import boto3

def handler(event, context):

    try:

        #dynamodb = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
        

        table = dynamodb.Table('Menu')

        response = table.get_item(Key={
            'menu_id':event.get('menu_id')
        })

        item = response['Item']
        return item

    except:

        return "500 Error"
