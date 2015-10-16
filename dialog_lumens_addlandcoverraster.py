#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensAddLandcoverRaster(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensAddLandcoverRaster, self).__init__(parent)
        
        self.setupUi(self)
        
        self.buttonSelectRasterfile.clicked.connect(self.handlerSelectRasterfile)
        self.buttonLumensAddLandcoverRaster.clicked.connect(self.handlerLumensAddLandcoverRaster)
    
    
    def setupUi(self, parent):
        super(DialogLumensAddLandcoverRaster, self).setupUi(self)
        
        layoutLumensAddLandcoverRaster = QtGui.QGridLayout()
        
        self.labelRasterfile = QtGui.QLabel(parent)
        self.labelRasterfile.setText('Raster file:')
        layoutLumensAddLandcoverRaster.addWidget(self.labelRasterfile, 0, 0)
        
        self.lineEditRasterfile = QtGui.QLineEdit(parent)
        self.lineEditRasterfile.setReadOnly(True)
        layoutLumensAddLandcoverRaster.addWidget(self.lineEditRasterfile, 0, 1)
        
        self.buttonSelectRasterfile = QtGui.QPushButton(parent)
        self.buttonSelectRasterfile.setText('Select &Raster File')
        layoutLumensAddLandcoverRaster.addWidget(self.buttonSelectRasterfile, 1, 0, 1, 2)
        
        self.labelPeriod = QtGui.QLabel(parent)
        self.labelPeriod.setText('&Period:')
        layoutLumensAddLandcoverRaster.addWidget(self.labelPeriod, 2, 0)
        
        self.spinBoxPeriod = QtGui.QSpinBox(parent)
        self.spinBoxPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod.setValue(td.year)
        layoutLumensAddLandcoverRaster.addWidget(self.spinBoxPeriod, 2, 1)
        
        self.labelPeriod.setBuddy(self.spinBoxPeriod)
        
        self.labelDescription = QtGui.QLabel(parent)
        self.labelDescription.setText('&Description:')
        layoutLumensAddLandcoverRaster.addWidget(self.labelDescription, 3, 0)
        
        self.lineEditDescription = QtGui.QLineEdit(parent)
        self.lineEditDescription.setText('description')
        layoutLumensAddLandcoverRaster.addWidget(self.lineEditDescription, 3, 1)
        
        self.labelDescription.setBuddy(self.lineEditDescription)
        
        self.buttonLumensAddLandcoverRaster = QtGui.QPushButton(parent)
        self.buttonLumensAddLandcoverRaster.setText('LUMENS Add Land Cover Raster')
        layoutLumensAddLandcoverRaster.addWidget(self.buttonLumensAddLandcoverRaster, 4, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensAddLandcoverRaster)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle('Dialog: LUMENS Add Land Cover Raster')
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
        self.main.appSettings[type(self).__name__]['period'] = self.spinBoxPeriod.value()
        self.main.appSettings[type(self).__name__]['description'] = unicode(self.lineEditDescription.text())
    
    
    def handlerLumensAddLandcoverRaster(self):
        """LUMENS Add Landcover Raster
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: LUMENS Add Land Cover Raster')
            
            self.buttonLumensAddLandcoverRaster.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:lumens_add_landcover_raster',
                self.main.appSettings[type(self).__name__]['rasterfile'],
                self.main.appSettings[type(self).__name__]['period'],
                self.main.appSettings[type(self).__name__]['description'],
            )
            
            self.buttonLumensAddLandcoverRaster.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: LUMENS Add Land Cover Raster')
            
            self.close()
            