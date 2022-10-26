import os
import boto3
import json


ERROR_HELP_STRINGS = {
    # Operation specific errors
    'ConditionalCheckFailedException': 'Condition check specified in the operation failed, review and update the condition check before retrying',
    'TransactionConflictException': 'Operation was rejected because there is an ongoing transaction for the item, generally safe to retry with exponential back-off',
    'ItemCollectionSizeLimitExceededException': 'An item collection is too large, you\'re using Local Secondary Index and exceeded size limit of items per partition key.' +
                                                ' Consider using Global Secondary Index instead',
    # Common Errors
    'InternalServerError': 'Internal Server Error, generally safe to retry with exponential back-off',
    'ProvisionedThroughputExceededException': 'Request rate is too high. If you\'re using a custom retry strategy make sure to retry with exponential back-off.' +
        'Otherwise consider reducing frequency of requests or increasing provisioned capacity for your table or secondary index',
    'ResourceNotFoundException': 'One of the tables was not found, verify table exists before retrying',
    'ServiceUnavailable': 'Had trouble reaching DynamoDB. generally safe to retry with exponential back-off',
    'ThrottlingException': 'Request denied due to throttling, generally safe to retry with exponential back-off',
    'UnrecognizedClientException': 'The request signature is incorrect most likely due to an invalid AWS access key ID or secret key, fix before retrying',
    'ValidationException': 'The input fails to satisfy the constraints specified by DynamoDB, fix input before retrying',
    'RequestLimitExceeded': 'Throughput exceeds the current throughput limit for your account, increase account level throughput before retrying',
}


def create_dynamodb_resource(dynamo_table_name):
    aws_environment = os.environ.get('AWS_ENV')

    if aws_environment == 'LOCAL':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/")
    else:
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    return dynamodb.Table(dynamo_table_name)


def execute_put_item(dynamodb_client, item):
    try:
        response = dynamodb_client.put_item(Item=item)
        return {
            "response": response,
            "item": item,
            "msg": f"""Registro {item['Name']} creado satisfactoriamente"""
        }
    except ClientError as error:
        return {
            "error": handle_error(error)
        }
    except BaseException as error:
        return {
            "error": "Error desconocido al crear el item: " + error.response['Error']['Message']
        }


def handle_error(error):
    error_code = error.response['Error']['Code']
    error_message = error.response['Error']['Message']

    error_help_string = ERROR_HELP_STRINGS[error_code]

    return '[{error_code}] {help_string}. Error message: {error_message}'.format(
        error_code=error_code,
        help_string=error_help_string,
        error_message=error_message
    )


def response_function(response_action_item):
    if "response" in response_action_item and response_action_item['response'] and response_action_item['response']['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "item": response_action_item["item"],
            "msg": response_action_item["msg"]
        }
    else:
        response = {
            "error": response_action_item["error"]
        }

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': "Content-Type",
        'Access-Control-Allow-Methods': "OPTIONS,POST"
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