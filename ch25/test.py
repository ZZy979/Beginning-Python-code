import os
import platform
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

import test_utils


class Ch25Tests(test_utils.TestCase):
    dirname = 'ch25'

    def setUp(self):
        super().setUp()
        cgi_bin_dir = self.src_dir / 'cgi-bin'
        for script in cgi_bin_dir.glob('*.cgi'):
            script.chmod(0o755)
            if platform.system() == 'Windows':
                # Windows doesn't support .cgi suffix
                with open(script) as cgi, open(script.with_suffix('.py'), 'w') as py:
                    py.write(cgi.read().replace('.cgi', '.py'))

    def tearDown(self):
        super().tearDown()
        cgi_bin_dir = self.src_dir / 'cgi-bin'
        if platform.system() == 'Windows':
            # cleanup
            for script in cgi_bin_dir.glob('*.py'):
                os.remove(script)

    def test_1st_impl(self):
        suffix = '.py' if platform.system() == 'Windows' else '.cgi'
        url = 'http://localhost:8000/cgi-bin/simple_edit' + suffix
        new_text = 'Hello, world!\nRemote Editing with CGI\n'

        def get_file():
            return requests.get(url).text

        def edit_file():
            time.sleep(0.5)
            return requests.post(url, {'text': new_text}).text

        def run_cgi_scripts():
            with ThreadPoolExecutor() as executor:
                client_futures = [executor.submit(get_file), executor.submit(edit_file)]
                return [f.result() for f in client_futures]

        shutil.copy(self.src_dir / 'simple_edit.dat', self.src_dir / 'simple_edit.dat.bak')

        _, _, result = self.run_server_cmd(
            f'{sys.executable} -m http.server --cgi'.split(), wait_time=2, client_func=run_cgi_scripts)
        self.assertIn('Nickety, nockety, noo, noo, noo...', result[0])
        self.assertIn(new_text.replace('\n', os.linesep), result[1])
        with open(self.src_dir / 'simple_edit.dat') as f:
            self.assertEqual(new_text, f.read())

        shutil.move(self.src_dir / 'simple_edit.dat.bak', self.src_dir / 'simple_edit.dat')

    def test_2nd_impl(self):
        suffix = '.py' if platform.system() == 'Windows' else '.cgi'
        base_url = 'http://localhost:8000/cgi-bin/'
        new_text = 'Hello, world!\nRemote Editing with CGI\n'

        def edit():
            url = base_url + 'edit' + suffix
            return requests.post(url, {'filename': 'foofile.txt'}).text

        def save():
            time.sleep(0.5)
            url = base_url + 'save' + suffix
            return requests.post(url, {'filename': 'foofile.txt', 'password': 'foobar', 'text': new_text}).text

        def run_cgi_scripts():
            with ThreadPoolExecutor() as executor:
                client_futures = [executor.submit(edit), executor.submit(save)]
                return [f.result() for f in client_futures]

        data_dir = self.src_dir / 'data'
        shutil.copy(data_dir / 'foofile.txt', data_dir / 'foofile.txt.bak')

        _, _, result = self.run_server_cmd(
            f'{sys.executable} -m http.server --cgi'.split(), wait_time=2, client_func=run_cgi_scripts)
        self.assertIn('Nickety, nockety, noo, noo, noo...', result[0])
        self.assertEqual('The file has been saved.', result[1].strip())
        with open(data_dir / 'foofile.txt') as f:
            self.assertEqual(new_text, f.read())

        shutil.move(data_dir / 'foofile.txt.bak', data_dir / 'foofile.txt')
