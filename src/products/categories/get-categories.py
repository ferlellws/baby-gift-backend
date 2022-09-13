import sys
from urllib import response
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import logging
import json
import jwt
import os

# client = boto3.client('ssm')

def lambda_handler(event, context):
    dynamo_table_name = os.environ.get('CATEGORIES_TABLE')
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    dynamo_table = dynamodb.Table(dynamo_table_name)
    response = dynamo_table.scan()
    
    # token = event['headers']['Authorization']

    # payload = decode_jwt(token)
    # stage = payload['custom:environment']
    # tenant = payload['custom:tenant']

    # conn = get_connection_to_db(stage, tenant)

    # response = {}
    # response['headers'] = ['', 'Nombre', 'Atributo', 'Estado', '']
    # response['dataTable'] = []

    # try:
    #     with conn.cursor() as cur:
    #         sql_get_actions = """
    #             SELECT
    #                 icon,
    #                 name,
    #                 attribute,
    #                 is_active,
    #                 id
    #             FROM
    #                 actions
    #             WHERE is_delete = false"""
    #         cur.execute(sql_get_actions)
    #         for row in cur:
    #             response['dataTable'].append({
    #                 'icon': row[0],
    #                 'name': row[1],
    #                 'attribute': row[2],
    #                 'is_active': row[3],
    #                 'id_for_options': row[4],
    #             })


    # except (Exception, psycopg2.Error) as error:
    #     print("Error in insert operation", error)

    headers = {}
    headers['HTTPHeaders'] = {}
    headers['HTTPHeaders']['Access-Control-Allow-Origin'] = '*'
    headers['HTTPHeaders']['Access-Control-Allow-Headers'] = "Content-Type"
    headers['HTTPHeaders']['Access-Control-Allow-Methods'] = "OPTIONS,POST,GET"
    
    # response = dynamo_table

    return {
        "headers": headers['HTTPHeaders'],
        "statusCode": 200,
        'body': json.dumps(
            response,
            indent=4,
            sort_keys=False,
            default=str
        )

    }

# def get_parameter_of_db(param, stage=""):
#     base_parameters = "/service/transport-app-pipeline/connection-bd"

#     if param == 'rds-host':
#         name = "%s/%s-%s" % (base_parameters, param, stage.lower())
#     else:
#         name = "%s/%s" % (base_parameters, param)

#     return client.get_parameter(
#         Name=name
#     )['Parameter']['Value']

# def get_connection_to_db(stage, tenant):
#     RDS_HOST = get_parameter_of_db('rds-host', stage)
#     RDS_DB_NAME = "%s%s%s" % (stage, get_parameter_of_db('db-name'), tenant)
#     RDS_USERNAME = get_parameter_of_db('username')
#     RDS_USER_PWD = get_parameter_of_db('password')

#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)

#     try:
#         conn_string = "host=%s user=%s password=%s dbname=%s" % \
#                         (RDS_HOST, RDS_USERNAME, RDS_USER_PWD, RDS_DB_NAME)
#         conn = psycopg2.connect(conn_string)
#     except:
#         logger.error("ERROR: Could not connect to Postgres instance.")
#         sys.exit()

#     logger.info("SUCCESS: Connection to RDS Postgres instance succeeded")
#     return conn

# def decode_jwt(token):
#     return jwt.decode(token, options={"verify_signature": False, "require":["iss"]})
