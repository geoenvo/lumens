#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensSCIENDOBuildScenario(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDOBuildScenario, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS SCIENDO Build Scenario'
        
        self.setupUi(self)
        
        self.buttonSelectHistoricalBaselineCar.clicked.connect(self.handlerSelectHistoricalBaselineCar)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensSCIENDOBuildScenario, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelHistoricalBaselineCar = QtGui.QLabel(parent)
        self.labelHistoricalBaselineCar.setText('Historical baseline car:')
        layoutLumensDialog.addWidget(self.labelHistoricalBaselineCar, 0, 0)
        
        self.lineEditHistoricalBaselineCar = QtGui.QLineEdit(parent)
        self.lineEditHistoricalBaselineCar.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditHistoricalBaselineCar, 0, 1)
        
        self.buttonSelectHistoricalBaselineCar = QtGui.QPushButton(parent)
        self.buttonSelectHistoricalBaselineCar.setText('Select &Historical Baseline Car')
        layoutLumensDialog.addWidget(self.buttonSelectHistoricalBaselineCar, 1, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 3, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['historicalBaselineCar'] = unicode(self.lineEditHistoricalBaselineCar.text())
    
    
    def handlerSelectHistoricalBaselineCar(self):
        """Select Historical Baseline Car
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Historical Baseline Car', QtCore.QDir.homePath(), 'Historical Baseline Car (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditHistoricalBaselineCar.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'r:abacususingabsolutearea',
                self.main.appSettings[type(self).__name__]['historicalBaselineCar'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            