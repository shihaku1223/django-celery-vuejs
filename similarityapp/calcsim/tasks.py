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
        numbers=130, method='id'):

    wsdlUrl = mantisUrl + '/api/soap/mantisconnect.php?wsdl'
    mantisConnector = Connector(
        wsdlUrl, MANTIS_USER, MANTIS_PASS)
    mantisConnector.connect()

    projectId = mantisConnector.getProjectId(projectName)
    issues = mantisConnector.getProjectIssues(projectId)

    taskUUIDStr = executeCalculation.request.id

    task = CalcTask(task_id = taskUUIDStr,
        status = TaskStatusToString(TaskStatus.CREATED))
    task.save()

    try:
        issue = mantisConnector.getIssue(mantisId)
    except:
        print('no issue found')

    print('calculate')
    try:
        if method == 'id':
            result = calculateByTicketIdwithProject(
                mantisId, issue, issues, 'description')
        elif method == 'text':
            result = calculateByTextwithProject(
                textPhrase, issues, 'description')
        print(result)

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

            print(mantisURL.format(key) +
                  ' score {}'.format(result[key]))
            i = i + 1
    except StopIteration:
        pass

    return resultList
