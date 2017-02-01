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
    # urlretrieve(s3_url, image_path)

    img_data = requests.get(s3_url).content
    with open(image_path, 'wb') as handler:
        handler.write(img_data)
    return image_path


def prepare_evidence(event):
    s3_url = event['s3_url']
    if 'hash_types' in event:
        hash_types = event['hash_types']
    else:
        hash_types = ['ahash', 'phash', 'dhash']
        print("No hash types specified, using defaults")
    file_name, bucket_name, s3_key = parse_s3_url(s3_url)
    image_path = save_image_from_s3_locally(s3_url, file_name)
    hash_lists = hash_generator.get_image_hashes(image_path, hash_types)
    return hash_generator.prepare_for_query(hash_lists)
