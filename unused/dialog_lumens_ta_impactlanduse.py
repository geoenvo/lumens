#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS TA Impact of Land Use to Regional Economy Indicator Analysis'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectLandCoverMapP1.clicked.connect(self.handlerSelectLandCoverMapP1)
        self.buttonSelectLandCoverMapP2.clicked.connect(self.handlerSelectLandCoverMapP2)
        self.buttonSelectIntermediateConsumptionMatrix.clicked.connect(self.handlerSelectIntermediateConsumptionMatrix)
        self.buttonSelectValueAddedMatrix.clicked.connect(self.handlerSelectValueAddedMatrix)
        self.buttonSelectFinalConsumptionMatrix.clicked.connect(self.handlerSelectFinalConsumptionMatrix)
        self.buttonSelectValueAddedComponent.clicked.connect(self.handlerSelectValueAddedComponent)
        self.buttonSelectFinalConsumptionComponent.clicked.connect(self.handlerSelectFinalConsumptionComponent)
        self.buttonSelectListOfEconomicSector.clicked.connect(self.handlerSelectListOfEconomicSector)
        self.buttonSelectLandDistributionMatrix.clicked.connect(self.handlerSelectLandDistributionMatrix)
        self.buttonSelectLandRequirementCoefficientMatrix.clicked.connect(self.handlerSelectLandRequirementCoefficientMatrix)
        self.buttonSelectLandCoverComponent.clicked.connect(self.handlerSelectLandCoverComponent)
        self.buttonSelectLabourRequirement.clicked.connect(self.handlerSelectLabourRequirement)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis, self).setupUi(self)
        
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
        
        self.labelLandCoverMapP1 = QtGui.QLabel(parent)
        self.labelLandCoverMapP1.setText('Land cover map period 1:')
        layoutLumensDialog.addWidget(self.labelLandCoverMapP1, 2, 0)
        
        self.lineEditLandCoverMapP1 = QtGui.QLineEdit(parent)
        self.lineEditLandCoverMapP1.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandCoverMapP1, 2, 1)
        
        self.buttonSelectLandCoverMapP1 = QtGui.QPushButton(parent)
        self.buttonSelectLandCoverMapP1.setText('Select Land Cover Map Period &1')
        layoutLumensDialog.addWidget(self.buttonSelectLandCoverMapP1, 3, 0, 1, 2)
        
        self.labelLandCoverMapP2 = QtGui.QLabel(parent)
        self.labelLandCoverMapP2.setText('Land cover map period 2:')
        layoutLumensDialog.addWidget(self.labelLandCoverMapP2, 4, 0)
        
        self.lineEditLandCoverMapP2 = QtGui.QLineEdit(parent)
        self.lineEditLandCoverMapP2.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandCoverMapP2, 4, 1)
        
        self.buttonSelectLandCoverMapP2 = QtGui.QPushButton(parent)
        self.buttonSelectLandCoverMapP2.setText('Select Land Cover Map Period &2')
        layoutLumensDialog.addWidget(self.buttonSelectLandCoverMapP2, 5, 0, 1, 2)
        
        self.labelIntermediateConsumptionMatrix = QtGui.QLabel(parent)
        self.labelIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        layoutLumensDialog.addWidget(self.labelIntermediateConsumptionMatrix, 6, 0)
        
        self.lineEditIntermediateConsumptionMatrix = QtGui.QLineEdit(parent)
        self.lineEditIntermediateConsumptionMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditIntermediateConsumptionMatrix, 6, 1)
        
        self.buttonSelectIntermediateConsumptionMatrix = QtGui.QPushButton(parent)
        self.buttonSelectIntermediateConsumptionMatrix.setText('Select &Intermediate Consumption Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectIntermediateConsumptionMatrix, 7, 0, 1, 2)
        
        self.labelValueAddedMatrix = QtGui.QLabel(parent)
        self.labelValueAddedMatrix.setText('Value added matrix:')
        layoutLumensDialog.addWidget(self.labelValueAddedMatrix, 8, 0)
        
        self.lineEditValueAddedMatrix = QtGui.QLineEdit(parent)
        self.lineEditValueAddedMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedMatrix, 8, 1)
        
        self.buttonSelectValueAddedMatrix = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedMatrix.setText('Select &Value Added Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedMatrix, 9, 0, 1, 2)
        
        self.labelFinalConsumptionMatrix = QtGui.QLabel(parent)
        self.labelFinalConsumptionMatrix.setText('Final consumption matrix:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionMatrix, 10, 0)
        
        self.lineEditFinalConsumptionMatrix = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionMatrix, 10, 1)
        
        self.buttonSelectFinalConsumptionMatrix = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionMatrix.setText('Select &Final Consumption Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionMatrix, 11, 0, 1, 2)
        
        self.labelValueAddedComponent = QtGui.QLabel(parent)
        self.labelValueAddedComponent.setText('Value added component:')
        layoutLumensDialog.addWidget(self.labelValueAddedComponent, 12, 0)
        
        self.lineEditValueAddedComponent = QtGui.QLineEdit(parent)
        self.lineEditValueAddedComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditValueAddedComponent, 12, 1)
        
        self.buttonSelectValueAddedComponent = QtGui.QPushButton(parent)
        self.buttonSelectValueAddedComponent.setText('Select &Value Added Component')
        layoutLumensDialog.addWidget(self.buttonSelectValueAddedComponent, 13, 0, 1, 2)
        
        self.labelFinalConsumptionComponent = QtGui.QLabel(parent)
        self.labelFinalConsumptionComponent.setText('Final consumption component:')
        layoutLumensDialog.addWidget(self.labelFinalConsumptionComponent, 14, 0)
        
        self.lineEditFinalConsumptionComponent = QtGui.QLineEdit(parent)
        self.lineEditFinalConsumptionComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFinalConsumptionComponent, 14, 1)
        
        self.buttonSelectFinalConsumptionComponent = QtGui.QPushButton(parent)
        self.buttonSelectFinalConsumptionComponent.setText('Select Final &Consumption Component')
        layoutLumensDialog.addWidget(self.buttonSelectFinalConsumptionComponent, 15, 0, 1, 2)
        
        self.labelListOfEconomicSector = QtGui.QLabel(parent)
        self.labelListOfEconomicSector.setText('List of economic sector:')
        layoutLumensDialog.addWidget(self.labelListOfEconomicSector, 16, 0)
        
        self.lineEditListOfEconomicSector = QtGui.QLineEdit(parent)
        self.lineEditListOfEconomicSector.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditListOfEconomicSector, 16, 1)
        
        self.buttonSelectListOfEconomicSector = QtGui.QPushButton(parent)
        self.buttonSelectListOfEconomicSector.setText('Select List of &Economic Sector')
        layoutLumensDialog.addWidget(self.buttonSelectListOfEconomicSector, 17, 0, 1, 2)
        
        self.labelLandDistributionMatrix = QtGui.QLabel(parent)
        self.labelLandDistributionMatrix.setText('Land distribution matrix:')
        layoutLumensDialog.addWidget(self.labelLandDistributionMatrix, 18, 0)
        
        self.lineEditLandDistributionMatrix = QtGui.QLineEdit(parent)
        self.lineEditLandDistributionMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandDistributionMatrix, 18, 1)
        
        self.buttonSelectLandDistributionMatrix = QtGui.QPushButton(parent)
        self.buttonSelectLandDistributionMatrix.setText('Select &Land Distribution Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectLandDistributionMatrix, 19, 0, 1, 2)
        
        self.labelLandRequirementCoefficientMatrix = QtGui.QLabel(parent)
        self.labelLandRequirementCoefficientMatrix.setText('Land requirement coefficient matrix:')
        layoutLumensDialog.addWidget(self.labelLandRequirementCoefficientMatrix, 20, 0)
        
        self.lineEditLandRequirementCoefficientMatrix = QtGui.QLineEdit(parent)
        self.lineEditLandRequirementCoefficientMatrix.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandRequirementCoefficientMatrix, 20, 1)
        
        self.buttonSelectLandRequirementCoefficientMatrix = QtGui.QPushButton(parent)
        self.buttonSelectLandRequirementCoefficientMatrix.setText('Select Land &Requirement Coefficient Matrix')
        layoutLumensDialog.addWidget(self.buttonSelectLandRequirementCoefficientMatrix, 21, 0, 1, 2)
        
        self.labelLandCoverComponent = QtGui.QLabel(parent)
        self.labelLandCoverComponent.setText('Land cover component:')
        layoutLumensDialog.addWidget(self.labelLandCoverComponent, 22, 0)
        
        self.lineEditLandCoverComponent = QtGui.QLineEdit(parent)
        self.lineEditLandCoverComponent.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandCoverComponent, 22, 1)
        
        self.buttonSelectLandCoverComponent = QtGui.QPushButton(parent)
        self.buttonSelectLandCoverComponent.setText('Select Land &Cover Component')
        layoutLumensDialog.addWidget(self.buttonSelectLandCoverComponent, 23, 0, 1, 2)
        
        self.labelLabourRequirement = QtGui.QLabel(parent)
        self.labelLabourRequirement.setText('Labour requirement:')
        layoutLumensDialog.addWidget(self.labelLabourRequirement, 24, 0)
        
        self.lineEditLabourRequirement = QtGui.QLineEdit(parent)
        self.lineEditLabourRequirement.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLabourRequirement, 24, 1)
        
        self.buttonSelectLabourRequirement = QtGui.QPushButton(parent)
        self.buttonSelectLabourRequirement.setText('Select &Labour Requirement')
        layoutLumensDialog.addWidget(self.buttonSelectLabourRequirement, 25, 0, 1, 2)
        
        self.labelFinancialUnit = QtGui.QLabel(parent)
        self.labelFinancialUnit.setText('Financial &unit:')
        layoutLumensDialog.addWidget(self.labelFinancialUnit, 26, 0)
        
        self.lineEditFinancialUnit = QtGui.QLineEdit(parent)
        self.lineEditFinancialUnit.setText('Million Rupiah')
        layoutLumensDialog.addWidget(self.lineEditFinancialUnit, 26, 1)
        
        self.labelFinancialUnit.setBuddy(self.lineEditFinancialUnit)
        
        self.labelAreaName = QtGui.QLabel(parent)
        self.labelAreaName.setText('&Area name:')
        layoutLumensDialog.addWidget(self.labelAreaName, 27, 0)
        
        self.lineEditAreaName = QtGui.QLineEdit(parent)
        self.lineEditAreaName.setText('area')
        layoutLumensDialog.addWidget(self.lineEditAreaName, 27, 1)
        
        self.labelAreaName.setBuddy(self.lineEditAreaName)
        
        self.labelSpinBoxPeriod = QtGui.QLabel(parent)
        self.labelSpinBoxPeriod.setText('&Period:')
        layoutLumensDialog.addWidget(self.labelSpinBoxPeriod, 28, 0)
        
        self.spinBoxPeriod = QtGui.QSpinBox(parent)
        self.spinBoxPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxPeriod, 28, 1)
        
        self.labelSpinBoxPeriod.setBuddy(self.spinBoxPeriod)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 29, 0, 1, 2)
        
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
        self.main.appSettings[type(self).__name__]['landCoverMapP1'] = unicode(self.lineEditLandCoverMapP1.text())
        self.main.appSettings[type(self).__name__]['landCoverMapP2'] = unicode(self.lineEditLandCoverMapP2.text())
        self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrix'] = unicode(self.lineEditIntermediateConsumptionMatrix.text())
        self.main.appSettings[type(self).__name__]['valueAddedMatrix'] = unicode(self.lineEditValueAddedMatrix.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionMatrix'] = unicode(self.lineEditFinalConsumptionMatrix.text())
        self.main.appSettings[type(self).__name__]['valueAddedComponent'] = unicode(self.lineEditValueAddedComponent.text())
        self.main.appSettings[type(self).__name__]['finalConsumptionComponent'] = unicode(self.lineEditFinalConsumptionComponent.text())
        self.main.appSettings[type(self).__name__]['listOfEconomicSector'] = unicode(self.lineEditListOfEconomicSector.text())
        self.main.appSettings[type(self).__name__]['landDistributionMatrix'] = unicode(self.lineEditLandDistributionMatrix.text())
        self.main.appSettings[type(self).__name__]['landRequirementCoefficientMatrix'] = unicode(self.lineEditLandRequirementCoefficientMatrix.text())
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
    
    
    def handlerSelectLandCoverMapP1(self):
        """Select Land Cover Map Period 1
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Map Period 1', QtCore.QDir.homePath(), 'Land Cover Map Period 1 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandCoverMapP1.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandCoverMapP2(self):
        """Select Land Cover Map Period 2
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Map Period 2', QtCore.QDir.homePath(), 'Land Cover Map Period 2 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandCoverMapP2.setText(file)
            
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
            self, 'Select Land Distribution Matrix', QtCore.QDir.homePath(), 'Land Distribution Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandDistributionMatrix.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementCoefficientMatrix(self):
        """Select Land Requirement Coefficient Matrix
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Requirement Coefficient Matrix', QtCore.QDir.homePath(), 'Land Requirement Coefficient Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandRequirementCoefficientMatrix.setText(file)
            
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
                'modeler:ta_reg_luc_gdp_lcc',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['landCoverMapP1'],
                self.main.appSettings[type(self).__name__]['landCoverMapP2'],
                self.main.appSettings[type(self).__name__]['intermediateConsumptionMatrix'],
                self.main.appSettings[type(self).__name__]['valueAddedMatrix'],
                self.main.appSettings[type(self).__name__]['finalConsumptionMatrix'],
                self.main.appSettings[type(self).__name__]['valueAddedComponent'],
                self.main.appSettings[type(self).__name__]['finalConsumptionComponent'],
                self.main.appSettings[type(self).__name__]['listOfEconomicSector'],
                self.main.appSettings[type(self).__name__]['landDistributionMatrix'],
                self.main.appSettings[type(self).__name__]['landRequirementCoefficientMatrix'],
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
            