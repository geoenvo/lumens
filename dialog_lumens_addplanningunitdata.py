#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensAddPlanningUnitData(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensAddPlanningUnitData, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS Add Planning Unit Data'
        
        self.setupUi(self)
        
        self.buttonSelectRasterfile.clicked.connect(self.handlerSelectRasterfile)
        self.buttonSelectCsvfile.clicked.connect(self.handlerSelectCsvfile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensAddPlanningUnitData, self).showEvent(event)
        self.loadSelectedRasterLayer()
    
    
    def loadSelectedRasterLayer(self):
        """Load the selected raster layer into the raster field
        """
        selectedIndexes = self.main.layerListView.selectedIndexes()
        
        if not selectedIndexes:
            return
        
        layerItemIndex = selectedIndexes[0]
        layerItem = self.main.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        
        if layerItemData['layerType'] == 'raster':
            self.lineEditRasterfile.setText(layerItemData['layerFile'])
    
    
    def setupUi(self, parent):
        super(DialogLumensAddPlanningUnitData, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelRasterfile = QtGui.QLabel(parent)
        self.labelRasterfile.setText('Planning unit:')
        layoutLumensDialog.addWidget(self.labelRasterfile, 0, 0)
        
        self.lineEditRasterfile = QtGui.QLineEdit(parent)
        self.lineEditRasterfile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditRasterfile, 0, 1)
        
        self.buttonSelectRasterfile = QtGui.QPushButton(parent)
        self.buttonSelectRasterfile.setText('Select &Planning Unit')
        layoutLumensDialog.addWidget(self.buttonSelectRasterfile, 1, 0, 1, 2)
        
        self.labelCsvfile = QtGui.QLabel(parent)
        self.labelCsvfile.setText('Planning unit lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvfile, 2, 0)
        
        self.lineEditCsvfile = QtGui.QLineEdit(parent)
        self.lineEditCsvfile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvfile, 2, 1)
        
        self.buttonSelectCsvfile = QtGui.QPushButton(parent)
        self.buttonSelectCsvfile.setText('Select &Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvfile, 3, 0, 1, 2)
        
        self.labelDescription = QtGui.QLabel(parent)
        self.labelDescription.setText('&Description:')
        layoutLumensDialog.addWidget(self.labelDescription, 4, 0)
        
        self.lineEditDescription = QtGui.QLineEdit(parent)
        self.lineEditDescription.setText('planning_unit')
        layoutLumensDialog.addWidget(self.lineEditDescription, 4, 1)
        
        self.labelDescription.setBuddy(self.lineEditDescription)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 5, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectRasterfile(self):
        """Select a tif file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Raster File', QtCore.QDir.homePath(), 'Planning Unit Raster File (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditRasterfile.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectCsvfile(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Lookup Table', QtCore.QDir.homePath(), 'Planning Unit Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvfile.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['rasterfile'] = unicode(self.lineEditRasterfile.text())
        self.main.appSettings[type(self).__name__]['csvfile'] = unicode(self.lineEditCsvfile.text())
        self.main.appSettings[type(self).__name__]['description'] = unicode(self.lineEditDescription.text())
    
    
    def handlerLumensDialogSubmit(self):
        """LUMENS Add Factor Data
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:lumens_add_planning_unit',
                self.main.appSettings[type(self).__name__]['rasterfile'],
                self.main.appSettings[type(self).__name__]['csvfile'],
                self.main.appSettings[type(self).__name__]['description'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            