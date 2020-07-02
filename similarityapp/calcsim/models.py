from django.db import models
import jsonfield
from enum import Enum

class TaskStatus(Enum):
    CREATED = 1
    RUNNING = 2
    INTERRUPTED = 3
    STOPPED = 4
    SUCCESS = 5
    FAILED = 6

TaskStatusMap = {
    TaskStatus.CREATED: 'created',
    TaskStatus.RUNNING: 'running',
    TaskStatus.INTERRUPTED: 'interrupted',
    TaskStatus.SUCCESS: 'success',
    TaskStatus.FAILED: 'failed',
    TaskStatus.STOPPED: 'stopped',
}

def TaskStatusToString(status):
    return TaskStatusMap[status]

class CalcTask(models.Model):

    task_id = models.CharField(max_length=32, blank=True, unique=True)

    status = models.CharField(max_length=20)

    message = models.CharField(max_length=80, default='')

    timestamp = models.DateTimeField(auto_now_add=True)
