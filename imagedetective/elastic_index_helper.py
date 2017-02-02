from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

host = 'search-image-detective-c2x7sc3cfwdlmc2gw5qpca4pwa.eu-central-1.es.amazonaws.com'
awsauth = AWS4Auth('', '', 'eu-central-1', 'es')
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

INDEX_NAME = "image-detective-hackathon"


def save_index(hashes, identifier):
    res = es.index(index=INDEX_NAME, doc_type='hash', body=hashes,
                   id=identifier)
    if res['created']:
        print("stored successfully")
    else:
        print("failed to store index")


def query_index(hashes, duplicate_threshold):
    full_query = {
        "query": {
            "bool": {
                'minimum_should_match': duplicate_threshold,
                "should": []
            }
        }
    }

    hash_type = 'dhash'
    these_hashes = [key for key in hashes.keys() if hash_type in key]
    for hash_key in these_hashes:
        term = {'term': {hash_key: hashes[hash_key]}}
        full_query['query']['bool']['should'].append(term)

    print full_query

    query_result = es.search(index=INDEX_NAME, doc_type='hash',
                             body=full_query, size=500)
    return [result_doc['_id'] for result_doc in query_result['hits']['hits']]
