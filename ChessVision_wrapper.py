from os import path
from PIL import Image
from io import BytesIO

import base64
import json
import datetime
import re
import time
import boto3

from botocore.config import Config

import utils
import ChessVision_config as conf

    # AWS.config.region = 'eu-central-1'; // Region
    # AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    #     IdentityPoolId: 'eu-central-1:d06d1df9-443e-49e3-84e8-d90aacb9b333',
    # });

    # lambda = new AWS.Lambda({region: "eu-central-1"});
    # lambda.config.credentials = AWS.config.credentials;
    # lambda.config.region = AWS.config.region;

    # lambda.config.credentials.get(function(){
    #     var accessKeyId = AWS.config.credentials.accessKeyId;
    #     var secretAccessKey = AWS.config.credentials.secretAccessKey;
    #     var sessionToken = AWS.config.credentials.sessionToken;
    # });

client = boto3.client('lambda',
  aws_access_key_id=conf.aws_access_key_id,
  aws_secret_access_key=conf.aws_secret_access_key,
  aws_session_token=conf.aws_session_token
, config = conf.my_config)

def invoke_lambda(json_payload):
  response = client.invoke(
      FunctionName=conf.function_name,
      InvocationType='RequestResponse',
      Payload=json_payload
  )

  payload = json.loads(response['Payload'].read())

  if payload['statusCode'] == 200:
    return json.loads(payload['body'])
  else:
    print (payload['statusCode'])
    return payload

def get_json_from_img(path):
  img = Image.open(path)
  buffered = BytesIO()
  img.save(buffered, format="JPEG")
  img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
  return json.dumps({
    'image': img_str,
    'flip': "false"
  })

def get_fen_from_dir(chessboards_dir):
  # chessboards_dir = '/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/cb_sample_300/'
  chessboard_images = utils.get_files_from_dir(chessboards_dir)
  
  chessboard_images.sort(key=utils.alphanum_key)
  
  for img_path in chessboard_images:
    json_data = get_json_from_img(path.join(chessboards_dir, img_path))
    response_data = invoke_lambda(json_data)
    print(response_data['FEN'])
  
def sample():
  data = get_json_from_img('./img/Image-2.jpg')
  response_data = json.loads(invoke_lambda(data)['body'])
  print(response_data['FEN'])

if __name__ == '__main__':
  start = time.time()
  get_fen_from_dir('/mnt/g/Documents/Chess/1001 Chess Exercises for Club Players/output/chessboard/')
  end = time.time()
  print('execution time: %ds', end-start)