import filecmp
import os
import sys
import time
from subprocess import Popen, PIPE
from xmlrpc.client import ServerProxy

import test_utils


class Ch27Tests(test_utils.TestCase):
    dirname = 'ch27'

    def test_1st_impl(self):
        from ch27.simple_node import OK, FAIL

        peer1 = Popen(
            f'{sys.executable} ../simple_node.py http://localhost:4242 files1 secret1'.split(),
            cwd=self.testdata_dir)
        peer2 = Popen(
            f'{sys.executable} ../simple_node.py http://localhost:4243 files2 secret2'.split(),
            cwd=self.testdata_dir)
        time.sleep(2)
        test_file1 = self.testdata_dir / 'files1/test.txt'
        test_file2 = self.testdata_dir / 'files2/test.txt'
        try:
            mypeer = ServerProxy('http://localhost:4242')
            code, _ = mypeer.query('test.txt')
            self.assertEqual(FAIL, code)

            otherpeer = ServerProxy('http://localhost:4243')
            code, data = otherpeer.query('test.txt')
            self.assertEqual(OK, code)
            self.assertEqual('This is a test\n', data)

            mypeer.hello('http://localhost:4243')
            code, data = mypeer.query('test.txt')
            self.assertEqual(OK, code)
            self.assertEqual('This is a test\n', data)

            code = mypeer.fetch('test.txt', 'secret1')
            self.assertEqual(OK, code)
            self.assertTrue(test_file1.exists())
            self.assertTrue(filecmp.cmp(test_file1, test_file2))
        finally:
            peer1.kill()
            peer2.kill()
            os.remove(test_file1)

    def test_2nd_impl(self):
        client1 = Popen(
            f'{sys.executable} ../client.py urls.txt files1 http://localhost:4242'.split(),
            stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testdata_dir, encoding='utf-8', text=True)
        client2 = Popen(
            f'{sys.executable} ../client.py urls.txt files2 http://localhost:4243'.split(),
            stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self.testdata_dir, encoding='utf-8', text=True)
        time.sleep(2)

        stdout, _ = client1.communicate('fetch foo.txt\nfetch test.txt\nexit\n')
        client2.communicate('exit\n')

        test_file1 = self.testdata_dir / 'files1/test.txt'
        test_file2 = self.testdata_dir / 'files2/test.txt'
        self.assertEqual("> Couldn't find the file foo.txt\n> > \n", stdout)
        self.assertTrue(test_file1.exists())
        self.assertTrue(filecmp.cmp(test_file1, test_file2))
        os.remove(test_file1)
