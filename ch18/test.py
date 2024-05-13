import os
import platform
import sys
import unittest

import test_utils


class Ch18Tests(test_utils.TestCase):
    dirname = 'ch18'

    def test_setup_hello(self):
        lib_dir = self.src_dir / 'hello'
        self.run_script('setup.py', args='build', cwd=lib_dir)
        self.assertTrue((lib_dir / 'build/lib/hello.py').exists())
        self.run_script('setup.py', args='sdist', cwd=lib_dir)
        self.assertTrue((lib_dir / 'dist/Hello-1.0.tar.gz').exists())

    def test_setup_palindrome(self):
        lib_dir = self.src_dir / 'palindrome'
        self.run_script('setup.py', args='build_ext --inplace', cwd=lib_dir)
        sys.path.append(str(lib_dir))

        from _palindrome import is_palindrome
        self.assertEqual(1, is_palindrome('ipreferpi'))
        self.assertEqual(0, is_palindrome('notlob'))
        self.assertEqual(1, is_palindrome('abba'))
        sys.path.pop()
        for f in ('palindrome.py', 'palindrome_wrap.c'):
            if (p := lib_dir / f).exists():
                os.remove(p)

    def test_setup_palindrome2(self):
        lib_dir = self.src_dir / 'palindrome2'
        self.run_script('setup.py', args='build_ext --inplace', cwd=lib_dir)
        sys.path.append(str(lib_dir))

        from palindrome import is_palindrome
        self.assertEqual(0, is_palindrome('foobar'))
        self.assertEqual(1, is_palindrome('deified'))
        sys.path.pop()

    @unittest.skipUnless(platform.system() == 'Windows', 'py2exe requires Windows')
    def test_setup_py2exe(self):
        lib_dir = self.src_dir / 'hello2'
        executable = lib_dir / 'dist/hello.exe'
        self.run_script('setup.py', args='py2exe', cwd=lib_dir)
        self.assertTrue(executable.exists())
        result = self.run_cmd(executable, input='\n')
        self.assertEqual('Hello, world!\nPress <enter>', result.stdout)
