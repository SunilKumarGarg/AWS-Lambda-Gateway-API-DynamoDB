# -*- coding: utf-8 -*-

import boto3
import json
from datetime import datetime

def handler(event, context):
    """
    Get the order details for a particular order
    """

    try:

        #Open Database
        #dynamodb = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

        #Get order details for current order id.
        tableOrder = dynamodb.Table('Order')
        response = tableOrder.get_item(Key={
            'order_id':event.get('order_id')
            })        

        res = {
            "menu_id": response['Item'].get('menu_id'),
            "order_id": response['Item'].get('order_id'),
            "customer_name": response['Item'].get('customer_name'),
            "customer_email": response['Item'].get('customer_email'),
            "order_status": response['Item'].get('order_status'),
            "order": {
                "selection": response['Item'].get('selection'),
                "size": response['Item'].get('size'),
                "costs": response['Item'].get('costs'),
                "order_time": response['Item'].get('order_time')
            }
        }

        return json.dumps(res)

    except:

        return "500 Error"
    

