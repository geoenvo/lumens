#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime, glob
##from qgis.core import *
##from processing.tools import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
import resource


class DialogLumensSCIENDO(QtGui.QDialog):
    """
    """
    def loadTemplateFiles(self):
        """List available ini template file inside the project folder
        """
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        
        if templateFiles:
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.clear()
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItems(sorted(templateFiles))
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            
            self.comboBoxLandUseChangeModelingTemplate.clear()
            self.comboBoxLandUseChangeModelingTemplate.addItems(sorted(templateFiles))
            self.comboBoxLandUseChangeModelingTemplate.setEnabled(True)
            self.buttonLoadLandUseChangeModelingTemplate.setEnabled(True)
            
            # MainWindow SCIENDO dashboard templates
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.clear()
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            self.main.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            
            self.main.comboBoxLandUseChangeModelingTemplate.clear()
            self.main.comboBoxLandUseChangeModelingTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxLandUseChangeModelingTemplate.setEnabled(True)
            self.main.buttonProcessSCIENDOLandUseChangeModelingTemplate.setEnabled(True)
        else:
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            
            self.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
            self.buttonLoadLandUseChangeModelingTemplate.setDisabled(True)
            
            # MainWindow SCIENDO dashboard templates
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            self.main.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            
            self.main.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
            self.main.buttonProcessSCIENDOLandUseChangeModelingTemplate.setDisabled(True)
    
    
    def loadTemplate(self, tabName, fileName, returnTemplateSettings=False):
        """Load the value saved in ini template file to the form widget
        """
        templateFilePath = os.path.join(self.settingsPath, fileName)
        settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        
        templateSettings = {}
        dialogsToLoad = None
        
        td = datetime.date.today()
        
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
            
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection'] = {}
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['workingDir'] = workingDir = settings.value('workingDir')
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['QUESCDatabase'] = QUESCDatabase = settings.value('QUESCDatabase')
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['t1'] = t1 = settings.value('t1')
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['t2'] = t2 = settings.value('t2')
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['iteration'] = iteration = settings.value('iteration')
            
            if not returnTemplateSettings:
                if workingDir and os.path.isdir(workingDir):
                    self.lineEditHistoricalBaselineProjectionWorkingDir.setText(workingDir)
                else:
                    self.lineEditHistoricalBaselineProjectionWorkingDir.setText('')
                if QUESCDatabase and os.path.exists(QUESCDatabase):
                    self.lineEditHistoricalBaselineProjectionQUESCDatabase.setText(QUESCDatabase)
                else:
                    self.lineEditHistoricalBaselineProjectionQUESCDatabase.setText('')
                if t1:
                    self.spinBoxHistoricalBaselineProjectionT1.setValue(int(t1))
                else:
                    self.spinBoxHistoricalBaselineProjectionT1.setValue(td.year)
                if t2:
                    self.spinBoxHistoricalBaselineProjectionT2.setValue(int(t2))
                else:
                    self.spinBoxHistoricalBaselineProjectionT2.setValue(td.year)
                if iteration:
                    self.spinBoxHistoricalBaselineProjectionIteration.setValue(int(iteration))
                else:
                    self.spinBoxHistoricalBaselineProjectionIteration.setValue(5)
            
            settings.endGroup()
            # /dialog
            
            # 'Historical baseline annual projection' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOHistoricalBaselineAnnualProjection')
            
            templateSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection'] = {}
            templateSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection']['iteration'] = iteration = settings.value('iteration')
            
            if not returnTemplateSettings:
                if iteration:
                    self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(int(iteration))
                else:
                    self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(5)
            
            settings.endGroup()
            # /dialog
            
            # 'Drivers analysis' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDODriversAnalysis')
            
            templateSettings['DialogLumensSCIENDODriversAnalysis'] = {}
            templateSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeDrivers'] = landUseCoverChangeDrivers = settings.value('landUseCoverChangeDrivers')
            templateSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeType'] = landUseCoverChangeType = settings.value('landUseCoverChangeType')
            
            if not returnTemplateSettings:
                if landUseCoverChangeDrivers and os.path.exists(landUseCoverChangeDrivers):
                    self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText(landUseCoverChangeDrivers)
                else:
                    self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText('')
                if landUseCoverChangeType:
                    self.lineEditDriversAnalysisLandUseCoverChangeType.setText(landUseCoverChangeType)
                else:
                    self.lineEditDriversAnalysisLandUseCoverChangeType.setText('Land use change')
            
            settings.endGroup()
            # /dialog
            
            # 'Build scenario' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOBuildScenario')
            
            templateSettings['DialogLumensSCIENDOBuildScenario'] = {}
            templateSettings['DialogLumensSCIENDOBuildScenario']['historicalBaselineCar'] = historicalBaselineCar = settings.value('historicalBaselineCar')
            
            if not returnTemplateSettings:
                if historicalBaselineCar and os.path.exists(historicalBaselineCar):
                    self.lineEditBuildScenarioHistoricalBaselineCar.setText(historicalBaselineCar)
                else:
                    self.lineEditBuildScenarioHistoricalBaselineCar.setText('')
            
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
            
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix'] = {}
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['factorsDir'] = factorsDir = settings.value('factorsDir')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['landUseLookup'] = landUseLookup = settings.value('landUseLookup')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['baseYear'] = baseYear = settings.value('baseYear')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['location'] = location = settings.value('location')
            
            if not returnTemplateSettings:
                if factorsDir and os.path.isdir(factorsDir):
                    self.lineEditLandUseChangeModelingFactorsDir.setText(factorsDir)
                else:
                    self.lineEditLandUseChangeModelingFactorsDir.setText('')
                if landUseLookup and os.path.exists(landUseLookup):
                    self.lineEditLandUseChangeModelingLandUseLookup.setText(landUseLookup)
                else:
                    self.lineEditLandUseChangeModelingLandUseLookup.setText('')
                if baseYear:
                    self.spinBoxLandUseChangeModelingBaseYear.setValue(int(baseYear))
                else:
                    self.spinBoxLandUseChangeModelingBaseYear.setValue(td.year)
                if location:
                    self.lineEditLandUseChangeModelingLocation.setText(location)
                else:
                    self.lineEditLandUseChangeModelingLocation.setText('location')
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        
        if returnTemplateSettings:
            return templateSettings
        
        """
        print 'DEBUG'
        settings.beginGroup(tabName)
        for dialog in dialogsToLoad:
            settings.beginGroup(dialog)
            for key in self.main.appSettings[dialog].keys():
                print key, settings.value(key)
            settings.endGroup()
        settings.endGroup()
        """
    
    
    def checkForDuplicateTemplates(self, tabName, templateToSkip):
        """
        """
        duplicateTemplate = None
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        dialogsToLoad = None
        
        if tabName == 'Low Emission Development Analysis':
            dialogsToLoad = (
                'DialogLumensSCIENDOHistoricalBaselineProjection',
                'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                'DialogLumensSCIENDODriversAnalysis',
                'DialogLumensSCIENDOBuildScenario',
            )
        elif tabName == 'Land Use Change Modeling':
            dialogsToLoad = (
                'DialogLumensSCIENDOCalculateTransitionMatrix',
            )
        
        for templateFile in templateFiles:
            if templateFile == templateToSkip:
                continue
            
            duplicateTemplate = templateFile
            templateSettings = self.loadTemplate(tabName, templateFile, True)
            
            print 'DEBUG'
            print templateFile, templateSettings
            
            # Loop thru all dialogs in a tab
            for dialog in dialogsToLoad:
                # Loop thru all settings in a dialog
                for key, val in self.main.appSettings[dialog].iteritems():
                    if templateSettings[dialog][key] != val:
                        # A setting doesn't match! This is not a matching template file, move along
                        duplicateTemplate = None
                    else:
                        print 'DEBUG equal settings'
                        print templateSettings[dialog][key], val
        
        # Found a duplicate template, offer to load it?
        if duplicateTemplate:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Existing Template',
                'The template you are about to save matches an existing template.\nDo you want to load \'{0}\' instead?'.format(duplicateTemplate),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                self.handlerLoadPURTemplate(duplicateTemplate)
                return True
        
        return False
    
    
    def saveTemplate(self, tabName, fileName):
        """Save form values according to their tab and dialog to a template file
        """
        self.setAppSettings()
        
        # Check if current form values duplicate an existing template
        if not self.checkForDuplicateTemplates(tabName, fileName):
            templateFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'], fileName)
            settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
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
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'])
        self.currentLowEmissionDevelopmentAnalysisTemplate = None
        self.currentLandUseChangeModelingTemplate = None
        
        # Init logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensSCIENDO init'
            self.logger = logging.getLogger(type(self).__name__)
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        # History log
        self.historyLog = '{0}{1}'.format('action', type(self).__name__)
        self.historyLogPath = os.path.join(self.settingsPath, self.historyLog + '.log')
        self.historyLogger = logging.getLogger(self.historyLog)
        fh = logging.FileHandler(self.historyLogPath)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.log_box.setFormatter(formatter)
        self.historyLogger.addHandler(self.log_box)
        self.historyLogger.setLevel(logging.INFO)
        
        self.loadHistoryLog()
        
        self.loadTemplateFiles()
        
        self.tabWidget.currentChanged.connect(self.handlerTabWidgetChanged)
        
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
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerLoadLowEmissionDevelopmentAnalysisTemplate)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerSaveLowEmissionDevelopmentAnalysisTemplate)
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerSaveAsLowEmissionDevelopmentAnalysisTemplate)
        
        # 'Land Use Change Modeling' tab buttons
        self.buttonSelectLandUseChangeModelingFactorsDir.clicked.connect(self.handlerSelectLandUseChangeModelingFactorsDir)
        self.buttonSelectLandUseChangeModelingLandUseLookup.clicked.connect(self.handlerSelectLandUseChangeModelingLandUseLookup)
        self.buttonProcessLandUseChangeModeling.clicked.connect(self.handlerProcessLandUseChangeModeling)
        self.buttonLoadLandUseChangeModelingTemplate.clicked.connect(self.handlerLoadLandUseChangeModelingTemplate)
        self.buttonSaveLandUseChangeModelingTemplate.clicked.connect(self.handlerSaveLandUseChangeModelingTemplate)
        self.buttonSaveAsLandUseChangeModelingTemplate.clicked.connect(self.handlerSaveAsLandUseChangeModelingTemplate)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabLowEmissionDevelopmentAnalysis = QtGui.QWidget()
        self.tabLandUseChangeModeling = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabLowEmissionDevelopmentAnalysis, 'Low Emission Development Analysis')
        self.tabWidget.addTab(self.tabLandUseChangeModeling, 'Land Use Change Modeling')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        ###self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QVBoxLayout()
        self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QGridLayout()
        ##self.layoutTabLandUseChangeModeling = QtGui.QVBoxLayout()
        self.layoutTabLandUseChangeModeling = QtGui.QGridLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabLowEmissionDevelopmentAnalysis.setLayout(self.layoutTabLowEmissionDevelopmentAnalysis)
        self.tabLandUseChangeModeling.setLayout(self.layoutTabLandUseChangeModeling)
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
        self.buttonProcessLowEmissionDevelopmentAnalysis.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonProcessLowEmissionDevelopmentAnalysis.setText('&Process')
        self.layoutButtonLowEmissionDevelopmentAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLowEmissionDevelopmentAnalysis.addWidget(self.buttonProcessLowEmissionDevelopmentAnalysis)
        
        # Template GroupBox
        self.groupBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLowEmissionDevelopmentAnalysisTemplate.setLayout(self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate)
        self.layoutLowEmissionDevelopmentAnalysisTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLowEmissionDevelopmentAnalysisTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutLowEmissionDevelopmentAnalysisTemplateInfo)
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutLowEmissionDevelopmentAnalysisTemplate)
        
        self.labelLoadedLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLoadedLowEmissionDevelopmentAnalysisTemplate.setText('Loaded template:')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLoadedLowEmissionDevelopmentAnalysisTemplate, 0, 0)
        
        self.loadedLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.loadedLowEmissionDevelopmentAnalysisTemplate.setText('<None>')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.loadedLowEmissionDevelopmentAnalysisTemplate, 0, 1)
        
        self.labelLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLowEmissionDevelopmentAnalysisTemplate.setText('Template name:')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLowEmissionDevelopmentAnalysisTemplate, 1, 0)
        
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItem('No template found')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.comboBoxLowEmissionDevelopmentAnalysisTemplate, 1, 1)
        
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setText('Load')
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setText('Save')
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.setText('Save As')
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonLoadLowEmissionDevelopmentAnalysisTemplate)
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonSaveLowEmissionDevelopmentAnalysisTemplate)
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate)
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutButtonLowEmissionDevelopmentAnalysisTemplate)
        
        # Place the GroupBoxes
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxHistoricalBaselineProjection, 0, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxHistoricalBaselineAnnualProjection, 1, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxDriversAnalysis, 2, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxBuildScenario, 3, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addLayout(self.layoutButtonLowEmissionDevelopmentAnalysis, 4, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxLowEmissionDevelopmentAnalysisTemplate, 0, 1, 4, 1)
        self.layoutTabLowEmissionDevelopmentAnalysis.setColumnStretch(0, 3)
        self.layoutTabLowEmissionDevelopmentAnalysis.setColumnStretch(1, 1) # Smaller template column
        
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
        self.checkBoxCreateRasterCubeOfFactors = QtGui.QCheckBox('Create raster cube of factors')
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
        
        # Template GroupBox
        self.groupBoxLandUseChangeModelingTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxLandUseChangeModelingTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeModelingTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeModelingTemplate.setLayout(self.layoutGroupBoxLandUseChangeModelingTemplate)
        self.layoutLandUseChangeModelingTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeModelingTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeModelingTemplate.addLayout(self.layoutLandUseChangeModelingTemplateInfo)
        self.layoutGroupBoxLandUseChangeModelingTemplate.addLayout(self.layoutLandUseChangeModelingTemplate)
        
        self.labelLoadedLandUseChangeModelingTemplate = QtGui.QLabel()
        self.labelLoadedLandUseChangeModelingTemplate.setText('Loaded template:')
        self.layoutLandUseChangeModelingTemplate.addWidget(self.labelLoadedLandUseChangeModelingTemplate, 0, 0)
        
        self.loadedLandUseChangeModelingTemplate = QtGui.QLabel()
        self.loadedLandUseChangeModelingTemplate.setText('<None>')
        self.layoutLandUseChangeModelingTemplate.addWidget(self.loadedLandUseChangeModelingTemplate, 0, 1)
        
        self.labelLandUseChangeModelingTemplate = QtGui.QLabel()
        self.labelLandUseChangeModelingTemplate.setText('Template name:')
        self.layoutLandUseChangeModelingTemplate.addWidget(self.labelLandUseChangeModelingTemplate, 1, 0)
        
        self.comboBoxLandUseChangeModelingTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
        self.comboBoxLandUseChangeModelingTemplate.addItem('No template found')
        self.layoutLandUseChangeModelingTemplate.addWidget(self.comboBoxLandUseChangeModelingTemplate, 1, 1)
        
        self.layoutButtonLandUseChangeModelingTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLandUseChangeModelingTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLandUseChangeModelingTemplate = QtGui.QPushButton()
        self.buttonLoadLandUseChangeModelingTemplate.setDisabled(True)
        self.buttonLoadLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLandUseChangeModelingTemplate.setText('Load')
        self.buttonSaveLandUseChangeModelingTemplate = QtGui.QPushButton()
        self.buttonSaveLandUseChangeModelingTemplate.setDisabled(True)
        self.buttonSaveLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLandUseChangeModelingTemplate.setText('Save')
        self.buttonSaveAsLandUseChangeModelingTemplate = QtGui.QPushButton()
        self.buttonSaveAsLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLandUseChangeModelingTemplate.setText('Save As')
        self.layoutButtonLandUseChangeModelingTemplate.addWidget(self.buttonLoadLandUseChangeModelingTemplate)
        self.layoutButtonLandUseChangeModelingTemplate.addWidget(self.buttonSaveLandUseChangeModelingTemplate)
        self.layoutButtonLandUseChangeModelingTemplate.addWidget(self.buttonSaveAsLandUseChangeModelingTemplate)
        self.layoutGroupBoxLandUseChangeModelingTemplate.addLayout(self.layoutButtonLandUseChangeModelingTemplate)
        
        # Place the GroupBoxes
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeModelingFunctions, 0, 0)
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeModelingParameters, 1, 0)
        self.layoutTabLandUseChangeModeling.addLayout(self.layoutButtonLandUseChangeModeling, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeModelingTemplate, 0, 1, 2, 1)
        self.layoutTabLandUseChangeModeling.setColumnStretch(0, 3)
        self.layoutTabLandUseChangeModeling.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Log' tab
        #***********************************************************
        # 'History Log' GroupBox
        self.groupBoxHistoryLog = QtGui.QGroupBox('{0} {1}'.format(self.dialogTitle, 'history log'))
        self.layoutGroupBoxHistoryLog = QtGui.QVBoxLayout()
        self.layoutGroupBoxHistoryLog.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxHistoryLog.setLayout(self.layoutGroupBoxHistoryLog)
        self.layoutHistoryLogInfo = QtGui.QVBoxLayout()
        self.layoutHistoryLog = QtGui.QVBoxLayout()
        self.layoutGroupBoxHistoryLog.addLayout(self.layoutHistoryLogInfo)
        self.layoutGroupBoxHistoryLog.addLayout(self.layoutHistoryLog)
        
        self.labelHistoryLogInfo = QtGui.QLabel()
        self.labelHistoryLogInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHistoryLogInfo.addWidget(self.labelHistoryLogInfo)
        
        self.log_box = QPlainTextEditLogger(self)
        self.layoutHistoryLog.addWidget(self.log_box.widget)
        
        self.layoutTabLog.addWidget(self.groupBoxHistoryLog)
        
        
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
    
    
    def loadHistoryLog(self):
        """Load the history log file
        """
        if os.path.exists(self.historyLogPath):
            logText = open(self.historyLogPath).read()
            self.log_box.widget.setPlainText(logText)
    
    
    def handlerTabWidgetChanged(self, index):
        """
        """
        if self.tabWidget.widget(index) == self.tabLog:
            self.log_box.widget.verticalScrollBar().triggerAction(QtGui.QAbstractSlider.SliderToMaximum)
    
    
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
    def handlerLoadLowEmissionDevelopmentAnalysisTemplate(self, fileName=None):
        """
        """
        templateFile = self.comboBoxLowEmissionDevelopmentAnalysisTemplate.currentText()
        reply = None
        
        if fileName:
            templateFile = fileName
        else:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Low Emission Development Analysis', templateFile)
            self.currentLowEmissionDevelopmentAnalysisTemplate = templateFile
            self.loadedLowEmissionDevelopmentAnalysisTemplate.setText(templateFile)
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setCurrentIndex(self.comboBoxLowEmissionDevelopmentAnalysisTemplate.findText(templateFile))
            self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
    
    
    def handlerSaveLowEmissionDevelopmentAnalysisTemplate(self, fileName=None):
        """
        """
        templateFile = self.currentLowEmissionDevelopmentAnalysisTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QtGui.QMessageBox.question(
            self,
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Low Emission Development Analysis', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLowEmissionDevelopmentAnalysisTemplate(self):
        """
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLowEmissionDevelopmentAnalysisTemplate(fileName)
            else:
                self.saveTemplate('Low Emission Development Analysis', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLowEmissionDevelopmentAnalysisTemplate(fileName)
    
    
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
    def handlerLoadLandUseChangeModelingTemplate(self, fileName=None):
        """
        """
        templateFile = self.comboBoxLandUseChangeModelingTemplate.currentText()
        reply = None
        
        if fileName:
            templateFile = fileName
        else:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Land Use Change Modeling', templateFile)
            self.currentLandUseChangeModelingTemplate = templateFile
            self.loadedLandUseChangeModelingTemplate.setText(templateFile)
            self.comboBoxLandUseChangeModelingTemplate.setCurrentIndex(self.comboBoxLandUseChangeModelingTemplate.findText(templateFile))
            self.buttonSaveLandUseChangeModelingTemplate.setEnabled(True)
    
    
    def handlerSaveLandUseChangeModelingTemplate(self, fileName=None):
        """
        """
        templateFile = self.currentLandUseChangeModelingTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QtGui.QMessageBox.question(
            self,
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Land Use Change Modeling', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLandUseChangeModelingTemplate(self):
        """
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLandUseChangeModelingTemplate(fileName)
            else:
                self.saveTemplate('Land Use Change Modeling', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLandUseChangeModelingTemplate(fileName)
    
    
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
    
    
    def outputsMessageBox(self, algName, outputs, successMessage, errorMessage):
        """Display a messagebox based on the processing result
        """
        if outputs and outputs['statuscode'] == '1':
            QtGui.QMessageBox.information(self, 'Success', successMessage)
            return True
        else:
            statusMessage = '"{0}" failed with status message:'.format(algName)
            
            if outputs and outputs['statusmessage']:
                statusMessage = '{0} {1}'.format(statusMessage, outputs['statusmessage'])
            
            logging.getLogger(type(self).__name__).error(statusMessage)
            QtGui.QMessageBox.critical(self, 'Error', errorMessage)
            return False
    
    
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
                
                self.outputsMessageBox(algName, outputs, '', '')
                
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
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        
        if self.checkBoxDriversAnalysis.isChecked():
            formName = 'DialogLumensSCIENDODriversAnalysis'
            algName = 'modeler:drivers_analysis'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['landUseCoverChangeDrivers'],
                    self.main.appSettings[formName]['landUseCoverChangeType'],
                )
                
                ##print outputs
                
                self.outputsMessageBox(algName, outputs, '', '')
                
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
                
                self.outputsMessageBox(algName, outputs, '', '')
                
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
                
                self.outputsMessageBox(algName, outputs, '', '')
                
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
                
                self.outputsMessageBox(algName, outputs, '', '')
                
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
                
                self.outputsMessageBox(algName, outputs, '', '')
                
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
                
                self.outputsMessageBox(algName, outputs, '', '')
                
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
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    