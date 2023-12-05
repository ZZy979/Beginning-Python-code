import pathlib

import test_utils


class Ch01Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_hello(self):
        self.assertScriptOutput('hello.py', output='Hello, world!\n')

    def test_whats_your_name(self):
        self.assertScriptOutput(
            'whats_your_name.py', input='Gumby', output='What is your name? Hello, Gumby!\n'
        )
