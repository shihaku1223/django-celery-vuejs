from django.shortcuts import render
from django.http import QueryDict

# Create your views here.

from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import mixins, status

from pymongo import MongoClient
from similarityapp.settings import MONGO_HOST, MONGO_USER, MONGO_PASS

from similarityapp.settings import ELASTICSEARCH_URL
import re
import json

import elasticsearch
from elasticsearch import Elasticsearch

class ESSearch:

    es = Elasticsearch(ELASTICSEARCH_URL)

    scroll_id = None
    scroll_size = None

    def generateQuery(self, keywords, targetProjects, targets=[], options={}):

        notPattern = re.compile("^-(.*)")

        must_not_keywords = []
        must_keywords = []

        for term in keywords:
            r = notPattern.search(term)
            if r is not None:
                must_not_keywords.append(r.group(1))
            else:
                must_keywords.append(term)

        query = {
            "_source": targets,
            "query": {
                "bool": {
                    "must": [],
                    "must_not": []
                },
            }
        }

        mustQuery = query["query"]["bool"]["must"]
        self.appendQueryStringKeywords(must_keywords, mustQuery)

        mustNotQuery = query["query"]["bool"]["must_not"]
        self.appendQueryStringKeywords(must_not_keywords, mustNotQuery)


        # filter projects
        projectQuery = self.generateShouldProjectsQuery(targetProjects)

        filterQuery = {
            "bool": { "must":[] }
        }
        f = filterQuery["bool"]["must"]
        f.append(projectQuery)

        if "status" in options:
            statusQuery = self.generateOptionQuery("status", options)

            if statusQuery is not None:
                f.append(statusQuery)

        if "resolution" in options:
            resolutionQuery = self.generateOptionQuery("resolution", options)

            if resolutionQuery is not None:
                f.append(resolutionQuery)

        for k, v in options.items():

            items = v.split(',')
            for item in items:
                d = { "term": { k + '.name': item } }
                f.append(d)

        query["query"]["bool"]["filter"] = filterQuery

        return query


    def generateOptionQuery(self, keyName, options):

        items = options[keyName].split(',')

        if "全て" in items:
            del options[keyName]
            return None

        query = self.generateShouldQuery(keyName, items)

        del options[keyName]

        return query

    def generateShouldQuery(self, keyName, items):
        query = {
            "bool": {
                "should": [
                ]
            }
        }
        f = query["bool"]["should"]
        for s in items:
            d = { "term": { keyName + ".name": s } }
            f.append(d)

        return query


    def generateShouldProjectsQuery(self, targetProjects):
        query = {
            "bool": {
                "should": [
                ]
            }
        }
        f = query["bool"]["should"]
        for p in targetProjects:
            d = { "term": { "project.name": p } }
            f.append(d)

        return query

    def appendQueryStringKeywords(self, keywords, query):
        for k in keywords:
            query.append({
                "query_string":  { "query": k }
            })


    def appendMatchKeywords(self, keywords, query):
        for k, v in keywords.items():
            query.append({
                "match":  { k: v }
            })

    def search(self, index,
               keywords,
               targetProjects,
               targetSources, options, size=50, scroll="1m"):

        query = self.generateQuery(keywords,
                    targetProjects,
                    targetSources,
                    options)

        print(json.dumps(query))

        res = self.es.search(index=index,
                body=query,
                size=size,
                scroll=scroll)


        print("Got %d Hits:" % res['hits']['total']['value'])

        total = res['hits']['total']['value']
        scroll_id = res["_scroll_id"]
        scroll_size = len(res['hits']['hits'])

        print(scroll_id)

        if scroll_size > 0:
            return (
                scroll_id,
                scroll_size,
                total,
                list(map(self.toSource, res['hits']['hits']))
            )

        return (None, None, 0, None)

    def scroll(self, scroll_id, scroll="1m"):
        res = self.es.scroll(scroll_id=scroll_id, scroll=scroll)

        scroll_id = res["_scroll_id"]
        scroll_size = len(res['hits']['hits'])

        if scroll_size > 0:
            return (
                scroll_id,
                scroll_size,
                list(map(self.toSource, res['hits']['hits']))
            )

        return (None, None, None)


    def clear_scroll(self, scroll_id):
        self.es.clear_scroll(scroll_id=scroll_id)

    def toSource(self, obj):
        return obj['_source']

