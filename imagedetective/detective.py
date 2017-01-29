import os
import urllib

import hash_generator
LOCAL_IMAGES = "/tmp/images/"


def parse_s3_url(s3_url):
    # split https://s3.region.amazonaws.com/bucket/folder/filename to be
    # ['https:', '', 's3.region.amazonaws.com', 'bucket', 'folder', 'filename']
    path_parts = s3_url.split('/')
    file_name = path_parts[-1]
    bucket_name = path_parts[3]
    s3_key = '/'.join(path_parts[4:])

    return file_name, bucket_name, s3_key


def s3_key_from_s3_url(s3_url):
    return '/'.join(s3_url.split('/')[4:])


def file_name_from_s3_url(s3_url):
    return s3_url.split('/')[-1]


def save_image_from_s3_locally(s3_url, file_name):
    if not os.path.exists(LOCAL_IMAGES):
        os.mkdir(LOCAL_IMAGES)
    image_path = LOCAL_IMAGES + file_name
    urllib.urlretrieve(s3_url, image_path)
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
