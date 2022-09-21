import sys
from urllib import response
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import logging
import json
import jwt
import os
import uuid


def lambda_handler(event, context):
    encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
    print("========================================")
    print(encoded_jwt)
    print("========================================")
    dynamo_table_name = os.environ.get('CATEGORIES_TABLE')

    dynamo_table = get_dynamo_table(dynamo_table_name)

    body = json.loads(event['body'])
    name = body['Name']
    description = body['Description']
    parent_id = body['ParentId'] if body['ParentId'] else ''
    active = body['Active'] if body['Active'] else True

    response = dynamo_table.put_item(Item={
        'Id': uuid.uuid4().hex,
        'Name': name,
        'Description': description,
        'ParentId': parent_id,
        'Active': active
    })

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': "Content-Type",
        'Access-Control-Allow-Methods': "OPTIONS,POST"
    }

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