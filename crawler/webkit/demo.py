#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: webkit demo
            configure LD_LIBRARY_PATH=/your/path/to/PySide/:$LD_LIBRARY_PATH
    @author: icejoywoo
    @date: 16/05/2017
"""

import lxml.html
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *


app = QApplication([])
webview = QWebView()
loop = QEventLoop()
webview.loadFinished.connect(loop.quit)
webview.load(QUrl('http://example.webscraping.com/dynamic'))
loop.exec_()

html = webview.page().mainFrame().toHtml()
tree = lxml.html.fromstring(html)
print tree.cssselect('#result')[0].text_content()
