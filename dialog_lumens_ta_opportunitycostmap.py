#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensTAOpportunityCostMap(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensTAOpportunityCostMap, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS TA Opportunity Cost Map'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectLandUseT1.clicked.connect(self.handlerSelectLandUseT1)
        self.buttonSelectLandUseT2.clicked.connect(self.handlerSelectLandUseT2)
        self.buttonSelectPlanningUnit.clicked.connect(self.handlerSelectPlanningUnit)
        self.buttonSelectCsvCarbon.clicked.connect(self.handlerSelectCsvCarbon)
        self.buttonSelectCsvProfitability.clicked.connect(self.handlerSelectCsvProfitability)
        self.buttonSelectCsvPlanningUnit.clicked.connect(self.handlerSelectCsvPlanningUnit)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensTAOpportunityCostMap, self).setupUi(self)
        
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
        
        self.labelLandUseT1 = QtGui.QLabel(parent)
        self.labelLandUseT1.setText('Land use map T1:')
        layoutLumensDialog.addWidget(self.labelLandUseT1, 2, 0)
        
        self.lineEditLandUseT1 = QtGui.QLineEdit(parent)
        self.lineEditLandUseT1.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandUseT1, 2, 1)
        
        self.buttonSelectLandUseT1 = QtGui.QPushButton(parent)
        self.buttonSelectLandUseT1.setText('Select &Land Use Map T1')
        layoutLumensDialog.addWidget(self.buttonSelectLandUseT1, 3, 0, 1, 2)
        
        self.labelLandUseT2 = QtGui.QLabel(parent)
        self.labelLandUseT2.setText('Land use map T2:')
        layoutLumensDialog.addWidget(self.labelLandUseT2, 4, 0)
        
        self.lineEditLandUseT2 = QtGui.QLineEdit(parent)
        self.lineEditLandUseT2.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLandUseT2, 4, 1)
        
        self.buttonSelectLandUseT2 = QtGui.QPushButton(parent)
        self.buttonSelectLandUseT2.setText('Select Land &Use Map T2')
        layoutLumensDialog.addWidget(self.buttonSelectLandUseT2, 5, 0, 1, 2)
        
        self.labelPlanningUnit = QtGui.QLabel(parent)
        self.labelPlanningUnit.setText('Planning unit map:')
        layoutLumensDialog.addWidget(self.labelPlanningUnit, 6, 0)
        
        self.lineEditPlanningUnit = QtGui.QLineEdit(parent)
        self.lineEditPlanningUnit.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditPlanningUnit, 6, 1)
        
        self.buttonSelectPlanningUnit = QtGui.QPushButton(parent)
        self.buttonSelectPlanningUnit.setText('Select &Planning Unit Map')
        layoutLumensDialog.addWidget(self.buttonSelectPlanningUnit, 7, 0, 1, 2)
        
        self.labelCsvCarbon = QtGui.QLabel(parent)
        self.labelCsvCarbon.setText('Carbon lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvCarbon, 8, 0)
        
        self.lineEditCsvCarbon = QtGui.QLineEdit(parent)
        self.lineEditCsvCarbon.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvCarbon, 8, 1)
        
        self.buttonSelectCsvCarbon = QtGui.QPushButton(parent)
        self.buttonSelectCsvCarbon.setText('Select &Carbon Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvCarbon, 9, 0, 1, 2)
        
        self.labelCsvProfitability = QtGui.QLabel(parent)
        self.labelCsvProfitability.setText('Profitability lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvProfitability, 10, 0)
        
        self.lineEditCsvProfitability = QtGui.QLineEdit(parent)
        self.lineEditCsvProfitability.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvProfitability, 10, 1)
        
        self.buttonSelectCsvProfitability = QtGui.QPushButton(parent)
        self.buttonSelectCsvProfitability.setText('Select &Profitability Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvProfitability, 11, 0, 1, 2)
        
        self.labelCsvPlanningUnit = QtGui.QLabel(parent)
        self.labelCsvPlanningUnit.setText('Planning unit lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvPlanningUnit, 12, 0)
        
        self.lineEditCsvPlanningUnit = QtGui.QLineEdit(parent)
        self.lineEditCsvPlanningUnit.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvPlanningUnit, 12, 1)
        
        self.buttonSelectCsvPlanningUnit = QtGui.QPushButton(parent)
        self.buttonSelectCsvPlanningUnit.setText('Select Planning Unit Lookup &Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvPlanningUnit, 13, 0, 1, 2)
        
        self.labelLocation = QtGui.QLabel(parent)
        self.labelLocation.setText('&Location:')
        layoutLumensDialog.addWidget(self.labelLocation, 14, 0)
        
        self.lineEditLocation = QtGui.QLineEdit(parent)
        self.lineEditLocation.setText('location')
        layoutLumensDialog.addWidget(self.lineEditLocation, 14, 1)
        
        self.labelLocation.setBuddy(self.lineEditLocation)
        
        self.labelSpinBoxT1 = QtGui.QLabel(parent)
        self.labelSpinBoxT1.setText('Year of T&1:')
        layoutLumensDialog.addWidget(self.labelSpinBoxT1, 15, 0)
        
        self.spinBoxT1 = QtGui.QSpinBox(parent)
        self.spinBoxT1.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxT1.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxT1, 15, 1)
        
        self.labelSpinBoxT1.setBuddy(self.spinBoxT1)
        
        self.labelSpinBoxT2 = QtGui.QLabel(parent)
        self.labelSpinBoxT2.setText('Year of T&2:')
        layoutLumensDialog.addWidget(self.labelSpinBoxT2, 16, 0)
        
        self.spinBoxT2 = QtGui.QSpinBox(parent)
        self.spinBoxT2.setRange(1, 9999)
        self.spinBoxT2.setValue(td.year)
        layoutLumensDialog.addWidget(self.spinBoxT2, 16, 1)
        
        self.labelSpinBoxT2.setBuddy(self.spinBoxT2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 17, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['landUseT1'] = unicode(self.lineEditLandUseT1.text())
        self.main.appSettings[type(self).__name__]['landUseT2'] = unicode(self.lineEditLandUseT2.text())
        self.main.appSettings[type(self).__name__]['planningUnit'] = unicode(self.lineEditPlanningUnit.text())
        self.main.appSettings[type(self).__name__]['csvCarbon'] = unicode(self.lineEditCsvCarbon.text())
        self.main.appSettings[type(self).__name__]['csvProfitability'] = unicode(self.lineEditCsvProfitability.text())
        self.main.appSettings[type(self).__name__]['csvPlanningUnit'] = unicode(self.lineEditCsvPlanningUnit.text())
        self.main.appSettings[type(self).__name__]['location'] = unicode(self.lineEditLocation.text())
        self.main.appSettings[type(self).__name__]['t1'] = self.spinBoxT1.value()
        self.main.appSettings[type(self).__name__]['t2'] = self.spinBoxT2.value()
    
    
    def handlerSelectWorkingDir(self):
        """Select a folder as working dir
        """
        workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if workingDir:
            self.lineEditWorkingDir.setText(workingDir)
            
            logging.getLogger(type(self).__name__).info('select working directory: %s', workingDir)
    
    
    def handlerSelectLandUseT1(self):
        """Select Land Use T1
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map T1', QtCore.QDir.homePath(), 'Land Use Map T1 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandUseT1.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseT2(self):
        """Select Land Use T2
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map T2', QtCore.QDir.homePath(), 'Land Use Map T2 (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandUseT2.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectPlanningUnit(self):
        """Select Planning Unit
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Map', QtCore.QDir.homePath(), 'Planning Unit Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditPlanningUnit.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectCsvCarbon(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Carbon Lookup Table', QtCore.QDir.homePath(), 'Carbon Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvCarbon.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerSelectCsvProfitability(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Profitability Lookup Table', QtCore.QDir.homePath(), 'Profitability Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvProfitability.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerSelectCsvPlanningUnit(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Planning Unit Lookup Table', QtCore.QDir.homePath(), 'Planning Unit Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvPlanningUnit.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:opcost_map',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['landUseT1'],
                self.main.appSettings[type(self).__name__]['landUseT2'],
                self.main.appSettings[type(self).__name__]['planningUnit'],
                self.main.appSettings[type(self).__name__]['csvCarbon'],
                self.main.appSettings[type(self).__name__]['csvProfitability'],
                self.main.appSettings[type(self).__name__]['csvPlanningUnit'],
                self.main.appSettings[type(self).__name__]['location'],
                self.main.appSettings[type(self).__name__]['t1'],
                self.main.appSettings[type(self).__name__]['t2'],
            )
            
            """
            print outputs
            """
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            