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
        self.buttonSelectWorkingDir = QtGui.QPushButton(parent)
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
        
        self.layoutTabPreQUES.addWidget(self.groupBoxPlanningUnit)
        self.layoutTabPreQUES.addWidget(self.groupBoxLandCover)
        self.layoutTabPreQUES.addLayout(self.layoutButtonPreQUES)
        
        self.tabPreQUES.setLayout(self.layoutTabPreQUES)
        
        #***********************************************************
        # Setup 'QUES-C' tab
        #***********************************************************
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
    