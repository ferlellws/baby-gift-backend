from urllib import response
import logging
import os
from product import Product
from functions import response_function


def lambda_handler(event, context):
    dynamo_table_name = os.environ.get('MAIN_TABLE_BABYGIFT')
    stage = os.environ.get('AWS_ENV')
    products = Product(dynamo_table_name, stage)
    product_id = event["pathParameters"]["id"]
    response = products.find(product_id)

    return response_function(response, True)