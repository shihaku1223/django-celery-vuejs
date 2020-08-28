from django.shortcuts import render

# Create your views here.

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import mixins, status

class SearchView(GenericAPIView):

    renderer_classes = (JSONRenderer, )
    def get(self, request, *args, **kwargs):
        content = {}
        return Response(content, status=status.HTTP_200_OK)

