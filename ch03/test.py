import pathlib

import test_utils


class Ch03Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_string_formatting_example(self):
        self.assertScriptOutput(
            'string_formatting_example.py', input='35',
            output_file=self.dir / 'testdata/string_formatting_example_output.txt'
        )
