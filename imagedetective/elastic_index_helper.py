import elasticsearch

ELASTICSEARCH_HOST = "localhost"
ELASTICSEARCH_PORT = "9200"
es = elasticsearch.Elasticsearch([{'host': ELASTICSEARCH_HOST,
                                   'port': ELASTICSEARCH_PORT}])
INDEX_NAME = "image-detective-test"


def save_index(hashes, identifier):
    res = es.index(index=INDEX_NAME, doc_type='hash', body=hashes,
                   id=identifier)
    if res['created']:
        print("stored successfully")
    else:
        print("failed to store index")


def query_index(hashes):
    full_query = {
        "query": {
            "bool": {
                'minimum_should_match': "75%",
                "should": []
            }
        }
    }

    hash_type = 'dhash'
    these_hashes = [key for key in hashes.keys() if hash_type in key]
    for hash_key in these_hashes:
        term = {'term': {hash_key: hashes[hash_key]}}
        full_query['query']['bool']['should'].append(term)

    query_result = es.search(index=INDEX_NAME, doc_type='hash',
                             body=full_query, size=500)
    return [result_doc['_id'] for result_doc in query_result['hits']['hits']]
