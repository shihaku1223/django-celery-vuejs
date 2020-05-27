#!env python3

import tensorflow_hub as hub
import tensorflow_text
import collections

import argparse
import numpy

from mantis_soap.Connector import Connector
import csv
import sys

def cos_sim(v1, v2):
    return numpy.dot(v1, v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))


def calculate(texts: list, idList: list, ticketsDict: dict, column: str):
    resultDict = {}

    embed = hub.load(
        "http://10.121.88.5:9000/universal-sentence-encoder-multilingual_3.tar.gz")

    # put the text of specified ticket
    for __id, ticket in ticketsDict.items():
        if __id != idList[0]:
            texts.append(ticket[column])
            idList.append(__id)

    result = embed(texts)

    # calculate the cos
    length = len(texts)
    i = 0
    while i < length:
        resultDict[idList[i]] = cos_sim(result[0], result[i])
        i = i + 1

    sorted_result = collections.OrderedDict(sorted(
        resultDict.items(), key=lambda x: x[1], reverse=True))

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

def calculateByTicketIdwithProject(_id: int, issue, issues: list, column: str):

    texts = [issue[column]]
    idList = [_id]

    ticketsDict = {}
    for issue in issues:
        ticketsDict[issue['id']] = issue

    return calculate(texts, idList,
        ticketsDict, column)

def calculateByTextwithProject(text: str, issues: list, column: str):

    texts = [text]
    idList = [-1]

    ticketsDict = {}
    for issue in issues:
        ticketsDict[issue['id']] = issue

    return calculate(texts, idList,
        ticketsDict, column)

def showResult(result, numbers: int):

    mantisURL='http://10.156.2.84/mantis/ipf3/app/view.php?id={}'
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
                  ' score {}'.format(result[key]))
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

    parser.add_argument('--csvs', type=str, action='append',
        help='Mantis csv')

    parser.add_argument('--column', type=str, default='要約',
        help='specify the column of csv file to calculate')

    parser.add_argument('--nums', type=int, default=130,
        help='the number of result to show')

    args = parser.parse_args()

    if args.project is not None:
        url = "http://osoft-de-c.olympus.co.jp/mantis/ipf3/app/api/soap/mantisconnect.php?wsdl"
        mantisConnector = Connector(url, args.user, args.password)
        mantisConnector.connect()

        projectId = mantisConnector.getProjectId(args.project)
        issues = mantisConnector.getProjectIssues(projectId)
        #issues = mantisConnector.getIssuesByFilter(projectId, 11092, 0, 0)

        if args.id is not None:
            issue = mantisConnector.getIssue(args.id)
            result = calculateByTicketIdwithProject(
                args.id, issue, issues, args.column)
        elif args.text is not None:
            result = calculateByTextwithProject(
                args.text, issues, args.column)

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
