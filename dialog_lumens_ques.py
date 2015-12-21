#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from processing.tools import *
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
        
        # 'Pre-QUES' tab buttons
        self.buttonSelectPreQUESWorkingDir.clicked.connect(self.handlerSelectPreQUESWorkingDir)
        self.buttonSelectPreQUESPlanningUnit.clicked.connect(self.handlerSelectPreQUESPlanningUnit)
        self.buttonSelectPreQUESCsvPlanningUnit.clicked.connect(self.handlerSelectPreQUESCsvPlanningUnit)
        self.buttonSelectLandCoverCsvLandUse.clicked.connect(self.handlerSelectLandCoverCsvLandUse)
        
        # 'QUES-C' tab checkboxes
        self.checkBoxCarbonAccounting.toggled.connect(self.toggleCarbonAccounting)
        self.checkBoxPeatlandCarbonAccounting.toggled.connect(self.togglePeatlandCarbonAccounting)
        self.checkBoxSummarizeMultiplePeriod.toggled.connect(self.toggleSummarizeMultiplePeriod)
        
        # 'QUES-C' tab buttons
        self.buttonSelectCACsvfile.clicked.connect(self.handlerSelectCACsvfile)
        self.buttonSelectPCACsvfile.clicked.connect(self.handlerSelectPCACsvfile)
        self.buttonProcessQUESC.clicked.connect(self.handlerProcessQUESC)
        
        # 'QUES-B' tab buttons
        self.buttonSelectQUESBCsvLandCover.clicked.connect(self.handlerSelectQUESBCsvLandCover)
        self.buttonSelectQUESBCsvClassDescriptors.clicked.connect(self.handlerSelectQUESBCsvClassDescriptors)
        self.buttonSelectQUESBCsvEdgeContrast.clicked.connect(self.handlerSelectQUESBCsvEdgeContrast)
        self.buttonSelectQUESBCsvZoneLookup.clicked.connect(self.handlerSelectQUESBCsvZoneLookup)
        self.buttonSelectQUESBOutputTECIInitial.clicked.connect(self.handlerSelectQUESBOutputTECIInitial)
        self.buttonSelectQUESBOutputTECIFinal.clicked.connect(self.handlerSelectQUESBOutputTECIFinal)
        self.buttonSelectQUESBOutputHabitatLoss.clicked.connect(self.handlerSelectQUESBOutputHabitatLoss)
        self.buttonSelectQUESBOutputDegradedHabitat.clicked.connect(self.handlerSelectQUESBOutputDegradedHabitat)
        self.buttonSelectQUESBOutputHabitatGain.clicked.connect(self.handlerSelectQUESBOutputHabitatGain)
        self.buttonSelectQUESBOutputRecoveredHabitat.clicked.connect(self.handlerSelectQUESBOutputRecoveredHabitat)
        self.buttonProcessQUESB.clicked.connect(self.handlerProcessQUESB)
        
        # 'QUES-H' tab checkboxes
        self.checkBoxMultipleHRU.toggled.connect(self.toggleMultipleHRU)
        
        # 'QUES-H' HRU tab buttons
        self.buttonSelectHRUWorkingDir.clicked.connect(self.handlerSelectHRUWorkingDir)
        self.buttonSelectHRULandUseMap.clicked.connect(self.handlerSelectHRULandUseMap)
        self.buttonSelectHRUSoilMap.clicked.connect(self.handlerSelectHRUSoilMap)
        self.buttonSelectHRUSlopeMap.clicked.connect(self.handlerSelectHRUSlopeMap)
        self.buttonSelectHRUSubcatchmentMap.clicked.connect(self.handlerSelectHRUSubcatchmentMap)
        self.buttonSelectHRULandUseClassification.clicked.connect(self.handlerSelectHRULandUseClassification)
        self.buttonSelectHRUSoilClassification.clicked.connect(self.handlerSelectHRUSoilClassification)
        self.buttonSelectHRUSlopeClassification.clicked.connect(self.handlerSelectHRUSlopeClassification)
        self.buttonProcessHRUDefinition.clicked.connect(self.handlerProcessQUESHHRUDefinition)
        
        # 'QUES-H' Watershed Model Evaluation tab buttons
        self.buttonSelectWatershedModelEvaluationWorkingDir.clicked.connect(self.handlerSelectWatershedModelEvaluationWorkingDir)
        self.buttonSelectWatershedModelEvaluationObservedDebitFile.clicked.connect(self.handlerSelectWatershedModelEvaluationObservedDebitFile)
        self.buttonSelectOutputWatershedModelEvaluation.clicked.connect(self.handlerSelectOutputWatershedModelEvaluation)
        self.buttonProcessWatershedModelEvaluation.clicked.connect(self.handlerProcessQUESHWatershedModelEvaluation)
        
        # 'QUES-H' Watershed Indicators tab buttons
        self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir.clicked.connect(self.handlerSelectWatershedIndicatorsSWATTXTINOUTDir)
        self.buttonSelectWatershedIndicatorsSubWatershedPolygon.clicked.connect(self.handlerSelectWatershedIndicatorsSubWatershedPolygon)
        self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.clicked.connect(self.handlerSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators)
        self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.clicked.connect(self.handlerSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators)
        self.buttonProcessWatershedIndicators.clicked.connect(self.handlerProcessQUESHWatershedIndicators)
        
    
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
        
        self.tabPreQUES.setLayout(self.layoutTabPreQUES)
        self.tabQUESC.setLayout(self.layoutTabQUESC)
        self.tabQUESB.setLayout(self.layoutTabQUESB)
        self.tabQUESH.setLayout(self.layoutTabQUESH)
        self.tabReclassification.setLayout(self.layoutTabReclassification)
        self.tabResult.setLayout(self.layoutTabResult)
        
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
        
        self.labelPreQUESWorkingDir = QtGui.QLabel()
        self.labelPreQUESWorkingDir.setText('Working directory:')
        self.layoutPlanningUnit.addWidget(self.labelPreQUESWorkingDir, 0, 0)
        self.lineEditPreQUESWorkingDir = QtGui.QLineEdit()
        self.lineEditPreQUESWorkingDir.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditPreQUESWorkingDir, 0, 1)
        self.buttonSelectPreQUESWorkingDir = QtGui.QPushButton()
        self.buttonSelectPreQUESWorkingDir.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectPreQUESWorkingDir, 0, 2)
        
        self.labelPreQUESLocation = QtGui.QLabel()
        self.labelPreQUESLocation.setText('&Location:')
        self.layoutPlanningUnit.addWidget(self.labelPreQUESLocation, 1, 0)
        self.lineEditPreQUESLocation = QtGui.QLineEdit()
        self.lineEditPreQUESLocation.setText('location')
        self.layoutPlanningUnit.addWidget(self.lineEditPreQUESLocation, 1, 1)
        self.labelPreQUESLocation.setBuddy(self.lineEditPreQUESLocation)
        
        self.labelPreQUESPlanningUnit = QtGui.QLabel()
        self.labelPreQUESPlanningUnit.setText('Planning unit map:')
        self.layoutPlanningUnit.addWidget(self.labelPreQUESPlanningUnit, 2, 0)
        self.lineEditPreQUESPlanningUnit = QtGui.QLineEdit()
        self.lineEditPreQUESPlanningUnit.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditPreQUESPlanningUnit, 2, 1)
        self.buttonSelectPreQUESPlanningUnit = QtGui.QPushButton()
        self.buttonSelectPreQUESPlanningUnit.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectPreQUESPlanningUnit, 2, 2)
        
        self.labelPreQUESCsvPlanningUnit = QtGui.QLabel()
        self.labelPreQUESCsvPlanningUnit.setText('Planning unit lookup table:')
        self.layoutPlanningUnit.addWidget(self.labelPreQUESCsvPlanningUnit, 3, 0)
        self.lineEditPreQUESCsvPlanningUnit = QtGui.QLineEdit()
        self.lineEditPreQUESCsvPlanningUnit.setReadOnly(True)
        self.layoutPlanningUnit.addWidget(self.lineEditPreQUESCsvPlanningUnit, 3, 1)
        self.buttonSelectPreQUESCsvPlanningUnit = QtGui.QPushButton()
        self.buttonSelectPreQUESCsvPlanningUnit.setText('&Browse')
        self.layoutPlanningUnit.addWidget(self.buttonSelectPreQUESCsvPlanningUnit, 3, 2)
        
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
        self.labelLandCoverCsvLandUse = QtGui.QLabel()
        self.labelLandCoverCsvLandUse.setText('Land use lookup table:')
        self.layoutLandCoverOptions.addWidget(self.labelLandCoverCsvLandUse, 0, 0)
        self.lineEditLandCoverCsvLandUse = QtGui.QLineEdit()
        self.lineEditLandCoverCsvLandUse.setReadOnly(True)
        self.layoutLandCoverOptions.addWidget(self.lineEditLandCoverCsvLandUse, 0, 1)
        self.buttonSelectLandCoverCsvLandUse = QtGui.QPushButton()
        self.buttonSelectLandCoverCsvLandUse.setText('&Browse')
        self.layoutLandCoverOptions.addWidget(self.buttonSelectLandCoverCsvLandUse, 0, 2)
        
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
        
        self.labelCANoDataValue = QtGui.QLabel()
        self.labelCANoDataValue.setText('&No data value:')
        self.layoutCarbonAccounting.addWidget(self.labelCANoDataValue, 1, 0)
        
        self.spinBoxCANoDataValue = QtGui.QSpinBox()
        self.spinBoxCANoDataValue.setRange(-9999, 9999)
        self.spinBoxCANoDataValue.setValue(0)
        self.layoutCarbonAccounting.addWidget(self.spinBoxCANoDataValue, 1, 1)
        self.labelCANoDataValue.setBuddy(self.spinBoxCANoDataValue)
        
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
        
        #***********************************************************
        # Setup 'QUES-B' tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxQUESBParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxQUESBParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxQUESBParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxQUESBParameters.setLayout(self.layoutGroupBoxQUESBParameters)
        self.layoutQUESBParametersInfo = QtGui.QVBoxLayout()
        self.layoutQUESBParameters = QtGui.QGridLayout()
        self.layoutGroupBoxQUESBParameters.addLayout(self.layoutQUESBParametersInfo)
        self.layoutGroupBoxQUESBParameters.addLayout(self.layoutQUESBParameters)
        
        self.labelQUESBParametersInfo = QtGui.QLabel()
        self.labelQUESBParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutQUESBParametersInfo.addWidget(self.labelQUESBParametersInfo)
        
        self.labelQUESBCsvLandCover = QtGui.QLabel()
        self.labelQUESBCsvLandCover.setText('Land cover lookup:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBCsvLandCover, 0, 0)
        
        self.lineEditQUESBCsvLandCover = QtGui.QLineEdit()
        self.lineEditQUESBCsvLandCover.setReadOnly(True)
        self.layoutQUESBParameters.addWidget(self.lineEditQUESBCsvLandCover, 0, 1)
        
        self.buttonSelectQUESBCsvLandCover = QtGui.QPushButton()
        self.buttonSelectQUESBCsvLandCover.setText('&Browse')
        self.layoutQUESBParameters.addWidget(self.buttonSelectQUESBCsvLandCover, 0, 2)
        
        self.labelQUESBSamplingGridRes = QtGui.QLabel()
        self.labelQUESBSamplingGridRes.setText('Sampling grid &resolution:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBSamplingGridRes, 1, 0)
        
        self.spinBoxQUESBSamplingGridRes = QtGui.QSpinBox()
        self.spinBoxQUESBSamplingGridRes.setRange(1, 9999)
        self.spinBoxQUESBSamplingGridRes.setValue(10000)
        self.layoutQUESBParameters.addWidget(self.spinBoxQUESBSamplingGridRes, 1, 1)
        self.labelQUESBSamplingGridRes.setBuddy(self.spinBoxQUESBSamplingGridRes)
        
        self.labelQUESBSamplingWindowSize = QtGui.QLabel()
        self.labelQUESBSamplingWindowSize.setText('Sampling &window size:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBSamplingWindowSize, 2, 0)
        
        self.spinBoxQUESBSamplingWindowSize = QtGui.QSpinBox()
        self.spinBoxQUESBSamplingWindowSize.setRange(1, 9999)
        self.spinBoxQUESBSamplingWindowSize.setValue(1000)
        self.layoutQUESBParameters.addWidget(self.spinBoxQUESBSamplingWindowSize, 2, 1)
        self.labelQUESBSamplingWindowSize.setBuddy(self.spinBoxQUESBSamplingWindowSize)
        
        self.labelQUESBWindowShape = QtGui.QLabel()
        self.labelQUESBWindowShape.setText('Window &shape:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBWindowShape, 3, 0)
        
        self.spinBoxQUESBWindowShape = QtGui.QSpinBox()
        self.spinBoxQUESBWindowShape.setRange(1, 9999)
        self.spinBoxQUESBWindowShape.setValue(1)
        self.layoutQUESBParameters.addWidget(self.spinBoxQUESBWindowShape, 3, 1)
        self.labelQUESBWindowShape.setBuddy(self.spinBoxQUESBWindowShape)
        
        self.labelQUESBNodata = QtGui.QLabel()
        self.labelQUESBNodata.setText('&No data value:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBNodata, 4, 0)
        
        self.spinBoxQUESBNodata = QtGui.QSpinBox()
        self.spinBoxQUESBNodata.setRange(-9999, 9999)
        self.spinBoxQUESBNodata.setValue(0)
        self.layoutQUESBParameters.addWidget(self.spinBoxQUESBNodata, 4, 1)
        self.labelQUESBNodata.setBuddy(self.spinBoxQUESBNodata)
        
        self.labelQUESBCsvClassDescriptors = QtGui.QLabel()
        self.labelQUESBCsvClassDescriptors.setText('Class descriptors:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBCsvClassDescriptors, 5, 0)
        
        self.lineEditQUESBCsvClassDescriptors = QtGui.QLineEdit()
        self.lineEditQUESBCsvClassDescriptors.setReadOnly(True)
        self.layoutQUESBParameters.addWidget(self.lineEditQUESBCsvClassDescriptors, 5, 1)
        
        self.buttonSelectQUESBCsvClassDescriptors = QtGui.QPushButton()
        self.buttonSelectQUESBCsvClassDescriptors.setText('&Browse')
        self.layoutQUESBParameters.addWidget(self.buttonSelectQUESBCsvClassDescriptors, 5, 2)
        
        self.labelQUESBCsvEdgeContrast = QtGui.QLabel()
        self.labelQUESBCsvEdgeContrast.setText('Edge contrast:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBCsvEdgeContrast, 6, 0)
        
        self.lineEditQUESBCsvEdgeContrast = QtGui.QLineEdit()
        self.lineEditQUESBCsvEdgeContrast.setReadOnly(True)
        self.layoutQUESBParameters.addWidget(self.lineEditQUESBCsvEdgeContrast, 6, 1)
        
        self.buttonSelectQUESBCsvEdgeContrast = QtGui.QPushButton()
        self.buttonSelectQUESBCsvEdgeContrast.setText('&Browse')
        self.layoutQUESBParameters.addWidget(self.buttonSelectQUESBCsvEdgeContrast, 6, 2)
        
        self.labelQUESBCsvZoneLookup = QtGui.QLabel()
        self.labelQUESBCsvZoneLookup.setText('Zone lookup:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBCsvZoneLookup, 7, 0)
        
        self.lineEditQUESBCsvZoneLookup = QtGui.QLineEdit()
        self.lineEditQUESBCsvZoneLookup.setReadOnly(True)
        self.layoutQUESBParameters.addWidget(self.lineEditQUESBCsvZoneLookup, 7, 1)
        
        self.buttonSelectQUESBCsvZoneLookup = QtGui.QPushButton()
        self.buttonSelectQUESBCsvZoneLookup.setText('&Browse')
        self.layoutQUESBParameters.addWidget(self.buttonSelectQUESBCsvZoneLookup, 7, 2)
        
        self.labelQUESBRefMapID = QtGui.QLabel()
        self.labelQUESBRefMapID.setText('Reference map ID:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBRefMapID, 8, 0)
        
        refMapID = {
            1: 'Land cover T1',
            2: 'Land cover T2',
            3: 'Zone',
        }
        
        self.comboBoxQUESBRefMapID = QtGui.QComboBox()
        
        for key, val in refMapID.iteritems():
            self.comboBoxQUESBRefMapID.addItem(val, key)
        self.layoutQUESBParameters.addWidget(self.comboBoxQUESBRefMapID, 8, 1)
        
        # 'Output' GroupBox
        self.groupBoxQUESBOutput = QtGui.QGroupBox('QUESBOutput')
        self.layoutGroupBoxQUESBOutput = QtGui.QVBoxLayout()
        self.layoutGroupBoxQUESBOutput.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxQUESBOutput.setLayout(self.layoutGroupBoxQUESBOutput)
        self.layoutQUESBOutputInfo = QtGui.QVBoxLayout()
        self.layoutQUESBOutput = QtGui.QGridLayout()
        self.layoutGroupBoxQUESBOutput.addLayout(self.layoutQUESBOutputInfo)
        self.layoutGroupBoxQUESBOutput.addLayout(self.layoutQUESBOutput)
        
        self.labelQUESBOutputInfo = QtGui.QLabel()
        self.labelQUESBOutputInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutQUESBOutputInfo.addWidget(self.labelQUESBOutputInfo)
        
        self.labelQUESBOutputTECIInitial = QtGui.QLabel()
        self.labelQUESBOutputTECIInitial.setText('[QUESBOutput] TECI initial:')
        self.layoutQUESBOutput.addWidget(self.labelQUESBOutputTECIInitial, 0, 0)
        
        self.lineEditQUESBOutputTECIInitial = QtGui.QLineEdit()
        self.lineEditQUESBOutputTECIInitial.setReadOnly(True)
        self.layoutQUESBOutput.addWidget(self.lineEditQUESBOutputTECIInitial, 0, 1)
        
        self.buttonSelectQUESBOutputTECIInitial = QtGui.QPushButton()
        self.buttonSelectQUESBOutputTECIInitial.setText('&Browse')
        self.layoutQUESBOutput.addWidget(self.buttonSelectQUESBOutputTECIInitial, 0, 2)
        
        self.labelQUESBOutputTECIFinal = QtGui.QLabel()
        self.labelQUESBOutputTECIFinal.setText('[QUESBOutput] TECI final:')
        self.layoutQUESBOutput.addWidget(self.labelQUESBOutputTECIFinal, 1, 0)
        
        self.lineEditQUESBOutputTECIFinal = QtGui.QLineEdit()
        self.lineEditQUESBOutputTECIFinal.setReadOnly(True)
        self.layoutQUESBOutput.addWidget(self.lineEditQUESBOutputTECIFinal, 1, 1)
        
        self.buttonSelectQUESBOutputTECIFinal = QtGui.QPushButton()
        self.buttonSelectQUESBOutputTECIFinal.setText('&Browse')
        self.layoutQUESBOutput.addWidget(self.buttonSelectQUESBOutputTECIFinal, 1, 2)
        
        self.labelQUESBOutputHabitatLoss = QtGui.QLabel()
        self.labelQUESBOutputHabitatLoss.setText('[QUESBOutput] Habitat Loss:')
        self.layoutQUESBOutput.addWidget(self.labelQUESBOutputHabitatLoss, 2, 0)
        
        self.lineEditQUESBOutputHabitatLoss = QtGui.QLineEdit()
        self.lineEditQUESBOutputHabitatLoss.setReadOnly(True)
        self.layoutQUESBOutput.addWidget(self.lineEditQUESBOutputHabitatLoss, 2, 1)
        
        self.buttonSelectQUESBOutputHabitatLoss = QtGui.QPushButton()
        self.buttonSelectQUESBOutputHabitatLoss.setText('&Browse')
        self.layoutQUESBOutput.addWidget(self.buttonSelectQUESBOutputHabitatLoss, 2, 2)
        
        self.labelQUESBOutputDegradedHabitat = QtGui.QLabel()
        self.labelQUESBOutputDegradedHabitat.setText('[QUESBOutput] Degraded habitat:')
        self.layoutQUESBOutput.addWidget(self.labelQUESBOutputDegradedHabitat, 3, 0)
        
        self.lineEditQUESBOutputDegradedHabitat = QtGui.QLineEdit()
        self.lineEditQUESBOutputDegradedHabitat.setReadOnly(True)
        self.layoutQUESBOutput.addWidget(self.lineEditQUESBOutputDegradedHabitat, 3, 1)
        
        self.buttonSelectQUESBOutputDegradedHabitat = QtGui.QPushButton()
        self.buttonSelectQUESBOutputDegradedHabitat.setText('&Browse')
        self.layoutQUESBOutput.addWidget(self.buttonSelectQUESBOutputDegradedHabitat, 3, 2)
        
        self.labelQUESBOutputHabitatGain = QtGui.QLabel()
        self.labelQUESBOutputHabitatGain.setText('[QUESBOutput] Habitat gain:')
        self.layoutQUESBOutput.addWidget(self.labelQUESBOutputHabitatGain, 4, 0)
        
        self.lineEditQUESBOutputHabitatGain = QtGui.QLineEdit()
        self.lineEditQUESBOutputHabitatGain.setReadOnly(True)
        self.layoutQUESBOutput.addWidget(self.lineEditQUESBOutputHabitatGain, 4, 1)
        
        self.buttonSelectQUESBOutputHabitatGain = QtGui.QPushButton()
        self.buttonSelectQUESBOutputHabitatGain.setText('&Browse')
        self.layoutQUESBOutput.addWidget(self.buttonSelectQUESBOutputHabitatGain, 4, 2)
        
        self.labelQUESBOutputRecoveredHabitat = QtGui.QLabel()
        self.labelQUESBOutputRecoveredHabitat.setText('[QUESBOutput] Recovered habitat:')
        self.layoutQUESBOutput.addWidget(self.labelQUESBOutputRecoveredHabitat, 5, 0)
        
        self.lineEditQUESBOutputRecoveredHabitat = QtGui.QLineEdit()
        self.lineEditQUESBOutputRecoveredHabitat.setReadOnly(True)
        self.layoutQUESBOutput.addWidget(self.lineEditQUESBOutputRecoveredHabitat, 5, 1)
        
        self.buttonSelectQUESBOutputRecoveredHabitat = QtGui.QPushButton()
        self.buttonSelectQUESBOutputRecoveredHabitat.setText('&Browse')
        self.layoutQUESBOutput.addWidget(self.buttonSelectQUESBOutputRecoveredHabitat, 5, 2)
        
        # Process tab button
        self.layoutButtonQUESB = QtGui.QHBoxLayout()
        self.buttonProcessQUESB = QtGui.QPushButton()
        self.buttonProcessQUESB.setText('&Process')
        self.layoutButtonQUESB.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonQUESB.addWidget(self.buttonProcessQUESB)
        
        # Place the GroupBoxes
        self.layoutTabQUESB.addWidget(self.groupBoxQUESBParameters)
        self.layoutTabQUESB.addWidget(self.groupBoxQUESBOutput)
        self.layoutTabQUESB.addLayout(self.layoutButtonQUESB)
        
        #***********************************************************
        # Setup 'QUES-H' tab
        #***********************************************************
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
        
        #***********************************************************
        # 'Watershed Delineation' sub tab
        #***********************************************************
        
        
        
        #***********************************************************
        # 'Hydrological Response Unit Definition' sub tab
        #***********************************************************
        # 'Functions' GroupBox
        self.groupBoxHRUFunctions = QtGui.QGroupBox('Functions')
        self.layoutGroupBoxHRUFunctions = QtGui.QVBoxLayout()
        self.layoutGroupBoxHRUFunctions.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxHRUFunctions.setLayout(self.layoutGroupBoxHRUFunctions)
        self.layoutHRUFunctionsInfo = QtGui.QVBoxLayout()
        self.layoutHRUFunctions = QtGui.QGridLayout()
        self.layoutGroupBoxHRUFunctions.addLayout(self.layoutHRUFunctionsInfo)
        self.layoutGroupBoxHRUFunctions.addLayout(self.layoutHRUFunctions)
        
        self.labelHRUFunctionsInfo = QtGui.QLabel()
        self.labelHRUFunctionsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHRUFunctionsInfo.addWidget(self.labelHRUFunctionsInfo)
        
        self.checkBoxDominantHRU = QtGui.QCheckBox('Dominant HRU')
        self.checkBoxDominantLUSSL = QtGui.QCheckBox('Dominant Land Use, Soil, and Slope')
        self.checkBoxMultipleHRU = QtGui.QCheckBox('Multiple HRU')
        
        self.layoutHRUFunctions.addWidget(self.checkBoxDominantHRU)
        self.layoutHRUFunctions.addWidget(self.checkBoxDominantLUSSL)
        self.layoutHRUFunctions.addWidget(self.checkBoxMultipleHRU)
        
        # 'Parameters' GroupBox
        self.groupBoxHRUParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxHRUParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxHRUParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxHRUParameters.setLayout(self.layoutGroupBoxHRUParameters)
        self.layoutHRUParametersInfo = QtGui.QVBoxLayout()
        self.layoutHRUParameters = QtGui.QGridLayout()
        self.layoutGroupBoxHRUParameters.addLayout(self.layoutHRUParametersInfo)
        self.layoutGroupBoxHRUParameters.addLayout(self.layoutHRUParameters)
        
        self.labelHRUParametersInfo = QtGui.QLabel()
        self.labelHRUParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHRUParametersInfo.addWidget(self.labelHRUParametersInfo)
        
        self.labelHRUWorkingDir = QtGui.QLabel()
        self.labelHRUWorkingDir.setText('Working directory:')
        self.layoutHRUParameters.addWidget(self.labelHRUWorkingDir, 0, 0)
        
        self.lineEditHRUWorkingDir = QtGui.QLineEdit()
        self.lineEditHRUWorkingDir.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUWorkingDir, 0, 1)
        
        self.buttonSelectHRUWorkingDir = QtGui.QPushButton()
        self.buttonSelectHRUWorkingDir.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUWorkingDir, 0, 2)
        
        self.labelHRULandUseMap = QtGui.QLabel()
        self.labelHRULandUseMap.setText('Land use map:')
        self.layoutHRUParameters.addWidget(self.labelHRULandUseMap, 1, 0)
        
        self.lineEditHRULandUseMap = QtGui.QLineEdit()
        self.lineEditHRULandUseMap.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRULandUseMap, 1, 1)
        
        self.buttonSelectHRULandUseMap = QtGui.QPushButton()
        self.buttonSelectHRULandUseMap.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRULandUseMap, 1, 2)
        
        self.labelHRUSoilMap = QtGui.QLabel()
        self.labelHRUSoilMap.setText('Soil map:')
        self.layoutHRUParameters.addWidget(self.labelHRUSoilMap, 2, 0)
        
        self.lineEditHRUSoilMap = QtGui.QLineEdit()
        self.lineEditHRUSoilMap.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSoilMap, 2, 1)
        
        self.buttonSelectHRUSoilMap = QtGui.QPushButton()
        self.buttonSelectHRUSoilMap.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSoilMap, 2, 2)
        
        self.labelHRUSlopeMap = QtGui.QLabel()
        self.labelHRUSlopeMap.setText('Slope map:')
        self.layoutHRUParameters.addWidget(self.labelHRUSlopeMap, 3, 0)
        
        self.lineEditHRUSlopeMap = QtGui.QLineEdit()
        self.lineEditHRUSlopeMap.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSlopeMap, 3, 1)
        
        self.buttonSelectHRUSlopeMap = QtGui.QPushButton()
        self.buttonSelectHRUSlopeMap.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSlopeMap, 3, 2)
        
        self.labelHRUSubcatchmentMap = QtGui.QLabel()
        self.labelHRUSubcatchmentMap.setText('Subcatchment map:')
        self.layoutHRUParameters.addWidget(self.labelHRUSubcatchmentMap, 4, 0)
        
        self.lineEditHRUSubcatchmentMap = QtGui.QLineEdit()
        self.lineEditHRUSubcatchmentMap.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSubcatchmentMap, 4, 1)
        
        self.buttonSelectHRUSubcatchmentMap = QtGui.QPushButton()
        self.buttonSelectHRUSubcatchmentMap.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSubcatchmentMap, 4, 2)
        
        self.labelHRULandUseClassification = QtGui.QLabel()
        self.labelHRULandUseClassification.setText('Land use classification:')
        self.layoutHRUParameters.addWidget(self.labelHRULandUseClassification, 5, 0)
        
        self.lineEditHRULandUseClassification = QtGui.QLineEdit()
        self.lineEditHRULandUseClassification.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRULandUseClassification, 5, 1)
        
        self.buttonSelectHRULandUseClassification = QtGui.QPushButton()
        self.buttonSelectHRULandUseClassification.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRULandUseClassification, 5, 2)
        
        self.labelHRUSoilClassification = QtGui.QLabel()
        self.labelHRUSoilClassification.setText('Soil classification:')
        self.layoutHRUParameters.addWidget(self.labelHRUSoilClassification, 6, 0)
        
        self.lineEditHRUSoilClassification = QtGui.QLineEdit()
        self.lineEditHRUSoilClassification.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSoilClassification, 6, 1)
        
        self.buttonSelectHRUSoilClassification = QtGui.QPushButton()
        self.buttonSelectHRUSoilClassification.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSoilClassification, 6, 2)
        
        self.labelHRUSlopeClassification = QtGui.QLabel()
        self.labelHRUSlopeClassification.setText('Slope classification:')
        self.layoutHRUParameters.addWidget(self.labelHRUSlopeClassification, 7, 0)
        
        self.lineEditHRUSlopeClassification = QtGui.QLineEdit()
        self.lineEditHRUSlopeClassification.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSlopeClassification, 7, 1)
        
        self.buttonSelectHRUSlopeClassification = QtGui.QPushButton()
        self.buttonSelectHRUSlopeClassification.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSlopeClassification, 7, 2)
        
        self.labelHRUAreaName = QtGui.QLabel()
        self.labelHRUAreaName.setText('&Area name:')
        self.layoutHRUParameters.addWidget(self.labelHRUAreaName, 8, 0)
        
        self.lineEditHRUAreaName = QtGui.QLineEdit()
        self.lineEditHRUAreaName.setText('areaname')
        self.layoutHRUParameters.addWidget(self.lineEditHRUAreaName, 8, 1)
        self.labelHRUAreaName.setBuddy(self.lineEditHRUAreaName)
        
        self.labelHRUPeriod = QtGui.QLabel()
        self.labelHRUPeriod.setText('Pe&riod:')
        self.layoutHRUParameters.addWidget(self.labelHRUPeriod, 9, 0)
        
        self.spinBoxHRUPeriod = QtGui.QSpinBox()
        self.spinBoxHRUPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxHRUPeriod.setValue(td.year)
        self.layoutHRUParameters.addWidget(self.spinBoxHRUPeriod, 9, 1)
        self.labelHRUPeriod.setBuddy(self.spinBoxHRUPeriod)
        
        self.labelMultipleHRULandUseThreshold = QtGui.QLabel()
        self.labelMultipleHRULandUseThreshold.setDisabled(True)
        self.labelMultipleHRULandUseThreshold.setText('Land use &threshold:')
        self.layoutHRUParameters.addWidget(self.labelMultipleHRULandUseThreshold, 10, 0)
        
        self.spinBoxMultipleHRULandUseThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRULandUseThreshold.setDisabled(True)
        self.spinBoxMultipleHRULandUseThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRULandUseThreshold.setValue(0)
        self.layoutHRUParameters.addWidget(self.spinBoxMultipleHRULandUseThreshold, 10, 1)
        self.labelMultipleHRULandUseThreshold.setBuddy(self.spinBoxMultipleHRULandUseThreshold)
        
        self.labelMultipleHRUSoilThreshold = QtGui.QLabel()
        self.labelMultipleHRUSoilThreshold.setDisabled(True)
        self.labelMultipleHRUSoilThreshold.setText('Soil t&hreshold:')
        self.layoutHRUParameters.addWidget(self.labelMultipleHRUSoilThreshold, 11, 0)
        
        self.spinBoxMultipleHRUSoilThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRUSoilThreshold.setDisabled(True)
        self.spinBoxMultipleHRUSoilThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRUSoilThreshold.setValue(0)
        self.layoutHRUParameters.addWidget(self.spinBoxMultipleHRUSoilThreshold, 11, 1)
        self.labelMultipleHRUSoilThreshold.setBuddy(self.spinBoxMultipleHRUSoilThreshold)
        
        self.labelMultipleHRUSlopeThreshold = QtGui.QLabel()
        self.labelMultipleHRUSlopeThreshold.setDisabled(True)
        self.labelMultipleHRUSlopeThreshold.setText('Slope th&reshold:')
        self.layoutHRUParameters.addWidget(self.labelMultipleHRUSlopeThreshold, 12, 0)
        
        self.spinBoxMultipleHRUSlopeThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRUSlopeThreshold.setDisabled(True)
        self.spinBoxMultipleHRUSlopeThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRUSlopeThreshold.setValue(0)
        self.layoutHRUParameters.addWidget(self.spinBoxMultipleHRUSlopeThreshold, 12, 1)
        self.labelMultipleHRUSlopeThreshold.setBuddy(self.spinBoxMultipleHRUSlopeThreshold)
        
        # Process tab button
        self.layoutButtonHRUDefinition = QtGui.QHBoxLayout()
        self.buttonProcessHRUDefinition = QtGui.QPushButton()
        self.buttonProcessHRUDefinition.setText('&Process')
        self.layoutButtonHRUDefinition.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonHRUDefinition.addWidget(self.buttonProcessHRUDefinition)
        
        # Place the GroupBoxes
        self.layoutTabHRUDefinition.addWidget(self.groupBoxHRUFunctions)
        self.layoutTabHRUDefinition.addWidget(self.groupBoxHRUParameters)
        self.layoutTabHRUDefinition.addLayout(self.layoutButtonHRUDefinition)
        
        #***********************************************************
        # 'Watershed Model Evaluation' sub tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxWatershedModelEvaluationParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxWatershedModelEvaluationParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedModelEvaluationParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedModelEvaluationParameters.setLayout(self.layoutGroupBoxWatershedModelEvaluationParameters)
        self.layoutWatershedModelEvaluationParametersInfo = QtGui.QVBoxLayout()
        self.layoutWatershedModelEvaluationParameters = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedModelEvaluationParameters.addLayout(self.layoutWatershedModelEvaluationParametersInfo)
        self.layoutGroupBoxWatershedModelEvaluationParameters.addLayout(self.layoutWatershedModelEvaluationParameters)
        
        self.labelWatershedModelEvaluationParametersInfo = QtGui.QLabel()
        self.labelWatershedModelEvaluationParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutWatershedModelEvaluationParametersInfo.addWidget(self.labelWatershedModelEvaluationParametersInfo)
        
        self.labelWatershedModelEvaluationWorkingDir = QtGui.QLabel()
        self.labelWatershedModelEvaluationWorkingDir.setText('Working directory:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationWorkingDir, 0, 0)
        
        self.lineEditWatershedModelEvaluationWorkingDir = QtGui.QLineEdit()
        self.lineEditWatershedModelEvaluationWorkingDir.setReadOnly(True)
        self.layoutWatershedModelEvaluationParameters.addWidget(self.lineEditWatershedModelEvaluationWorkingDir, 0, 1)
        
        self.buttonSelectWatershedModelEvaluationWorkingDir = QtGui.QPushButton()
        self.buttonSelectWatershedModelEvaluationWorkingDir.setText('&Browse')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.buttonSelectWatershedModelEvaluationWorkingDir, 0, 2)
        
        self.labelWatershedModelEvaluationDateInitial = QtGui.QLabel()
        self.labelWatershedModelEvaluationDateInitial.setText('Initial date:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationDateInitial, 1, 0)
        
        self.dateWatershedModelEvaluationDateInitial = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.dateWatershedModelEvaluationDateInitial.setCalendarPopup(True)
        self.dateWatershedModelEvaluationDateInitial.setDisplayFormat('dd/MM/yyyy')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.dateWatershedModelEvaluationDateInitial, 1, 1)
        
        self.labelWatershedModelEvaluationDateFinal = QtGui.QLabel()
        self.labelWatershedModelEvaluationDateFinal.setText('Final date:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationDateFinal, 2, 0)
        
        self.dateWatershedModelEvaluationDateFinal = QtGui.QDateEdit(QtCore.QDate.currentDate(), )
        self.dateWatershedModelEvaluationDateFinal.setCalendarPopup(True)
        self.dateWatershedModelEvaluationDateFinal.setDisplayFormat('dd/MM/yyyy')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.dateWatershedModelEvaluationDateFinal, 2, 1)
        
        self.labelWatershedModelEvaluationSWATModel = QtGui.QLabel()
        self.labelWatershedModelEvaluationSWATModel.setText('SWAT &model:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationSWATModel, 3, 0)
        
        SWATModel = {
            1: 'Skip',
            2: 'Run',
        }
        
        self.comboBoxWatershedModelEvaluationSWATModel = QtGui.QComboBox()
        
        for key, val in SWATModel.iteritems():
            self.comboBoxWatershedModelEvaluationSWATModel.addItem(val, key)
        
        self.layoutWatershedModelEvaluationParameters.addWidget(self.comboBoxWatershedModelEvaluationSWATModel, 3, 1)
        self.labelWatershedModelEvaluationSWATModel.setBuddy(self.comboBoxWatershedModelEvaluationSWATModel)
        
        self.labelWatershedModelEvaluationLocation = QtGui.QLabel()
        self.labelWatershedModelEvaluationLocation.setText('&Location:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationLocation, 4, 0)
        
        self.lineEditWatershedModelEvaluationLocation = QtGui.QLineEdit()
        self.lineEditWatershedModelEvaluationLocation.setText('location')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.lineEditWatershedModelEvaluationLocation, 4, 1)
        self.labelWatershedModelEvaluationLocation.setBuddy(self.lineEditWatershedModelEvaluationLocation)
        
        self.labelWatershedModelEvaluationOutletReachSubBasinID = QtGui.QLabel()
        self.labelWatershedModelEvaluationOutletReachSubBasinID.setText('Outlet reach/sub-basin ID:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationOutletReachSubBasinID, 5, 0)
        
        self.spinBoxWatershedModelEvaluationOutletReachSubBasinID = QtGui.QSpinBox()
        self.spinBoxWatershedModelEvaluationOutletReachSubBasinID.setRange(1, 99999)
        self.spinBoxWatershedModelEvaluationOutletReachSubBasinID.setValue(10)
        self.layoutWatershedModelEvaluationParameters.addWidget(self.spinBoxWatershedModelEvaluationOutletReachSubBasinID, 5, 1)
        self.labelWatershedModelEvaluationOutletReachSubBasinID.setBuddy(self.spinBoxWatershedModelEvaluationOutletReachSubBasinID)
        
        self.labelWatershedModelEvaluationObservedDebitFile = QtGui.QLabel()
        self.labelWatershedModelEvaluationObservedDebitFile.setText('Observed debit file:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationObservedDebitFile, 6, 0)
        
        self.lineEditWatershedModelEvaluationObservedDebitFile = QtGui.QLineEdit()
        self.lineEditWatershedModelEvaluationObservedDebitFile.setReadOnly(True)
        self.layoutWatershedModelEvaluationParameters.addWidget(self.lineEditWatershedModelEvaluationObservedDebitFile, 6, 1)
        
        self.buttonSelectWatershedModelEvaluationObservedDebitFile = QtGui.QPushButton()
        self.buttonSelectWatershedModelEvaluationObservedDebitFile.setText('&Browse')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.buttonSelectWatershedModelEvaluationObservedDebitFile, 6, 2)
        
        # 'Output' GroupBox
        self.groupBoxWatershedModelEvaluationOutput = QtGui.QGroupBox('Output')
        self.layoutGroupBoxWatershedModelEvaluationOutput = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedModelEvaluationOutput.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedModelEvaluationOutput.setLayout(self.layoutGroupBoxWatershedModelEvaluationOutput)
        self.layoutWatershedModelEvaluationOutputInfo = QtGui.QVBoxLayout()
        self.layoutWatershedModelEvaluationOutput = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedModelEvaluationOutput.addLayout(self.layoutWatershedModelEvaluationOutputInfo)
        self.layoutGroupBoxWatershedModelEvaluationOutput.addLayout(self.layoutWatershedModelEvaluationOutput)
        
        self.labelWatershedModelEvaluationOutputInfo = QtGui.QLabel()
        self.labelWatershedModelEvaluationOutputInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutWatershedModelEvaluationOutputInfo.addWidget(self.labelWatershedModelEvaluationOutputInfo)
        
        self.labelOutputWatershedModelEvaluation = QtGui.QLabel()
        self.labelOutputWatershedModelEvaluation.setText('[Output] Watershed model evaluation:')
        self.layoutWatershedModelEvaluationOutput.addWidget(self.labelOutputWatershedModelEvaluation, 0, 0)
        
        self.lineEditOutputWatershedModelEvaluation = QtGui.QLineEdit()
        self.lineEditOutputWatershedModelEvaluation.setReadOnly(True)
        self.layoutWatershedModelEvaluationOutput.addWidget(self.lineEditOutputWatershedModelEvaluation, 0, 1)
        
        self.buttonSelectOutputWatershedModelEvaluation = QtGui.QPushButton()
        self.buttonSelectOutputWatershedModelEvaluation.setText('&Browse')
        self.layoutWatershedModelEvaluationOutput.addWidget(self.buttonSelectOutputWatershedModelEvaluation, 0, 2)
        
        # Process tab button
        self.layoutButtonWatershedModelEvaluation = QtGui.QHBoxLayout()
        self.buttonProcessWatershedModelEvaluation = QtGui.QPushButton()
        self.buttonProcessWatershedModelEvaluation.setText('&Process')
        self.layoutButtonWatershedModelEvaluation.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonWatershedModelEvaluation.addWidget(self.buttonProcessWatershedModelEvaluation)
        
        # Place the GroupBoxes
        self.layoutTabWatershedModelEvaluation.addWidget(self.groupBoxWatershedModelEvaluationParameters)
        self.layoutTabWatershedModelEvaluation.addWidget(self.groupBoxWatershedModelEvaluationOutput)
        self.layoutTabWatershedModelEvaluation.addLayout(self.layoutButtonWatershedModelEvaluation)
        
        #***********************************************************
        # 'Watershed Indicators' sub tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxWatershedIndicatorsParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxWatershedIndicatorsParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedIndicatorsParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedIndicatorsParameters.setLayout(self.layoutGroupBoxWatershedIndicatorsParameters)
        self.layoutWatershedIndicatorsParametersInfo = QtGui.QVBoxLayout()
        self.layoutWatershedIndicatorsParameters = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedIndicatorsParameters.addLayout(self.layoutWatershedIndicatorsParametersInfo)
        self.layoutGroupBoxWatershedIndicatorsParameters.addLayout(self.layoutWatershedIndicatorsParameters)
        
        self.labelWatershedIndicatorsParametersInfo = QtGui.QLabel()
        self.labelWatershedIndicatorsParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutWatershedIndicatorsParametersInfo.addWidget(self.labelWatershedIndicatorsParametersInfo)
        
        self.labelWatershedIndicatorsSWATTXTINOUTDir = QtGui.QLabel()
        self.labelWatershedIndicatorsSWATTXTINOUTDir.setText('SWAT TXTINOUT directory:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsSWATTXTINOUTDir, 0, 0)
        
        self.lineEditWatershedIndicatorsSWATTXTINOUTDir = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsSWATTXTINOUTDir.setReadOnly(True)
        self.layoutWatershedIndicatorsParameters.addWidget(self.lineEditWatershedIndicatorsSWATTXTINOUTDir, 0, 1)
        
        self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir = QtGui.QPushButton()
        self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir.setText('&Browse')
        self.layoutWatershedIndicatorsParameters.addWidget(self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir, 0, 2)
        
        self.labelWatershedIndicatorsDateInitial = QtGui.QLabel()
        self.labelWatershedIndicatorsDateInitial.setText('Initial date:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsDateInitial, 1, 0)
        
        self.dateWatershedIndicatorsDateInitial = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.dateWatershedIndicatorsDateInitial.setCalendarPopup(True)
        self.dateWatershedIndicatorsDateInitial.setDisplayFormat('dd/MM/yyyy')
        self.layoutWatershedIndicatorsParameters.addWidget(self.dateWatershedIndicatorsDateInitial, 1, 1)
        
        self.labelWatershedIndicatorsDateFinal = QtGui.QLabel()
        self.labelWatershedIndicatorsDateFinal.setText('Final date:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsDateFinal, 2, 0)
        
        self.dateWatershedIndicatorsDateFinal = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.dateWatershedIndicatorsDateFinal.setCalendarPopup(True)
        self.dateWatershedIndicatorsDateFinal.setDisplayFormat('dd/MM/yyyy')
        self.layoutWatershedIndicatorsParameters.addWidget(self.dateWatershedIndicatorsDateFinal, 2, 1)
        
        self.labelWatershedIndicatorsSubWatershedPolygon = QtGui.QLabel()
        self.labelWatershedIndicatorsSubWatershedPolygon.setText('Sub watershed polygon:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsSubWatershedPolygon, 3, 0)
        
        self.lineEditWatershedIndicatorsSubWatershedPolygon = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsSubWatershedPolygon.setReadOnly(True)
        self.layoutWatershedIndicatorsParameters.addWidget(self.lineEditWatershedIndicatorsSubWatershedPolygon, 3, 1)
        
        self.buttonSelectWatershedIndicatorsSubWatershedPolygon = QtGui.QPushButton()
        self.buttonSelectWatershedIndicatorsSubWatershedPolygon.setText('&Browse')
        self.layoutWatershedIndicatorsParameters.addWidget(self.buttonSelectWatershedIndicatorsSubWatershedPolygon, 3, 2)
        
        self.labelWatershedIndicatorsLocation = QtGui.QLabel()
        self.labelWatershedIndicatorsLocation.setText('&Location:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsLocation, 4, 0)
        
        self.lineEditWatershedIndicatorsLocation = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsLocation.setText('location')
        self.layoutWatershedIndicatorsParameters.addWidget(self.lineEditWatershedIndicatorsLocation, 4, 1)
        self.labelWatershedIndicatorsLocation.setBuddy(self.lineEditWatershedIndicatorsLocation)
        
        self.labelWatershedIndicatorsSubWatershedOutput = QtGui.QLabel()
        self.labelWatershedIndicatorsSubWatershedOutput.setText('&Sub watershed output:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsSubWatershedOutput, 5, 0)
        
        self.spinBoxWatershedIndicatorsSubWatershedOutput = QtGui.QSpinBox()
        self.spinBoxWatershedIndicatorsSubWatershedOutput.setRange(1, 99999)
        self.spinBoxWatershedIndicatorsSubWatershedOutput.setValue(10)
        self.layoutWatershedIndicatorsParameters.addWidget(self.spinBoxWatershedIndicatorsSubWatershedOutput, 5, 1)
        self.labelWatershedIndicatorsSubWatershedOutput.setBuddy(self.spinBoxWatershedIndicatorsSubWatershedOutput)
        
        # 'Output' GroupBox
        self.groupBoxWatershedIndicatorsOutput = QtGui.QGroupBox('Output')
        self.layoutGroupBoxWatershedIndicatorsOutput = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedIndicatorsOutput.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedIndicatorsOutput.setLayout(self.layoutGroupBoxWatershedIndicatorsOutput)
        self.layoutWatershedIndicatorsOutputInfo = QtGui.QVBoxLayout()
        self.layoutWatershedIndicatorsOutput = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedIndicatorsOutput.addLayout(self.layoutWatershedIndicatorsOutputInfo)
        self.layoutGroupBoxWatershedIndicatorsOutput.addLayout(self.layoutWatershedIndicatorsOutput)
        
        self.labelWatershedIndicatorsOutputInfo = QtGui.QLabel()
        self.labelWatershedIndicatorsOutputInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutWatershedIndicatorsOutputInfo.addWidget(self.labelWatershedIndicatorsOutputInfo)
        
        self.labelWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators = QtGui.QLabel()
        self.labelWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setText('[Output] Initial year sub watershed level indicators:')
        self.layoutWatershedIndicatorsOutput.addWidget(self.labelWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators, 0, 0)
        
        self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setReadOnly(True)
        self.layoutWatershedIndicatorsOutput.addWidget(self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators, 0, 1)
        
        self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators = QtGui.QPushButton()
        self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setText('&Browse')
        self.layoutWatershedIndicatorsOutput.addWidget(self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators, 0, 2)
        
        self.labelWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators = QtGui.QLabel()
        self.labelWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setText('[Output] Final year sub watershed level indicators:')
        self.layoutWatershedIndicatorsOutput.addWidget(self.labelWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators, 1, 0)
        
        self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setReadOnly(True)
        self.layoutWatershedIndicatorsOutput.addWidget(self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators, 1, 1)
        
        self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators = QtGui.QPushButton()
        self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setText('&Browse')
        self.layoutWatershedIndicatorsOutput.addWidget(self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators, 1, 2)
        
        # Process tab button
        self.layoutButtonWatershedIndicators = QtGui.QHBoxLayout()
        self.buttonProcessWatershedIndicators = QtGui.QPushButton()
        self.buttonProcessWatershedIndicators.setText('&Process')
        self.layoutButtonWatershedIndicators.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonWatershedIndicators.addWidget(self.buttonProcessWatershedIndicators)
        
        # Place the GroupBoxes
        self.layoutTabWatershedIndicators.addWidget(self.groupBoxWatershedIndicatorsParameters)
        self.layoutTabWatershedIndicators.addWidget(self.groupBoxWatershedIndicatorsOutput)
        self.layoutTabWatershedIndicators.addLayout(self.layoutButtonWatershedIndicators)
        
        
        #***********************************************************
        # Setup 'Reclassification' tab
        #***********************************************************
        
        
        
        #***********************************************************
        # Setup 'Result' tab
        #***********************************************************
        
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 640)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensQUES, self).showEvent(event)
    
    
    #***********************************************************
    # 'QUES-C' tab QGroupBox toggle handlers
    #***********************************************************
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
    
    
    #***********************************************************
    # 'QUES-H' tab QGroupBox toggle handlers
    #***********************************************************
    def toggleMultipleHRU(self, checked):
        """
        """
        if checked:
            self.labelMultipleHRULandUseThreshold.setEnabled(True)
            self.spinBoxMultipleHRULandUseThreshold.setEnabled(True)
            self.labelMultipleHRUSoilThreshold.setEnabled(True)
            self.spinBoxMultipleHRUSoilThreshold.setEnabled(True)
            self.labelMultipleHRUSlopeThreshold.setEnabled(True)
            self.spinBoxMultipleHRUSlopeThreshold.setEnabled(True)
        else:
            self.labelMultipleHRULandUseThreshold.setDisabled(True)
            self.spinBoxMultipleHRULandUseThreshold.setDisabled(True)
            self.labelMultipleHRUSoilThreshold.setDisabled(True)
            self.spinBoxMultipleHRUSoilThreshold.setDisabled(True)
            self.labelMultipleHRUSlopeThreshold.setDisabled(True)
            self.spinBoxMultipleHRUSlopeThreshold.setDisabled(True)
    
    
    #***********************************************************
    # 'Pre-QUES' tab QPushButton handlers
    #***********************************************************
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
    
    
    def handlerSelectPreQUESWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditPreQUESWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectPreQUESPlanningUnit(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Map', QtCore.QDir.homePath(), 'Planning Unit Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditPreQUESPlanningUnit.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectPreQUESCsvPlanningUnit(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Lookup Table', QtCore.QDir.homePath(), 'Planning Unit Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditPreQUESCsvPlanningUnit.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandCoverCsvLandUse(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Lookup Table', QtCore.QDir.homePath(), 'Land Use Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandCoverCsvLandUse.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'QUES-C' tab QPushButton handlers
    #***********************************************************
    def handlerSelectCACsvfile(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Carbon Density Lookup Table', QtCore.QDir.homePath(), 'Carbon Density Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditCACsvfile.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectPCACsvfile(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Carbon Stock Lookup Table', QtCore.QDir.homePath(), 'Carbon Stock Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditPCACsvfile.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'QUES-B' tab QPushButton handlers
    #***********************************************************
    def handlerSelectQUESBCsvLandCover(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Lookup', QtCore.QDir.homePath(), 'Land Cover Lookup (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditQUESBCsvLandCover.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectQUESBCsvClassDescriptors(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Class Descriptors', QtCore.QDir.homePath(), 'Class Descriptors (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditQUESBCsvClassDescriptors.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectQUESBCsvEdgeContrast(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Edge Contrast', QtCore.QDir.homePath(), 'Edge Contrast (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditQUESBCsvEdgeContrast.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectQUESBCsvZoneLookup(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Zone Lookup', QtCore.QDir.homePath(), 'Zone Lookup (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditQUESBCsvZoneLookup.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectQUESBOutputTECIInitial(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select TECI Initial Output', QtCore.QDir.homePath(), 'TECI Initial (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditQUESBOutputTECIInitial.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectQUESBOutputTECIFinal(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select TECI Final Output', QtCore.QDir.homePath(), 'TECI Final (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditQUESBOutputTECIFinal.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectQUESBOutputHabitatLoss(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Habitat Loss Output', QtCore.QDir.homePath(), 'Habitat Loss (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditOutputHabitatLoss.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectQUESBOutputDegradedHabitat(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Degraded Habitat', QtCore.QDir.homePath(), 'Degraded Habitat (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditQUESBOutputDegradedHabitat.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectQUESBOutputHabitatGain(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Habitat Gain', QtCore.QDir.homePath(), 'Habitat Gain (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditQUESBOutputHabitatGain.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectQUESBOutputRecoveredHabitat(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Recovered Habitat Output', QtCore.QDir.homePath(), 'Recovered Habitat (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditQUESBOutputRecoveredHabitat.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    #***********************************************************
    # 'QUES-H' Hydrological Response Unit Definition tab QPushButton handlers
    #***********************************************************
    def handlerSelectHRUWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditHRUWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectHRULandUseMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map', QtCore.QDir.homePath(), 'Land Use Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditHRULandUseMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSoilMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Map', QtCore.QDir.homePath(), 'Soil Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditHRUSoilMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSlopeMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Map', QtCore.QDir.homePath(), 'Slope Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditHRUSlopeMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSubcatchmentMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Subcatchment Map', QtCore.QDir.homePath(), 'Subcatchment Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditHRUSubcatchmentMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRULandUseClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Classification', QtCore.QDir.homePath(), 'Land Use Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditHRULandUseClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSoilClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Classification', QtCore.QDir.homePath(), 'Soil Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditHRUSoilClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSlopeClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Classification', QtCore.QDir.homePath(), 'Slope Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditHRUSlopeClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'QUES-H' Watershed Model Evaluation tab QPushButton handlers
    #***********************************************************
    def handlerSelectWatershedModelEvaluationWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditWatershedModelEvaluationWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select working directory: %s', dir)
    
    
    def handlerSelectWatershedModelEvaluationObservedDebitFile(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Observed Debit File', QtCore.QDir.homePath(), 'Observed Debit File (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if file:
            self.lineEditWatershedModelEvaluationObservedDebitFile.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOutputWatershedModelEvaluation(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Watershed Model Evaluation Output', QtCore.QDir.homePath(), 'Watershed Model Evaluation (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOutputWatershedModelEvaluation.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    #***********************************************************
    # 'QUES-H' Watershed Indicators tab QPushButton handlers
    #***********************************************************
    def handlerSelectWatershedIndicatorsSWATTXTINOUTDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select SWAT TXTINOUT Directory'))
        
        if dir:
            self.lineEditWatershedIndicatorsSWATTXTINOUTDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectWatershedIndicatorsSubWatershedPolygon(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Sub Watershed Polygon', QtCore.QDir.homePath(), 'Sub Watershed Polygon (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if file:
            self.lineEditWatershedIndicatorsSubWatershedPolygon.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Initial Year Sub Watershed Level Indicators Output', QtCore.QDir.homePath(), 'Initial Year Sub Watershed Level Indicators (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators(self):
        """
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Final Year Sub Watershed Level Indicators Output', QtCore.QDir.homePath(), 'Final Year Sub Watershed Level Indicators (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSetings(self):
        """
        """
        # 'Pre-QUES' tab fields
        
        
        # 'QUES-C' Carbon Accounting tab fields
        self.main.appSettings['DialogLumensQUESCCarbonAccounting']['csvfile'] \
            = unicode(self.lineEditCACsvfile.text())
        self.main.appSettings['DialogLumensQUESCCarbonAccounting']['nodata'] \
            = self.spinBoxCANoDataValue.value()
        
        # 'QUES-C' Peatland Carbon Accounting tab fields
        self.main.appSettings['DialogLumensQUESCPeatlandCarbonAccounting']['csvfile'] \
            = unicode(self.lineEditPCACsvfile.text())
        
        # 'QUES-C' Summarize Multiple Period tab fields
        includePeat = 0
        
        if self.SMPCheckBox.isChecked():
            includePeat = 1
            
        self.main.appSettings['DialogLumensQUESCSummarizeMultiplePeriod']['checkbox'] \
            = includePeat
        
        # 'QUES-B' tab fields
        self.main.appSettings['DialogLumensQUESBAnalysis']['csvLandCover'] \
            = unicode(self.lineEditQUESBCsvLandCover.text())
        self.main.appSettings['DialogLumensQUESBAnalysis']['samplingGridRes'] \
            = self.spinBoxQUESBSamplingGridRes.value()
        self.main.appSettings['DialogLumensQUESBAnalysis']['samplingWindowSize'] \
            = self.spinBoxQUESBSamplingWindowSize.value()
        self.main.appSettings['DialogLumensQUESBAnalysis']['windowShape'] \
            = self.spinBoxQUESBWindowShape.value()
        self.main.appSettings['DialogLumensQUESBAnalysis']['nodata'] \
            = self.spinBoxQUESBNodata.value()
        self.main.appSettings['DialogLumensQUESBAnalysis']['csvClassDescriptors'] \
            = unicode(self.lineEditQUESBCsvClassDescriptors.text())
        self.main.appSettings['DialogLumensQUESBAnalysis']['csvEdgeContrast'] \
            = unicode(self.lineEditQUESBCsvEdgeContrast.text())
        self.main.appSettings['DialogLumensQUESBAnalysis']['csvZoneLookup'] \
            = unicode(self.lineEditQUESBCsvZoneLookup.text())
        self.main.appSettings['DialogLumensQUESBAnalysis']['refMapID'] \
            = self.comboBoxQUESBRefMapID.itemData(self.comboBoxQUESBRefMapID.currentIndex())
        
        outputTECIInitial = unicode(self.lineEditQUESBOutputTECIInitial.text())
        outputTECIFinal = unicode(self.lineEditQUESBOutputTECIFinal.text())
        outputHabitatLoss = unicode(self.lineEditQUESBOutputHabitatLoss.text())
        outputDegradedHabitat = unicode(self.lineEditQUESBOutputDegradedHabitat.text())
        outputHabitatGain = unicode(self.lineEditQUESBOutputHabitatGain.text())
        outputRecoveredHabitat = unicode(self.lineEditQUESBOutputRecoveredHabitat.text())
        
        if not outputTECIInitial:
            outputTECIInitial = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESBAnalysis']['outputTECIInitial'] = outputTECIInitial
        
        if not outputTECIFinal:
            outputTECIFinal = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESBAnalysis']['outputTECIFinal'] = outputTECIFinal
        
        if not outputHabitatLoss:
            outputHabitatLoss = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESBAnalysis']['outputHabitatLoss'] = outputHabitatLoss
        
        if not outputDegradedHabitat:
            outputDegradedHabitat = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESBAnalysis']['outputDegradedHabitat'] = outputDegradedHabitat
        
        if not outputHabitatGain:
            outputHabitatGain = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESBAnalysis']['outputHabitatGain'] = outputHabitatGain
        
        if not outputRecoveredHabitat:
            outputRecoveredHabitat = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESBAnalysis']['outputRecoveredHabitat'] = outputRecoveredHabitat
        
        # 'QUES-H' Hydrological Response Unit Definition tab fields
        self.main.appSettings['DialogLumensQUESHDominantHRU']['workingDir'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['workingDir'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['workingDir'] \
            = unicode(self.lineEditHRUWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensQUESHDominantHRU']['landUseMap'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['LandUseMap'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['landUseMap'] \
            = unicode(self.lineEditHRULandUseMap.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['soilMap'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['soilMap'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['soilMap'] \
            = unicode(self.lineEditHRUSoilMap.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['slopeMap'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['slopeMap'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['slopeMap'] \
            = unicode(self.lineEditHRUSlopeMap.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['subcatchmentMap'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['subcatchmentMap'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['subcatchmentMap'] \
            = unicode(self.lineEditHRUSubcatchmentMap.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['landUseClassification'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['landUseClassification'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['landUseClassification'] \
            = unicode(self.lineEditHRULandUseClassification.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['soilClassification'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['soilClassification'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['soilClassification'] \
            = unicode(self.lineEditHRUSoilClassification.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['slopeClassification'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['slopeClassification'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['slopeClassification'] \
            = unicode(self.lineEditHRUSlopeClassification.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['areaName'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['areaName'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['areaName'] \
            = unicode(self.lineEditHRUAreaName.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['period'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['period'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['period'] \
            = self.spinBoxHRUPeriod.value()
        self.main.appSettings['DialogLumensQUESHMultipleHRU']['landUseThreshold'] \
            = self.spinBoxMultipleHRULandUseThreshold.value()
        self.main.appSettings['DialogLumensQUESHMultipleHRU']['soilThreshold'] \
            = self.spinBoxMultipleHRUSoilThreshold.value()
        self.main.appSettings['DialogLumensQUESHMultipleHRU']['slopeThreshold'] \
            = self.spinBoxMultipleHRUSlopeThreshold.value()
        
        # 'QUES-H' Watershed Model Evaluation tab fields
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['workingDir'] = unicode(self.lineEditWatershedModelEvaluationWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['dateInitial'] = self.dateWatershedIndicatorsDateInitial.date().toString('dd/MM/yyyy')
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['dateFinal'] = self.dateWatershedModelEvaluationDateFinal.date().toString('dd/MM/yyyy')
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['SWATModel'] = self.comboBoxWatershedModelEvaluationSWATModel.itemData(self.comboBoxWatershedModelEvaluationSWATModel.currentIndex())
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['location'] = unicode(self.lineEditWatershedModelEvaluationLocation.text())
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['outletReachSubBasinID'] = self.spinBoxWatershedModelEvaluationOutletReachSubBasinID.value()
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['observedDebitFile'] = unicode(self.lineEditWatershedModelEvaluationObservedDebitFile.text())
        
        outputWatershedModelEvaluation = unicode(self.lineEditOutputWatershedModelEvaluation.text())
        
        if not outputWatershedModelEvaluation:
            outputWatershedModelEvaluation = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['outputWatershedModelEvaluation'] = outputWatershedModelEvaluation
        
        # 'QUES-H' Watershed Indicators tab fields
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['SWATTXTINOUTDir'] = unicode(self.lineEditWatershedIndicatorsSWATTXTINOUTDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['dateInitial'] = self.dateWatershedIndicatorsDateInitial.date().toString('dd/MM/yyyy')
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['dateFinal'] = self.dateWatershedIndicatorsDateFinal.date().toString('dd/MM/yyyy')
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['subWatershedPolygon'] = unicode(self.lineEditWatershedIndicatorsSubWatershedPolygon.text())
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['location'] = unicode(self.lineEditWatershedIndicatorsLocation.text())
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['subWatershedOutput'] = self.spinBoxWatershedIndicatorsSubWatershedOutput.value()
        
        outputInitialYearSubWatershedLevelIndicators = unicode(self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.text())
        outputFinalYearSubWatershedLevelIndicators = unicode(self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.text())
        
        if not outputInitialYearSubWatershedLevelIndicators:
            outputInitialYearSubWatershedLevelIndicators = '__UNSET__'
        
        if not outputFinalYearSubWatershedLevelIndicators:
            outputFinalYearSubWatershedLevelIndicators = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['outputInitialYearSubWatershedLevelIndicators'] = outputInitialYearSubWatershedLevelIndicators
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['outputFinalYearSubWatershedLevelIndicators'] = outputFinalYearSubWatershedLevelIndicators
    
    
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
    
    
    def handlerProcessQUESC(self):
        """
        """
        self.setAppSetings()
        
        if self.checkBoxCarbonAccounting.isChecked():
            formName = 'DialogLumensQUESCCarbonAccounting'
            algName = 'modeler:ques-c'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessQUESC.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['csvfile'],
                    self.main.appSettings[formName]['nodata'],
                )
                
                ##print outputs
                
                self.buttonProcessQUESC.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxPeatlandCarbonAccounting.isChecked():
            formName = 'DialogLumensQUESCPeatlandCarbonAccounting'
            algName = 'modeler:ques-c_peat'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessQUESC.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['csvfile'],
                )
                
                ##print outputs
                
                self.buttonProcessQUESC.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        
        if self.checkBoxSummarizeMultiplePeriod.isChecked():
            formName = 'DialogLumensQUESCSummarizeMultiplePeriod'
            algName = 'r:summarizemultipleperiod'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessQUESC.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['checkbox'],
                )
                
                ##print outputs
                
                self.buttonProcessQUESC.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    
    
    def handlerProcessQUESB(self):
        """
        """
        self.setAppSetings()
        
        formName = 'DialogLumensQUESBAnalysis'
        algName = 'modeler:ques-b'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            
            self.buttonProcessQUESB.setDisabled(True)
            
            outputTECIInitial = self.main.appSettings[formName]['outputTECIInitial']
            outputTECIFinal = self.main.appSettings[formName]['outputTECIFinal']
            outputHabitatLoss = self.main.appSettings[formName]['outputHabitatLoss']
            outputDegradedHabitat = self.main.appSettings[formName]['outputDegradedHabitat']
            outputHabitatGain = self.main.appSettings[formName]['outputHabitatGain']
            outputRecoveredHabitat = self.main.appSettings[formName]['outputRecoveredHabitat']
            
            if outputTECIInitial == '__UNSET__':
                outputTECIInitial = None
            
            if outputTECIFinal == '__UNSET__':
                outputTECIFinal = None
            
            if outputHabitatLoss == '__UNSET__':
                outputHabitatLoss = None
            
            if outputDegradedHabitat == '__UNSET__':
                outputDegradedHabitat = None
            
            if outputHabitatGain == '__UNSET__':
                outputHabitatGain = None
            
            if outputRecoveredHabitat == '__UNSET__':
                outputRecoveredHabitat = None
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['csvLandCover'],
                self.main.appSettings[formName]['samplingGridRes'],
                self.main.appSettings[formName]['samplingWindowSize'],
                self.main.appSettings[formName]['windowShape'],
                self.main.appSettings[formName]['nodata'],
                self.main.appSettings[formName]['csvClassDescriptors'],
                self.main.appSettings[formName]['csvEdgeContrast'],
                self.main.appSettings[formName]['csvZoneLookup'],
                self.main.appSettings[formName]['refMapID'],
                outputTECIInitial,
                outputTECIFinal,
                outputHabitatLoss,
                outputDegradedHabitat,
                outputHabitatGain,
                outputRecoveredHabitat,
            )
            
            ##print outputs
            
            self.buttonProcessQUESB.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    
    
    def handlerProcessQUESHHRUDefinition(self):
        """
        """
        self.setAppSetings()
        
        if self.checkBoxDominantHRU.isChecked():
            formName = 'DialogLumensQUESHDominantHRU'
            algName = 'modeler:ques-h_dhru'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessHRUDefinition.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['workingDir'],
                    self.main.appSettings[formName]['landUseMap'],
                    self.main.appSettings[formName]['soilMap'],
                    self.main.appSettings[formName]['slopeMap'],
                    self.main.appSettings[formName]['subcatchmentMap'],
                    self.main.appSettings[formName]['landUseClassification'],
                    self.main.appSettings[formName]['soilClassification'],
                    self.main.appSettings[formName]['slopeClassification'],
                    self.main.appSettings[formName]['areaName'],
                    self.main.appSettings[formName]['period'],
                )
                
                ##print outputs
                
                self.buttonProcessHRUDefinition.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxDominantLUSSL.isChecked():
            formName = 'DialogLumensQUESHDominantLUSSL'
            algName = 'modeler:ques-h_dlussl'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessHRUDefinition.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['workingDir'],
                    self.main.appSettings[formName]['landUseMap'],
                    self.main.appSettings[formName]['soilMap'],
                    self.main.appSettings[formName]['slopeMap'],
                    self.main.appSettings[formName]['subcatchmentMap'],
                    self.main.appSettings[formName]['landUseClassification'],
                    self.main.appSettings[formName]['soilClassification'],
                    self.main.appSettings[formName]['slopeClassification'],
                    self.main.appSettings[formName]['areaName'],
                    self.main.appSettings[formName]['period'],
                )
                
                ##print outputs
                
                self.buttonProcessHRUDefinition.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxMultipleHRU.isChecked():
            formName = 'DialogLumensQUESHMultipleHRU'
            algName = 'modeler:ques-h_mhru'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                
                self.buttonProcessHRUDefinition.setDisabled(True)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['workingDir'],
                    self.main.appSettings[formName]['landUseMap'],
                    self.main.appSettings[formName]['soilMap'],
                    self.main.appSettings[formName]['slopeMap'],
                    self.main.appSettings[formName]['subcatchmentMap'],
                    self.main.appSettings[formName]['landUseClassification'],
                    self.main.appSettings[formName]['soilClassification'],
                    self.main.appSettings[formName]['slopeClassification'],
                    self.main.appSettings[formName]['areaName'],
                    self.main.appSettings[formName]['period'],
                    self.main.appSettings[formName]['landUseThreshold'],
                    self.main.appSettings[formName]['soilThreshold'],
                    self.main.appSettings[formName]['slopeThreshold'],
                )
                
                ##print outputs
                
                self.buttonProcessHRUDefinition.setEnabled(True)
                
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    
    
    def handlerProcessQUESHWatershedModelEvaluation(self):
        """
        """
        self.setAppSetings()
        
        formName = 'DialogLumensQUESHWatershedModelEvaluation'
        algName = 'modeler:ques-h_watershed_model_evaluation'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            
            self.buttonProcessWatershedModelEvaluation.setDisabled(True)
            
            outputWatershedModelEvaluation = self.main.appSettings[formName]['outputWatershedModelEvaluation']
            
            if outputWatershedModelEvaluation == '__UNSET__':
                outputWatershedModelEvaluation = None
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['workingDir'],
                self.main.appSettings[formName]['period1'],
                self.main.appSettings[formName]['period2'],
                self.main.appSettings[formName]['SWATModel'],
                self.main.appSettings[formName]['location'],
                self.main.appSettings[formName]['outletReachSubBasinID'],
                self.main.appSettings[formName]['observedDebitFile'],
                outputWatershedModelEvaluation,
            )
            
            ##print outputs
            
            self.buttonProcessWatershedModelEvaluation.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    
    
    def handlerProcessQUESHWatershedIndicators(self):
        """
        """
        self.setAppSetings()
        
        formName = 'DialogLumensQUESHWatershedIndicators'
        algName = 'modeler:ques-h_watershed_indicators'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            
            self.buttonProcessWatershedIndicators.setDisabled(True)
            
            outputInitialYearSubWatershedLevelIndicators = self.main.appSettings[formName]['outputInitialYearSubWatershedLevelIndicators']
            outputFinalYearSubWatershedLevelIndicators = self.main.appSettings[formName]['outputFinalYearSubWatershedLevelIndicators']
            
            if outputInitialYearSubWatershedLevelIndicators == '__UNSET__':
                outputInitialYearSubWatershedLevelIndicators = None
            
            if outputFinalYearSubWatershedLevelIndicators == '__UNSET__':
                outputFinalYearSubWatershedLevelIndicators = None
            
            outputs = general.runalg(
                'modeler:ques-h_watershed_indicators',
                self.main.appSettings[formName]['SWATTXTINOUTDir'],
                self.main.appSettings[formName]['dateInitial'],
                self.main.appSettings[formName]['dateFinal'],
                self.main.appSettings[formName]['subWatershedPolygon'],
                self.main.appSettings[formName]['location'],
                self.main.appSettings[formName]['subWatershedOutput'],
                outputInitialYearSubWatershedLevelIndicators,
                outputFinalYearSubWatershedLevelIndicators,
            )
            
            ##print outputs
            
            self.buttonProcessWatershedIndicators.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
    
    