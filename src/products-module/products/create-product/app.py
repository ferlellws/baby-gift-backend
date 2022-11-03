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
    response_save_item = ProductModel.create(parameters)
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