#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
##from qgis.core import *
##from processing.tools import *
from PyQt4 import QtCore, QtGui
import resource


class DialogLumensTAOpportunityCost(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTAOpportunityCost, self).__init__(parent)
        print 'DEBUG: DialogLumensTAOpportunityCost init'
        
        self.main = parent
        self.dialogTitle = 'LUMENS Trade-Off Analysis [Opportunity Cost]'
        
        self.setupUi(self)
        
        self.buttonSelectProjectFile.clicked.connect(self.handlerSelectProjectFile)
    
    
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
        
        self.layoutTabAbacusOpportunityCost = QtGui.QVBoxLayout()
        self.layoutTabOpportunityCostCurve = QtGui.QVBoxLayout()
        self.layoutTabOpportunityCostMap = QtGui.QVBoxLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        
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
        
        self.labelProjectFile = QtGui.QLabel(parent)
        self.labelProjectFile.setText('Abacus project file:')
        self.layoutOther.addWidget(self.labelProjectFile, 0, 0)
        
        self.lineEditProjectFile = QtGui.QLineEdit(parent)
        self.lineEditProjectFile.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditProjectFile, 0, 1)
        
        self.buttonSelectProjectFile = QtGui.QPushButton(parent)
        self.buttonSelectProjectFile.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectProjectFile, 0, 2)
        
        # Process tab button
        self.layoutButtonAbacusOpportunityCost = QtGui.QHBoxLayout()
        self.buttonProcessAbacusOpportunityCost = QtGui.QPushButton()
        self.buttonProcessAbacusOpportunityCost.setText('&Process')
        self.layoutButtonAbacusOpportunityCost.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonAbacusOpportunityCost.addWidget(self.buttonProcessAbacusOpportunityCost)
        
        self.layoutTabAbacusOpportunityCost.addWidget(self.groupBoxOther)
        self.layoutTabAbacusOpportunityCost.addLayout(self.layoutButtonAbacusOpportunityCost)
        
        self.tabAbacusOpportunityCost.setLayout(self.layoutTabAbacusOpportunityCost)
        
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
        
        self.labelQUESCDatabase = QtGui.QLabel(parent)
        self.labelQUESCDatabase.setText('QUES-C Database:')
        self.layoutOCCOther.addWidget(self.labelQUESCDatabase, 1, 0)
        
        self.lineEditQUESCDatabase = QtGui.QLineEdit()
        self.lineEditQUESCDatabase.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditQUESCDatabase, 1, 1)
        
        self.buttonSelectQUESCDatabase = QtGui.QPushButton()
        self.buttonSelectQUESCDatabase.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectQUESCDatabase, 1, 2)
        
        self.labelCsvNPVTable = QtGui.QLabel(parent)
        self.labelCsvNPVTable.setText('Net Present Value (NPV) table:')
        self.layoutOCCOther.addWidget(self.labelCsvNPVTable, 2, 0)
        
        self.lineEditCsvNPVTable = QtGui.QLineEdit(parent)
        self.lineEditCsvNPVTable.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditCsvNPVTable, 2, 1)
        
        self.buttonSelectCsvNPVTable = QtGui.QPushButton()
        self.buttonSelectCsvNPVTable.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectCsvNPVTable, 2, 2)
        
        self.labelSpinBoxCostThreshold = QtGui.QLabel()
        self.labelSpinBoxCostThreshold.setText('Cost &Threshold:')
        self.layoutOCCOther.addWidget(self.labelSpinBoxCostThreshold, 3, 0)
        
        self.spinBoxCostThreshold = QtGui.QSpinBox()
        self.spinBoxCostThreshold.setValue(5)
        self.layoutOCCOther.addWidget(self.spinBoxCostThreshold, 3, 1)
        self.labelSpinBoxCostThreshold.setBuddy(self.spinBoxCostThreshold)
        
        self.labelOutputOpportunityCostDatabase = QtGui.QLabel()
        self.labelOutputOpportunityCostDatabase.setText('[Output] Opportunity cost database:')
        self.layoutOCCOther.addWidget(self.labelOutputOpportunityCostDatabase, 4, 0)
        
        self.lineEditOutputOpportunityCostDatabase = QtGui.QLineEdit()
        self.lineEditOutputOpportunityCostDatabase.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditOutputOpportunityCostDatabase, 4, 1)
        
        self.buttonSelectOutputOpportunityCostDatabase = QtGui.QPushButton(parent)
        self.buttonSelectOutputOpportunityCostDatabase.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectOutputOpportunityCostDatabase, 4, 2)
        
        self.labelOutputOpportunityCostReport = QtGui.QLabel()
        self.labelOutputOpportunityCostReport.setText('[Output] Opportunity cost report:')
        self.layoutOCCOther.addWidget(self.labelOutputOpportunityCostReport, 5, 0)
        
        self.lineEditOutputOpportunityCostReport = QtGui.QLineEdit()
        self.lineEditOutputOpportunityCostReport.setReadOnly(True)
        self.layoutOCCOther.addWidget(self.lineEditOutputOpportunityCostReport, 5, 1)
        
        self.buttonSelectOutputOpportunityCostReport = QtGui.QPushButton(parent)
        self.buttonSelectOutputOpportunityCostReport.setText('&Browse')
        self.layoutOCCOther.addWidget(self.buttonSelectOutputOpportunityCostReport, 5, 2)
        
        # Process tab button
        self.layoutButtonOpportunityCostCurve = QtGui.QHBoxLayout()
        self.buttonProcessOpportunityCostCurve = QtGui.QPushButton()
        self.buttonProcessOpportunityCostCurve.setText('&Process')
        self.layoutButtonOpportunityCostCurve.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonOpportunityCostCurve.addWidget(self.buttonProcessOpportunityCostCurve)
        
        # Place the GroupBoxes
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOCCPeriod)
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOCCOther)
        self.layoutTabOpportunityCostCurve.addLayout(self.layoutButtonOpportunityCostCurve)
        
        self.layoutTabOpportunityCostCurve.setStretchFactor(self.groupBoxOCCPeriod, 1)
        self.layoutTabOpportunityCostCurve.setStretchFactor(self.groupBoxOCCOther, 4)
        
        self.tabOpportunityCostCurve.setLayout(self.layoutTabOpportunityCostCurve)
        
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
        
        self.labelSpinBoxOCMPeriod1 = QtGui.QLabel(parent)
        self.labelSpinBoxOCMPeriod1.setText('T&1:')
        self.layoutOCMPeriod.addWidget(self.labelSpinBoxOCMPeriod1, 0, 0)
        self.spinBoxOCMPeriod1 = QtGui.QSpinBox(parent)
        self.spinBoxOCMPeriod1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxOCMPeriod1.setValue(td.year)
        self.layoutOCMPeriod.addWidget(self.spinBoxOCMPeriod1, 0, 1)
        self.labelSpinBoxOCMPeriod1.setBuddy(self.spinBoxOCMPeriod1)
        
        self.labelSpinBoxOCMPeriod2 = QtGui.QLabel(parent)
        self.labelSpinBoxOCMPeriod2.setText('T&2:')
        self.layoutOCMPeriod.addWidget(self.labelSpinBoxOCMPeriod2, 1, 0)
        self.spinBoxOCMPeriod2 = QtGui.QSpinBox(parent)
        self.spinBoxOCMPeriod2.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxOCMPeriod2.setValue(td.year)
        self.layoutOCMPeriod.addWidget(self.spinBoxOCMPeriod2, 1, 1)
        self.labelSpinBoxOCMPeriod2.setBuddy(self.spinBoxOCMPeriod2)
        
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
        
        self.labelLandUseT1 = QtGui.QLabel(parent)
        self.labelLandUseT1.setText('T1:')
        self.layoutLandUseMap.addWidget(self.labelLandUseT1, 0, 0)
        
        self.lineEditLandUseT1 = QtGui.QLineEdit(parent)
        self.lineEditLandUseT1.setReadOnly(True)
        self.layoutLandUseMap.addWidget(self.lineEditLandUseT1, 0, 1)
        
        self.buttonSelectLandUseT1 = QtGui.QPushButton(parent)
        self.buttonSelectLandUseT1.setText('&Browse')
        self.layoutLandUseMap.addWidget(self.buttonSelectLandUseT1, 0, 2)
        
        self.labelLandUseT2 = QtGui.QLabel(parent)
        self.labelLandUseT2.setText('T2:')
        self.layoutLandUseMap.addWidget(self.labelLandUseT2, 1, 0)
        
        self.lineEditLandUseT2 = QtGui.QLineEdit(parent)
        self.lineEditLandUseT2.setReadOnly(True)
        self.layoutLandUseMap.addWidget(self.lineEditLandUseT2, 1, 1)
        
        self.buttonSelectLandUseT2 = QtGui.QPushButton(parent)
        self.buttonSelectLandUseT2.setText('&Browse')
        self.layoutLandUseMap.addWidget(self.buttonSelectLandUseT2, 1, 2)
        
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
        
        self.labelPlanningUnit = QtGui.QLabel()
        self.labelPlanningUnit.setText('Planning unit map:')
        self.layoutPlanningUnit.addWidget(self.labelPlanningUnit, 0, 0)
        
        self.lineEditPlanningUnit = QtGui.QLineEdit()
        self.lineEditPlanningUnit.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditPlanningUnit, 0, 1)
        
        self.buttonSelectPlanningUnit = QtGui.QPushButton()
        self.buttonSelectPlanningUnit.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectPlanningUnit, 0, 2)
        
        self.labelCsvPlanningUnit = QtGui.QLabel()
        self.labelCsvPlanningUnit.setText('Planning unit lookup table:')
        self.layoutPlanningUnit.addWidget(self.labelCsvPlanningUnit, 1, 0)
        
        self.lineEditCsvPlanningUnit = QtGui.QLineEdit()
        self.lineEditCsvPlanningUnit.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditCsvPlanningUnit, 1, 1)
        
        self.buttonSelectCsvPlanningUnit = QtGui.QPushButton()
        self.buttonSelectCsvPlanningUnit.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectCsvPlanningUnit, 1, 2)
        
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
        
        self.labelLocation = QtGui.QLabel()
        self.labelLocation.setText('&Location:')
        self.layoutOCMOther.addWidget(self.labelLocation, 1, 0)
        
        self.lineEditLocation = QtGui.QLineEdit()
        self.lineEditLocation.setText('location')
        self.layoutOCMOther.addWidget(self.lineEditLocation, 1, 1)
        self.labelLocation.setBuddy(self.lineEditLocation)
        
        self.labelCsvCarbon = QtGui.QLabel()
        self.labelCsvCarbon.setText('Carbon lookup table:')
        self.layoutOCMOther.addWidget(self.labelCsvCarbon, 2, 0)
        
        self.lineEditCsvCarbon = QtGui.QLineEdit()
        self.lineEditCsvCarbon.setReadOnly(True)
        self.layoutOCMOther.addWidget(self.lineEditCsvCarbon, 2, 1)
        
        self.buttonSelectCsvCarbon = QtGui.QPushButton()
        self.buttonSelectCsvCarbon.setText('&Browse')
        self.layoutOCMOther.addWidget(self.buttonSelectCsvCarbon, 2, 2)
        
        self.labelCsvProfitability = QtGui.QLabel(parent)
        self.labelCsvProfitability.setText('Profitability lookup table:')
        self.layoutOCMOther.addWidget(self.labelCsvProfitability, 3, 0)
        
        self.lineEditCsvProfitability = QtGui.QLineEdit(parent)
        self.lineEditCsvProfitability.setReadOnly(True)
        self.layoutOCMOther.addWidget(self.lineEditCsvProfitability, 3, 1)
        
        self.buttonSelectCsvProfitability = QtGui.QPushButton()
        self.buttonSelectCsvProfitability.setText('&Browse')
        self.layoutOCMOther.addWidget(self.buttonSelectCsvProfitability, 3, 2)
        
        # Process tab button
        self.layoutButtonOpportunityCostMap = QtGui.QHBoxLayout()
        self.buttonProcessOpportunityCostMap = QtGui.QPushButton()
        self.buttonProcessOpportunityCostMap.setText('&Process')
        self.layoutButtonOpportunityCostMap.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonOpportunityCostMap.addWidget(self.buttonProcessOpportunityCostMap)
        
        # Place the GroupBoxes
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOCMPeriod)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxLandUseMap)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxPlanningUnit)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOCMOther)
        self.layoutTabOpportunityCostMap.addLayout(self.layoutButtonOpportunityCostMap)
        
        self.tabOpportunityCostMap.setLayout(self.layoutTabOpportunityCostMap)
        
        #***********************************************************
        # Setup 'Result' tab
        #***********************************************************
        self.tabResult.setLayout(self.layoutTabResult)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensTAOpportunityCost, self).showEvent(event)
    
    
    def handlerSelectProjectFile(self):
        """Select Project File
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Project File', QtCore.QDir.homePath(), 'Project File (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditProjectFile.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)