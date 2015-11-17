#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *




class DialogLumensBase(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, parent):
        print 'debug: DialogLumensBase init'
        
        super(DialogLumensBase, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS Dialog'
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout(parent)
        
        self.logBox = QPlainTextEditLogger(parent)
        
        self.logger = logging.getLogger(type(parent).__name__)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logBox.setFormatter(formatter)
        self.logger.addHandler(self.logBox)
        self.logger.setLevel(logging.DEBUG)
        
        self.dialogLayout.addWidget(self.logBox.widget)
        
        # Show the logging widget only in debug mode
        if not self.main.appSettings['debug']:
            self.logBox.widget.setVisible(False)
        
        self.setWindowTitle(self.dialogTitle)
    
    
    def validDialogForm(self):
        """Check for empty form fields
        """
        logging.getLogger(type(self).__name__).info(self.main.appSettings)
        
        valid = True
        
        for key, val in self.main.appSettings[type(self).__name__].iteritems():
            if not val:
                valid = False
        
        if not valid:
            QtGui.QMessageBox.critical(self, 'Error', 'Please complete the fields.')
        
        return valid
    
    
    def clearLayout(self, layout):
        """Clear a layout and all its child widgets
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtGui.QWidgetItem):
                ## print "widget" + str(item)
                ## item.widget().close()
                item.widget().deleteLater() # use this to properly delete the widget
                # or
                # item.widget().setParent(None)
            elif isinstance(item, QtGui.QSpacerItem):
                ## print "spacer " + str(item)
                pass
                # no need to do extra stuff
            else:
                ## print "layout " + str(item)
                self.clearLayout(item.layout())

            # remove the item from layout
            layout.removeItem(item)