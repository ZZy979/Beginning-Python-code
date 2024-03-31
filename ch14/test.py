import platform
import unittest
from concurrent.futures import ThreadPoolExecutor

import test_utils


class Ch14Tests(test_utils.TestCase):
    dirname = 'ch14'

    def _test_socket_server(self, server_script):
        with self.popen(server_script) as server_proc:
            with ThreadPoolExecutor() as executor:
                client_futures = [executor.submit(self.run_script, 'minimal_client.py') for _ in range(5)]
                client_results = [f.result() for f in client_futures]
            server_proc.kill()
            stderr = server_proc.stderr.read()
            stdout = server_proc.stdout.read()

        self.assertFalse(stderr)
        self.assertEqual(len(client_results), stdout.count('Got connection from'))
        for r in client_results:
            self.assertEqual('Thank you for connecting\n', r.stdout)

    def test_minimal_server(self):
        self._test_socket_server('minimal_server.py')

    def test_socketserver_minimal_server(self):
        self._test_socket_server('socketserver_minimal_server.py')

    @unittest.skipIf(platform.system() == 'Windows', "forking doesn't work on Windows")
    def test_forking_server(self):
        self._test_socket_server('forking_server.py')

    def test_threading_server(self):
        self._test_socket_server('threading_server.py')

    def _test_logger_server(self, server_script):
        data = [f'client{i}\n' for i in range(5)]
        with self.popen(server_script) as server_proc:
            with ThreadPoolExecutor() as executor:
                for d in data:
                    executor.submit(self.run_script, 'telnet_client.py', input=d)
            server_proc.kill()
            stderr = server_proc.stderr.read()
            stdout = server_proc.stdout.read()

        self.assertFalse('', stderr)
        self.assertEqual(len(data), stdout.count('Got connection from'))
        self.assertEqual(len(data), stdout.count('disconnected'))
        for d in data:
            self.assertIn(d, stdout)

    def test_select_server(self):
        self._test_logger_server('select_server.py')

    @unittest.skipIf(platform.system() == 'Windows', "poll doesn't work in Windows")
    def test_poll_server(self):
        self._test_logger_server('poll_server.py')

    def test_twisted_server(self):
        self._test_logger_server('twisted_server.py')

    def test_twisted_line_server(self):
        self._test_logger_server('twisted_line_server.py')
