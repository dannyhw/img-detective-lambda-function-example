from __future__ import print_function

import imagedetective.detective as detective
import imagedetective.elastic_index_helper as elastic


def lambda_handler(event, context):
    hashes = detective.prepare_evidence(event)

    if 'duplicate_threshold' in event:
        duplicate_threshold = event['duplicate_threshold']
    else:
        duplicate_threshold = "75%"

    suspects = elastic.query_index(hashes, duplicate_threshold)
    url = detective.get_url_from_event(event)

    print("suspects before removing same url", suspects)

    if url in suspects:
        suspects.remove(url)

    return {'suspects': suspects}


def main():
    s3_link = 'https://s3-eu-west-1.amazonaws.com/adamtui/2016_10/31_14/d36e3561-50f8-4884-9795-a6b000eca6b1/IL241342Preview.jpg'
    event = {
                's3_url': s3_link,
                'hash_types': ['ahash', 'phash', 'dhash']
            }
    lambda_handler(event, None)


if __name__ == '__main__':
    main()
