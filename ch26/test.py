import os
import shutil
import sys

import requests

import test_utils


class Ch26Tests(test_utils.TestCase):
    dirname = 'ch26'

    def setUp(self):
        super().setUp()
        self.setUpCGI()
        self.create_test_database()

    def tearDown(self):
        super().tearDown()
        self.tearDownCGI()
        self.delete_test_database()

    def create_test_database(self):
        database = self.src_dir / 'messages.db'
        backup_database = self.src_dir / 'messages.db.bak'
        if database.exists():
            shutil.copy(database, backup_database)
        self.run_script('execute_sql.py', 'messages.db create_table_sqlite.sql')
        self.run_script('execute_sql.py', 'messages.db testdata/messages.sql')

    def delete_test_database(self):
        database = self.src_dir / 'messages.db'
        backup_database = self.src_dir / 'messages.db.bak'
        os.remove(database)
        if backup_database.exists():
            shutil.move(backup_database, database)

    def test_1st_impl(self):
        def run_cgi_scripts():
            url = 'http://localhost:8000/cgi-bin/simple_main' + self.cgi_suffix
            return requests.get(url).text

        _, _, result = self.run_server_cmd(
            f'{sys.executable} -m http.server --cgi'.split(), wait_time=2, client_func=run_cgi_scripts)
        self.assertIn('Re: Mr. Gumby is in town', result)
        self.assertIn('Earn $$$ in no time!!!', result)

    def test_2nd_impl(self):
        base_url = 'http://localhost:8000/cgi-bin'

        def main():
            url = f'{base_url}/main{self.cgi_suffix}'
            return requests.get(url).text

        def view(id):
            url = f'{base_url}/view{self.cgi_suffix}?id={id}'
            return requests.get(url).text

        def edit(reply_to):
            url = f'{base_url}/edit{self.cgi_suffix}'
            if reply_to is not None:
                url += f'?reply_to={reply_to}'
            return requests.get(url).text

        def save(reply_to, sender, subject, text):
            url = f'{base_url}/save{self.cgi_suffix}'
            data = {'sender': sender, 'subject': subject, 'text': text}
            if reply_to is not None:
                data['reply_to'] = reply_to
            return requests.post(url, data).text

        def run_cgi_scripts():
            return [
                main(), view(2), edit(1),
                save(None, 'Alice', 'Hello!', "Hello, I'm Alice."),
                save(5, 'Bob', 'Re: Mr. Gumby has left the building', 'Goodbye, Mr. Gumby!'),
                main()
            ]

        _, _, result = self.run_server_cmd(
            f'{sys.executable} -m http.server --cgi'.split(), wait_time=2, client_func=run_cgi_scripts)
        self.assertIn('Mr. Gumby is in town', result[0])
        self.assertIn('Yes, the rumors are true. I have arrived.', result[1])
        self.assertIn('Re: Anyone here?', result[2])
        self.assertIn('Message Saved', result[3])
        self.assertIn('Message Saved', result[4])
        self.assertIn('Hello!', result[5])
        self.assertIn('Re: Mr. Gumby has left the building', result[5])
