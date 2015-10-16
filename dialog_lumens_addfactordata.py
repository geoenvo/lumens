#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensAddFactorData(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensAddFactorData, self).__init__(parent)
        
        self.setupUi(self)
        
        self.buttonSelectRasterfile.clicked.connect(self.handlerSelectRasterfile)
        self.buttonLumensAddFactorData.clicked.connect(self.handlerLumensAddFactorData)
    
    
    def setupUi(self, parent):
        super(DialogLumensAddFactorData, self).setupUi(self)
        
        layoutLumensAddFactorData = QtGui.QGridLayout()
        
        self.labelRasterfile = QtGui.QLabel(parent)
        self.labelRasterfile.setText('Raster file:')
        layoutLumensAddFactorData.addWidget(self.labelRasterfile, 0, 0)
        
        self.lineEditRasterfile = QtGui.QLineEdit(parent)
        self.lineEditRasterfile.setReadOnly(True)
        layoutLumensAddFactorData.addWidget(self.lineEditRasterfile, 0, 1)
        
        self.buttonSelectRasterfile = QtGui.QPushButton(parent)
        self.buttonSelectRasterfile.setText('Select &Raster File')
        layoutLumensAddFactorData.addWidget(self.buttonSelectRasterfile, 1, 0, 1, 2)
        
        self.labelDescription = QtGui.QLabel(parent)
        self.labelDescription.setText('&Description:')
        layoutLumensAddFactorData.addWidget(self.labelDescription, 2, 0)
        
        self.lineEditDescription = QtGui.QLineEdit(parent)
        self.lineEditDescription.setText('description')
        layoutLumensAddFactorData.addWidget(self.lineEditDescription, 2, 1)
        
        self.labelDescription.setBuddy(self.lineEditDescription)
        
        self.buttonLumensAddFactorData = QtGui.QPushButton(parent)
        self.buttonLumensAddFactorData.setText('LUMENS Add Factor Data')
        layoutLumensAddFactorData.addWidget(self.buttonLumensAddFactorData, 4, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensAddFactorData)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle('Dialog: LUMENS Add Factor Data')
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectRasterfile(self):
        """Select a tif file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Raster File', QtCore.QDir.homePath(), 'Raster File (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditRasterfile.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['rasterfile'] = unicode(self.lineEditRasterfile.text())
        self.main.appSettings[type(self).__name__]['description'] = unicode(self.lineEditDescription.text())
    
    
    def handlerLumensAddFactorData(self):
        """LUMENS Add Factor Data
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: LUMENS Add Factor Data')
            
            self.buttonLumensAddFactorData.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:lumens_add_factor_data',
                self.main.appSettings[type(self).__name__]['rasterfile'],
                self.main.appSettings[type(self).__name__]['description'],
            )
            
            self.buttonLumensAddFactorData.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: LUMENS Add Factor Data')
            
            self.close()
            