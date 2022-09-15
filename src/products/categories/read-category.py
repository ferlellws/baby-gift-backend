import sys
from urllib import response
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import logging
import json
import jwt
import os


def lambda_handler(event, context):
    categoryId = event['pathParameters']['id']
    dynamo_table_name = os.environ.get('CATEGORIES_TABLE')
    
    dynamo_table = get_dynamo_table(dynamo_table_name)

    # print(dynamo_table)
    # response = dynamo_table.query(
    #     KeyConditionExpression="Id > 0"
    # )

    try:
        statusCode = 200
        response = dynamo_table.get_item(Key={"Id": categoryId})
        response = response['Item']
    except:
        statusCode = 400
        response = {
            "errorMsg": "No se encuentra la categoría"
        }
        
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': "Content-Type",
        'Access-Control-Allow-Methods': "OPTIONS,POST,GET"
    }
    # response = dynamo_table

    return {
        "headers": headers,
        "statusCode": statusCode,
        'body': json.dumps(
            response,
            indent=4,
            sort_keys=False,
            default=str
        )
    }


def get_dynamo_table(dynamo_table_name):
    aws_environment = os.environ.get('AWS_ENV')

    if aws_environment == 'LOCAL':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/")
    else:
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    return dynamodb.Table(dynamo_table_name)