import pathlib
import shlex
import subprocess
import sys
import unittest


class TestCase(unittest.TestCase):
    dirname = ''

    def setUp(self):
        self.root_dir = pathlib.Path(__file__).resolve().parent
        self.dir = self.root_dir / self.dirname

    def run_script(self, script, args='', input=None, input_file=None, cwd=None):
        """运行指定的脚本，返回subprocess.CompletedProcess对象。

        :param script: str 脚本文件名，相对于cwd参数指定的目录
        :param args: str 命令行参数，空格分隔
        :param input: str 输入文本
        :param input_file: str 输入文件名，如果未指定input参数则从该文件读取输入，如果该参数也未指定则没有输入
        :param cwd: str 当前工作目录，默认为self.dir
        :return: subprocess.CompletedProcess对象
        """
        stdin = _prepare_stdin(input, input_file)
        cmd = [sys.executable, script, *shlex.split(args)]
        result = subprocess.run(
            cmd, stdin=stdin, input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=self.get_cwd(cwd), encoding='utf-8', text=True)
        if input_file:
            stdin.close()

        return result

    def assertScriptOutput(
            self, script, args='', input=None, input_file=None,
            prompt=None, output=None, output_file=None, cwd=None):
        """运行指定的脚本，并比较标准输出。

        :param script: str 脚本文件名，相对于cwd参数指定的目录
        :param args: str 命令行参数，空格分隔
        :param input: str 输入文本
        :param input_file: str 输入文件名，如果未指定input参数则从该文件读取输入，如果该参数也未指定则没有输入
        :param prompt: str 输入提示文本，如果指定了output参数则将其拼接到output开头
        :param output: str 期望输出文本
        :param output_file: str 期望输出文件名，如果未指定output参数则与该文件比较输出，如果该参数也未指定则期望无输出
        :param cwd: str 当前工作目录，默认为self.dir
        """
        expected_output = _prepare_expected_output(prompt, output, output_file)
        actual_output = self.run_script(script, args, input, input_file, cwd).stdout
        self.assertEqual(expected_output, actual_output)

    def get_cwd(self, cwd=None):
        return cwd if cwd is not None else self.dir


def _prepare_stdin(input, input_file):
    if input is not None:
        return None
    elif input_file:
        return open(input_file, encoding='utf-8')
    else:
        return subprocess.DEVNULL


def _prepare_expected_output(prompt, output, output_file):
    if output is not None:
        return (prompt or '') + output
    elif output_file:
        with open(output_file, encoding='utf-8') as f:
            return f.read()
    else:
        return ''
