import json
import boto3
from botocore.config import Config


class ChessVisionWrapper:
    def __init__(self, identity_pool_id, region_name):
        print('init ChessVisionWrapper started.')
        
        self.config = Config(region_name=region_name)
        self.identity_pool_id = identity_pool_id

        self.init_identity_client()
        self.init_lambda_client()
        
        print('init ChessVisionWrapper completed.')

    def init_identity_client(self):
        print('>> init_identity_client')
        
        self.identity_client = boto3.client('cognito-identity', config=self.config)

    def init_lambda_client(self):
        print('>> init_lambda_client')
        
        credentials = self.get_credentials()
        self.lambda_client = boto3.client(
            'lambda',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretKey'],
            aws_session_token=credentials['SessionToken'],
            config=self.config
        )

    def get_credentials(self):
        identity_id = self.identity_client.get_id(
            IdentityPoolId=self.identity_pool_id
        )['IdentityId']

        response = self.identity_client.get_credentials_for_identity(
            IdentityId=identity_id
        )

        credentials = response['Credentials']
        return credentials

    def invoke_lambda_fn(self, function_name, json_string):
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json_string
        )

        data = json.loads(response['Payload'].read())
        return json.loads(data['body'])


