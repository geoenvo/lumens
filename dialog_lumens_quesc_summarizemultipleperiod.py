#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensQUESCSummarizeMultiplePeriod(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensQUESCSummarizeMultiplePeriod, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS QUES-C Summarize Multiple Period'
        
        self.setupUi(self)
        
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensQUESCSummarizeMultiplePeriod, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelCheckbox = QtGui.QLabel(parent)
        self.labelCheckbox.setText('Include &peat:')
        layoutLumensDialog.addWidget(self.labelCheckbox, 0, 0)
        
        self.checkbox = QtGui.QCheckBox(parent)
        self.checkbox.setChecked(True)
        layoutLumensDialog.addWidget(self.checkbox, 0, 1)
        
        self.labelCheckbox.setBuddy(self.checkbox)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 1, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        checkboxVal = None
        
        if self.checkbox.isChecked():
            checkboxVal = 0
        else:
            checkboxVal = 1
        
        self.main.appSettings[type(self).__name__]['checkbox'] = checkboxVal
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'r:summarizemultipleperiod',
                self.main.appSettings[type(self).__name__]['checkbox'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            