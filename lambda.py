from __future__ import print_function

import os
import urllib

import boto3
from imgdetective import hash_generator

TEMP_FILE_PATH = '/tmp/img.png'
S3_CLIENT = boto3.client('s3')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event[
            'Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        # response = s3.get_object(Bucket=bucket, Key=key)
        # print("CONTENT TYPE: " + response['ContentType'])
        S3_CLIENT.download_file(Bucket=bucket, Key=key,
                                Filename=TEMP_FILE_PATH)
        hash_generator.generate_hashes_for_image(TEMP_FILE_PATH)
        print(os.listdir("/tmp"))
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist \
               and your bucket is in the same region as this \
               function.'.format(key, bucket))
        raise e
