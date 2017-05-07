# -*- coding: utf-8 -*-

import boto3
import json

def handler(event, context):

    try:

        #Open Database
        #dynamodb = boto3.resource('dynamodb', region_name='us-west-1', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')        

        #enter the order in database
        tableOrder = dynamodb.Table('Order')        
        tableOrder.put_item(Item=event)

        return nextStep(dynamodb, tableOrder, event)

    except:

        return "500 Error"

def nextStep(dynamodb, tableOrder, event):

    #Get data from the menu for this order.
    tableMenu = dynamodb.Table('Menu')

    responseMenu = tableMenu.get_item(Key={
        'menu_id':event.get('menu_id')
    })
    
    sequence = responseMenu['Item'].get('sequence')
    selection = responseMenu['Item'].get('selection')
    size = responseMenu['Item'].get('size')

    #In case there is no information in Database, initialize in
    if sequence == None:
        sequence = ["selection","size"]
    if selection == None:
        selection = ["Cheese","Pepperoni"]
    if size == None:
        size = ["Slide", "Small", "Medium", "Large", "X-Large"]

    #Get current status from Order Table
    responseOrder = tableOrder.get_item(Key={
        'order_id':event.get('order_id')
    })

    statusOrder = responseOrder['Item'].get('order_status')

    nextStatus = findOrderNextStatus(sequence, statusOrder)


    #Update the sequence Data in order table
    tableOrder.update_item(
        Key={
            'order_id': event.get('order_id')
        },
        UpdateExpression='SET order_status = :val1',
        ExpressionAttributeValues={
            ':val1': nextStatus
        }
    )


    if nextStatus == 'selection':
        i =1
        s = ""
        for sel in selection:            
            s = s + " " + str(i) + ". " + sel + ","
            i = i + 1

        res = {} 
        res.setdefault("Message", "Hi " + event.get('customer_name') + ", " + "please choose one of these selection: " +s )
        return json.dumps(res)

    elif nextStatus == 'size':
        i =1
        s = ""
        for si in size:            
            s = s + " " + str(i) + ". " + si + ","
            i = i + 1

        res = {} 
        res.setdefault("Message", "Which size do you want?: " +s )
        return json.dumps(res)

    elif nextStatus == 'processing':
        #Read the order and return to user
        return;


def findOrderNextStatus(sequence, statusOrder):
    if statusOrder == None:
        return sequence[0]
    for i, seq in enumerate(sequence):
        if (i+1) == len(sequence):
            return "processing"
        elif seq == statusOrder:
            return sequence[i+1] 

    

