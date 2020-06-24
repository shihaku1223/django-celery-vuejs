#!env python3

import tensorflow_hub as hub
import tensorflow_text
import collections

import argparse
import numpy

from mantis_soap.Connector import Connector
import csv
import sys
import io
import zeep

from pymongo import MongoClient

def insert_vectors(ticketId, summary, description, steps,
        host, username, password):
    client = MongoClient(host, username=username, password=password)

    db = client['similarity']
    collect = db['vectors']
    obj = {}
    obj['ticketId'] = ticketId
    obj['description'] = description
    obj['summary'] = summary
    if steps is not None:
        obj['steps_to_reproduce'] = steps

    try:
        ids = collect.insert_one(obj)
    except Exception as e:
        raise(e)

    client.close()

def insert_task_result(task_id, result_list,
        host, username, password):
    client = MongoClient(host, username=username, password=password)

    db = client['similarity']
    collect = db['tasks']
    obj = {}
    obj['task_id'] = task_id
    obj['result'] = result_list

    try:
        ids = collect.insert_one(obj)
    except Exception as e:
        raise(e)

    client.close()

def get_issues_by_project(project, host, username, password):
    client = MongoClient(host, username=username, password=password)

    pipeline = [
        { "$match": { "$and":[ { 'project.name': project  } ] } },
        { "$project": {
            "id": 1,
            "summary": 1,
            "description": 1,
            "project": 1
        } }
    ]
    db = client['mantis']
    result = db.issues.aggregate(pipeline)
    client.close()
    return list(result)

def get_issues_by_projectId(projectId, host, username, password):
    client = MongoClient(host, username=username, password=password)

    pipeline = [
        { "$match": { "$and":[ { 'project.id': projectId  } ] } },
        { "$project": {
            "id": 1,
            "summary": 1,
            "description": 1,
            "project": 1
        } }
    ]
    db = client['mantis']
    result = db.issues.aggregate(pipeline)
    client.close()
    return list(result)


def cos_sim(v1, v2):
    return numpy.dot(v1, v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))


def sort_result(x, y):
    r = {}

def __retrieveVector(client, ticketId):
    pipeline = [
        { "$match": { 'ticketId': ticketId }},
        { "$project": {
            "ticketId": 1,
            "description": 1,
            "summary": 1,
            'steps_to_reproduce': 1
          }
        }
    ]
    db = client['similarity']
    result = db.vectors.aggregate(pipeline)

    return list(result)[0]


def retrieveVector(ticketId, host, username, password):
    client = MongoClient(host, username=username, password=password)

    pipeline = [
        { "$match": { 'ticketId': ticketId }},
        { "$project": {
            "ticketId": 1,
            "description": 1,
            "summary": 1,
            'steps_to_reproduce': 1
          }
        }
    ]
    db = client['similarity']
    result = db.vectors.aggregate(pipeline)

    client.close()
    return list(result)[0]

def serializeNumpy(vector):
    out = io.BytesIO()
    numpy.save(out, vector)
    out.seek(0)
    serialized = out.read()
    return serialized

def unserializeNumpy(b):
    inStream = io.BytesIO(b)
    inStream.seek(0)
    data = numpy.load(inStream)

    return data


