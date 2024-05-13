from setuptools import setup, Extension

setup(
    name='palindrome',
    version='1.0',
    ext_modules=[
        Extension('_palindrome', ['palindrome.c', 'palindrome.i'])
    ]
)
