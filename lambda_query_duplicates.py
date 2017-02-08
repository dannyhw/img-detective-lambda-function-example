from __future__ import print_function

import imagedetective.detective as detective
import imagedetective.elastic_index_helper as elastic


def lambda_handler(event, context):
    print(event)

    hashes = detective.prepare_evidence(event)

    if 'duplicate_threshold' in event:
        duplicate_threshold = event['duplicate_threshold'] + "%"
    else:
        duplicate_threshold = "75%"

    suspects = elastic.query_index(hashes, duplicate_threshold)
    url = detective.get_url_from_event(event)

    print("suspects before removing same url", suspects)

    if url in suspects:
        suspects.remove(url)

    return {'suspects': suspects}


def main():
    event = {
                "s3_url": "https://s3.eu-central-1.amazonaws.com/tuichhackathon/image-detective/LIB_SHU_12_F995_RFPreview.jpg",
                "hash_types": ["ahash", "phash", "dhash"],
                "duplicate_threshold": "82"
            }
    lambda_handler(event, None)


if __name__ == '__main__':
    main()
