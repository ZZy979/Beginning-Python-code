import test_utils


class Ch01Tests(test_utils.TestCase):
    dirname = 'ch01'

    def test_hello(self):
        self.assertScriptOutput('hello.py', output='Hello, world!\n')

    def test_whats_your_name(self):
        self.assertScriptOutput(
            'whats_your_name.py', input='Gumby',
            prompt='What is your name? ', output='Hello, Gumby!\n'
        )
