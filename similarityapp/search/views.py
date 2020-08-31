from django.shortcuts import render
from django.http import QueryDict

# Create your views here.

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import mixins, status

from pymongo import MongoClient
from similarityapp.settings import MONGO_HOST, MONGO_USER, MONGO_PASS

class SearchView(GenericAPIView):

    renderer_classes = (JSONRenderer, )
    def get(self, request, *args, **kwargs):
        print(request.GET.urlencode())

        q = QueryDict(request.GET.urlencode())
        print(q['q'])

        r = self.searchKeyword(q['q'])

        content = {}
        if r is not None:
            content["result"] = r

        return Response(content, status=status.HTTP_200_OK)

    def getQueryPipeline(self, queryString):
        return [
            { "$match": { "$text": { "$search": queryString } } },
            { "$sort": { "score": { "$meta": "textScore" } } },
            { "$project": {
                "_id": 0,
                "id": 1,
                "summary": 1,
                "status.name": 1,
                "handler.real_name": 1
            }}
        ]
    def getPipelineResult(self, client, pipeline):
        db = client['mantis']
        return list(db.issues.aggregate(pipeline))

    def searchKeyword(self, queryString):
        client = MongoClient(MONGO_HOST,
            username=MONGO_USER, password=MONGO_PASS)

        r = self.getPipelineResult(client,
                self.getQueryPipeline(queryString))
        return r
