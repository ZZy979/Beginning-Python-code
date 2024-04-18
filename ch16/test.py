import test_utils


class Ch16Tests(test_utils.TestCase):
    dirname = 'ch16'

    def test_area(self):
        self.assertScriptOutput('area_test.py', output='Test passed \n')

    def test_my_math(self):
        result = self.run_script('my_math.py', '-v')
        self.assertIn('Test passed.', result.stdout)
