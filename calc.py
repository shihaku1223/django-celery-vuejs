import sys

from similarityapp.similarityapp.utils import execute
from mantis_soap.Connector import Connector
from mantisconnect.project import Issue
from pathlib import Path
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', type=str,
        help='specify the project name to search from')
    args = parser.parse_args()

    url = "http://osoft-de-c.olympus.co.jp/mantis/ipf3/app/api/soap/mantisconnect.php?wsdl"
    connector = Connector(url, "ipf3-system", "iY59RsDn")
    connector.connect()

    print("Mantis SOAP MC Version:" + connector.getVersion())
    app_path = Path(Path(__file__).parent.absolute(),
        './similarityapp/similarityapp/app.py')

    projectId = connector.getProjectId(args.project)
    print(projectId)
    args = [
        '--projectId', str(projectId),
        '--mongo-host', 'mongodb://localhost:27017/',
        '--mongo-user', 'root',
        '--mongo-pass', 'root',
        '--vectors'
    ]
    result = execute(['python3', app_path], args)
    print(result['stdout'])
    print(result['stderr'])

    subprojects = connector._mc.client.service.mc_project_get_all_subprojects(
            connector._mc.user_name, connector._mc.user_passwd, projectId)
    print(subprojects)
    for _id in subprojects:
        args = [
            '--projectId', _id,
            '--mongo-host', 'mongodb://localhost:27017/',
            '--mongo-user', 'root',
            '--mongo-pass', 'root',
            '--vectors'
        ]
        result = execute(['python3', app_path], args)
        print(result['stdout'])
        print(result['stderr'])
    sys.exit(0)

