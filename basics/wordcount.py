#!/usr/bin/env python2.7
# encoding: utf-8

import string

# 文件读取可以使用 with 语法，来省略掉 try finally
# read_file = open('input1.txt')
# try:
with open('input1.txt') as read_file:
    # text = read_file.read()
    # 最好按行读，整个文件读进来太大的话会很慢，而且容易爆内存，比如读几百兆的文件

    # dict = {}
    # 变量命名没有意义，改为有意义的名字；而且这个 dict 与 Python 内建函数 dict 冲突了
    word_counter = {}

    # 文件按行读取可以直接用 in，比较简洁
    for text in read_file:
        text = text.translate(None, string.punctuation)  # 去除标点符号
        # 这里直接 split 即可，默认不带参数的 split 会已空白字符来分隔
        # text = text.replace("\n", " ").replace("\r", " ")
        # text_list = text.split(" ")
        text_list = text.split()

        for word in text_list:
            # if word_counter.has_key(i):
            # dict 判断 key 是否存在，可以使用 in 的语法；set 和 list 也一样
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1

    dict_to_sort_list = sorted(word_counter.items(), key=lambda x: x[1], reverse=False)
    with open('output.txt', 'w') as write_file:
        for k, v in dict_to_sort_list:
            write_file.write('%s:%d\n' % (k, v))

    # 不建议使用 + 大量拼接字符串，字符串在 Python 中是不可变类型，会占用大量内存，单行输出即可
    # 字符串的格式化参考：https://pyformat.info/
            # % 后面加 tuple： '%s:%d\n' % (k, v)
            # % 后面加 dict：'%(k)s:%(v)d\n' % {'k': k, 'v': v}
            # format 用法，比较灵活，多种用法
    # s = ""
    # for i in dict_to_sort_list:
    #     s += str(i[0]) + ":" + str(i[1]) + "\n"
    #     print s

    buf = []
    for k, v in dict_to_sort_list:
        buf.append('%s:%d' % (k, v))
    print '\n'.join(buf)
# finally:
#     read_file.close()

# write_file = open('output.txt', 'w')
# try:
#     write_file.write(s)
# finally:
#     write_file.close()
