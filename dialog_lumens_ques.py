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
        
        # 'QUES-H' tab checkboxes
        self.checkBoxDominantHRU.toggled.connect(self.toggleDominantHRU)
        self.checkBoxDominantLUSSL.toggled.connect(self.toggleDominantLUSSL)
        self.checkBoxMultipleHRU.toggled.connect(self.toggleMultipleHRU)
        
        # 'QUES-H' Dominant HRU tab buttons
        self.buttonSelectDominantHRUWorkingDir.clicked.connect(self.handlerSelectDominantHRUWorkingDir)
        self.buttonSelectDominantHRULandUseMap.clicked.connect(self.handlerSelectDominantHRULandUseMap)
        self.buttonSelectDominantHRUSoilMap.clicked.connect(self.handlerSelectDominantHRUSoilMap)
        self.buttonSelectDominantHRUSlopeMap.clicked.connect(self.handlerSelectDominantHRUSlopeMap)
        self.buttonSelectDominantHRUSubcatchmentMap.clicked.connect(self.handlerSelectDominantHRUSubcatchmentMap)
        self.buttonSelectDominantHRULandUseClassification.clicked.connect(self.handlerSelectDominantHRULandUseClassification)
        self.buttonSelectDominantHRUSoilClassification.clicked.connect(self.handlerSelectDominantHRUSoilClassification)
        self.buttonSelectDominantHRUSlopeClassification.clicked.connect(self.handlerSelectDominantHRUSlopeClassification)
        
        # 'QUES-H' Dominant LUSSL tab buttons
        self.buttonSelectDominantLUSSLWorkingDir.clicked.connect(self.handlerSelectDominantLUSSLWorkingDir)
        self.buttonSelectDominantLUSSLLandUseMap.clicked.connect(self.handlerSelectDominantLUSSLLandUseMap)
        self.buttonSelectDominantLUSSLSoilMap.clicked.connect(self.handlerSelectDominantLUSSLSoilMap)
        self.buttonSelectDominantLUSSLSlopeMap.clicked.connect(self.handlerSelectDominantLUSSLSlopeMap)
        self.buttonSelectDominantLUSSLSubcatchmentMap.clicked.connect(self.handlerSelectDominantLUSSLSubcatchmentMap)
        self.buttonSelectDominantLUSSLLandUseClassification.clicked.connect(self.handlerSelectDominantLUSSLLandUseClassification)
        self.buttonSelectDominantLUSSLSoilClassification.clicked.connect(self.handlerSelectDominantLUSSLSoilClassification)
        self.buttonSelectDominantLUSSLSlopeClassification.clicked.connect(self.handlerSelectDominantLUSSLSlopeClassification)
        
        # 'QUES-H' Multiple HRU tab buttons
        self.buttonSelectMultipleHRUWorkingDir.clicked.connect(self.handlerSelectMultipleHRUWorkingDir)
        self.buttonSelectMultipleHRULandUseMap.clicked.connect(self.handlerSelectMultipleHRULandUseMap)
        self.buttonSelectMultipleHRUSoilMap.clicked.connect(self.handlerSelectMultipleHRUSoilMap)
        self.buttonSelectMultipleHRUSlopeMap.clicked.connect(self.handlerSelectMultipleHRUSlopeMap)
        self.buttonSelectMultipleHRUSubcatchmentMap.clicked.connect(self.handlerSelectMultipleHRUSubcatchmentMap)
        self.buttonSelectMultipleHRULandUseClassification.clicked.connect(self.handlerSelectMultipleHRULandUseClassification)
        self.buttonSelectMultipleHRUSoilClassification.clicked.connect(self.handlerSelectMultipleHRUSoilClassification)
        self.buttonSelectMultipleHRUSlopeClassification.clicked.connect(self.handlerSelectMultipleHRUSlopeClassification)
        
        # 'QUES-H' Watershed Model Evaluation tab buttons
        self.buttonSelectWatershedModelEvaluationWorkingDir.clicked.connect(self.handlerSelectWatershedModelEvaluationWorkingDir)
        self.buttonSelectWatershedModelEvaluationObservedDebitFile.clicked.connect(self.handlerSelectWatershedModelEvaluationObservedDebitFile)
        self.buttonSelectOutputWatershedModelEvaluation.clicked.connect(self.handlerSelectOutputWatershedModelEvaluation)
        
        # 'QUES-H' Watershed Indicators tab buttons
        self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir.clicked.connect(self.handlerSelectWatershedIndicatorsSWATTXTINOUTDir)
        self.buttonSelectWatershedIndicatorsSubWatershedPolygon.clicked.connect(self.handlerSelectWatershedIndicatorsSubWatershedPolygon)
        self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.clicked.connect(self.handlerSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators)
        self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.clicked.connect(self.handlerSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators)
        
    
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
        
        self.spinBoxSamplingGridRes = QtGui.QSpinBox()
        self.spinBoxSamplingGridRes.setRange(1, 9999)
        self.spinBoxSamplingGridRes.setValue(10000)
        self.layoutQUESBParameters.addWidget(self.spinBoxSamplingGridRes, 1, 1)
        self.labelQUESBSamplingGridRes.setBuddy(self.spinBoxSamplingGridRes)
        
        self.labelQUESBSamplingWindowSize = QtGui.QLabel()
        self.labelQUESBSamplingWindowSize.setText('Sampling &window size:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBSamplingWindowSize, 2, 0)
        
        self.spinBoxSamplingWindowSize = QtGui.QSpinBox()
        self.spinBoxSamplingWindowSize.setRange(1, 9999)
        self.spinBoxSamplingWindowSize.setValue(1000)
        self.layoutQUESBParameters.addWidget(self.spinBoxSamplingWindowSize, 2, 1)
        self.labelQUESBSamplingWindowSize.setBuddy(self.spinBoxSamplingWindowSize)
        
        self.labelQUESBWindowShape = QtGui.QLabel()
        self.labelQUESBWindowShape.setText('Window &shape:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBWindowShape, 3, 0)
        
        self.spinBoxWindowShape = QtGui.QSpinBox()
        self.spinBoxWindowShape.setRange(1, 9999)
        self.spinBoxWindowShape.setValue(1)
        self.layoutQUESBParameters.addWidget(self.spinBoxWindowShape, 3, 1)
        self.labelQUESBWindowShape.setBuddy(self.spinBoxWindowShape)
        
        self.labelQUESBNodata = QtGui.QLabel()
        self.labelQUESBNodata.setText('&No data value:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBNodata, 4, 0)
        
        self.spinBoxNodata = QtGui.QSpinBox()
        self.spinBoxNodata.setRange(-9999, 9999)
        self.spinBoxNodata.setValue(0)
        self.layoutQUESBParameters.addWidget(self.spinBoxNodata, 4, 1)
        self.labelQUESBNodata.setBuddy(self.spinBoxNodata)
        
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
        
        self.labelSWATModel = QtGui.QLabel()
        self.labelSWATModel.setText('SWAT &model:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelSWATModel, 3, 0)
        
        SWATModel = {
            1: 'Skip',
            2: 'Run',
        }
        
        self.comboBoxSWATModel = QtGui.QComboBox()
        
        for key, val in SWATModel.iteritems():
            self.comboBoxSWATModel.addItem(val, key)
        
        self.layoutWatershedModelEvaluationParameters.addWidget(self.comboBoxSWATModel, 3, 1)
        self.labelSWATModel.setBuddy(self.comboBoxSWATModel)
        
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
    def handlerSelectDominantHRUWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditDominantHRUWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectDominantHRULandUseMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map', QtCore.QDir.homePath(), 'Land Use Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditDominantHRULandUseMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantHRUSoilMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Map', QtCore.QDir.homePath(), 'Soil Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditDominantHRUSoilMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantHRUSlopeMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Map', QtCore.QDir.homePath(), 'Slope Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditDominantHRUSlopeMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantHRUSubcatchmentMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Subcatchment Map', QtCore.QDir.homePath(), 'Subcatchment Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditDominantHRUSubcatchmentMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantHRULandUseClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Classification', QtCore.QDir.homePath(), 'Land Use Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditDominantHRULandUseClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantHRUSoilClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Classification', QtCore.QDir.homePath(), 'Soil Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditDominantHRUSoilClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantHRUSlopeClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Classification', QtCore.QDir.homePath(), 'Slope Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditDominantHRUSlopeClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantLUSSLWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditDominantLUSSLWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectDominantLUSSLLandUseMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map', QtCore.QDir.homePath(), 'Land Use Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditDominantLUSSLLandUseMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantLUSSLSoilMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Map', QtCore.QDir.homePath(), 'Soil Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditDominantLUSSLSoilMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantLUSSLSlopeMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Map', QtCore.QDir.homePath(), 'Slope Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditDominantLUSSLSlopeMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantLUSSLSubcatchmentMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Subcatchment Map', QtCore.QDir.homePath(), 'Subcatchment Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditDominantLUSSLSubcatchmentMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantLUSSLLandUseClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Classification', QtCore.QDir.homePath(), 'Land Use Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditDominantLUSSLLandUseClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantLUSSLSoilClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Classification', QtCore.QDir.homePath(), 'Soil Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditDominantLUSSLSoilClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectDominantLUSSLSlopeClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Classification', QtCore.QDir.homePath(), 'Slope Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditDominantLUSSLSlopeClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleHRUWorkingDir(self):
        """
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditMultipleHRUWorkingDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectMultipleHRULandUseMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map', QtCore.QDir.homePath(), 'Land Use Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditMultipleHRULandUseMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleHRUSoilMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Map', QtCore.QDir.homePath(), 'Soil Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditMultipleHRUSoilMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleHRUSlopeMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Map', QtCore.QDir.homePath(), 'Slope Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditMultipleHRUSlopeMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleHRUSubcatchmentMap(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Subcatchment Map', QtCore.QDir.homePath(), 'Subcatchment Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditMultipleHRUSubcatchmentMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleHRULandUseClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Classification', QtCore.QDir.homePath(), 'Land Use Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditMultipleHRULandUseClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleHRUSoilClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Classification', QtCore.QDir.homePath(), 'Soil Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditMultipleHRUSoilClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleHRUSlopeClassification(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Classification', QtCore.QDir.homePath(), 'Slope Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditMultipleHRUSlopeClassification.setText(file)
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
    