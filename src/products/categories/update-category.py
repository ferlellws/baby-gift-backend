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

# client = boto3.client('ssm')

def lambda_handler(event, context):
    dynamo_table_name = os.environ.get('CATEGORIES_TABLE')
    
    dynamo_table = get_dynamo_table(dynamo_table_name)

    response = dynamo_table.update_item(
        Key={"Id": "a7aaba4cd4684a1eb764d524cd55bd11"},
        # Expression attribute names specify placeholders for attribute names to use in your update expressions.
        ExpressionAttributeNames={
            "#category": "Category",
            "#description": "Description",
        },
        # Expression attribute values specify placeholders for attribute values to use in your update expressions.
        ExpressionAttributeValues={
            ":category": "Bebes",
            ":description": "Productos para bebé",
        },
        # UpdateExpression declares the updates you want to perform on your item.
        # For more details about update expressions, see https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
        UpdateExpression="SET #category = :category, #description = :description",
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