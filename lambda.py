"""
This module contains the handler method for a lambda function that will
generate hashes for an image uploaded to S3.
"""

from __future__ import print_function

import json
import urllib

import boto3
from imgdetective import hash_generator

TEMP_FILE_PATH = '/tmp/img.png'
S3_CLIENT = boto3.client('s3')


def lambda_handler(event, context):
    """
    Handler for an AWS lambda function which is triggered by an object being
    created in an S3 bucket, hashes will be generated for that image and
    printed.
    
    Args:
        event: dict containing information on the create object event
        context: LambdaContext object with information (unused)
    Returns:
        Null
    """
    print("Received event: " + json.dumps(event, indent=2))

    # get the s3 object from the event object
    bucket = event['Records'][0]['s3']['bucket']['name']
    # get s3 object key
    key = urllib.unquote_plus(event[
            'Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        # download file into /tmp so we can work with it
        S3_CLIENT.download_file(Bucket=bucket, Key=key,
                                Filename=TEMP_FILE_PATH)

        # generate hashes for image and log them
        hashes = hash_generator.generate_hashes_for_image(TEMP_FILE_PATH)
        print(hashes)

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist \
               and your bucket is in the same region as this \
               function.'.format(key, bucket))
        raise e
