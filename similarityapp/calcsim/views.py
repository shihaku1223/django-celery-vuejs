from django.shortcuts import render

from .models import CalcTask

from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.generics import GenericAPIView, ListAPIView

from django.http import HttpResponse

# Create your views here.

class TaskCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    model = CalcTask
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, world. You're at the polls index.")

    def post(self, request, *args, **kwargs):
        return HttpResponse("Hello, world. You're at the polls index.")
