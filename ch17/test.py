import os
import platform
import sys
import sysconfig
import unittest
from subprocess import run

import test_utils


class Ch17Tests(test_utils.TestCase):
    dirname = 'ch17'
    make_cmd = 'make'
    makefile = ''

    @classmethod
    def setUpClass(cls):
        if cls is Ch17Tests:
            raise unittest.SkipTest('Base class')
        super().setUpClass()
        os.environ['python_include_dir'] = sysconfig.get_path('include')
        src_dir = cls.root_dir / cls.dirname
        run(f'{cls.make_cmd} -f {cls.makefile}'.split(), cwd=src_dir, check=True)
        sys.path.append(str(src_dir))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        del os.environ['python_include_dir']
        src_dir = cls.root_dir / cls.dirname
        run(f'{cls.make_cmd} -f {cls.makefile} clean'.split(), cwd=src_dir)
        sys.path.pop()

    def test_jython(self):
        os.environ['CLASSPATH'] = 'JythonTest.class'
        result = self.run_cmd('jython jython_test.py'.split())
        self.assertEqual('Hello, world!\n', result.stdout)

    def test_palindrome(self):
        from _palindrome import is_palindrome
        self.assertEqual(1, is_palindrome('ipreferpi'))
        self.assertEqual(0, is_palindrome('notlob'))
        self.assertEqual(1, is_palindrome('abba'))

    def test_palindrome2(self):
        from palindrome import is_palindrome
        self.assertEqual(0, is_palindrome('foobar'))
        self.assertEqual(1, is_palindrome('deified'))


@unittest.skipUnless(platform.system() == 'Linux', 'requires Linux')
class Ch17TestsLinux(Ch17Tests):
    makefile = 'Makefile_Linux'


@unittest.skipUnless(platform.system() == 'Darwin', 'requires macOS')
class Ch17TestsMacOS(Ch17Tests):
    makefile = 'Makefile_macOS'


class Ch17TestsWindows(Ch17Tests):
    make_cmd = 'mingw32-make'

    @classmethod
    def setUpClass(cls):
        if cls is Ch17TestsWindows:
            raise unittest.SkipTest('Base class')
        super().setUpClass()

    def test_iron_python(self):
        os.environ['IRONPYTHONPATH'] = str(self.src_dir)
        result = self.run_cmd('ipy ipy_test.py'.split())
        self.assertEqual('Hello, world!\n', result.stdout)


@unittest.skipUnless(platform.system() == 'Windows', 'requires Windows')
class Ch17TestsWindowsGcc(Ch17TestsWindows):
    makefile = 'Makefile_Windows_gcc'
