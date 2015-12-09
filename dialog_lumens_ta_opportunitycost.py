#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
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
        
        self.tabWidget.addTab(self.tabAbacusOpportunityCost, 'Abacus opportunity cost')
        self.tabWidget.addTab(self.tabOpportunityCostCurve, 'Opportunity cost curve')
        self.tabWidget.addTab(self.tabOpportunityCostMap, 'Opportunity cost map')
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
        # Setup 'Opportunity cost map' tab
        #***********************************************************
        self.tabOpportunityCostMap.setLayout(self.layoutTabOpportunityCostMap)
        
        #***********************************************************
        # Setup 'Opportunity cost curve' tab
        #***********************************************************
        self.tabOpportunityCostCurve.setLayout(self.layoutTabOpportunityCostCurve)
        
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