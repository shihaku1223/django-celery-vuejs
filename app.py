#!env python3

import tensorflow_hub as hub
import tensorflow_text

import argparse
import numpy

from mantis_soap.Connector import Connector
import csv

def cos_sim(v1, v2):
    return numpy.dot(v1, v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))

def calculate(_id, ticketsDict, column):

    # put the text of specified ticket
    texts = [ticketsDict[_id][column]]
    idList = [_id]

    for __id, ticket in ticketsDict.items():
        if __id != _id:
            texts.append(ticket[column])
            idList.append(__id)

    result = embed(texts)

    length = len(texts)
    i = 0
    while i < length:
        print('{}, score {}'.format(idList[i],
            cos_sim(result[0], result[i])))
        i = i + 1

def readCSV(csv_list):
    ticketsDict = {}
    for fileName in csv_list:
        with open(fileName, 'r', encoding='cp932') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ticketsDict[int(row['Id'])] = row
    return ticketsDict

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--id', type=int,
        help='Mantis Id')

    parser.add_argument('--text', type=int,
        help='check the similarity with specified text')

    """
    parser.add_argument('--user', type=str, required=True,
        help='Mantis User')

    parser.add_argument('--password', type=str, required=True,
        help='Mantis Password')
    """
    parser.add_argument('--csvs', type=str, action='append',
        help='Mantis csv')

    parser.add_argument('--column', type=str, default='要約',
        help='specify the column of csv file to calculate')

    args = parser.parse_args()

    """
    url = "http://osoft-de-c.olympus.co.jp/mantis/ipf3/app/api/soap/mantisconnect.php?wsdl"
    mantisConnector = Connector(url, args.user, args.password)
    """

    print('loading hub')
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

    print('reading csv files')
    if args.csvs is not None:
        ticketsDict = readCSV(args.csvs)
    print('ticket count {}'.format(len(ticketsDict)))

    if args.id is not None:
        if args.id in ticketsDict:
            print('check the similarity with {}'.format(args.column))
            calculate(args.id, ticketsDict, args.column)
        else:
            print('Cound not find the ticket id {}'.format(args.id))
