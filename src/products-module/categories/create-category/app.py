from urllib import response
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import logging
import json
import os
import uuid

from functions import get_dynamo_table, response_function


def lambda_handler(event, context):
    category = get_category_to_parameters(event)

    if validate_parameters(category)['success']:
        response_save_item = save_item(category)
    else:
        response_save_item = {
            'msg': 'El categoría {} ya existe' . format(category['Name'])
        }

    msg_error = "No se creó la categoría {}" . format(category['Name'])
    item_response = {
        'item': category,
        'msg': "Categoría {} creada satisfactoriamente" . format(category['Name'])
    }
    
    return response_function(response_save_item, item_response, msg_error)


def get_category_to_parameters(parameters):
    data = parameters["body"]
    body = json.loads(data)
    return get_category_json(body)


def get_category_json(body):
    category_id = str(uuid.uuid4().hex)[:8]
    name = body['Name']
    description = body['Description']
    parents_id = body['ParentsId'] if body['ParentsId'] else category_id
    active = body['Active'] if body['Active'] else True

    return {
        'PK': "category#" + category_id,
        'SK': "CATEGORY",
        'Data': parents_id,
        'Name': name,
        'Description': description,
        'Active': active
    }


def validate_parameters(category):
    # TODO: Hacer validación de los parametros entrantes
    response_validations = True
    return {
        'success': response_validations
    }


def save_item(item):
    dynamo_table_name = os.environ.get('MAIN_TABLE_BABYGIFT')

    items_table = get_dynamo_table(dynamo_table_name)

    data = items_table.put_item(Item=item)
    return data