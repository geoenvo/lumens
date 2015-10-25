#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensPURFinalization(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensPURFinalization, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS PUR Finalization'
        
        self.main.appSettings[type(self).__name__]['shapefile'] = self.main.appSettings['DialogLumensPURReconcilePlanningUnit']['outputFile']
        
        self.setupUi(self)
        
        self.buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensPURFinalization, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelShapefile = QtGui.QLabel(parent)
        self.labelShapefile.setText('Shapefile:')
        layoutLumensDialog.addWidget(self.labelShapefile, 0, 0)
        
        self.lineEditShapefile = QtGui.QLineEdit(parent)
        self.lineEditShapefile.setReadOnly(True)
        self.lineEditShapefile.setText(self.main.appSettings[type(self).__name__]['shapefile'])
        layoutLumensDialog.addWidget(self.lineEditShapefile, 0, 1)
        
        self.buttonSelectShapefile = QtGui.QPushButton(parent)
        self.buttonSelectShapefile.setText('Select &Shapefile')
        layoutLumensDialog.addWidget(self.buttonSelectShapefile, 1, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 2, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectShapefile(self):
        """Select a shp file
        """
        shapefile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Shapefile', QtCore.QDir.homePath(), 'Shapefile (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if shapefile:
            self.lineEditShapefile.setText(shapefile)
            logging.getLogger(type(self).__name__).info('select shapefile: %s', shapefile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['shapefile'] = unicode(self.lineEditShapefile.text())
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:pur_step4_finalization',
                self.main.appSettings[type(self).__name__]['shapefile'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            