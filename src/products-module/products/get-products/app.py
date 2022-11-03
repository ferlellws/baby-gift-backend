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
from product import Product
from functions import response_function


def lambda_handler(event, context):
    dynamo_table_name = os.environ.get('MAIN_TABLE_BABYGIFT')
    stage = os.environ.get('AWS_ENV')
    products = Product(dynamo_table_name, stage)

    response = products.all()

    products_json = process_data_products(response)
    response['response']['Items'] = products_json

    return response_function(response, True)


def process_data_products(data):
    list_products = data['response']['Items']
    products = []
    for product in list_products:
        discount_price = get_discount_price(product['Price'], product['Discount'])
        product_json = {
            'id': product['PK'].split('#')[1],
            'name': product['Name'],
            'brand': product['Brand'],
            'description': product['Description'],
            'finalPrice': float(product['Price']),
            'discountPrice': discount_price,
            'image': '',
            'rating': 3
        }

        products.append(product_json)

    return products


def get_discount_price(price, discount_obj):
    print(discount_obj['Percentage'])
    if 'Percentage' in discount_obj:
        discount = float(price) * float(discount_obj['Percentage']) / 100
        return float(price) - discount
    elif 'Price' in discount_obj:
        return price - discount_obj['Price']