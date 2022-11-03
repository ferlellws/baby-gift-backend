import sys
from urllib import response
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import logging
import json
import jwt
import os
from category import Category
from functions import response_function


def lambda_handler(event, context):
    dynamo_table_name = os.environ.get('MAIN_TABLE_BABYGIFT')
    stage = os.environ.get('AWS_ENV')
    categories = Category(dynamo_table_name, stage)

    response = categories.all()
    
    categories_json = process_data_categories(response)
    response['response']['Items'] = categories_json

    return response_function(response, True)
    # dynamo_table = get_dynamo_table(dynamo_table_name)

    # response = dynamo_table.query(
    #     IndexName="GSI_1",
    #     KeyConditionExpression=Key('SK').eq('CATEGORY')
    # )

    # headers = {
    #     'Access-Control-Allow-Origin': '*',
    #     'Access-Control-Allow-Headers': "Content-Type",
    #     'Access-Control-Allow-Methods': "OPTIONS,POST,GET"
    # }
    # # response = dynamo_table

    # return {
    #     "headers": headers,
    #     "statusCode": 200,
    #     'body': json.dumps(
    #         response['Items'],
    #         indent=4,
    #         sort_keys=False,
    #         default=str
    #     )
    # }


def process_data_categories(data):
    list_categories = data['response']['Items']
    categories = []
    # sub_categories = []
    sub_categories = {}
    key = 0
    key_last = 0
    for category in list_categories:
        category_pk_array = category['PK'].split('#')
        parents_ids_array = category['Data'].split('#')
        category_id = category_pk_array[1]
        parent_id = parents_ids_array[1]
        print(f"""category_id: {category_id}""")
        print(f"""parent_id: {parent_id}""")
        print(f"""len(category_pk_array): {len(category_pk_array)}""")
        print(f"""len(parents_ids_array): {len(parents_ids_array)}""")
        is_parent = (category_id == parent_id and len(category_pk_array) == len(parents_ids_array))
        category_json = get_category_json(category, category_id)
        if is_parent:
            categories.append(category_json)
            key_last = key
            key += 1
        else:
            print(categories[key_last])
            if not 'subCategories' in categories[key_last]:
                categories[key_last]['subCategories'] = []
            sub_categories = categories[key_last]['subCategories']
            sub_categories.append(category_json)

    return categories

def get_category_json(category, category_id):
    return {
        'id': category_id,
        'name': category['Name'],
        'image': '',
        'description': category['Description']
    }


def get_subcategories(category, sub_categories):
    parent_id = category['Data'].split('#')[1]
    sub_categories[parent_id] = []
    sub_categories[parent_id].append(category)
    print(sub_categories)


def get_dynamo_table(dynamo_table_name):
    aws_environment = os.environ.get('AWS_ENV')
    region = os.environ.get('REGION')

    if aws_environment == 'LOCAL':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/")
    else:
        dynamodb = boto3.resource('dynamodb', region_name=region)

    return dynamodb.Table(dynamo_table_name)