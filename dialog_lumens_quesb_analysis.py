#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensQUESBAnalysis(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensQUESBAnalysis, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS QUES-B Analysis'
        
        self.setupUi(self)
        
        self.buttonSelectCsvLandCover.clicked.connect(self.handlerSelectCsvLandCover)
        self.buttonSelectCsvClassDescriptors.clicked.connect(self.handlerSelectCsvClassDescriptors)
        self.buttonSelectCsvEdgeContrast.clicked.connect(self.handlerSelectCsvEdgeContrast)
        self.buttonSelectCsvZoneLookup.clicked.connect(self.handlerSelectCsvZoneLookup)
        self.buttonSelectOutputTECIInitial.clicked.connect(self.handlerSelectOutputTECIInitial)
        self.buttonSelectOutputTECIFinal.clicked.connect(self.handlerSelectOutputTECIFinal)
        self.buttonSelectOutputHabitatLoss.clicked.connect(self.handlerSelectOutputHabitatLoss)
        self.buttonSelectOutputDegradedHabitat.clicked.connect(self.handlerSelectOutputDegradedHabitat)
        self.buttonSelectOutputHabitatGain.clicked.connect(self.handlerSelectOutputHabitatGain)
        self.buttonSelectOutputRecoveredHabitat.clicked.connect(self.handlerSelectOutputRecoveredHabitat)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensQUESBAnalysis, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelCsvLandCover = QtGui.QLabel(parent)
        self.labelCsvLandCover.setText('Land cover lookup:')
        layoutLumensDialog.addWidget(self.labelCsvLandCover, 0, 0)
        
        self.lineEditCsvLandCover = QtGui.QLineEdit(parent)
        self.lineEditCsvLandCover.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvLandCover, 0, 1)
        
        self.buttonSelectCsvLandCover = QtGui.QPushButton(parent)
        self.buttonSelectCsvLandCover.setText('Select &Land Cover Lookup')
        layoutLumensDialog.addWidget(self.buttonSelectCsvLandCover, 1, 0, 1, 2)
        
        self.labelSpinBoxSamplingGridRes = QtGui.QLabel(parent)
        self.labelSpinBoxSamplingGridRes.setText('Sampling grid &resolution:')
        layoutLumensDialog.addWidget(self.labelSpinBoxSamplingGridRes, 2, 0)
        
        self.spinBoxSamplingGridRes = QtGui.QSpinBox(parent)
        self.spinBoxSamplingGridRes.setRange(1, 9999)
        self.spinBoxSamplingGridRes.setValue(10000)
        layoutLumensDialog.addWidget(self.spinBoxSamplingGridRes, 2, 1)
        
        self.labelSpinBoxSamplingGridRes.setBuddy(self.spinBoxSamplingGridRes)
        
        self.labelSpinBoxSamplingWindowSize = QtGui.QLabel(parent)
        self.labelSpinBoxSamplingWindowSize.setText('Sampling &window size:')
        layoutLumensDialog.addWidget(self.labelSpinBoxSamplingWindowSize, 3, 0)
        
        self.spinBoxSamplingWindowSize = QtGui.QSpinBox(parent)
        self.spinBoxSamplingWindowSize.setRange(1, 9999)
        self.spinBoxSamplingWindowSize.setValue(1000)
        layoutLumensDialog.addWidget(self.spinBoxSamplingWindowSize, 3, 1)
        
        self.labelSpinBoxSamplingWindowSize.setBuddy(self.spinBoxSamplingWindowSize)
        
        self.labelSpinBoxWindowShape = QtGui.QLabel(parent)
        self.labelSpinBoxWindowShape.setText('Window &shape:')
        layoutLumensDialog.addWidget(self.labelSpinBoxWindowShape, 4, 0)
        
        self.spinBoxWindowShape = QtGui.QSpinBox(parent)
        self.spinBoxWindowShape.setRange(1, 9999)
        self.spinBoxWindowShape.setValue(1)
        layoutLumensDialog.addWidget(self.spinBoxWindowShape, 4, 1)
        
        self.labelSpinBoxWindowShape.setBuddy(self.spinBoxWindowShape)
        
        self.labelSpinBoxNodata = QtGui.QLabel(parent)
        self.labelSpinBoxNodata.setText('&No data value:')
        layoutLumensDialog.addWidget(self.labelSpinBoxNodata, 5, 0)
        
        self.spinBoxNodata = QtGui.QSpinBox(parent)
        self.spinBoxNodata.setRange(-9999, 9999)
        self.spinBoxNodata.setValue(0)
        layoutLumensDialog.addWidget(self.spinBoxNodata, 5, 1)
        
        self.labelSpinBoxNodata.setBuddy(self.spinBoxNodata)
        
        self.labelCsvClassDescriptors = QtGui.QLabel(parent)
        self.labelCsvClassDescriptors.setText('Class descriptors:')
        layoutLumensDialog.addWidget(self.labelCsvClassDescriptors, 6, 0)
        
        self.lineEditCsvClassDescriptors = QtGui.QLineEdit(parent)
        self.lineEditCsvClassDescriptors.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvClassDescriptors, 6, 1)
        
        self.buttonSelectCsvClassDescriptors = QtGui.QPushButton(parent)
        self.buttonSelectCsvClassDescriptors.setText('Select &Class Descriptors')
        layoutLumensDialog.addWidget(self.buttonSelectCsvClassDescriptors, 7, 0, 1, 2)
        
        self.labelCsvEdgeContrast = QtGui.QLabel(parent)
        self.labelCsvEdgeContrast.setText('Edge contrast:')
        layoutLumensDialog.addWidget(self.labelCsvEdgeContrast, 8, 0)
        
        self.lineEditCsvEdgeContrast = QtGui.QLineEdit(parent)
        self.lineEditCsvEdgeContrast.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvEdgeContrast, 8, 1)
        
        self.buttonSelectCsvEdgeContrast = QtGui.QPushButton(parent)
        self.buttonSelectCsvEdgeContrast.setText('Select &Edge Contrast')
        layoutLumensDialog.addWidget(self.buttonSelectCsvEdgeContrast, 9, 0, 1, 2)
        
        self.labelCsvZoneLookup = QtGui.QLabel(parent)
        self.labelCsvZoneLookup.setText('Zone lookup:')
        layoutLumensDialog.addWidget(self.labelCsvZoneLookup, 10, 0)
        
        self.lineEditCsvZoneLookup = QtGui.QLineEdit(parent)
        self.lineEditCsvZoneLookup.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvZoneLookup, 10, 1)
        
        self.buttonSelectCsvZoneLookup = QtGui.QPushButton(parent)
        self.buttonSelectCsvZoneLookup.setText('Select &Zone Lookup')
        layoutLumensDialog.addWidget(self.buttonSelectCsvZoneLookup, 11, 0, 1, 2)
        
        self.labelSpinBoxRefMapID = QtGui.QLabel(parent)
        self.labelSpinBoxRefMapID.setText('&Reference map ID:')
        layoutLumensDialog.addWidget(self.labelSpinBoxRefMapID, 12, 0)
        
        self.spinBoxRefMapID = QtGui.QSpinBox(parent)
        self.spinBoxRefMapID.setRange(-9999, 9999)
        self.spinBoxRefMapID.setValue(1)
        layoutLumensDialog.addWidget(self.spinBoxRefMapID, 12, 1)
        
        self.labelSpinBoxRefMapID.setBuddy(self.spinBoxRefMapID)
        
        self.labelOutputTECIInitial = QtGui.QLabel(parent)
        self.labelOutputTECIInitial.setText('TECI initial (output):')
        layoutLumensDialog.addWidget(self.labelOutputTECIInitial, 13, 0)
        
        self.lineEditOutputTECIInitial = QtGui.QLineEdit(parent)
        self.lineEditOutputTECIInitial.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputTECIInitial, 13, 1)
        
        self.buttonSelectOutputTECIInitial = QtGui.QPushButton(parent)
        self.buttonSelectOutputTECIInitial.setText('Select TECI &Initial Output')
        layoutLumensDialog.addWidget(self.buttonSelectOutputTECIInitial, 14, 0, 1, 2)
        
        self.labelOutputTECIFinal = QtGui.QLabel(parent)
        self.labelOutputTECIFinal.setText('TECI final (output):')
        layoutLumensDialog.addWidget(self.labelOutputTECIFinal, 15, 0)
        
        self.lineEditOutputTECIFinal = QtGui.QLineEdit(parent)
        self.lineEditOutputTECIFinal.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputTECIFinal, 15, 1)
        
        self.buttonSelectOutputTECIFinal = QtGui.QPushButton(parent)
        self.buttonSelectOutputTECIFinal.setText('Select TECI &Final Output')
        layoutLumensDialog.addWidget(self.buttonSelectOutputTECIFinal, 16, 0, 1, 2)
        
        self.labelOutputHabitatLoss = QtGui.QLabel(parent)
        self.labelOutputHabitatLoss.setText('Habitat Loss (output):')
        layoutLumensDialog.addWidget(self.labelOutputHabitatLoss, 17, 0)
        
        self.lineEditOutputHabitatLoss = QtGui.QLineEdit(parent)
        self.lineEditOutputHabitatLoss.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputHabitatLoss, 17, 1)
        
        self.buttonSelectOutputHabitatLoss = QtGui.QPushButton(parent)
        self.buttonSelectOutputHabitatLoss.setText('Select Habitat &Loss Output')
        layoutLumensDialog.addWidget(self.buttonSelectOutputHabitatLoss, 18, 0, 1, 2)
        
        self.labelOutputDegradedHabitat = QtGui.QLabel(parent)
        self.labelOutputDegradedHabitat.setText('Degraded habitat (output):')
        layoutLumensDialog.addWidget(self.labelOutputDegradedHabitat, 19, 0)
        
        self.lineEditOutputDegradedHabitat = QtGui.QLineEdit(parent)
        self.lineEditOutputDegradedHabitat.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputDegradedHabitat, 19, 1)
        
        self.buttonSelectOutputDegradedHabitat = QtGui.QPushButton(parent)
        self.buttonSelectOutputDegradedHabitat.setText('Select &Degraded Habitat Output')
        layoutLumensDialog.addWidget(self.buttonSelectOutputDegradedHabitat, 20, 0, 1, 2)
        
        self.labelOutputHabitatGain = QtGui.QLabel(parent)
        self.labelOutputHabitatGain.setText('Habitat gain (output):')
        layoutLumensDialog.addWidget(self.labelOutputHabitatGain, 21, 0)
        
        self.lineEditOutputHabitatGain = QtGui.QLineEdit(parent)
        self.lineEditOutputHabitatGain.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputHabitatGain, 21, 1)
        
        self.buttonSelectOutputHabitatGain = QtGui.QPushButton(parent)
        self.buttonSelectOutputHabitatGain.setText('Select Habitat &Gain Output')
        layoutLumensDialog.addWidget(self.buttonSelectOutputHabitatGain, 22, 0, 1, 2)
        
        self.labelOutputRecoveredHabitat = QtGui.QLabel(parent)
        self.labelOutputRecoveredHabitat.setText('Recovered habitat (output):')
        layoutLumensDialog.addWidget(self.labelOutputRecoveredHabitat, 23, 0)
        
        self.lineEditOutputRecoveredHabitat = QtGui.QLineEdit(parent)
        self.lineEditOutputRecoveredHabitat.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditOutputRecoveredHabitat, 23, 1)
        
        self.buttonSelectOutputRecoveredHabitat = QtGui.QPushButton(parent)
        self.buttonSelectOutputRecoveredHabitat.setText('Select &Recovered Habitat Output')
        layoutLumensDialog.addWidget(self.buttonSelectOutputRecoveredHabitat, 24, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 25, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectCsvLandCover(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Lookup', QtCore.QDir.homePath(), 'Land Cover Lookup (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvLandCover.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerSelectCsvClassDescriptors(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Class Descriptors', QtCore.QDir.homePath(), 'Class Descriptors (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvClassDescriptors.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerSelectCsvEdgeContrast(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Edge Contrast', QtCore.QDir.homePath(), 'Edge Contrast (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvEdgeContrast.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerSelectCsvZoneLookup(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Zone Lookup', QtCore.QDir.homePath(), 'Zone Lookup (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvZoneLookup.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def handlerSelectOutputTECIInitial(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select TECI Initial Output', QtCore.QDir.homePath(), 'TECI Initial (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditOutputTECIInitial.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOutputTECIFinal(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select TECI Final Output', QtCore.QDir.homePath(), 'TECI Final (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditOutputTECIFinal.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOutputHabitatLoss(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Habitat Loss Output', QtCore.QDir.homePath(), 'Habitat Loss (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditOutputHabitatLoss.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOutputDegradedHabitat(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Degraded Habitat', QtCore.QDir.homePath(), 'Degraded Habitat (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditOutputDegradedHabitat.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOutputHabitatGain(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Habitat Gain', QtCore.QDir.homePath(), 'Habitat Gain (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditOutputHabitatGain.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOutputRecoveredHabitat(self):
        """Select a output file
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Recovered Habitat Output', QtCore.QDir.homePath(), 'Recovered Habitat (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if outputfile:
            self.lineEditOutputRecoveredHabitat.setText(outputfile)
            
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['csvLandCover'] = unicode(self.lineEditCsvLandCover.text())
        self.main.appSettings[type(self).__name__]['samplingGridRes'] = self.spinBoxSamplingGridRes.value()
        self.main.appSettings[type(self).__name__]['samplingWindowSize'] = self.spinBoxSamplingWindowSize.value()
        self.main.appSettings[type(self).__name__]['windowShape'] = self.spinBoxWindowShape.value()
        self.main.appSettings[type(self).__name__]['nodata'] = self.spinBoxNodata.value()
        self.main.appSettings[type(self).__name__]['csvClassDescriptors'] = unicode(self.lineEditCsvClassDescriptors.text())
        self.main.appSettings[type(self).__name__]['csvEdgeContrast'] = unicode(self.lineEditCsvEdgeContrast.text())
        self.main.appSettings[type(self).__name__]['csvZoneLookup'] = unicode(self.lineEditCsvZoneLookup.text())
        self.main.appSettings[type(self).__name__]['refMapID'] = self.spinBoxRefMapID.value()
        
        outputTECIInitial = unicode(self.lineEditOutputTECIInitial.text())
        outputTECIFinal = unicode(self.lineEditOutputTECIFinal.text())
        outputHabitatLoss = unicode(self.lineEditOutputHabitatLoss.text())
        outputDegradedHabitat = unicode(self.lineEditOutputDegradedHabitat.text())
        outputHabitatGain = unicode(self.lineEditOutputHabitatGain.text())
        outputRecoveredHabitat = unicode(self.lineEditOutputRecoveredHabitat.text())
        
        if not outputTECIInitial:
            outputTECIInitial = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputTECIInitial'] = outputTECIInitial
        
        if not outputTECIFinal:
            outputTECIFinal = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputTECIFinal'] = outputTECIFinal
        
        if not outputHabitatLoss:
            outputHabitatLoss = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputHabitatLoss'] = outputHabitatLoss
        
        if not outputDegradedHabitat:
            outputDegradedHabitat = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputDegradedHabitat'] = outputDegradedHabitat
        
        if not outputHabitatGain:
            outputHabitatGain = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputHabitatGain'] = outputHabitatGain
        
        if not outputRecoveredHabitat:
            outputRecoveredHabitat = '__UNSET__'
        
        self.main.appSettings[type(self).__name__]['outputRecoveredHabitat'] = outputRecoveredHabitat
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputTECIInitial = self.main.appSettings[type(self).__name__]['outputTECIInitial']
            outputTECIFinal = self.main.appSettings[type(self).__name__]['outputTECIFinal']
            outputHabitatLoss = self.main.appSettings[type(self).__name__]['outputHabitatLoss']
            outputDegradedHabitat = self.main.appSettings[type(self).__name__]['outputDegradedHabitat']
            outputHabitatGain = self.main.appSettings[type(self).__name__]['outputHabitatGain']
            outputRecoveredHabitat = self.main.appSettings[type(self).__name__]['outputRecoveredHabitat']
            
            if outputTECIInitial == '__UNSET__':
                outputTECIInitial = None
            
            if outputTECIFinal == '__UNSET__':
                outputTECIFinal = None
            
            if outputHabitatLoss == '__UNSET__':
                outputHabitatLoss = None
            
            if outputDegradedHabitat == '__UNSET__':
                outputDegradedHabitat = None
            
            if outputHabitatGain == '__UNSET__':
                outputHabitatGain = None
            
            if outputRecoveredHabitat == '__UNSET__':
                outputRecoveredHabitat = None
            
            outputs = general.runalg(
                'modeler:ques-b',
                self.main.appSettings[type(self).__name__]['csvLandCover'],
                self.main.appSettings[type(self).__name__]['samplingGridRes'],
                self.main.appSettings[type(self).__name__]['samplingWindowSize'],
                self.main.appSettings[type(self).__name__]['windowShape'],
                self.main.appSettings[type(self).__name__]['nodata'],
                self.main.appSettings[type(self).__name__]['csvClassDescriptors'],
                self.main.appSettings[type(self).__name__]['csvEdgeContrast'],
                self.main.appSettings[type(self).__name__]['csvZoneLookup'],
                self.main.appSettings[type(self).__name__]['refMapID'],
                outputTECIInitial,
                outputTECIFinal,
                outputHabitatLoss,
                outputDegradedHabitat,
                outputHabitatGain,
                outputRecoveredHabitat,
            )
            
            """
            print outputs
            
            if not outputTECIInitial:
                self.main.appSettings[type(self).__name__]['outputTECIInitial'] = outputs['????']
            
            if not outputTECIFinal:
                self.main.appSettings[type(self).__name__]['outputTECIFinal'] = outputs['????']
            
            if not outputHabitatLoss:
                self.main.appSettings[type(self).__name__]['outputHabitatLoss'] = outputs['????']
            
            if not outputDegradedHabitat:
                self.main.appSettings[type(self).__name__]['outputDegradedHabitat'] = outputs['????']
            
            if not outputHabitatGain:
                self.main.appSettings[type(self).__name__]['outputHabitatGain'] = outputs['????']
            
            if not outputRecoveredHabitat:
                self.main.appSettings[type(self).__name__]['outputRecoveredHabitat'] = outputs['????']
            """
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            