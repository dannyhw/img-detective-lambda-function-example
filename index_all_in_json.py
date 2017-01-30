import json
from lambda_index_one import lambda_handler
with open('TUI_DS_S3Paths.json') as data_file:
    data = json.load(data_file)
    for s3_url in data:
        lambda_handler({'s3_url': s3_url,
                        'hash_types': ['ahash', 'phash', 'dhash']}, None)
