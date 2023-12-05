import shlex
import subprocess
import unittest


class TestCase(unittest.TestCase):

    def assertScriptOutput(
            self, script, args='', input=None, input_file=None,
            output=None, output_file=None, cwd=None):
        if input is not None:
            stdin = None
        elif input_file:
            stdin = open(input_file, encoding='utf-8')
        else:
            stdin = subprocess.DEVNULL

        if output is not None:
            expected_output = output
        elif output_file:
            with open(output_file, encoding='utf-8') as f:
                expected_output = f.read()
        else:
            expected_output = ''

        if cwd is None and hasattr(self, 'dir'):
            cwd = self.dir

        cmd = ['python', script, *shlex.split(args)]
        actual_output = subprocess.run(
            cmd, stdin=stdin, input=input, stdout=subprocess.PIPE,
            cwd=cwd, check=True, encoding='utf-8', text=True).stdout
        if input_file:
            stdin.close()

        self.assertEqual(expected_output, actual_output)
