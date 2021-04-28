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
import ChessVision_config as conf


def inititalize_credentials():
    identity_client = boto3.client('cognito-identity', config=conf.my_config)

    identity_id = identity_client.get_id(
        IdentityPoolId='eu-central-1:d06d1df9-443e-49e3-84e8-d90aacb9b333'
    )['IdentityId']

    response = identity_client.get_credentials_for_identity(
        IdentityId=identity_id
    )
    
    credentials = response['Credentials']
    return credentials


def initialize_lambda_client():
    global lambda_client
    credentials = inititalize_credentials()
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretKey'],
        aws_session_token=credentials['SessionToken'], 
        config=conf.my_config
    )


def invoke_lambda(json_payload):
    response = lambda_client.invoke(
        FunctionName=conf.function_name,
        InvocationType='RequestResponse',
        Payload=json_payload
    )

    data = json.loads(response['Payload'].read())

    if data['statusCode'] == 200:
        return json.loads(data['body'])
    else:
        print(data['statusCode'])
        return data


def get_json_from_img(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    base64str = base64.b64encode(buffered.getvalue()).decode('ascii')
    return json.dumps({
        'image': base64str,
        'flip': False
    })


def get_fen_from_dir(credentials, chessboards_dir):
    # chessboards_dir = '/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/cb_sample_300/'
    chessboard_images = utils.get_filenames_from_dir(chessboards_dir)

    chessboard_images.sort(key=utils.alphanum_key)

    for img_path in chessboard_images:
        json_data = get_json_from_img(path.join(chessboards_dir, img_path))
        response_data = invoke_lambda(credentials, json_data)
        print(response_data['FEN'])


def sample():
    data = get_json_from_img('./img/Image-2.jpg')
    initialize_lambda_client()
    response_data = invoke_lambda(data)
    print(response_data['FEN'])


if __name__ == '__main__':
    start = time.time()
    # credentials = inititalize_credentials()
    # get_fen_from_dir(credentials, '/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/chessboard/')
    sample()
    end = time.time()
    print('execution time: %ds', end-start)
