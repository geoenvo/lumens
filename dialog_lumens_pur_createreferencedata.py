#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensPURCreateReferenceData(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensPURCreateReferenceData, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS PUR Create Reference Data'
        
        self.setupUi(self)
        
        self.buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensPURCreateReferenceData, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelShapefile = QtGui.QLabel(parent)
        self.labelShapefile.setText('Shapefile:')
        layoutLumensDialog.addWidget(self.labelShapefile, 0, 0)
        
        self.lineEditShapefile = QtGui.QLineEdit(parent)
        self.lineEditShapefile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditShapefile, 0, 1)
        
        self.buttonSelectShapefile = QtGui.QPushButton(parent)
        self.buttonSelectShapefile.setText('Select &Shapefile')
        layoutLumensDialog.addWidget(self.buttonSelectShapefile, 1, 0, 1, 2)
        
        self.labelShapefileAttr = QtGui.QLabel(parent)
        self.labelShapefileAttr.setText('Shapefile &attribute:')
        layoutLumensDialog.addWidget(self.labelShapefileAttr, 2, 0)
        
        self.comboBoxShapefileAttr = QtGui.QComboBox(parent)
        self.comboBoxShapefileAttr.setDisabled(True)
        layoutLumensDialog.addWidget(self.comboBoxShapefileAttr, 2, 1)
        
        self.labelShapefileAttr.setBuddy(self.comboBoxShapefileAttr)
        
        self.labelDataTitle = QtGui.QLabel(parent)
        self.labelDataTitle.setText('Data &title:')
        layoutLumensDialog.addWidget(self.labelDataTitle, 3, 0)
        
        self.lineEditDataTitle = QtGui.QLineEdit(parent)
        self.lineEditDataTitle.setText('description')
        layoutLumensDialog.addWidget(self.lineEditDataTitle, 3, 1)
        
        self.labelDataTitle.setBuddy(self.lineEditDataTitle)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 4, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectShapefile(self):
        """Select a shp file and load the attributes in the shapefile attribute combobox
        """
        shapefile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Shapefile', QtCore.QDir.homePath(), 'Shapefile (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if shapefile:
            self.lineEditShapefile.setText(shapefile)
            
            registry = QgsProviderRegistry.instance()
            provider = registry.provider('ogr', shapefile)
            
            if not provider.isValid():
                logging.getLogger(type(self).__name__).error('invalid shapefile')
                
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            self.comboBoxShapefileAttr.clear()
            self.comboBoxShapefileAttr.addItems(sorted(attributes))
            self.comboBoxShapefileAttr.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('select shapefile: %s', shapefile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['shapefile'] = unicode(self.lineEditShapefile.text())
        self.main.appSettings[type(self).__name__]['shapefileAttr'] = unicode(self.comboBoxShapefileAttr.currentText())
        self.main.appSettings[type(self).__name__]['dataTitle'] = unicode(self.lineEditDataTitle.text())
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:pur_step1_create_reference_data',
                self.main.appSettings[type(self).__name__]['shapefile'],
                self.main.appSettings[type(self).__name__]['shapefileAttr'],
                self.main.appSettings[type(self).__name__]['dataTitle'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            