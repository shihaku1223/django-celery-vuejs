#!env python3

import argparse
import json, zeep
from mantis_soap.Connector import Connector
from pymongo import MongoClient

host="mongodb://localhost:27017/"
username="root"
password="root"
dbname="mantis"
collection="issues"
client = MongoClient(host, username=username, password=password)

db = client[dbname]
collect = db[collection]

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--user', type=str,
        help='Mantis User')

    parser.add_argument('--password', type=str,
        help='Mantis Password')

    parser.add_argument('--project', type=str,
        help='specify the project name to search from')

    args = parser.parse_args()

    url = "http://osoft-de-c.olympus.co.jp/mantis/ipf3/app/api/soap/mantisconnect.php?wsdl"
    mantisConnector = Connector(url, args.user, args.password)
    mantisConnector.connect()

    projectId = mantisConnector.getProjectId(args.project)

    m = float('inf')
    i = 1
    while i < m:
        issues = mantisConnector.getIssuesByFilter(projectId, 11092, i, 50)

        if len(issues) == 0:
            break
        print("Issues count: {} {}".format(str(len(issues)), i),
              flush=True)

        obj = zeep.helpers.serialize_object(issues)
        try:
            ids = collect.insert_many(obj)
        except Exception as e:
            print(e)

        i = i + 1

    client.close()
