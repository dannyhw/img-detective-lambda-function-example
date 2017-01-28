import elasticsearch

elasticsearch_host = "localhost"
elasticsearch_port = "9200"
es = elasticsearch.Elasticsearch([{'host': elasticsearch_host,
                                   'port': elasticsearch_port}])


def save_index(hashes, identifier):
    res = es.index(index="image-detective-test", doc_type='hash', body=hashes,
                   id=identifier)
    if res['created']:
        print("stored successfully")
    else:
        print("failed to store index")
