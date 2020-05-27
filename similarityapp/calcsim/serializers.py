from rest_framework import serializers
from .models import CalcTask

class CalcTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalcTask
        fields = '__all__'
