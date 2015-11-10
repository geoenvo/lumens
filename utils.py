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


#############################################################################


class DetailedMessageBox(QtGui.QMessageBox):
    """
    """
    def __init__(self, *args, **kwargs):            
        super(DetailedMessageBox, self).__init__(*args, **kwargs)
    
    
    def showEvent(self, event):
        super(DetailedMessageBox, self).showEvent(event)
        
        # show details on messagebox open
        for button in self.buttons():
            if button.text() == 'Show Details...':
                button.click()
    
    
    def resizeEvent(self, event):

        result = super(DetailedMessageBox, self).resizeEvent(event)

        details_box = self.findChild(QtGui.QTextEdit)
        
        if details_box is not None:
            details_box.setFixedSize(details_box.sizeHint())

        return result

