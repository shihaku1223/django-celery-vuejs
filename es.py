from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch("searchappbackend:9200")

import json

query = {
    "query": {
        "bool": {
            "must": [],
            "must_not": []
        }
    }
}

filterQuery = {
    "bool": {
        "should": [
            { "term": { "project.name": "CV2K_App_内部課題" } },
            { "term": { "project.name": "CV2K_App" } }
        ]
    }
}

query["query"]["bool"]["filter"] = filterQuery

mustQuery = query["query"]["bool"]["must"]
mustQuery.append({
    "match":  { "summary": "アプリ" }
})
mustQuery.append({
    "match":  { "summary": "製品機能試験" }
})


mustNotQuery = query["query"]["bool"]["must_not"]
mustNotQuery.append({
    "match":  { "summary": "リアルタイム反映" }
})


print(json.dumps(query))
#res = es.search(index="issues", body={"query": {"match_all": {}}})

res = es.search(index="test-issues",
                body=query,
                size=1000,
                scroll="1m")
print("Got %d Hits:" % res['hits']['total']['value'])
total = res['hits']['total']['value']
for hit in res['hits']['hits']:
    print(hit["_source"]["id"])

scrollId = res["_scroll_id"]
scrollSize = len(res['hits']['hits'])

while(scrollSize > 0):

    res = es.scroll(scroll_id=scrollId, scroll="1m")
    scrollId = res["_scroll_id"]
    scrollSize = len(res['hits']['hits'])

    for hit in res['hits']['hits']:
        print(hit["_source"]["id"])


print(total)
es.clear_scroll(scroll_id=scrollId)