class ESSearchView(GenericAPIView):

    renderer_classes = (JSONRenderer, )

    ess = ESSearch()

    def post(self, request, *args, **kwargs):
        print(request.GET.urlencode())

        q = QueryDict(request.GET.urlencode())
        keywords = q['q'].split()

        if q['p'] == '':
            targetProjects=[]
        else:
            targetProjects = q['p'].split(',')

        try:
            targetSources = q['s'].split(',')
        except:
            targetSources = []

        print('data')
        for k, v in request.data.items():
            print("key", k, "val", v)

        scroll_id, scroll_size, total, r = self.ess.search(
            "issues",
            keywords,
            targetProjects,
            targetSources,
            request.data)

        content = {}
        content["scroll_id"] = scroll_id
        content["scroll_size"] = scroll_size
        content["total"] = total
        content["result"] = r

        return Response(content, status=status.HTTP_200_OK)

class ESScrollView(RetrieveAPIView):
    renderer_classes = (JSONRenderer, )

    ess = ESSearch()

    def retrieve(self, request, scroll_id, *args, **kwargs):
        print(scroll_id)

        r = None
        error = None
        try:
            scroll_id, scroll_size, r = self.ess.scroll(scroll_id)
        except elasticsearch.exceptions.RequestError as e:
            print(e.info)
            error = e.info["error"]["root_cause"][0]["reason"]
        except elasticsearch.exceptions.NotFoundError as e:
            print(e.info)
            error = e.info["error"]["root_cause"][0]["reason"]
        except Exception as e:
            error = e.info["error"]["root_cause"][0]["reason"]

        content = {}
        response_status = status.HTTP_200_OK
        if error is not None:
            content["error"] = error
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        elif r is not None:
            print(scroll_size)
            print(scroll_id)
            content["scroll_id"] = scroll_id
            content["scroll_size"] = scroll_size
            content["result"] = r
        else:
            print("clear scroll")
            try:
                self.ess.clear_scroll(scroll_id)
            except Exception as e:
                pass

        return Response(content, status=response_status)

class SearchView(GenericAPIView):

    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        print(request.GET.urlencode())

        q = QueryDict(request.GET.urlencode())

        r = self.searchKeyword(q['q'], q['p'])
        r = None

        content = {}
        if r is not None:
            content["result"] = r

        return Response(content, status=status.HTTP_200_OK)

    def getQueryPipeline(self, queryString, targetProjects):
        pipeline = [
            { "$match": {
                "$and": [
                  { "$text": { "$search": queryString } }
                ]
              }
            },
            { "$sort": { "score": { "$meta": "textScore" } } },
            { "$project": {
                "_id": 0,
                "id": 1,
                "project.name": 1,
                "summary": 1,
                "description": 1,
                "steps_to_reproduce": 1,
                "additional_information": 1,
                "status.name": 1,
                "handler.real_name": 1
            }}
        ]

        if len(targetProjects) > 0:
            projectPipeline = {
                "$or": []
            }

            for project in targetProjects:
                projectPipeline["$or"].append({
                    "project.name": project
                })
            pipeline[0]["$match"]["$and"].append(projectPipeline)

        return pipeline
    def getPipelineResult(self, client, pipeline):
        db = client['mantis']
        return list(db.issues.aggregate(pipeline))

    def searchKeyword(self, queryString, projectString):
        client = MongoClient(MONGO_HOST,
            username=MONGO_USER, password=MONGO_PASS)

        targetProjects = projectString.split(',')

        r = self.getPipelineResult(client,
                self.getQueryPipeline(queryString, targetProjects))
        return r
