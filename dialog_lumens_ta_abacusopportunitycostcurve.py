#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensTAAbacusOpportunityCostCurve(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTAAbacusOpportunityCostCurve, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS TA Abacus Opportunity Cost Curve'
        
        self.setupUi(self)
        
        self.buttonSelectProjectFile.clicked.connect(self.handlerSelectProjectFile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensTAAbacusOpportunityCostCurve, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelProjectFile = QtGui.QLabel(parent)
        self.labelProjectFile.setText('Abacus project file:')
        layoutLumensDialog.addWidget(self.labelProjectFile, 0, 0)
        
        self.lineEditProjectFile = QtGui.QLineEdit(parent)
        self.lineEditProjectFile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditProjectFile, 0, 1)
        
        self.buttonSelectProjectFile = QtGui.QPushButton(parent)
        self.buttonSelectProjectFile.setText('Select &Abacus Project File')
        layoutLumensDialog.addWidget(self.buttonSelectProjectFile, 1, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 2, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['projectFile'] = unicode(self.lineEditProjectFile.text())
    
    
    def handlerSelectProjectFile(self):
        """Select Project File
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Project File', QtCore.QDir.homePath(), 'Project File (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditProjectFile.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:abacus_opportunity_cost',
                self.main.appSettings[type(self).__name__]['projectFile'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            