from __future__ import print_function

import os
import urllib

import imagedetective.hash_generator as hash_generator
import imagedetective.elastic_index_helper as elastic


LOCAL_IMAGES = "/tmp/images/"


def lambda_handler(event, context):
    # define event such that the s3 link is provided as s3_path 
    s3path = event['s3_path']
    if 'hash_types' in event:
        hash_types = event['hash_types']
    else:
        hash_types = ['ahash', 'phash', 'dhash']
        print("No hash types specified, using defaults")

    # split https://s3.region.amazonaws.com/bucket/folder/filename to be
    # ['https:', '', 's3.region.amazonaws.com', 'bucket', 'folder', 'filename']
    path_parts = s3path.split('/')
    # use bucket name and s3 key as an identifier
    identifier = '/'.join(path_parts[3:])

    # -1 gets last element
    file_name = path_parts[-1]
    if not os.path.exists(LOCAL_IMAGES):
        os.mkdir(LOCAL_IMAGES)

    image_path = LOCAL_IMAGES + file_name
    # if the image is public we don't need to use the s3 client
    urllib.urlretrieve(s3path, image_path)

    # S3_CLIENT.download_file(Bucket=bucket, Key=s3_key, Filename=image_path)

    hashes = hash_generator.get_image_hashes(image_path, hash_types)
    elastic.save_index(hashes, identifier)


def main():
    s3_link = 'https://s3-eu-west-1.amazonaws.com/adamtui/2015_6/20_7/dc9ee2c7-a8bd-40a8-bf80-a4bd007da9a5/AC9953935_MAJ_ALC_34131.jpg'
    event = {
                's3_path': s3_link,
                'hash_types': ['ahash', 'phash', 'dhash']
            }
    lambda_handler(event, None)


if __name__ == '__main__':
    main()

