# pdfbookmark
# PDF 文档自动添加书签工具

## Features
## 描述

Automatically add bookmarks to pdf documents according to the given regex.

You have to go through a somewhat painful debugging process
if you want every added bookmark is exactly what you want
and never omit where you desire it to be added.

根据给定正则表达式遍历 PDF 文档的所有页，
将匹配的页加上书签。

要想书签加得好，关键得正则写的准。

## Dependencies
## 依赖

- PyPDF2, which can be installed via pip

- PyPDF2，可以用 pip 安装。

- pdftotext, which is available from the package poppler-utils

- pdftotext，由软件包 popler-utils 提供

## Examples
## 演示用例

See samples.txt

Also see this real world case,
[man2pdf](https://github.com/NoviceLive/man2pdf)
.

参见 samples.txt

还可以参见这个使用示例，
[man2pdf](https://github.com/NoviceLive/man2pdf)
。

## TODO
## 改进

- Heirarchical bookmarks

- 有层次的书签

## Copyright
## 版权

Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

## License
## 授权

GPL
