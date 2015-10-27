#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensTARegionalEconomySingleIODescriptiveAnalysis(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTARegionalEconomySingleIODescriptiveAnalysis, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS TA Regional Economy Single I-O Descriptive Analysis'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectIntermediateConsumptionMatrix.clicked.connect(self.handlerSelectIntermediateConsumptionMatrix)
        self.buttonSelectValueAddedMatrix.clicked.connect(self.handlerSelectValueAddedMatrix)
        self.buttonSelectFinalConsumptionMatrix.clicked.connect(self.handlerSelectFinalConsumptionMatrix)
        self.buttonSelectValueAddedComponent.clicked.connect(self.handlerSelectValueAddedComponent)
        self.buttonSelectFinalConsumptionComponent.clicked.connect(self.handlerSelectFinalConsumptionComponent)
        self.buttonSelectListOfEconomicSector.clicked.connect(self.handlerSelectListOfEconomicSector)
        self.buttonSelectLabourRequirement.clicked.connect(self.handlerSelectLabourRequirement)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensTARegionalEconomySingleIODescriptiveAnalysis, self).setupUi(self)
        
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
        
        self.labelIntermediateConsumptionMatrix = QtGui.QLabel(parent)
        self.labelIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        layoutLumensDialog.addWidget(self.labelIntermediateConsumptionMatrix, 2, 0)
        
        self.lineEditIntermediateConsumptionMatrix = QtGui.QLineEdit(parent)
        self.lineEditIntermediateConsumptionMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditIntermediateConsumptionMatrix, 2, 1)
        
        self.buttonSelectIntermediateConsumptionMatrix = QtGui.QPushButton(parent)
        self.buttonSelectIntermediateConsumptionMatrix.setText('Select &Intermediate Consumption Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectIntermediateConsumptionMatrix, 3, 0, 1, 2)
        
        self.labelValueAddedMatrix = QtGui.QLabel(parent)
        self.labelValueAddedMatrix.setText('Value added matrix:')
        layoutLumensDialog.addWidget(self.labelValueAddedMatrix, 4, 0)
        
        self.lineEditValueAddedMatrix = QtGui.QLineEdit(parent)
        self.lineEditValueAddedMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedMatrix, 4, 1)
        
        self.buttonSelectValueAddedMatrix = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedMatrix.setText('Select &Value Added Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedMatrix, 5, 0, 1, 2)
        
        self.labelFinalConsumptionMatrix = QtGui.QLabel(parent)
        self.labelFinalConsumptionMatrix.setText('Final consumption matrix:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionMatrix, 6, 0)
        
        self.lineEditFinalConsumptionMatrix = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionMatrix, 6, 1)
        
        self.buttonSelectFinalConsumptionMatrix = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionMatrix.setText('Select &Final Consumption Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionMatrix, 7, 0, 1, 2)
        
        self.labelValueAddedComponent = QtGui.QLabel(parent)
        self.labelValueAddedComponent.setText('Value added component:')
        layoutLumensDialog.addWidget(self.labelValueAddedComponent, 8, 0)
        
        self.lineEditValueAddedComponent = QtGui.QLineEdit(parent)
        self.lineEditValueAddedComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedComponent, 8, 1)
        
        self.buttonSelectValueAddedComponent = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedComponent.setText('Select &Value Added Component')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedComponent, 9, 0, 1, 2)
        
        self.labelFinalConsumptionComponent = QtGui.QLabel(parent)
        self.labelFinalConsumptionComponent.setText('Final consumption component:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionComponent, 10, 0)
        
        self.lineEditFinalConsumptionComponent = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionComponent, 10, 1)
        
        self.buttonSelectFinalConsumptionComponent = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionComponent.setText('Select Final &Consumption Component')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionComponent, 11, 0, 1, 2)
        
        self.labelListOfEconomicSector = QtGui.QLabel(parent)
        self.labelListOfEconomicSector.setText('List of economic sector:')
        layoutLumensDialog.addWidget(self.labelListOfEconomicSector, 12, 0)
        
        self.lineEditListOfEconomicSector = QtGui.QLineEdit(parent)
        self.lineEditListOfEconomicSector.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditListOfEconomicSector, 12, 1)
        
        self.buttonSelectListOfEconomicSector = QtGui.QPushButton(parent)
        self.buttonSelectListOfEconomicSector.setText('Select List of &Economic Sector')
        layoutLumensDialog.addWidget(self.buttonSelectListOfEconomicSector, 13, 0, 1, 2)
        
        self.labelLabourRequirement = QtGui.QLabel(parent)
        self.labelLabourRequirement.setText('Labour requirement:')
        layoutLumensDialog.addWidget(self.labelLabourRequirement, 14, 0)
        
        self.lineEditLabourRequirement = QtGui.QLineEdit(parent)
        self.lineEditLabourRequirement.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLabourRequirement, 14, 1)
        
        self.buttonSelectLabourRequirement = QtGui.QPushButton(parent)
        self.buttonSelectLabourRequirement.setText('Select &Labour Requirement')
        layoutLumensDialog.addWidget(self.buttonSelectLabourRequirement, 15, 0, 1, 2)
        
        self.labelFinancialUnit = QtGui.QLabel(parent)
        self.labelFinancialUnit.setText('Financial &unit:')
        layoutLumensDialog.addWidget(self.labelFinancialUnit, 16, 0)
        
        self.lineEditFinancialUnit = QtGui.QLineEdit(parent)
        self.lineEditFinancialUnit.setText('Million Rupiah')
        layoutLumensDialog.addWidget(self.lineEditFinancialUnit, 16, 1)
        
        self.labelFinancialUnit.setBuddy(self.lineEditFinancialUnit)
        
        self.labelAreaName = QtGui.QLabel(parent)
        self.labelAreaName.setText('&Area name:')
        layoutLumensDialog.addWidget(self.labelAreaName, 17, 0)
        
        self.lineEditAreaName = QtGui.QLineEdit(parent)
        self.lineEditAreaName.setText('area')
        layoutLumensDialog.addWidget(self.lineEditAreaName, 17, 1)
        
        self.labelAreaName.setBuddy(self.lineEditAreaName)
        
        self.labelSpinBoxPeriod = QtGui.QLabel(parent)
        self.labelSpinBoxPeriod.setText('&Period:')
        layoutLumensDialog.addWidget(self.labelSpinBoxPeriod, 18, 0)
        
        self.spinBoxPeriod = QtGui.QSpinBox(parent)
        self.spinBoxPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxPeriod, 18, 1)
        
        self.labelSpinBoxPeriod.setBuddy(self.spinBoxPeriod)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 19, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrix'] = unicode(self.lineEditIntermediateConsumptionMatrix.text())
        self.main.appSettings[type(self).__name__]['valueAddedMatrix'] = unicode(self.lineEditValueAddedMatrix.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionMatrix'] = unicode(self.lineEditFinalConsumptionMatrix.text())
        self.main.appSettings[type(self).__name__]['valueAddedComponent'] = unicode(self.lineEditValueAddedComponent.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionComponent'] = unicode(self.lineEditFinalConsumptionComponent.text())
        self.main.appSettings[type(self).__name__]['listOfEconomicSector'] = unicode(self.lineEditListOfEconomicSector.text())
        self.main.appSettings[type(self).__name__]['labourRequirement'] = unicode(self.lineEditLabourRequirement.text())
        self.main.appSettings[type(self).__name__]['financialUnit'] = unicode(self.lineEditFinancialUnit.text())
        self.main.appSettings[type(self).__name__]['areaName'] = unicode(self.lineEditAreaName.text())
        self.main.appSettings[type(self).__name__]['period'] = self.spinBoxPeriod.value()
    
    
    def handlerSelectWorkingDir(self):
        """Select a folder as working dir
        """
        workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if workingDir:
            self.lineEditWorkingDir.setText(workingDir)
            
            logging.getLogger(type(self).__name__).info('select working directory: %s', workingDir)
    
    
    def handlerSelectIntermediateConsumptionMatrix(self):
        """Select Intermediate Consumption Matrix
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditIntermediateConsumptionMatrix.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectValueAddedMatrix(self):
        """Select Value Added Matrix
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix', QtCore.QDir.homePath(), 'Value Added Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditValueAddedMatrix.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectFinalConsumptionMatrix(self):
        """Select Final Consumption Matrix
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix', QtCore.QDir.homePath(), 'Final Consumption Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditFinalConsumptionMatrix.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectValueAddedComponent(self):
        """Select Value Added Component
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Component', QtCore.QDir.homePath(), 'Value Added Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditValueAddedComponent.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectFinalConsumptionComponent(self):
        """Select Final Consumption Component
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Component', QtCore.QDir.homePath(), 'Final Consumption Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditFinalConsumptionComponent.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectListOfEconomicSector(self):
        """Select List of Economic Sector
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select List of Economic Sector', QtCore.QDir.homePath(), 'List of Economic Sector (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditListOfEconomicSector.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLabourRequirement(self):
        """Select Labour Requirement
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Labour Requirement', QtCore.QDir.homePath(), 'Labour Requirement (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLabourRequirement.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:ta_reg_io_da',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrix'],
                self.main.appSettings[type(self).__name__]['valueAddedMatrix'],
                self.main.appSettings[type(self).__name__]['finalConsumptionMatrix'],
                self.main.appSettings[type(self).__name__]['valueAddedComponent'],
                self.main.appSettings[type(self).__name__]['finalConsumptionComponent'],
                self.main.appSettings[type(self).__name__]['listOfEconomicSector'],
                self.main.appSettings[type(self).__name__]['labourRequirement'],
                self.main.appSettings[type(self).__name__]['financialUnit'],
                self.main.appSettings[type(self).__name__]['areaName'],
                self.main.appSettings[type(self).__name__]['period'],
            )
            
            """
            print outputs
            """
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            