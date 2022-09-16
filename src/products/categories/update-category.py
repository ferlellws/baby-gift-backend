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

from re import sub

# client = boto3.client('ssm')

def lambda_handler(event, context):
    obj_attributes = json.loads(event['body'])
    categoryId = event['pathParameters']['id']

    response = update_item(categoryId, obj_attributes)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': "Content-Type",
        'Access-Control-Allow-Methods': "OPTIONS,POST,GET,PUT"
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


def update_item(categoryId, obj_attributes):
    dynamo_table_name = os.environ.get('CATEGORIES_TABLE')
    dynamo_table = get_dynamo_table(dynamo_table_name)

    parameters_to_update = get_parameters_to_update(obj_attributes)

    response = dynamo_table.update_item(
        Key={"Id": categoryId},
        ExpressionAttributeNames=parameters_to_update['expression_attribute_names'],
        ExpressionAttributeValues=parameters_to_update['expression_attribute_values'],
        UpdateExpression=parameters_to_update['update_expression'],
    )

    return response

def get_parameters_to_update(obj_attributes):
    attributes_to_update = list(obj_attributes.keys())

    expression_attribute_names = {}
    expression_attribute_values = {}
    array_update_expression = []

    for key in attributes_to_update:
        key_tmp = camel_case(key)
        expression_attribute_names['#%s' % key_tmp] = key
        expression_attribute_values[':%s' % key_tmp] = obj_attributes[key]
        array_update_expression.append('#%s = :%s' % (key_tmp, key_tmp))

    response = {
        'expression_attribute_names': expression_attribute_names,
        'expression_attribute_values': expression_attribute_values,
        'update_expression': 'SET %s' %  ', '.join(array_update_expression)
    }

    return response


def camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])