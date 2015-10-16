#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensAddPeat(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensAddPeat, self).__init__(parent)
        
        self.setupUi(self)
        
        self.buttonSelectRasterfile.clicked.connect(self.handlerSelectRasterfile)
        self.buttonLumensAddPeat.clicked.connect(self.handlerLumensAddPeat)
    
    
    def setupUi(self, parent):
        super(DialogLumensAddPeat, self).setupUi(self)
        
        layoutLumensAddPeat = QtGui.QGridLayout()
        
        self.labelRasterfile = QtGui.QLabel(parent)
        self.labelRasterfile.setText('Raster file:')
        layoutLumensAddPeat.addWidget(self.labelRasterfile, 0, 0)
        
        self.lineEditRasterfile = QtGui.QLineEdit(parent)
        self.lineEditRasterfile.setReadOnly(True)
        layoutLumensAddPeat.addWidget(self.lineEditRasterfile, 0, 1)
        
        self.buttonSelectRasterfile = QtGui.QPushButton(parent)
        self.buttonSelectRasterfile.setText('Select &Raster File')
        layoutLumensAddPeat.addWidget(self.buttonSelectRasterfile, 1, 0, 1, 2)
        
        self.labelDescription = QtGui.QLabel(parent)
        self.labelDescription.setText('&Description:')
        layoutLumensAddPeat.addWidget(self.labelDescription, 2, 0)
        
        self.lineEditDescription = QtGui.QLineEdit(parent)
        self.lineEditDescription.setText('description')
        layoutLumensAddPeat.addWidget(self.lineEditDescription, 2, 1)
        
        self.labelDescription.setBuddy(self.lineEditDescription)
        
        self.buttonLumensAddPeat = QtGui.QPushButton(parent)
        self.buttonLumensAddPeat.setText('LUMENS Add Land Cover Raster')
        layoutLumensAddPeat.addWidget(self.buttonLumensAddPeat, 4, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensAddPeat)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle('Dialog: LUMENS Add Peat')
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
    
    
    def handlerLumensAddPeat(self):
        """LUMENS Add Peat
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: LUMENS Add Peat')
            
            self.buttonLumensAddPeat.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:lumens_add_peat',
                self.main.appSettings[type(self).__name__]['rasterfile'],
                self.main.appSettings[type(self).__name__]['description'],
            )
            
            self.buttonLumensAddPeat.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: LUMENS Add Peat')
            
            self.close()
            