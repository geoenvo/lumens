#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensCombinedPreQUES(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensCombinedPreQUES, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS Combined PreQUES'
        
        self.setupUi(self)
        
        self.buttonSelectCsvfile.clicked.connect(self.handlerSelectCsvfile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensCombinedPreQUES, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelCsvfile = QtGui.QLabel(parent)
        self.labelCsvfile.setText('Land cover lookup table:')
        layoutLumensDialog.addWidget(self.labelCsvfile, 0, 0)
        
        self.lineEditCsvfile = QtGui.QLineEdit(parent)
        self.lineEditCsvfile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditCsvfile, 0, 1)
        
        self.buttonSelectCsvfile = QtGui.QPushButton(parent)
        self.buttonSelectCsvfile.setText('Select &Lookup Table')
        layoutLumensDialog.addWidget(self.buttonSelectCsvfile, 1, 0, 1, 2)
        
        self.labelOption = QtGui.QLabel(parent)
        self.labelOption.setText('Analysis &option:')
        layoutLumensDialog.addWidget(self.labelOption, 2, 0)
        
        self.comboBoxOption = QtGui.QComboBox(parent)
        comboBoxItems = [
            'All analysis',
            'Perubahan dominan di tiap zona',
            'Dinamika perubahan di tiap zona (Alpha-Beta)',
            'Analisis Alur Perubahan (Pre-QUES)',
        ]
        self.comboBoxOption.addItems(comboBoxItems)
        layoutLumensDialog.addWidget(self.comboBoxOption, 2, 1)
        
        self.labelOption.setBuddy(self.comboBoxOption)
        
        self.labelSpinBox = QtGui.QLabel(parent)
        self.labelSpinBox.setText('Land cover &no data value:')
        layoutLumensDialog.addWidget(self.labelSpinBox, 3, 0)
        
        self.spinBox = QtGui.QSpinBox(parent)
        self.spinBox.setRange(-9999, 9999)
        self.spinBox.setValue(0)
        layoutLumensDialog.addWidget(self.spinBox, 3, 1)
        
        self.labelSpinBox.setBuddy(self.spinBox)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 4, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectCsvfile(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Lookup Table', QtCore.QDir.homePath(), 'Land Cover Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditCsvfile.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['csvfile'] = unicode(self.lineEditCsvfile.text())
        self.main.appSettings[type(self).__name__]['option'] = unicode(self.comboBoxOption.currentText())
        self.main.appSettings[type(self).__name__]['nodata'] = self.spinBox.value()
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'r:lumenscombinedpreques',
                self.main.appSettings[type(self).__name__]['csvfile'],
                self.main.appSettings[type(self).__name__]['option'],
                self.main.appSettings[type(self).__name__]['nodata'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            