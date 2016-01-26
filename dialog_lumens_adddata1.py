#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_viewer import DialogLumensViewer


class DialogLumensAddData1(QtGui.QDialog):
    """
    """
    def __init__(self, parent):
        super(DialogLumensAddData1, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS Add Data'
        self.tableAddDataRowCount = 0
        self.tableAddData = []
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensAddData1 init'
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
        
        self.buttonAddDataRow.clicked.connect(self.handlerButtonAddDataRow)
        self.buttonProcessAddData.clicked.connect(self.handlerProcessAddData)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.groupBoxAddData = QtGui.QGroupBox('Add data')
        self.layoutGroupBoxAddData = QtGui.QVBoxLayout()
        self.layoutGroupBoxAddData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxAddData.setLayout(self.layoutGroupBoxAddData)
        self.layoutAddDataInfo = QtGui.QVBoxLayout()
        self.layoutAddData = QtGui.QVBoxLayout()
        self.layoutGroupBoxAddData.addLayout(self.layoutAddDataInfo)
        self.layoutGroupBoxAddData.addLayout(self.layoutAddData)
        
        self.labelAddDataInfo = QtGui.QLabel()
        self.labelAddDataInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutAddDataInfo.addWidget(self.labelAddDataInfo)
        
        self.layoutButtonAddData = QtGui.QHBoxLayout()
        self.layoutButtonAddData.setContentsMargins(0, 0, 0, 0)
        self.layoutButtonAddData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.buttonAddDataRow = QtGui.QPushButton()
        self.buttonAddDataRow.setText('Add Data')
        self.buttonAddDataRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonAddData.addWidget(self.buttonAddDataRow)
        
        self.layoutContentAddData = QtGui.QVBoxLayout()
        self.layoutContentAddData.setContentsMargins(5, 5, 5, 5)
        self.contentAddData = QtGui.QWidget()
        self.contentAddData.setLayout(self.layoutContentAddData)
        self.scrollAddData = QtGui.QScrollArea()
        self.scrollAddData.setWidgetResizable(True);
        self.scrollAddData.setWidget(self.contentAddData)
        self.layoutTableAddData = QtGui.QVBoxLayout()
        self.layoutTableAddData.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentAddData.addLayout(self.layoutTableAddData)
        
        self.layoutAddData.addLayout(self.layoutButtonAddData)
        self.layoutAddData.addWidget(self.scrollAddData)
        
        self.layoutButtonProcessAddData = QtGui.QHBoxLayout()
        self.buttonProcessAddData = QtGui.QPushButton()
        self.buttonProcessAddData.setText('&Process')
        self.layoutButtonProcessAddData.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonProcessAddData.addWidget(self.buttonProcessAddData)
        
        self.dialogLayout.addWidget(self.groupBoxAddData)
        self.dialogLayout.addLayout(self.layoutButtonProcessAddData)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensAddData1, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Called when the widget is closed
        """
        super(DialogLumensAddData1, self).closeEvent(event)
    
    
    def clearLayout(self, layout):
        """Clear a layout and all its child widgets
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtGui.QWidgetItem):
                item.widget().deleteLater() # use this to properly delete the widget
            elif isinstance(item, QtGui.QSpacerItem):
                pass
            else:
                self.clearLayout(item.layout())
            
            layout.removeItem(item)
    
    
    def addDataRow(self):
        """Add a data row
        """
        self.tableAddDataRowCount = self.tableAddDataRowCount + 1
        
        layoutDataRow = QtGui.QHBoxLayout()
        
        buttonDeleteDataRow = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionClear.png')
        buttonDeleteDataRow.setIcon(icon)
        buttonDeleteDataRow.setObjectName('buttonDeleteDataRow_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(buttonDeleteDataRow)
        
        comboBoxDataType = QtGui.QComboBox()
        comboBoxDataType.addItems(['Land Use/Cover', 'Planning Unit', 'Factor'])
        comboBoxDataType.setObjectName('comboBoxDataType_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(comboBoxDataType)
        
        lineEditDataFile = QtGui.QLineEdit()
        lineEditDataFile.setReadOnly(True)
        lineEditDataFile.setObjectName('lineEditDataFile_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(lineEditDataFile)
        
        buttonSelectDataFile = QtGui.QPushButton()
        buttonSelectDataFile.setText('Select File')
        buttonSelectDataFile.setObjectName('buttonSelectDataFile_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(buttonSelectDataFile)
        
        spinBoxDataPeriod = QtGui.QSpinBox()
        spinBoxDataPeriod.setRange(1, 9999)
        td = datetime.date.today()
        spinBoxDataPeriod.setValue(td.year)
        spinBoxDataPeriod.setObjectName('spinBoxDataPeriod_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(spinBoxDataPeriod)
        
        lineEditDataDescription = QtGui.QLineEdit()
        lineEditDataDescription.setText('description')
        lineEditDataDescription.setObjectName('lineEditDataDescription_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(lineEditDataDescription)
        
        self.layoutTableAddData.addLayout(layoutDataRow)
        
        buttonSelectDataFile.clicked.connect(self.handlerSelectDataFile)
        buttonDeleteDataRow.clicked.connect(self.handlerDeleteDataRow)
    
    
    #***********************************************************
    # 'Add Data' QPushButton handlers
    #***********************************************************
    def handlerButtonAddDataRow(self):
        """
        """
        self.addDataRow()
    
    
    def handlerSelectDataFile(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select File', QtCore.QDir.homePath(), 'File (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if file:        
            buttonSender = self.sender()
            objectName = buttonSender.objectName()
            tableRow = objectName.split('_')[1]
            
            lineEditDataFile = self.contentAddData.findChild(QtGui.QLineEdit, 'lineEditDataFile_' + tableRow)
            lineEditDataFile.setText(file)
    
    
    def handlerDeleteDataRow(self):
        """
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        layoutRow = self.layoutTableAddData.itemAt(int(tableRow) - 1).layout()
        self.clearLayout(layoutRow)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        completeData = True
        self.tableAddData = []
        
        for tableRow in range(1, self.tableAddDataRowCount + 1):
            lineEditDataFile = self.findChild(QtGui.QLineEdit, 'lineEditDataFile_' + str(tableRow))
            
            if not lineEditDataFile: # Row has been deleted
                print 'DEBUG: skipping a deleted row.'
                continue
            
            comboBoxDataType = self.findChild(QtGui.QComboBox, 'comboBoxDataType_' + str(tableRow))
            spinBoxDataPeriod = self.findChild(QtGui.QSpinBox, 'spinBoxDataPeriod_' + str(tableRow))
            lineEditDataDescription = self.findChild(QtGui.QLineEdit, 'lineEditDataDescription_' + str(tableRow))
            
            dataFile = unicode(lineEditDataFile.text())
            dataType = unicode(comboBoxDataType.currentText())
            dataPeriod = spinBoxDataPeriod.value()
            dataDescription = unicode(lineEditDataDescription.text())
            
            if dataFile and dataType and dataPeriod and dataDescription:
                if dataType == 'Land Use/Cover':
                    dataType = 0
                elif dataType == 'Planning Unit':
                    dataType = 1
                elif dataType == 'Factor':
                    dataType = 2
                else:
                    dataType = 0
                
                tableRowData = {
                    'dataFile': dataFile,
                    'dataType': dataType,
                    'dataPeriod': dataPeriod,
                    'dataDescription': dataDescription,
                }
                
                self.tableAddData.append(tableRowData)
            else:
                completeData = False
        
        if not len(self.tableAddData):
            completeData = False
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
        
        return completeData
    
    
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
        completeData = self.setAppSettings()
        
        if completeData:
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            self.buttonProcessAddData.setDisabled(True)
            
            algName = None
            outputs = None
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            for tableRowData in self.tableAddData:
                # The algName to be used depends on the type of the dataFile (vector or raster)
                algName = 'r:lumensaddrasterdata1'
                
                outputs = general.runalg(
                    algName,
                    tableRowData['dataType'],
                    tableRowData['dataFile'],
                    tableRowData['dataPeriod'],
                    tableRowData['dataDescription'],
                    None,
                    None,
                    None,
                )
                
                print 'DEBUG'
                print outputs
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(QtCore.Qt.WindowActive)
            
            algSuccess = self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessAddData.setEnabled(True)
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            