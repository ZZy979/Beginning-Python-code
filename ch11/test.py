import pathlib

import test_utils


class Ch11Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_wordcount(self):
        self.assertScriptOutput(
            'wordcount.py', input_file=self.dir / 'testdata/somefile.txt', output='Wordcount: 11\n')
        self.assertScriptOutput(
            'wordcount.py', input_file=self.dir / 'testdata/somefile2.txt', output='Wordcount: 12\n')
        self.assertScriptOutput('wordcount.py', output='Wordcount: 0\n')
