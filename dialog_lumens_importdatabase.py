#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase



class DialogLumensImportDatabase(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensImportDatabase, self).__init__(parent)
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectLumensDatabase.clicked.connect(self.handlerSelectLumensDatabase)
        self.buttonLumensImportDatabase.clicked.connect(self.handlerLumensImportDatabase)
    
    
    def setupUi(self, parent):
        super(DialogLumensImportDatabase, self).setupUi(self)
        
        layoutLumensImportDatabase = QtGui.QGridLayout()
        
        self.labelWorkingDir = QtGui.QLabel(parent)
        self.labelWorkingDir.setText('Working directory:')
        layoutLumensImportDatabase.addWidget(self.labelWorkingDir, 0, 0)
        
        self.lineEditWorkingDir = QtGui.QLineEdit(parent)
        self.lineEditWorkingDir.setReadOnly(True)
        layoutLumensImportDatabase.addWidget(self.lineEditWorkingDir, 0, 1)
        
        self.buttonSelectWorkingDir = QtGui.QPushButton(parent)
        self.buttonSelectWorkingDir.setText('Select &Working Directory')
        layoutLumensImportDatabase.addWidget(self.buttonSelectWorkingDir, 1, 0, 1, 2)
        
        self.labelLumensDatabase = QtGui.QLabel(parent)
        self.labelLumensDatabase.setText('LUMENS database:')
        layoutLumensImportDatabase.addWidget(self.labelLumensDatabase, 2, 0)
        
        self.lineEditLumensDatabase = QtGui.QLineEdit(parent)
        self.lineEditLumensDatabase.setReadOnly(True)
        layoutLumensImportDatabase.addWidget(self.lineEditLumensDatabase, 2, 1)
        
        self.buttonSelectLumensDatabase = QtGui.QPushButton(parent)
        self.buttonSelectLumensDatabase.setText('&Select LUMENS Database')
        layoutLumensImportDatabase.addWidget(self.buttonSelectLumensDatabase, 3, 0, 1, 2)
        
        self.buttonLumensImportDatabase = QtGui.QPushButton(parent)
        self.buttonLumensImportDatabase.setText('&Import LUMENS Database')
        layoutLumensImportDatabase.addWidget(self.buttonLumensImportDatabase, 4, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensImportDatabase)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle('Dialog: LUMENS Import Database')
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectWorkingDir(self):
        """Select a folder as working dir
        """
        workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if workingDir:
            self.lineEditWorkingDir.setText(workingDir)
            
            logging.getLogger(type(self).__name__).info('select working directory: %s', workingDir)
    
    
    def handlerSelectLumensDatabase(self):
        """Select a .lpj database file
        """
        projectFile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select LUMENS Database', QtCore.QDir.homePath(), 'LUMENS Database (*{0})'.format(self.main.appSettings['selectProjectFileExt'])))
        
        if projectFile:
            self.lineEditLumensDatabase.setText(projectFile)
            
            logging.getLogger(type(self).__name__).info('select LUMENS database: %s', projectFile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        # BUG? workingDir path separator must be forward slash
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['projectFile'] = unicode(self.lineEditLumensDatabase.text())
    
    
    def handlerLumensImportDatabase(self):
        """LUMENS Import Database
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: LUMENS Import Database')
            
            self.buttonLumensImportDatabase.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:lumens_import_database',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['projectFile'],
            )
            
            self.buttonLumensImportDatabase.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: LUMENS Import Database')
            
            projectName = os.path.basename(os.path.splitext(self.main.appSettings[type(self).__name__]['projectFile'])[0])
            
            lumensDatabase = os.path.join(
                self.main.appSettings[type(self).__name__]['workingDir'],
                projectName,
                os.path.basename(self.main.appSettings[type(self).__name__]['projectFile'])
            )
            
            # if LUMENS database file exists, open it and close dialog
            if os.path.exists(lumensDatabase):
                self.main.lumensOpenDatabase(lumensDatabase)
                self.close()
            else:
                logging.getLogger(type(self).__name__).error('modeler:lumens_import_database failed...')
            