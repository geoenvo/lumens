#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS TA Regional Economy Land Distribution & Requirement Analysis'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectLandCoverMap.clicked.connect(self.handlerSelectLandCoverMap)
        self.buttonSelectIntermediateConsumptionMatrix.clicked.connect(self.handlerSelectIntermediateConsumptionMatrix)
        self.buttonSelectValueAddedMatrix.clicked.connect(self.handlerSelectValueAddedMatrix)
        self.buttonSelectFinalConsumptionMatrix.clicked.connect(self.handlerSelectFinalConsumptionMatrix)
        self.buttonSelectValueAddedComponent.clicked.connect(self.handlerSelectValueAddedComponent)
        self.buttonSelectFinalConsumptionComponent.clicked.connect(self.handlerSelectFinalConsumptionComponent)
        self.buttonSelectListOfEconomicSector.clicked.connect(self.handlerSelectListOfEconomicSector)
        self.buttonSelectLandDistributionMatrix.clicked.connect(self.handlerSelectLandDistributionMatrix)
        self.buttonSelectLandCoverComponent.clicked.connect(self.handlerSelectLandCoverComponent)
        self.buttonSelectLabourRequirement.clicked.connect(self.handlerSelectLabourRequirement)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis, self).setupUi(self)
        
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
        
        self.labelLandCoverMap = QtGui.QLabel(parent)
        self.labelLandCoverMap.setText('Land cover map:')
        layoutLumensDialog.addWidget(self.labelLandCoverMap, 2, 0)
        
        self.lineEditLandCoverMap = QtGui.QLineEdit(parent)
        self.lineEditLandCoverMap.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandCoverMap, 2, 1)
        
        self.buttonSelectLandCoverMap = QtGui.QPushButton(parent)
        self.buttonSelectLandCoverMap.setText('Select &Land Cover Map')
        layoutLumensDialog.addWidget(self.buttonSelectLandCoverMap, 3, 0, 1, 2)
        
        self.labelIntermediateConsumptionMatrix = QtGui.QLabel(parent)
        self.labelIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        layoutLumensDialog.addWidget(self.labelIntermediateConsumptionMatrix, 4, 0)
        
        self.lineEditIntermediateConsumptionMatrix = QtGui.QLineEdit(parent)
        self.lineEditIntermediateConsumptionMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditIntermediateConsumptionMatrix, 4, 1)
        
        self.buttonSelectIntermediateConsumptionMatrix = QtGui.QPushButton(parent)
        self.buttonSelectIntermediateConsumptionMatrix.setText('Select &Intermediate Consumption Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectIntermediateConsumptionMatrix, 5, 0, 1, 2)
        
        self.labelValueAddedMatrix = QtGui.QLabel(parent)
        self.labelValueAddedMatrix.setText('Value added matrix:')
        layoutLumensDialog.addWidget(self.labelValueAddedMatrix, 6, 0)
        
        self.lineEditValueAddedMatrix = QtGui.QLineEdit(parent)
        self.lineEditValueAddedMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedMatrix, 6, 1)
        
        self.buttonSelectValueAddedMatrix = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedMatrix.setText('Select &Value Added Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedMatrix, 7, 0, 1, 2)
        
        self.labelFinalConsumptionMatrix = QtGui.QLabel(parent)
        self.labelFinalConsumptionMatrix.setText('Final consumption matrix:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionMatrix, 8, 0)
        
        self.lineEditFinalConsumptionMatrix = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionMatrix, 8, 1)
        
        self.buttonSelectFinalConsumptionMatrix = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionMatrix.setText('Select &Final Consumption Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionMatrix, 9, 0, 1, 2)
        
        self.labelValueAddedComponent = QtGui.QLabel(parent)
        self.labelValueAddedComponent.setText('Value added component:')
        layoutLumensDialog.addWidget(self.labelValueAddedComponent, 10, 0)
        
        self.lineEditValueAddedComponent = QtGui.QLineEdit(parent)
        self.lineEditValueAddedComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedComponent, 10, 1)
        
        self.buttonSelectValueAddedComponent = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedComponent.setText('Select &Value Added Component')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedComponent, 11, 0, 1, 2)
        
        self.labelFinalConsumptionComponent = QtGui.QLabel(parent)
        self.labelFinalConsumptionComponent.setText('Final consumption component:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionComponent, 12, 0)
        
        self.lineEditFinalConsumptionComponent = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionComponent, 12, 1)
        
        self.buttonSelectFinalConsumptionComponent = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionComponent.setText('Select Final &Consumption Component')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionComponent, 13, 0, 1, 2)
        
        self.labelListOfEconomicSector = QtGui.QLabel(parent)
        self.labelListOfEconomicSector.setText('List of economic sector:')
        layoutLumensDialog.addWidget(self.labelListOfEconomicSector, 14, 0)
        
        self.lineEditListOfEconomicSector = QtGui.QLineEdit(parent)
        self.lineEditListOfEconomicSector.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditListOfEconomicSector, 14, 1)
        
        self.buttonSelectListOfEconomicSector = QtGui.QPushButton(parent)
        self.buttonSelectListOfEconomicSector.setText('Select List of &Economic Sector')
        layoutLumensDialog.addWidget(self.buttonSelectListOfEconomicSector, 15, 0, 1, 2)
        
        self.labelLandDistributionMatrix = QtGui.QLabel(parent)
        self.labelLandDistributionMatrix.setText('Land distribution matrix:')
        layoutLumensDialog.addWidget(self.labelLandDistributionMatrix, 16, 0)
        
        self.lineEditLandDistributionMatrix = QtGui.QLineEdit(parent)
        self.lineEditLandDistributionMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandDistributionMatrix, 16, 1)
        
        self.buttonSelectLandDistributionMatrix = QtGui.QPushButton(parent)
        self.buttonSelectLandDistributionMatrix.setText('Select &Land Distribution Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectLandDistributionMatrix, 17, 0, 1, 2)
        
        self.labelLandCoverComponent = QtGui.QLabel(parent)
        self.labelLandCoverComponent.setText('Land cover component:')
        layoutLumensDialog.addWidget(self.labelLandCoverComponent, 18, 0)
        
        self.lineEditLandCoverComponent = QtGui.QLineEdit(parent)
        self.lineEditLandCoverComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandCoverComponent, 18, 1)
        
        self.buttonSelectLandCoverComponent = QtGui.QPushButton(parent)
        self.buttonSelectLandCoverComponent.setText('Select Land &Cover Component')
        layoutLumensDialog.addWidget(self.buttonSelectLandCoverComponent, 19, 0, 1, 2)
        
        self.labelLabourRequirement = QtGui.QLabel(parent)
        self.labelLabourRequirement.setText('Labour requirement:')
        layoutLumensDialog.addWidget(self.labelLabourRequirement, 20, 0)
        
        self.lineEditLabourRequirement = QtGui.QLineEdit(parent)
        self.lineEditLabourRequirement.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLabourRequirement, 20, 1)
        
        self.buttonSelectLabourRequirement = QtGui.QPushButton(parent)
        self.buttonSelectLabourRequirement.setText('Select &Labour Requirement')
        layoutLumensDialog.addWidget(self.buttonSelectLabourRequirement, 21, 0, 1, 2)
        
        self.labelFinancialUnit = QtGui.QLabel(parent)
        self.labelFinancialUnit.setText('Financial &unit:')
        layoutLumensDialog.addWidget(self.labelFinancialUnit, 22, 0)
        
        self.lineEditFinancialUnit = QtGui.QLineEdit(parent)
        self.lineEditFinancialUnit.setText('Million Rupiah')
        layoutLumensDialog.addWidget(self.lineEditFinancialUnit, 22, 1)
        
        self.labelFinancialUnit.setBuddy(self.lineEditFinancialUnit)
        
        self.labelAreaName = QtGui.QLabel(parent)
        self.labelAreaName.setText('&Area name:')
        layoutLumensDialog.addWidget(self.labelAreaName, 23, 0)
        
        self.lineEditAreaName = QtGui.QLineEdit(parent)
        self.lineEditAreaName.setText('area')
        layoutLumensDialog.addWidget(self.lineEditAreaName, 23, 1)
        
        self.labelAreaName.setBuddy(self.lineEditAreaName)
        
        self.labelSpinBoxPeriod = QtGui.QLabel(parent)
        self.labelSpinBoxPeriod.setText('&Period:')
        layoutLumensDialog.addWidget(self.labelSpinBoxPeriod, 24, 0)
        
        self.spinBoxPeriod = QtGui.QSpinBox(parent)
        self.spinBoxPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxPeriod, 24, 1)
        
        self.labelSpinBoxPeriod.setBuddy(self.spinBoxPeriod)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 25, 0, 1, 2)
        
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
        self.main.appSettings[type(self).__name__]['landCoverMap'] = unicode(self.lineEditLandCoverMap.text())
        self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrix'] = unicode(self.lineEditIntermediateConsumptionMatrix.text())
        self.main.appSettings[type(self).__name__]['valueAddedMatrix'] = unicode(self.lineEditValueAddedMatrix.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionMatrix'] = unicode(self.lineEditFinalConsumptionMatrix.text())
        self.main.appSettings[type(self).__name__]['valueAddedComponent'] = unicode(self.lineEditValueAddedComponent.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionComponent'] = unicode(self.lineEditFinalConsumptionComponent.text())
        self.main.appSettings[type(self).__name__]['listOfEconomicSector'] = unicode(self.lineEditListOfEconomicSector.text())
        self.main.appSettings[type(self).__name__]['landDistributionMatrix'] = unicode(self.lineEditLandDistributionMatrix.text())
        self.main.appSettings[type(self).__name__]['landCoverComponent'] = unicode(self.lineEditLandCoverComponent.text())
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
    
    
    def handlerSelectLandCoverMap(self):
        """Select Land Cover Map
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Map', QtCore.QDir.homePath(), 'Land Cover Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandCoverMap.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectIntermediateConsumptionMatrix(self):
        """Select Intermediate Consumption Matrix
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditIntermediateConsumptionMatrix.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectValueAddedMatrix(self):
        """Select Value Added Matrix
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix', QtCore.QDir.homePath(), 'Value Added Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditValueAddedMatrix.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectFinalConsumptionMatrix(self):
        """Select Final Consumption Matrix
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix', QtCore.QDir.homePath(), 'Final Consumption Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
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
    
    
    def handlerSelectLandDistributionMatrix(self):
        """Select Land Distribution Matrix
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Distribution Matrix', QtCore.QDir.homePath(), 'Land Distribution Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandDistributionMatrix.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandCoverComponent(self):
        """Select Land Cover Component
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Component', QtCore.QDir.homePath(), 'Land Cover Component (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandCoverComponent.setText(file)
            
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
                'modeler:ta_reg_ld_lr',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['landCoverMap'],
                self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrix'],
                self.main.appSettings[type(self).__name__]['valueAddedMatrix'],
                self.main.appSettings[type(self).__name__]['finalConsumptionMatrix'],
                self.main.appSettings[type(self).__name__]['valueAddedComponent'],
                self.main.appSettings[type(self).__name__]['finalConsumptionComponent'],
                self.main.appSettings[type(self).__name__]['listOfEconomicSector'],
                self.main.appSettings[type(self).__name__]['landDistributionMatrix'],
                self.main.appSettings[type(self).__name__]['landCoverComponent'],
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
            