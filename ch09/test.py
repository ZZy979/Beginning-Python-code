import test_utils


class Ch09Tests(test_utils.TestCase):
    dirname = 'ch09'

    def test_arithseq(self):
        from ch09.arithseq import ArithmeticSequence
        s = ArithmeticSequence(1, 2)
        self.assertEqual(9, s[4])
        s[4] = 2
        self.assertEqual(2, s[4])
        self.assertEqual(11, s[5])
        with self.assertRaises(AttributeError):
            del s[4]
        self.assertRaises(TypeError, lambda: s['four'])
        self.assertRaises(IndexError, lambda: s[-42])

    def test_counter_list(self):
        from ch09.counter_list import CounterList
        cl = CounterList(range(10))
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], cl)
        cl.reverse()
        self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], cl)
        del cl[3:6]
        self.assertEqual([9, 8, 7, 3, 2, 1, 0], cl)
        self.assertEqual(0, cl.counter)
        self.assertEqual(9, cl[4] + cl[2])
        self.assertEqual(2, cl.counter)

    def test_rectangle_property(self):
        from ch09.rectangle_property import Rectangle
        r = Rectangle()
        r.width = 10
        r.height = 5
        self.assertEqual((10, 5), r.size)
        r.size = 150, 100
        self.assertEqual(150, r.width)

    def test_rectangle_getattr(self):
        from ch09.rectangle_getattr import Rectangle
        r = Rectangle()
        r.width = 10
        r.height = 5
        self.assertEqual((10, 5), r.size)
        r.size = 150, 100
        self.assertEqual(150, r.width)
        self.assertRaises(AttributeError, lambda: r.area)

    def test_fibonacci_iterator(self):
        from ch09.fibonacci_iterator import Fibs
        fibs = Fibs()
        for f in fibs:
            if f > 1000:
                break
        self.assertEqual(1597, f)

    def test_test_iterator(self):
        from ch09.test_iterator import TestIterator
        ti = TestIterator()
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], list(ti))

    def test_flatten(self):
        from ch09.flatten import flatten
        test_cases = [
            ([[[1], 2], 3, 4, [5, [6, 7]], 8], [1, 2, 3, 4, 5, 6, 7, 8]),
            (['foo', ['bar', ['baz']]], ['foo', 'bar', 'baz']),
        ]
        for nested, expected in test_cases:
            self.assertEqual(expected, list(flatten(nested)))

    def test_non_generator_flatten(self):
        from ch09.non_generator_flatten import flatten
        test_cases = [
            ([[[1], 2], 3, 4, [5, [6, 7]], 8], [1, 2, 3, 4, 5, 6, 7, 8]),
            (['foo', ['bar', ['baz']]], ['foo', 'bar', 'baz']),
        ]
        for nested, expected in test_cases:
            self.assertEqual(expected, list(flatten(nested)))

    def test_queens(self):
        from ch09.queens import queens
        self.assertEqual([], list(queens(3)))
        self.assertEqual([(1, 3, 0, 2), (2, 0, 3, 1)], list(queens(4)))
        self.assertEqual(92, len(list(queens(8))))
