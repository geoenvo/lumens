#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
##from qgis.core import *
##from processing.tools import *
from PyQt4 import QtCore, QtGui
import resource


class DialogLumensTARegionalEconomy(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTARegionalEconomy, self).__init__(parent)
        print 'DEBUG: DialogLumensTARegionalEconomy init'
        
        self.main = parent
        self.dialogTitle = 'LUMENS Trade-Off Analysis [Regional Economy]'
        
        self.setupUi(self)
        
        self.checkBoxMultiplePeriod.toggled.connect(self.toggleMultiplePeriod)
        
        self.radioRegionalEconomicScenarioImpactFinalDemand.toggled.connect(lambda:self.toggleRegionalEconomicScenarioImpactType(self.radioRegionalEconomicScenarioImpactFinalDemand))
        self.radioRegionalEconomicScenarioImpactGDP.toggled.connect(lambda:self.toggleRegionalEconomicScenarioImpactType(self.radioRegionalEconomicScenarioImpactGDP))
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabDescriptiveAnalysis = QtGui.QWidget()
        self.tabRegionalEconomicScenarioImpact = QtGui.QWidget()
        self.tabLandRequirementAnalysis = QtGui.QWidget()
        self.tabLandUseChangeImpact = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        self.tabReport = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabDescriptiveAnalysis, 'Descriptive Analysis of Regional Economy')
        self.tabWidget.addTab(self.tabRegionalEconomicScenarioImpact, 'Regional Economic Scenario Impact')
        self.tabWidget.addTab(self.tabLandRequirementAnalysis, 'Land Requirement Analysis')
        self.tabWidget.addTab(self.tabLandUseChangeImpact, 'Land Use Change Impact')
        self.tabWidget.addTab(self.tabResult, 'Result')
        self.tabWidget.addTab(self.tabReport, 'Report')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        self.layoutTabDescriptiveAnalysis = QtGui.QVBoxLayout()
        self.layoutTabRegionalEconomicScenarioImpact = QtGui.QVBoxLayout()
        self.layoutTabLandRequirementAnalysis = QtGui.QVBoxLayout()
        self.layoutTabLandUseChangeImpact = QtGui.QVBoxLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        self.layoutTabReport = QtGui.QVBoxLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabDescriptiveAnalysis.setLayout(self.layoutTabDescriptiveAnalysis)
        self.tabRegionalEconomicScenarioImpact.setLayout(self.layoutTabRegionalEconomicScenarioImpact)
        self.tabLandRequirementAnalysis.setLayout(self.layoutTabLandRequirementAnalysis)
        self.tabLandUseChangeImpact.setLayout(self.layoutTabLandUseChangeImpact)
        self.tabResult.setLayout(self.layoutTabResult)
        self.tabReport.setLayout(self.layoutTabReport)
        self.tabLog.setLayout(self.layoutTabLog)
        
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Descriptive Analysis of Regional Economy' tab
        #***********************************************************
        # Use QScrollArea
        self.layoutContentDescriptiveAnalysis = QtGui.QVBoxLayout()
        self.contentDescriptiveAnalysis = QtGui.QWidget()
        self.contentDescriptiveAnalysis.setLayout(self.layoutContentDescriptiveAnalysis)
        self.scrollDescriptiveAnalysis = QtGui.QScrollArea()
        self.scrollDescriptiveAnalysis.setWidgetResizable(True);
        self.scrollDescriptiveAnalysis.setWidget(self.contentDescriptiveAnalysis)
        self.layoutTabDescriptiveAnalysis.addWidget(self.scrollDescriptiveAnalysis)
        
        # 'Single period' GroupBox
        self.groupBoxSinglePeriod = QtGui.QGroupBox('Single period')
        self.layoutGroupBoxSinglePeriod = QtGui.QVBoxLayout()
        self.layoutGroupBoxSinglePeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxSinglePeriod.setLayout(self.layoutGroupBoxSinglePeriod)
        self.layoutSinglePeriodInfo = QtGui.QVBoxLayout()
        self.layoutSinglePeriod = QtGui.QGridLayout()
        self.layoutGroupBoxSinglePeriod.addLayout(self.layoutSinglePeriodInfo)
        self.layoutGroupBoxSinglePeriod.addLayout(self.layoutSinglePeriod)
        
        self.labelSinglePeriodInfo = QtGui.QLabel()
        self.labelSinglePeriodInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutSinglePeriodInfo.addWidget(self.labelSinglePeriodInfo)
        
        self.labelSinglePeriod = QtGui.QLabel()
        self.labelSinglePeriod.setText('&Period T1:')
        self.layoutSinglePeriod.addWidget(self.labelSinglePeriod, 0, 0)
        
        self.spinBoxSinglePeriod = QtGui.QSpinBox()
        self.spinBoxSinglePeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxSinglePeriod.setValue(td.year)
        self.layoutSinglePeriod.addWidget(self.spinBoxSinglePeriod, 0, 1)
        self.labelSinglePeriod.setBuddy(self.spinBoxSinglePeriod)
        
        self.labelSingleIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelSingleIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleIntermediateConsumptionMatrix, 1, 0)
        
        self.lineEditSingleIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditSingleIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutSinglePeriod.addWidget(self.lineEditSingleIntermediateConsumptionMatrix, 1, 1)
        
        self.buttonSelectSingleIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectSingleIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutSinglePeriod.addWidget(self.buttonSelectSingleIntermediateConsumptionMatrix, 1, 2)
        
        self.labelSingleValueAddedMatrix = QtGui.QLabel()
        self.labelSingleValueAddedMatrix.setText('Value added matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleValueAddedMatrix, 2, 0)
        
        self.lineEditSingleValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditSingleValueAddedMatrix.setReadOnly(True)
        self.layoutSinglePeriod.addWidget(self.lineEditSingleValueAddedMatrix, 2, 1)
        
        self.buttonSelectSingleValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectSingleValueAddedMatrix.setText('&Browse')
        self.layoutSinglePeriod.addWidget(self.buttonSelectSingleValueAddedMatrix, 2, 2)
        
        self.labelSingleFinalConsumptionMatrix = QtGui.QLabel()
        self.labelSingleFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleFinalConsumptionMatrix, 3, 0)
        
        self.lineEditSingleFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditSingleFinalConsumptionMatrix.setReadOnly(True)
        self.layoutSinglePeriod.addWidget(self.lineEditSingleFinalConsumptionMatrix, 3, 1)
        
        self.buttonSelectSingleFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectSingleFinalConsumptionMatrix.setText('&Browse')
        self.layoutSinglePeriod.addWidget(self.buttonSelectSingleFinalConsumptionMatrix, 3, 2)
        
        self.labelSingleLabourRequirement = QtGui.QLabel()
        self.labelSingleLabourRequirement.setText('Labour requirement:')
        self.layoutSinglePeriod.addWidget(self.labelSingleLabourRequirement, 4, 0)
        
        self.lineEditSingleLabourRequirement = QtGui.QLineEdit()
        self.lineEditSingleLabourRequirement.setReadOnly(True)
        self.layoutSinglePeriod.addWidget(self.lineEditSingleLabourRequirement, 4, 1)
        
        self.buttonSelectSingleLabourRequirement = QtGui.QPushButton()
        self.buttonSelectSingleLabourRequirement.setText('&Browse')
        self.layoutSinglePeriod.addWidget(self.buttonSelectSingleLabourRequirement, 4, 2)
        
        # 'Multiple period' GroupBox
        self.groupBoxMultiplePeriod = QtGui.QGroupBox('Multiple period')
        self.layoutGroupBoxMultiplePeriod = QtGui.QHBoxLayout()
        self.groupBoxMultiplePeriod.setLayout(self.layoutGroupBoxMultiplePeriod)
        self.layoutOptionsMultiplePeriod = QtGui.QVBoxLayout()
        self.layoutOptionsMultiplePeriod.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsMultiplePeriod = QtGui.QWidget()
        self.contentOptionsMultiplePeriod.setLayout(self.layoutOptionsMultiplePeriod)
        self.layoutOptionsMultiplePeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxMultiplePeriod = QtGui.QCheckBox()
        self.checkBoxMultiplePeriod.setChecked(False)
        self.contentOptionsMultiplePeriod.setDisabled(True)
        self.layoutGroupBoxMultiplePeriod.addWidget(self.checkBoxMultiplePeriod)
        self.layoutGroupBoxMultiplePeriod.addWidget(self.contentOptionsMultiplePeriod)
        #self.layoutGroupBoxMultiplePeriod.insertStretch(2, 1)
        self.layoutGroupBoxMultiplePeriod.setAlignment(self.checkBoxMultiplePeriod, QtCore.Qt.AlignTop)
        self.layoutMultiplePeriodInfo = QtGui.QVBoxLayout()
        self.layoutMultiplePeriod = QtGui.QGridLayout()
        self.layoutOptionsMultiplePeriod.addLayout(self.layoutMultiplePeriodInfo)
        self.layoutOptionsMultiplePeriod.addLayout(self.layoutMultiplePeriod)
        
        self.labelMultiplePeriodInfo = QtGui.QLabel()
        self.labelMultiplePeriodInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutMultiplePeriodInfo.addWidget(self.labelMultiplePeriodInfo)
        
        self.labelMultiplePeriod = QtGui.QLabel()
        self.labelMultiplePeriod.setText('&Period T2:')
        self.layoutMultiplePeriod.addWidget(self.labelMultiplePeriod, 0, 0)
        
        self.spinBoxMultiplePeriod = QtGui.QSpinBox()
        self.spinBoxMultiplePeriod.setRange(1, 9999)
        self.spinBoxMultiplePeriod.setValue(td.year)
        self.layoutMultiplePeriod.addWidget(self.spinBoxMultiplePeriod, 0, 1)
        self.labelMultiplePeriod.setBuddy(self.spinBoxMultiplePeriod)
        
        self.labelMultipleIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelMultipleIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutMultiplePeriod.addWidget(self.labelMultipleIntermediateConsumptionMatrix, 1, 0)
        
        self.lineEditMultipleIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditMultipleIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutMultiplePeriod.addWidget(self.lineEditMultipleIntermediateConsumptionMatrix, 1, 1)
        
        self.buttonSelectMultipleIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectMultipleIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutMultiplePeriod.addWidget(self.buttonSelectMultipleIntermediateConsumptionMatrix, 1, 2)
        
        self.labelMultipleValueAddedMatrix = QtGui.QLabel()
        self.labelMultipleValueAddedMatrix.setText('Value added matrix:')
        self.layoutMultiplePeriod.addWidget(self.labelMultipleValueAddedMatrix, 2, 0)
        
        self.lineEditMultipleValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditMultipleValueAddedMatrix.setReadOnly(True)
        self.layoutMultiplePeriod.addWidget(self.lineEditMultipleValueAddedMatrix, 2, 1)
        
        self.buttonSelectMultipleValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectMultipleValueAddedMatrix.setText('&Browse')
        self.layoutMultiplePeriod.addWidget(self.buttonSelectMultipleValueAddedMatrix, 2, 2)
        
        self.labelMultipleFinalConsumptionMatrix = QtGui.QLabel()
        self.labelMultipleFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutMultiplePeriod.addWidget(self.labelMultipleFinalConsumptionMatrix, 3, 0)
        
        self.lineEditMultipleFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditMultipleFinalConsumptionMatrix.setReadOnly(True)
        self.layoutMultiplePeriod.addWidget(self.lineEditMultipleFinalConsumptionMatrix, 3, 1)
        
        self.buttonSelectMultipleFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectMultipleFinalConsumptionMatrix.setText('&Browse')
        self.layoutMultiplePeriod.addWidget(self.buttonSelectMultipleFinalConsumptionMatrix, 3, 2)
        
        self.labelMultipleLabourRequirement = QtGui.QLabel()
        self.labelMultipleLabourRequirement.setText('Labour requirement:')
        self.layoutMultiplePeriod.addWidget(self.labelMultipleLabourRequirement, 4, 0)
        
        self.lineEditMultipleLabourRequirement = QtGui.QLineEdit()
        self.lineEditMultipleLabourRequirement.setReadOnly(True)
        self.layoutMultiplePeriod.addWidget(self.lineEditMultipleLabourRequirement, 4, 1)
        
        self.buttonSelectMultipleLabourRequirement = QtGui.QPushButton()
        self.buttonSelectMultipleLabourRequirement.setText('&Browse')
        self.layoutMultiplePeriod.addWidget(self.buttonSelectMultipleLabourRequirement, 4, 2)
        
        # 'Other' GroupBox
        self.groupBoxOther = QtGui.QGroupBox('Other parameters')
        self.layoutGroupBoxOther = QtGui.QVBoxLayout()
        self.layoutGroupBoxOther.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOther.setLayout(self.layoutGroupBoxOther)
        self.layoutOtherInfo = QtGui.QVBoxLayout()
        self.layoutOther = QtGui.QGridLayout()
        self.layoutGroupBoxOther.addLayout(self.layoutOtherInfo)
        self.layoutGroupBoxOther.addLayout(self.layoutOther)
        
        self.labelOtherInfo = QtGui.QLabel()
        self.labelOtherInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOtherInfo.addWidget(self.labelOtherInfo)
        
        self.labelWorkingDir = QtGui.QLabel()
        self.labelWorkingDir.setText('Working directory:')
        self.layoutOther.addWidget(self.labelWorkingDir, 0, 0)
        
        self.lineEditWorkingDir = QtGui.QLineEdit()
        self.lineEditWorkingDir.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditWorkingDir, 0, 1)
        
        self.buttonSelectWorkingDir = QtGui.QPushButton()
        self.buttonSelectWorkingDir.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectWorkingDir, 0, 2)
        
        self.labelValueAddedComponent = QtGui.QLabel()
        self.labelValueAddedComponent.setText('Value added component:')
        self.layoutOther.addWidget(self.labelValueAddedComponent, 1, 0)
        
        self.lineEditValueAddedComponent = QtGui.QLineEdit()
        self.lineEditValueAddedComponent.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditValueAddedComponent, 1, 1)
        
        self.buttonSelectValueAddedComponent = QtGui.QPushButton()
        self.buttonSelectValueAddedComponent.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectValueAddedComponent, 1, 2)
        
        self.labelFinalConsumptionComponent = QtGui.QLabel()
        self.labelFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutOther.addWidget(self.labelFinalConsumptionComponent, 2, 0)
        
        self.lineEditFinalConsumptionComponent = QtGui.QLineEdit()
        self.lineEditFinalConsumptionComponent.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditFinalConsumptionComponent, 2, 1)
        
        self.buttonSelectFinalConsumptionComponent = QtGui.QPushButton()
        self.buttonSelectFinalConsumptionComponent.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectFinalConsumptionComponent, 2, 2)
        
        self.labelListOfEconomicSector = QtGui.QLabel()
        self.labelListOfEconomicSector.setText('List of economic sector:')
        self.layoutOther.addWidget(self.labelListOfEconomicSector, 3, 0)
        
        self.lineEditListOfEconomicSector = QtGui.QLineEdit()
        self.lineEditListOfEconomicSector.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditListOfEconomicSector, 3, 1)
        
        self.buttonSelectListOfEconomicSector = QtGui.QPushButton()
        self.buttonSelectListOfEconomicSector.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectListOfEconomicSector, 3, 2)
        
        self.labelFinancialUnit = QtGui.QLabel()
        self.labelFinancialUnit.setText('Financial &unit:')
        self.layoutOther.addWidget(self.labelFinancialUnit, 4, 0)
        
        self.lineEditFinancialUnit = QtGui.QLineEdit()
        self.lineEditFinancialUnit.setText('Million Rupiah')
        self.layoutOther.addWidget(self.lineEditFinancialUnit, 4, 1)
        self.labelFinancialUnit.setBuddy(self.lineEditFinancialUnit)
        
        self.labelAreaName = QtGui.QLabel()
        self.labelAreaName.setText('&Area name:')
        self.layoutOther.addWidget(self.labelAreaName, 5, 0)
        
        self.lineEditAreaName = QtGui.QLineEdit()
        self.lineEditAreaName.setText('area')
        self.layoutOther.addWidget(self.lineEditAreaName, 5, 1)
        self.labelAreaName.setBuddy(self.lineEditAreaName)
        
        # Process tab button
        self.layoutButtonDescriptiveAnalysis = QtGui.QHBoxLayout()
        self.buttonProcessDescriptiveAnalysis = QtGui.QPushButton()
        self.buttonProcessDescriptiveAnalysis.setText('&Process')
        self.layoutButtonDescriptiveAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonDescriptiveAnalysis.addWidget(self.buttonProcessDescriptiveAnalysis)
        
        # Place the GroupBoxes
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxSinglePeriod)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxMultiplePeriod)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxOther)
        self.layoutContentDescriptiveAnalysis.addLayout(self.layoutButtonDescriptiveAnalysis)
        
        #***********************************************************
        # Setup 'Regional Economic Scenario Impact' tab
        #***********************************************************
        # Use QScrollArea
        self.layoutContentRegionalEconomicScenarioImpact = QtGui.QVBoxLayout()
        self.contentRegionalEconomicScenarioImpact = QtGui.QWidget()
        self.contentRegionalEconomicScenarioImpact.setLayout(self.layoutContentRegionalEconomicScenarioImpact)
        self.scrollRegionalEconomicScenarioImpact = QtGui.QScrollArea()
        self.scrollRegionalEconomicScenarioImpact.setWidgetResizable(True);
        self.scrollRegionalEconomicScenarioImpact.setWidget(self.contentRegionalEconomicScenarioImpact)
        self.layoutTabRegionalEconomicScenarioImpact.addWidget(self.scrollRegionalEconomicScenarioImpact)
        
        # 'Type' GroupBox
        self.groupBoxRegionalEconomicScenarioImpactType = QtGui.QGroupBox('Scenario type')
        self.layoutGroupBoxRegionalEconomicScenarioImpactType = QtGui.QVBoxLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxRegionalEconomicScenarioImpactType.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactType)
        self.layoutRegionalEconomicScenarioImpactTypeInfo = QtGui.QVBoxLayout()
        self.layoutRegionalEconomicScenarioImpactType = QtGui.QGridLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addLayout(self.layoutRegionalEconomicScenarioImpactTypeInfo)
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addLayout(self.layoutRegionalEconomicScenarioImpactType)
        
        self.labelRegionalEconomicScenarioImpactTypeInfo = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactTypeInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutRegionalEconomicScenarioImpactTypeInfo.addWidget(self.labelRegionalEconomicScenarioImpactTypeInfo)
        
        self.radioRegionalEconomicScenarioImpactFinalDemand = QtGui.QRadioButton('Final Demand Scenario')
        self.radioRegionalEconomicScenarioImpactFinalDemand.setChecked(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.radioRegionalEconomicScenarioImpactFinalDemand, 0, 0)
        
        self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText('Final demand change scenario:')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario, 1, 0)
        
        self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario, 1, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario, 1, 2)
        
        self.radioRegionalEconomicScenarioImpactGDP = QtGui.QRadioButton('GDP Scenario')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.radioRegionalEconomicScenarioImpactGDP, 2, 0)
        
        # 'Parameters' GroupBox
        self.groupBoxRegionalEconomicScenarioImpactParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxRegionalEconomicScenarioImpactParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxRegionalEconomicScenarioImpactParameters.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactParameters)
        self.layoutRegionalEconomicScenarioImpactParametersInfo = QtGui.QVBoxLayout()
        self.layoutRegionalEconomicScenarioImpactParameters = QtGui.QGridLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactParameters.addLayout(self.layoutRegionalEconomicScenarioImpactParametersInfo)
        self.layoutGroupBoxRegionalEconomicScenarioImpactParameters.addLayout(self.layoutRegionalEconomicScenarioImpactParameters)
        
        self.labelRegionalEconomicScenarioImpactParametersInfo = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutRegionalEconomicScenarioImpactParametersInfo.addWidget(self.labelRegionalEconomicScenarioImpactParametersInfo)
        
        self.labelRegionalEconomicScenarioImpactWorkingDir = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactWorkingDir.setText('Working directory:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactWorkingDir, 0, 0)
        
        self.lineEditRegionalEconomicScenarioImpactWorkingDir = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactWorkingDir.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactWorkingDir, 0, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactWorkingDir = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactWorkingDir.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactWorkingDir, 0, 2)
        
        self.labelRegionalEconomicScenarioImpactIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactIntermediateConsumptionMatrix, 1, 0)
        
        self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix, 1, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix, 1, 2)
        
        self.labelRegionalEconomicScenarioImpactValueAddedMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactValueAddedMatrix.setText('Value added matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactValueAddedMatrix, 2, 0)
        
        self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix, 2, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactValueAddedMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactValueAddedMatrix, 2, 2)
        
        self.labelRegionalEconomicScenarioImpactFinalConsumptionMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactFinalConsumptionMatrix, 3, 0)
        
        self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix, 3, 1)
        
        self.buttonRegionalEconomicScenarioImpactSelectFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonRegionalEconomicScenarioImpactSelectFinalConsumptionMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonRegionalEconomicScenarioImpactSelectFinalConsumptionMatrix, 3, 2)
        
        self.labelRegionalEconomicScenarioImpactValueAddedComponent = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactValueAddedComponent.setText('Value added component:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactValueAddedComponent, 4, 0)
        
        self.lineEditRegionalEconomicScenarioImpactValueAddedComponent = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactValueAddedComponent.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactValueAddedComponent, 4, 1)
        
        self.buttonRegionalEconomicScenarioImpactSelectValueAddedComponent = QtGui.QPushButton()
        self.buttonRegionalEconomicScenarioImpactSelectValueAddedComponent.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonRegionalEconomicScenarioImpactSelectValueAddedComponent, 4, 2)
        
        self.labelRegionalEconomicScenarioImpactFinalConsumptionComponent = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactFinalConsumptionComponent, 5, 0)
        
        self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent, 5, 1)
        
        self.buttonRegionalEconomicScenarioImpactSelectFinalConsumptionComponent = QtGui.QPushButton()
        self.buttonRegionalEconomicScenarioImpactSelectFinalConsumptionComponent.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonRegionalEconomicScenarioImpactSelectFinalConsumptionComponent, 5, 2)
        
        self.labelRegionalEconomicScenarioImpactListOfEconomicSector = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactListOfEconomicSector.setText('List of economic sector:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactListOfEconomicSector, 6, 0)
        
        self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector, 6, 1)
        
        self.buttonRegionalEconomicScenarioImpactSelectListOfEconomicSector = QtGui.QPushButton()
        self.buttonRegionalEconomicScenarioImpactSelectListOfEconomicSector.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonRegionalEconomicScenarioImpactSelectListOfEconomicSector, 6, 2)
        
        self.labelRegionalEconomicScenarioImpactLandDistributionMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactLandDistributionMatrix.setText('Land distribution matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactLandDistributionMatrix, 7, 0)
        
        self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix, 7, 1)
        
        self.buttonRegionalEconomicScenarioImpactSelectLandDistributionMatrix = QtGui.QPushButton()
        self.buttonRegionalEconomicScenarioImpactSelectLandDistributionMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonRegionalEconomicScenarioImpactSelectLandDistributionMatrix, 7, 2)
        
        self.labelRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.setText('Land requirement coefficient matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix, 8, 0)
        
        self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix, 8, 1)
        
        self.buttonRegionalEconomicScenarioImpactSelectLandRequirementCoefficientMatrix = QtGui.QPushButton()
        self.buttonRegionalEconomicScenarioImpactSelectLandRequirementCoefficientMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonRegionalEconomicScenarioImpactSelectLandRequirementCoefficientMatrix, 8, 2)
        
        self.labelRegionalEconomicScenarioImpactLandCoverComponent = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactLandCoverComponent.setText('Land cover component:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactLandCoverComponent, 9, 0)
        
        self.lineEditRegionalEconomicScenarioImpactLandCoverComponent = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactLandCoverComponent.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactLandCoverComponent, 9, 1)
        
        self.buttonRegionalEconomicScenarioImpactSelectLandCoverComponent = QtGui.QPushButton()
        self.buttonRegionalEconomicScenarioImpactSelectLandCoverComponent.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonRegionalEconomicScenarioImpactSelectLandCoverComponent, 9, 2)
        
        self.labelRegionalEconomicScenarioImpactLabourRequirement = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactLabourRequirement.setText('Labour requirement:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactLabourRequirement, 10, 0)
        
        self.lineEditRegionalEconomicScenarioImpactLabourRequirement = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactLabourRequirement.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactLabourRequirement, 10, 1)
        
        self.buttonRegionalEconomicScenarioImpactSelectLabourRequirement = QtGui.QPushButton()
        self.buttonRegionalEconomicScenarioImpactSelectLabourRequirement.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonRegionalEconomicScenarioImpactSelectLabourRequirement, 10, 2)
        
        self.labelRegionalEconomicScenarioImpactFinancialUnit = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinancialUnit.setText('Financial &unit:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactFinancialUnit, 11, 0)
        
        self.lineEditRegionalEconomicScenarioImpactFinancialUnit = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactFinancialUnit.setText('Million Rupiah')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactFinancialUnit, 11, 1)
        self.labelRegionalEconomicScenarioImpactFinancialUnit.setBuddy(self.lineEditRegionalEconomicScenarioImpactFinancialUnit)
        
        self.labelRegionalEconomicScenarioImpactAreaName = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactAreaName.setText('&Area name:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactAreaName, 12, 0)
        
        self.lineEditRegionalEconomicScenarioImpactAreaName = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactAreaName.setText('area')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactAreaName, 12, 1)
        self.labelRegionalEconomicScenarioImpactAreaName.setBuddy(self.lineEditRegionalEconomicScenarioImpactAreaName)
        
        self.labelRegionalEconomicScenarioImpactSpinBoxPeriod = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactSpinBoxPeriod.setText('&Period:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactSpinBoxPeriod, 13, 0)
        
        self.spinBoxRegionalEconomicScenarioImpactPeriod = QtGui.QSpinBox()
        self.spinBoxRegionalEconomicScenarioImpactPeriod.setRange(1, 9999)
        self.spinBoxRegionalEconomicScenarioImpactPeriod.setValue(td.year)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.spinBoxRegionalEconomicScenarioImpactPeriod, 13, 1)
        self.labelRegionalEconomicScenarioImpactSpinBoxPeriod.setBuddy(self.spinBoxRegionalEconomicScenarioImpactPeriod)
        
        # Process tab button
        self.layoutButtonRegionalEconomicScenarioImpact = QtGui.QHBoxLayout()
        self.buttonProcessRegionalEconomicScenarioImpact = QtGui.QPushButton()
        self.buttonProcessRegionalEconomicScenarioImpact.setText('&Process')
        self.layoutButtonRegionalEconomicScenarioImpact.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonRegionalEconomicScenarioImpact.addWidget(self.buttonProcessRegionalEconomicScenarioImpact)
        
        # Place the GroupBoxes
        self.layoutContentRegionalEconomicScenarioImpact.addWidget(self.groupBoxRegionalEconomicScenarioImpactType)
        self.layoutContentRegionalEconomicScenarioImpact.addWidget(self.groupBoxRegionalEconomicScenarioImpactParameters)
        self.layoutContentRegionalEconomicScenarioImpact.addLayout(self.layoutButtonRegionalEconomicScenarioImpact)
        
        #***********************************************************
        # Setup 'Land Requirement Analysis' tab
        #***********************************************************
        # Use QScrollArea
        self.layoutContentLandRequirementAnalysis = QtGui.QVBoxLayout()
        self.contentLandRequirementAnalysis = QtGui.QWidget()
        self.contentLandRequirementAnalysis.setLayout(self.layoutContentLandRequirementAnalysis)
        self.scrollLandRequirementAnalysis = QtGui.QScrollArea()
        self.scrollLandRequirementAnalysis.setWidgetResizable(True);
        self.scrollLandRequirementAnalysis.setWidget(self.contentLandRequirementAnalysis)
        self.layoutTabLandRequirementAnalysis.addWidget(self.scrollLandRequirementAnalysis)
        
        # Parameters 'GroupBox'
        self.groupBoxLandRequirementAnalysisParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxLandRequirementAnalysisParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandRequirementAnalysisParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandRequirementAnalysisParameters.setLayout(self.layoutGroupBoxLandRequirementAnalysisParameters)
        self.layoutLandRequirementAnalysisParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandRequirementAnalysisParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandRequirementAnalysisParameters.addLayout(self.layoutLandRequirementAnalysisParametersInfo)
        self.layoutGroupBoxLandRequirementAnalysisParameters.addLayout(self.layoutLandRequirementAnalysisParameters)
        
        self.labelLandRequirementAnalysisParametersInfo = QtGui.QLabel()
        self.labelLandRequirementAnalysisParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandRequirementAnalysisParametersInfo.addWidget(self.labelLandRequirementAnalysisParametersInfo)
        
        self.labelLandRequirementAnalysisWorkingDir = QtGui.QLabel()
        self.labelLandRequirementAnalysisWorkingDir.setText('Working directory:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisWorkingDir, 0, 0)
        
        self.lineEditLandRequirementAnalysisWorkingDir = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisWorkingDir.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisWorkingDir, 0, 1)
        
        self.buttonSelectLandRequirementAnalysisWorkingDir = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisWorkingDir.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisWorkingDir, 0, 2)
        
        self.labelLandRequirementAnalysisLandCoverMap = QtGui.QLabel()
        self.labelLandRequirementAnalysisLandCoverMap.setText('Land cover map:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLandCoverMap, 1, 0)
        
        self.lineEditLandRequirementAnalysisLandCoverMap = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisLandCoverMap.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisLandCoverMap, 1, 1)
        
        self.buttonSelectLandRequirementAnalysisLandCoverMap = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisLandCoverMap.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisLandCoverMap, 1, 2)
        
        self.labelLandRequirementAnalysisIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelLandRequirementAnalysisIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisIntermediateConsumptionMatrix, 2, 0)
        
        self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix, 2, 1)
        
        self.buttonSelectLandRequirementAnalysisIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisIntermediateConsumptionMatrix, 2, 2)
        
        self.labelLandRequirementAnalysisValueAddedMatrix = QtGui.QLabel()
        self.labelLandRequirementAnalysisValueAddedMatrix.setText('Value added matrix:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisValueAddedMatrix, 3, 0)
        
        self.lineEditLandRequirementAnalysisValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisValueAddedMatrix.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisValueAddedMatrix, 3, 1)
        
        self.buttonSelectLandRequirementAnalysisValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisValueAddedMatrix.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisValueAddedMatrix, 3, 2)
        
        self.labelLandRequirementAnalysisFinalConsumptionMatrix = QtGui.QLabel()
        self.labelLandRequirementAnalysisFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisFinalConsumptionMatrix, 4, 0)
        
        self.lineEditLandRequirementAnalysisFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisFinalConsumptionMatrix.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisFinalConsumptionMatrix, 4, 1)
        
        self.buttonSelectLandRequirementAnalysisFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisFinalConsumptionMatrix.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisFinalConsumptionMatrix, 4, 2)
        
        self.labelLandRequirementAnalysisValueAddedComponent = QtGui.QLabel()
        self.labelLandRequirementAnalysisValueAddedComponent.setText('Value added component:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisValueAddedComponent, 5, 0)
        
        self.lineEditLandRequirementAnalysisValueAddedComponent = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisValueAddedComponent.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisValueAddedComponent, 5, 1)
        
        self.buttonSelectLandRequirementAnalysisValueAddedComponent = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisValueAddedComponent.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisValueAddedComponent, 5, 2)
        
        self.labelLandRequirementAnalysisFinalConsumptionComponent = QtGui.QLabel()
        self.labelLandRequirementAnalysisFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisFinalConsumptionComponent, 6, 0)
        
        self.lineEditLandRequirementAnalysisFinalConsumptionComponent = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisFinalConsumptionComponent.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisFinalConsumptionComponent, 6, 1)
        
        self.buttonSelectLandRequirementAnalysisFinalConsumptionComponent = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisFinalConsumptionComponent.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisFinalConsumptionComponent, 6, 2)
        
        self.labelLandRequirementAnalysisListOfEconomicSector = QtGui.QLabel()
        self.labelLandRequirementAnalysisListOfEconomicSector.setText('List of economic sector:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisListOfEconomicSector, 7, 0)
        
        self.lineEditLandRequirementAnalysisListOfEconomicSector = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisListOfEconomicSector.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisListOfEconomicSector, 7, 1)
        
        self.buttonSelectLandRequirementAnalysisListOfEconomicSector = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisListOfEconomicSector.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisListOfEconomicSector, 7, 2)
        
        self.labelLandRequirementAnalysisLandDistributionMatrix = QtGui.QLabel()
        self.labelLandRequirementAnalysisLandDistributionMatrix.setText('Land distribution matrix:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLandDistributionMatrix, 8, 0)
        
        self.lineEditLandRequirementAnalysisLandDistributionMatrix = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisLandDistributionMatrix.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisLandDistributionMatrix, 8, 1)
        
        self.buttonSelectLandRequirementAnalysisLandDistributionMatrix = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisLandDistributionMatrix.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisLandDistributionMatrix, 8, 2)
        
        self.labelLandRequirementAnalysisLandCoverComponent = QtGui.QLabel()
        self.labelLandRequirementAnalysisLandCoverComponent.setText('Land cover component:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLandCoverComponent, 9, 0)
        
        self.lineEditLandRequirementAnalysisLandCoverComponent = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisLandCoverComponent.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisLandCoverComponent, 9, 1)
        
        self.buttonSelectLandRequirementAnalysisLandCoverComponent = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisLandCoverComponent.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisLandCoverComponent, 9, 2)
        
        self.labelLandRequirementAnalysisLabourRequirement = QtGui.QLabel()
        self.labelLandRequirementAnalysisLabourRequirement.setText('Labour requirement:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLabourRequirement, 10, 0)
        
        self.lineEditLandRequirementAnalysisLabourRequirement = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisLabourRequirement.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisLabourRequirement, 10, 1)
        
        self.buttonSelectLandRequirementAnalysisLabourRequirement = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisLabourRequirement.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisLabourRequirement, 10, 2)
        
        self.labelLandRequirementAnalysisFinancialUnit = QtGui.QLabel()
        self.labelLandRequirementAnalysisFinancialUnit.setText('Financial &unit:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisFinancialUnit, 11, 0)
        
        self.lineEditLandRequirementAnalysisFinancialUnit = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisFinancialUnit.setText('Million Rupiah')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisFinancialUnit, 11, 1)
        
        self.labelLandRequirementAnalysisFinancialUnit.setBuddy(self.lineEditLandRequirementAnalysisFinancialUnit)
        
        self.labelLandRequirementAnalysisAreaName = QtGui.QLabel()
        self.labelLandRequirementAnalysisAreaName.setText('&Area name:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisAreaName, 12, 0)
        
        self.lineEditLandRequirementAnalysisAreaName = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisAreaName.setText('area')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisAreaName, 12, 1)
        self.labelLandRequirementAnalysisAreaName.setBuddy(self.lineEditLandRequirementAnalysisAreaName)
        
        self.labelLandRequirementAnalysisPeriod = QtGui.QLabel()
        self.labelLandRequirementAnalysisPeriod.setText('&Period:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisPeriod, 13, 0)
        
        self.spinBoxLandRequirementAnalysisPeriod = QtGui.QSpinBox()
        self.spinBoxLandRequirementAnalysisPeriod.setRange(1, 9999)
        self.spinBoxLandRequirementAnalysisPeriod.setValue(td.year)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.spinBoxLandRequirementAnalysisPeriod, 13, 1)
        self.labelLandRequirementAnalysisPeriod.setBuddy(self.spinBoxLandRequirementAnalysisPeriod)
            
        # Process tab button
        self.layoutButtonLandRequirementAnalysis = QtGui.QHBoxLayout()
        self.buttonProcessLandRequirementAnalysis = QtGui.QPushButton()
        self.buttonProcessLandRequirementAnalysis.setText('&Process')
        self.layoutButtonLandRequirementAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLandRequirementAnalysis.addWidget(self.buttonProcessLandRequirementAnalysis)
        
        # Place the GroupBoxes
        self.layoutContentLandRequirementAnalysis.addWidget(self.groupBoxLandRequirementAnalysisParameters)
        self.layoutContentLandRequirementAnalysis.addLayout(self.layoutButtonLandRequirementAnalysis)
        
        #***********************************************************
        # Setup 'Land Use Change Impact' tab
        #***********************************************************
        # Use QScrollArea
        self.layoutContentLandUseChangeImpact = QtGui.QVBoxLayout()
        self.contentLandUseChangeImpact = QtGui.QWidget()
        self.contentLandUseChangeImpact.setLayout(self.layoutContentLandUseChangeImpact)
        self.scrollLandUseChangeImpact = QtGui.QScrollArea()
        self.scrollLandUseChangeImpact.setWidgetResizable(True);
        self.scrollLandUseChangeImpact.setWidget(self.contentLandUseChangeImpact)
        self.layoutTabLandUseChangeImpact.addWidget(self.scrollLandUseChangeImpact)
        
        # Parameters 'GroupBox'
        self.groupBoxLandUseChangeImpactParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxLandUseChangeImpactParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeImpactParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeImpactParameters.setLayout(self.layoutGroupBoxLandUseChangeImpactParameters)
        self.layoutLandUseChangeImpactParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeImpactParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeImpactParameters.addLayout(self.layoutLandUseChangeImpactParametersInfo)
        self.layoutGroupBoxLandUseChangeImpactParameters.addLayout(self.layoutLandUseChangeImpactParameters)
        
        self.labelLandUseChangeImpactParametersInfo = QtGui.QLabel()
        self.labelLandUseChangeImpactParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseChangeImpactParametersInfo.addWidget(self.labelLandUseChangeImpactParametersInfo)
        
        self.labelLandUseChangeImpactWorkingDir = QtGui.QLabel()
        self.labelLandUseChangeImpactWorkingDir.setText('Working directory:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactWorkingDir, 0, 0)
        
        self.lineEditLandUseChangeImpactWorkingDir = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactWorkingDir.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactWorkingDir, 0, 1)
        
        self.buttonSelectLandUseChangeImpactWorkingDir = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactWorkingDir.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactWorkingDir, 0, 2)
        
        self.labelLandUseChangeImpactLandCoverMapP1 = QtGui.QLabel()
        self.labelLandUseChangeImpactLandCoverMapP1.setText('Land cover map period 1:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLandCoverMapP1, 1, 0)
        
        self.lineEditLandUseChangeImpactLandCoverMapP1 = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLandCoverMapP1.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLandCoverMapP1, 1, 1)
        
        self.buttonSelectLandUseChangeImpactLandCoverMapP1 = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLandCoverMapP1.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLandCoverMapP1, 1, 2)
        
        self.labelLandUseChangeImpactLandCoverMapP2 = QtGui.QLabel()
        self.labelLandUseChangeImpactLandCoverMapP2.setText('Land cover map period 2:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLandCoverMapP2, 2, 0)
        
        self.lineEditLandUseChangeImpactLandCoverMapP2 = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLandCoverMapP2.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLandCoverMapP2, 2, 1)
        
        self.buttonSelectLandUseChangeImpactLandCoverMapP2 = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLandCoverMapP2.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLandCoverMapP2, 2, 2)
        
        self.labelLandUseChangeImpactIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactIntermediateConsumptionMatrix, 3, 0)
        
        self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix, 3, 1)
        
        self.buttonSelectLandUseChangeImpactIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactIntermediateConsumptionMatrix, 3, 2)
        
        self.labelLandUseChangeImpactValueAddedMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactValueAddedMatrix.setText('Value added matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactValueAddedMatrix, 4, 0)
        
        self.lineEditLandUseChangeImpactValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactValueAddedMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactValueAddedMatrix, 4, 1)
        
        self.buttonSelectLandUseChangeImpactValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactValueAddedMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactValueAddedMatrix, 4, 2)
        
        self.labelLandUseChangeImpactFinalConsumptionMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactFinalConsumptionMatrix, 5, 0)
        
        self.lineEditLandUseChangeImpactFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactFinalConsumptionMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactFinalConsumptionMatrix, 5, 1)
        
        self.buttonSelectLandUseChangeImpactFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactFinalConsumptionMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactFinalConsumptionMatrix, 5, 2)
        
        self.labelLandUseChangeImpactValueAddedComponent = QtGui.QLabel()
        self.labelLandUseChangeImpactValueAddedComponent.setText('Value added component:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactValueAddedComponent, 6, 0)
        
        self.lineEditLandUseChangeImpactValueAddedComponent = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactValueAddedComponent.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactValueAddedComponent, 6, 1)
        
        self.buttonSelectLandUseChangeImpactValueAddedComponent = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactValueAddedComponent.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactValueAddedComponent, 6, 2)
        
        self.labelLandUseChangeImpactFinalConsumptionComponent = QtGui.QLabel()
        self.labelLandUseChangeImpactFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactFinalConsumptionComponent, 7, 0)
        
        self.lineEditLandUseChangeImpactFinalConsumptionComponent = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactFinalConsumptionComponent.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactFinalConsumptionComponent, 7, 1)
        
        self.buttonSelectLandUseChangeImpactFinalConsumptionComponent = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactFinalConsumptionComponent.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactFinalConsumptionComponent, 7, 2)
        
        self.labelLandUseChangeImpactListOfEconomicSector = QtGui.QLabel()
        self.labelLandUseChangeImpactListOfEconomicSector.setText('List of economic sector:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactListOfEconomicSector, 8, 0)
        
        self.lineEditLandUseChangeImpactListOfEconomicSector = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactListOfEconomicSector.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactListOfEconomicSector, 8, 1)
        
        self.buttonSelectLandUseChangeImpactListOfEconomicSector = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactListOfEconomicSector.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactListOfEconomicSector, 8, 2)
        
        self.labelLandUseChangeImpactLandDistributionMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactLandDistributionMatrix.setText('Land distribution matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLandDistributionMatrix, 9, 0)
        
        self.lineEditLandUseChangeImpactLandDistributionMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLandDistributionMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLandDistributionMatrix, 9, 1)
        
        self.buttonSelectLandUseChangeImpactLandDistributionMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLandDistributionMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLandDistributionMatrix, 9, 2)
        
        self.labelLandUseChangeImpactLandRequirementCoefficientMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactLandRequirementCoefficientMatrix.setText('Land requirement coefficient matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLandRequirementCoefficientMatrix, 10, 0)
        
        self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix, 10, 1)
        
        self.buttonSelectLandUseChangeImpactLandRequirementCoefficientMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLandRequirementCoefficientMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLandRequirementCoefficientMatrix, 10, 2)
        
        self.labelLandUseChangeImpactLandCoverComponent = QtGui.QLabel()
        self.labelLandUseChangeImpactLandCoverComponent.setText('Land cover component:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLandCoverComponent, 11, 0)
        
        self.lineEditLandUseChangeImpactLandCoverComponent = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLandCoverComponent.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLandCoverComponent, 11, 1)
        
        self.buttonSelectLandUseChangeImpactLandCoverComponent = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLandCoverComponent.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLandCoverComponent, 11, 2)
        
        self.labelLandUseChangeImpactLabourRequirement = QtGui.QLabel()
        self.labelLandUseChangeImpactLabourRequirement.setText('Labour requirement:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLabourRequirement, 12, 0)
        
        self.lineEditLandUseChangeImpactLabourRequirement = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLabourRequirement.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLabourRequirement, 12, 1)
        
        self.buttonSelectLandUseChangeImpactLabourRequirement = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLabourRequirement.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLabourRequirement, 12, 2)
        
        self.labelLandUseChangeImpactFinancialUnit = QtGui.QLabel()
        self.labelLandUseChangeImpactFinancialUnit.setText('Financial &unit:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactFinancialUnit, 13, 0)
        
        self.lineEditLandUseChangeImpactFinancialUnit = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactFinancialUnit.setText('Million Rupiah')
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactFinancialUnit, 13, 1)
        self.labelLandUseChangeImpactFinancialUnit.setBuddy(self.lineEditLandUseChangeImpactFinancialUnit)
        
        self.labelLandUseChangeImpactAreaName = QtGui.QLabel()
        self.labelLandUseChangeImpactAreaName.setText('&Area name:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactAreaName, 14, 0)
        
        self.lineEditLandUseChangeImpactAreaName = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactAreaName.setText('area')
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactAreaName, 14, 1)
        self.labelLandUseChangeImpactAreaName.setBuddy(self.lineEditLandUseChangeImpactAreaName)
        
        self.labelLandUseChangeImpactPeriod = QtGui.QLabel()
        self.labelLandUseChangeImpactPeriod.setText('&Period:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactPeriod, 15, 0)
        
        self.spinBoxLandUseChangeImpactPeriod = QtGui.QSpinBox()
        self.spinBoxLandUseChangeImpactPeriod.setRange(1, 9999)
        self.spinBoxLandUseChangeImpactPeriod.setValue(td.year)
        self.layoutLandUseChangeImpactParameters.addWidget(self.spinBoxLandUseChangeImpactPeriod, 15, 1)
        self.labelLandUseChangeImpactPeriod.setBuddy(self.spinBoxLandUseChangeImpactPeriod)
        
        # Process tab button
        self.layoutButtonLandUseChangeImpact = QtGui.QHBoxLayout()
        self.buttonProcessLandUseChangeImpact = QtGui.QPushButton()
        self.buttonProcessLandUseChangeImpact.setText('&Process')
        self.layoutButtonLandUseChangeImpact.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLandUseChangeImpact.addWidget(self.buttonProcessLandUseChangeImpact)
        
        # Place the GroupBoxes
        self.layoutContentLandUseChangeImpact.addWidget(self.groupBoxLandUseChangeImpactParameters)
        self.layoutContentLandUseChangeImpact.addLayout(self.layoutButtonLandUseChangeImpact)
        
        #***********************************************************
        # Setup 'Result' tab
        #***********************************************************
        
        
        #***********************************************************
        # Setup 'Report' tab
        #***********************************************************
        
        
        #***********************************************************
        # Setup 'Log' tab
        #***********************************************************
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 600)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensTARegionalEconomy, self).showEvent(event)
    
    
    def toggleMultiplePeriod(self, checked):
        """
        """
        if checked:
            self.contentOptionsMultiplePeriod.setEnabled(True)
        else:
            self.contentOptionsMultiplePeriod.setDisabled(True)
    
    
    def toggleRegionalEconomicScenarioImpactType(self, radio):
        """
        """
        if radio.text() == 'Final Demand Scenario':
            self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario.setEnabled(True)
            self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setEnabled(True)
            self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario.setEnabled(True)
        elif radio.text() == 'GDP Scenario': 
            self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario.setDisabled(True)
            self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setDisabled(True)
            self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario.setDisabled(True)
    