#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_viewer import DialogLumensViewer


class DialogLumensAddData(QtGui.QDialog):
    """
    """
    def __init__(self, parent):
        super(DialogLumensAddData, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS Add Data'
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensAddData init'
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        # 'Add Data' checkboxes
        self.checkBoxAddLandUseCoverData.toggled.connect(self.toggleAddLandUseCoverData)
        self.checkBoxAddPeatData.toggled.connect(self.toggleAddPeatData)
        self.checkBoxAddFactorData.toggled.connect(self.toggleAddFactorData)
        self.checkBoxAddPlanningUnitData.toggled.connect(self.toggleAddPlanningUnitData)
        
        # 'Add Data' buttons
        self.buttonSelectAddLandUseCoverDataRasterfile.clicked.connect(self.handlerSelectAddLandUseCoverDataRasterfile)
        self.buttonSelectAddPeatDataRasterfile.clicked.connect(self.handlerSelectAddPeatDataRasterfile)
        self.buttonSelectAddFactorDataRasterfile.clicked.connect(self.handlerSelectAddFactorDataRasterfile)
        self.buttonSelectAddPlanningUnitDataRasterfile.clicked.connect(self.handlerSelectAddPlanningUnitRasterfile)
        self.buttonSelectAddPlanningUnitDataCsvfile.clicked.connect(self.handlerSelectAddPlanningUnitCsvfile)
        self.buttonProcessAddData.clicked.connect(self.handlerProcessAddData)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        
        # 'Land use/cover data' GroupBox
        self.groupBoxAddLandUseCoverData = QtGui.QGroupBox('Land use/cover data')
        self.layoutGroupBoxAddLandUseCoverData = QtGui.QHBoxLayout()
        self.groupBoxAddLandUseCoverData.setLayout(self.layoutGroupBoxAddLandUseCoverData)
        self.layoutOptionsAddLandUseCoverData = QtGui.QVBoxLayout()
        self.layoutOptionsAddLandUseCoverData.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsAddLandUseCoverData = QtGui.QWidget()
        self.contentOptionsAddLandUseCoverData.setLayout(self.layoutOptionsAddLandUseCoverData)
        self.layoutOptionsAddLandUseCoverData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxAddLandUseCoverData = QtGui.QCheckBox()
        self.checkBoxAddLandUseCoverData.setChecked(False)
        self.contentOptionsAddLandUseCoverData.setDisabled(True)
        self.layoutGroupBoxAddLandUseCoverData.addWidget(self.checkBoxAddLandUseCoverData)
        self.layoutGroupBoxAddLandUseCoverData.addWidget(self.contentOptionsAddLandUseCoverData)
        self.layoutGroupBoxAddLandUseCoverData.setAlignment(self.checkBoxAddLandUseCoverData, QtCore.Qt.AlignTop)
        self.layoutAddLandUseCoverDataInfo = QtGui.QVBoxLayout()
        self.layoutAddLandUseCoverData = QtGui.QGridLayout()
        self.layoutOptionsAddLandUseCoverData.addLayout(self.layoutAddLandUseCoverDataInfo)
        self.layoutOptionsAddLandUseCoverData.addLayout(self.layoutAddLandUseCoverData)
        
        self.labelAddLandUseCoverDataInfo = QtGui.QLabel()
        self.labelAddLandUseCoverDataInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutAddLandUseCoverDataInfo.addWidget(self.labelAddLandUseCoverDataInfo)
        
        self.labelAddLandUseCoverDataRasterfile = QtGui.QLabel()
        self.labelAddLandUseCoverDataRasterfile.setText('Raster file:')
        self.layoutAddLandUseCoverData.addWidget(self.labelAddLandUseCoverDataRasterfile, 0, 0)
        
        self.lineEditAddLandUseCoverDataRasterfile = QtGui.QLineEdit()
        self.lineEditAddLandUseCoverDataRasterfile.setReadOnly(True)
        self.layoutAddLandUseCoverData.addWidget(self.lineEditAddLandUseCoverDataRasterfile, 0, 1)
        
        self.buttonSelectAddLandUseCoverDataRasterfile = QtGui.QPushButton()
        self.buttonSelectAddLandUseCoverDataRasterfile.setText('&Browse')
        self.layoutAddLandUseCoverData.addWidget(self.buttonSelectAddLandUseCoverDataRasterfile, 0, 2)
        
        self.labelAddLandUseCoverDataPeriod = QtGui.QLabel()
        self.labelAddLandUseCoverDataPeriod.setText('&Period:')
        self.layoutAddLandUseCoverData.addWidget(self.labelAddLandUseCoverDataPeriod, 1, 0)
        
        self.spinBoxAddLandUseCoverDataPeriod = QtGui.QSpinBox()
        self.spinBoxAddLandUseCoverDataPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxAddLandUseCoverDataPeriod.setValue(td.year)
        self.layoutAddLandUseCoverData.addWidget(self.spinBoxAddLandUseCoverDataPeriod, 1, 1)
        
        self.labelAddLandUseCoverDataPeriod.setBuddy(self.spinBoxAddLandUseCoverDataPeriod)
        
        self.labelAddLandUseCoverDataDescription = QtGui.QLabel()
        self.labelAddLandUseCoverDataDescription.setText('&Description:')
        self.layoutAddLandUseCoverData.addWidget(self.labelAddLandUseCoverDataDescription, 2, 0)
        
        self.lineEditAddLandUseCoverDataDescription = QtGui.QLineEdit()
        self.lineEditAddLandUseCoverDataDescription.setText('description')
        self.layoutAddLandUseCoverData.addWidget(self.lineEditAddLandUseCoverDataDescription, 2, 1)
        
        self.labelAddLandUseCoverDataDescription.setBuddy(self.lineEditAddLandUseCoverDataDescription)
        
        # 'Peat data' GroupBox
        self.groupBoxAddPeatData = QtGui.QGroupBox('Peat data')
        self.layoutGroupBoxAddPeatData = QtGui.QHBoxLayout()
        self.groupBoxAddPeatData.setLayout(self.layoutGroupBoxAddPeatData)
        self.layoutOptionsAddPeatData = QtGui.QVBoxLayout()
        self.layoutOptionsAddPeatData.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsAddPeatData = QtGui.QWidget()
        self.contentOptionsAddPeatData.setLayout(self.layoutOptionsAddPeatData)
        self.layoutOptionsAddPeatData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxAddPeatData = QtGui.QCheckBox()
        self.checkBoxAddPeatData.setChecked(False)
        self.contentOptionsAddPeatData.setDisabled(True)
        self.layoutGroupBoxAddPeatData.addWidget(self.checkBoxAddPeatData)
        self.layoutGroupBoxAddPeatData.addWidget(self.contentOptionsAddPeatData)
        self.layoutGroupBoxAddPeatData.setAlignment(self.checkBoxAddPeatData, QtCore.Qt.AlignTop)
        self.layoutAddPeatDataInfo = QtGui.QVBoxLayout()
        self.layoutAddPeatData = QtGui.QGridLayout()
        self.layoutOptionsAddPeatData.addLayout(self.layoutAddPeatDataInfo)
        self.layoutOptionsAddPeatData.addLayout(self.layoutAddPeatData)
        
        self.labelAddPeatDataInfo = QtGui.QLabel()
        self.labelAddPeatDataInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutAddPeatDataInfo.addWidget(self.labelAddPeatDataInfo)
        
        self.labelAddPeatDataRasterfile = QtGui.QLabel()
        self.labelAddPeatDataRasterfile.setText('Raster file:')
        self.layoutAddPeatData.addWidget(self.labelAddPeatDataRasterfile, 0, 0)
        
        self.lineEditAddPeatDataRasterfile = QtGui.QLineEdit()
        self.lineEditAddPeatDataRasterfile.setReadOnly(True)
        self.layoutAddPeatData.addWidget(self.lineEditAddPeatDataRasterfile, 0, 1)
        
        self.buttonSelectAddPeatDataRasterfile = QtGui.QPushButton()
        self.buttonSelectAddPeatDataRasterfile.setText('&Browse')
        self.layoutAddPeatData.addWidget(self.buttonSelectAddPeatDataRasterfile, 0, 2)
        
        self.labelAddPeatDataDescription = QtGui.QLabel()
        self.labelAddPeatDataDescription.setText('&Description:')
        self.layoutAddPeatData.addWidget(self.labelAddPeatDataDescription, 1, 0)
        
        self.lineEditAddPeatDataDescription = QtGui.QLineEdit()
        self.lineEditAddPeatDataDescription.setText('description')
        self.layoutAddPeatData.addWidget(self.lineEditAddPeatDataDescription, 1, 1)
        
        self.labelAddPeatDataDescription.setBuddy(self.lineEditAddPeatDataDescription)
        
        # 'Factor data' GroupBox
        self.groupBoxAddFactorData = QtGui.QGroupBox('Factor data')
        self.layoutGroupBoxAddFactorData = QtGui.QHBoxLayout()
        self.groupBoxAddFactorData.setLayout(self.layoutGroupBoxAddFactorData)
        self.layoutOptionsAddFactorData = QtGui.QVBoxLayout()
        self.layoutOptionsAddFactorData.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsAddFactorData = QtGui.QWidget()
        self.contentOptionsAddFactorData.setLayout(self.layoutOptionsAddFactorData)
        self.layoutOptionsAddFactorData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxAddFactorData = QtGui.QCheckBox()
        self.checkBoxAddFactorData.setChecked(False)
        self.contentOptionsAddFactorData.setDisabled(True)
        self.layoutGroupBoxAddFactorData.addWidget(self.checkBoxAddFactorData)
        self.layoutGroupBoxAddFactorData.addWidget(self.contentOptionsAddFactorData)
        self.layoutGroupBoxAddFactorData.setAlignment(self.checkBoxAddFactorData, QtCore.Qt.AlignTop)
        self.layoutAddFactorDataInfo = QtGui.QVBoxLayout()
        self.layoutAddFactorData = QtGui.QGridLayout()
        self.layoutOptionsAddFactorData.addLayout(self.layoutAddFactorDataInfo)
        self.layoutOptionsAddFactorData.addLayout(self.layoutAddFactorData)
        
        self.labelAddFactorDataInfo = QtGui.QLabel()
        self.labelAddFactorDataInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutAddFactorDataInfo.addWidget(self.labelAddFactorDataInfo)
        
        self.labelAddFactorDataRasterfile = QtGui.QLabel()
        self.labelAddFactorDataRasterfile.setText('Raster file:')
        self.layoutAddFactorData.addWidget(self.labelAddFactorDataRasterfile, 0, 0)
        
        self.lineEditAddFactorDataRasterfile = QtGui.QLineEdit()
        self.lineEditAddFactorDataRasterfile.setReadOnly(True)
        self.layoutAddFactorData.addWidget(self.lineEditAddFactorDataRasterfile, 0, 1)
        
        self.buttonSelectAddFactorDataRasterfile = QtGui.QPushButton()
        self.buttonSelectAddFactorDataRasterfile.setText('&Browse')
        self.layoutAddFactorData.addWidget(self.buttonSelectAddFactorDataRasterfile, 0, 2)
        
        self.labelAddFactorDataDescription = QtGui.QLabel()
        self.labelAddFactorDataDescription.setText('&Description:')
        self.layoutAddFactorData.addWidget(self.labelAddFactorDataDescription, 1, 0)
        
        self.lineEditAddFactorDataDescription = QtGui.QLineEdit()
        self.lineEditAddFactorDataDescription.setText('description')
        self.layoutAddFactorData.addWidget(self.lineEditAddFactorDataDescription, 1, 1)
        
        self.labelAddFactorDataDescription.setBuddy(self.lineEditAddFactorDataDescription)
        
        # 'Planning unit data' GroupBox
        self.groupBoxAddPlanningUnitData = QtGui.QGroupBox('Planning unit data')
        self.layoutGroupBoxAddPlanningUnitData = QtGui.QHBoxLayout()
        self.groupBoxAddPlanningUnitData.setLayout(self.layoutGroupBoxAddPlanningUnitData)
        self.layoutOptionsAddPlanningUnitData = QtGui.QVBoxLayout()
        self.layoutOptionsAddPlanningUnitData.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsAddPlanningUnitData = QtGui.QWidget()
        self.contentOptionsAddPlanningUnitData.setLayout(self.layoutOptionsAddPlanningUnitData)
        self.layoutOptionsAddPlanningUnitData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxAddPlanningUnitData = QtGui.QCheckBox()
        self.checkBoxAddPlanningUnitData.setChecked(False)
        self.contentOptionsAddPlanningUnitData.setDisabled(True)
        self.layoutGroupBoxAddPlanningUnitData.addWidget(self.checkBoxAddPlanningUnitData)
        self.layoutGroupBoxAddPlanningUnitData.addWidget(self.contentOptionsAddPlanningUnitData)
        self.layoutGroupBoxAddPlanningUnitData.setAlignment(self.checkBoxAddPlanningUnitData, QtCore.Qt.AlignTop)
        self.layoutAddPlanningUnitDataInfo = QtGui.QVBoxLayout()
        self.layoutAddPlanningUnitData = QtGui.QGridLayout()
        self.layoutOptionsAddPlanningUnitData.addLayout(self.layoutAddPlanningUnitDataInfo)
        self.layoutOptionsAddPlanningUnitData.addLayout(self.layoutAddPlanningUnitData)
        
        self.labelAddPlanningUnitDataInfo = QtGui.QLabel()
        self.labelAddPlanningUnitDataInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutAddPlanningUnitDataInfo.addWidget(self.labelAddPlanningUnitDataInfo)
        
        self.labelAddPlanningUnitDataRasterfile = QtGui.QLabel()
        self.labelAddPlanningUnitDataRasterfile.setText('Planning unit:')
        self.layoutAddPlanningUnitData.addWidget(self.labelAddPlanningUnitDataRasterfile, 0, 0)
        
        self.lineEditAddPlanningUnitDataRasterfile = QtGui.QLineEdit()
        self.lineEditAddPlanningUnitDataRasterfile.setReadOnly(True)
        self.layoutAddPlanningUnitData.addWidget(self.lineEditAddPlanningUnitDataRasterfile, 0, 1)
        
        self.buttonSelectAddPlanningUnitDataRasterfile = QtGui.QPushButton()
        self.buttonSelectAddPlanningUnitDataRasterfile.setText('&Browse')
        self.layoutAddPlanningUnitData.addWidget(self.buttonSelectAddPlanningUnitDataRasterfile, 0, 2)
        
        self.labelAddPlanningUnitDataCsvfile = QtGui.QLabel()
        self.labelAddPlanningUnitDataCsvfile.setText('Planning unit lookup table:')
        self.layoutAddPlanningUnitData.addWidget(self.labelAddPlanningUnitDataCsvfile, 1, 0)
        
        self.lineEditAddPlanningUnitDataCsvfile = QtGui.QLineEdit()
        self.lineEditAddPlanningUnitDataCsvfile.setReadOnly(True)
        self.layoutAddPlanningUnitData.addWidget(self.lineEditAddPlanningUnitDataCsvfile, 1, 1)
        
        self.buttonSelectAddPlanningUnitDataCsvfile = QtGui.QPushButton()
        self.buttonSelectAddPlanningUnitDataCsvfile.setText('&Browse')
        self.layoutAddPlanningUnitData.addWidget(self.buttonSelectAddPlanningUnitDataCsvfile, 1, 2)
        
        self.labelAddPlanningUnitDataDescription = QtGui.QLabel()
        self.labelAddPlanningUnitDataDescription.setText('&Description:')
        self.layoutAddPlanningUnitData.addWidget(self.labelAddPlanningUnitDataDescription, 2, 0)
        
        self.lineEditAddPlanningUnitDataDescription = QtGui.QLineEdit()
        self.lineEditAddPlanningUnitDataDescription.setText('planning_unit')
        self.layoutAddPlanningUnitData.addWidget(self.lineEditAddPlanningUnitDataDescription, 2, 1)
        
        self.labelAddPlanningUnitDataDescription.setBuddy(self.lineEditAddPlanningUnitDataDescription)
        
        self.layoutButtonAddData = QtGui.QHBoxLayout()
        self.buttonProcessAddData = QtGui.QPushButton()
        self.buttonProcessAddData.setText('&Process')
        self.layoutButtonAddData.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonAddData.addWidget(self.buttonProcessAddData)
        
        self.dialogLayout.addWidget(self.groupBoxAddLandUseCoverData)
        self.dialogLayout.addWidget(self.groupBoxAddPeatData)
        self.dialogLayout.addWidget(self.groupBoxAddFactorData)
        self.dialogLayout.addWidget(self.groupBoxAddPlanningUnitData)
        self.dialogLayout.addLayout(self.layoutButtonAddData)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensAddData, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Called when the widget is closed
        """
        super(DialogLumensAddData, self).closeEvent(event)
    
    
    #***********************************************************
    # 'Add Data' QGroupBox toggle handlers
    #***********************************************************
    def toggleAddLandUseCoverData(self, checked):
        """
        """
        if checked:
            self.contentOptionsAddLandUseCoverData.setEnabled(True)
        else:
            self.contentOptionsAddLandUseCoverData.setDisabled(True)
    
    
    def toggleAddPeatData(self, checked):
        """
        """
        if checked:
            self.contentOptionsAddPeatData.setEnabled(True)
        else:
            self.contentOptionsAddPeatData.setDisabled(True)
    
    
    def toggleAddFactorData(self, checked):
        """
        """
        if checked:
            self.contentOptionsAddFactorData.setEnabled(True)
        else:
            self.contentOptionsAddFactorData.setDisabled(True)
    
    
    def toggleAddPlanningUnitData(self, checked):
        """
        """
        if checked:
            self.contentOptionsAddPlanningUnitData.setEnabled(True)
        else:
            self.contentOptionsAddPlanningUnitData.setDisabled(True)
    
    
    #***********************************************************
    # 'Add Data' QPushButton handlers
    #***********************************************************
    def handlerSelectAddLandUseCoverDataRasterfile(self):
        """Select a raster file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Raster File', QtCore.QDir.homePath(), 'Raster File (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditAddLandUseCoverDataRasterfile.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectAddPeatDataRasterfile(self):
        """Select a raster file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Raster File', QtCore.QDir.homePath(), 'Raster File (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditAddPeatDataRasterfile.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectAddFactorDataRasterfile(self):
        """Select a raster file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Raster File', QtCore.QDir.homePath(), 'Raster File (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditAddFactorDataRasterfile.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectAddPlanningUnitRasterfile(self):
        """Select a raster file
        """
        rasterfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Raster File', QtCore.QDir.homePath(), 'Planning Unit Raster File (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if rasterfile:
            self.lineEditAddPlanningUnitDataRasterfile.setText(rasterfile)
            
            logging.getLogger(type(self).__name__).info('select rasterfile: %s', rasterfile)
    
    
    def handlerSelectAddPlanningUnitCsvfile(self):
        """Select a csv file
        """
        csvfile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Lookup Table', QtCore.QDir.homePath(), 'Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if csvfile:
            self.lineEditAddPlanningUnitDataCsvfile.setText(csvfile)
            
            logging.getLogger(type(self).__name__).info('select csvfile: %s', csvfile)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        # 'Land use/cover data' groupbox fields
        self.main.appSettings['DialogLumensAddLandcoverRaster']['rasterfile'] \
            = unicode(self.lineEditAddLandUseCoverDataRasterfile.text())
        self.main.appSettings['DialogLumensAddLandcoverRaster']['period'] \
            = self.spinBoxAddLandUseCoverDataPeriod.value()
        self.main.appSettings['DialogLumensAddLandcoverRaster']['description'] \
            = unicode(self.lineEditAddLandUseCoverDataDescription.text())
        
        # 'Peat data' groupbox fields
        self.main.appSettings['DialogLumensAddPeatData']['rasterfile'] \
            = unicode(self.lineEditAddPeatDataRasterfile.text())
        self.main.appSettings['DialogLumensAddPeatData']['description'] \
            = unicode(self.lineEditAddPeatDataDescription.text())
        
        # 'Factor data' groupbox fields
        self.main.appSettings['DialogLumensAddFactorData']['rasterfile'] \
            = unicode(self.lineEditAddFactorDataRasterfile.text())
        self.main.appSettings['DialogLumensAddFactorData']['description'] \
            = unicode(self.lineEditAddFactorDataDescription.text())
        
        # 'Planning unit data' groupbox fields
        self.main.appSettings['DialogLumensAddPlanningUnitData']['rasterfile'] \
            = unicode(self.lineEditAddPlanningUnitDataRasterfile.text())
        self.main.appSettings['DialogLumensAddPlanningUnitData']['csvfile'] \
            = unicode(self.lineEditAddPlanningUnitDataCsvfile.text())
        self.main.appSettings['DialogLumensAddPlanningUnitData']['description'] \
            = unicode(self.lineEditAddPlanningUnitDataDescription.text())
        
    
    def validForm(self, formName):
        """
        """
        logging.getLogger(type(self).__name__).info('form validate: %s', formName)
        logging.getLogger(type(self).__name__).info('form values: %s', self.main.appSettings[formName])
        
        valid = True
        
        for key, val in self.main.appSettings[formName].iteritems():
            if val == 0: # for values set specific to 0
                continue
            elif not val:
                valid = False
        
        if not valid:
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
        
        return valid
    
    
    def outputsMessageBox(self, algName, outputs, successMessage, errorMessage):
        """Display a messagebox based on the processing result
        """
        if outputs and outputs['statuscode'] == '1':
            QtGui.QMessageBox.information(self, 'Success', successMessage)
            return True
        else:
            statusMessage = '"{0}" failed with status message:'.format(algName)
            
            if outputs and outputs['statusmessage']:
                statusMessage = '{0} {1}'.format(statusMessage, outputs['statusmessage'])
            
            logging.getLogger(type(self).__name__).error(statusMessage)
            QtGui.QMessageBox.critical(self, 'Error', errorMessage)
            return False
    
    
    def handlerProcessAddData(self):
        """
        """
        self.setAppSettings()
        
        if self.checkBoxAddLandUseCoverData.isChecked():
            formName = 'DialogLumensAddLandcoverRaster'
            algName = 'modeler:lumens_add_landcover_raster'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                self.buttonProcessAddData.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['rasterfile'],
                    self.main.appSettings[formName]['period'],
                    self.main.appSettings[formName]['description'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessAddData.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxAddPeatData.isChecked():
            formName = 'DialogLumensAddPeatData'
            algName = 'modeler:lumens_add_peat'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                self.buttonProcessAddData.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['rasterfile'],
                    self.main.appSettings[formName]['description'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessAddData.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxAddFactorData.isChecked():
            formName = 'DialogLumensAddFactorData'
            algName = 'modeler:lumens_add_factor_data'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                self.buttonProcessAddData.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['rasterfile'],
                    self.main.appSettings[formName]['description'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessAddData.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        
        if self.checkBoxAddPlanningUnitData.isChecked():
            formName = 'DialogLumensAddPlanningUnitData'
            algName = 'modeler:lumens_add_planning_unit'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                self.buttonProcessAddData.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['rasterfile'],
                    self.main.appSettings[formName]['csvfile'],
                    self.main.appSettings[formName]['description'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessAddData.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
        