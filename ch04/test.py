import test_utils


class Ch04Tests(test_utils.TestCase):
    dirname = 'ch04'

    def test_dictionary_example(self):
        prompt = 'Name: Phone number (p) or address (a)? '
        test_cases = [
            ('Beth\np\n', "Beth's phone number is 9102.\n"),
            ('Alice\na\n', "Alice's address is Foo drive 23.\n"),
            ('Earl\np\n', '')
        ]
        for input, output in test_cases:
            self.assertScriptOutput('dictionary_example.py', input=input, prompt=prompt, output=output)

    def test_dictionary_method_example(self):
        prompt = 'Name: Phone number (p) or address (a)? '
        test_cases = [
            ('Beth\np\n', "Beth's phone number is 9102.\n"),
            ('Alice\na\n', "Alice's address is Foo drive 23.\n"),
            ('Cecil\nbirthday\n', "Cecil's birthday is not available.\n"),
            ('Earl\np\n', "Earl's phone number is not available.\n"),
            ('Gumby\nbatting average\n', "Gumby's batting average is not available.\n")
        ]
        for input, output in test_cases:
            self.assertScriptOutput('dictionary_method_example.py', input=input, prompt=prompt, output=output)
