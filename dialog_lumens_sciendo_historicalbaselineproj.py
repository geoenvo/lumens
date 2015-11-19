#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensSCIENDOHistoricalBaselineProjection(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDOHistoricalBaselineProjection, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS SCIENDO Historical Baseline Projection'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectQUESCDatabase.clicked.connect(self.handlerSelectQUESCDatabase)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensSCIENDOHistoricalBaselineProjection, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelWorkingDir = QtGui.QLabel(parent)
        self.labelWorkingDir.setText('Working directory:')
        layoutLumensDialog.addWidget(self.labelWorkingDir, 0, 0)
        
        self.lineEditWorkingDir = QtGui.QLineEdit(parent)
        self.lineEditWorkingDir.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditWorkingDir, 0, 1)
        
        self.buttonSelectWorkingDir = QtGui.QPushButton(parent)
        self.buttonSelectWorkingDir.setText('Select &Working Directory')
        layoutLumensDialog.addWidget(self.buttonSelectWorkingDir, 1, 0, 1, 2)
        
        self.labelQUESCDatabase = QtGui.QLabel(parent)
        self.labelQUESCDatabase.setText('QUES-C Database:')
        layoutLumensDialog.addWidget(self.labelQUESCDatabase, 2, 0)
        
        self.lineEditQUESCDatabase = QtGui.QLineEdit(parent)
        self.lineEditQUESCDatabase.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditQUESCDatabase, 2, 1)
        
        self.buttonSelectQUESCDatabase = QtGui.QPushButton(parent)
        self.buttonSelectQUESCDatabase.setText('Select &QUES-C Database')
        layoutLumensDialog.addWidget(self.buttonSelectQUESCDatabase, 3, 0, 1, 2)
        
        self.labelSpinBoxT1 = QtGui.QLabel(parent)
        self.labelSpinBoxT1.setText('Base year T&1:')
        layoutLumensDialog.addWidget(self.labelSpinBoxT1, 4, 0)
        
        self.spinBoxT1 = QtGui.QSpinBox(parent)
        self.spinBoxT1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxT1.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxT1, 4, 1)
        
        self.labelSpinBoxT1.setBuddy(self.spinBoxT1)
        
        self.labelSpinBoxT2 = QtGui.QLabel(parent)
        self.labelSpinBoxT2.setText('Base year T&2:')
        layoutLumensDialog.addWidget(self.labelSpinBoxT2, 5, 0)
        
        self.spinBoxT2 = QtGui.QSpinBox(parent)
        self.spinBoxT2.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxT2.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxT2, 5, 1)
        
        self.labelSpinBoxT2.setBuddy(self.spinBoxT2)
        
        self.labelSpinBoxIteration = QtGui.QLabel(parent)
        self.labelSpinBoxIteration.setText('&Iteration:')
        layoutLumensDialog.addWidget(self.labelSpinBoxIteration, 6, 0)
        
        self.spinBoxIteration = QtGui.QSpinBox(parent)
        self.spinBoxIteration.setValue(5)
        layoutLumensDialog.addWidget(self.spinBoxIteration, 6, 1)
        
        self.labelSpinBoxIteration.setBuddy(self.spinBoxIteration)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 7, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['QUESCDatabase'] = unicode(self.lineEditQUESCDatabase.text())
        self.main.appSettings[type(self).__name__]['t1'] = self.spinBoxT1.value()
        self.main.appSettings[type(self).__name__]['t2'] = self.spinBoxT2.value()
        self.main.appSettings[type(self).__name__]['iteration'] = self.spinBoxIteration.value()
    
    
    def handlerSelectWorkingDir(self):
        """Select a folder as working dir
        """
        workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if workingDir:
            self.lineEditWorkingDir.setText(workingDir)
            
            logging.getLogger(type(self).__name__).info('select working directory: %s', workingDir)
    
    
    def handlerSelectQUESCDatabase(self):
        """Select QUES-C database
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select QUES-C Database', QtCore.QDir.homePath(), 'QUES-C Database (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if file:
            self.lineEditQUESCDatabase.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:projection_historical_baseline',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['QUESCDatabase'],
                self.main.appSettings[type(self).__name__]['t1'],
                self.main.appSettings[type(self).__name__]['t2'],
                self.main.appSettings[type(self).__name__]['iteration'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            