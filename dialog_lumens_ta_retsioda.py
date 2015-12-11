#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS TA Regional Economy Time Series I-O Descriptive Analysis'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectIntermediateConsumptionMatrixP1.clicked.connect(self.handlerSelectIntermediateConsumptionMatrixP1)
        self.buttonSelectIntermediateConsumptionMatrixP2.clicked.connect(self.handlerSelectIntermediateConsumptionMatrixP2)
        self.buttonSelectValueAddedMatrixP1.clicked.connect(self.handlerSelectValueAddedMatrixP1)
        self.buttonSelectValueAddedMatrixP2.clicked.connect(self.handlerSelectValueAddedMatrixP2)
        self.buttonSelectFinalConsumptionMatrixP1.clicked.connect(self.handlerSelectFinalConsumptionMatrixP1)
        self.buttonSelectFinalConsumptionMatrixP2.clicked.connect(self.handlerSelectFinalConsumptionMatrixP2)
        self.buttonSelectValueAddedComponent.clicked.connect(self.handlerSelectValueAddedComponent)
        self.buttonSelectFinalConsumptionComponent.clicked.connect(self.handlerSelectFinalConsumptionComponent)
        self.buttonSelectListOfEconomicSector.clicked.connect(self.handlerSelectListOfEconomicSector)
        self.buttonSelectLabourRequirementP1.clicked.connect(self.handlerSelectLabourRequirementP1)
        self.buttonSelectLabourRequirementP2.clicked.connect(self.handlerSelectLabourRequirementP2)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis, self).setupUi(self)
        
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
        
        self.labelIntermediateConsumptionMatrixP1 = QtGui.QLabel(parent)
        self.labelIntermediateConsumptionMatrixP1.setText('Intermediate consumption matrix period 1:')
        layoutLumensDialog.addWidget(self.labelIntermediateConsumptionMatrixP1, 2, 0)
        
        self.lineEditIntermediateConsumptionMatrixP1 = QtGui.QLineEdit(parent)
        self.lineEditIntermediateConsumptionMatrixP1.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditIntermediateConsumptionMatrixP1, 2, 1)
        
        self.buttonSelectIntermediateConsumptionMatrixP1 = QtGui.QPushButton(parent)
        self.buttonSelectIntermediateConsumptionMatrixP1.setText('Select &Intermediate Consumption Matrix Period 1')
        layoutLumensDialog.addWidget(self.buttonSelectIntermediateConsumptionMatrixP1, 3, 0, 1, 2)
        
        self.labelIntermediateConsumptionMatrixP2 = QtGui.QLabel(parent)
        self.labelIntermediateConsumptionMatrixP2.setText('Intermediate consumption matrix period 2:')
        layoutLumensDialog.addWidget(self.labelIntermediateConsumptionMatrixP2, 4, 0)
        
        self.lineEditIntermediateConsumptionMatrixP2 = QtGui.QLineEdit(parent)
        self.lineEditIntermediateConsumptionMatrixP2.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditIntermediateConsumptionMatrixP2, 4, 1)
        
        self.buttonSelectIntermediateConsumptionMatrixP2 = QtGui.QPushButton(parent)
        self.buttonSelectIntermediateConsumptionMatrixP2.setText('Select Intermediate Consumption &Matrix Period 2')
        layoutLumensDialog.addWidget(self.buttonSelectIntermediateConsumptionMatrixP2, 5, 0, 1, 2)
        
        self.labelValueAddedMatrixP1 = QtGui.QLabel(parent)
        self.labelValueAddedMatrixP1.setText('Value added matrix period 1:')
        layoutLumensDialog.addWidget(self.labelValueAddedMatrixP1, 6, 0)
        
        self.lineEditValueAddedMatrixP1 = QtGui.QLineEdit(parent)
        self.lineEditValueAddedMatrixP1.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedMatrixP1, 6, 1)
        
        self.buttonSelectValueAddedMatrixP1 = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedMatrixP1.setText('Select &Value Added Matrix Period 1')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedMatrixP1, 7, 0, 1, 2)
        
        self.labelValueAddedMatrixP2 = QtGui.QLabel(parent)
        self.labelValueAddedMatrixP2.setText('Value added matrix period 2:')
        layoutLumensDialog.addWidget(self.labelValueAddedMatrixP2, 8, 0)
        
        self.lineEditValueAddedMatrixP2 = QtGui.QLineEdit(parent)
        self.lineEditValueAddedMatrixP2.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedMatrixP2, 8, 1)
        
        self.buttonSelectValueAddedMatrixP2 = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedMatrixP2.setText('Select Value &Added Matrix Period 2')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedMatrixP2, 9, 0, 1, 2)
        
        self.labelFinalConsumptionMatrixP1 = QtGui.QLabel(parent)
        self.labelFinalConsumptionMatrixP1.setText('Final consumption matrix period 1:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionMatrixP1, 10, 0)
        
        self.lineEditFinalConsumptionMatrixP1 = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionMatrixP1.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionMatrixP1, 10, 1)
        
        self.buttonSelectFinalConsumptionMatrixP1 = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionMatrixP1.setText('Select &Final Consumption Matrix Period 1')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionMatrixP1, 11, 0, 1, 2)
        
        self.labelFinalConsumptionMatrixP2 = QtGui.QLabel(parent)
        self.labelFinalConsumptionMatrixP2.setText('Final consumption matrix period 2:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionMatrixP2, 12, 0)
        
        self.lineEditFinalConsumptionMatrixP2 = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionMatrixP2.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionMatrixP2, 12, 1)
        
        self.buttonSelectFinalConsumptionMatrixP2 = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionMatrixP2.setText('Select Final &Consumption Matrix Period 2')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionMatrixP2, 13, 0, 1, 2)
        
        self.labelValueAddedComponent = QtGui.QLabel(parent)
        self.labelValueAddedComponent.setText('Value added component:')
        layoutLumensDialog.addWidget(self.labelValueAddedComponent, 14, 0)
        
        self.lineEditValueAddedComponent = QtGui.QLineEdit(parent)
        self.lineEditValueAddedComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedComponent, 14, 1)
        
        self.buttonSelectValueAddedComponent = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedComponent.setText('Select &Value Added Component')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedComponent, 15, 0, 1, 2)
        
        self.labelFinalConsumptionComponent = QtGui.QLabel(parent)
        self.labelFinalConsumptionComponent.setText('Final consumption component:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionComponent, 16, 0)
        
        self.lineEditFinalConsumptionComponent = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionComponent, 16, 1)
        
        self.buttonSelectFinalConsumptionComponent = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionComponent.setText('&Select Final Consumption Component')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionComponent, 17, 0, 1, 2)
        
        self.labelListOfEconomicSector = QtGui.QLabel(parent)
        self.labelListOfEconomicSector.setText('List of economic sector:')
        layoutLumensDialog.addWidget(self.labelListOfEconomicSector, 18, 0)
        
        self.lineEditListOfEconomicSector = QtGui.QLineEdit(parent)
        self.lineEditListOfEconomicSector.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditListOfEconomicSector, 18, 1)
        
        self.buttonSelectListOfEconomicSector = QtGui.QPushButton(parent)
        self.buttonSelectListOfEconomicSector.setText('Select List of &Economic Sector')
        layoutLumensDialog.addWidget(self.buttonSelectListOfEconomicSector, 19, 0, 1, 2)
        
        self.labelLabourRequirementP1 = QtGui.QLabel(parent)
        self.labelLabourRequirementP1.setText('Labour requirement period 1:')
        layoutLumensDialog.addWidget(self.labelLabourRequirementP1, 20, 0)
        
        self.lineEditLabourRequirementP1 = QtGui.QLineEdit(parent)
        self.lineEditLabourRequirementP1.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLabourRequirementP1, 20, 1)
        
        self.buttonSelectLabourRequirementP1 = QtGui.QPushButton(parent)
        self.buttonSelectLabourRequirementP1.setText('Select &Labour Requirement Period 1')
        layoutLumensDialog.addWidget(self.buttonSelectLabourRequirementP1, 21, 0, 1, 2)
        
        self.labelLabourRequirementP2 = QtGui.QLabel(parent)
        self.labelLabourRequirementP2.setText('Labour requirement period 2:')
        layoutLumensDialog.addWidget(self.labelLabourRequirementP2, 22, 0)
        
        self.lineEditLabourRequirementP2 = QtGui.QLineEdit(parent)
        self.lineEditLabourRequirementP2.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLabourRequirementP2, 22, 1)
        
        self.buttonSelectLabourRequirementP2 = QtGui.QPushButton(parent)
        self.buttonSelectLabourRequirementP2.setText('Select Labour &Requirement Period 2')
        layoutLumensDialog.addWidget(self.buttonSelectLabourRequirementP2, 23, 0, 1, 2)
        
        self.labelFinancialUnit = QtGui.QLabel(parent)
        self.labelFinancialUnit.setText('Financial &unit:')
        layoutLumensDialog.addWidget(self.labelFinancialUnit, 24, 0)
        
        self.lineEditFinancialUnit = QtGui.QLineEdit(parent)
        self.lineEditFinancialUnit.setText('Million Rupiah')
        layoutLumensDialog.addWidget(self.lineEditFinancialUnit, 24, 1)
        
        self.labelFinancialUnit.setBuddy(self.lineEditFinancialUnit)
        
        self.labelAreaName = QtGui.QLabel(parent)
        self.labelAreaName.setText('&Area name:')
        layoutLumensDialog.addWidget(self.labelAreaName, 25, 0)
        
        self.lineEditAreaName = QtGui.QLineEdit(parent)
        self.lineEditAreaName.setText('area')
        layoutLumensDialog.addWidget(self.lineEditAreaName, 25, 1)
        
        self.labelAreaName.setBuddy(self.lineEditAreaName)
        
        self.labelSpinBoxPeriod1 = QtGui.QLabel(parent)
        self.labelSpinBoxPeriod1.setText('Period &1:')
        layoutLumensDialog.addWidget(self.labelSpinBoxPeriod1, 28, 0)
        
        self.spinBoxPeriod1 = QtGui.QSpinBox(parent)
        self.spinBoxPeriod1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod1.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxPeriod1, 28, 1)
        
        self.labelSpinBoxPeriod1.setBuddy(self.spinBoxPeriod1)
        
        self.labelSpinBoxPeriod2 = QtGui.QLabel(parent)
        self.labelSpinBoxPeriod2.setText('Period &2:')
        layoutLumensDialog.addWidget(self.labelSpinBoxPeriod2, 29, 0)
        
        self.spinBoxPeriod2 = QtGui.QSpinBox(parent)
        self.spinBoxPeriod2.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod2.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxPeriod2, 29, 1)
        
        self.labelSpinBoxPeriod2.setBuddy(self.spinBoxPeriod2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 30, 0, 1, 2)
        
        contents = QtGui.QWidget()
        contents.setLayout(layoutLumensDialog)
        
        scrollArea = QtGui.QScrollArea()
        scrollArea.setFixedHeight(500)
        scrollArea.setWidget(contents)
        
        self.dialogLayout.addWidget(scrollArea)
        ##self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setFixedWidth(410)
        ##self.setMinimumSize(400, 200)
        ##self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrixP1'] = unicode(self.lineEditIntermediateConsumptionMatrixP1.text())
        self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrixP2'] = unicode(self.lineEditIntermediateConsumptionMatrixP2.text())
        self.main.appSettings[type(self).__name__]['valueAddedMatrixP1'] = unicode(self.lineEditValueAddedMatrixP1.text())
        self.main.appSettings[type(self).__name__]['valueAddedMatrixP2'] = unicode(self.lineEditValueAddedMatrixP2.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionMatrixP1'] = unicode(self.lineEditFinalConsumptionMatrixP1.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionMatrixP2'] = unicode(self.lineEditFinalConsumptionMatrixP2.text())
        self.main.appSettings[type(self).__name__]['valueAddedComponent'] = unicode(self.lineEditValueAddedComponent.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionComponent'] = unicode(self.lineEditFinalConsumptionComponent.text())
        self.main.appSettings[type(self).__name__]['listOfEconomicSector'] = unicode(self.lineEditListOfEconomicSector.text())
        self.main.appSettings[type(self).__name__]['labourRequirementP1'] = unicode(self.lineEditLabourRequirementP1.text())
        self.main.appSettings[type(self).__name__]['labourRequirementP2'] = unicode(self.lineEditLabourRequirementP2.text())
        self.main.appSettings[type(self).__name__]['financialUnit'] = unicode(self.lineEditFinancialUnit.text())
        self.main.appSettings[type(self).__name__]['areaName'] = unicode(self.lineEditAreaName.text())
        self.main.appSettings[type(self).__name__]['period1'] = self.spinBoxPeriod1.value()
        self.main.appSettings[type(self).__name__]['period2'] = self.spinBoxPeriod2.value()
    
    
    def handlerSelectWorkingDir(self):
        """Select a folder as working dir
        """
        workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if workingDir:
            self.lineEditWorkingDir.setText(workingDir)
            
            logging.getLogger(type(self).__name__).info('select working directory: %s', workingDir)
    
    
    def handlerSelectIntermediateConsumptionMatrixP1(self):
        """Select Intermediate Consumption Matrix P2
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix Period 1', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix Period 1 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditIntermediateConsumptionMatrixP1.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectIntermediateConsumptionMatrixP2(self):
        """Select Intermediate Consumption Matrix P2
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix Period 2', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix Period 2 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditIntermediateConsumptionMatrixP2.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectValueAddedMatrixP1(self):
        """Select Value Added Matrix P1
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix Period 1', QtCore.QDir.homePath(), 'Value Added Matrix Period 1 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditValueAddedMatrixP1.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectValueAddedMatrixP2(self):
        """Select Value Added Matrix P2
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix Period 2', QtCore.QDir.homePath(), 'Value Added Matrix Period 2 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditValueAddedMatrixP2.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectFinalConsumptionMatrixP1(self):
        """Select Final Consumption Matrix P1
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix Period 1', QtCore.QDir.homePath(), 'Final Consumption Matrix Period 1 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditFinalConsumptionMatrixP1.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectFinalConsumptionMatrixP2(self):
        """Select Final Consumption Matrix P2
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix Period 2', QtCore.QDir.homePath(), 'Final Consumption Matrix Period 2 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditFinalConsumptionMatrixP2.setText(file)
            
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
    
    
    def handlerSelectLabourRequirementP1(self):
        """Select Labour Requirement P1
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Labour Requirement Period 1', QtCore.QDir.homePath(), 'Labour Requirement Period 1 (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLabourRequirementP1.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLabourRequirementP2(self):
        """Select Labour Requirement P2
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Labour Requirement Period 2', QtCore.QDir.homePath(), 'Labour Requirement Period 2 (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLabourRequirementP2.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:ta_reg_ts_io',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrixP1'],
                self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrixP2'],
                self.main.appSettings[type(self).__name__]['valueAddedMatrixP1'],
                self.main.appSettings[type(self).__name__]['valueAddedMatrixP2'],
                self.main.appSettings[type(self).__name__]['finalConsumptionMatrixP1'],
                self.main.appSettings[type(self).__name__]['finalConsumptionMatrixP2'],
                self.main.appSettings[type(self).__name__]['valueAddedComponent'],
                self.main.appSettings[type(self).__name__]['finalConsumptionComponent'],
                self.main.appSettings[type(self).__name__]['listOfEconomicSector'],
                self.main.appSettings[type(self).__name__]['labourRequirementP1'],
                self.main.appSettings[type(self).__name__]['labourRequirementP2'],
                self.main.appSettings[type(self).__name__]['financialUnit'],
                self.main.appSettings[type(self).__name__]['areaName'],
                self.main.appSettings[type(self).__name__]['period1'],
                self.main.appSettings[type(self).__name__]['period2'],
            )
            
            """
            print outputs
            """
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            