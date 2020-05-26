from celery import shared_task

from calcsim.models import CalcTask, TaskStatus, TaskStatusToString

@shared_task(bind=True)
def executeCalculation(self, log_id = None, symbol_id = None):

    taskUUIDStr = executeCalcuation.request.id

    task = CalcTask(task_id = taskUUIDStr,
        status = TaskStatusToString(TaskStatus.CREATED))
    task.save()

    return task
