from celery import shared_task

from calcsim.models import CalcTask, TaskStatus, TaskStatusToString
from similarityapp.utils import execute
from similarityapp.settings import MANTIS_HOST, MANTIS_USER, MANTIS_PASS
from mantis_soap.Connector import Connector

# similarity calculation function
from similarityapp.app import calculateByTicketIdwithProject
from similarityapp.app import calculateByTextwithProject

@shared_task(bind=True)
def executeCalculation(self, mantisId,
        textPhrase, projectName, mantisUrl,
        numbers=130, method='id', column='summary'):

    wsdlUrl = mantisUrl + '/api/soap/mantisconnect.php?wsdl'
    mantisConnector = Connector(
        wsdlUrl, MANTIS_USER, MANTIS_PASS)
    mantisConnector.connect()

    projectId = mantisConnector.getProjectId(projectName)
    issues = mantisConnector.getProjectIssues(projectId)
    #issues = mantisConnector.getIssuesByFilter(projectId, 11092, 0, 0)

    taskUUIDStr = executeCalculation.request.id

    task = CalcTask(task_id = taskUUIDStr,
        status = TaskStatusToString(TaskStatus.CREATED))
    task.save()

    result = {}
    try:
        issue = mantisConnector.getIssue(mantisId)

        if method == 'id':
            result = calculateByTicketIdwithProject(
                mantisId, issue, issues, column)
        elif method == 'text':
            result = calculateByTextwithProject(
                textPhrase, issues, column)

        task.status = TaskStatusToString(
            TaskStatus.SUCCESS)
    except:
        task.status = TaskStatusToString(
            TaskStatus.FAILED)

    task.save()

    resultList = []
    mantisURL='http://10.156.2.84/mantis/ipf3/app/view.php?id={}'
    i = 0
    t = iter(result)
    print(len(result))
    try:
        while i < numbers:
            key = next(t)
            if key == -1:
                i = i + 1
                continue

            obj = {}
            obj['href'] = mantisURL.format(key)
            obj['score'] = '{}'.format(result[key])
            resultList.append(obj)
            i = i + 1
    except StopIteration:
        pass

    return resultList
