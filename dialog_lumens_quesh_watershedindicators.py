#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensQUESHWatershedIndicators(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensQUESHWatershedIndicators, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS QUES-H Watershed Indicators'
        
        self.setupUi(self)
        
        self.buttonSelectSWATTXTINOUTDir.clicked.connect(self.handlerSelectSWATTXTINOUTDir)
        self.buttonSelectSubWatershedPolygon.clicked.connect(self.handlerSelectSubWatershedPolygon)
        self.buttonSelectOutputInitialYearSubWatershedLevelIndicators.clicked.connect(self.handlerSelectOutputInitialYearSubWatershedLevelIndicators)
        self.buttonSelectOutputFinalYearSubWatershedLevelIndicators.clicked.connect(self.handlerSelectOutputFinalYearSubWatershedLevelIndicators)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensQUESHWatershedIndicators, self).showEvent(event)
        self.loadSelectedVectorLayer()
    
    
    def loadSelectedVectorLayer(self):
        """Load the selected layer
        """
        selectedIndexes = self.main.layerListView.selectedIndexes()
        
        if not selectedIndexes:
            return
        
        layerItemIndex = selectedIndexes[0]
        layerItem = self.main.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        
        if layerItemData['layerType'] == 'vector':
            self.lineEditSubWatershedPolygon.setText(layerItemData['layerFile'])
    
    
    def setupUi(self, parent):
        super(DialogLumensQUESHWatershedIndicators, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelSWATTXTINOUTDir = QtGui.QLabel(parent)
        self.labelSWATTXTINOUTDir.setText('SWAT TXTINOUT directory:')
        layoutLumensDialog.addWidget(self.labelSWATTXTINOUTDir, 0, 0)
        
        self.lineEditSWATTXTINOUTDir = QtGui.QLineEdit(parent)
        self.lineEditSWATTXTINOUTDir.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditSWATTXTINOUTDir, 0, 1)
        
        self.buttonSelectSWATTXTINOUTDir = QtGui.QPushButton(parent)
        self.buttonSelectSWATTXTINOUTDir.setText('Select &SWAT TXTINOUT Directory')
        layoutLumensDialog.addWidget(self.buttonSelectSWATTXTINOUTDir, 1, 0, 1, 2)
        
        self.labelDateInitial = QtGui.QLabel(parent)
        self.labelDateInitial.setText('Initial date:')
        layoutLumensDialog.addWidget(self.labelDateInitial, 2, 0)
        
        today = datetime.date.today()
        
        self.dateInitial = QtGui.QDateEdit(QtCore.QDate.currentDate(), parent)
        self.dateInitial.setCalendarPopup(True)
        self.dateInitial.setDisplayFormat('dd/MM/yyyy')
        layoutLumensDialog.addWidget(self.dateInitial, 2, 1)
        
        self.labelDateFinal = QtGui.QLabel(parent)
        self.labelDateFinal.setText('Final date:')
        layoutLumensDialog.addWidget(self.labelDateFinal, 3, 0)
        
        self.dateFinal = QtGui.QDateEdit(QtCore.QDate.currentDate(), parent)
        self.dateFinal.setCalendarPopup(True)
        self.dateFinal.setDisplayFormat('dd/MM/yyyy')
        layoutLumensDialog.addWidget(self.dateFinal, 3, 1)
        
        self.labelSubWatershedPolygon = QtGui.QLabel(parent)
        self.labelSubWatershedPolygon.setText('Sub watershed polygon:')
        layoutLumensDialog.addWidget(self.labelSubWatershedPolygon, 4, 0)
        
        self.lineEditSubWatershedPolygon = QtGui.QLineEdit(parent)
        self.lineEditSubWatershedPolygon.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditSubWatershedPolygon, 4, 1)
        
        self.buttonSelectSubWatershedPolygon = QtGui.QPushButton(parent)
        self.buttonSelectSubWatershedPolygon.setText('Select Sub Watershed &Polygon')
        layoutLumensDialog.addWidget(self.buttonSelectSubWatershedPolygon, 5, 0, 1, 2)
        
        self.labelLocation = QtGui.QLabel(parent)
        self.labelLocation.setText('&Location:')
        layoutLumensDialog.addWidget(self.labelLocation, 6, 0)
        
        self.lineEditLocation = QtGui.QLineEdit(parent)
        self.lineEditLocation.setText('location')
        layoutLumensDialog.addWidget(self.lineEditLocation, 6, 1)
        
        self.labelLocation.setBuddy(self.lineEditLocation)
        
        self.labelSubWatershedOutput = QtGui.QLabel(parent)
        self.labelSubWatershedOutput.setText('&Sub watershed output:')
        layoutLumensDialog.addWidget(self.labelSubWatershedOutput, 7, 0)
        
        self.spinBoxSubWatershedOutput = QtGui.QSpinBox(parent)
        self.spinBoxSubWatershedOutput.setRange(1, 99999)
        self.spinBoxSubWatershedOutput.setValue(10)
        layoutLumensDialog.addWidget(self.spinBoxSubWatershedOutput, 7, 1)
        
        self.labelSubWatershedOutput.setBuddy(self.spinBoxSubWatershedOutput)
        
        self.labelOutputInitialYearSubWatershedLevelIndicators = QtGui.QLabel(parent)
        self.labelOutputInitialYearSubWatershedLevelIndicators.setText('Initial year sub watershed level indicators (output):')
        layoutLumensDialog.addWidget(self.labelOutputInitialYearSubWatershedLevelIndicators, 8, 0)
        
        self.lineEditOutputInitialYearSubWatershedLevelIndicators = QtGui.QLineEdit(parent)
        self.lineEditOutputInitialYearSubWatershedLevelIndicators.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputInitialYearSubWatershedLevelIndicators, 8, 1)
        
        self.buttonSelectOutputInitialYearSubWatershedLevelIndicators = QtGui.QPushButton(parent)
        self.buttonSelectOutputInitialYearSubWatershedLevelIndicators.setText('Select Initial Year Sub Watershed Level Indicators')
        layoutLumensDialog.addWidget(self.buttonSelectOutputInitialYearSubWatershedLevelIndicators, 9, 0, 1, 2)
        
        self.labelOutputFinalYearSubWatershedLevelIndicators = QtGui.QLabel(parent)
        self.labelOutputFinalYearSubWatershedLevelIndicators.setText('Final year sub watershed level indicators (output):')
        layoutLumensDialog.addWidget(self.labelOutputFinalYearSubWatershedLevelIndicators, 10, 0)
        
        self.lineEditOutputFinalYearSubWatershedLevelIndicators = QtGui.QLineEdit(parent)
        self.lineEditOutputFinalYearSubWatershedLevelIndicators.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputFinalYearSubWatershedLevelIndicators, 10, 1)
        
        self.buttonSelectOutputFinalYearSubWatershedLevelIndicators = QtGui.QPushButton(parent)
        self.buttonSelectOutputFinalYearSubWatershedLevelIndicators.setText('Select Final Year Sub Watershed Level Indicators')
        layoutLumensDialog.addWidget(self.buttonSelectOutputFinalYearSubWatershedLevelIndicators, 11, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 12, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['SWATTXTINOUTDir'] = unicode(self.lineEditSWATTXTINOUTDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['dateInitial'] = self.dateInitial.date().toString('dd/MM/yyyy')
        self.main.appSettings[type(self).__name__]['dateFinal'] = self.dateFinal.date().toString('dd/MM/yyyy')
        self.main.appSettings[type(self).__name__]['subWatershedPolygon'] = unicode(self.lineEditSubWatershedPolygon.text())
        self.main.appSettings[type(self).__name__]['location'] = unicode(self.lineEditLocation.text())
        self.main.appSettings[type(self).__name__]['subWatershedOutput'] = self.spinBoxSubWatershedOutput.value()
        
        outputInitialYearSubWatershedLevelIndicators = unicode(self.lineEditOutputInitialYearSubWatershedLevelIndicators.text())
        outputFinalYearSubWatershedLevelIndicators = unicode(self.lineEditOutputFinalYearSubWatershedLevelIndicators.text())
        
        if not outputInitialYearSubWatershedLevelIndicators:
            outputInitialYearSubWatershedLevelIndicators = '__UNSET__'
        
        if not outputFinalYearSubWatershedLevelIndicators:
            outputFinalYearSubWatershedLevelIndicators = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputInitialYearSubWatershedLevelIndicators'] = outputInitialYearSubWatershedLevelIndicators
        self.main.appSettings[type(self).__name__]['outputFinalYearSubWatershedLevelIndicators'] = outputFinalYearSubWatershedLevelIndicators
    
    
    def handlerSelectSWATTXTINOUTDir(self):
        """Select a folder as SWAT TXTINOUT dir
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select SWAT TXTINOUT Directory'))
        
        if dir:
            self.lineEditSWATTXTINOUTDir.setText(dir)
            
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectSubWatershedPolygon(self):
        """Select observed debit file
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Sub Watershed Polygon', QtCore.QDir.homePath(), 'Sub Watershed Polygon (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if file:
            self.lineEditSubWatershedPolygon.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOutputInitialYearSubWatershedLevelIndicators(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Initial Year Sub Watershed Level Indicators Output', QtCore.QDir.homePath(), 'Initial Year Sub Watershed Level Indicators (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOutputInitialYearSubWatershedLevelIndicators.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOutputFinalYearSubWatershedLevelIndicators(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Final Year Sub Watershed Level Indicators Output', QtCore.QDir.homePath(), 'Final Year Sub Watershed Level Indicators (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOutputFinalYearSubWatershedLevelIndicators.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputInitialYearSubWatershedLevelIndicators = self.main.appSettings[type(self).__name__]['outputInitialYearSubWatershedLevelIndicators']
            outputFinalYearSubWatershedLevelIndicators = self.main.appSettings[type(self).__name__]['outputFinalYearSubWatershedLevelIndicators']
            
            if outputInitialYearSubWatershedLevelIndicators == '__UNSET__':
                outputInitialYearSubWatershedLevelIndicators = None
            
            if outputFinalYearSubWatershedLevelIndicators == '__UNSET__':
                outputFinalYearSubWatershedLevelIndicators = None
            
            outputs = general.runalg(
                'modeler:ques-h_watershed_indicators',
                self.main.appSettings[type(self).__name__]['SWATTXTINOUTDir'],
                self.main.appSettings[type(self).__name__]['dateInitial'],
                self.main.appSettings[type(self).__name__]['dateFinal'],
                self.main.appSettings[type(self).__name__]['subWatershedPolygon'],
                self.main.appSettings[type(self).__name__]['location'],
                self.main.appSettings[type(self).__name__]['subWatershedOutput'],
                outputInitialYearSubWatershedLevelIndicators,
                outputFinalYearSubWatershedLevelIndicators,
            )
            
            """
            print outputs
            """
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            