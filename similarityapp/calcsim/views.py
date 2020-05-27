from django.shortcuts import render

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.generics import GenericAPIView, ListAPIView

from rest_framework.renderers import JSONRenderer

from django.http import HttpResponse

from .models import CalcTask
from .tasks import executeCalculation
from .serializers import CalcTaskSerializer

# Create your views here.

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
        data = {}

        projectName = request.data['projectName']
        mantisId = request.data['mantisId']
        textPhrase = request.data['textPhrase']
        numberToShow = request.data['numberToShow']
        mantisUrl = request.data['mantisUrl']
        method = request.data['method']

        print(projectName)
        print(mantisId)
        print(textPhrase)
        print(mantisUrl)

        result =  executeCalculation.delay(
            mantisId,
            textPhrase,
            projectName,
            mantisUrl,
            numberToShow,
            method)
        print(result.get())
        data['result'] =  result.get()

        return Response(data)
