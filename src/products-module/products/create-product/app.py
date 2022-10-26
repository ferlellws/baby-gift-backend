from itertools import product
from urllib import response
# from boto3.dynamodb.conditions import Key
# from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import logging
import json
import os
import uuid
from functions import create_dynamodb_resource, response_function, execute_put_item, ERROR_HELP_STRINGS
from product_model import Product


def lambda_handler(event, context):
    dynamo_table_name = os.environ.get('MAIN_TABLE_BABYGIFT')
    main_table = create_dynamodb_resource(dynamo_table_name)

    parameters = extract_data_parameter(event)
    model = Product(parameters)
    product = create_put_item_input(model)

    if validate_parameters(product)['valid']:
        if exist_product(product)['exist']:
            response_save_item = {
                'error': 'El producto {} ya existe' . format(product['Name'])
            }
        else:
            response_save_item = execute_put_item(main_table, product)
    else:
        response_save_item = {
            'error': 'Algunos campos no pasaron la validación, por favor verifique'
        }

    return response_function(response_save_item)


def extract_data_parameter(parameters):
    data = parameters["body"]
    return json.loads(data)


def create_put_item_input(model):
    return model.to_item()


def exist_product(product):
    # TODO: Hacer validación si existe el product
    response_validations = False
    return {
        'exist': response_validations
    }

def validate_parameters(product):
    # TODO: Hacer validación de los parametros entrantes
    response_validations = True
    return {
        'valid': response_validations
    }