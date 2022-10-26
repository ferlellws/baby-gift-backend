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
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    product_table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

    response = product_table.scan()

    headers = {
        "Content-Type": "application/json"
    }

    return {
        "headers": headers,
        "statusCode": 200,
        'body': json.dumps(
            response
        )
    }