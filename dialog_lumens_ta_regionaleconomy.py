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
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabDescriptiveAnalysis = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        self.tabReport = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabDescriptiveAnalysis, 'Descriptive Analysis of Regional Economy')
        self.tabWidget.addTab(self.tabResult, 'Result')
        self.tabWidget.addTab(self.tabReport, 'Report')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        self.layoutTabDescriptiveAnalysis = QtGui.QVBoxLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        self.layoutTabReport = QtGui.QVBoxLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabDescriptiveAnalysis.setLayout(self.layoutTabDescriptiveAnalysis)
        self.tabResult.setLayout(self.layoutTabResult)
        self.tabReport.setLayout(self.layoutTabReport)
        self.tabLog.setLayout(self.layoutTabLog)
        
        self.dialogLayout.addWidget(self.tabWidget)
        
        self.layoutContentDescriptiveAnalysis = QtGui.QVBoxLayout()
        self.contentDescriptiveAnalysis = QtGui.QWidget()
        self.contentDescriptiveAnalysis.setLayout(self.layoutContentDescriptiveAnalysis)
        self.scrollDescriptiveAnalysis = QtGui.QScrollArea()
        self.scrollDescriptiveAnalysis.setWidgetResizable(True);
        self.scrollDescriptiveAnalysis.setWidget(self.contentDescriptiveAnalysis)
        self.layoutTabDescriptiveAnalysis.addWidget(self.scrollDescriptiveAnalysis)
        
        #***********************************************************
        # Setup 'Descriptive Analysis of Regional Economy' tab
        #***********************************************************
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
        
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxSinglePeriod)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxMultiplePeriod)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxOther)
        self.layoutContentDescriptiveAnalysis.addLayout(self.layoutButtonDescriptiveAnalysis)
        
        
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
    