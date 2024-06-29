import os
import shutil
import sys

import requests

import test_utils


class Ch25Tests(test_utils.TestCase):
    dirname = 'ch25'

    @property
    def data_dir(self):
        return self.src_dir / 'data'

    def setUp(self):
        super().setUp()
        self.setUpCGI()
        shutil.copy(self.src_dir / 'simple_edit.dat', self.src_dir / 'simple_edit.dat.bak')
        shutil.copy(self.data_dir / 'foofile.txt', self.data_dir / 'foofile.txt.bak')

    def tearDown(self):
        super().tearDown()
        self.tearDownCGI()
        shutil.move(self.src_dir / 'simple_edit.dat.bak', self.src_dir / 'simple_edit.dat')
        shutil.move(self.data_dir / 'foofile.txt.bak', self.data_dir / 'foofile.txt')

    def test_1st_impl(self):
        url = 'http://localhost:8000/cgi-bin/simple_edit' + self.cgi_suffix
        new_text = 'Hello, world!\nRemote Editing with CGI\n'

        def get_file():
            return requests.get(url).text

        def edit_file():
            return requests.post(url, {'text': new_text}).text

        def run_cgi_scripts():
            return [get_file(), edit_file()]

        _, _, result = self.run_server_cmd(
            f'{sys.executable} -m http.server --cgi'.split(), wait_time=2, client_func=run_cgi_scripts)
        self.assertIn('Nickety, nockety, noo, noo, noo...', result[0])
        self.assertIn(new_text.replace('\n', os.linesep), result[1])
        with open(self.src_dir / 'simple_edit.dat') as f:
            self.assertEqual(new_text, f.read())

    def test_2nd_impl(self):
        base_url = 'http://localhost:8000/cgi-bin'
        new_text = 'Hello, world!\nRemote Editing with CGI\n'

        def edit():
            url = f'{base_url}/edit{self.cgi_suffix}'
            return requests.post(url, {'filename': 'foofile.txt'}).text

        def save():
            url = f'{base_url}/save{self.cgi_suffix}'
            return requests.post(url, {'filename': 'foofile.txt', 'password': 'foobar', 'text': new_text}).text

        def run_cgi_scripts():
            return [edit(), save()]

        _, _, result = self.run_server_cmd(
            f'{sys.executable} -m http.server --cgi'.split(), wait_time=2, client_func=run_cgi_scripts)
        self.assertIn('Nickety, nockety, noo, noo, noo...', result[0])
        self.assertEqual('The file has been saved.', result[1].strip())
        with open(self.data_dir / 'foofile.txt') as f:
            self.assertEqual(new_text, f.read())
