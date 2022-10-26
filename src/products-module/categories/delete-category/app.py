import sys
from unicodedata import category
from urllib import response
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import logging
import json
import jwt
import os
import uuid

# client = boto3.client('ssm')

def lambda_handler(event, context):
    dynamo_table_name = os.environ.get('MAIN_TABLE_BABYGIFT')
    
    dynamo_table = get_dynamo_table(dynamo_table_name)
    
    pathParameters = event['pathParameters']
    category_id = "category#" + pathParameters['id']
    response = dynamo_table.delete_item(
        Key={
            "PK": category_id,
            "SK": "CATEGORY"
        }
    )

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': "Content-Type",
        'Access-Control-Allow-Methods': "OPTIONS,POST,GET,PUT"
    }
    # response = dynamo_table

    return {
        "headers": headers,
        "statusCode": 200,
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