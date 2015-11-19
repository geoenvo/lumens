#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensPreQUESLandcoverTrajectoriesAnalysis(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensPreQUESLandcoverTrajectoriesAnalysis, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS PreQUES Land Cover Trajectories Analysis'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectLandCoverT1.clicked.connect(self.handlerSelectLandCoverT1)
        self.buttonSelectLandCoverT2.clicked.connect(self.handlerSelectLandCoverT2)
        self.buttonSelectPlanningUnit.clicked.connect(self.handlerSelectPlanningUnit)
        self.buttonSelectCsvLandUse.clicked.connect(self.handlerSelectCsvLandUse)
        self.buttonSelectCsvPlanningUnit.clicked.connect(self.handlerSelectCsvPlanningUnit)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensPreQUESLandcoverTrajectoriesAnalysis, self).setupUi(self)
        
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
        
        self.labelLocation = QtGui.QLabel(parent)
        self.labelLocation.setText('&Location:')
        layoutLumensDialog.addWidget(self.labelLocation, 2, 0)
        
        self.lineEditLocation = QtGui.QLineEdit(parent)
        self.lineEditLocation.setText('location')
        layoutLumensDialog.addWidget(self.lineEditLocation, 2, 1)
        
        self.labelLocation.setBuddy(self.lineEditLocation)
        
        self.labelSpinBoxT1 = QtGui.QLabel(parent)
        self.labelSpinBoxT1.setText('Year of T&1:')
        layoutLumensDialog.addWidget(self.labelSpinBoxT1, 3, 0)
        
        self.spinBoxT1 = QtGui.QSpinBox(parent)
        self.spinBoxT1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxT1.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxT1, 3, 1)
        
        self.labelSpinBoxT1.setBuddy(self.spinBoxT1)
        
        self.labelSpinBoxT2 = QtGui.QLabel(parent)
        self.labelSpinBoxT2.setText('Year of T&2:')
        layoutLumensDialog.addWidget(self.labelSpinBoxT2, 4, 0)
        
        self.spinBoxT2 = QtGui.QSpinBox(parent)
        self.spinBoxT2.setRange(1, 9999)
        self.spinBoxT2.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxT2, 4, 1)
        
        self.labelSpinBoxT2.setBuddy(self.spinBoxT2)
        
        self.labelLandCoverT1 = QtGui.QLabel(parent)
        self.labelLandCoverT1.setText('Land cover map of T1:')
        layoutLumensDialog.addWidget(self.labelLandCoverT1, 5, 0)
        
        self.lineEditLandCoverT1 = QtGui.QLineEdit(parent)
        self.lineEditLandCoverT1.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandCoverT1, 5, 1)
        
        self.buttonSelectLandCoverT1 = QtGui.QPushButton(parent)
        self.buttonSelectLandCoverT1.setText('Select Land &Cover Map of T1')
        layoutLumensDialog.addWidget(self.buttonSelectLandCoverT1, 6, 0, 1, 2)
        
        self.labelLandCoverT2 = QtGui.QLabel(parent)
        self.labelLandCoverT2.setText('Land cover map of T2:')
        layoutLumensDialog.addWidget(self.labelLandCoverT2, 7, 0)
        
        self.lineEditLandCoverT2 = QtGui.QLineEdit(parent)
        self.lineEditLandCoverT2.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandCoverT2, 7, 1)
        
        self.buttonSelectLandCoverT2 = QtGui.QPushButton(parent)
        self.buttonSelectLandCoverT2.setText('Select Land Cover &Map of T2')
        layoutLumensDialog.addWidget(self.buttonSelectLandCoverT2, 8, 0, 1, 2)
        
        self.labelPlanningUnit = QtGui.QLabel(parent)
        self.labelPlanningUnit.setText('Planning unit map:')
        layoutLumensDialog.addWidget(self.labelPlanningUnit, 9, 0)
        
        self.lineEditPlanningUnit = QtGui.QLineEdit(parent)
        self.lineEditPlanningUnit.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditPlanningUnit, 9, 1)
        
        self.buttonSelectPlanningUnit = QtGui.QPushButton(parent)
        self.buttonSelectPlanningUnit.setText('Select &Planning Unit Map')
        layoutLumensDialog.addWidget(self.buttonSelectPlanningUnit, 10, 0, 1, 2)
        
        self.labelCsvLandUse = QtGui.QLabel(parent)
        self.labelCsvLandUse.setText('Land use lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvLandUse, 11, 0)
        
        self.lineEditCsvLandUse = QtGui.QLineEdit(parent)
        self.lineEditCsvLandUse.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvLandUse, 11, 1)
        
        self.buttonSelectCsvLandUse = QtGui.QPushButton(parent)
        self.buttonSelectCsvLandUse.setText('Select Land &Use Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvLandUse, 12, 0, 1, 2)
        
        self.labelCsvPlanningUnit = QtGui.QLabel(parent)
        self.labelCsvPlanningUnit.setText('Planning unit lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvPlanningUnit, 13, 0)
        
        self.lineEditCsvPlanningUnit = QtGui.QLineEdit(parent)
        self.lineEditCsvPlanningUnit.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvPlanningUnit, 13, 1)
        
        self.buttonSelectCsvPlanningUnit = QtGui.QPushButton(parent)
        self.buttonSelectCsvPlanningUnit.setText('&Select Planning Unit Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvPlanningUnit, 14, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 15, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectWorkingDir(self):
        """Select a folder as working dir
        """
        workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if workingDir:
            self.lineEditWorkingDir.setText(workingDir)
            
            logging.getLogger(type(self).__name__).info('select working directory: %s', workingDir)
    
    
    def handlerSelectLandCoverT1(self):
        """Select a raster file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Map of T1', QtCore.QDir.homePath(), 'Land Cover Map of T1 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditLandCoverT1.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectLandCoverT2(self):
        """Select a raster file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Map of T2', QtCore.QDir.homePath(), 'Land Cover Map of T2 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditLandCoverT2.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectLandCoverT1(self):
        """Select a raster file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Map of T1', QtCore.QDir.homePath(), 'Land Cover Map of T1 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditLandCoverT1.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectPlanningUnit(self):
        """Select a raster file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Map', QtCore.QDir.homePath(), 'Planning Unit Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditLandCoverT2.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectCsvLandUse(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Lookup Table', QtCore.QDir.homePath(), 'Land Use Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvLandUse.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerSelectCsvPlanningUnit(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Lookup Table', QtCore.QDir.homePath(), 'Planning Unit Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvPlanningUnit.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        # BUG? workingDir path separator must be forward slash
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['location'] = unicode(self.lineEditLocation.text())
        self.main.appSettings[type(self).__name__]['t1'] = self.spinBoxT1.value()
        self.main.appSettings[type(self).__name__]['t2'] = self.spinBoxT2.value()
        self.main.appSettings[type(self).__name__]['landCoverT1'] = unicode(self.lineEditLandCoverT1.text())
        self.main.appSettings[type(self).__name__]['landCoverT2'] = unicode(self.lineEditLandCoverT2.text())
        self.main.appSettings[type(self).__name__]['planningUnit'] = unicode(self.lineEditPlanningUnit.text())
        self.main.appSettings[type(self).__name__]['csvLandUse'] = unicode(self.lineEditCsvLandUse.text())
        self.main.appSettings[type(self).__name__]['csvPlanningUnit'] = unicode(self.lineEditCsvPlanningUnit.text())
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:pre-ques_trajectory',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['location'],
                self.main.appSettings[type(self).__name__]['t1'],
                self.main.appSettings[type(self).__name__]['t2'],
                self.main.appSettings[type(self).__name__]['landCoverT1'],
                self.main.appSettings[type(self).__name__]['landCoverT2'],
                self.main.appSettings[type(self).__name__]['planningUnit'],
                self.main.appSettings[type(self).__name__]['csvLandUse'],
                self.main.appSettings[type(self).__name__]['csvPlanningUnit'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            