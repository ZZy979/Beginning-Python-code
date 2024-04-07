import test_utils


class Ch11Tests(test_utils.TestCase):
    dirname = 'ch11'

    def test_wordcount(self):
        self.assertScriptOutput(
            'wordcount.py', input_file=self.testdata_dir / 'somefile.txt', output='Wordcount: 11\n')
        self.assertScriptOutput(
            'wordcount.py', input_file=self.testdata_dir / 'somefile2.txt', output='Wordcount: 12\n')
        self.assertScriptOutput('wordcount.py', output='Wordcount: 0\n')
