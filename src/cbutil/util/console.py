import subprocess as subproc
import sys

class Console:
    def __init__(self, *args):
        self.proc = subproc.Popen(args = args, stdin = subproc.PIPE, stdout = subproc.PIPE, shell = True, text = True)

    def execute(self, cmd, end = '\n'):
        proc = self.proc
        stdin = proc.stdin
        stdin.write(cmd+end)
        stdin.flush()
        stdout = proc.stdout
        stdout.read()

    def exit(self):
        proc = self.proc
        proc.stdin.write('exit\n')
        proc.wait()

    def kill(self):
        self.proc.kill()
