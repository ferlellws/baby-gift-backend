import boto3
# print("=========== Entra a Connectdb ============")

class Connection:
    def __init__(self, table, stage):
        self.table = table
        self.stage = stage


    def create_dynamodb_resource(self):
        aws_environment = self.stage

        if aws_environment == 'LOCAL':
            dynamodb = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/")
        else:
            dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

        return dynamodb.Table(self.table)