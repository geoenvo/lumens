#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensTAOpportunityCost(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTAOpportunityCost, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS TA Opportunity Cost'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectQUESCDatabase.clicked.connect(self.handlerSelectQUESCDatabase)
        self.buttonSelectCsvNPVTable.clicked.connect(self.handlerSelectCsvNPVTable)
        self.buttonSelectOutputOpportunityCostDatabase.clicked.connect(self.handlerSelectOutputOpportunityCostDatabase)
        self.buttonSelectOutputOpportunityCostReport.clicked.connect(self.handlerSelectOutputOpportunityCostReport)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensTAOpportunityCost, self).setupUi(self)
        
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
        
        self.labelCsvNPVTable = QtGui.QLabel(parent)
        self.labelCsvNPVTable.setText('Net Present Value (NPV) table:')
        layoutLumensDialog.addWidget(self.labelCsvNPVTable, 4, 0)
        
        self.lineEditCsvNPVTable = QtGui.QLineEdit(parent)
        self.lineEditCsvNPVTable.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvNPVTable, 4, 1)
        
        self.buttonSelectCsvNPVTable = QtGui.QPushButton(parent)
        self.buttonSelectCsvNPVTable.setText('Select &NPV Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvNPVTable, 5, 0, 1, 2)
        
        self.labelSpinBoxPeriod1 = QtGui.QLabel(parent)
        self.labelSpinBoxPeriod1.setText('Period &1:')
        layoutLumensDialog.addWidget(self.labelSpinBoxPeriod1, 6, 0)
        
        self.spinBoxPeriod1 = QtGui.QSpinBox(parent)
        self.spinBoxPeriod1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod1.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxPeriod1, 6, 1)
        
        self.labelSpinBoxPeriod1.setBuddy(self.spinBoxPeriod1)
        
        self.labelSpinBoxPeriod2 = QtGui.QLabel(parent)
        self.labelSpinBoxPeriod2.setText('Period &2:')
        layoutLumensDialog.addWidget(self.labelSpinBoxPeriod2, 7, 0)
        
        self.spinBoxPeriod2 = QtGui.QSpinBox(parent)
        self.spinBoxPeriod2.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod2.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxPeriod2, 7, 1)
        
        self.labelSpinBoxPeriod2.setBuddy(self.spinBoxPeriod2)
        
        self.labelSpinBoxCostThreshold = QtGui.QLabel(parent)
        self.labelSpinBoxCostThreshold.setText('Cost &Threshold:')
        layoutLumensDialog.addWidget(self.labelSpinBoxCostThreshold, 8, 0)
        
        self.spinBoxCostThreshold = QtGui.QSpinBox(parent)
        self.spinBoxCostThreshold.setValue(5)
        layoutLumensDialog.addWidget(self.spinBoxCostThreshold, 8, 1)
        
        self.labelSpinBoxCostThreshold.setBuddy(self.spinBoxCostThreshold)
        
        self.labelOutputOpportunityCostDatabase = QtGui.QLabel(parent)
        self.labelOutputOpportunityCostDatabase.setText('Opportunity cost database (output):')
        layoutLumensDialog.addWidget(self.labelOutputOpportunityCostDatabase, 9, 0)
        
        self.lineEditOutputOpportunityCostDatabase = QtGui.QLineEdit(parent)
        self.lineEditOutputOpportunityCostDatabase.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputOpportunityCostDatabase, 9, 1)
        
        self.buttonSelectOutputOpportunityCostDatabase = QtGui.QPushButton(parent)
        self.buttonSelectOutputOpportunityCostDatabase.setText('Select Opportunity Cost &Database')
        layoutLumensDialog.addWidget(self.buttonSelectOutputOpportunityCostDatabase, 10, 0, 1, 2)
        
        self.labelOutputOpportunityCostReport = QtGui.QLabel(parent)
        self.labelOutputOpportunityCostReport.setText('Opportunity cost report (output):')
        layoutLumensDialog.addWidget(self.labelOutputOpportunityCostReport, 11, 0)
        
        self.lineEditOutputOpportunityCostReport = QtGui.QLineEdit(parent)
        self.lineEditOutputOpportunityCostReport.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputOpportunityCostReport, 11, 1)
        
        self.buttonSelectOutputOpportunityCostReport = QtGui.QPushButton(parent)
        self.buttonSelectOutputOpportunityCostReport.setText('Select Opportunity Cost &Report')
        layoutLumensDialog.addWidget(self.buttonSelectOutputOpportunityCostReport, 13, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 14, 0, 1, 2)
        
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
        self.main.appSettings[type(self).__name__]['csvNPVTable'] = unicode(self.lineEditCsvNPVTable.text())
        self.main.appSettings[type(self).__name__]['period1'] = self.spinBoxPeriod1.value()
        self.main.appSettings[type(self).__name__]['period2'] = self.spinBoxPeriod2.value()
        self.main.appSettings[type(self).__name__]['costThreshold'] = self.spinBoxCostThreshold.value()
        
        outputOpportunityCostDatabase = unicode(self.lineEditOutputOpportunityCostDatabase.text())
        outputOpportunityCostReport = unicode(self.lineEditOutputOpportunityCostReport.text())
        
        if not outputOpportunityCostDatabase:
            outputOpportunityCostDatabase = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputOpportunityCostDatabase'] = outputOpportunityCostDatabase
        
        if not outputOpportunityCostReport:
            outputOpportunityCostReport = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputOpportunityCostReport'] = outputOpportunityCostReport
    
    
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
    
    
    def handlerSelectCsvNPVTable(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select NPV Table', QtCore.QDir.homePath(), 'NPV Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvNPVTable.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerSelectOutputOpportunityCostDatabase(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Opportunity Cost Database Output', QtCore.QDir.homePath(), 'Opportunity Cost Database (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOutputOpportunityCostDatabase.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOutputOpportunityCostReport(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Opportunity Cost Report Output', QtCore.QDir.homePath(), 'Opportunity Cost Report (*{0})'.format(self.main.appSettings['selectHTMLfileExt'])))
        
        if outputfile:
            self.lineEditOutputOpportunityCostReport.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputOpportunityCostDatabase = self.main.appSettings[type(self).__name__]['outputOpportunityCostDatabase']
            outputOpportunityCostReport = self.main.appSettings[type(self).__name__]['outputOpportunityCostReport']
            
            if outputOpportunityCostDatabase == '__UNSET__':
                outputOpportunityCostDatabase = None
            
            if outputOpportunityCostReport == '__UNSET__':
                outputOpportunityCostReport = None
            
            outputs = general.runalg(
                'modeler:opportunity_cost',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['QUESCDatabase'],
                self.main.appSettings[type(self).__name__]['csvNPVTable'],
                self.main.appSettings[type(self).__name__]['period1'],
                self.main.appSettings[type(self).__name__]['period2'],
                self.main.appSettings[type(self).__name__]['costThreshold'],
                outputOpportunityCostDatabase,
                outputOpportunityCostReport,
            )
            
            """
            print outputs
            
            if not outputOpportunityCostDatabase:
                self.main.appSettings[type(self).__name__]['outputOpportunityCostDatabase'] = outputs['????']
            
            if not outputOpportunityCostReport:
                self.main.appSettings[type(self).__name__]['outputOpportunityCostReport'] = outputs['????']
            """
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            