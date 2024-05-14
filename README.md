# Beginning-Python-code
《Python基础教程》(Beginning Python: From Novice to Professional)（第3版）书中代码

* 本书网站：<https://folk.idi.ntnu.no/mlh/hetland_org/writing/beginning-python-2/>
* 源代码：<https://github.com/Apress/beginning-python-3ed>
* 笔记：<https://zzy979.github.io/posts/python-note-index/>

# 依赖
## Python版本
Python 3.11

## Python依赖库

```shell
pip install -r requirements.txt
```

## 其他依赖
第17章代码还依赖以下软件：
* JDK 8
* Jython 2.7.3
* C#编译器
* IronPython 3.4.1
* SWIG 4.2.1
* GCC编译器(Linux)或MSVC编译器(Windows)

# 单元测试
在项目根目录下执行：

```shell
python -m unittest
```

# 代码目录
## 第1章 基础知识
* [Hello world](ch01/hello.py)
* [What's your name](ch01/whats_your_name.py)
* [绘制三角形](ch01/draw_triangle.py)

## 第2章 列表和元组
* [代码清单2-1 索引示例](ch02/indexing_example.py)
* [代码清单2-2 切片示例](ch02/slicing_example.py)
* [代码清单2-3 序列乘法示例](ch02/sequence_multiplication_example.py)
* [代码清单2-4 序列成员资格示例](ch02/sequence_membership_example.py)

## 第3章 使用字符串
* [代码清单3-1 字符串格式化示例](ch03/string_formatting_example.py)

## 第4章 字典：当索引行不通时
* [代码清单4-1 字典示例](ch04/dictionary_example.py)
* [代码清单4-2 字典方法示例](ch04/dictionary_method_example.py)

## 第5章 条件、循环和其他语句
* [if语句示例](ch05/if_statement_example.py)
* [else子句示例](ch05/else_clause_example.py)
* [elif子句示例](ch05/elif_clause_example.py)
* [嵌套代码块示例](ch05/nested_blocks_example.py)
* [while语句示例](ch05/while_statement_example.py)
* [break语句示例](ch05/break_statement_example.py)
* [while True/break示例](ch05/while_true_break_idiom_example.py)
* [循环中的else子句示例](ch05/else_clause_in_loop_example.py)

## 第6章 抽象
* [简单联系人应用](ch06/simple_contacts.py)
* [参数练习](ch06/parameter_practice.py)
* [阶乘](ch06/factorial.py)
* [幂](ch06/power.py)
* [二分查找](ch06/binary_search.py)

## 第7章 再谈抽象
* [多态示例](ch07/polymorphism_example.py)
* [自定义类示例](ch07/person.py)
* [类命名空间示例](ch07/member_counter.py)
* [超类示例](ch07/filters.py)
* [多个超类示例](ch07/talking_calculator.py)

## 第8章 异常
* [异常示例](ch08/exception_example.py)
* [无参数raise示例](ch08/muffled_calculator.py)
* [多个except子句示例](ch08/except_clause_example.py)
* [try语句else子句示例](ch08/try_else_clause_example.py)

## 第9章 魔法方法、特性和迭代器
* [算术序列](ch09/arithseq.py)
* [带访问计数器的列表](ch09/counter_list.py)
* [property示例](ch09/rectangle_property.py)
* [\_\_getattr\_\_示例](ch09/rectangle_getattr.py)
* [迭代器示例](ch09/fibonacci_iterator.py)
* [从迭代器创建序列示例](ch09/test_iterator.py)
* [递归生成器示例](ch09/flatten.py)
* [模拟生成器示例](ch09/non_generator_flatten.py)
* [八皇后问题](ch09/queens.py)

## 第10章 自带电池
* [代码清单10-4 带有条件测试代码的模块](ch10/hello4.py)
* [包示例](ch10/drawing)
* [代码清单10-5 反序打印命令行参数](ch10/reverseargs.py)
* [代码清单10-6 给Python脚本添加行号](ch10/numberlines.py)
* [随机时间](ch10/random_time.py)
* [掷骰子](ch10/throw_dice.py)
* [随机谚语](ch10/random_fortune.py)
* [随机发牌](ch10/deal_cards.py)
* [代码清单10-8 简单的数据库应用](ch10/database.py)
* [代码清单10-10 查找发件人](ch10/find_sender.py)
* [列出邮件地址](ch10/list_email_addresses.py)
* [代码清单10-11 一个模板系统](ch10/templates.py)

## 第11章 文件
* [代码清单11-1 单词计数](ch11/wordcount.py)

## 第12章 图形用户界面
* [代码清单12-1 简单文本编辑器](ch12/text_editor.py)

## 第13章 数据库支持
* 数据库应用程序示例
  * [代码清单13-1 将数据导入数据库](ch13/importdata.py)
  * [代码清单13-2 食品数据库查询程序](ch13/food_query.py)

## 第14章 网络编程
* [代码清单14-1 小型服务器](ch14/minimal_server.py)
* [代码清单14-2 小型客户端](ch14/minimal_client.py)
* [代码清单14-3 基于socketserver的小型服务器](ch14/socketserver_minimal_server.py)
* [代码清单14-4 分叉服务器](ch14/forking_server.py)
* [代码清单14-5 线程化服务器](ch14/threading_server.py)
* [代码清单14-6 使用select的简单服务器](ch14/select_server.py)
* [Telnet客户端](ch14/telnet_client.py)
* [代码清单14-7 使用poll的简单服务器](ch14/poll_server.py)
* [代码清单14-8 使用Twisted的简单服务器](ch14/twisted_server.py)
* [代码清单14-9 使用LineReceiver改进的日志服务器](ch14/twisted_line_server.py)

## 第15章 Python和Web
* [代码清单15-1 简单的屏幕抓取程序](ch15/scrape_python_jobs.py)
* [代码清单15-2 使用HTMLParser的屏幕抓取程序](ch15/scrape_python_jobs_html_parser.py)
* [代码清单15-3 使用Beautiful Soup的屏幕抓取程序](ch15/scrape_python_jobs_bs.py)
* [代码清单15-4 简单的CGI脚本](ch15/cgi-bin/simple1.cgi)
* [CGI HTTP服务器](ch15/cgi_server.py)
* [代码清单15-5 显示栈跟踪的CGI脚本](ch15/cgi-bin/faulty.cgi)
* [代码清单15-6 从FieldStorage获取单个值的CGI脚本](ch15/cgi-bin/simple2.cgi)
* [代码清单15-7 带有HTML表单的问候CGI脚本](ch15/cgi-bin/simple3.cgi)
* [Flask示例](ch15/powers.py)

## 第16章 测试
* [代码清单16-1 简单的测试程序](ch16/area_test.py)
* [doctest示例](ch16/my_math.py)
* [代码清单16-2 使用unittest框架的简单测试](ch16/test_my_math.py)

## 第17章 扩展Python
* [代码清单17-1 一个简单的Java类](ch17/JythonTest.java)
* [代码清单17-2 一个简单的C#类](ch17/IronPythonTest.cs)
* [代码清单17-3 检测回文的C语言函数](ch17/palindrome.c)
* [代码清单17-4 检测回文的Python函数](ch17/palindrome_pure.py)
* [代码清单17-5 回文库的接口文件](ch17/palindrome.i)
* [代码清单17-6 检测回文2](ch17/palindrome2.c)

## 第18章 程序打包
* [代码清单18-1 简单的Setuptools安装脚本](ch18/hello/setup.py)
* [palindrome安装脚本](ch18/palindrome2/setup.py)
* [使用SWIG的palindrome安装脚本](ch18/palindrome/setup.py)
* [py2exe安装脚本](ch18/hello2/setup.py)
