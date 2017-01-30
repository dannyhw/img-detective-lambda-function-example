from __future__ import print_function

import imagedetective.detective as detective
import imagedetective.elastic_index_helper as elastic


def lambda_handler(event, context):
    hashes = detective.prepare_evidence(event)
    elastic.save_index(hashes, event['s3_url'])


def main():
    s3_link = 'https://s3-eu-west-1.amazonaws.com/adamtui/2015_6/20_7/dc9ee2c7-a8bd-40a8-bf80-a4bd007da9a5/AC9953935_MAJ_ALC_34131.jpg'
    event = {
                's3_url': s3_link,
                'hash_types': ['ahash', 'phash', 'dhash']
            }
    lambda_handler(event, None)


if __name__ == '__main__':
    main()
