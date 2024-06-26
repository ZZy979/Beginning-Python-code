import os
import pathlib
import platform
import runpy
import shlex
import subprocess
import sys
import time
import unittest
from io import StringIO
from subprocess import PIPE, DEVNULL, CompletedProcess, Popen
from unittest.mock import patch


class TestCase(unittest.TestCase):
    root_dir = pathlib.Path(__file__).resolve().parent
    dirname = ''

    @property
    def src_dir(self):
        return self.root_dir / self.dirname

    @property
    def testdata_dir(self):
        return self.src_dir / 'testdata'

    @property
    def cgi_bin_dir(self):
        return self.src_dir / 'cgi-bin'

    @property
    def cgi_suffix(self):
        return '.py' if platform.system() == 'Windows' else '.cgi'

    @classmethod
    def setUpClass(cls):
        os.environ['PYTHONUNBUFFERED'] = '1'
        os.environ['PYTHONIOENCODING'] = 'UTF-8'

    def setUpCGI(self):
        """准备CGI脚本测试。"""
        for script in self.cgi_bin_dir.glob('*.cgi'):
            script.chmod(0o755)
            if platform.system() == 'Windows':
                # Windows doesn't support .cgi suffix
                with open(script) as cgi, open(script.with_suffix('.py'), 'w') as py:
                    py.write(cgi.read().replace('.cgi', '.py'))

    def tearDownCGI(self):
        """清理CGI脚本测试。"""
        if platform.system() == 'Windows':
            for script in self.cgi_bin_dir.glob('*.py'):
                os.remove(script)

    def assertScriptOutput(
            self, script, args='', input=None, input_file=None, subproc=True,
            prompt=None, output=None, output_file=None, cwd=None):
        """运行指定的脚本，并比较标准输出。

        :param script: str 脚本文件名
        :param args: str 命令行参数，空格分隔
        :param input: str 输入文本
        :param input_file: str 输入文件名，如果未指定input参数则从该文件读取输入，如果该参数也未指定则没有输入
        :param subproc: bool 如果为True则在子进程中运行，否则在当前进程中运行
        :param prompt: str 输入提示文本，如果指定了output参数则将其拼接到output开头
        :param output: str 期望输出文本
        :param output_file: str 期望输出文件名，如果未指定output参数则与该文件比较输出，如果该参数也未指定则期望无输出
        :param cwd: str 当前工作目录，默认为self.dir
        """
        if output is not None:
            expected_output = (prompt or '') + output
        elif output_file:
            with open(output_file, encoding='utf-8') as f:
                expected_output = f.read()
        else:
            expected_output = ''

        actual_output = self.run_script(script, args, input, input_file, subproc, cwd).stdout
        self.assertEqual(expected_output, actual_output)

    def run_script(self, script, args='', input=None, input_file=None, subproc=True, cwd=None):
        """运行指定的脚本，返回subprocess.CompletedProcess对象。

        :param script: str 脚本文件名
        :param args: str 命令行参数，空格分隔
        :param input: str 输入文本
        :param input_file: str 输入文件名，如果未指定input参数则从该文件读取输入，如果该参数也未指定则没有输入
        :param subproc: bool 如果为True则在子进程中运行，否则在当前进程中运行
        :param cwd: str 当前工作目录，默认为self.dir
        :return: subprocess.CompletedProcess对象
        """
        return self.run_script_subprocess(script, args, input, input_file, cwd) if subproc \
            else self.run_script_runpy(script, args, input, input_file, cwd)

    def run_script_subprocess(self, script, args='', input=None, input_file=None, cwd=None):
        cmd = [sys.executable, script, *shlex.split(args)]
        return self.run_cmd(cmd, input, input_file, cwd)

    def run_cmd(self, cmd, input=None, input_file=None, cwd=None):
        """运行指定的命令，返回subprocess.CompletedProcess对象。

        :param cmd: str or List[str] 要运行的命令
        :param input: str 输入文本
        :param input_file: str 输入文件名，如果未指定input参数则从该文件读取输入，如果该参数也未指定则没有输入
        :param cwd: str 当前工作目录，默认为self.dir
        :return: subprocess.CompletedProcess对象
        """
        if input is not None:
            stdin = None
        elif input_file:
            stdin = open(input_file, encoding='utf-8')
        else:
            stdin = DEVNULL

        result = subprocess.run(
            cmd, stdin=stdin, input=input, stdout=PIPE, stderr=PIPE,
            cwd=self.get_cwd(cwd), encoding='utf-8', text=True)
        if input_file:
            stdin.close()

        return result

    def run_script_runpy(self, script, args='', input=None, input_file=None, cwd=None):
        if input is not None:
            stdin = StringIO(input)
        elif input_file:
            stdin = open(input_file, encoding='utf-8')
        else:
            stdin = open(os.devnull)

        with patch('sys.argv', [script, *shlex.split(args)]), \
                patch('sys.stdin', stdin) as stdin, \
                patch('sys.stdout', new_callable=StringIO) as stdout, \
                patch('sys.stderr', new_callable=StringIO) as stderr:
            runpy.run_path(self.get_cwd(cwd) / script, run_name='__main__')
            stdin.close()
            return CompletedProcess(args, 0, stdout.getvalue(), stderr.getvalue())

    def run_server_script(self, server_script, server_args='', wait_time=1, client_func=None, cwd=None):
        """运行指定的服务器脚本，之后调用客户端，并返回服务器的输出。

        :param server_script: str 服务器脚本文件名
        :param server_args: str 服务器命令行参数，空格分隔
        :param wait_time: float 启动服务器后的等待时间，单位：秒
        :param client_func: Callable[[], Any] 调用客户端的函数
        :param cwd: str 当前工作目录，默认为self.dir
        :return: (str, str, Any) 服务器的标准输出、标准错误和客户端函数的返回结果
        """
        cmd = [sys.executable, server_script, *shlex.split(server_args)]
        return self.run_server_cmd(cmd, wait_time, client_func, cwd)

    def run_server_cmd(self, cmd, wait_time=1, client_func=None, cwd=None):
        """运行指定的服务器命令，之后调用客户端，并返回服务器的输出。

        :param cmd: str or List[str] 服务器命令
        :param wait_time: float 启动服务器后的等待时间，单位：秒
        :param client_func: Callable[[], Any] 调用客户端的函数
        :param cwd: str 当前工作目录，默认为self.dir
        :return: (str, str, Any) 服务器的标准输出、标准错误和客户端函数的返回结果
        """
        server_proc = Popen(
            cmd, stdin=DEVNULL, stdout=PIPE, stderr=PIPE,
            cwd=self.get_cwd(cwd), encoding='utf-8', text=True)
        time.sleep(wait_time)
        client_results = client_func() if callable(client_func) else None
        server_proc.kill()
        stdout, stderr = server_proc.communicate()
        return stdout, stderr, client_results

    def get_cwd(self, cwd):
        return pathlib.Path(cwd).resolve() if cwd is not None else self.src_dir
