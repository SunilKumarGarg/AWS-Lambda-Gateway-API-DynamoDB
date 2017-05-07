# -*- coding: utf-8 -*-

import boto3
import json
from datetime import datetime

def handler(event, context):
    """
    This is a handler to process order refinement for pizza. User sends json with attribute "order_id" and "input". 
    Depending on what is the stage of the order, input field define different thing. When orser is in selection stage, input field means selection of different kind of pizza.
    When order is in size stage, input field means size of the pizza
    """

    try:

        #Open Database
        #dynamodb = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

        #Get order details for current order id.
        tableOrder = dynamodb.Table('Order')
        responseOrder = tableOrder.get_item(Key={
            'order_id':event.get('order_id')
            })

        #Get the menu if for this particular order. Menu is fetched from Menu table using menu id stored for each order in order table.
        menu_id = responseOrder['Item'].get('menu_id')
        tableMenu = dynamodb.Table('Menu')

        responseMenu = tableMenu.get_item(Key={
            'menu_id':menu_id
        })        
        
        #Get Menu item details
        sequence = responseMenu['Item'].get('sequence')
        selection = responseMenu['Item'].get('selection')
        size = responseMenu['Item'].get('size')
        price = responseMenu['Item'].get('price')

        #In case there is no information in Database, initialize in
        if sequence == None:
            sequence = ["selection","size"]
        if selection == None:
            selection = ["Cheese","Pepperoni"]
        if size == None:
            size = ["Slide", "Small", "Medium", "Large", "X-Large"]
        if price == None:
            price = ["3.50", "7.00", "10.00", "15.00", "20.00"]

        #Get the order stage from order table. Order can be in different stage, but in one stage at one time.

        orderStatus = responseOrder['Item'].get('order_status')

        #If order is in selection stage, it means the "input" field in user data is to select selection if different type of pizza.
        if orderStatus == 'selection':
            tableOrder.update_item(
                Key={
                    'order_id': event.get('order_id')
                },
                UpdateExpression='SET selection = :val1',
                ExpressionAttributeValues={
                    ':val1': selection[int(event.get('input'))-1]
                }
            )

        #If order is in size stage, it means the "input" field in user data is to select pizza size.
        elif orderStatus == 'size':
            tableOrder.update_item(
                Key={
                    'order_id': event.get('order_id')
                },
                UpdateExpression='SET size = :val1',
                ExpressionAttributeValues={
                    ':val1': size[int(event.get('input'))-1]
                }
            )

        #Get current status from Order Table
        responseOrder = tableOrder.get_item(Key={
            'order_id':responseOrder['Item'].get('order_id')
        })

        #find next order stage from sequence field in menu
        nextStatus = findOrderNextStatus(sequence, orderStatus)


        #Update the next stage data in order table
        tableOrder.update_item(
            Key={
                'order_id': responseOrder['Item'].get('order_id')
            },
            UpdateExpression='SET order_status = :val1',
            ExpressionAttributeValues={
                ':val1': nextStatus
            }
        )

        #if next order stage is selection, get the selection choice from menu and give proper message to user
        if nextStatus == 'selection':
            s = ""
            for i, sel in enumerate(selection):            
                s = s + " " + str(i+1) + ". " + sel + ","

            res = {} 
            res.setdefault("Message", "Hi " + event.get('customer_name') + ", " + "please choose one of these selection: " +s )
            return json.dumps(res)

        #if next order stage is size, get the selection choice from menu and give proper message to user
        elif nextStatus == 'size':
            s = ""
            for i, si in enumerate(size):            
                s = s + " " + str(i+1) + ". " + si + ","

            res = {} 
            res.setdefault("Message", "Which size do you want?: " +s )
            return json.dumps(res)

        #if next order stage is processing, get the order details from order table for this order id and present order details to user
        elif nextStatus == 'processing':

            response = tableOrder.get_item(Key={
                'order_id':responseOrder['Item'].get('order_id')
            })

            #Get the size index in menu. same index needs to be used in price.
            i = 0
            for ss in size:
                if ss == response['Item'].get('size'):                
                    break
                i = i+1

            tableOrder.update_item(
                Key={
                    'order_id': event.get('order_id')
                },
                UpdateExpression='SET costs = :val1',
                ExpressionAttributeValues={
                    ':val1': price[i]
                }
            )

            tableOrder.update_item(
                Key={
                    'order_id': event.get('order_id')
                },
                UpdateExpression='SET order_time= :val1',
                ExpressionAttributeValues={
                    ':val1': datetime.now().strftime('%Y-%m-%d@%H:%M:%S')
                }
            )

            res = "Message: Your order costs $"+ price[i]+". We will email you when the order is ready. Thank you!"            

            return json.dumps(res)

    except:

        return "500 Error"
    


def findOrderNextStatus(sequence, statusOrder):
    if statusOrder == None:
        return sequence[0]
    for i, seq in enumerate(sequence):
        if (i+1) == len(sequence):
            return "processing"
        elif seq == statusOrder:
            return sequence[i+1] 

    

