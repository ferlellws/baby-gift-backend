from datetime import datetime
from botocore.exceptions import ClientError
from connectdb import Connection

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

class Model:
    obj = {}
    def __init__(self, dynamo_table_name, stage):
        self.stage = stage
        self.dynamo_table_name = dynamo_table_name
        self.connection = Connection(dynamo_table_name, stage)
        self.main_table = self.connection.create_dynamodb_resource()


    def get_keys(self):
        return {
            "PK": self.pk,
            "SK": self.sk
        }


    def new(self, obj):
        self.obj = obj


    def save(self):
        return self.execute_put_item()


    def show_item(self):
        print(self.obj)


    def item(self):
        return self.obj


    def show_varibles(self):
        print("=====================================")
        print(f"""self.stage: {self.stage}""")
        print(f"""self.dynamo_table_name: {self.dynamo_table_name}""")
        print(f"""self.connection: {self.connection}""")
        print(f"""self.main_table: {self.main_table}""")
        print(f"""self.obj.brand: {self.obj['Brand']}""")
        print("=====================================")


    def execute_put_item(self):
        try:
            print(self.obj)
            response = self.main_table.put_item(Item=self.obj)
            return {
                "response": response,
                "item": self.obj,
                "msg": f"""Registro {self.obj['Name']} creado satisfactoriamente"""
            }
        except ClientError as error:
            return {
                "error": self.handle_error(error)
            }
        except BaseException as error:
            return {
                "error": "Error desconocido al crear el item: " + error.response['Error']['Message']
            }


    def handle_error(self, error):
        error_code = error.response['Error']['Code']
        error_message = error.response['Error']['Message']

        error_help_string = ERROR_HELP_STRINGS[error_code]

        return '[{error_code}] {help_string}. Error message: {error_message}'.format(
            error_code=error_code,
            help_string=error_help_string,
            error_message=error_message
        )

