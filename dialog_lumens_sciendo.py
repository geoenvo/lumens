#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
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
        
        self.tabSetup = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        self.tabReport = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabSetup, 'Setup')
        self.tabWidget.addTab(self.tabResult, 'Result')
        self.tabWidget.addTab(self.tabReport, 'Report')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        self.layoutTabSetup = QtGui.QVBoxLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        self.layoutTabReport = QtGui.QVBoxLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Setup' tab
        #***********************************************************
        # 'Base year' GroupBox
        self.groupBoxBaseYear = QtGui.QGroupBox('Base year')
        self.layoutGroupBoxBaseYear = QtGui.QVBoxLayout()
        self.groupBoxBaseYear.setLayout(self.layoutGroupBoxBaseYear)
        
        # Process tab button
        self.layoutButtonSetup = QtGui.QHBoxLayout()
        self.buttonProcessSetup = QtGui.QPushButton()
        self.buttonProcessSetup.setText('&Process')
        self.layoutButtonSetup.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonSetup.addWidget(self.buttonProcessSetup)
        
        self.layoutTabSetup.addWidget(self.groupBoxBaseYear)
        self.layoutTabSetup.addLayout(self.layoutButtonSetup)
        
        self.tabSetup.setLayout(self.layoutTabSetup)
        
        #***********************************************************
        # Setup 'Result' tab
        #***********************************************************
        self.tabResult.setLayout(self.layoutTabResult)
        
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
    