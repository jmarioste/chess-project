from os import path
from PIL import Image
from io import BytesIO

import base64
import json
import re
import time
import boto3

from botocore.config import Config

import utils
import constants as const


class ChessVisionWrapper:
    def __init__(self, identity_pool_id):
        self.config = Config(region_name=const.AWS_REGION_NAME)
        self.identity_pool_id = identity_pool_id

        self.init_identity_client()
        self.init_lambda_client()
        pass

    def init_identity_client(self):
        self.identity_client = boto3.client('cognito-identity',
                                            config=self.config)

    def init_lambda_client(self):
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

    def invoke_lambda_fn(self, json_string):
        response = self.lambda_client.invoke(
            FunctionName=const.AWS_FUNCTION_NAME,
            InvocationType='RequestResponse',
            Payload=json_string
        )

        data = json.loads(response['Payload'].read())
        return json.loads(data['body'])


def get_json_from_img(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    base64str = base64.b64encode(buffered.getvalue()).decode('ascii')
    return json.dumps({
        'image': base64str,
        'flip': False
    })

# functions below should be outside chessvision wrapper
def get_fen_from_dir(chessboards_dir):
    # chessboards_dir = '/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/cb_sample_300/'
    chessboard_images = utils.get_filenames_from_dir(chessboards_dir)
    chessboard_images.sort(key=utils.alphanum_key)
    wrapper = ChessVisionWrapper(const.AWS_IDENTITY_POOL_ID)

    for img_path in chessboard_images:
        json_data = get_json_from_img(path.join(chessboards_dir, img_path))
        response_data = wrapper.invoke_lambda_fn(credentials, json_data)
        print(response_data['FEN'])


def sample():
    data = get_json_from_img('./img/Image-2.jpg')
    wrapper = ChessVisionWrapper(const.AWS_IDENTITY_POOL_ID)
    response_data = wrapper.invoke_lambda_fn(data)
    print(response_data['FEN'])


if __name__ == '__main__':
    start = time.time()
    # credentials = inititalize_credentials()
    # get_fen_from_dir(credentials, '/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/chessboard/')
    sample()
    end = time.time()
    print('execution time: %ds', end-start)
