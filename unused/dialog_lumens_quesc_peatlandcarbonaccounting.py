#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensQUESCPeatlandCarbonAccounting(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensQUESCPeatlandCarbonAccounting, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS QUES-C Peatland Carbon Accounting'
        
        self.setupUi(self)
        
        self.buttonSelectCsvfile.clicked.connect(self.handlerSelectCsvfile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensQUESCPeatlandCarbonAccounting, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelCsvfile = QtGui.QLabel(parent)
        self.labelCsvfile.setText('Carbon stock lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvfile, 0, 0)
        
        self.lineEditCsvfile = QtGui.QLineEdit(parent)
        self.lineEditCsvfile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvfile, 0, 1)
        
        self.buttonSelectCsvfile = QtGui.QPushButton(parent)
        self.buttonSelectCsvfile.setText('Select &Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvfile, 1, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 2, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectCsvfile(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Carbon Stock Lookup Table', QtCore.QDir.homePath(), 'Carbon Stock Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvfile.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['csvfile'] = unicode(self.lineEditCsvfile.text())
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:ques-c_peat',
                self.main.appSettings[type(self).__name__]['csvfile'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            