import pathlib

import test_utils


class Ch10Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_hello4(self):
        self.assertScriptOutput('hello4.py', output='Hello, world!\n')

    def test_package(self):
        import sys
        sys.path.append(str(self.dir))

        import drawing
        self.assertEqual('1.0', drawing.VERSION)
        self.assertFalse(hasattr(drawing, 'colors'))
        self.assertFalse(hasattr(drawing, 'shapes'))

        import drawing.colors
        self.assertTrue(hasattr(drawing, 'colors'))
        self.assertEqual(1, drawing.colors.Color.RED)

        from drawing import shapes
        self.assertTrue(hasattr(drawing, 'shapes'))
        r = shapes.Rectangle((100, 100), 800, 600)
        r.color = drawing.colors.Color.BLUE
        r.draw()

        sys.path.pop()

    def test_reverseargs(self):
        test_cases = [
            ('this is a test', 'test a is this\n'),
            ('foobar', 'foobar\n'),
            ('', '\n')
        ]
        for args, output in test_cases:
            self.assertScriptOutput('reverseargs.py', args=args, output=output)

    def test_numberlines(self):
        import filecmp, os, shutil

        input_file = self.dir / 'numberlines.py'
        expected_file = self.dir / 'testdata/numberlines_output.txt'

        # read from file in command-line arguments
        tmp_file = self.dir / 'testdata/numberlines.py'
        shutil.copy(input_file, tmp_file)
        self.run_script('numberlines.py', args='testdata/numberlines.py')
        self.assertTrue(filecmp.cmp(expected_file, tmp_file))
        os.remove(tmp_file)

        # read from stdin
        self.assertScriptOutput('numberlines.py', input_file=input_file, output_file=expected_file)

    def test_random_time(self):
        import time

        begin, end = (2016, 1, 1, 0, 0, 0), (2017, 1, 1, 0, 0, 0)
        for _ in range(10):
            output = self.run_script('random_time.py').stdout
            t = time.strptime(output.rstrip(), '%a %b %d %X %Y')[:6]
            self.assertGreaterEqual(t, begin)
            self.assertLessEqual(t, end)

    def test_throw_dice(self):
        import re

        output_pat = re.compile(r'How many dice\? How many sides per die\? The result is (\d+)')
        test_cases = [(3, 6), (5, 6), (8, 3), (4, 10), (1, 100), (100, 1), (0, 8)]
        for n, s in test_cases:
            for _ in range(3):
                output = self.run_script('throw_dice.py', input=f'{n}\n{s}').stdout
                m = re.match(output_pat, output)
                self.assertIsNotNone(m)
                self.assertTrue(n <= int(m.group(1)) <= n * s)

    def test_random_fortune(self):
        with open(self.dir / 'testdata/fortunes.txt') as f:
            fortunes = list(f)
        for _ in range(10):
            output = self.run_script('random_fortune.py', args='testdata/fortunes.txt').stdout
            self.assertIn(output, fortunes)

    def test_deal_cards(self):
        import re

        card_pat = re.compile(r'([1-9]|10|Jack|Queen|King) of (diamonds|clubs|hearts|spades)')
        output = self.run_script('deal_cards.py', input='\n' * 52).stdout
        cards = set()
        for card in output.splitlines():
            self.assertTrue(re.fullmatch(card_pat, card))
            self.assertNotIn(card, cards)
            cards.add(card)

    def test_database(self):
        import glob, os

        test_dir = self.dir / 'testdata'
        for i in (1, 2):
            self.assertScriptOutput(
                'database.py', args='testdata/database.dat',
                input_file=test_dir / f'database_input{i}.txt',
                output_file=test_dir / f'database_output{i}.txt')

        for f in glob.glob('database.dat*', root_dir=test_dir):
            os.remove(test_dir / f)

    def test_find_sender(self):
        self.assertScriptOutput('find_sender.py', input_file=self.dir / 'testdata/message.eml', output='Foo Fie\n')

        test_cases = [
            ('From: Alice <alice@example.com>', 'Alice\n'),
            (' From: Bob <bob@example.com>', ''),
            ('from: Cindy <cindy@example.com>', ''),
            ('From: Dale Brown  <>', 'Dale Brown \n'),
            ('From: Eric <eric@example.com> ', ''),
            ('From: Foo<bar> <foo@bar.com>', 'Foo<bar>\n'),
        ]
        for input, output in test_cases:
            self.assertScriptOutput('find_sender.py', input=input, output=output)

    def test_list_email_addresses(self):
        self.assertScriptOutput(
            'list_email_addresses.py', args='testdata/message.eml',
            output_file=self.dir / 'testdata/list_email_addresses_output.txt')

    def test_templates(self):
        self.assertScriptOutput(
            'templates.py', input='The sum of 7 and 9 is [7 + 9].',
            output='The sum of 7 and 9 is 16.\n')
        self.assertScriptOutput(
            'templates.py', input='[name="Mr. Gumby"]Hello, [name]',
            output='Hello, Mr. Gumby\n')
        self.assertScriptOutput(
            'templates.py', args='testdata/simple_template.txt',
            output_file=self.dir / 'testdata/simple_template_output.txt')

        import difflib, fileinput
        expected_output = ''.join(fileinput.input(self.dir / 'testdata/email_template_output.txt'))
        output = self.run_script('templates.py', args='testdata/magnus.txt testdata/email_template.txt').stdout
        diff = list(difflib.ndiff(expected_output.splitlines(), output.splitlines()))
        self.assertTrue(all(diff[i].startswith('  ') for i in range(len(diff)) if i not in (11, 12)))
        self.assertEqual('- Fooville, Mon Jul 18 15:24:10 2016', diff[11])