def calculateVectors(ticketsDict):
    embed = hub.load(
        "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

    columns = [
        'summary',
        'description',
        'steps_to_reproduce'
    ]

    for __id, ticket in ticketsDict.items():
        print('calculate {}'.format(__id))
        texts = []
        for column in columns:
            try:
                if ticket[column] is not None:
                    texts.append(ticket[column])
            except:
                pass

        vectors = embed(texts)
        summary = serializeNumpy(vectors[0].numpy())
        description = serializeNumpy(vectors[1].numpy())
        steps = None
        try:
            steps = serializeNumpy(vectors[2].numpy())
        except:
            pass

        insert_vectors(__id, summary, description, steps,
            args.mongo_host, args.mongo_user, args.mongo_pass)
        """
        vectors = retrieveVector(__id,
            args.mongo_host, args.mongo_user, args.mongo_pass)

        print('summary', unserializeNumpy(vectors['summary']))
        print('description', unserializeNumpy(vectors['description']))
        try:
            print('steps', unserializeNumpy(vectors['steps_to_reproduce']))
        except:
            print('no steps to reproduce')

        """

# calculating function using calcuated vector data
def calculateFetch(texts: list, idList: list, ticketsDict: dict, column: str):
    resultDict = {}
    embed = hub.load(
        "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

    calculated = {}
    client = MongoClient(args.mongo_host,
                         username=args.mongo_user,
                         password=args.mongo_pass)

    for __id, ticket in ticketsDict.items():
        if __id != idList[0]:
            vectors = __retrieveVector(client, __id)
            calculated[__id] = unserializeNumpy(vectors[column])
            idList.append(__id)
    client.close()

    # calculate the vector of target to compare
    result = embed(texts)

    # calculate the similarity
    length = len(idList)
    # start from the second record
    # the first record is the target compare to
    i = 1
    while i < length:
        obj = {}
        _id = idList[i]

        obj['id'] = _id
        obj['value'] = cos_sim(result[0], calculated[_id])
        resultDict[_id] = obj
        i = i + 1

    sorted_result = collections.OrderedDict(sorted(
        resultDict.items(), key=lambda x: x[1]['value'], reverse=True))

    return sorted_result

def calculate(texts: list, idList: list, ticketsDict: dict, column: str):
    resultDict = {}

    embed = hub.load(
        "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

    # put the text of specified ticket
    for __id, ticket in ticketsDict.items():
        if __id != idList[0]:
            texts.append(ticket[column])
            idList.append(__id)

    result = embed(texts)

    # calculate the cos
    length = len(texts)
    i = 1
    while i < length:
        obj = {}
        obj['id'] = idList[i]
        obj['value'] = cos_sim(result[0], result[i])
        resultDict[idList[i]] = obj
        i = i + 1

    sorted_result = collections.OrderedDict(sorted(
        resultDict.items(), key=lambda x: x[1]['value'], reverse=True))

    """
    sorted_result = sorted(resultDict,
        key=lambda x: x[1]['value'], reverse=True)
    """
    return sorted_result


def calculateText(text: str, ticketsDict: dict, column: str):

    # put the text and dummy id
    texts = [text]
    idList = [-1]

    return calculate(texts, idList,
        ticketsDict, column)

def calculateByTicketId(_id: int, ticketsDict: dict, column: str):

    # put the text of specified ticket
    texts = [ticketsDict[_id][column]]
    idList = [_id]

    return calculate(texts, idList,
        ticketsDict, column)

def calculateVectorswithProject(issues: list):
    print('calculate')
    ticketsDict = {}
    l = len(issues)
    i = 0
    while i < l:
        _issue = issues[i]
        ticketsDict[_issue['id']] = _issue

        if (i + 1) % 100 == 0:
            print(i)
            r = calculateVectors(ticketsDict)

            ticketsDict = {}
        i = i + 1

    r = calculateVectors(ticketsDict)

def calculateByTicketIdwithProject(_id: int, issue, issues: list, column: str):

    texts = [issue[column]]
    idList = [_id]
    result = {}

    ticketsDict = {}
    l = len(issues)
    i = 0
    while i < l:
        _issue = issues[i]
        ticketsDict[_issue['id']] = _issue

        if (i + 1) % 1000 == 0:
            r = calculateFetch(texts, idList, ticketsDict, column)

            #result.extend(r)
            result = {**result, **r}
            texts = [issue[column]]
            idList = [_id]
            ticketsDict = {}

        i = i + 1
    r = calculateFetch(texts, idList, ticketsDict, column)
    result = {**result, **r}

    """
    sorted_result = sorted(result,
        key=lambda x: x['value'], reverse=True)
    """
    sorted_result = collections.OrderedDict(sorted(
        result.items(), key=lambda x: x[1]['value'], reverse=True))

    return sorted_result

def calculateByTextwithProject(text: str, issues: list, column: str):

    texts = [text]
    idList = [-1]

    #result = []
    result = {}

    ticketsDict = {}
    l = len(issues)
    i = 0
    while i < l:
        _issue = issues[i]
        ticketsDict[_issue['id']] = _issue

        if (i + 1) % 1000 == 0:
            r = calculateFetch(texts, idList, ticketsDict, column)

            result = {**result, **r}
            texts = [text]
            idList = [-1]

            ticketsDict = {}

        i = i + 1
    r = calculateFetch(texts, idList, ticketsDict, column)
    #result.extend(r)
    result = {**result, **r}

    """
    sorted_result = sorted(result,
        key=lambda x: x['value'], reverse=True)
    """
    sorted_result = collections.OrderedDict(sorted(
        result.items(), key=lambda x: x[1]['value'], reverse=True))

    return sorted_result

def showResult(result, numbers: int):

    mantisURL='http://10.156.2.84/mantis/ipf3/app/view.php?id={}'

    """
    i = 0
    l = len(result)
    while i < numbers and i < l:
        print(mantisURL.format(result[i]['id']) +
              ' score {}'.format(result[i]['value']))
        i = i + 1
    """
    i = 0
    t = iter(result)
    try:
        while i < numbers:
            key = next(t)
            if key == -1:
                print('text phrase', args.text)
                i = i + 1
                continue

            print(mantisURL.format(key) +
                  ' score {}'.format(result[key]['value']))
            i = i + 1
    except StopIteration:
        return

def readCSV(csv_list):
    ticketsDict = {}
    for fileName in csv_list:
        with open(fileName, 'r', encoding='cp932') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['fileName'] = fileName
                ticketsDict[int(row['Id'])] = row
    return ticketsDict

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--id', type=int, help='Mantis Id')

    parser.add_argument('--show-id',
        action='store_true',
        help='list all of ticket id from csv files')

    parser.add_argument('--text', type=str,
        help='check the similarity with specified text')

    parser.add_argument('--user', type=str,
        help='Mantis User')

    parser.add_argument('--password', type=str,
        help='Mantis Password')

    parser.add_argument('--project', type=str,
        help='specify the project name to search from')

    parser.add_argument('--projectId', type=int,
        help='specify the project name to search from')

    parser.add_argument('--csvs', type=str, action='append',
        help='Mantis csv')

    parser.add_argument('--column', type=str, default='要約',
        help='specify the column of csv file to calculate')

    parser.add_argument('--nums', type=int, default=130,
        help='the number of result to show')

    parser.add_argument('--mongo-host', type=str, default=None,
        help='MongoDB Host')
    parser.add_argument('--mongo-user', type=str, default=None,
        help='MongoDB user')
    parser.add_argument('--mongo-pass', type=str, default=None,
        help='MongoDB password')

    parser.add_argument("--vectors", default = None, action='store_true',
        help = "calculate the vectors")

    parser.add_argument("--task-id", default = None, type=str,
        help = "task id")

    args = parser.parse_args()

    if args.projectId is not None:

        issues = get_issues_by_projectId(args.projectId,
            args.mongo_host, args.mongo_user, args.mongo_pass)

        if args.vectors is True:
            calculateVectorswithProject(issues)
            sys.exit(0)

    if args.project is not None:
        url = "http://osoft-de-c.olympus.co.jp/mantis/ipf3/app/api/soap/mantisconnect.php?wsdl"
        mantisConnector = Connector(url, args.user, args.password)
        mantisConnector.connect()

        projectId = mantisConnector.getProjectId(args.project)
        issues = get_issues_by_project(args.project,
            args.mongo_host, args.mongo_user, args.mongo_pass)

        if args.id is not None:
            issue = mantisConnector.getIssue(args.id)
            result = calculateByTicketIdwithProject(
                args.id, issue, issues, args.column)
        elif args.text is not None:
            result = calculateByTextwithProject(
                args.text, issues, args.column)

        if args.task_id is not None:
            resultList = []
            mantisURL='http://10.156.2.84/mantis/ipf3/app/view.php?id={}'
            i = 0
            t = iter(result)
            try:
                while i < args.nums:
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

            insert_task_result(args.task_id, resultList,
                args.mongo_host, args.mongo_user, args.mongo_pass)
            sys.exit(0)
        showResult(result, args.nums)
        sys.exit(0)

    print('reading csv files')
    if args.csvs is not None:
        ticketsDict = readCSV(args.csvs)
    print('ticket count {}'.format(len(ticketsDict)))

    if args.show_id is True:
        for key in sorted(ticketsDict):
            print(key , ticketsDict[key]['fileName'])
        sys.exit(0)

    result = None
    if args.id is not None:
        if args.id in ticketsDict:
            print('check the similarity with {}'.format(args.column))
            result = calculateByTicketId(args.id, ticketsDict, args.column)
        else:
            print('Cound not find the ticket id {}'.format(args.id))
    elif args.text is not None:
        result = calculateText(args.text, ticketsDict, args.column)

    if args.nums > 0 and result is not None:
        showResult(result, args.nums)
