import subprocess


def execute(command, args = [], env = None, cwd = None):

    for arg in args:
        print('{}'.format(arg))
        command.append(arg)

    proc = subprocess.Popen(command,
        env = env, cwd = cwd,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    return { 'stdout': stdout, 'stderr': stderr, 'returncode': proc.returncode }
