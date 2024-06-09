import filecmp
import json
import os
import pathlib
from nntplib import ArticleInfo
from unittest.mock import Mock, patch

import test_utils


class Ch23Tests(test_utils.TestCase):
    dirname = 'ch23'

    def setUp(self):
        super().setUp()
        self.setup_nntp_mock()
        self.setup_web_mock()

    def setup_nntp_mock(self):
        with open(self.testdata_dir / 'nntp_response.json') as f:
            d = json.load(f)
        self.mock_nntp = Mock(name='NNTP')
        mock_server = self.mock_nntp.return_value
        mock_server.group.return_value = [d['group'][key] for key in ('response', 'count', 'first', 'last', 'name')]
        mock_server.over.return_value = [d['over'][key] for key in ('response', 'overviews')]

        head, body = {}, {}
        for id, ad in d['article'].items():
            id = int(id)
            info = ad['info']
            sep_index = ad['info']['lines'].index('')
            head_lines = [line.encode() for line in info['lines'][:sep_index]]
            body_lines = [line.encode() for line in info['lines'][sep_index + 1:]]
            head[id] = (ad['response'], ArticleInfo(number=info['number'], message_id=info['message_id'], lines=head_lines))
            body[id] = (ad['response'], ArticleInfo(number=info['number'], message_id=info['message_id'], lines=body_lines))
        mock_server.head.side_effect = head.__getitem__
        mock_server.body.side_effect = body.__getitem__

    def setup_web_mock(self):
        self.mock_urlopen = Mock(name='urlopen')
        self.mock_urlopen.side_effect = lambda _: open(self.testdata_dir / 'nbc_news.html', 'rb')

    def test_1st_impl(self):
        with patch('nntplib.NNTP', self.mock_nntp):
            with open(self.testdata_dir / 'newsagent1_output.txt', encoding='utf-8') as f:
                expected_output = f.read()
            actual_output = self.run_script('newsagent1.py', subproc=False).stdout
            self.assertEqual(expected_output, actual_output)

            self.mock_nntp.assert_called_once_with('freenews.netfront.net')
            mock_server = self.mock_nntp.return_value
            mock_server.group.assert_called_once_with('comp.lang.python.announce')
            mock_server.over.assert_called_once_with((683, 692))
            self.assertEqual(10, mock_server.head.call_count)
            self.assertEqual(10, mock_server.body.call_count)

    def test_2nd_impl(self):
        with patch('nntplib.NNTP', self.mock_nntp), patch('urllib.request.urlopen', self.mock_urlopen):
            with open(self.testdata_dir / 'newsagent2_output.txt', encoding='utf-8') as f:
                expected_output = f.read()
            actual_output = self.run_script('newsagent2.py', subproc=False).stdout
            self.assertEqual(expected_output, actual_output)

            self.mock_urlopen.assert_called_once_with('https://www.nbcnews.com/world')

            output_file = pathlib.Path.cwd() / 'news.html'
            expected_file = self.testdata_dir / 'news.html'
            self.assertTrue(output_file.exists())
            self.assertTrue(filecmp.cmp(expected_file, output_file))
            os.remove(output_file)
