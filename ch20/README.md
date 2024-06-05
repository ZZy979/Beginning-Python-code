# 项目1：即时标记
## 目标
解析纯文本文件中的各种文本元素（例如标题、强调、列表项等），并转换为HTML。

## 代码
初次实现
* [文本块生成器](util.py)
* [简单的标记程序](simple_markup.py)

再次实现
* [处理器](handlers.py)
* [规则](rules.py)
* [主程序](markup.py)

## 运行

```shell
$ python markup.py < testdata/test_input.txt > testdata/test_output.html
```

## 截图
![生成的网页](screenshots/再次尝试生成的网页.png)
