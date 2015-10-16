#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
from PyQt4 import QtGui

class QPlainTextEditLogger(logging.Handler):
    """Custom logging widget class
    """
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()
        
        self.widget = QtGui.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
    
    
    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
    
    
    def write(self, m):
        pass