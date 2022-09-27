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
    response = "Endpoint para Crear Producto"

    return {
        # "headers": headers,
        "statusCode": 200,
        'body': json.dumps(
            response,
            indent=4,
            sort_keys=False,
            default=str
        )
    }