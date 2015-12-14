#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
##from qgis.core import *
##from processing.tools import *
from PyQt4 import QtCore, QtGui
import resource


class DialogLumensSCIENDO(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDO, self).__init__(parent)
        print 'DEBUG: DialogLumensSCIENDO init'
        
        self.main = parent
        self.dialogTitle = 'LUMENS SCIENDO Low Emission Development Analysis'
        
        self.setupUi(self)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabLandUseChangeModeling = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        self.tabReport = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabLandUseChangeModeling, 'Land Use Change Modeling')
        self.tabWidget.addTab(self.tabResult, 'Result')
        self.tabWidget.addTab(self.tabReport, 'Report')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        self.layoutTabLandUseChangeModeling = QtGui.QVBoxLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        self.layoutTabReport = QtGui.QVBoxLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabLandUseChangeModeling.setLayout(self.layoutTabLandUseChangeModeling)
        self.tabResult.setLayout(self.layoutTabResult)
        self.tabReport.setLayout(self.layoutTabReport)
        self.tabLog.setLayout(self.layoutTabLog)
        
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Land Use Change Modeling' tab
        #***********************************************************
        # 'Functions' GroupBox
        self.groupBoxLandUseChangeModelingFunctions = QtGui.QGroupBox('Functions')
        self.layoutGroupBoxLandUseChangeModelingFunctions = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeModelingFunctions.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeModelingFunctions.setLayout(self.layoutGroupBoxLandUseChangeModelingFunctions)
        self.layoutLandUseChangeModelingFunctionsInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeModelingFunctions = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeModelingFunctions.addLayout(self.layoutLandUseChangeModelingFunctionsInfo)
        self.layoutGroupBoxLandUseChangeModelingFunctions.addLayout(self.layoutLandUseChangeModelingFunctions)
        
        self.labelLandUseChangeModelingFunctionsInfo = QtGui.QLabel()
        self.labelLandUseChangeModelingFunctionsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseChangeModelingFunctionsInfo.addWidget(self.labelLandUseChangeModelingFunctionsInfo)
        
        self.checkBoxCalculateTransitionMatrix = QtGui.QCheckBox('Calculate transition matrix')
        self.checkBoxCreateRasterCubeOfFactors = QtGui.QCheckBox('Create raster cuve of factors')
        self.checkBoxCalculateWeightOfEvidence = QtGui.QCheckBox('Calculate weight of evidence')
        self.checkBoxSimulateLandUseChange = QtGui.QCheckBox('Simulate land use change')
        self.checkBoxSimulateWithScenario = QtGui.QCheckBox('Simulate with scenario')
        
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCalculateTransitionMatrix)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCreateRasterCubeOfFactors)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCalculateWeightOfEvidence)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxSimulateLandUseChange)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxSimulateWithScenario)
        
        # 'Parameters' GroupBox
        self.groupBoxLandUseChangeModelingParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxLandUseChangeModelingParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeModelingParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeModelingParameters.setLayout(self.layoutGroupBoxLandUseChangeModelingParameters)
        self.layoutLandUseChangeModelingParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeModelingParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeModelingParameters.addLayout(self.layoutLandUseChangeModelingParametersInfo)
        self.layoutGroupBoxLandUseChangeModelingParameters.addLayout(self.layoutLandUseChangeModelingParameters)
        
        self.labelLandUseChangeModelingParametersInfo = QtGui.QLabel()
        self.labelLandUseChangeModelingParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseChangeModelingParametersInfo.addWidget(self.labelLandUseChangeModelingParametersInfo)
        
        self.labelLandUseChangeModelingFactorsDir = QtGui.QLabel()
        self.labelLandUseChangeModelingFactorsDir.setText('Factors directory:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingFactorsDir, 0, 0)
        
        self.lineEditLandUseChangeModelingFactorsDir = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingFactorsDir.setReadOnly(True)
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingFactorsDir, 0, 1)
        
        self.buttonSelectLandUseChangeModelingFactorsDir = QtGui.QPushButton()
        self.buttonSelectLandUseChangeModelingFactorsDir.setText('&Browse')
        self.layoutLandUseChangeModelingParameters.addWidget(self.buttonSelectLandUseChangeModelingFactorsDir, 0, 2)
        
        self.labelLandUseChangeModelingLandUseLookup = QtGui.QLabel()
        self.labelLandUseChangeModelingLandUseLookup.setText('Land use lookup table:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingLandUseLookup, 1, 0)
        
        self.lineEditLandUseChangeModelingLandUseLookup = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingLandUseLookup.setReadOnly(True)
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingLandUseLookup, 1, 1)
        
        self.buttonSelectLandUseChangeModelingLandUseLookup = QtGui.QPushButton()
        self.buttonSelectLandUseChangeModelingLandUseLookup.setText('&Browse')
        self.layoutLandUseChangeModelingParameters.addWidget(self.buttonSelectLandUseChangeModelingLandUseLookup, 1, 2)
        
        self.labelLandUseChangeModelingBaseYear = QtGui.QLabel()
        self.labelLandUseChangeModelingBaseYear.setText('Base &year:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingBaseYear, 2, 0)
        
        self.spinBoxLandUseChangeModelingBaseYear = QtGui.QSpinBox()
        self.spinBoxLandUseChangeModelingBaseYear.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxLandUseChangeModelingBaseYear.setValue(td.year)
        self.layoutLandUseChangeModelingParameters.addWidget(self.spinBoxLandUseChangeModelingBaseYear, 2, 1)
        self.labelLandUseChangeModelingBaseYear.setBuddy(self.spinBoxLandUseChangeModelingBaseYear)
        
        self.labelLandUseChangeModelingLocation = QtGui.QLabel()
        self.labelLandUseChangeModelingLocation.setText('Location:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingLocation, 3, 0)
        
        self.lineEditLandUseChangeModelingLocation = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingLocation.setText('location')
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingLocation, 3, 1)
        self.labelLandUseChangeModelingLocation.setBuddy(self.lineEditLandUseChangeModelingLocation)
        
        # Process tab button
        self.layoutButtonLandUseChangeModeling = QtGui.QHBoxLayout()
        self.buttonProcessLandUseChangeModeling = QtGui.QPushButton()
        self.buttonProcessLandUseChangeModeling.setText('&Process')
        self.layoutButtonLandUseChangeModeling.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLandUseChangeModeling.addWidget(self.buttonProcessLandUseChangeModeling)
        
        # Place the GroupBoxes
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeModelingFunctions)
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeModelingParameters)
        self.layoutTabLandUseChangeModeling.addLayout(self.layoutButtonLandUseChangeModeling)
        
        #***********************************************************
        # Setup 'Result' tab
        #***********************************************************
        
        
        #***********************************************************
        # Setup 'Report' tab
        #***********************************************************
        self.tabReport.setLayout(self.layoutTabReport)
        
        #***********************************************************
        # Setup 'Log' tab
        #***********************************************************
        self.tabLog.setLayout(self.layoutTabLog)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensSCIENDO, self).showEvent(event)
    