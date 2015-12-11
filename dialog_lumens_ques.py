#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
##from qgis.core import *
##from processing.tools import *
from PyQt4 import QtCore, QtGui
import resource


class DialogLumensQUES(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensQUES, self).__init__(parent)
        print 'DEBUG: DialogLumensQUES init'
        
        self.main = parent
        self.dialogTitle = 'LUMENS Quantification Environmental Services'
        
        self.setupUi(self)
        
        self.checkBoxCarbonAccounting.toggled.connect(self.toggleCarbonAccounting)
        self.checkBoxPeatlandCarbonAccounting.toggled.connect(self.togglePeatlandCarbonAccounting)
        self.checkBoxSummarizeMultiplePeriod.toggled.connect(self.toggleSummarizeMultiplePeriod)
        
        self.checkBoxDominantHRU.toggled.connect(self.toggleDominantHRU)
        self.checkBoxDominantLUSSL.toggled.connect(self.toggleDominantLUSSL)
        self.checkBoxMultipleHRU.toggled.connect(self.toggleMultipleHRU)
        
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabPreQUES = QtGui.QWidget()
        self.tabQUESC = QtGui.QWidget()
        self.tabQUESB = QtGui.QWidget()
        self.tabQUESH = QtGui.QWidget()
        self.tabReclassification = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabPreQUES, 'Pre-QUES')
        self.tabWidget.addTab(self.tabQUESC, 'QUES-C')
        self.tabWidget.addTab(self.tabQUESB, 'QUES-B')
        self.tabWidget.addTab(self.tabQUESH, 'QUES-H')
        self.tabWidget.addTab(self.tabReclassification, 'Reclassification')
        self.tabWidget.addTab(self.tabResult, 'Result')
        
        self.layoutTabPreQUES = QtGui.QVBoxLayout()
        self.layoutTabQUESC = QtGui.QVBoxLayout()
        self.layoutTabQUESB = QtGui.QVBoxLayout()
        self.layoutTabQUESH = QtGui.QVBoxLayout()
        self.layoutTabReclassification = QtGui.QVBoxLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Pre-QUES' tab
        #***********************************************************
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
        
        self.labelWorkingDir = QtGui.QLabel()
        self.labelWorkingDir.setText('Working directory:')
        self.layoutPlanningUnit.addWidget(self.labelWorkingDir, 0, 0)
        self.lineEditWorkingDir = QtGui.QLineEdit()
        self.lineEditWorkingDir.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditWorkingDir, 0, 1)
        self.buttonSelectWorkingDir = QtGui.QPushButton()
        self.buttonSelectWorkingDir.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectWorkingDir, 0, 2)
        
        self.labelLocation = QtGui.QLabel()
        self.labelLocation.setText('&Location:')
        self.layoutPlanningUnit.addWidget(self.labelLocation, 1, 0)
        self.lineEditLocation = QtGui.QLineEdit()
        self.lineEditLocation.setText('location')
        self.layoutPlanningUnit.addWidget(self.lineEditLocation, 1, 1)
        self.labelLocation.setBuddy(self.lineEditLocation)
        
        self.labelPlanningUnit = QtGui.QLabel()
        self.labelPlanningUnit.setText('Planning unit map:')
        self.layoutPlanningUnit.addWidget(self.labelPlanningUnit, 2, 0)
        self.lineEditPlanningUnit = QtGui.QLineEdit()
        self.lineEditPlanningUnit.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditPlanningUnit, 2, 1)
        self.buttonSelectPlanningUnit = QtGui.QPushButton()
        self.buttonSelectPlanningUnit.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectPlanningUnit, 2, 2)
        
        self.labelCsvPlanningUnit = QtGui.QLabel()
        self.labelCsvPlanningUnit.setText('Planning unit lookup table:')
        self.layoutPlanningUnit.addWidget(self.labelCsvPlanningUnit, 3, 0)
        self.lineEditCsvPlanningUnit = QtGui.QLineEdit()
        self.lineEditCsvPlanningUnit.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditCsvPlanningUnit, 3, 1)
        self.buttonSelectCsvPlanningUnit = QtGui.QPushButton()
        self.buttonSelectCsvPlanningUnit.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectCsvPlanningUnit, 3, 2)
        
        #######################################################################
        # 'Land cover' GroupBox
        self.groupBoxLandCover = QtGui.QGroupBox('Land cover')
        self.layoutGroupBoxLandCover = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandCover.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandCover.setLayout(self.layoutGroupBoxLandCover)
        
        self.layoutLandCoverInfo = QtGui.QVBoxLayout()
        self.labelLandCoverInfo = QtGui.QLabel()
        self.labelLandCoverInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandCoverInfo.addWidget(self.labelLandCoverInfo)
        
        self.layoutLandCoverOptions = QtGui.QGridLayout()
        self.layoutLandCoverOptions.setContentsMargins(0, 0, 0, 0)
        self.labelCsvLandUse = QtGui.QLabel()
        self.labelCsvLandUse.setText('Land use lookup table:')
        self.layoutLandCoverOptions.addWidget(self.labelCsvLandUse, 0, 0)
        self.lineEditCsvLandUse = QtGui.QLineEdit()
        self.lineEditCsvLandUse.setReadOnly(True)
        self.layoutLandCoverOptions.addWidget(self.lineEditCsvLandUse, 0, 1)
        self.buttonSelectCsvLandUse = QtGui.QPushButton()
        self.buttonSelectCsvLandUse.setText('&Browse')
        self.layoutLandCoverOptions.addWidget(self.buttonSelectCsvLandUse, 0, 2)
        
        self.layoutContentGroupBoxLandCover = QtGui.QVBoxLayout()
        self.layoutContentGroupBoxLandCover.setContentsMargins(10, 10, 10, 10)
        self.contentGroupBoxLandCover = QtGui.QWidget()
        self.contentGroupBoxLandCover.setLayout(self.layoutContentGroupBoxLandCover)
        self.scrollLandCover = QtGui.QScrollArea()
        self.scrollLandCover.setWidgetResizable(True);
        self.scrollLandCover.setWidget(self.contentGroupBoxLandCover)
        
        self.layoutTableLandCover = QtGui.QVBoxLayout()
        self.layoutTableLandCover.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentGroupBoxLandCover.addLayout(self.layoutTableLandCover)
        
        self.layoutGroupBoxLandCover.addLayout(self.layoutLandCoverInfo)
        self.layoutGroupBoxLandCover.addLayout(self.layoutLandCoverOptions)
        self.layoutGroupBoxLandCover.addSpacing(10)
        self.layoutGroupBoxLandCover.addWidget(self.scrollLandCover)
        
        # Add land cover rows, T1 T2 T3
        self.addLandCoverRow('T1')
        self.addLandCoverRow('T2')
        ##self.addLandCoverRow('T3')
        
        # Process tab button
        self.layoutButtonPreQUES = QtGui.QHBoxLayout()
        self.buttonProcessPreQUES = QtGui.QPushButton()
        self.buttonProcessPreQUES.setText('&Process')
        self.layoutButtonPreQUES.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonPreQUES.addWidget(self.buttonProcessPreQUES)
        
        # Place the GroupBoxes
        self.layoutTabPreQUES.addWidget(self.groupBoxPlanningUnit)
        self.layoutTabPreQUES.addWidget(self.groupBoxLandCover)
        self.layoutTabPreQUES.addLayout(self.layoutButtonPreQUES)
        
        self.tabPreQUES.setLayout(self.layoutTabPreQUES)
        
        #***********************************************************
        # Setup 'QUES-C' tab
        #***********************************************************
        # 'Carbon accounting' GroupBox
        self.groupBoxCarbonAccounting = QtGui.QGroupBox('Carbon accounting')
        self.layoutGroupBoxCarbonAccounting = QtGui.QHBoxLayout()
        self.groupBoxCarbonAccounting.setLayout(self.layoutGroupBoxCarbonAccounting)
        self.layoutOptionsCarbonAccounting = QtGui.QVBoxLayout()
        self.layoutOptionsCarbonAccounting.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsCarbonAccounting = QtGui.QWidget()
        self.contentOptionsCarbonAccounting.setLayout(self.layoutOptionsCarbonAccounting)
        self.layoutOptionsCarbonAccounting.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxCarbonAccounting = QtGui.QCheckBox()
        self.checkBoxCarbonAccounting.setChecked(False)
        self.contentOptionsCarbonAccounting.setDisabled(True)
        self.layoutGroupBoxCarbonAccounting.addWidget(self.checkBoxCarbonAccounting)
        self.layoutGroupBoxCarbonAccounting.addWidget(self.contentOptionsCarbonAccounting)
        self.layoutGroupBoxCarbonAccounting.setAlignment(self.checkBoxCarbonAccounting, QtCore.Qt.AlignTop)
        self.layoutCarbonAccountingInfo = QtGui.QVBoxLayout()
        self.layoutCarbonAccounting = QtGui.QGridLayout()
        self.layoutOptionsCarbonAccounting.addLayout(self.layoutCarbonAccountingInfo)
        self.layoutOptionsCarbonAccounting.addLayout(self.layoutCarbonAccounting)
        
        self.labelCarbonAccountingInfo = QtGui.QLabel()
        self.labelCarbonAccountingInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutCarbonAccountingInfo.addWidget(self.labelCarbonAccountingInfo)
        
        self.labelCACsvfile = QtGui.QLabel()
        self.labelCACsvfile.setText('Carbon density lookup table:')
        self.layoutCarbonAccounting.addWidget(self.labelCACsvfile, 0, 0)
        
        self.lineEditCACsvfile = QtGui.QLineEdit()
        self.lineEditCACsvfile.setReadOnly(True)
        self.layoutCarbonAccounting.addWidget(self.lineEditCACsvfile, 0, 1)
        
        self.buttonSelectCACsvfile = QtGui.QPushButton()
        self.buttonSelectCACsvfile.setText('&Browse')
        self.layoutCarbonAccounting.addWidget(self.buttonSelectCACsvfile, 0, 2)
        
        self.labelSpinBoxNoDataValue = QtGui.QLabel()
        self.labelSpinBoxNoDataValue.setText('&No data value:')
        self.layoutCarbonAccounting.addWidget(self.labelSpinBoxNoDataValue, 1, 0)
        
        self.spinBoxNoDataValue = QtGui.QSpinBox()
        self.spinBoxNoDataValue.setRange(-9999, 9999)
        self.spinBoxNoDataValue.setValue(0)
        self.layoutCarbonAccounting.addWidget(self.spinBoxNoDataValue, 1, 1)
        self.labelSpinBoxNoDataValue.setBuddy(self.spinBoxNoDataValue)
        
        # 'Peatland carbon accounting' GroupBox
        self.groupBoxPeatlandCarbonAccounting = QtGui.QGroupBox('Peatland carbon accounting')
        self.layoutGroupBoxPeatlandCarbonAccounting = QtGui.QHBoxLayout()
        self.groupBoxPeatlandCarbonAccounting.setLayout(self.layoutGroupBoxPeatlandCarbonAccounting)
        self.layoutOptionsPeatlandCarbonAccounting = QtGui.QVBoxLayout()
        self.layoutOptionsPeatlandCarbonAccounting.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsPeatlandCarbonAccounting = QtGui.QWidget()
        self.contentOptionsPeatlandCarbonAccounting.setLayout(self.layoutOptionsPeatlandCarbonAccounting)
        self.layoutOptionsPeatlandCarbonAccounting.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxPeatlandCarbonAccounting = QtGui.QCheckBox()
        self.checkBoxPeatlandCarbonAccounting.setChecked(False)
        self.contentOptionsPeatlandCarbonAccounting.setDisabled(True)
        self.layoutGroupBoxPeatlandCarbonAccounting.addWidget(self.checkBoxPeatlandCarbonAccounting)
        self.layoutGroupBoxPeatlandCarbonAccounting.addWidget(self.contentOptionsPeatlandCarbonAccounting)
        self.layoutGroupBoxPeatlandCarbonAccounting.setAlignment(self.checkBoxPeatlandCarbonAccounting, QtCore.Qt.AlignTop)
        self.layoutPeatlandCarbonAccountingInfo = QtGui.QVBoxLayout()
        self.layoutPeatlandCarbonAccounting = QtGui.QGridLayout()
        self.layoutOptionsPeatlandCarbonAccounting.addLayout(self.layoutPeatlandCarbonAccountingInfo)
        self.layoutOptionsPeatlandCarbonAccounting.addLayout(self.layoutPeatlandCarbonAccounting)
        
        self.labelPeatlandCarbonAccountingInfo = QtGui.QLabel()
        self.labelPeatlandCarbonAccountingInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutPeatlandCarbonAccountingInfo.addWidget(self.labelPeatlandCarbonAccountingInfo)
        
        self.labelPCACsvfile = QtGui.QLabel()
        self.labelPCACsvfile.setText('Carbon stock lookup table:')
        self.layoutPeatlandCarbonAccounting.addWidget(self.labelPCACsvfile, 0, 0)
        
        self.lineEditPCACsvfile = QtGui.QLineEdit()
        self.lineEditPCACsvfile.setReadOnly(True)
        self.layoutPeatlandCarbonAccounting.addWidget(self.lineEditPCACsvfile, 0, 1)
        
        self.buttonSelectPCACsvfile = QtGui.QPushButton()
        self.buttonSelectPCACsvfile.setText('&Browse')
        self.layoutPeatlandCarbonAccounting.addWidget(self.buttonSelectPCACsvfile, 0, 2)
        
        # 'Summarize multiple period' GroupBox
        self.groupBoxSummarizeMultiplePeriod = QtGui.QGroupBox('Summarize multiple period')
        self.layoutGroupBoxSummarizeMultiplePeriod = QtGui.QHBoxLayout()
        self.groupBoxSummarizeMultiplePeriod.setLayout(self.layoutGroupBoxSummarizeMultiplePeriod)
        self.layoutOptionsSummarizeMultiplePeriod = QtGui.QVBoxLayout()
        self.layoutOptionsSummarizeMultiplePeriod.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsSummarizeMultiplePeriod = QtGui.QWidget()
        self.contentOptionsSummarizeMultiplePeriod.setLayout(self.layoutOptionsSummarizeMultiplePeriod)
        self.layoutOptionsSummarizeMultiplePeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxSummarizeMultiplePeriod = QtGui.QCheckBox()
        self.checkBoxSummarizeMultiplePeriod.setChecked(False)
        self.contentOptionsSummarizeMultiplePeriod.setDisabled(True)
        self.layoutGroupBoxSummarizeMultiplePeriod.addWidget(self.checkBoxSummarizeMultiplePeriod)
        self.layoutGroupBoxSummarizeMultiplePeriod.addWidget(self.contentOptionsSummarizeMultiplePeriod)
        self.layoutGroupBoxSummarizeMultiplePeriod.insertStretch(2, 1)
        self.layoutGroupBoxSummarizeMultiplePeriod.setAlignment(self.checkBoxSummarizeMultiplePeriod, QtCore.Qt.AlignTop)
        self.layoutSummarizeMultiplePeriodInfo = QtGui.QVBoxLayout()
        self.layoutSummarizeMultiplePeriod = QtGui.QGridLayout()
        self.layoutOptionsSummarizeMultiplePeriod.addLayout(self.layoutSummarizeMultiplePeriodInfo)
        self.layoutOptionsSummarizeMultiplePeriod.addLayout(self.layoutSummarizeMultiplePeriod)
        
        self.labelSummarizeMultiplePeriodInfo = QtGui.QLabel()
        self.labelSummarizeMultiplePeriodInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutSummarizeMultiplePeriodInfo.addWidget(self.labelSummarizeMultiplePeriodInfo)
        
        self.labelSMPCheckBox = QtGui.QLabel()
        self.labelSMPCheckBox.setText('Include &peat:')
        self.layoutSummarizeMultiplePeriod.addWidget(self.labelSMPCheckBox, 0, 0)
        
        self.SMPCheckBox = QtGui.QCheckBox()
        self.SMPCheckBox.setChecked(True)
        self.layoutSummarizeMultiplePeriod.addWidget(self.SMPCheckBox, 0, 1)
        self.labelSMPCheckBox.setBuddy(self.SMPCheckBox)
        
        # Process tab button
        self.layoutButtonQUESC = QtGui.QHBoxLayout()
        self.buttonProcessQUESC = QtGui.QPushButton()
        self.buttonProcessQUESC.setText('&Process')
        self.layoutButtonQUESC.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonQUESC.addWidget(self.buttonProcessQUESC)
        
        # Place the GroupBoxes
        self.layoutTabQUESC.addWidget(self.groupBoxCarbonAccounting)
        self.layoutTabQUESC.addWidget(self.groupBoxPeatlandCarbonAccounting)
        self.layoutTabQUESC.addWidget(self.groupBoxSummarizeMultiplePeriod)
        self.layoutTabQUESC.addLayout(self.layoutButtonQUESC)
        
        self.tabQUESC.setLayout(self.layoutTabQUESC)
        
        #***********************************************************
        # Setup 'QUES-B' tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxParameters.setLayout(self.layoutGroupBoxParameters)
        self.layoutParametersInfo = QtGui.QVBoxLayout()
        self.layoutParameters = QtGui.QGridLayout()
        self.layoutGroupBoxParameters.addLayout(self.layoutParametersInfo)
        self.layoutGroupBoxParameters.addLayout(self.layoutParameters)
        
        self.labelParametersInfo = QtGui.QLabel()
        self.labelParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutParametersInfo.addWidget(self.labelParametersInfo)
        
        self.labelCsvLandCover = QtGui.QLabel()
        self.labelCsvLandCover.setText('Land cover lookup:')
        self.layoutParameters.addWidget(self.labelCsvLandCover, 0, 0)
        
        self.lineEditCsvLandCover = QtGui.QLineEdit()
        self.lineEditCsvLandCover.setReadOnly(True)
        self.layoutParameters.addWidget(self.lineEditCsvLandCover, 0, 1)
        
        self.buttonSelectCsvLandCover = QtGui.QPushButton()
        self.buttonSelectCsvLandCover.setText('&Browse')
        self.layoutParameters.addWidget(self.buttonSelectCsvLandCover, 0, 2)
        
        self.labelSpinBoxSamplingGridRes = QtGui.QLabel()
        self.labelSpinBoxSamplingGridRes.setText('Sampling grid &resolution:')
        self.layoutParameters.addWidget(self.labelSpinBoxSamplingGridRes, 1, 0)
        
        self.spinBoxSamplingGridRes = QtGui.QSpinBox()
        self.spinBoxSamplingGridRes.setRange(1, 9999)
        self.spinBoxSamplingGridRes.setValue(10000)
        self.layoutParameters.addWidget(self.spinBoxSamplingGridRes, 1, 1)
        self.labelSpinBoxSamplingGridRes.setBuddy(self.spinBoxSamplingGridRes)
        
        self.labelSpinBoxSamplingWindowSize = QtGui.QLabel()
        self.labelSpinBoxSamplingWindowSize.setText('Sampling &window size:')
        self.layoutParameters.addWidget(self.labelSpinBoxSamplingWindowSize, 2, 0)
        
        self.spinBoxSamplingWindowSize = QtGui.QSpinBox()
        self.spinBoxSamplingWindowSize.setRange(1, 9999)
        self.spinBoxSamplingWindowSize.setValue(1000)
        self.layoutParameters.addWidget(self.spinBoxSamplingWindowSize, 2, 1)
        
        self.labelSpinBoxSamplingWindowSize.setBuddy(self.spinBoxSamplingWindowSize)
        
        self.labelSpinBoxWindowShape = QtGui.QLabel()
        self.labelSpinBoxWindowShape.setText('Window &shape:')
        self.layoutParameters.addWidget(self.labelSpinBoxWindowShape, 3, 0)
        
        self.spinBoxWindowShape = QtGui.QSpinBox()
        self.spinBoxWindowShape.setRange(1, 9999)
        self.spinBoxWindowShape.setValue(1)
        self.layoutParameters.addWidget(self.spinBoxWindowShape, 3, 1)
        self.labelSpinBoxWindowShape.setBuddy(self.spinBoxWindowShape)
        
        self.labelSpinBoxNodata = QtGui.QLabel()
        self.labelSpinBoxNodata.setText('&No data value:')
        self.layoutParameters.addWidget(self.labelSpinBoxNodata, 4, 0)
        
        self.spinBoxNodata = QtGui.QSpinBox()
        self.spinBoxNodata.setRange(-9999, 9999)
        self.spinBoxNodata.setValue(0)
        self.layoutParameters.addWidget(self.spinBoxNodata, 4, 1)
        
        self.labelSpinBoxNodata.setBuddy(self.spinBoxNodata)
        
        self.labelCsvClassDescriptors = QtGui.QLabel()
        self.labelCsvClassDescriptors.setText('Class descriptors:')
        self.layoutParameters.addWidget(self.labelCsvClassDescriptors, 5, 0)
        
        self.lineEditCsvClassDescriptors = QtGui.QLineEdit()
        self.lineEditCsvClassDescriptors.setReadOnly(True)
        self.layoutParameters.addWidget(self.lineEditCsvClassDescriptors, 5, 1)
        
        self.buttonSelectCsvClassDescriptors = QtGui.QPushButton()
        self.buttonSelectCsvClassDescriptors.setText('&Browse')
        self.layoutParameters.addWidget(self.buttonSelectCsvClassDescriptors, 5, 2)
        
        self.labelCsvEdgeContrast = QtGui.QLabel()
        self.labelCsvEdgeContrast.setText('Edge contrast:')
        self.layoutParameters.addWidget(self.labelCsvEdgeContrast, 6, 0)
        
        self.lineEditCsvEdgeContrast = QtGui.QLineEdit()
        self.lineEditCsvEdgeContrast.setReadOnly(True)
        self.layoutParameters.addWidget(self.lineEditCsvEdgeContrast, 6, 1)
        
        self.buttonSelectCsvEdgeContrast = QtGui.QPushButton()
        self.buttonSelectCsvEdgeContrast.setText('&Browse')
        self.layoutParameters.addWidget(self.buttonSelectCsvEdgeContrast, 6, 2)
        
        self.labelCsvZoneLookup = QtGui.QLabel()
        self.labelCsvZoneLookup.setText('Zone lookup:')
        self.layoutParameters.addWidget(self.labelCsvZoneLookup, 7, 0)
        
        self.lineEditCsvZoneLookup = QtGui.QLineEdit()
        self.lineEditCsvZoneLookup.setReadOnly(True)
        self.layoutParameters.addWidget(self.lineEditCsvZoneLookup, 7, 1)
        
        self.buttonSelectCsvZoneLookup = QtGui.QPushButton()
        self.buttonSelectCsvZoneLookup.setText('&Browse')
        self.layoutParameters.addWidget(self.buttonSelectCsvZoneLookup, 7, 2)
        
        self.labelSpinBoxRefMapID = QtGui.QLabel()
        self.labelSpinBoxRefMapID.setText('Reference map ID:')
        self.layoutParameters.addWidget(self.labelSpinBoxRefMapID, 8, 0)
        
        refMapID = {
            1: 'Land cover T1',
            2: 'Land cover T2',
            3: 'Zone',
        }
        
        self.comboBoxRefMapID = QtGui.QComboBox()
        
        for key, val in refMapID.iteritems():
            self.comboBoxRefMapID.addItem(val, key)
        self.layoutParameters.addWidget(self.comboBoxRefMapID, 8, 1)
        
        # 'Output' GroupBox
        self.groupBoxOutput = QtGui.QGroupBox('Output')
        self.layoutGroupBoxOutput = QtGui.QVBoxLayout()
        self.layoutGroupBoxOutput.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOutput.setLayout(self.layoutGroupBoxOutput)
        self.layoutOutputInfo = QtGui.QVBoxLayout()
        self.layoutOutput = QtGui.QGridLayout()
        self.layoutGroupBoxOutput.addLayout(self.layoutOutputInfo)
        self.layoutGroupBoxOutput.addLayout(self.layoutOutput)
        
        self.labelOutputInfo = QtGui.QLabel()
        self.labelOutputInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOutputInfo.addWidget(self.labelOutputInfo)
        
        self.labelOutputTECIInitial = QtGui.QLabel()
        self.labelOutputTECIInitial.setText('[Output] TECI initial:')
        self.layoutOutput.addWidget(self.labelOutputTECIInitial, 0, 0)
        
        self.lineEditOutputTECIInitial = QtGui.QLineEdit()
        self.lineEditOutputTECIInitial.setReadOnly(True)
        self.layoutOutput.addWidget(self.lineEditOutputTECIInitial, 0, 1)
        
        self.buttonSelectOutputTECIInitial = QtGui.QPushButton()
        self.buttonSelectOutputTECIInitial.setText('&Browse')
        self.layoutOutput.addWidget(self.buttonSelectOutputTECIInitial, 0, 2)
        
        self.labelOutputTECIFinal = QtGui.QLabel()
        self.labelOutputTECIFinal.setText('[Output] TECI final:')
        self.layoutOutput.addWidget(self.labelOutputTECIFinal, 1, 0)
        
        self.lineEditOutputTECIFinal = QtGui.QLineEdit()
        self.lineEditOutputTECIFinal.setReadOnly(True)
        self.layoutOutput.addWidget(self.lineEditOutputTECIFinal, 1, 1)
        
        self.buttonSelectOutputTECIFinal = QtGui.QPushButton()
        self.buttonSelectOutputTECIFinal.setText('&Browse')
        self.layoutOutput.addWidget(self.buttonSelectOutputTECIFinal, 1, 2)
        
        self.labelOutputHabitatLoss = QtGui.QLabel()
        self.labelOutputHabitatLoss.setText('[Output] Habitat Loss:')
        self.layoutOutput.addWidget(self.labelOutputHabitatLoss, 2, 0)
        
        self.lineEditOutputHabitatLoss = QtGui.QLineEdit()
        self.lineEditOutputHabitatLoss.setReadOnly(True)
        self.layoutOutput.addWidget(self.lineEditOutputHabitatLoss, 2, 1)
        
        self.buttonSelectOutputHabitatLoss = QtGui.QPushButton()
        self.buttonSelectOutputHabitatLoss.setText('&Browse')
        self.layoutOutput.addWidget(self.buttonSelectOutputHabitatLoss, 2, 2)
        
        self.labelOutputDegradedHabitat = QtGui.QLabel()
        self.labelOutputDegradedHabitat.setText('[Output] Degraded habitat:')
        self.layoutOutput.addWidget(self.labelOutputDegradedHabitat, 3, 0)
        
        self.lineEditOutputDegradedHabitat = QtGui.QLineEdit()
        self.lineEditOutputDegradedHabitat.setReadOnly(True)
        self.layoutOutput.addWidget(self.lineEditOutputDegradedHabitat, 3, 1)
        
        self.buttonSelectOutputDegradedHabitat = QtGui.QPushButton()
        self.buttonSelectOutputDegradedHabitat.setText('&Browse')
        self.layoutOutput.addWidget(self.buttonSelectOutputDegradedHabitat, 3, 2)
        
        self.labelOutputHabitatGain = QtGui.QLabel()
        self.labelOutputHabitatGain.setText('[Output] Habitat gain:')
        self.layoutOutput.addWidget(self.labelOutputHabitatGain, 4, 0)
        
        self.lineEditOutputHabitatGain = QtGui.QLineEdit()
        self.lineEditOutputHabitatGain.setReadOnly(True)
        self.layoutOutput.addWidget(self.lineEditOutputHabitatGain, 4, 1)
        
        self.buttonSelectOutputHabitatGain = QtGui.QPushButton()
        self.buttonSelectOutputHabitatGain.setText('&Browse')
        self.layoutOutput.addWidget(self.buttonSelectOutputHabitatGain, 4, 2)
        
        self.labelOutputRecoveredHabitat = QtGui.QLabel()
        self.labelOutputRecoveredHabitat.setText('[Output] Recovered habitat:')
        self.layoutOutput.addWidget(self.labelOutputRecoveredHabitat, 5, 0)
        
        self.lineEditOutputRecoveredHabitat = QtGui.QLineEdit()
        self.lineEditOutputRecoveredHabitat.setReadOnly(True)
        self.layoutOutput.addWidget(self.lineEditOutputRecoveredHabitat, 5, 1)
        
        self.buttonSelectOutputRecoveredHabitat = QtGui.QPushButton()
        self.buttonSelectOutputRecoveredHabitat.setText('&Browse')
        self.layoutOutput.addWidget(self.buttonSelectOutputRecoveredHabitat, 5, 2)
        
        # Process tab button
        self.layoutButtonQUESB = QtGui.QHBoxLayout()
        self.buttonProcessQUESB = QtGui.QPushButton()
        self.buttonProcessQUESB.setText('&Process')
        self.layoutButtonQUESB.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonQUESB.addWidget(self.buttonProcessQUESB)
        
        # Place the GroupBoxes
        self.layoutTabQUESB.addWidget(self.groupBoxParameters)
        self.layoutTabQUESB.addWidget(self.groupBoxOutput)
        self.layoutTabQUESB.addLayout(self.layoutButtonQUESB)
        
        self.tabQUESB.setLayout(self.layoutTabQUESB)
        
        #***********************************************************
        # Setup 'QUES-H' tab
        #***********************************************************
        self.tabQUESH.setLayout(self.layoutTabQUESH)
        
        self.tabWidgetQUESH = QtGui.QTabWidget()
        
        self.tabWatershedDelineation = QtGui.QWidget()
        self.tabHRUDefinition = QtGui.QWidget()
        self.tabWatershedModelEvaluation = QtGui.QWidget()
        self.tabWatershedIndicators = QtGui.QWidget()
        
        self.tabWidgetQUESH.addTab(self.tabWatershedDelineation, 'Watershed Delineation')
        self.tabWidgetQUESH.addTab(self.tabHRUDefinition, 'Hydrological Response Unit Definition')
        self.tabWidgetQUESH.addTab(self.tabWatershedModelEvaluation, 'Watershed Model Evaluation')
        self.tabWidgetQUESH.addTab(self.tabWatershedIndicators, 'Watershed Indicators')
        
        self.layoutTabQUESH.addWidget(self.tabWidgetQUESH)
        
        self.layoutTabWatershedDelineation = QtGui.QVBoxLayout()
        self.layoutTabHRUDefinition = QtGui.QVBoxLayout()
        self.layoutTabWatershedModelEvaluation = QtGui.QVBoxLayout()
        self.layoutTabWatershedIndicators = QtGui.QVBoxLayout()
        
        self.tabWatershedDelineation.setLayout(self.layoutTabWatershedDelineation)
        self.tabHRUDefinition.setLayout(self.layoutTabHRUDefinition)
        self.tabWatershedModelEvaluation.setLayout(self.layoutTabWatershedModelEvaluation)
        self.tabWatershedIndicators.setLayout(self.layoutTabWatershedIndicators)
        
        # 'Hydrological Response Unit Definition' sub tab
        self.layoutContentHRUDefinition = QtGui.QVBoxLayout()
        self.contentHRUDefinition = QtGui.QWidget()
        self.contentHRUDefinition.setLayout(self.layoutContentHRUDefinition)
        self.scrollHRUDefinition = QtGui.QScrollArea()
        self.scrollHRUDefinition.setWidgetResizable(True);
        self.scrollHRUDefinition.setWidget(self.contentHRUDefinition)
        self.layoutTabHRUDefinition.addWidget(self.scrollHRUDefinition)
        
        # 'Dominant HRU' GroupBox
        self.groupBoxDominantHRU = QtGui.QGroupBox('Dominant HRU')
        self.layoutGroupBoxDominantHRU = QtGui.QHBoxLayout()
        self.groupBoxDominantHRU.setLayout(self.layoutGroupBoxDominantHRU)
        self.layoutOptionsDominantHRU = QtGui.QVBoxLayout()
        self.layoutOptionsDominantHRU.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsDominantHRU = QtGui.QWidget()
        self.contentOptionsDominantHRU.setLayout(self.layoutOptionsDominantHRU)
        self.layoutOptionsDominantHRU.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxDominantHRU = QtGui.QCheckBox()
        self.checkBoxDominantHRU.setChecked(False)
        self.contentOptionsDominantHRU.setDisabled(True)
        self.layoutGroupBoxDominantHRU.addWidget(self.checkBoxDominantHRU)
        self.layoutGroupBoxDominantHRU.addWidget(self.contentOptionsDominantHRU)
        self.layoutGroupBoxDominantHRU.setAlignment(self.checkBoxDominantHRU, QtCore.Qt.AlignTop)
        self.layoutDominantHRUInfo = QtGui.QVBoxLayout()
        self.layoutDominantHRU = QtGui.QGridLayout()
        self.layoutOptionsDominantHRU.addLayout(self.layoutDominantHRUInfo)
        self.layoutOptionsDominantHRU.addLayout(self.layoutDominantHRU)
        
        self.labelDominantHRUInfo = QtGui.QLabel()
        self.labelDominantHRUInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutDominantHRUInfo.addWidget(self.labelDominantHRUInfo)
        
        self.labelDominantHRUWorkingDir = QtGui.QLabel()
        self.labelDominantHRUWorkingDir.setText('Working directory:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRUWorkingDir, 0, 0)
        
        self.lineEditDominantHRUWorkingDir = QtGui.QLineEdit()
        self.lineEditDominantHRUWorkingDir.setReadOnly(True)
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRUWorkingDir, 0, 1)
        
        self.buttonSelectDominantHRUWorkingDir = QtGui.QPushButton()
        self.buttonSelectDominantHRUWorkingDir.setText('&Browse')
        self.layoutDominantHRU.addWidget(self.buttonSelectDominantHRUWorkingDir, 0, 2)
        
        self.labelDominantHRULandUseMap = QtGui.QLabel()
        self.labelDominantHRULandUseMap.setText('Land use map:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRULandUseMap, 1, 0)
        
        self.lineEditDominantHRULandUseMap = QtGui.QLineEdit()
        self.lineEditDominantHRULandUseMap.setReadOnly(True)
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRULandUseMap, 1, 1)
        
        self.buttonSelectDominantHRULandUseMap = QtGui.QPushButton()
        self.buttonSelectDominantHRULandUseMap.setText('&Browse')
        self.layoutDominantHRU.addWidget(self.buttonSelectDominantHRULandUseMap, 1, 2)
        
        self.labelDominantHRUSoilMap = QtGui.QLabel()
        self.labelDominantHRUSoilMap.setText('Soil map:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRUSoilMap, 2, 0)
        
        self.lineEditDominantHRUSoilMap = QtGui.QLineEdit()
        self.lineEditDominantHRUSoilMap.setReadOnly(True)
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRUSoilMap, 2, 1)
        
        self.buttonSelectDominantHRUSoilMap = QtGui.QPushButton()
        self.buttonSelectDominantHRUSoilMap.setText('&Browse')
        self.layoutDominantHRU.addWidget(self.buttonSelectDominantHRUSoilMap, 2, 2)
        
        self.labelDominantHRUSlopeMap = QtGui.QLabel()
        self.labelDominantHRUSlopeMap.setText('Slope map:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRUSlopeMap, 3, 0)
        
        self.lineEditDominantHRUSlopeMap = QtGui.QLineEdit()
        self.lineEditDominantHRUSlopeMap.setReadOnly(True)
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRUSlopeMap, 3, 1)
        
        self.buttonSelectDominantHRUSlopeMap = QtGui.QPushButton()
        self.buttonSelectDominantHRUSlopeMap.setText('&Browse')
        self.layoutDominantHRU.addWidget(self.buttonSelectDominantHRUSlopeMap, 3, 2)
        
        self.labelDominantHRUSubcatchmentMap = QtGui.QLabel()
        self.labelDominantHRUSubcatchmentMap.setText('Subcatchment map:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRUSubcatchmentMap, 4, 0)
        
        self.lineEditDominantHRUSubcatchmentMap = QtGui.QLineEdit()
        self.lineEditDominantHRUSubcatchmentMap.setReadOnly(True)
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRUSubcatchmentMap, 4, 1)
        
        self.buttonSelectDominantHRUSubcatchmentMap = QtGui.QPushButton()
        self.buttonSelectDominantHRUSubcatchmentMap.setText('&Browse')
        self.layoutDominantHRU.addWidget(self.buttonSelectDominantHRUSubcatchmentMap, 4, 2)
        
        self.labelDominantHRULandUseClassification = QtGui.QLabel()
        self.labelDominantHRULandUseClassification.setText('Land use classification:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRULandUseClassification, 5, 0)
        
        self.lineEditDominantHRULandUseClassification = QtGui.QLineEdit()
        self.lineEditDominantHRULandUseClassification.setReadOnly(True)
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRULandUseClassification, 5, 1)
        
        self.buttonSelectDominantHRULandUseClassification = QtGui.QPushButton()
        self.buttonSelectDominantHRULandUseClassification.setText('&Browse')
        self.layoutDominantHRU.addWidget(self.buttonSelectDominantHRULandUseClassification, 5, 2)
        
        self.labelDominantHRUSoilClassification = QtGui.QLabel()
        self.labelDominantHRUSoilClassification.setText('Soil classification:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRUSoilClassification, 6, 0)
        
        self.lineEditDominantHRUSoilClassification = QtGui.QLineEdit()
        self.lineEditDominantHRUSoilClassification.setReadOnly(True)
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRUSoilClassification, 6, 1)
        
        self.buttonSelectDominantHRUSoilClassification = QtGui.QPushButton()
        self.buttonSelectDominantHRUSoilClassification.setText('&Browse')
        self.layoutDominantHRU.addWidget(self.buttonSelectDominantHRUSoilClassification, 6, 2)
        
        self.labelDominantHRUSlopeClassification = QtGui.QLabel()
        self.labelDominantHRUSlopeClassification.setText('Slope classification:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRUSlopeClassification, 7, 0)
        
        self.lineEditDominantHRUSlopeClassification = QtGui.QLineEdit()
        self.lineEditDominantHRUSlopeClassification.setReadOnly(True)
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRUSlopeClassification, 7, 1)
        
        self.buttonSelectDominantHRUSlopeClassification = QtGui.QPushButton()
        self.buttonSelectDominantHRUSlopeClassification.setText('&Browse')
        self.layoutDominantHRU.addWidget(self.buttonSelectDominantHRUSlopeClassification, 7, 2)
        
        self.labelDominantHRUAreaName = QtGui.QLabel()
        self.labelDominantHRUAreaName.setText('&Area name:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRUAreaName, 8, 0)
        
        self.lineEditDominantHRUAreaName = QtGui.QLineEdit()
        self.lineEditDominantHRUAreaName.setText('areaname')
        self.layoutDominantHRU.addWidget(self.lineEditDominantHRUAreaName, 8, 1)
        self.labelDominantHRUAreaName.setBuddy(self.lineEditDominantHRUAreaName)
        
        self.labelDominantHRUPeriod = QtGui.QLabel()
        self.labelDominantHRUPeriod.setText('Pe&riod:')
        self.layoutDominantHRU.addWidget(self.labelDominantHRUPeriod, 9, 0)
        
        self.spinBoxDominantHRUPeriod = QtGui.QSpinBox()
        self.spinBoxDominantHRUPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxDominantHRUPeriod.setValue(td.year)
        self.layoutDominantHRU.addWidget(self.spinBoxDominantHRUPeriod, 9, 1)
        self.labelDominantHRUPeriod.setBuddy(self.spinBoxDominantHRUPeriod)
        
        # 'Dominant Land Use, Soil, and Slope' GroupBox
        self.groupBoxDominantLUSSL = QtGui.QGroupBox('Dominant Land Use, Soil, and Slope')
        self.layoutGroupBoxDominantLUSSL = QtGui.QHBoxLayout()
        self.groupBoxDominantLUSSL.setLayout(self.layoutGroupBoxDominantLUSSL)
        self.layoutOptionsDominantLUSSL = QtGui.QVBoxLayout()
        self.layoutOptionsDominantLUSSL.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsDominantLUSSL = QtGui.QWidget()
        self.contentOptionsDominantLUSSL.setLayout(self.layoutOptionsDominantLUSSL)
        self.layoutOptionsDominantLUSSL.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxDominantLUSSL = QtGui.QCheckBox()
        self.checkBoxDominantLUSSL.setChecked(False)
        self.contentOptionsDominantLUSSL.setDisabled(True)
        self.layoutGroupBoxDominantLUSSL.addWidget(self.checkBoxDominantLUSSL)
        self.layoutGroupBoxDominantLUSSL.addWidget(self.contentOptionsDominantLUSSL)
        self.layoutGroupBoxDominantLUSSL.setAlignment(self.checkBoxDominantLUSSL, QtCore.Qt.AlignTop)
        self.layoutDominantLUSSLInfo = QtGui.QVBoxLayout()
        self.layoutDominantLUSSL = QtGui.QGridLayout()
        self.layoutOptionsDominantLUSSL.addLayout(self.layoutDominantLUSSLInfo)
        self.layoutOptionsDominantLUSSL.addLayout(self.layoutDominantLUSSL)
        
        self.labelDominantLUSSLInfo = QtGui.QLabel()
        self.labelDominantLUSSLInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutDominantLUSSLInfo.addWidget(self.labelDominantLUSSLInfo)
        
        self.labelDominantLUSSLWorkingDir = QtGui.QLabel()
        self.labelDominantLUSSLWorkingDir.setText('Working directory:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLWorkingDir, 0, 0)
        
        self.lineEditDominantLUSSLWorkingDir = QtGui.QLineEdit()
        self.lineEditDominantLUSSLWorkingDir.setReadOnly(True)
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLWorkingDir, 0, 1)
        
        self.buttonSelectDominantLUSSLWorkingDir = QtGui.QPushButton()
        self.buttonSelectDominantLUSSLWorkingDir.setText('&Browse')
        self.layoutDominantLUSSL.addWidget(self.buttonSelectDominantLUSSLWorkingDir, 0, 2)
        
        self.labelDominantLUSSLLandUseMap = QtGui.QLabel()
        self.labelDominantLUSSLLandUseMap.setText('Land use map:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLLandUseMap, 1, 0)
        
        self.lineEditDominantLUSSLLandUseMap = QtGui.QLineEdit()
        self.lineEditDominantLUSSLLandUseMap.setReadOnly(True)
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLLandUseMap, 1, 1)
        
        self.buttonSelectDominantLUSSLLandUseMap = QtGui.QPushButton()
        self.buttonSelectDominantLUSSLLandUseMap.setText('&Browse')
        self.layoutDominantLUSSL.addWidget(self.buttonSelectDominantLUSSLLandUseMap, 1, 2)
        
        self.labelDominantLUSSLSoilMap = QtGui.QLabel()
        self.labelDominantLUSSLSoilMap.setText('Soil map:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLSoilMap, 2, 0)
        
        self.lineEditDominantLUSSLSoilMap = QtGui.QLineEdit()
        self.lineEditDominantLUSSLSoilMap.setReadOnly(True)
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLSoilMap, 2, 1)
        
        self.buttonSelectDominantLUSSLSoilMap = QtGui.QPushButton()
        self.buttonSelectDominantLUSSLSoilMap.setText('&Browse')
        self.layoutDominantLUSSL.addWidget(self.buttonSelectDominantLUSSLSoilMap, 2, 2)
        
        self.labelDominantLUSSLSlopeMap = QtGui.QLabel()
        self.labelDominantLUSSLSlopeMap.setText('Slope map:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLSlopeMap, 3, 0)
        
        self.lineEditDominantLUSSLSlopeMap = QtGui.QLineEdit()
        self.lineEditDominantLUSSLSlopeMap.setReadOnly(True)
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLSlopeMap, 3, 1)
        
        self.buttonSelectDominantLUSSLSlopeMap = QtGui.QPushButton()
        self.buttonSelectDominantLUSSLSlopeMap.setText('&Browse')
        self.layoutDominantLUSSL.addWidget(self.buttonSelectDominantLUSSLSlopeMap, 3, 2)
        
        self.labelDominantLUSSLSubcatchmentMap = QtGui.QLabel()
        self.labelDominantLUSSLSubcatchmentMap.setText('Subcatchment map:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLSubcatchmentMap, 4, 0)
        
        self.lineEditDominantLUSSLSubcatchmentMap = QtGui.QLineEdit()
        self.lineEditDominantLUSSLSubcatchmentMap.setReadOnly(True)
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLSubcatchmentMap, 4, 1)
        
        self.buttonSelectDominantLUSSLSubcatchmentMap = QtGui.QPushButton()
        self.buttonSelectDominantLUSSLSubcatchmentMap.setText('&Browse')
        self.layoutDominantLUSSL.addWidget(self.buttonSelectDominantLUSSLSubcatchmentMap, 4, 2)
        
        self.labelDominantLUSSLLandUseClassification = QtGui.QLabel()
        self.labelDominantLUSSLLandUseClassification.setText('Land use classification:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLLandUseClassification, 5, 0)
        
        self.lineEditDominantLUSSLLandUseClassification = QtGui.QLineEdit()
        self.lineEditDominantLUSSLLandUseClassification.setReadOnly(True)
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLLandUseClassification, 5, 1)
        
        self.buttonSelectDominantLUSSLLandUseClassification = QtGui.QPushButton()
        self.buttonSelectDominantLUSSLLandUseClassification.setText('&Browse')
        self.layoutDominantLUSSL.addWidget(self.buttonSelectDominantLUSSLLandUseClassification, 5, 2)
        
        self.labelDominantLUSSLSoilClassification = QtGui.QLabel()
        self.labelDominantLUSSLSoilClassification.setText('Soil classification:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLSoilClassification, 6, 0)
        
        self.lineEditDominantLUSSLSoilClassification = QtGui.QLineEdit()
        self.lineEditDominantLUSSLSoilClassification.setReadOnly(True)
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLSoilClassification, 6, 1)
        
        self.buttonSelectDominantLUSSLSoilClassification = QtGui.QPushButton()
        self.buttonSelectDominantLUSSLSoilClassification.setText('&Browse')
        self.layoutDominantLUSSL.addWidget(self.buttonSelectDominantLUSSLSoilClassification, 6, 2)
        
        self.labelDominantLUSSLSlopeClassification = QtGui.QLabel()
        self.labelDominantLUSSLSlopeClassification.setText('Slope classification:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLSlopeClassification, 7, 0)
        
        self.lineEditDominantLUSSLSlopeClassification = QtGui.QLineEdit()
        self.lineEditDominantLUSSLSlopeClassification.setReadOnly(True)
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLSlopeClassification, 7, 1)
        
        self.buttonSelectDominantLUSSLSlopeClassification = QtGui.QPushButton()
        self.buttonSelectDominantLUSSLSlopeClassification.setText('&Browse')
        self.layoutDominantLUSSL.addWidget(self.buttonSelectDominantLUSSLSlopeClassification, 7, 2)
        
        self.labelDominantLUSSLAreaName = QtGui.QLabel()
        self.labelDominantLUSSLAreaName.setText('&Area name:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLAreaName, 8, 0)
        
        self.lineEditDominantLUSSLAreaName = QtGui.QLineEdit()
        self.lineEditDominantLUSSLAreaName.setText('areaname')
        self.layoutDominantLUSSL.addWidget(self.lineEditDominantLUSSLAreaName, 8, 1)
        self.labelDominantLUSSLAreaName.setBuddy(self.lineEditDominantLUSSLAreaName)
        
        self.labelDominantLUSSLPeriod = QtGui.QLabel()
        self.labelDominantLUSSLPeriod.setText('Pe&riod:')
        self.layoutDominantLUSSL.addWidget(self.labelDominantLUSSLPeriod, 9, 0)
        
        self.spinBoxDominantLUSSLPeriod = QtGui.QSpinBox()
        self.spinBoxDominantLUSSLPeriod.setRange(1, 9999)
        self.spinBoxDominantLUSSLPeriod.setValue(td.year)
        self.layoutDominantLUSSL.addWidget(self.spinBoxDominantLUSSLPeriod, 9, 1)
        self.labelDominantLUSSLPeriod.setBuddy(self.spinBoxDominantLUSSLPeriod)
        
        # 'Multiple HRU' GroupBox
        self.groupBoxMultipleHRU = QtGui.QGroupBox('Multiple HRU')
        self.layoutGroupBoxMultipleHRU = QtGui.QHBoxLayout()
        self.groupBoxMultipleHRU.setLayout(self.layoutGroupBoxMultipleHRU)
        self.layoutOptionsMultipleHRU = QtGui.QVBoxLayout()
        self.layoutOptionsMultipleHRU.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsMultipleHRU = QtGui.QWidget()
        self.contentOptionsMultipleHRU.setLayout(self.layoutOptionsMultipleHRU)
        self.layoutOptionsMultipleHRU.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxMultipleHRU = QtGui.QCheckBox()
        self.checkBoxMultipleHRU.setChecked(False)
        self.contentOptionsMultipleHRU.setDisabled(True)
        self.layoutGroupBoxMultipleHRU.addWidget(self.checkBoxMultipleHRU)
        self.layoutGroupBoxMultipleHRU.addWidget(self.contentOptionsMultipleHRU)
        self.layoutGroupBoxMultipleHRU.setAlignment(self.checkBoxMultipleHRU, QtCore.Qt.AlignTop)
        self.layoutMultipleHRUInfo = QtGui.QVBoxLayout()
        self.layoutMultipleHRU = QtGui.QGridLayout()
        self.layoutOptionsMultipleHRU.addLayout(self.layoutMultipleHRUInfo)
        self.layoutOptionsMultipleHRU.addLayout(self.layoutMultipleHRU)
        
        self.labelMultipleHRUInfo = QtGui.QLabel()
        self.labelMultipleHRUInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutMultipleHRUInfo.addWidget(self.labelMultipleHRUInfo)
        
        self.labelMultipleHRUWorkingDir = QtGui.QLabel()
        self.labelMultipleHRUWorkingDir.setText('Working directory:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUWorkingDir, 0, 0)
        
        self.lineEditMultipleHRUWorkingDir = QtGui.QLineEdit()
        self.lineEditMultipleHRUWorkingDir.setReadOnly(True)
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRUWorkingDir, 0, 1)
        
        self.buttonSelectMultipleHRUWorkingDir = QtGui.QPushButton()
        self.buttonSelectMultipleHRUWorkingDir.setText('&Browse')
        self.layoutMultipleHRU.addWidget(self.buttonSelectMultipleHRUWorkingDir, 0, 2)
        
        self.labelMultipleHRULandUseMap = QtGui.QLabel()
        self.labelMultipleHRULandUseMap.setText('Land use map:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRULandUseMap, 1, 0)
        
        self.lineEditMultipleHRULandUseMap = QtGui.QLineEdit()
        self.lineEditMultipleHRULandUseMap.setReadOnly(True)
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRULandUseMap, 1, 1)
        
        self.buttonSelectMultipleHRULandUseMap = QtGui.QPushButton()
        self.buttonSelectMultipleHRULandUseMap.setText('&Browse')
        self.layoutMultipleHRU.addWidget(self.buttonSelectMultipleHRULandUseMap, 1, 2)
        
        self.labelMultipleHRUSoilMap = QtGui.QLabel()
        self.labelMultipleHRUSoilMap.setText('Soil map:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUSoilMap, 2, 0)
        
        self.lineEditMultipleHRUSoilMap = QtGui.QLineEdit()
        self.lineEditMultipleHRUSoilMap.setReadOnly(True)
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRUSoilMap, 2, 1)
        
        self.buttonSelectMultipleHRUSoilMap = QtGui.QPushButton()
        self.buttonSelectMultipleHRUSoilMap.setText('&Browse')
        self.layoutMultipleHRU.addWidget(self.buttonSelectMultipleHRUSoilMap, 2, 2)
        
        self.labelMultipleHRUSlopeMap = QtGui.QLabel()
        self.labelMultipleHRUSlopeMap.setText('Slope map:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUSlopeMap, 3, 0)
        
        self.lineEditMultipleHRUSlopeMap = QtGui.QLineEdit()
        self.lineEditMultipleHRUSlopeMap.setReadOnly(True)
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRUSlopeMap, 3, 1)
        
        self.buttonSelectMultipleHRUSlopeMap = QtGui.QPushButton()
        self.buttonSelectMultipleHRUSlopeMap.setText('&Browse')
        self.layoutMultipleHRU.addWidget(self.buttonSelectMultipleHRUSlopeMap, 3, 2)
        
        self.labelMultipleHRUSubcatchmentMap = QtGui.QLabel()
        self.labelMultipleHRUSubcatchmentMap.setText('Subcatchment map:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUSubcatchmentMap, 4, 0)
        
        self.lineEditMultipleHRUSubcatchmentMap = QtGui.QLineEdit()
        self.lineEditMultipleHRUSubcatchmentMap.setReadOnly(True)
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRUSubcatchmentMap, 4, 1)
        
        self.buttonSelectMultipleHRUSubcatchmentMap = QtGui.QPushButton()
        self.buttonSelectMultipleHRUSubcatchmentMap.setText('&Browse')
        self.layoutMultipleHRU.addWidget(self.buttonSelectMultipleHRUSubcatchmentMap, 4, 2)
        
        self.labelMultipleHRULandUseClassification = QtGui.QLabel()
        self.labelMultipleHRULandUseClassification.setText('Land use classification:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRULandUseClassification, 5, 0)
        
        self.lineEditMultipleHRULandUseClassification = QtGui.QLineEdit()
        self.lineEditMultipleHRULandUseClassification.setReadOnly(True)
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRULandUseClassification, 5, 1)
        
        self.buttonSelectMultipleHRULandUseClassification = QtGui.QPushButton()
        self.buttonSelectMultipleHRULandUseClassification.setText('&Browse')
        self.layoutMultipleHRU.addWidget(self.buttonSelectMultipleHRULandUseClassification, 5, 2)
        
        self.labelMultipleHRUSoilClassification = QtGui.QLabel()
        self.labelMultipleHRUSoilClassification.setText('Soil classification:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUSoilClassification, 6, 0)
        
        self.lineEditMultipleHRUSoilClassification = QtGui.QLineEdit()
        self.lineEditMultipleHRUSoilClassification.setReadOnly(True)
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRUSoilClassification, 6, 1)
        
        self.buttonSelectMultipleHRUSoilClassification = QtGui.QPushButton()
        self.buttonSelectMultipleHRUSoilClassification.setText('&Browse')
        self.layoutMultipleHRU.addWidget(self.buttonSelectMultipleHRUSoilClassification, 6, 2)
        
        self.labelMultipleHRUSlopeClassification = QtGui.QLabel()
        self.labelMultipleHRUSlopeClassification.setText('Slope classification:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUSlopeClassification, 7, 0)
        
        self.lineEditMultipleHRUSlopeClassification = QtGui.QLineEdit()
        self.lineEditMultipleHRUSlopeClassification.setReadOnly(True)
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRUSlopeClassification, 7, 1)
        
        self.buttonSelectMultipleHRUSlopeClassification = QtGui.QPushButton()
        self.buttonSelectMultipleHRUSlopeClassification.setText('&Browse')
        self.layoutMultipleHRU.addWidget(self.buttonSelectMultipleHRUSlopeClassification, 7, 2)
        
        self.labelMultipleHRUAreaName = QtGui.QLabel()
        self.labelMultipleHRUAreaName.setText('&Area name:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUAreaName, 8, 0)
        
        self.lineEditMultipleHRUAreaName = QtGui.QLineEdit()
        self.lineEditMultipleHRUAreaName.setText('areaname')
        self.layoutMultipleHRU.addWidget(self.lineEditMultipleHRUAreaName, 8, 1)
        self.labelMultipleHRUAreaName.setBuddy(self.lineEditMultipleHRUAreaName)
        
        self.labelMultipleHRUPeriod = QtGui.QLabel()
        self.labelMultipleHRUPeriod.setText('Pe&riod:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUPeriod, 9, 0)
        
        self.spinBoxMultipleHRUPeriod = QtGui.QSpinBox()
        self.spinBoxMultipleHRUPeriod.setRange(1, 9999)
        self.spinBoxMultipleHRUPeriod.setValue(td.year)
        self.layoutMultipleHRU.addWidget(self.spinBoxMultipleHRUPeriod, 9, 1)
        self.labelMultipleHRUPeriod.setBuddy(self.spinBoxMultipleHRUPeriod)
        
        self.labelMultipleHRULandUseThreshold = QtGui.QLabel()
        self.labelMultipleHRULandUseThreshold.setText('Land use &threshold:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRULandUseThreshold, 10, 0)
        
        self.spinBoxMultipleHRULandUseThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRULandUseThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRULandUseThreshold.setValue(0)
        self.layoutMultipleHRU.addWidget(self.spinBoxMultipleHRULandUseThreshold, 10, 1)
        self.labelMultipleHRULandUseThreshold.setBuddy(self.spinBoxMultipleHRULandUseThreshold)
        
        self.labelMultipleHRUSoilThreshold = QtGui.QLabel()
        self.labelMultipleHRUSoilThreshold.setText('Soil t&hreshold:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUSoilThreshold, 11, 0)
        
        self.spinBoxMultipleHRUSoilThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRUSoilThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRUSoilThreshold.setValue(0)
        self.layoutMultipleHRU.addWidget(self.spinBoxMultipleHRUSoilThreshold, 11, 1)
        self.labelMultipleHRUSoilThreshold.setBuddy(self.spinBoxMultipleHRUSoilThreshold)
        
        self.labelMultipleHRUSlopeThreshold = QtGui.QLabel()
        self.labelMultipleHRUSlopeThreshold.setText('Slope th&reshold:')
        self.layoutMultipleHRU.addWidget(self.labelMultipleHRUSlopeThreshold, 12, 0)
        
        self.spinBoxMultipleHRUSlopeThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRUSlopeThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRUSlopeThreshold.setValue(0)
        self.layoutMultipleHRU.addWidget(self.spinBoxMultipleHRUSlopeThreshold, 12, 1)
        self.labelMultipleHRUSlopeThreshold.setBuddy(self.spinBoxMultipleHRUSlopeThreshold)
        
        # Process tab button
        self.layoutButtonHRUDefinition = QtGui.QHBoxLayout()
        self.buttonProcessHRUDefinition = QtGui.QPushButton()
        self.buttonProcessHRUDefinition.setText('&Process')
        self.layoutButtonHRUDefinition.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonHRUDefinition.addWidget(self.buttonProcessHRUDefinition)
        
        # Place the GroupBoxes
        self.layoutContentHRUDefinition.addWidget(self.groupBoxDominantHRU)
        self.layoutContentHRUDefinition.addWidget(self.groupBoxDominantLUSSL)
        self.layoutContentHRUDefinition.addWidget(self.groupBoxMultipleHRU)
        self.layoutContentHRUDefinition.addLayout(self.layoutButtonHRUDefinition)
        
        #***********************************************************
        # Setup 'Reclassification' tab
        #***********************************************************
        self.tabReclassification.setLayout(self.layoutTabReclassification)
        
        #***********************************************************
        # Setup 'Result' tab
        #***********************************************************
        self.tabResult.setLayout(self.layoutTabResult)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 640)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensQUES, self).showEvent(event)
    
    
    def toggleCarbonAccounting(self, checked):
        """
        """
        if checked:
            self.contentOptionsCarbonAccounting.setEnabled(True)
        else:
            self.contentOptionsCarbonAccounting.setDisabled(True)
    
    
    def togglePeatlandCarbonAccounting(self, checked):
        """
        """
        if checked:
            self.contentOptionsPeatlandCarbonAccounting.setEnabled(True)
        else:
            self.contentOptionsPeatlandCarbonAccounting.setDisabled(True)
    
    
    def toggleSummarizeMultiplePeriod(self, checked):
        """
        """
        if checked:
            self.contentOptionsSummarizeMultiplePeriod.setEnabled(True)
        else:
            self.contentOptionsSummarizeMultiplePeriod.setDisabled(True)
    
    
    def toggleDominantHRU(self, checked):
        """
        """
        if checked:
            self.contentOptionsDominantHRU.setEnabled(True)
        else:
            self.contentOptionsDominantHRU.setDisabled(True)
    
    
    def toggleDominantLUSSL(self, checked):
        """
        """
        if checked:
            self.contentOptionsDominantLUSSL.setEnabled(True)
        else:
            self.contentOptionsDominantLUSSL.setDisabled(True)
    
    
    def toggleMultipleHRU(self, checked):
        """
        """
        if checked:
            self.contentOptionsMultipleHRU.setEnabled(True)
        else:
            self.contentOptionsMultipleHRU.setDisabled(True)
    
    
    def addLandCoverRow(self, period):
        """
        """
        layoutRow = QtGui.QHBoxLayout()
        
        labelLandCoverPeriod = QtGui.QLabel()
        labelLandCoverPeriod.setText(period)
        layoutRow.addWidget(labelLandCoverPeriod)
        
        lineEditLandCoverRasterfile = QtGui.QLineEdit()
        lineEditLandCoverRasterfile.setReadOnly(True)
        lineEditLandCoverRasterfile.setObjectName('lineEditLandCoverRasterfile_{0}'.format(period))
        layoutRow.addWidget(lineEditLandCoverRasterfile)
        
        buttonSelectLandCoverRasterfile = QtGui.QPushButton()
        buttonSelectLandCoverRasterfile.setText('Select {0} Raster'.format(period))
        buttonSelectLandCoverRasterfile.setObjectName('buttonSelectLandCoverRasterfile_{0}'.format(period))
        layoutRow.addWidget(buttonSelectLandCoverRasterfile)
        
        spinBoxLandCover = QtGui.QSpinBox()
        spinBoxLandCover.setRange(1, 9999)
        td = datetime.date.today()
        spinBoxLandCover.setValue(td.year)
        spinBoxLandCover.setObjectName('spinBoxLandCover_{0}'.format(period))
        layoutRow.addWidget(spinBoxLandCover)
        
        self.layoutTableLandCover.addLayout(layoutRow)
        
        buttonSelectLandCoverRasterfile.clicked.connect(self.handlerSelectLandCoverRasterfile)
    
    
    def handlerSelectLandCoverRasterfile(self):
        """
        """
        pass
    