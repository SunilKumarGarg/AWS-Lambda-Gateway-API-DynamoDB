# -*- coding: utf-8 -*-

import boto3

def handler(event, context):

    try:

        #dynamodb = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
        

        table = dynamodb.Table('Menu')

        table.delete_item(Key={
            'menu_id':event.get('menu_id')
        })

        
        return "200 OK"

    except:

        return "500 Error"
