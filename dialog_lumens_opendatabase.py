#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensOpenDatabase(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensOpenDatabase, self).__init__(parent)
        
        self.setupUi(self)
        
        self.buttonLumensOpenDatabase.clicked.connect(self.handlerSelectLumensDatabase)
    
    
    def setupUi(self, parent):
        super(DialogLumensOpenDatabase, self).setupUi(self)
        
        layoutLumensDatabase = QtGui.QHBoxLayout()
        
        self.labelLumensDatabase = QtGui.QLabel(parent)
        self.labelLumensDatabase.setText('LUMENS database:')
        layoutLumensDatabase.addWidget(self.labelLumensDatabase)
        
        self.lineEditLumensDatabase = QtGui.QLineEdit(parent)
        self.lineEditLumensDatabase.setReadOnly(True)
        layoutLumensDatabase.addWidget(self.lineEditLumensDatabase)
        
        self.dialogLayout.addLayout(layoutLumensDatabase)
        
        self.buttonLumensOpenDatabase = QtGui.QPushButton(parent)
        self.buttonLumensOpenDatabase.setText('&Open LUMENS Database')
        self.dialogLayout.addWidget(self.buttonLumensOpenDatabase)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle('Dialog: LUMENS Open Database')
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectLumensDatabase(self):
        """Select a .lpj database file and open it
        """
        lumensDatabase = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select LUMENS Database', QtCore.QDir.homePath(), 'LUMENS Database (*{0})'.format(self.main.appSettings['selectProjectfileExt'])))
        
        if lumensDatabase:
            self.lineEditLumensDatabase.setText(lumensDatabase)
            
            logging.getLogger(type(self).__name__).info('select LUMENS database: %s', lumensDatabase)
            
            self.main.lumensOpenDatabase(lumensDatabase)
            
            self.close()