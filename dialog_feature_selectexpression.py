#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from dialog_lumens_base import DialogLumensBase


class DialogFeatureSelectExpression(DialogLumensBase):
    """
    """
    
    
    def __init__(self, vectorLayer, parent):
        super(DialogFeatureSelectExpression, self).__init__(parent)
        
        self.vectorLayer = vectorLayer
        self.dialogTitle = 'Select Features By Expression - ' + self.vectorLayer.name()
        
        self.setupUi(self)
        
        self.buttonDialogSubmit.clicked.connect(self.handlerDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogFeatureSelectExpression, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelExpression = QtGui.QLabel(parent)
        self.labelExpression.setText('Expression:')
        layoutLumensDialog.addWidget(self.labelExpression, 0, 0)
        
        self.textEditExpression = QtGui.QPlainTextEdit(parent)
        layoutLumensDialog.addWidget(self.textEditExpression, 0, 1)
        
        self.buttonDialogSubmit = QtGui.QPushButton(parent)
        self.buttonDialogSubmit.setText('Select Features')
        layoutLumensDialog.addWidget(self.buttonDialogSubmit, 1, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['expression'] = unicode(self.textEditExpression.toPlainText())
    
    
    def handlerDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonDialogSubmit.setDisabled(True)
            
            # TODO qgsexpression
            
            self.buttonDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
