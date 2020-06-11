from celery import shared_task

from calcsim.models import CalcTask, TaskStatus, TaskStatusToString
from similarityapp.utils import execute
from similarityapp.settings import MANTIS_HOST, MANTIS_USER, MANTIS_PASS
from similarityapp.settings import MONGO_HOST, MONGO_USER, MONGO_PASS
from similarityapp.settings import CALCAPP_PATH
from mantis_soap.Connector import Connector

# similarity calculation function
from similarityapp.app import calculateByTicketIdwithProject
from similarityapp.app import calculateByTextwithProject
from similarityapp.app import get_issues_by_project
from similarityapp.app import insert_task_result

from django.conf import settings
from pathlib import Path

@shared_task(bind=True)
def executeCalculation(self, mantisId,
        textPhrase, projectName, mantisUrl,
        numbers=130, method='id', column='summary'):

    """
    wsdlUrl = mantisUrl + '/api/soap/mantisconnect.php?wsdl'
    mantisConnector = Connector(
        wsdlUrl, MANTIS_USER, MANTIS_PASS)
    mantisConnector.connect()

    projectId = mantisConnector.getProjectId(projectName)
    issues = get_issues_by_project(projectName,
        MONGO_HOST, MONGO_USER, MONGO_PASS)

    print(len(issues))
    """
    taskUUIDStr = executeCalculation.request.id

    task = CalcTask(task_id = taskUUIDStr,
        status = TaskStatusToString(TaskStatus.CREATED))
    task.save()

    args = [
        "--task-id", taskUUIDStr,
        "--mongo-host", MONGO_HOST,
        "--mongo-user", MONGO_USER,
        "--mongo-pass", MONGO_PASS,
        "--project", projectName,
        "--user", MANTIS_USER,
        "--password", MANTIS_PASS,
        "--column", column
    ]

    result = {}
    try:
        #issue = mantisConnector.getIssue(mantisId)

        if method == 'id':
            args.append("--id")
            args.append(str(mantisId))
            """
            result = calculateByTicketIdwithProject(
                mantisId, issue, issues, column)
            """
        elif method == 'text':
            args.append("--text")
            args.append(textPhrase)
            """
            result = calculateByTextwithProject(
                textPhrase, issues, column)
            """
        """
        resultList = []
        mantisURL='http://10.156.2.84/mantis/ipf3/app/view.php?id={}'
        i = 0
        t = iter(result)
        try:
            while i < numbers:
                key = next(t)
                if key == -1:
                    print('text phrase', args.text)
                    continue
                obj = {}
                obj['href'] = mantisURL.format(result[key]['id'])
                obj['score'] = '{}'.format(result[key]['value'])
                resultList.append(obj)
                i = i + 1
        except StopIteration:
            pass

        insert_task_result(taskUUIDStr, resultList,
            MONGO_HOST, MONGO_USER, MONGO_PASS)
        """
        binaryPath = Path(CALCAPP_PATH)
        result = execute(['python3', CALCAPP_PATH], args)
        if result['returncode'] != 0:
            raise Exception('error')

        task.status = TaskStatusToString(
            TaskStatus.SUCCESS)
    except Exception as e:
        print(e)
        task.status = TaskStatusToString(
            TaskStatus.FAILED)

    task.save()
