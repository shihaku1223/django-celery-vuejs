#!env python3

import argparse
import tensorflow
import tensorflow_hub as hub

import numpy

from mantis_soap.Connector import Connector

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--id', type=int,
        help='Mantis Id')

    parser.add_argument('--user', type=str, required=True,
        help='Mantis User')

    parser.add_argument('--password', type=str, required=True,
        help='Mantis Password')

    args = parser.parse_args()

    url = "http://osoft-de-c.olympus.co.jp/mantis/ipf3/app/api/soap/mantisconnect.php?wsdl"
    mantisConnector = Connector(url, args.user, args.password)

    print('loading hub')
    embed = hub.load(
        "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

    if args.id is not None:
        issue = mantisConnector.getIssue(args.id)
