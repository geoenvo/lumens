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
        
        self.dialogTitle = 'LUMENS Import Database'
        
        self.setupUi(self)
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectLumensDatabase.clicked.connect(self.handlerSelectLumensDatabase)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensImportDatabase, self).setupUi(self)
        
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
        
        self.labelLumensDatabase = QtGui.QLabel(parent)
        self.labelLumensDatabase.setText('LUMENS database:')
        layoutLumensDialog.addWidget(self.labelLumensDatabase, 2, 0)
        
        self.lineEditLumensDatabase = QtGui.QLineEdit(parent)
        self.lineEditLumensDatabase.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditLumensDatabase, 2, 1)
        
        self.buttonSelectLumensDatabase = QtGui.QPushButton(parent)
        self.buttonSelectLumensDatabase.setText('&Select LUMENS Database')
        layoutLumensDialog.addWidget(self.buttonSelectLumensDatabase, 3, 0, 1, 2)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 4, 0, 1, 2)
        
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
    
    
    def handlerSelectLumensDatabase(self):
        """Select a .lpj database file
        """
        projectFile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select LUMENS Database', QtCore.QDir.homePath(), 'LUMENS Database (*{0})'.format(self.main.appSettings['selectProjectfileExt'])))
        
        if projectFile:
            self.lineEditLumensDatabase.setText(projectFile)
            
            logging.getLogger(type(self).__name__).info('select LUMENS database: %s', projectFile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        # BUG? workingDir path separator must be forward slash
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['projectFile'] = unicode(self.lineEditLumensDatabase.text())
    
    
    def handlerLumensDialogSubmit(self):
        """LUMENS Import Database
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:lumens_import_database',
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['projectFile'],
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
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
            