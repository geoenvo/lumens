#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensToolsREDDAbacusSP(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensToolsREDDAbacusSP, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS Tools REDD Abacus SP'
        
        self.setupUi(self)
        
        self.buttonSelectCarfile.clicked.connect(self.handlerSelectCarfile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensToolsREDDAbacusSP, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelCarfile = QtGui.QLabel(parent)
        self.labelCarfile.setText('Abacus project file:')
        layoutLumensDialog.addWidget(self.labelCarfile, 0, 0)
        
        self.lineEditCarfile = QtGui.QLineEdit(parent)
        self.lineEditCarfile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCarfile, 0, 1)
        
        self.buttonSelectCarfile = QtGui.QPushButton(parent)
        self.buttonSelectCarfile.setText('Select &Abacus Project File')
        layoutLumensDialog.addWidget(self.buttonSelectCarfile, 1, 0, 1, 2)
        
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
        self.main.appSettings[type(self).__name__]['carfile'] = unicode(self.lineEditCarfile.text())
    
    
    def handlerSelectCarfile(self):
        """Select Abacus Project File
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Abacus Project File', QtCore.QDir.homePath(), 'Abacus Project File (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditCarfile.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:redd_abacus_sp',
                self.main.appSettings[type(self).__name__]['carfile'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            