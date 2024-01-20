import pathlib

import test_utils
from ch06.parameter_practice import *
from ch06.simple_contacts import *


class Ch06Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_simple_contacts(self):
        names = {}
        init(names)
        self.assertEqual({'first': {}, 'middle': {}, 'last': {}}, names)

        store(names, 'Magnus Lie Hetland')
        self.assertEqual(['Magnus Lie Hetland'], lookup(names, 'middle', 'Lie'))

        store(names, 'Anne Lie Hetland')
        self.assertEqual(['Anne Lie Hetland'], lookup(names, 'first', 'Anne'))
        self.assertEqual(['Magnus Lie Hetland', 'Anne Lie Hetland'], lookup(names, 'middle', 'Lie'))

        store(names, 'Robin Hood')
        store(names, 'Robin Locksley')
        self.assertEqual(['Robin Hood', 'Robin Locksley'], lookup(names, 'first', 'Robin'))

        store(names, 'Mr. Gumby')
        self.assertEqual(['Robin Hood', 'Robin Locksley', 'Mr. Gumby'], lookup(names, 'middle', ''))

    def test_parameter_practice_story(self):
        self.assertEqual('Once upon a time, there was a king called Gumby.', story(job='king', name='Gumby'))
        self.assertEqual(
            'Once upon a time, there was a brave knight called Sir Robin.',
            story(name='Sir Robin', job='brave knight'))

        params = {'job': 'language', 'name': 'Python'}
        self.assertEqual('Once upon a time, there was a language called Python.', story(**params))

        del params['job']
        self.assertEqual(
            'Once upon a time, there was a stroke of genius called Python.',
            story(job='stroke of genius', **params))

    def test_parameter_practice_power(self):
        self.assertEqual(8, power(2, 3))
        self.assertEqual(9, power(3, 2))
        self.assertEqual(8, power(y=3, x=2))

        params = (5,) * 2
        self.assertEqual(3125, power(*params))

        self.assertEqual(27, power(3, 3, 'Hello, world'))

    def test_parameter_practice_interval(self):
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], interval(10))
        self.assertEqual([1, 2, 3, 4], interval(1, 5))
        self.assertEqual([3, 7, 11], interval(3, 12, 4))
        self.assertEqual(81, power(*interval(3, 7)))

    def test_factorial(self):
        from ch06.factorial import factorial
        test_cases = [
            (1, 1), (2, 2), (3, 6), (5, 120), (9, 362880),
            (12, 479001600), (20, 2432902008176640000)
        ]
        for n, fact in test_cases:
            self.assertEqual(fact, factorial(n))

    def test_power(self):
        from ch06.power import power
        test_cases = [
            (0, 0, 1), (1, 100, 1), (-1, 3, -1), (2, 0, 1), (2, 3, 8), (3, 2, 9), (-5, 5, -3125),
            (2, 32, 4294967296), (2, 100, 1267650600228229401496703205376), (3.14, 25, 2649971491658.3813),
            (-123, 45, -11110408185131956285910790587176451918559153212268021823629073199866111001242743283966127048043)
        ]
        for x, n, p in test_cases:
            self.assertEqual(p, power(x, n))

    def test_binary_search(self):
        from ch06.binary_search import search
        a = [4, 8, 34, 67, 95, 100, 123]
        b = [1, 1, 2, 3, 3, 3, 4, 4, 5]
        keywords = [
            'False', 'None', 'True',
            'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del',
            'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
        ]
        test_cases = [
            (a, 34, 2), (a, 100, 5), (a, 1, None), (a, 4, 0), (a, 123, 6), (a, 999, None),
            (b, 1, 0), (b, 2, 2), (b, 3, 3), (b, 4, 6), (b, 5, 8),
            (keywords, 'def', 11), (keywords, 'return', 30), (keywords, 'False', 0), (keywords, 'int', None)
        ]
        for seq, num, index in test_cases:
            if index is None:
                self.assertRaises(AssertionError, search, seq, num)
            else:
                self.assertEqual(index, search(seq, num))
