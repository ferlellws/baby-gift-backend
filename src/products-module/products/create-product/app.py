from itertools import product
from urllib import response
from botocore.exceptions import ClientError
import logging
import json
import os
from functions import response_function
from product import Product


def lambda_handler(event, context):
    dynamo_table_name = os.environ.get('MAIN_TABLE_BABYGIFT')
    stage = os.environ.get('AWS_ENV')
    ProductModel = Product(dynamo_table_name, stage)

    parameters = extract_data_parameter(event)
    product = ProductModel.new(parameters)

    if validate_parameters(product.item())['valid']:
        if exist_product(product.item())['exist']:
            response_save_item = {
                'error': 'El producto {} ya existe' . format(product['Name'])
            }
        else:
            response_save_item = product.save()
    else:
        response_save_item = {
            'error': 'Algunos campos no pasaron la validación, por favor verifique'
        }

    return response_function(response_save_item)


def extract_data_parameter(parameters):
    data = parameters["body"]
    return json.loads(data)


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