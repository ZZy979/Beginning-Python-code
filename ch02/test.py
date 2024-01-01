import pathlib

import test_utils


class Ch02Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_indexing_example(self):
        self.assertScriptOutput(
            'indexing_example.py', input='1974\n8\n16',
            prompt='Year: Month (1-12): Day (1-31): ', output='August 16th, 1974\n'
        )

    def test_slicing_example(self):
        self.assertScriptOutput(
            'slicing_example.py', input='http://www.python.org',
            prompt='Please enter the URL: ', output='Domain name: python\n'
        )

    def test_sequence_multiplication_example(self):
        self.assertScriptOutput(
            'sequence_multiplication_example.py',
            input_file=self.dir / 'testdata/sequence_multiplication_example_input.txt',
            output_file=self.dir / 'testdata/sequence_multiplication_example_output.txt'
        )

    def test_sequence_membership_example(self):
        prompt = 'User name: PIN code: '
        test_cases = [
            ('smith\n7524\n', 'Access granted\n'),
            ('smith\n1234\n', ''),
        ]
        for input, output in test_cases:
            self.assertScriptOutput('sequence_membership_example.py', input=input, prompt=prompt, output=output)
