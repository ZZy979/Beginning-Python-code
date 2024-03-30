import test_utils


class Ch05Tests(test_utils.TestCase):
    dirname = 'ch05'

    def test_if_statement_example(self):
        prompt = 'What is your name? '
        test_cases = [
            ('Edward Gumby', 'Hello, Mr. Gumby\n'),
            ('John Gumby', 'Hello, Mr. Gumby\n'),
            ('Mr. Gumby', 'Hello, Mr. Gumby\n'),
            ('Mrs. Gumby', 'Hello, Mr. Gumby\n'),
            ('Gumby', 'Hello, Mr. Gumby\n'),
            ('gumby', ''),
            ('Gumby.', ''),
            ('John Smith', ''),
        ]
        for input, output in test_cases:
            self.assertScriptOutput('if_statement_example.py', input=input, prompt=prompt, output=output)

    def test_else_clause_example(self):
        prompt = 'What is your name? '
        test_cases = [
            ('Edward Gumby', 'Hello, Mr. Gumby\n'),
            ('John Gumby', 'Hello, Mr. Gumby\n'),
            ('Mr. Gumby', 'Hello, Mr. Gumby\n'),
            ('Mrs. Gumby', 'Hello, Mr. Gumby\n'),
            ('Gumby', 'Hello, Mr. Gumby\n'),
            ('gumby', 'Hello, stranger\n'),
            ('Gumby.', 'Hello, stranger\n'),
            ('John Smith', 'Hello, stranger\n'),
        ]
        for input, output in test_cases:
            self.assertScriptOutput('else_clause_example.py', input=input, prompt=prompt, output=output)

    def test_elif_clause_example(self):
        prompt = 'Enter a number: '
        test_cases = [
            ('42', 'The number is positive\n'),
            ('-88', 'The number is negative\n'),
            ('0', 'The number is zero\n')
        ]
        for input, output in test_cases:
            self.assertScriptOutput('elif_clause_example.py', input=input, prompt=prompt, output=output)

    def test_nested_blocks_example(self):
        prompt = 'What is your name? '
        test_cases = [
            ('Edward Gumby', 'Hello, Gumby\n'),
            ('John Gumby', 'Hello, Gumby\n'),
            ('Mr. Gumby', 'Hello, Mr. Gumby\n'),
            ('Mrs. Gumby', 'Hello, Mrs. Gumby\n'),
            ('Gumby', 'Hello, Gumby\n'),
            ('gumby', 'Hello, stranger\n'),
            ('Gumby.', 'Hello, stranger\n'),
            ('John Smith', 'Hello, stranger\n'),
        ]
        for input, output in test_cases:
            self.assertScriptOutput('nested_blocks_example.py', input=input, prompt=prompt, output=output)

    def test_while_statement_example(self):
        script = 'while_statement_example.py'
        prompt = 'Please enter your name: '
        test_cases = [
            ('Alice', 1, 'Hello, Alice!\n', None),
            ('\n  \n\t\nBob', 4, 'Hello, Bob!\n', None),
            ('', 1, '', 'EOFError'),
            ('\n\n', 3, '', 'EOFError'),
        ]
        for input, n, output, error in test_cases:
            result = self.run_script(script, input=input)
            self.assertEqual(prompt * n + output, result.stdout)
            if error:
                self.assertIn(error, result.stderr)

    def test_break_statement_example(self):
        self.assertScriptOutput('break_statement_example.py', output='81\n')

    def test_while_true_break_idiom_example(self):
        prompt = 'Please enter a word: '
        test_cases = [
            ('first\nsecond', ['first', 'second']),
            ('example', ['example']),
            (' foo \nbar\n\nbaz', [' foo ', 'bar']),
            ('\nfoo', []),
        ]
        for input, words in test_cases:
            output = prompt + ''.join(f'The word was {word}\n{prompt}' for word in words)
            self.assertScriptOutput('while_true_break_idiom_example.py', input=input, output=output)

    def test_else_clause_in_loop_example(self):
        self.assertScriptOutput('else_clause_in_loop_example.py', output="Didn't find it!\n")
