from django.shortcuts import render

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.generics import GenericAPIView, ListAPIView
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.renderers import JSONRenderer

from django.http import HttpResponseNotFound
from django.http import HttpResponse

from .models import CalcTask
from .tasks import executeCalculation
from .serializers import CalcTaskSerializer

from pymongo import MongoClient
from similarityapp.settings import MONGO_HOST, MONGO_USER, MONGO_PASS

# Create your views here.

class TaskResultRetrieveView(RetrieveAPIView):
    renderer_classes = (JSONRenderer, )

    def retrieve(self, request, task_id, *args, **kwargs):
        content = {}
        return Response(content, status=status.HTTP_200_OK)

class TaskRetrieveView(RetrieveAPIView):
    renderer_classes = (JSONRenderer, )
    serializer_class = CalcTaskSerializer

    def retrieve(self, request, task_id, *args, **kwargs):
        task = None
        try:
            task = CalcTask.objects.get(task_id=task_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound(
                '{} task not found.'.format(task_id))

        client = MongoClient(MONGO_HOST,
            username=MONGO_USER, password=MONGO_PASS)

        db = client['similarity']
        result = db.tasks.find_one(
            {"task_id": str(task_id)},
            { "_id": 0 }
        )

        if result is not  None:
            content = {}
            content['task_id'] = task.task_id
            content['status'] = task.status
            content['result'] = result['result']
            return Response(content, status=status.HTTP_200_OK)

        serializer = self.serializer_class(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):

    model = CalcTask
    renderer_classes = (JSONRenderer, )
    queryset = CalcTask.objects.all()
    serializer_class = CalcTaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        projectName = request.data['projectName']
        mantisId = request.data['mantisId']
        textPhrase = request.data['textPhrase']
        numberToShow = request.data['numberToShow']
        mantisUrl = request.data['mantisUrl']
        method = request.data['method']
        column = request.data['column']

        print(projectName)
        print(mantisId)
        print(textPhrase)
        print(mantisUrl)
        print(column)

        result =  executeCalculation.delay(
            mantisId,
            textPhrase,
            projectName,
            mantisUrl,
            numberToShow,
            method,
            column)

        return Response({
          'task_id': result.id
        })
