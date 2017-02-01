import base64
import os

import hash_generator
import requests

requests.packages.urllib3.disable_warnings()

LOCAL_IMAGES = "/tmp/images/"


def parse_s3_url(s3_url):
    # split https://s3.region.amazonaws.com/bucket/folder/filename to be
    # ['https:', '', 's3.region.amazonaws.com', 'bucket', 'folder', 'filename']
    path_parts = s3_url.split('/')
    file_name = path_parts[-1]
    bucket_name = path_parts[3]
    s3_key = '/'.join(path_parts[4:])

    return file_name, bucket_name, s3_key


def save_image_from_s3_locally(s3_url, file_name):
    if not os.path.exists(LOCAL_IMAGES):
        os.mkdir(LOCAL_IMAGES)
    image_path = LOCAL_IMAGES + file_name

    img_data = requests.get(s3_url).content
    with open(image_path, 'wb') as handler:
        handler.write(img_data)
    return image_path


def get_url_from_event(event):
    s3_url = ''
    if 's3_url' in event:
        s3_url = event['s3_url']
        print("Url from direct lambda call: ", s3_url)
    else:
        record = event["Records"][0]
        if 'kinesis' in record:
            s3_url = base64.b64decode(record['kinesis']['data'])
            print("Url from  Kenesis: ", s3_url)
    return s3_url


def prepare_evidence(event):
    s3_url = get_url_from_event(event)
    if 'hash_types' in event:
        hash_types = event['hash_types']
    else:
        hash_types = ['ahash', 'phash', 'dhash']
        print("No hash types specified, using defaults")
    file_name, bucket_name, s3_key = parse_s3_url(s3_url)
    image_path = save_image_from_s3_locally(s3_url, file_name)
    hash_lists = hash_generator.get_image_hashes(image_path, hash_types)
    return hash_generator.prepare_for_query(hash_lists)
