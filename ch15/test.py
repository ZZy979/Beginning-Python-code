from concurrent.futures import ThreadPoolExecutor

import requests

import test_utils


class Ch15Tests(test_utils.TestCase):
    dirname = 'ch15'

    def setUp(self):
        super().setUp()
        self.setUpCGI()

    def tearDown(self):
        super().tearDown()
        self.tearDownCGI()

    def _test_python_jobs_crawler(self, script):
        from unittest.mock import patch

        with open(self.testdata_dir / 'python_jobs.html', encoding='utf-8') as page, \
                patch('requests.get', **{'return_value.text': page.read()}):
            self.assertScriptOutput(
                script, subproc=False, output_file=self.testdata_dir / 'python_jobs_crawler_output.txt')

    def test_scrape_python_jobs(self):
        self._test_python_jobs_crawler('scrape_python_jobs.py')

    def test_scrape_python_jobs_html_parser(self):
        self._test_python_jobs_crawler('scrape_python_jobs_html_parser.py')

    def test_scrape_python_jobs_bs(self):
        self._test_python_jobs_crawler('scrape_python_jobs_bs.py')

    def test_cgi_scripts(self):
        import platform, unittest

        if platform.system() == 'Darwin':
            raise unittest.SkipTest('macOS: Connection reset by peer')  # TODO solve this

        def _run_cgi_scripts():
            test_cases = [
                ('simple1', 'simple1', None),
                ('faulty', 'faulty', None),
                ('simple2_1', 'simple2', None),
                ('simple2_2', 'simple2', {'name': 'Gumby', 'age': '42'}),
                ('simple3_1', 'simple3', None),
                ('simple3_2', 'simple3', {'name': 'Mr. Gumby'}),
            ]
            base_url = 'http://localhost:8000/cgi-bin'
            with ThreadPoolExecutor() as executor:
                client_futures = {
                    name: executor.submit(requests.get, f'{base_url}/{cgi_script}{self.cgi_suffix}', params)
                    for name, cgi_script, params in test_cases
                }
                return {name: f.result().text for name, f in client_futures.items()}

        _, _, result = self.run_server_script('cgi_server.py', wait_time=2, client_func=_run_cgi_scripts)
        self.assertIn('Hello, world!', result['simple1'])
        self.assertIn('ZeroDivisionError', result['faulty'])
        self.assertIn('Hello, world!', result['simple2_1'])
        self.assertIn('Hello, Gumby!', result['simple2_2'])
        self.assertIn('Hello, world!', result['simple3_1'])
        self.assertIn('Hello, Mr. Gumby!', result['simple3_2'])

    def test_powers(self):
        def _clients():
            test_cases = [3, 10, 1, 0, -1, 'abc', '']
            base_url = 'http://localhost:5000/powers'
            with ThreadPoolExecutor() as executor:
                client_futures = {n: executor.submit(requests.get, f'{base_url}/{n}') for n in test_cases}
                return {n: f.result().text for n, f in client_futures.items()}

        _, _, results = self.run_server_cmd('flask --app powers run'.split(), client_func=_clients)
        self.assertEqual('1, 2, 4', results[3])
        self.assertEqual('1, 2, 4, 8, 16, 32, 64, 128, 256, 512', results[10])
        self.assertEqual('1', results[1])
        self.assertFalse(results[0])
        self.assertIn('Not Found', results[-1])
        self.assertIn('Not Found', results['abc'])
        self.assertIn('Not Found', results[''])
