#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensQUESHDominantHRU(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensQUESHDominantHRU, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS QUES-H Dominant HRU'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectLandUseMap.clicked.connect(self.handlerSelectLandUseMap)
        self.buttonSelectSoilMap.clicked.connect(self.handlerSelectSoilMap)
        self.buttonSelectSlopeMap.clicked.connect(self.handlerSelectSlopeMap)
        self.buttonSelectSubcatchmentMap.clicked.connect(self.handlerSelectSubcatchmentMap)
        self.buttonSelectLandUseClassification.clicked.connect(self.handlerSelectLandUseClassification)
        self.buttonSelectSoilClassification.clicked.connect(self.handlerSelectSoilClassification)
        self.buttonSelectSlopeClassification.clicked.connect(self.handlerSelectSlopeClassification)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensQUESHDominantHRU, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelWorkingDir = QtGui.QLabel(parent)
        self.labelWorkingDir.setText('Working directory:')
        layoutLumensDialog.addWidget(self.labelWorkingDir, 0, 0)
        
        self.lineEditWorkingDir = QtGui.QLineEdit(parent)
        self.lineEditWorkingDir.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditWorkingDir, 0, 1)
        
        self.buttonSelectWorkingDir = QtGui.QPushButton(parent)
        self.buttonSelectWorkingDir.setText('Select &Working Directory')
        layoutLumensDialog.addWidget(self.buttonSelectWorkingDir, 1, 0, 1, 2)
        
        self.labelLandUseMap = QtGui.QLabel(parent)
        self.labelLandUseMap.setText('Land use map:')
        layoutLumensDialog.addWidget(self.labelLandUseMap, 2, 0)
        
        self.lineEditLandUseMap = QtGui.QLineEdit(parent)
        self.lineEditLandUseMap.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandUseMap, 2, 1)
        
        self.buttonSelectLandUseMap = QtGui.QPushButton(parent)
        self.buttonSelectLandUseMap.setText('Select &Land Use Map')
        layoutLumensDialog.addWidget(self.buttonSelectLandUseMap, 3, 0, 1, 2)
        
        self.labelSoilMap = QtGui.QLabel(parent)
        self.labelSoilMap.setText('Soil map:')
        layoutLumensDialog.addWidget(self.labelSoilMap, 4, 0)
        
        self.lineEditSoilMap = QtGui.QLineEdit(parent)
        self.lineEditSoilMap.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditSoilMap, 4, 1)
        
        self.buttonSelectSoilMap = QtGui.QPushButton(parent)
        self.buttonSelectSoilMap.setText('Select &Soil Map')
        layoutLumensDialog.addWidget(self.buttonSelectSoilMap, 5, 0, 1, 2)
        
        self.labelSlopeMap = QtGui.QLabel(parent)
        self.labelSlopeMap.setText('Slope map:')
        layoutLumensDialog.addWidget(self.labelSlopeMap, 6, 0)
        
        self.lineEditSlopeMap = QtGui.QLineEdit(parent)
        self.lineEditSlopeMap.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditSlopeMap, 6, 1)
        
        self.buttonSelectSlopeMap = QtGui.QPushButton(parent)
        self.buttonSelectSlopeMap.setText('Select S&lope Map')
        layoutLumensDialog.addWidget(self.buttonSelectSlopeMap, 7, 0, 1, 2)
        
        self.labelSubcatchmentMap = QtGui.QLabel(parent)
        self.labelSubcatchmentMap.setText('Subcatchment map:')
        layoutLumensDialog.addWidget(self.labelSubcatchmentMap, 8, 0)
        
        self.lineEditSubcatchmentMap = QtGui.QLineEdit(parent)
        self.lineEditSubcatchmentMap.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditSubcatchmentMap, 8, 1)
        
        self.buttonSelectSubcatchmentMap = QtGui.QPushButton(parent)
        self.buttonSelectSubcatchmentMap.setText('Select Sub&catchment Map')
        layoutLumensDialog.addWidget(self.buttonSelectSubcatchmentMap, 9, 0, 1, 2)
        
        self.labelLandUseClassification = QtGui.QLabel(parent)
        self.labelLandUseClassification.setText('Land use classification:')
        layoutLumensDialog.addWidget(self.labelLandUseClassification, 10, 0)
        
        self.lineEditLandUseClassification = QtGui.QLineEdit(parent)
        self.lineEditLandUseClassification.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandUseClassification, 10, 1)
        
        self.buttonSelectLandUseClassification = QtGui.QPushButton(parent)
        self.buttonSelectLandUseClassification.setText('Select Land &Use Classification')
        layoutLumensDialog.addWidget(self.buttonSelectLandUseClassification, 11, 0, 1, 2)
        
        self.labelSoilClassification = QtGui.QLabel(parent)
        self.labelSoilClassification.setText('Soil classification:')
        layoutLumensDialog.addWidget(self.labelSoilClassification, 12, 0)
        
        self.lineEditSoilClassification = QtGui.QLineEdit(parent)
        self.lineEditSoilClassification.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditSoilClassification, 12, 1)
        
        self.buttonSelectSoilClassification = QtGui.QPushButton(parent)
        self.buttonSelectSoilClassification.setText('Select S&oil Classification')
        layoutLumensDialog.addWidget(self.buttonSelectSoilClassification, 13, 0, 1, 2)
        
        self.labelSlopeClassification = QtGui.QLabel(parent)
        self.labelSlopeClassification.setText('Slope classification:')
        layoutLumensDialog.addWidget(self.labelSlopeClassification, 14, 0)
        
        self.lineEditSlopeClassification = QtGui.QLineEdit(parent)
        self.lineEditSlopeClassification.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditSlopeClassification, 14, 1)
        
        self.buttonSelectSlopeClassification = QtGui.QPushButton(parent)
        self.buttonSelectSlopeClassification.setText('Select Slo&pe Classification')
        layoutLumensDialog.addWidget(self.buttonSelectSlopeClassification, 15, 0, 1, 2)
        
        self.labelAreaName = QtGui.QLabel(parent)
        self.labelAreaName.setText('&Area name:')
        layoutLumensDialog.addWidget(self.labelAreaName, 16, 0)
        
        self.lineEditAreaName = QtGui.QLineEdit(parent)
        self.lineEditAreaName.setText('areaname')
        layoutLumensDialog.addWidget(self.lineEditAreaName, 16, 1)
        
        self.labelAreaName.setBuddy(self.lineEditAreaName)
        
        self.labelPeriod = QtGui.QLabel(parent)
        self.labelPeriod.setText('Pe&riod:')
        layoutLumensDialog.addWidget(self.labelPeriod, 17, 0)
        
        self.spinBoxPeriod = QtGui.QSpinBox(parent)
        self.spinBoxPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxPeriod.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxPeriod, 17, 1)
        
        self.labelPeriod.setBuddy(self.spinBoxPeriod)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 18, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['landUseMap'] = unicode(self.lineEditLandUseMap.text())
        self.main.appSettings[type(self).__name__]['soilMap'] = unicode(self.lineEditSoilMap.text())
        self.main.appSettings[type(self).__name__]['slopeMap'] = unicode(self.lineEditSlopeMap.text())
        self.main.appSettings[type(self).__name__]['subcatchmentMap'] = unicode(self.lineEditSubcatchmentMap.text())
        self.main.appSettings[type(self).__name__]['landUseClassification'] = unicode(self.lineEditLandUseClassification.text())
        self.main.appSettings[type(self).__name__]['soilClassification'] = unicode(self.lineEditSoilClassification.text())
        self.main.appSettings[type(self).__name__]['slopeClassification'] = unicode(self.lineEditSlopeClassification.text())
        self.main.appSettings[type(self).__name__]['areaName'] = unicode(self.lineEditAreaName.text())
        self.main.appSettings[type(self).__name__]['period'] = self.spinBoxPeriod.value()
    
    
    def handlerSelectWorkingDir(self):
        """Select a folder as working dir
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if dir:
            self.lineEditWorkingDir.setText(dir)
            
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectLandUseMap(self):
        """Select a file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map', QtCore.QDir.homePath(), 'Land Use Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandUseMap.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectSoilMap(self):
        """Select a file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Map', QtCore.QDir.homePath(), 'Soil Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditSoilMap.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectSlopeMap(self):
        """Select a file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Map', QtCore.QDir.homePath(), 'Slope Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditSlopeMap.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectSubcatchmentMap(self):
        """Select a file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Subcatchment Map', QtCore.QDir.homePath(), 'Subcatchment Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditSubcatchmentMap.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseClassification(self):
        """Select a file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Classification', QtCore.QDir.homePath(), 'Land Use Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseClassification.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectSoilClassification(self):
        """Select a file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Classification', QtCore.QDir.homePath(), 'Soil Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditSoilClassification.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectSlopeClassification(self):
        """Select a file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Classification', QtCore.QDir.homePath(), 'Slope Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditSlopeClassification.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:ques-h_dhru',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['landUseMap'],
                self.main.appSettings[type(self).__name__]['soilMap'],
                self.main.appSettings[type(self).__name__]['slopeMap'],
                self.main.appSettings[type(self).__name__]['subcatchmentMap'],
                self.main.appSettings[type(self).__name__]['landUseClassification'],
                self.main.appSettings[type(self).__name__]['soilClassification'],
                self.main.appSettings[type(self).__name__]['slopeClassification'],
                self.main.appSettings[type(self).__name__]['areaName'],
                self.main.appSettings[type(self).__name__]['period'],
            )
            
            """
            print outputs
            """
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            