#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime, glob
from qgis.core import *
from processing.tools import *
from PyQt4 import QtCore, QtGui
import resource


class DialogLumensTAOpportunityCost(QtGui.QDialog):
    """
    """
    def loadTemplateFiles(self):
        """List available ini template file inside the project folder
        """
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        
        if templateFiles:
            self.comboBoxAbacusOpportunityCostTemplate.clear()
            self.comboBoxAbacusOpportunityCostTemplate.addItems(sorted(templateFiles))
            self.comboBoxAbacusOpportunityCostTemplate.setEnabled(True)
            self.buttonLoadAbacusOpportunityCostTemplate.setEnabled(True)
            
            self.comboBoxOpportunityCostCurveTemplate.clear()
            self.comboBoxOpportunityCostCurveTemplate.addItems(sorted(templateFiles))
            self.comboBoxOpportunityCostCurveTemplate.setEnabled(True)
            self.buttonLoadOpportunityCostCurveTemplate.setEnabled(True)
            
            self.comboBoxOpportunityCostMapTemplate.clear()
            self.comboBoxOpportunityCostMapTemplate.addItems(sorted(templateFiles))
            self.comboBoxOpportunityCostMapTemplate.setEnabled(True)
            self.buttonLoadOpportunityCostMapTemplate.setEnabled(True)
        else:
            self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
            self.buttonLoadAbacusOpportunityCostTemplate.setDisabled(True)
            
            self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
            self.buttonLoadOpportunityCostCurveTemplate.setDisabled(True)
            
            self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
            self.buttonLoadOpportunityCostMapTemplate.setDisabled(True)
        
    
    def loadTemplate(self, tabName, fileName):
        """Load the value saved in ini template file to the form widget
        """
        templateFilePath = os.path.join(self.settingsPath, fileName)
        settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        
        dialogsToLoad = None
        
        td = datetime.date.today()
        
        if tabName == 'Abacus Opportunity Cost':
            dialogsToLoad = (
                'DialogLumensTAAbacusOpportunityCostCurve',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Abacus opportunity cost' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensTAAbacusOpportunityCostCurve')
            
            projectFile = settings.value('projectFile')
            
            if projectFile and os.path.isdir(projectFile):
                self.lineEditAOCProjectFile.setText(projectFile)
            else:
                self.lineEditAOCProjectFile.setText('')
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Opportunity Cost Curve':
            dialogsToLoad = (
                'DialogLumensTAOpportunityCostCurve',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Opportunity Cost Curve' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensTAOpportunityCostCurve')
            
            period1 = settings.value('period1')
            period2 = settings.value('period2')
            workingDir = settings.value('workingDir')
            QUESCDatabase = settings.value('QUESCDatabase')
            csvNPVTable = settings.value('csvNPVTable')
            costThreshold = settings.value('costThreshold')
            outputOpportunityCostDatabase = settings.value('outputOpportunityCostDatabase')
            outputOpportunityCostReport = settings.value('outputOpportunityCostReport')
            
            if period1:
                self.spinBoxOCCPeriod1.setValue(int(period1))
            else:
                self.spinBoxOCCPeriod1.setValue(td.year)
            if period2:
                self.spinBoxOCCPeriod2.setValue(int(period2))
            else:
                self.spinBoxOCCPeriod2.setValue(td.year)
            if workingDir and os.path.isdir(workingDir):
                self.lineEditOCCWorkingDir.setText(workingDir)
            else:
                self.lineEditOCCWorkingDir.setText('')
            if QUESCDatabase and os.path.exists(QUESCDatabase):
                self.lineEditOCCQUESCDatabase.setText(QUESCDatabase)
            else:
                self.lineEditOCCQUESCDatabase.setText('')
            if csvNPVTable and os.path.exists(csvNPVTable):
                self.lineEditOCCCsvNPVTable.setText(csvNPVTable)
            else:
                self.lineEditOCCCsvNPVTable.setText('')
            if costThreshold:
                self.spinBoxOCCCostThreshold.setValue(int(costThreshold))
            else:
                self.spinBoxOCCCostThreshold.setValue(5)
            if outputOpportunityCostDatabase:
                self.lineEditOCCOutputOpportunityCostDatabase.setText(outputOpportunityCostDatabase)
            else:
                self.lineEditOCCOutputOpportunityCostDatabase.setText('')
            if outputOpportunityCostReport:
                self.lineEditOCCOutputOpportunityCostReport.setText(outputOpportunityCostReport)
            else:
                self.lineEditOCCOutputOpportunityCostReport.setText('')
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Opportunity Cost Map':
            dialogsToLoad = (
                'DialogLumensTAOpportunityCostMap',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Opportunity Cost Map' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensTAOpportunityCostMap')
            
            t1 = settings.value('t1')
            t2 = settings.value('t2')
            landUseT1 = settings.value('landUseT1')
            landUseT2 = settings.value('landUseT2')
            planningUnit = settings.value('planningUnit')
            csvPlanningUnit = settings.value('csvPlanningUnit')
            workingDir = settings.value('workingDir')
            location = settings.value('location')
            csvCarbon = settings.value('csvCarbon')
            csvProfitability = settings.value('csvProfitability')
            
            if t1:
                self.spinBoxOCMPeriod1.setValue(int(t1))
            else:
                self.spinBoxOCMPeriod1.setValue(td.year)
            if t2:
                self.spinBoxOCMPeriod2.setValue(int(t2))
            else:
                self.spinBoxOCMPeriod2.setValue(td.year)
            if landUseT1 and os.path.exists(landUseT1):
                self.lineEditOCMLandUseT1.setText(landUseT1)
            else:
                self.lineEditOCMLandUseT1.setText('')
            if landUseT2 and os.path.exists(landUseT2):
                self.lineEditOCMLandUseT2.setText(landUseT2)
            else:
                self.lineEditOCMLandUseT2.setText('')
            if planningUnit and os.path.exists(planningUnit):
                self.lineEditOCMPlanningUnit.setText(planningUnit)
            else:
                self.lineEditOCMPlanningUnit.setText('')
            if csvPlanningUnit and os.path.exists(csvPlanningUnit):
                self.lineEditOCMCsvPlanningUnit.setText(csvPlanningUnit)
            else:
                self.lineEditOCMCsvPlanningUnit.setText('')
            if workingDir and os.path.isdir(workingDir):
                self.lineEditOCMWorkingDir.setText(workingDir)
            else:
                self.lineEditOCMWorkingDir.setText('')
            if location:
                self.lineEditOCMLocation.setText(location)
            else:
                self.lineEditOCMLocation.setText('location')
            if csvCarbon and os.path.exists(csvCarbon):
                self.lineEditOCMCsvCarbon.setText(csvCarbon)
            else:
                self.lineEditOCMCsvCarbon.setText('')
            if csvProfitability and os.path.exists(csvProfitability):
                self.lineEditOCMCsvProfitability.setText(csvProfitability)
            else:
                self.lineEditOCMCsvProfitability.setText('')
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        
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
    
    
    def saveTemplate(self, tabName, fileName):
        """Save form values according to their tab and dialog to a template file
        """
        self.setAppSettings()
        templateFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderTA'], fileName)
        settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        
        dialogsToSave = None
        
        if tabName == 'Abacus Opportunity Cost':
            dialogsToSave = (
                'DialogLumensTAAbacusOpportunityCostCurve',
            )
        elif tabName == 'Opportunity Cost Curve':
            dialogsToSave = (
                'DialogLumensTAOpportunityCostCurve',
            )
        elif tabName == 'Opportunity Cost Map':
            dialogsToSave = (
                'DialogLumensTAOpportunityCostMap',
            )
        
        settings.beginGroup(tabName)
        for dialog in dialogsToSave:
            settings.beginGroup(dialog)
            for key, val in self.main.appSettings[dialog].iteritems():
                settings.setValue(key, val)
            settings.endGroup()
        settings.endGroup()
    
    
    def __init__(self, parent):
        super(DialogLumensTAOpportunityCost, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS Trade-Off Analysis [Opportunity Cost]'
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderTA'])
        self.currentAbacusOpportunityCostTemplate = None
        self.currentOpportunityCostCurveTemplate = None
        self.currentOpportunityCostMapTemplate = None
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensTAOpportunityCost init'
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        self.loadTemplateFiles()
        
        # 'Abacus Opportunity Cost' tab buttons
        self.buttonSelectAOCProjectFile.clicked.connect(self.handlerSelectAOCProjectFile)
        self.buttonProcessAbacusOpportunityCost.clicked.connect(self.handlerProcessAbacusOpportunityCost)
        self.buttonLoadAbacusOpportunityCostTemplate.clicked.connect(self.handlerLoadAbacusOpportunityCostTemplate)
        self.buttonSaveAbacusOpportunityCostTemplate.clicked.connect(self.handlerSaveAbacusOpportunityCostTemplate)
        self.buttonSaveAsAbacusOpportunityCostTemplate.clicked.connect(self.handlerSaveAsAbacusOpportunityCostTemplate)
        
        # 'Opportunity Cost Curve' tab buttons
        self.buttonSelectOCCWorkingDir.clicked.connect(self.handlerSelectOCCWorkingDir)
        self.buttonSelectOCCQUESCDatabase.clicked.connect(self.handlerSelectOCCQUESCDatabase)
        self.buttonSelectOCCCsvNPVTable.clicked.connect(self.handlerSelectOCCCsvNPVTable)
        self.buttonSelectOCCOutputOpportunityCostDatabase.clicked.connect(self.handlerSelectOCCOutputOpportunityCostDatabase)
        self.buttonSelectOCCOutputOpportunityCostReport.clicked.connect(self.handlerSelectOCCOutputOpportunityCostReport)
        self.buttonProcessOpportunityCostCurve.clicked.connect(self.handlerProcessOpportunityCostCurve)
        self.buttonLoadOpportunityCostCurveTemplate.clicked.connect(self.handlerLoadOpportunityCostCurveTemplate)
        self.buttonSaveOpportunityCostCurveTemplate.clicked.connect(self.handlerSaveOpportunityCostCurveTemplate)
        self.buttonSaveAsOpportunityCostCurveTemplate.clicked.connect(self.handlerSaveAsOpportunityCostCurveTemplate)
        
        # 'Opportunity Cost Map' tab buttons
        self.buttonSelectOCMLandUseT1.clicked.connect(self.handlerSelectOCMLandUseT1)
        self.buttonSelectOCMLandUseT2.clicked.connect(self.handlerSelectOCMLandUseT2)
        self.buttonSelectOCMPlanningUnit.clicked.connect(self.handlerSelectOCMPlanningUnit)
        self.buttonSelectOCMCsvPlanningUnit.clicked.connect(self.handlerSelectOCMCsvPlanningUnit)
        self.buttonSelectOCMWorkingDir.clicked.connect(self.handlerSelectOCMWorkingDir)
        self.buttonSelectOCMCsvCarbon.clicked.connect(self.handlerSelectOCMCsvCarbon)
        self.buttonSelectOCMCsvProfitability.clicked.connect(self.handlerSelectOCMCsvProfitability)
        self.buttonProcessOpportunityCostMap.clicked.connect(self.handlerProcessOpportunityCostMap)
        self.buttonLoadOpportunityCostMapTemplate.clicked.connect(self.handlerLoadOpportunityCostMapTemplate)
        self.buttonSaveOpportunityCostMapTemplate.clicked.connect(self.handlerSaveOpportunityCostMapTemplate)
        self.buttonSaveAsOpportunityCostMapTemplate.clicked.connect(self.handlerSaveAsOpportunityCostMapTemplate)
        
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabAbacusOpportunityCost = QtGui.QWidget()
        self.tabOpportunityCostCurve = QtGui.QWidget()
        self.tabOpportunityCostMap = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabAbacusOpportunityCost, 'Abacus Opportunity Cost')
        self.tabWidget.addTab(self.tabOpportunityCostCurve, 'Opportunity Cost Curve')
        self.tabWidget.addTab(self.tabOpportunityCostMap, 'Opportunity Cost Map')
        self.tabWidget.addTab(self.tabResult, 'Result')
        
        ##self.layoutTabAbacusOpportunityCost = QtGui.QVBoxLayout()
        self.layoutTabAbacusOpportunityCost = QtGui.QGridLayout()
        ##self.layoutTabOpportunityCostCurve = QtGui.QVBoxLayout()
        self.layoutTabOpportunityCostCurve = QtGui.QGridLayout()
        ##self.layoutTabOpportunityCostMap = QtGui.QVBoxLayout()
        self.layoutTabOpportunityCostMap = QtGui.QGridLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        
        self.tabAbacusOpportunityCost.setLayout(self.layoutTabAbacusOpportunityCost)
        self.tabOpportunityCostCurve.setLayout(self.layoutTabOpportunityCostCurve)
        self.tabOpportunityCostMap.setLayout(self.layoutTabOpportunityCostMap)
        self.tabResult.setLayout(self.layoutTabResult)
        
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Abacus opportunity cost' tab
        #***********************************************************
        # 'Other' GroupBox
        self.groupBoxOther = QtGui.QGroupBox('Other')
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
        
        self.labelAOCProjectFile = QtGui.QLabel(parent)
        self.labelAOCProjectFile.setText('Abacus project file:')
        self.layoutOther.addWidget(self.labelAOCProjectFile, 0, 0)
        
        self.lineEditAOCProjectFile = QtGui.QLineEdit(parent)
        self.lineEditAOCProjectFile.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditAOCProjectFile, 0, 1)
        
        self.buttonSelectAOCProjectFile = QtGui.QPushButton(parent)
        self.buttonSelectAOCProjectFile.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectAOCProjectFile, 0, 2)
        
        # Process tab button
        self.layoutButtonAbacusOpportunityCost = QtGui.QHBoxLayout()
        self.buttonProcessAbacusOpportunityCost = QtGui.QPushButton()
        self.buttonProcessAbacusOpportunityCost.setText('&Process')
        self.layoutButtonAbacusOpportunityCost.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonAbacusOpportunityCost.addWidget(self.buttonProcessAbacusOpportunityCost)
        
        # Template GroupBox
        self.groupBoxAbacusOpportunityCostTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxAbacusOpportunityCostTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxAbacusOpportunityCostTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxAbacusOpportunityCostTemplate.setLayout(self.layoutGroupBoxAbacusOpportunityCostTemplate)
        self.layoutAbacusOpportunityCostTemplateInfo = QtGui.QVBoxLayout()
        self.layoutAbacusOpportunityCostTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutAbacusOpportunityCostTemplateInfo)
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutAbacusOpportunityCostTemplate)
        
        self.labelLoadedAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.labelLoadedAbacusOpportunityCostTemplate.setText('Loaded template:')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.labelLoadedAbacusOpportunityCostTemplate, 0, 0)
        
        self.loadedAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.loadedAbacusOpportunityCostTemplate.setText('<None>')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.loadedAbacusOpportunityCostTemplate, 0, 1)
        
        self.labelAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.labelAbacusOpportunityCostTemplate.setText('Template name:')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.labelAbacusOpportunityCostTemplate, 1, 0)
        
        self.comboBoxAbacusOpportunityCostTemplate = QtGui.QComboBox()
        self.comboBoxAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
        self.comboBoxAbacusOpportunityCostTemplate.addItem('No template found')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.comboBoxAbacusOpportunityCostTemplate, 1, 1)
        
        self.layoutButtonAbacusOpportunityCostTemplate = QtGui.QHBoxLayout()
        self.layoutButtonAbacusOpportunityCostTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonLoadAbacusOpportunityCostTemplate.setDisabled(True)
        self.buttonLoadAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadAbacusOpportunityCostTemplate.setText('Load')
        self.buttonSaveAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonSaveAbacusOpportunityCostTemplate.setDisabled(True)
        self.buttonSaveAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAbacusOpportunityCostTemplate.setText('Save')
        self.buttonSaveAsAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonSaveAsAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsAbacusOpportunityCostTemplate.setText('Save As')
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonLoadAbacusOpportunityCostTemplate)
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonSaveAbacusOpportunityCostTemplate)
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonSaveAsAbacusOpportunityCostTemplate)
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutButtonAbacusOpportunityCostTemplate)
        
        # Place the GroupBoxes
        self.layoutTabAbacusOpportunityCost.addWidget(self.groupBoxOther, 0, 0)
        self.layoutTabAbacusOpportunityCost.addLayout(self.layoutButtonAbacusOpportunityCost, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabAbacusOpportunityCost.addWidget(self.groupBoxAbacusOpportunityCostTemplate, 0, 1, 1, 1)
        self.layoutTabAbacusOpportunityCost.setColumnStretch(0, 3)
        self.layoutTabAbacusOpportunityCost.setColumnStretch(1, 1) # Smaller template column
        
        
        #***********************************************************
        # Setup 'Opportunity cost curve' tab
        #***********************************************************
        # 'Period' GroupBox
        self.groupBoxOCCPeriod = QtGui.QGroupBox('Period')
        self.layoutGroupBoxOCCPeriod = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCCPeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCCPeriod.setLayout(self.layoutGroupBoxOCCPeriod)
        self.layoutOCCPeriodInfo = QtGui.QVBoxLayout()
        self.layoutOCCPeriod = QtGui.QGridLayout()
        self.layoutGroupBoxOCCPeriod.addLayout(self.layoutOCCPeriodInfo)
        self.layoutGroupBoxOCCPeriod.addLayout(self.layoutOCCPeriod)
        
        self.labelOCCPeriodInfo = QtGui.QLabel()
        self.labelOCCPeriodInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOCCPeriodInfo.addWidget(self.labelOCCPeriodInfo)
        
        self.labelSpinBoxOCCPeriod1 = QtGui.QLabel(parent)
        self.labelSpinBoxOCCPeriod1.setText('T&1:')
        self.layoutOCCPeriod.addWidget(self.labelSpinBoxOCCPeriod1, 0, 0)
        self.spinBoxOCCPeriod1 = QtGui.QSpinBox(parent)
        self.spinBoxOCCPeriod1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxOCCPeriod1.setValue(td.year)
        self.layoutOCCPeriod.addWidget(self.spinBoxOCCPeriod1, 0, 1)
        self.labelSpinBoxOCCPeriod1.setBuddy(self.spinBoxOCCPeriod1)
        
        self.labelSpinBoxOCCPeriod2 = QtGui.QLabel(parent)
        self.labelSpinBoxOCCPeriod2.setText('T&2:')
        self.layoutOCCPeriod.addWidget(self.labelSpinBoxOCCPeriod2, 1, 0)
        self.spinBoxOCCPeriod2 = QtGui.QSpinBox(parent)
        self.spinBoxOCCPeriod2.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxOCCPeriod2.setValue(td.year)
        self.layoutOCCPeriod.addWidget(self.spinBoxOCCPeriod2, 1, 1)
        self.labelSpinBoxOCCPeriod2.setBuddy(self.spinBoxOCCPeriod2)
        
        # 'Other' GroupBox
        self.groupBoxOCCOther = QtGui.QGroupBox('Other')
        self.layoutGroupBoxOCCOther = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCCOther.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCCOther.setLayout(self.layoutGroupBoxOCCOther)
        self.layoutOCCOtherInfo = QtGui.QVBoxLayout()
        self.layoutOCCOther = QtGui.QGridLayout()
        self.layoutGroupBoxOCCOther.addLayout(self.layoutOCCOtherInfo)
        self.layoutGroupBoxOCCOther.addLayout(self.layoutOCCOther)
        
        self.labelOCCOtherInfo = QtGui.QLabel()
        self.labelOCCOtherInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOCCOtherInfo.addWidget(self.labelOCCOtherInfo)
        
        self.labelOCCWorkingDir = QtGui.QLabel()
        self.labelOCCWorkingDir.setText('Working directory:')
        self.layoutOCCOther.addWidget(self.labelOCCWorkingDir, 0, 0)
        
        self.lineEditOCCWorkingDir = QtGui.QLineEdit()
        self.lineEditOCCWorkingDir.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditOCCWorkingDir, 0, 1)
        
        self.buttonSelectOCCWorkingDir = QtGui.QPushButton()
        self.buttonSelectOCCWorkingDir.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectOCCWorkingDir, 0, 2)
        
        self.labelOCCQUESCDatabase = QtGui.QLabel(parent)
        self.labelOCCQUESCDatabase.setText('QUES-C Database:')
        self.layoutOCCOther.addWidget(self.labelOCCQUESCDatabase, 1, 0)
        
        self.lineEditOCCQUESCDatabase = QtGui.QLineEdit()
        self.lineEditOCCQUESCDatabase.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditOCCQUESCDatabase, 1, 1)
        
        self.buttonSelectOCCQUESCDatabase = QtGui.QPushButton()
        self.buttonSelectOCCQUESCDatabase.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectOCCQUESCDatabase, 1, 2)
        
        self.labelOCCCsvNPVTable = QtGui.QLabel(parent)
        self.labelOCCCsvNPVTable.setText('Net Present Value (NPV) table:')
        self.layoutOCCOther.addWidget(self.labelOCCCsvNPVTable, 2, 0)
        
        self.lineEditOCCCsvNPVTable = QtGui.QLineEdit(parent)
        self.lineEditOCCCsvNPVTable.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditOCCCsvNPVTable, 2, 1)
        
        self.buttonSelectOCCCsvNPVTable = QtGui.QPushButton()
        self.buttonSelectOCCCsvNPVTable.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectOCCCsvNPVTable, 2, 2)
        
        self.labelOCCCostThreshold = QtGui.QLabel()
        self.labelOCCCostThreshold.setText('Cost &Threshold:')
        self.layoutOCCOther.addWidget(self.labelOCCCostThreshold, 3, 0)
        
        self.spinBoxOCCCostThreshold = QtGui.QSpinBox()
        self.spinBoxOCCCostThreshold.setValue(5)
        self.layoutOCCOther.addWidget(self.spinBoxOCCCostThreshold, 3, 1)
        self.labelOCCCostThreshold.setBuddy(self.spinBoxOCCCostThreshold)
        
        self.labelOCCOutputOpportunityCostDatabase = QtGui.QLabel()
        self.labelOCCOutputOpportunityCostDatabase.setText('[Output] Opportunity cost database:')
        self.layoutOCCOther.addWidget(self.labelOCCOutputOpportunityCostDatabase, 4, 0)
        
        self.lineEditOCCOutputOpportunityCostDatabase = QtGui.QLineEdit()
        self.lineEditOCCOutputOpportunityCostDatabase.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditOCCOutputOpportunityCostDatabase, 4, 1)
        
        self.buttonSelectOCCOutputOpportunityCostDatabase = QtGui.QPushButton(parent)
        self.buttonSelectOCCOutputOpportunityCostDatabase.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectOCCOutputOpportunityCostDatabase, 4, 2)
        
        self.labelOCCOutputOpportunityCostReport = QtGui.QLabel()
        self.labelOCCOutputOpportunityCostReport.setText('[Output] Opportunity cost report:')
        self.layoutOCCOther.addWidget(self.labelOCCOutputOpportunityCostReport, 5, 0)
        
        self.lineEditOCCOutputOpportunityCostReport = QtGui.QLineEdit()
        self.lineEditOCCOutputOpportunityCostReport.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditOCCOutputOpportunityCostReport, 5, 1)
        
        self.buttonSelectOCCOutputOpportunityCostReport = QtGui.QPushButton(parent)
        self.buttonSelectOCCOutputOpportunityCostReport.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectOCCOutputOpportunityCostReport, 5, 2)
        
        # Process tab button
        self.layoutButtonOpportunityCostCurve = QtGui.QHBoxLayout()
        self.buttonProcessOpportunityCostCurve = QtGui.QPushButton()
        self.buttonProcessOpportunityCostCurve.setText('&Process')
        self.layoutButtonOpportunityCostCurve.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonOpportunityCostCurve.addWidget(self.buttonProcessOpportunityCostCurve)
        
        # Template GroupBox
        self.groupBoxOpportunityCostCurveTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxOpportunityCostCurveTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOpportunityCostCurveTemplate.setLayout(self.layoutGroupBoxOpportunityCostCurveTemplate)
        self.layoutOpportunityCostCurveTemplateInfo = QtGui.QVBoxLayout()
        self.layoutOpportunityCostCurveTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplateInfo)
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplate)
        
        self.labelLoadedOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelLoadedOpportunityCostCurveTemplate.setText('Loaded template:')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelLoadedOpportunityCostCurveTemplate, 0, 0)
        
        self.loadedOpportunityCostCurveTemplate = QtGui.QLabel()
        self.loadedOpportunityCostCurveTemplate.setText('<None>')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.loadedOpportunityCostCurveTemplate, 0, 1)
        
        self.labelOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelOpportunityCostCurveTemplate.setText('Template name:')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelOpportunityCostCurveTemplate, 1, 0)
        
        self.comboBoxOpportunityCostCurveTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        self.comboBoxOpportunityCostCurveTemplate.addItem('No template found')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.comboBoxOpportunityCostCurveTemplate, 1, 1)
        
        self.layoutButtonOpportunityCostCurveTemplate = QtGui.QHBoxLayout()
        self.layoutButtonOpportunityCostCurveTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonLoadOpportunityCostCurveTemplate.setDisabled(True)
        self.buttonLoadOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadOpportunityCostCurveTemplate.setText('Load')
        self.buttonSaveOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonSaveOpportunityCostCurveTemplate.setDisabled(True)
        self.buttonSaveOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveOpportunityCostCurveTemplate.setText('Save')
        self.buttonSaveAsOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonSaveAsOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsOpportunityCostCurveTemplate.setText('Save As')
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonLoadOpportunityCostCurveTemplate)
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonSaveOpportunityCostCurveTemplate)
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonSaveAsOpportunityCostCurveTemplate)
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutButtonOpportunityCostCurveTemplate)
        
        # Place the GroupBoxes
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOCCPeriod, 0, 0)
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOCCOther, 1, 0)
        self.layoutTabOpportunityCostCurve.addLayout(self.layoutButtonOpportunityCostCurve, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOpportunityCostCurveTemplate, 0, 1, 2, 1)
        self.layoutTabOpportunityCostCurve.setColumnStretch(0, 3)
        self.layoutTabOpportunityCostCurve.setColumnStretch(1, 1) # Smaller template column
        
        ##self.layoutTabOpportunityCostCurve.insertStretch(2, 1)
        
        ##self.layoutTabOpportunityCostCurve.setStretchFactor(self.groupBoxOCCPeriod, 1)
        ##self.layoutTabOpportunityCostCurve.setStretchFactor(self.groupBoxOCCOther, 4)
        
        
        #***********************************************************
        # Setup 'Opportunity cost map' tab
        #***********************************************************
        # 'Period' GroupBox
        self.groupBoxOCMPeriod = QtGui.QGroupBox('Period')
        self.layoutGroupBoxOCMPeriod = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCMPeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCMPeriod.setLayout(self.layoutGroupBoxOCMPeriod)
        self.layoutOCMPeriodInfo = QtGui.QVBoxLayout()
        self.layoutOCMPeriod = QtGui.QGridLayout()
        self.layoutGroupBoxOCMPeriod.addLayout(self.layoutOCMPeriodInfo)
        self.layoutGroupBoxOCMPeriod.addLayout(self.layoutOCMPeriod)
        
        self.labelOCMPeriodInfo = QtGui.QLabel()
        self.labelOCMPeriodInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOCMPeriodInfo.addWidget(self.labelOCMPeriodInfo)
        
        self.labelOCMPeriod1 = QtGui.QLabel(parent)
        self.labelOCMPeriod1.setText('T&1:')
        self.layoutOCMPeriod.addWidget(self.labelOCMPeriod1, 0, 0)
        self.spinBoxOCMPeriod1 = QtGui.QSpinBox(parent)
        self.spinBoxOCMPeriod1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxOCMPeriod1.setValue(td.year)
        self.layoutOCMPeriod.addWidget(self.spinBoxOCMPeriod1, 0, 1)
        self.labelOCMPeriod1.setBuddy(self.spinBoxOCMPeriod1)
        
        self.labelOCMPeriod2 = QtGui.QLabel(parent)
        self.labelOCMPeriod2.setText('T&2:')
        self.layoutOCMPeriod.addWidget(self.labelOCMPeriod2, 1, 0)
        self.spinBoxOCMPeriod2 = QtGui.QSpinBox(parent)
        self.spinBoxOCMPeriod2.setRange(1, 9999)
        self.spinBoxOCMPeriod2.setValue(td.year)
        self.layoutOCMPeriod.addWidget(self.spinBoxOCMPeriod2, 1, 1)
        self.labelOCMPeriod2.setBuddy(self.spinBoxOCMPeriod2)
        
        # 'Land use map' GroupBox
        self.groupBoxLandUseMap = QtGui.QGroupBox('Land use map')
        self.layoutGroupBoxLandUseMap = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseMap.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseMap.setLayout(self.layoutGroupBoxLandUseMap)
        self.layoutLandUseMapInfo = QtGui.QVBoxLayout()
        self.layoutLandUseMap = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseMap.addLayout(self.layoutLandUseMapInfo)
        self.layoutGroupBoxLandUseMap.addLayout(self.layoutLandUseMap)
        
        self.labelLandUseMapInfo = QtGui.QLabel()
        self.labelLandUseMapInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseMapInfo.addWidget(self.labelLandUseMapInfo)
        
        self.labelOCMLandUseT1 = QtGui.QLabel(parent)
        self.labelOCMLandUseT1.setText('T1:')
        self.layoutLandUseMap.addWidget(self.labelOCMLandUseT1, 0, 0)
        
        self.lineEditOCMLandUseT1 = QtGui.QLineEdit(parent)
        self.lineEditOCMLandUseT1.setReadOnly(True)
        self.layoutLandUseMap.addWidget(self.lineEditOCMLandUseT1, 0, 1)
        
        self.buttonSelectOCMLandUseT1 = QtGui.QPushButton(parent)
        self.buttonSelectOCMLandUseT1.setText('&Browse')
        self.layoutLandUseMap.addWidget(self.buttonSelectOCMLandUseT1, 0, 2)
        
        self.labelOCMLandUseT2 = QtGui.QLabel(parent)
        self.labelOCMLandUseT2.setText('T2:')
        self.layoutLandUseMap.addWidget(self.labelOCMLandUseT2, 1, 0)
        
        self.lineEditOCMLandUseT2 = QtGui.QLineEdit(parent)
        self.lineEditOCMLandUseT2.setReadOnly(True)
        self.layoutLandUseMap.addWidget(self.lineEditOCMLandUseT2, 1, 1)
        
        self.buttonSelectOCMLandUseT2 = QtGui.QPushButton(parent)
        self.buttonSelectOCMLandUseT2.setText('&Browse')
        self.layoutLandUseMap.addWidget(self.buttonSelectOCMLandUseT2, 1, 2)
        
        # 'Planning unit' GroupBox
        self.groupBoxPlanningUnit = QtGui.QGroupBox('Planning unit')
        self.layoutGroupBoxPlanningUnit = QtGui.QVBoxLayout()
        self.layoutGroupBoxPlanningUnit.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxPlanningUnit.setLayout(self.layoutGroupBoxPlanningUnit)
        self.layoutPlanningUnitInfo = QtGui.QVBoxLayout()
        self.layoutPlanningUnit = QtGui.QGridLayout()
        self.layoutGroupBoxPlanningUnit.addLayout(self.layoutPlanningUnitInfo)
        self.layoutGroupBoxPlanningUnit.addLayout(self.layoutPlanningUnit)
        
        self.labelPlanningUnitInfo = QtGui.QLabel()
        self.labelPlanningUnitInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutPlanningUnitInfo.addWidget(self.labelPlanningUnitInfo)
        
        self.labelOCMPlanningUnit = QtGui.QLabel()
        self.labelOCMPlanningUnit.setText('Planning unit map:')
        self.layoutPlanningUnit.addWidget(self.labelOCMPlanningUnit, 0, 0)
        
        self.lineEditOCMPlanningUnit = QtGui.QLineEdit()
        self.lineEditOCMPlanningUnit.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditOCMPlanningUnit, 0, 1)
        
        self.buttonSelectOCMPlanningUnit = QtGui.QPushButton()
        self.buttonSelectOCMPlanningUnit.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectOCMPlanningUnit, 0, 2)
        
        self.labelOCMCsvPlanningUnit = QtGui.QLabel()
        self.labelOCMCsvPlanningUnit.setText('Planning unit lookup table:')
        self.layoutPlanningUnit.addWidget(self.labelOCMCsvPlanningUnit, 1, 0)
        
        self.lineEditOCMCsvPlanningUnit = QtGui.QLineEdit()
        self.lineEditOCMCsvPlanningUnit.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditOCMCsvPlanningUnit, 1, 1)
        
        self.buttonSelectOCMCsvPlanningUnit = QtGui.QPushButton()
        self.buttonSelectOCMCsvPlanningUnit.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectOCMCsvPlanningUnit, 1, 2)
        
        # 'Other' GroupBox
        self.groupBoxOCMOther = QtGui.QGroupBox('Other')
        self.layoutGroupBoxOCMOther = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCMOther.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCMOther.setLayout(self.layoutGroupBoxOCMOther)
        self.layoutOCMOtherInfo = QtGui.QVBoxLayout()
        self.layoutOCMOther = QtGui.QGridLayout()
        self.layoutGroupBoxOCMOther.addLayout(self.layoutOCMOtherInfo)
        self.layoutGroupBoxOCMOther.addLayout(self.layoutOCMOther)
        
        self.labelOCMOtherInfo = QtGui.QLabel()
        self.labelOCMOtherInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOCMOtherInfo.addWidget(self.labelOCMOtherInfo)
        
        self.labelOCMWorkingDir = QtGui.QLabel(parent)
        self.labelOCMWorkingDir.setText('Working directory:')
        self.layoutOCMOther.addWidget(self.labelOCMWorkingDir, 0, 0)
        
        self.lineEditOCMWorkingDir = QtGui.QLineEdit()
        self.lineEditOCMWorkingDir.setReadOnly(True)
        self.layoutOCMOther.addWidget(self.lineEditOCMWorkingDir, 0, 1)
        
        self.buttonSelectOCMWorkingDir = QtGui.QPushButton()
        self.buttonSelectOCMWorkingDir.setText('&Browse')
        self.layoutOCMOther.addWidget(self.buttonSelectOCMWorkingDir, 0, 2)
        
        self.labelOCMLocation = QtGui.QLabel()
        self.labelOCMLocation.setText('&Location:')
        self.layoutOCMOther.addWidget(self.labelOCMLocation, 1, 0)
        
        self.lineEditOCMLocation = QtGui.QLineEdit()
        self.lineEditOCMLocation.setText('location')
        self.layoutOCMOther.addWidget(self.lineEditOCMLocation, 1, 1)
        self.labelOCMLocation.setBuddy(self.lineEditOCMLocation)
        
        self.labelOCMCsvCarbon = QtGui.QLabel()
        self.labelOCMCsvCarbon.setText('Carbon lookup table:')
        self.layoutOCMOther.addWidget(self.labelOCMCsvCarbon, 2, 0)
        
        self.lineEditOCMCsvCarbon = QtGui.QLineEdit()
        self.lineEditOCMCsvCarbon.setReadOnly(True)
        self.layoutOCMOther.addWidget(self.lineEditOCMCsvCarbon, 2, 1)
        
        self.buttonSelectOCMCsvCarbon = QtGui.QPushButton()
        self.buttonSelectOCMCsvCarbon.setText('&Browse')
        self.layoutOCMOther.addWidget(self.buttonSelectOCMCsvCarbon, 2, 2)
        
        self.labelOCMCsvProfitability = QtGui.QLabel(parent)
        self.labelOCMCsvProfitability.setText('Profitability lookup table:')
        self.layoutOCMOther.addWidget(self.labelOCMCsvProfitability, 3, 0)
        
        self.lineEditOCMCsvProfitability = QtGui.QLineEdit(parent)
        self.lineEditOCMCsvProfitability.setReadOnly(True)
        self.layoutOCMOther.addWidget(self.lineEditOCMCsvProfitability, 3, 1)
        
        self.buttonSelectOCMCsvProfitability = QtGui.QPushButton()
        self.buttonSelectOCMCsvProfitability.setText('&Browse')
        self.layoutOCMOther.addWidget(self.buttonSelectOCMCsvProfitability, 3, 2)
        
        # Process tab button
        self.layoutButtonOpportunityCostMap = QtGui.QHBoxLayout()
        self.buttonProcessOpportunityCostMap = QtGui.QPushButton()
        self.buttonProcessOpportunityCostMap.setText('&Process')
        self.layoutButtonOpportunityCostMap.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonOpportunityCostMap.addWidget(self.buttonProcessOpportunityCostMap)
        
        # Template GroupBox
        self.groupBoxOpportunityCostMapTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxOpportunityCostMapTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOpportunityCostMapTemplate.setLayout(self.layoutGroupBoxOpportunityCostMapTemplate)
        self.layoutOpportunityCostMapTemplateInfo = QtGui.QVBoxLayout()
        self.layoutOpportunityCostMapTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplateInfo)
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplate)
        
        self.labelLoadedOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelLoadedOpportunityCostMapTemplate.setText('Loaded template:')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelLoadedOpportunityCostMapTemplate, 0, 0)
        
        self.loadedOpportunityCostMapTemplate = QtGui.QLabel()
        self.loadedOpportunityCostMapTemplate.setText('<None>')
        self.layoutOpportunityCostMapTemplate.addWidget(self.loadedOpportunityCostMapTemplate, 0, 1)
        
        self.labelOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelOpportunityCostMapTemplate.setText('Template name:')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelOpportunityCostMapTemplate, 1, 0)
        
        self.comboBoxOpportunityCostMapTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        self.comboBoxOpportunityCostMapTemplate.addItem('No template found')
        self.layoutOpportunityCostMapTemplate.addWidget(self.comboBoxOpportunityCostMapTemplate, 1, 1)
        
        self.layoutButtonOpportunityCostMapTemplate = QtGui.QHBoxLayout()
        self.layoutButtonOpportunityCostMapTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonLoadOpportunityCostMapTemplate.setDisabled(True)
        self.buttonLoadOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadOpportunityCostMapTemplate.setText('Load')
        self.buttonSaveOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonSaveOpportunityCostMapTemplate.setDisabled(True)
        self.buttonSaveOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveOpportunityCostMapTemplate.setText('Save')
        self.buttonSaveAsOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonSaveAsOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsOpportunityCostMapTemplate.setText('Save As')
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonLoadOpportunityCostMapTemplate)
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonSaveOpportunityCostMapTemplate)
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonSaveAsOpportunityCostMapTemplate)
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutButtonOpportunityCostMapTemplate)
        
        # Place the GroupBoxes
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOCMPeriod, 0, 0)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxLandUseMap, 1, 0)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxPlanningUnit, 2, 0)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOCMOther, 3, 0)
        self.layoutTabOpportunityCostMap.addLayout(self.layoutButtonOpportunityCostMap, 4, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOpportunityCostMapTemplate, 0, 1, 4, 1)
        self.layoutTabOpportunityCostMap.setColumnStretch(0, 3)
        self.layoutTabOpportunityCostMap.setColumnStretch(1, 1) # Smaller template column
        
        
        #***********************************************************
        # Setup 'Result' tab
        #***********************************************************
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensTAOpportunityCost, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Called when the widget is closed
        """
        super(DialogLumensTAOpportunityCost, self).closeEvent(event)
    
    
    #***********************************************************
    # 'Abacus Opportunity Cost' tab QPushButton handlers
    #***********************************************************
    def handlerLoadAbacusOpportunityCostTemplate(self, fileName=None):
        """
        """
        templateFile = self.comboBoxAbacusOpportunityCostTemplate.currentText()
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
            self.loadTemplate('Abacus Opportunity Cost', templateFile)
            self.currentAbacusOpportunityCostTemplate = templateFile
            self.loadedAbacusOpportunityCostTemplate.setText(templateFile)
            self.comboBoxAbacusOpportunityCostTemplate.setCurrentIndex(self.comboBoxAbacusOpportunityCostTemplate.findText(templateFile))
            self.buttonSaveAbacusOpportunityCostTemplate.setEnabled(True)
    
    
    def handlerSaveAbacusOpportunityCostTemplate(self, fileName=None):
        """
        """
        templateFile = self.currentAbacusOpportunityCostTemplate
        
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
            self.saveTemplate('Abacus Opportunity Cost', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsAbacusOpportunityCostTemplate(self):
        """
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            fileName = fileName + '.ini'
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveAbacusOpportunityCostTemplate(fileName)
            else:
                self.saveTemplate('Abacus Opportunity Cost', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadAbacusOpportunityCostTemplate(fileName)
    
    
    def handlerSelectAOCProjectFile(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Project File', QtCore.QDir.homePath(), 'Project File (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditAOCProjectFile.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'Opportunity Cost Curve' tab QPushButton handlers
    #***********************************************************
    def handlerLoadOpportunityCostCurveTemplate(self, fileName=None):
        """
        """
        templateFile = self.comboBoxOpportunityCostCurveTemplate.currentText()
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
            self.loadTemplate('Opportunity Cost Curve', templateFile)
            self.currentOpportunityCostCurveTemplate = templateFile
            self.loadedOpportunityCostCurveTemplate.setText(templateFile)
            self.comboBoxOpportunityCostCurveTemplate.setCurrentIndex(self.comboBoxOpportunityCostCurveTemplate.findText(templateFile))
            self.buttonSaveOpportunityCostCurveTemplate.setEnabled(True)
    
    
    def handlerSaveOpportunityCostCurveTemplate(self, fileName=None):
        """
        """
        templateFile = self.currentOpportunityCostCurveTemplate
        
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
            self.saveTemplate('Opportunity Cost Curve', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsOpportunityCostCurveTemplate(self):
        """
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            fileName = fileName + '.ini'
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveOpportunityCostCurveTemplate(fileName)
            else:
                self.saveTemplate('Opportunity Cost Curve', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadOpportunityCostCurveTemplate(fileName)
    
    
    def handlerSelectOCCWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditOCCWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select working directory: %s', dir)
    
    
    def handlerSelectOCCQUESCDatabase(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select QUES-C Database', QtCore.QDir.homePath(), 'QUES-C Database (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if file:
            self.lineEditOCCQUESCDatabase.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCCCsvNPVTable(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select NPV Table', QtCore.QDir.homePath(), 'NPV Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOCCCsvNPVTable.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCCOutputOpportunityCostDatabase(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Opportunity Cost Database Output', QtCore.QDir.homePath(), 'Opportunity Cost Database (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOCCOutputOpportunityCostDatabase.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOCCOutputOpportunityCostReport(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Opportunity Cost Report Output', QtCore.QDir.homePath(), 'Opportunity Cost Report (*{0})'.format(self.main.appSettings['selectHTMLfileExt'])))
        
        if outputfile:
            self.lineEditOCCOutputOpportunityCostReport.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    #***********************************************************
    # 'Opportunity Cost Map' tab QPushButton handlers
    #***********************************************************
    def handlerLoadOpportunityCostMapTemplate(self, fileName=None):
        """
        """
        templateFile = self.comboBoxOpportunityCostMapTemplate.currentText()
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
            self.loadTemplate('Opportunity Cost Map', templateFile)
            self.currentOpportunityCostMapTemplate = templateFile
            self.loadedOpportunityCostMapTemplate.setText(templateFile)
            self.comboBoxOpportunityCostMapTemplate.setCurrentIndex(self.comboBoxOpportunityCostMapTemplate.findText(templateFile))
            self.buttonSaveOpportunityCostMapTemplate.setEnabled(True)
    
    
    def handlerSaveOpportunityCostMapTemplate(self, fileName=None):
        """
        """
        templateFile = self.currentOpportunityCostMapTemplate
        
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
            self.saveTemplate('Opportunity Cost Map', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsOpportunityCostMapTemplate(self):
        """
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            fileName = fileName + '.ini'
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveOpportunityCostMapTemplate(fileName)
            else:
                self.saveTemplate('Opportunity Cost Map', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadOpportunityCostMapTemplate(fileName)
    
    
    def handlerSelectOCMWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditOCMWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select working directory: %s', dir)
    
    
    def handlerSelectOCMLandUseT1(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map T1', QtCore.QDir.homePath(), 'Land Use Map T1 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditOCMLandUseT1.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCMLandUseT2(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map T2', QtCore.QDir.homePath(), 'Land Use Map T2 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditOCMLandUseT2.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCMPlanningUnit(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Map', QtCore.QDir.homePath(), 'Planning Unit Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditOCMPlanningUnit.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCMCsvPlanningUnit(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Lookup Table', QtCore.QDir.homePath(), 'Planning Unit Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOCMCsvPlanningUnit.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCMCsvCarbon(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Carbon Lookup Table', QtCore.QDir.homePath(), 'Carbon Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOCMCsvCarbon.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCMCsvProfitability(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Profitability Lookup Table', QtCore.QDir.homePath(), 'Profitability Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOCMCsvProfitability.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSetings(self):
        """
        """
        # 'Abacus Opportunity Cost' tab fields
        self.main.appSettings['DialogLumensTAAbacusOpportunityCostCurve']['projectFile'] = unicode(self.lineEditAOCProjectFile.text())
        
        # 'Opportunity Cost Curve' tab fields
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['workingDir'] = unicode(self.lineEditOCCWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['QUESCDatabase'] = unicode(self.lineEditOCCQUESCDatabase.text())
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['csvNPVTable'] = unicode(self.lineEditOCCCsvNPVTable.text())
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['period1'] = self.spinBoxOCCPeriod1.value()
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['period2'] = self.spinBoxOCCPeriod2.value()
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['costThreshold'] = self.spinBoxOCCCostThreshold.value()
        
        outputOpportunityCostDatabase = unicode(self.lineEditOCCOutputOpportunityCostDatabase.text())
        outputOpportunityCostReport = unicode(self.lineEditOCCOutputOpportunityCostReport.text())
        
        if not outputOpportunityCostDatabase:
            self.main.appSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostDatabase'] = '__UNSET__'
        
        if not outputOpportunityCostReport:
            self.main.appSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostReport'] = '__UNSET__'
        
        # 'Opportunity Cost Map' tab fields
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['workingDir'] = unicode(self.lineEditOCMWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['landUseT1'] = unicode(self.lineEditOCMLandUseT1.text())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['landUseT2'] = unicode(self.lineEditOCMLandUseT2.text())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['planningUnit'] = unicode(self.lineEditOCMPlanningUnit.text())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['csvPlanningUnit'] = unicode(self.lineEditOCMCsvPlanningUnit.text())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['csvCarbon'] = unicode(self.lineEditOCMCsvCarbon.text())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['csvProfitability'] = unicode(self.lineEditOCMCsvProfitability.text())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['location'] = unicode(self.lineEditOCMLocation.text())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['t1'] = self.spinBoxOCMPeriod1.value()
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['t2'] = self.spinBoxOCMPeriod2.value()
        
    
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
    
    
    def handlerProcessAbacusOpportunityCost(self):
        """
        """
        self.setAppSetings()
        
        formName = 'DialogLumensTAAbacusOpportunityCostCurve'
        algName = 'modeler:abacus_opportunity_cost'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            
            self.buttonProcessAbacusOpportunityCost.setDisabled(True)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['projectFile'],
            )
            
            ##print outputs
            
            self.buttonProcessAbacusOpportunityCost.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    
    
    def handlerProcessOpportunityCostCurve(self):
        """
        """
        self.setAppSetings()
        
        formName = 'DialogLumensTAOpportunityCostCurve'
        algName = 'modeler:opportunity_cost'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            
            self.buttonProcessOpportunityCostCurve.setDisabled(True)
            
            outputOpportunityCostDatabase = self.main.appSettings[formName]['outputOpportunityCostDatabase']
            outputOpportunityCostReport = self.main.appSettings[formName]['outputOpportunityCostReport']
            
            if outputOpportunityCostDatabase == '__UNSET__':
                outputOpportunityCostDatabase = None
            
            if outputOpportunityCostReport == '__UNSET__':
                outputOpportunityCostReport = None
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['workingDir'],
                self.main.appSettings[formName]['QUESCDatabase'],
                self.main.appSettings[formName]['csvNPVTable'],
                self.main.appSettings[formName]['period1'],
                self.main.appSettings[formName]['period2'],
                self.main.appSettings[formName]['costThreshold'],
                outputOpportunityCostDatabase,
                outputOpportunityCostReport,
            )
            
            ##print outputs
            
            self.buttonProcessOpportunityCostCurve.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    
    
    def handlerProcessOpportunityCostMap(self):
        """
        """
        self.setAppSetings()
        
        formName = 'DialogLumensTAOpportunityCostMap'
        algName = 'modeler:opcost_map'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            
            self.buttonProcessOpportunityCostMap.setDisabled(True)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['workingDir'],
                self.main.appSettings[formName]['landUseT1'],
                self.main.appSettings[formName]['landUseT2'],
                self.main.appSettings[formName]['planningUnit'],
                self.main.appSettings[formName]['csvCarbon'],
                self.main.appSettings[formName]['csvProfitability'],
                self.main.appSettings[formName]['csvPlanningUnit'],
                self.main.appSettings[formName]['location'],
                self.main.appSettings[formName]['t1'],
                self.main.appSettings[formName]['t2'],
            )
            
            ##print outputs
            
            self.buttonProcessOpportunityCostMap.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
    