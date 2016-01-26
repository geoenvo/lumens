#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensSCIENDOHistoricalBaselineAnnualProjection(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDOHistoricalBaselineAnnualProjection, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS SCIENDO Historical Baseline Annual Projection'
        
        self.setupUi(self)
        
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensSCIENDOHistoricalBaselineAnnualProjection, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelSpinBoxIteration = QtGui.QLabel(parent)
        self.labelSpinBoxIteration.setText('&Iteration:')
        layoutLumensDialog.addWidget(self.labelSpinBoxIteration, 0, 0)
        
        self.spinBoxIteration = QtGui.QSpinBox(parent)
        self.spinBoxIteration.setValue(5)
        layoutLumensDialog.addWidget(self.spinBoxIteration, 0, 1)
        
        self.labelSpinBoxIteration.setBuddy(self.spinBoxIteration)
        
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
        self.main.appSettings[type(self).__name__]['iteration'] = self.spinBoxIteration.value()
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'r:historicalbaselineannualprojection',
                self.main.appSettings[type(self).__name__]['iteration'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            