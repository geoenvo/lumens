#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensQUESCCarbonAccounting(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensQUESCCarbonAccounting, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS QUES-C Carbon Accounting'
        
        self.setupUi(self)
        
        self.buttonSelectCsvfile.clicked.connect(self.handlerSelectCsvfile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensQUESCCarbonAccounting, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelCsvfile = QtGui.QLabel(parent)
        self.labelCsvfile.setText('Carbon density lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvfile, 0, 0)
        
        self.lineEditCsvfile = QtGui.QLineEdit(parent)
        self.lineEditCsvfile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvfile, 0, 1)
        
        self.buttonSelectCsvfile = QtGui.QPushButton(parent)
        self.buttonSelectCsvfile.setText('Select &Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvfile, 1, 0, 1, 2)
        
        self.labelSpinBox = QtGui.QLabel(parent)
        self.labelSpinBox.setText('&No data value:')
        layoutLumensDialog.addWidget(self.labelSpinBox, 2, 0)
        
        self.spinBox = QtGui.QSpinBox(parent)
        self.spinBox.setRange(-9999, 9999)
        self.spinBox.setValue(0)
        layoutLumensDialog.addWidget(self.spinBox, 2, 1)
        
        self.labelSpinBox.setBuddy(self.spinBox)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 3, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectCsvfile(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Carbon Density Lookup Table', QtCore.QDir.homePath(), 'Carbon Density Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvfile.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['csvfile'] = unicode(self.lineEditCsvfile.text())
        self.main.appSettings[type(self).__name__]['nodata'] = self.spinBox.value()
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:ques-c',
                self.main.appSettings[type(self).__name__]['csvfile'],
                self.main.appSettings[type(self).__name__]['nodata'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            