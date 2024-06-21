import socket
import time
from concurrent.futures import ThreadPoolExecutor
from telnetlib import Telnet

import test_utils


class Ch24Tests(test_utils.TestCase):
    dirname = 'ch24'

    def test_minimal_chat_server(self):
        self.assertScriptOutput('minimal_chat_server.py')

    def _test_basic_chat_server(self, server_script):
        def client():
            s = socket.socket()
            s.connect(('localhost', 5005))
            s.close()

        def call_clients():
            with ThreadPoolExecutor() as executor:
                client_futures = [executor.submit(client) for _ in range(5)]
                return [f.result() for f in client_futures]

        stdout, _, _ = self.run_server_script(server_script, client_func=call_clients)
        self.assertEqual(5, stdout.count('Connection attempt from'))

    def test_chat_server_accept_connections(self):
        self._test_basic_chat_server('chat_server_accept_connections.py')

    def test_chat_server_with_cleanup(self):
        self._test_basic_chat_server('chat_server_with_cleanup.py')

    def test_chat_server_with_session(self):
        def client(msg):
            with Telnet('localhost', 5005) as tn:
                tn.write(msg.encode())
                time.sleep(0.5)

        msgs = ["I'm Alice!\r\n", "I'm Bob!\r\n"]

        def call_clients():
            with ThreadPoolExecutor() as executor:
                client_futures = [executor.submit(client, msg) for msg in msgs]
                return [f.result() for f in client_futures]

        stdout, _, _ = self.run_server_script('chat_server_with_session.py', client_func=call_clients)
        for msg in msgs:
            self.assertIn(msg.strip(), stdout)

    def test_1st_impl(self):
        def alice():
            with Telnet('localhost', 5005) as tn:
                tn.write(b"I'm Alice.\r\n")
                time.sleep(1)
                tn.write(b"Hello, Bob!\r\n")
                time.sleep(0.5)
                return tn.read_very_eager().decode()

        def bob():
            with Telnet('localhost', 5005) as tn:
                time.sleep(0.5)
                tn.write(b"Hello, Alice! I'm Bob.\r\n")
                time.sleep(1)
                return tn.read_very_eager().decode()

        def call_clients():
            with ThreadPoolExecutor() as executor:
                client_futures = [executor.submit(alice), executor.submit(bob)]
                return [f.result() for f in client_futures]

        _, _, client_results = self.run_server_script('simple_chat.py', client_func=call_clients)
        expected_output = "Welcome to TestChat\r\nI'm Alice.\r\nHello, Alice! I'm Bob.\r\nHello, Bob!\r\n"
        for r in client_results:
            self.assertEqual(expected_output, r)

    def test_2nd_impl(self):
        def magnus():
            with Telnet('localhost', 5005) as tn:
                tn.write(b'login magnus\r\n')
                time.sleep(2)
                tn.write(b'say Hi, there, dilbert.\r\n')
                time.sleep(1.5)
                tn.write(b'say Yup.\r\n')
                time.sleep(1)
                return tn.read_very_eager().decode()

        def dilbert():
            with Telnet('localhost', 5005) as tn:
                time.sleep(0.5)
                tn.write(b'login dilbert\r\n')
                time.sleep(0.5)
                tn.write(b'look\r\n')
                time.sleep(0.5)
                tn.write(b'say Hi, magnus!\r\n')
                time.sleep(1)
                tn.write(b"Nice weather we're having...\r\n")
                time.sleep(0.5)
                tn.write(b"say Nice weather we're having...\r\n")
                time.sleep(1)
                tn.write(b'logout\r\n')
                time.sleep(0.5)
                return tn.read_very_eager().decode()

        def call_clients():
            with ThreadPoolExecutor() as executor:
                client_futures = [executor.submit(magnus), executor.submit(dilbert)]
                return [f.result() for f in client_futures]

        _, _, client_results = self.run_server_script('chatserver.py', client_func=call_clients)
        expected_magnus_output = "Welcome to TestChat\r\n" \
                                 "dilbert has entered the room.\r\n" \
                                 "dilbert: Hi, magnus!\r\n" \
                                 "magnus: Hi, there, dilbert.\r\n" \
                                 "dilbert: Nice weather we're having...\r\n" \
                                 "magnus: Yup.\r\n" \
                                 "dilbert has left the room.\r\n"
        expected_dilbert_output = "Welcome to TestChat\r\n" \
                                  "The following are in this room:\r\n" \
                                  "magnus\r\n" \
                                  "dilbert\r\n" \
                                  "dilbert: Hi, magnus!\r\n" \
                                  "magnus: Hi, there, dilbert.\r\n" \
                                  "Unknown command: Nice\r\n" \
                                  "dilbert: Nice weather we're having...\r\n" \
                                  "magnus: Yup.\r\n"
        self.assertEqual(expected_magnus_output, client_results[0])
        self.assertEqual(expected_dilbert_output, client_results[1])
