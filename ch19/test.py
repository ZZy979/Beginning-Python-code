import test_utils


class Ch19Tests(test_utils.TestCase):
    dirname = 'ch19'

    def test_config_example(self):
        self.assertScriptOutput(
            'config_example.py', input='2\n', output_file=self.testdata_dir / 'config_example_output.txt')

    def test_logging_example(self):
        import filecmp, os
        self.run_script('logging_example.py')
        expected_file = self.testdata_dir / 'logging_example_output.log'
        log_file = self.src_dir / 'mylog.log'
        self.assertTrue(filecmp.cmp(expected_file, log_file))
        os.remove(log_file)
