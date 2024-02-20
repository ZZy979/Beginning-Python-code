import pathlib

import test_utils


class Ch08Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_exception_example(self):
        prompt = 'Enter the first number: Enter the second number: '
        test_cases = [
            ('5\n2', '2.5\n'),
            ('10\n0', "The second number can't be zero!\n"),
        ]
        for input, output in test_cases:
            self.assertScriptOutput('exception_example.py', input=input, prompt=prompt, output=output)

    def test_muffled_calculator(self):
        from ch08.muffled_calculator import MuffledCalculator
        calculator = MuffledCalculator()
        self.assertEqual(5.0, calculator.calc('10 / 2'))
        self.assertRaises(ZeroDivisionError, calculator.calc, '10 / 0')
        calculator.muffled = True
        self.assertIsNone(calculator.calc('10 / 0'))

    def test_except_clause_example(self):
        prompt1 = 'Enter the first number: '
        prompt2 = 'Enter the second number: '
        test_cases = [
            ('5\n2', prompt1 + prompt2, '2.5\n'),
            ('10\n0', prompt1 + prompt2, "The second number can't be zero!\n"),
            ('8\nHello', prompt1 + prompt2, "That wasn't a number, was it?\n"),
            ('@#$\n123', prompt1, "That wasn't a number, was it?\n"),
        ]
        for input, prompt, output in test_cases:
            self.assertScriptOutput('except_clause_example.py', input=input, prompt=prompt, output=output)

    def test_try_else_clause_example(self):
        input = "1\n0\n'x'\n'y'\nquuux\n2\n10\n2"
        prompt = 'Enter the first number: Enter the second number: '
        output = prompt + 'Invalid input: division by zero\nPlease try again.\n' \
            + prompt + "Invalid input: unsupported operand type(s) for /: 'str' and 'str'\nPlease try again.\n" \
            + prompt + "Invalid input: name 'quuux' is not defined\nPlease try again.\n" \
            + prompt + '5.0\n'
        self.assertScriptOutput('try_else_clause_example.py', input=input, output=output)
