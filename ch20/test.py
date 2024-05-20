import test_utils


class Ch20Tests(test_utils.TestCase):
    dirname = 'ch20'

    def test_1st_impl(self):
        self.assertScriptOutput(
            'simple_markup.py', input_file=self.src_dir / 'test_input.txt',
            output_file=self.src_dir / 'test_output.html')

    def test_2nd_impl(self):
        self.assertScriptOutput(
            'markup.py', input_file=self.src_dir / 'test_input.txt',
            output_file=self.src_dir / 'test_output2.html')
