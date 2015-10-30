#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensSCIENDODriversAnalysis(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDODriversAnalysis, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS SCIENDO Drivers Analysis'
        
        self.setupUi(self)
        
        self.buttonSelectLandUseCoverChangeDrivers.clicked.connect(self.handlerSelectLandUseCoverChangeDrivers)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensSCIENDODriversAnalysis, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelLandUseCoverChangeDrivers = QtGui.QLabel(parent)
        self.labelLandUseCoverChangeDrivers.setText('Drivers of land use/cover change:')
        layoutLumensDialog.addWidget(self.labelLandUseCoverChangeDrivers, 0, 0)
        
        self.lineEditLandUseCoverChangeDrivers = QtGui.QLineEdit(parent)
        self.lineEditLandUseCoverChangeDrivers.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandUseCoverChangeDrivers, 0, 1)
        
        self.buttonSelectLandUseCoverChangeDrivers = QtGui.QPushButton(parent)
        self.buttonSelectLandUseCoverChangeDrivers.setText('Select &Drivers of Land Use/Cover Change')
        layoutLumensDialog.addWidget(self.buttonSelectLandUseCoverChangeDrivers, 1, 0, 1, 2)
        
        self.labellandUseCoverChangeType = QtGui.QLabel(parent)
        self.labellandUseCoverChangeType.setText('Land use/cover change type:')
        layoutLumensDialog.addWidget(self.labellandUseCoverChangeType, 2, 0)
        
        self.lineEditlandUseCoverChangeType = QtGui.QLineEdit(parent)
        self.lineEditlandUseCoverChangeType.setText('Perubahan penggunaan lahan')
        layoutLumensDialog.addWidget(self.lineEditlandUseCoverChangeType, 2, 1)
        
        self.labellandUseCoverChangeType.setBuddy(self.lineEditlandUseCoverChangeType)
        
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
        self.main.appSettings[type(self).__name__]['landUseCoverChangeDrivers'] = unicode(self.lineEditLandUseCoverChangeDrivers.text())
        self.main.appSettings[type(self).__name__]['landUseCoverChangeType'] = unicode(self.lineEditlandUseCoverChangeType.text())
    
    
    def handlerSelectLandUseCoverChangeDrivers(self):
        """Select Land Use Cover Change Drivers
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use/Cover Change Drivers', QtCore.QDir.homePath(), 'Land Use/Cover Change Drivers (*{0})'.format(self.main.appSettings['selectTextfileExt'])))
        
        if file:
            self.lineEditLandUseCoverChangeDrivers.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:drivers_analysis',
                self.main.appSettings[type(self).__name__]['landUseCoverChangeDrivers'],
                self.main.appSettings[type(self).__name__]['landUseCoverChangeType'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            