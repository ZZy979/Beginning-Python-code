import pathlib

import test_utils


class Ch07Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_polymorphism_example_count(self):
        from ch07.polymorphism_example import count
        self.assertEqual(1, count('abc', 'a'))
        self.assertEqual(2, count([1, 2, 'e', 'e', 4], 'e'))
        self.assertEqual(3, count(('SPAM', 'SPAM', 'eggs', 'SPAM', 'bacon'), 'SPAM'))
        self.assertEqual(0, count(range(10), 100))

    def test_polymorphism_example_add(self):
        from ch07.polymorphism_example import add
        self.assertEqual(3, add(1, 2))
        self.assertEqual('Fishlicense', add('Fish', 'license'))
        self.assertEqual([1, 2, 3, 4, 5], add([1, 2, 3], [4, 5]))
        self.assertRaises(TypeError, add, 1, 'license')

    def test_polymorphism_example_length_message(self):
        from ch07.polymorphism_example import length_message
        self.assertEqual("The length of 'Fnord' is 5", length_message('Fnord'))
        self.assertEqual('The length of [1, 2, 3] is 3', length_message([1, 2, 3]))
        self.assertRaises(TypeError, length_message, 42)

    def test_member_counter(self):
        from ch07.member_counter import MemberCounter

        m1 = MemberCounter()
        m1.init()
        self.assertEqual(1, MemberCounter.members)

        m2 = MemberCounter()
        m2.init()
        self.assertEqual(2, MemberCounter.members)

        m1.members = 'Two'
        self.assertEqual('Two', m1.members)
        self.assertEqual(2, m2.members)

    def test_filters(self):
        from ch07.filters import Filter, SPAMFilter

        f = Filter()
        f.init()
        self.assertEqual([1, 2, 3], f.filter([1, 2, 3]))

        s = SPAMFilter()
        s.init()
        self.assertEqual(['eggs', 'bacon'], s.filter(['SPAM', 'SPAM', 'SPAM', 'SPAM', 'eggs', 'bacon', 'SPAM']))
