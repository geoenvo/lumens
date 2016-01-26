#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensQUESHWatershedModelEvaluation(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensQUESHWatershedModelEvaluation, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS QUES-H Watershed Model Evaluation'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectObservedDebitFile.clicked.connect(self.handlerSelectObservedDebitFile)
        self.buttonSelectOutputWatershedModelEvaluation.clicked.connect(self.handlerSelectOutputWatershedModelEvaluation)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensQUESHWatershedModelEvaluation, self).setupUi(self)
        
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
        
        self.labelDateInitial = QtGui.QLabel(parent)
        self.labelDateInitial.setText('Initial date:')
        layoutLumensDialog.addWidget(self.labelDateInitial, 2, 0)
        
        self.dateDateInitial = QtGui.QDateEdit(QtCore.QDate.currentDate(), parent)
        self.dateDateInitial.setCalendarPopup(True)
        self.dateDateInitial.setDisplayFormat('dd/MM/yyyy')
        layoutLumensDialog.addWidget(self.dateDateInitial, 2, 1)
        
        self.labelDateFinal = QtGui.QLabel(parent)
        self.labelDateFinal.setText('Final date:')
        layoutLumensDialog.addWidget(self.labelDateFinal, 3, 0)
        
        self.dateDateFinal = QtGui.QDateEdit(QtCore.QDate.currentDate(), parent)
        self.dateDateFinal.setCalendarPopup(True)
        self.dateDateFinal.setDisplayFormat('dd/MM/yyyy')
        layoutLumensDialog.addWidget(self.dateDateFinal, 3, 1)
        
        self.labelSWATModel = QtGui.QLabel(parent)
        self.labelSWATModel.setText('SWAT &model:')
        layoutLumensDialog.addWidget(self.labelSWATModel, 4, 0)
        
        SWATModel = {
            1: 'Skip',
            2: 'Run',
        }
        
        self.comboBoxSWATModel = QtGui.QComboBox()
        
        for key, val in SWATModel.iteritems():
            self.comboBoxSWATModel.addItem(val, key)
        
        layoutLumensDialog.addWidget(self.comboBoxSWATModel, 4, 1)
        
        self.labelSWATModel.setBuddy(self.comboBoxSWATModel)
        
        self.labelLocation = QtGui.QLabel(parent)
        self.labelLocation.setText('&Location:')
        layoutLumensDialog.addWidget(self.labelLocation, 5, 0)
        
        self.lineEditLocation = QtGui.QLineEdit(parent)
        self.lineEditLocation.setText('location')
        layoutLumensDialog.addWidget(self.lineEditLocation, 5, 1)
        
        self.labelLocation.setBuddy(self.lineEditLocation)
        
        self.labelOutletReachSubBasinID = QtGui.QLabel(parent)
        self.labelOutletReachSubBasinID.setText('Outlet reach/sub-basin ID:')
        layoutLumensDialog.addWidget(self.labelOutletReachSubBasinID, 6, 0)
        
        self.spinBoxOutletReachSubBasinID = QtGui.QSpinBox(parent)
        self.spinBoxOutletReachSubBasinID.setRange(1, 99999)
        self.spinBoxOutletReachSubBasinID.setValue(10)
        layoutLumensDialog.addWidget(self.spinBoxOutletReachSubBasinID, 6, 1)
        
        self.labelOutletReachSubBasinID.setBuddy(self.spinBoxOutletReachSubBasinID)
        
        self.labelObservedDebitFile = QtGui.QLabel(parent)
        self.labelObservedDebitFile.setText('Observed debit file:')
        layoutLumensDialog.addWidget(self.labelObservedDebitFile, 7, 0)
        
        self.lineEditObservedDebitFile = QtGui.QLineEdit(parent)
        self.lineEditObservedDebitFile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditObservedDebitFile, 7, 1)
        
        self.buttonSelectObservedDebitFile = QtGui.QPushButton(parent)
        self.buttonSelectObservedDebitFile.setText('Select Observed &Debit File')
        layoutLumensDialog.addWidget(self.buttonSelectObservedDebitFile, 8, 0, 1, 2)
        
        self.labelOutputWatershedModelEvaluation = QtGui.QLabel(parent)
        self.labelOutputWatershedModelEvaluation.setText('Watershed model evaluation (output):')
        layoutLumensDialog.addWidget(self.labelOutputWatershedModelEvaluation, 9, 0)
        
        self.lineEditOutputWatershedModelEvaluation = QtGui.QLineEdit(parent)
        self.lineEditOutputWatershedModelEvaluation.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputWatershedModelEvaluation, 9, 1)
        
        self.buttonSelectOutputWatershedModelEvaluation = QtGui.QPushButton(parent)
        self.buttonSelectOutputWatershedModelEvaluation.setText('Select Watershed Model Evaluation')
        layoutLumensDialog.addWidget(self.buttonSelectOutputWatershedModelEvaluation, 10, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 11, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['dateInitial'] = self.dateDateInitial.date().toString('dd/MM/yyyy')
        self.main.appSettings[type(self).__name__]['dateFinal'] = self.dateDateFinal.date().toString('dd/MM/yyyy')
        self.main.appSettings[type(self).__name__]['SWATModel'] = self.comboBoxSWATModel.itemData(self.comboBoxSWATModel.currentIndex())
        self.main.appSettings[type(self).__name__]['location'] = unicode(self.lineEditLocation.text())
        self.main.appSettings[type(self).__name__]['outletReachSubBasinID'] = self.spinBoxOutletReachSubBasinID.value()
        self.main.appSettings[type(self).__name__]['observedDebitFile'] = unicode(self.lineEditObservedDebitFile.text())
        
        outputWatershedModelEvaluation = unicode(self.lineEditOutputWatershedModelEvaluation.text())
        
        if not outputWatershedModelEvaluation:
            outputWatershedModelEvaluation = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputWatershedModelEvaluation'] = outputWatershedModelEvaluation
    
    
    def handlerSelectWorkingDir(self):
        """Select a folder as working dir
        """
        workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if workingDir:
            self.lineEditWorkingDir.setText(workingDir)
            
            logging.getLogger(type(self).__name__).info('select working directory: %s', workingDir)
    
    
    def handlerSelectObservedDebitFile(self):
        """Select observed debit file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Observed Debit File', QtCore.QDir.homePath(), 'Observed Debit File (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if file:
            self.lineEditObservedDebitFile.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOutputWatershedModelEvaluation(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Watershed Model Evaluation Output', QtCore.QDir.homePath(), 'Watershed Model Evaluation (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOutputWatershedModelEvaluation.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputWatershedModelEvaluation = self.main.appSettings[type(self).__name__]['outputWatershedModelEvaluation']
            
            if outputWatershedModelEvaluation == '__UNSET__':
                outputWatershedModelEvaluation = None
            
            outputs = general.runalg(
                'modeler:ques-h_watershed_model_evaluation',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['period1'],
                self.main.appSettings[type(self).__name__]['period2'],
                self.main.appSettings[type(self).__name__]['SWATModel'],
                self.main.appSettings[type(self).__name__]['location'],
                self.main.appSettings[type(self).__name__]['outletReachSubBasinID'],
                self.main.appSettings[type(self).__name__]['observedDebitFile'],
                outputWatershedModelEvaluation,
            )
            
            """
            print outputs
            """
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            