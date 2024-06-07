import filecmp
import os
import shutil

import test_utils


class Ch22Tests(test_utils.TestCase):
    dirname = 'ch22'

    def test_test_handler(self):
        self.assertScriptOutput('test_handler.py', output_file=self.testdata_dir / 'test_handler_output.txt')

    def test_headline_handler(self):
        self.assertScriptOutput('headline_handler.py', output_file=self.testdata_dir / 'headline_handler_output.txt')

    def test_1st_impl(self):
        html_files = ['index.html', 'shouting.html', 'sleeping.html', 'eating.html']
        self.run_script('pagemaker.py')
        for f in html_files:
            output_file = self.src_dir / f
            expected_file = self.testdata_dir / 'v1' / f
            self.assertTrue(output_file.exists())
            self.assertTrue(filecmp.cmp(expected_file, output_file))
            os.remove(output_file)

    def test_2nd_impl(self):
        base_dir = 'public_html'
        html_files = ['index.html', 'interests/shouting.html', 'interests/sleeping.html', 'interests/eating.html']
        self.run_script('website.py')
        for f in html_files:
            output_file = self.src_dir / base_dir / f
            expected_file = self.testdata_dir / 'v2' / base_dir / f
            self.assertTrue(output_file.exists())
            self.assertTrue(filecmp.cmp(expected_file, output_file))
        shutil.rmtree(self.src_dir / base_dir)
