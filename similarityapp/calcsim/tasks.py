from celery import shared_task

from calcsim.models import CalcTask, TaskStatus, TaskStatusToString
from similarityapp.utils import execute

@shared_task(bind=True)
def executeCalculation(self, log_id = None, symbol_id = None):

    taskUUIDStr = executeCalculation.request.id

    task = CalcTask(task_id = taskUUIDStr,
        status = TaskStatusToString(TaskStatus.CREATED))
    task.save()

    args = ['-l']
    result = execute("ls", args)
    if result['returncode'] != 0:
        task.status = TaskStatusToString(
            TaskStatus.FAILED)
    else:
        task.status = TaskStatusToString(
            TaskStatus.SUCCESS)

    task.save()
    return task
