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
    def loadSettings(self, tabName, fileName):
        """
        """
        settingsFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'], fileName)
        settings = QtCore.QSettings(settingsFilePath, QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        
        dialogsToLoad = None
        
        if tabName == 'Low Emission Development Analysis':
            dialogsToLoad = (
                'DialogLumensSCIENDOHistoricalBaselineProjection',
                'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                'DialogLumensSCIENDODriversAnalysis',
                'DialogLumensSCIENDOBuildScenario',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Historical baseline projection' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOHistoricalBaselineProjection')
            
            workingDir = settings.value('workingDir')
            QUESCDatabase = settings.value('QUESCDatabase')
            t1 = settings.value('t1')
            t2 = settings.value('t2')
            iteration = settings.value('iteration')
            
            if workingDir and os.path.isdir(workingDir):
                self.lineEditHistoricalBaselineProjectionWorkingDir.setText(workingDir)
            if QUESCDatabase and os.path.exists(QUESCDatabase):
                self.lineEditHistoricalBaselineProjectionQUESCDatabase.setText(QUESCDatabase)
            if t1:
                self.spinBoxHistoricalBaselineProjectionT1.setValue(int(t1))
            if t2:
                self.spinBoxHistoricalBaselineProjectionT2.setValue(int(t2))
            if iteration:
                self.spinBoxHistoricalBaselineProjectionIteration.setValue(int(iteration))
            
            settings.endGroup()
            # /dialog
            
            # 'Historical baseline annual projection' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOHistoricalBaselineAnnualProjection')
            
            iteration = settings.value('iteration')
            
            if iteration:
                self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(int(iteration))
            
            settings.endGroup()
            # /dialog
            
            # 'Drivers analysis' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDODriversAnalysis')
            
            landUseCoverChangeDrivers = settings.value('landUseCoverChangeDrivers')
            landUseCoverChangeType = settings.value('landUseCoverChangeType')
            
            if landUseCoverChangeDrivers and os.path.exists(landUseCoverChangeDrivers):
                self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText(landUseCoverChangeDrivers)
            if landUseCoverChangeType:
                self.lineEditDriversAnalysisLandUseCoverChangeType.setText(landUseCoverChangeType)
            
            settings.endGroup()
            # /dialog
            
            # 'Build scenario' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOBuildScenario')
            
            historicalBaselineCar = settings.value('historicalBaselineCar')
            
            if historicalBaselineCar and os.path.exists(historicalBaselineCar):
                self.lineEditBuildScenarioHistoricalBaselineCar.setText(historicalBaselineCar)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Land Use Change Modeling':
            dialogsToLoad = (
                'DialogLumensSCIENDOCalculateTransitionMatrix',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Land Use Change Modeling' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOCalculateTransitionMatrix')
            
            factorsDir = settings.value('factorsDir')
            landUseLookup = settings.value('landUseLookup')
            baseYear = settings.value('baseYear')
            location = settings.value('location')
            
            if factorsDir and os.path.isdir(factorsDir):
                self.lineEditLandUseChangeModelingFactorsDir.setText(factorsDir)
            if landUseLookup and os.path.exists(landUseLookup):
                self.lineEditLandUseChangeModelingLandUseLookup.setText(landUseLookup)
            if baseYear:
                self.spinBoxLandUseChangeModelingBaseYear.setValue(int(baseYear))
            if location:
                self.lineEditLandUseChangeModelingLocation.setText(location)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        
        print 'DEBUG'
        settings.beginGroup(tabName)
        for dialog in dialogsToLoad:
            settings.beginGroup(dialog)
            for key in self.main.appSettings[dialog].keys():
                print key, settings.value(key)
            settings.endGroup()
        settings.endGroup()
    
    
    def saveSettings(self, tabName, fileName):
        """Save form values according to their tab and dialog
        """
        self.setAppSettings()
        settingsFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'], fileName)
        settings = QtCore.QSettings(settingsFilePath, QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        
        dialogsToSave = None
        
        if tabName == 'Low Emission Development Analysis':
            dialogsToSave = (
                'DialogLumensSCIENDOHistoricalBaselineProjection',
                'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                'DialogLumensSCIENDODriversAnalysis',
                'DialogLumensSCIENDOBuildScenario',
            )
        elif tabName == 'Land Use Change Modeling':
            dialogsToSave = (
                'DialogLumensSCIENDOCalculateTransitionMatrix',
            )
        
        settings.beginGroup(tabName)
        for dialog in dialogsToSave:
            settings.beginGroup(dialog)
            for key, val in self.main.appSettings[dialog].iteritems():
                settings.setValue(key, val)
            settings.endGroup()
        settings.endGroup()
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDO, self).__init__(parent)
        print 'DEBUG: DialogLumensSCIENDO init'
        
        self.main = parent
        self.dialogTitle = 'LUMENS SCIENDO'
        
        self.setupUi(self)
        
        print 'DEBUG'
        self.loadSettings('Low Emission Development Analysis', 'mysettings.ini')
        self.loadSettings('Land Use Change Modeling', 'mysettings.ini')
        
        # 'Low Emission Development Analysis' tab checkboxes
        self.checkBoxHistoricalBaselineProjection.toggled.connect(self.toggleHistoricalBaselineProjection)
        self.checkBoxHistoricalBaselineAnnualProjection.toggled.connect(self.toggleHistoricalBaselineAnnualProjection)
        self.checkBoxDriversAnalysis.toggled.connect(self.toggleDriversAnalysis)
        self.checkBoxBuildScenario.toggled.connect(self.toggleBuildScenario)
        
        # 'Low Emission Development Analysis' tab buttons
        self.buttonSelectHistoricalBaselineProjectionWorkingDir.clicked.connect(self.handlerSelectHistoricalBaselineProjectionWorkingDir)
        self.buttonSelectHistoricalBaselineProjectionQUESCDatabase.clicked.connect(self.handlerSelectHistoricalBaselineProjectionQUESCDatabase)
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers.clicked.connect(self.handlerSelectDriversAnalysisLandUseCoverChangeDrivers)
        self.buttonSelectBuildScenarioHistoricalBaselineCar.clicked.connect(self.handlerSelectBuildScenarioHistoricalBaselineCar)
        self.buttonProcessLowEmissionDevelopmentAnalysis.clicked.connect(self.handlerProcessLowEmissionDevelopmentAnalysis)
        
        # 'Land Use Change Modeling' tab buttons
        self.buttonSelectLandUseChangeModelingFactorsDir.clicked.connect(self.handlerSelectLandUseChangeModelingFactorsDir)
        self.buttonSelectLandUseChangeModelingLandUseLookup.clicked.connect(self.handlerSelectLandUseChangeModelingLandUseLookup)
        self.buttonProcessLandUseChangeModeling.clicked.connect(self.handlerProcessLandUseChangeModeling)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabLowEmissionDevelopmentAnalysis = QtGui.QWidget()
        self.tabLandUseChangeModeling = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        self.tabReport = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabLowEmissionDevelopmentAnalysis, 'Low Emission Development Analysis')
        self.tabWidget.addTab(self.tabLandUseChangeModeling, 'Land Use Change Modeling')
        self.tabWidget.addTab(self.tabResult, 'Result')
        self.tabWidget.addTab(self.tabReport, 'Report')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QVBoxLayout()
        self.layoutTabLandUseChangeModeling = QtGui.QVBoxLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        self.layoutTabReport = QtGui.QVBoxLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabLowEmissionDevelopmentAnalysis.setLayout(self.layoutTabLowEmissionDevelopmentAnalysis)
        self.tabLandUseChangeModeling.setLayout(self.layoutTabLandUseChangeModeling)
        self.tabResult.setLayout(self.layoutTabResult)
        self.tabReport.setLayout(self.layoutTabReport)
        self.tabLog.setLayout(self.layoutTabLog)
        
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Low Emission Development Analysis' tab
        #***********************************************************
        # 'Historical baseline projection' GroupBox
        self.groupBoxHistoricalBaselineProjection = QtGui.QGroupBox('Historical baseline projection')
        self.layoutGroupBoxHistoricalBaselineProjection = QtGui.QHBoxLayout()
        self.groupBoxHistoricalBaselineProjection.setLayout(self.layoutGroupBoxHistoricalBaselineProjection)
        self.layoutOptionsHistoricalBaselineProjection = QtGui.QVBoxLayout()
        self.layoutOptionsHistoricalBaselineProjection.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsHistoricalBaselineProjection = QtGui.QWidget()
        self.contentOptionsHistoricalBaselineProjection.setLayout(self.layoutOptionsHistoricalBaselineProjection)
        self.layoutOptionsHistoricalBaselineProjection.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxHistoricalBaselineProjection = QtGui.QCheckBox()
        self.checkBoxHistoricalBaselineProjection.setChecked(False)
        self.contentOptionsHistoricalBaselineProjection.setDisabled(True)
        self.layoutGroupBoxHistoricalBaselineProjection.addWidget(self.checkBoxHistoricalBaselineProjection)
        self.layoutGroupBoxHistoricalBaselineProjection.addWidget(self.contentOptionsHistoricalBaselineProjection)
        self.layoutGroupBoxHistoricalBaselineProjection.setAlignment(self.checkBoxHistoricalBaselineProjection, QtCore.Qt.AlignTop)
        self.layoutHistoricalBaselineProjectionInfo = QtGui.QVBoxLayout()
        self.layoutHistoricalBaselineProjection = QtGui.QGridLayout()
        self.layoutOptionsHistoricalBaselineProjection.addLayout(self.layoutHistoricalBaselineProjectionInfo)
        self.layoutOptionsHistoricalBaselineProjection.addLayout(self.layoutHistoricalBaselineProjection)
        
        self.labelHistoricalBaselineProjectionInfo = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHistoricalBaselineProjectionInfo.addWidget(self.labelHistoricalBaselineProjectionInfo)
        
        self.labelHistoricalBaselineProjectionWorkingDir = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionWorkingDir.setText('Working directory:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionWorkingDir, 0, 0)
        
        self.lineEditHistoricalBaselineProjectionWorkingDir = QtGui.QLineEdit()
        self.lineEditHistoricalBaselineProjectionWorkingDir.setReadOnly(True)
        self.layoutHistoricalBaselineProjection.addWidget(self.lineEditHistoricalBaselineProjectionWorkingDir, 0, 1)
        
        self.buttonSelectHistoricalBaselineProjectionWorkingDir = QtGui.QPushButton()
        self.buttonSelectHistoricalBaselineProjectionWorkingDir.setText('&Browse')
        self.layoutHistoricalBaselineProjection.addWidget(self.buttonSelectHistoricalBaselineProjectionWorkingDir, 0, 2)
        
        self.labelHistoricalBaselineProjectionQUESCDatabase = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionQUESCDatabase.setText('QUES-C Database:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionQUESCDatabase, 1, 0)
        
        self.lineEditHistoricalBaselineProjectionQUESCDatabase = QtGui.QLineEdit()
        self.lineEditHistoricalBaselineProjectionQUESCDatabase.setReadOnly(True)
        self.layoutHistoricalBaselineProjection.addWidget(self.lineEditHistoricalBaselineProjectionQUESCDatabase, 1, 1)
        
        self.buttonSelectHistoricalBaselineProjectionQUESCDatabase = QtGui.QPushButton()
        self.buttonSelectHistoricalBaselineProjectionQUESCDatabase.setText('&Browse')
        self.layoutHistoricalBaselineProjection.addWidget(self.buttonSelectHistoricalBaselineProjectionQUESCDatabase, 1, 2)
        
        self.labelHistoricalBaselineProjectionT1 = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionT1.setText('Base year T&1:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionT1, 2, 0)
        
        self.spinBoxHistoricalBaselineProjectionT1 = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineProjectionT1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxHistoricalBaselineProjectionT1.setValue(td.year)
        self.layoutHistoricalBaselineProjection.addWidget(self.spinBoxHistoricalBaselineProjectionT1, 2, 1)
        
        self.labelHistoricalBaselineProjectionT1.setBuddy(self.spinBoxHistoricalBaselineProjectionT1)
        
        self.labelHistoricalBaselineProjectionT2 = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionT2.setText('Base year T&2:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionT2, 3, 0)
        
        self.spinBoxHistoricalBaselineProjectionT2 = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineProjectionT2.setRange(1, 9999)
        self.spinBoxHistoricalBaselineProjectionT2.setValue(td.year)
        self.layoutHistoricalBaselineProjection.addWidget(self.spinBoxHistoricalBaselineProjectionT2, 3, 1)
        self.labelHistoricalBaselineProjectionT2.setBuddy(self.spinBoxHistoricalBaselineProjectionT2)
        
        self.labelHistoricalBaselineProjectionIteration = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionIteration.setText('&Iteration:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionIteration, 4, 0)
        
        self.spinBoxHistoricalBaselineProjectionIteration = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineProjectionIteration.setRange(1, 9999)
        self.spinBoxHistoricalBaselineProjectionIteration.setValue(5)
        self.layoutHistoricalBaselineProjection.addWidget(self.spinBoxHistoricalBaselineProjectionIteration, 4, 1)
        self.labelHistoricalBaselineProjectionIteration.setBuddy(self.spinBoxHistoricalBaselineProjectionIteration) 
        
        # 'Historical baseline annual projection' GroupBox
        self.groupBoxHistoricalBaselineAnnualProjection = QtGui.QGroupBox('Historical baseline annual projection')
        self.layoutGroupBoxHistoricalBaselineAnnualProjection = QtGui.QHBoxLayout()
        self.groupBoxHistoricalBaselineAnnualProjection.setLayout(self.layoutGroupBoxHistoricalBaselineAnnualProjection)
        self.layoutOptionsHistoricalBaselineAnnualProjection = QtGui.QVBoxLayout()
        self.layoutOptionsHistoricalBaselineAnnualProjection.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsHistoricalBaselineAnnualProjection = QtGui.QWidget()
        self.contentOptionsHistoricalBaselineAnnualProjection.setLayout(self.layoutOptionsHistoricalBaselineAnnualProjection)
        self.layoutOptionsHistoricalBaselineAnnualProjection.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxHistoricalBaselineAnnualProjection = QtGui.QCheckBox()
        self.checkBoxHistoricalBaselineAnnualProjection.setChecked(False)
        self.contentOptionsHistoricalBaselineAnnualProjection.setDisabled(True)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.addWidget(self.checkBoxHistoricalBaselineAnnualProjection)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.addWidget(self.contentOptionsHistoricalBaselineAnnualProjection)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.insertStretch(2, 1)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.setAlignment(self.checkBoxHistoricalBaselineAnnualProjection, QtCore.Qt.AlignTop)
        self.layoutHistoricalBaselineAnnualProjectionInfo = QtGui.QVBoxLayout()
        self.layoutHistoricalBaselineAnnualProjection = QtGui.QGridLayout()
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(self.layoutHistoricalBaselineAnnualProjectionInfo)
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(self.layoutHistoricalBaselineAnnualProjection)
        
        self.labelHistoricalBaselineAnnualProjectionInfo = QtGui.QLabel()
        self.labelHistoricalBaselineAnnualProjectionInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHistoricalBaselineAnnualProjectionInfo.addWidget(self.labelHistoricalBaselineAnnualProjectionInfo)
        
        self.labelHistoricalBaselineAnnualProjectionIteration = QtGui.QLabel()
        self.labelHistoricalBaselineAnnualProjectionIteration.setText('&Iteration:')
        self.layoutHistoricalBaselineAnnualProjection.addWidget(self.labelHistoricalBaselineAnnualProjectionIteration, 0, 0)
        
        self.spinBoxHistoricalBaselineAnnualProjectionIteration = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineAnnualProjectionIteration.setRange(1, 9999)
        self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(5)
        self.layoutHistoricalBaselineAnnualProjection.addWidget(self.spinBoxHistoricalBaselineAnnualProjectionIteration, 0, 1)
        self.labelHistoricalBaselineAnnualProjectionIteration.setBuddy(self.spinBoxHistoricalBaselineAnnualProjectionIteration)
        
        # 'Drivers analysis' GroupBox
        self.groupBoxDriversAnalysis = QtGui.QGroupBox('Drivers analysis')
        self.layoutGroupBoxDriversAnalysis = QtGui.QHBoxLayout()
        self.groupBoxDriversAnalysis.setLayout(self.layoutGroupBoxDriversAnalysis)
        self.layoutOptionsDriversAnalysis = QtGui.QVBoxLayout()
        self.layoutOptionsDriversAnalysis.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsDriversAnalysis = QtGui.QWidget()
        self.contentOptionsDriversAnalysis.setLayout(self.layoutOptionsDriversAnalysis)
        self.layoutOptionsDriversAnalysis.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxDriversAnalysis = QtGui.QCheckBox()
        self.checkBoxDriversAnalysis.setChecked(False)
        self.contentOptionsDriversAnalysis.setDisabled(True)
        self.layoutGroupBoxDriversAnalysis.addWidget(self.checkBoxDriversAnalysis)
        self.layoutGroupBoxDriversAnalysis.addWidget(self.contentOptionsDriversAnalysis)
        self.layoutGroupBoxDriversAnalysis.setAlignment(self.checkBoxDriversAnalysis, QtCore.Qt.AlignTop)
        self.layoutDriversAnalysisInfo = QtGui.QVBoxLayout()
        self.layoutDriversAnalysis = QtGui.QGridLayout()
        self.layoutOptionsDriversAnalysis.addLayout(self.layoutDriversAnalysisInfo)
        self.layoutOptionsDriversAnalysis.addLayout(self.layoutDriversAnalysis)
        
        self.labelDriversAnalysisInfo = QtGui.QLabel()
        self.labelDriversAnalysisInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutDriversAnalysisInfo.addWidget(self.labelDriversAnalysisInfo)
        
        self.labelDriversAnalysisLandUseCoverChangeDrivers = QtGui.QLabel()
        self.labelDriversAnalysisLandUseCoverChangeDrivers.setText('Drivers of land use/cover change:')
        self.layoutDriversAnalysis.addWidget(self.labelDriversAnalysisLandUseCoverChangeDrivers, 0, 0)
        
        self.lineEditDriversAnalysisLandUseCoverChangeDrivers = QtGui.QLineEdit()
        self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setReadOnly(True)
        self.layoutDriversAnalysis.addWidget(self.lineEditDriversAnalysisLandUseCoverChangeDrivers, 0, 1)
        
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers = QtGui.QPushButton()
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers.setText('&Browse')
        self.layoutDriversAnalysis.addWidget(self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers, 0, 2)
        
        self.labelDriversAnalysislandUseCoverChangeType = QtGui.QLabel()
        self.labelDriversAnalysislandUseCoverChangeType.setText('Land use/cover change type:')
        self.layoutDriversAnalysis.addWidget(self.labelDriversAnalysislandUseCoverChangeType, 1, 0)
        
        self.lineEditDriversAnalysisLandUseCoverChangeType = QtGui.QLineEdit()
        self.lineEditDriversAnalysisLandUseCoverChangeType.setText('Land use change')
        self.layoutDriversAnalysis.addWidget(self.lineEditDriversAnalysisLandUseCoverChangeType, 1, 1)
        self.labelDriversAnalysislandUseCoverChangeType.setBuddy(self.lineEditDriversAnalysisLandUseCoverChangeType)
        
        # 'Build scenario' GroupBox
        self.groupBoxBuildScenario = QtGui.QGroupBox('Build scenario')
        self.layoutGroupBoxBuildScenario = QtGui.QHBoxLayout()
        self.groupBoxBuildScenario.setLayout(self.layoutGroupBoxBuildScenario)
        self.layoutOptionsBuildScenario = QtGui.QVBoxLayout()
        self.layoutOptionsBuildScenario.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsBuildScenario = QtGui.QWidget()
        self.contentOptionsBuildScenario.setLayout(self.layoutOptionsBuildScenario)
        self.layoutOptionsBuildScenario.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxBuildScenario = QtGui.QCheckBox()
        self.checkBoxBuildScenario.setChecked(False)
        self.contentOptionsBuildScenario.setDisabled(True)
        self.layoutGroupBoxBuildScenario.addWidget(self.checkBoxBuildScenario)
        self.layoutGroupBoxBuildScenario.addWidget(self.contentOptionsBuildScenario)
        self.layoutGroupBoxBuildScenario.setAlignment(self.checkBoxBuildScenario, QtCore.Qt.AlignTop)
        self.layoutBuildScenarioInfo = QtGui.QVBoxLayout()
        self.layoutBuildScenario = QtGui.QGridLayout()
        self.layoutOptionsBuildScenario.addLayout(self.layoutBuildScenarioInfo)
        self.layoutOptionsBuildScenario.addLayout(self.layoutBuildScenario)
        
        self.labelBuildScenarioInfo = QtGui.QLabel()
        self.labelBuildScenarioInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutBuildScenarioInfo.addWidget(self.labelBuildScenarioInfo)
        
        self.labelBuildScenarioHistoricalBaselineCar = QtGui.QLabel()
        self.labelBuildScenarioHistoricalBaselineCar.setText('Historical baseline car:')
        self.layoutBuildScenario.addWidget(self.labelBuildScenarioHistoricalBaselineCar, 0, 0)
        
        self.lineEditBuildScenarioHistoricalBaselineCar = QtGui.QLineEdit()
        self.lineEditBuildScenarioHistoricalBaselineCar.setReadOnly(True)
        self.layoutBuildScenario.addWidget(self.lineEditBuildScenarioHistoricalBaselineCar, 0, 1)
        
        self.buttonSelectBuildScenarioHistoricalBaselineCar = QtGui.QPushButton()
        self.buttonSelectBuildScenarioHistoricalBaselineCar.setText('&Browse')
        self.layoutBuildScenario.addWidget(self.buttonSelectBuildScenarioHistoricalBaselineCar, 0, 2)
        
        # Process tab button
        self.layoutButtonLowEmissionDevelopmentAnalysis = QtGui.QHBoxLayout()
        self.buttonProcessLowEmissionDevelopmentAnalysis = QtGui.QPushButton()
        self.buttonProcessLowEmissionDevelopmentAnalysis.setText('&Process')
        self.layoutButtonLowEmissionDevelopmentAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLowEmissionDevelopmentAnalysis.addWidget(self.buttonProcessLowEmissionDevelopmentAnalysis)
        
        # Place the GroupBoxes
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxHistoricalBaselineProjection)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxHistoricalBaselineAnnualProjection)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxDriversAnalysis)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxBuildScenario)
        self.layoutTabLowEmissionDevelopmentAnalysis.addLayout(self.layoutButtonLowEmissionDevelopmentAnalysis)
        
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
        super(DialogLumensSCIENDO, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Called when the widget is closed
        """
        super(DialogLumensSCIENDO, self).closeEvent(event)
        
        print 'DEBUG'
        self.saveSettings('Low Emission Development Analysis', 'mysettings.ini')
        self.saveSettings('Land Use Change Modeling', 'mysettings.ini')
    
    
    #***********************************************************
    # 'Low Emission Development Analysis' tab QGroupBox toggle handlers
    #***********************************************************
    def toggleHistoricalBaselineProjection(self, checked):
        """
        """
        if checked:
            self.contentOptionsHistoricalBaselineProjection.setEnabled(True)
        else:
            self.contentOptionsHistoricalBaselineProjection.setDisabled(True)
    
    
    def toggleHistoricalBaselineAnnualProjection(self, checked):
        """
        """
        if checked:
            self.contentOptionsHistoricalBaselineAnnualProjection.setEnabled(True)
        else:
            self.contentOptionsHistoricalBaselineAnnualProjection.setDisabled(True)
    
    
    def toggleDriversAnalysis(self, checked):
        """
        """
        if checked:
            self.contentOptionsDriversAnalysis.setEnabled(True)
        else:
            self.contentOptionsDriversAnalysis.setDisabled(True)
    
    
    def toggleBuildScenario(self, checked):
        """
        """
        if checked:
            self.contentOptionsBuildScenario.setEnabled(True)
        else:
            self.contentOptionsBuildScenario.setDisabled(True)
    
    
    #***********************************************************
    # 'Low Emission Development Analysis' tab QPushButton handlers
    #***********************************************************
    def handlerSelectHistoricalBaselineProjectionWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditHistoricalBaselineProjectionWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectHistoricalBaselineProjectionQUESCDatabase(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select QUES-C Database', QtCore.QDir.homePath(), 'QUES-C Database (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if file:
            self.lineEditHistoricalBaselineProjectionQUESCDatabase.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDriversAnalysisLandUseCoverChangeDrivers(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use/Cover Change Drivers', QtCore.QDir.homePath(), 'Land Use/Cover Change Drivers (*{0})'.format(self.main.appSettings['selectTextfileExt'])))
        
        if file:
            self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectBuildScenarioHistoricalBaselineCar(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Historical Baseline Car', QtCore.QDir.homePath(), 'Historical Baseline Car (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditBuildScenarioHistoricalBaselineCar.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'Land Use Change Modeling' tab QPushButton handlers
    #***********************************************************
    def handlerSelectLandUseChangeModelingFactorsDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Factors Directory'))
        
        if dir:
            self.lineEditLandUseChangeModelingFactorsDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectLandUseChangeModelingLandUseLookup(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Lookup Table', QtCore.QDir.homePath(), 'Land Use Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeModelingLandUseLookup.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSettings(self):
        """
        """
        # 'Historical baseline projection' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['workingDir'] \
            = unicode(self.lineEditHistoricalBaselineProjectionWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['QUESCDatabase'] \
            = unicode(self.lineEditHistoricalBaselineProjectionQUESCDatabase.text())
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['t1'] \
            = self.spinBoxHistoricalBaselineProjectionT1.value()
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['t2'] \
            = self.spinBoxHistoricalBaselineProjectionT2.value()
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['iteration'] \
            = self.spinBoxHistoricalBaselineProjectionIteration.value()
        
        # 'Historical baseline annual projection' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection']['iteration'] \
            = self.spinBoxHistoricalBaselineAnnualProjectionIteration.value()
        
        # 'Drivers analysis' groupbox fields
        self.main.appSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeDrivers'] \
            = unicode(self.lineEditDriversAnalysisLandUseCoverChangeDrivers.text())
        self.main.appSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeType'] \
            = unicode(self.lineEditDriversAnalysisLandUseCoverChangeType.text())
        
        # 'Build scenario' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOBuildScenario']['historicalBaselineCar'] \
            = unicode(self.lineEditBuildScenarioHistoricalBaselineCar.text())
        
        # 'Land Use Change Modeling' tab fields
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['factorsDir'] \
            = unicode(self.lineEditLandUseChangeModelingFactorsDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['landUseLookup'] \
            = unicode(self.lineEditLandUseChangeModelingLandUseLookup.text())
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['baseYear'] \
            = self.spinBoxLandUseChangeModelingBaseYear.value()
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['location'] \
            = unicode(self.lineEditLandUseChangeModelingLocation.text())
    
    
    def validForm(self, formName):
        """
        """
        logging.getLogger(type(self).__name__).info('form validate: %s', formName)
        logging.getLogger(type(self).__name__).info('form values: %s', self.main.appSettings[formName])
        
        valid = True
        
        for key, val in self.main.appSettings[formName].iteritems():
            if val == 0: # for values set specific to 0
                continue
            elif not val:
                valid = False
        
        if not valid:
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
        
        return valid
    
    
    def handlerProcessLowEmissionDevelopmentAnalysis(self):
        """
        """
        self.setAppSettings()
        
        if self.checkBoxHistoricalBaselineProjection.isChecked():
            formName = 'DialogLumensSCIENDOHistoricalBaselineProjection'
            algName = 'modeler:projection_historical_baseline'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['workingDir'],
                    self.main.appSettings[formName]['QUESCDatabase'],
                    self.main.appSettings[formName]['t1'],
                    self.main.appSettings[formName]['t2'],
                    self.main.appSettings[formName]['iteration'],
                )
                
                ##print outputs
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxHistoricalBaselineAnnualProjection.isChecked():
            formName = 'DialogLumensSCIENDOHistoricalBaselineAnnualProjection'
            algName = 'r:historicalbaselineannualprojection'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['iteration'],
                )
                
                ##print outputs
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxBuildScenario.isChecked():
            formName = 'DialogLumensSCIENDOBuildScenario'
            algName = 'r:abacususingabsolutearea'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['historicalBaselineCar'],
                )
                
                ##print outputs
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    
    
    def handlerProcessLandUseChangeModeling(self):
        """
        """
        if self.checkBoxCalculateTransitionMatrix.isChecked():
            formName = 'DialogLumensSCIENDOCalculateTransitionMatrix'
            algName = 'modeler:sciendo1_calculate_transition_matrix'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                ##print outputs
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxCreateRasterCubeOfFactors.isChecked():
            formName = 'DialogLumensSCIENDOCreateRasterCube'
            algName = 'modeler:sciendo1_create_raster_cube'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                ##print outputs
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxCalculateWeightOfEvidence.isChecked():
            formName = 'DialogLumensSCIENDOCalculateWeightofEvidence'
            algName = 'modeler:sciendo3_calculate_weight_of_evidence'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                ##print outputs
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxSimulateLandUseChange.isChecked():
            formName = 'DialogLumensSCIENDOSimulateLandUseChange'
            algName = 'modeler:sciendo4_simulate_land_use_change'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                ##print outputs
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxSimulateWithScenario.isChecked():
            formName = 'DialogLumensSCIENDOSimulateWithScenario'
            algName = 'modeler:sciendo5_simulate_with_scenario'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                ##print outputs
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    