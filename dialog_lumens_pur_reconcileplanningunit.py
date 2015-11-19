#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensPURReconcilePlanningUnit(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensPURReconcilePlanningUnit, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS PUR Reconcile Planning Unit'
        
        self.setupUi(self)
        
        self.buttonSelectOutputFile.clicked.connect(self.handlerSelectOutputFile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensPURReconcilePlanningUnit, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelOutputFile = QtGui.QLabel(parent)
        self.labelOutputFile.setText('Output file:')
        layoutLumensDialog.addWidget(self.labelOutputFile, 0, 0)
        
        self.lineEditOutputFile = QtGui.QLineEdit(parent)
        self.lineEditOutputFile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputFile, 0, 1)
        
        self.buttonSelectOutputFile = QtGui.QPushButton(parent)
        self.buttonSelectOutputFile.setText('Select &Output File')
        layoutLumensDialog.addWidget(self.buttonSelectOutputFile, 1, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 2, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectOutputFile(self):
        """Select a output file
        """
        shapefile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Output File', QtCore.QDir.homePath(), 'Output Shapefile (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if shapefile:
            self.lineEditShapefile.setText(shapefile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', shapefile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        outputFile = unicode(self.lineEditOutputFile.text())
        
        if not outputFile:
            outputFile = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputFile'] = outputFile
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputFile = self.main.appSettings[type(self).__name__]['outputFile']
            
            if outputFile == '__UNSET__':
                outputFile = None
            
            outputs = general.runalg(
                'modeler:pur_step3_reconcile_planning_unit',
                outputFile,
            )
            
            # temporary output file
            if not outputFile:
                self.main.appSettings[type(self).__name__]['outputFile'] = outputs['OUTPUT_ALG1']
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            