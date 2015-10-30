#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensSCIENDOCreateRasterCube(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDOCreateRasterCube, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS SCIENDO Create Raster Cube'
        
        self.setupUi(self)
        
        self.buttonSelectFactorsDir.clicked.connect(self.handlerSelectFactorsDir)
        self.buttonSelectLandUseLookup.clicked.connect(self.handlerSelectLandUseLookup)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensSCIENDOCreateRasterCube, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelFactorsDir = QtGui.QLabel(parent)
        self.labelFactorsDir.setText('Factors directory:')
        layoutLumensDialog.addWidget(self.labelFactorsDir, 0, 0)
        
        self.lineEditFactorsDir = QtGui.QLineEdit(parent)
        self.lineEditFactorsDir.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditFactorsDir, 0, 1)
        
        self.buttonSelectFactorsDir = QtGui.QPushButton(parent)
        self.buttonSelectFactorsDir.setText('Select &Factors Directory')
        layoutLumensDialog.addWidget(self.buttonSelectFactorsDir, 1, 0, 1, 2)
        
        self.labelLandUseLookup = QtGui.QLabel(parent)
        self.labelLandUseLookup.setText('Land use lookup table:')
        layoutLumensDialog.addWidget(self.labelLandUseLookup, 2, 0)
        
        self.lineEditLandUseLookup = QtGui.QLineEdit(parent)
        self.lineEditLandUseLookup.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandUseLookup, 2, 1)
        
        self.buttonSelectLandUseLookup = QtGui.QPushButton(parent)
        self.buttonSelectLandUseLookup.setText('Select &Land Use Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectLandUseLookup, 3, 0, 1, 2)
        
        self.labelSpinBoxBaseYear = QtGui.QLabel(parent)
        self.labelSpinBoxBaseYear.setText('Base &year:')
        layoutLumensDialog.addWidget(self.labelSpinBoxBaseYear, 4, 0)
        
        self.spinBoxBaseYear = QtGui.QSpinBox(parent)
        self.spinBoxBaseYear.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxBaseYear.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxBaseYear, 4, 1)
        
        self.labelSpinBoxBaseYear.setBuddy(self.spinBoxBaseYear)
        
        self.labelLocation = QtGui.QLabel(parent)
        self.labelLocation.setText('Location:')
        layoutLumensDialog.addWidget(self.labelLocation, 5, 0)
        
        self.lineEditLocation = QtGui.QLineEdit(parent)
        self.lineEditLocation.setText('location')
        layoutLumensDialog.addWidget(self.lineEditLocation, 5, 1)
        
        self.labelLocation.setBuddy(self.lineEditLocation)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 6, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['factorsDir'] = unicode(self.lineEditFactorsDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['landUseLookup'] = unicode(self.lineEditLandUseLookup.text())
        self.main.appSettings[type(self).__name__]['baseYear'] = self.spinBoxBaseYear.value()
        self.main.appSettings[type(self).__name__]['location'] = unicode(self.lineEditLocation.text())
    
    
    def handlerSelectFactorsDir(self):
        """Select a folder as factors dir
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Factors Directory'))
        
        if dir:
            self.lineEditFactorsDir.setText(dir)
            
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectLandUseLookup(self):
        """Select Land Use Lookup Table
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Lookup Table', QtCore.QDir.homePath(), 'Land Use Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseLookup.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:sciendo1_create_raster_cube',
                self.main.appSettings[type(self).__name__]['factorsDir'],
                self.main.appSettings[type(self).__name__]['landUseLookup'],
                self.main.appSettings[type(self).__name__]['baseYear'],
                self.main.appSettings[type(self).__name__]['location'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            