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
        self.addLandCoverRow('T3')
        
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
        self.groupBoxPeatlandCarbonAccounting = QtGui.QGroupBox('Carbon accounting')
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
        self.tabQUESB.setLayout(self.layoutTabQUESB)
        
        #***********************************************************
        # Setup 'QUES-H' tab
        #***********************************************************
        self.tabQUESH.setLayout(self.layoutTabQUESH)
        
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
        self.setMinimumSize(640, 480)
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
    