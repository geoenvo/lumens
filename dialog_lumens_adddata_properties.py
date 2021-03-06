#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, csv, tempfile, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *

from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer


class DialogLumensAddDataProperties(QtGui.QDialog):
    """LUMENS dialog class for the "Add Data" data properties.
    
    Attributes:
        dataType (str): the type of the added data, can be either raster, vector, or csv files.
        dataFile (str): the file path of the added data.
        dataDescription (str): the description of the added data.
        dataPeriod (int): the period of the added data.
        dataTableCsv (str): the path to the table csv temporary file
        dataFieldAttribute (str): the selected attribute of the added shapefile data.
        dataDissolvedShapefile (str): the file path of the added shapefile data that has been dissolved.
    """
    
    def __init__(self, parent, dataType, dataFile):
        """Constructor method for initializing a LUMENS "Add Data" data properties dialog window instance.
        
        Args:
            parent: the dialog window's parent instance.
            dataType (str): the type of the added data.
            dataFile (str): the file path of the added data.
        """
        super(DialogLumensAddDataProperties, self).__init__(parent)
        self.parent = parent
        self.dialogTitle = 'LUMENS Data Properties'
        
        self.dataType = dataType
        self.dataFile = dataFile
        # Use file name without extension as data description
        self.dataDescription = os.path.splitext(os.path.basename(dataFile))[0]
        self.dataPeriod = 0
        self.dataTableCsv = None
        self.dataFieldAttribute = None
        self.dataDissolvedShapefile = None
        
        # The classification of the data to be added
        self.classifiedOptions = {
            1: 'Hutan primer',
            2: 'Hutan sekunder',
            3: 'Tanaman pohon monokultur',
            4: 'Tanaman pohon campuran',
            5: 'Tanaman pertanian semusim',
            6: 'Semak, rumput dan lahan terbuka',
            7: 'Pemukiman',
            8: 'Lain-lain',
        }
        self.isRasterFile = False
        self.isVectorFile = False
        self.isCsvFile = False
        
        if self.dataFile.lower().endswith(self.parent.main.appSettings['selectRasterfileExt']):
            self.isRasterFile = True
        elif self.dataFile.lower().endswith(self.parent.main.appSettings['selectShapefileExt']):
            self.isVectorFile = True
        elif self.dataFile.lower().endswith(self.parent.main.appSettings['selectCsvfileExt']):
            self.isCsvFile = True
        
        if self.parent.main.appSettings['debug']:
            print 'DEBUG: DialogLumensAddDataProperties init'
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.parent.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        # Raster data table is loaded only for 'Land Use/Cover' and 'Planning Unit'
        if self.isRasterFile and self.dataType in ('Land Use/Cover', 'Planning Unit'):
            self.loadRasterDataTable()
        elif self.isVectorFile:
            self.loadDataFieldAttributes()
        
        self.buttonProcessDissolve.clicked.connect(self.handlerProcessDissolve)
        self.buttonProcessSave.clicked.connect(self.handlerProcessSave)
        self.buttonSelectDataMapping.clicked.connect(self.handlerSelectDataMapping)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()
        
        addFileType = None
        
        if self.isRasterFile:
            addFileType = 'Add raster data'
        elif self.isVectorFile:
            addFileType = 'Add vector data'
        elif self.isCsvFile:
            addFileType = 'Add tabular data'
        
        self.groupBoxDataProperties = QtGui.QGroupBox('{0}: {1}'.format(self.dataType, addFileType))
        self.layoutGroupBoxDataProperties = QtGui.QVBoxLayout()
        self.layoutGroupBoxDataProperties.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDataProperties.setLayout(self.layoutGroupBoxDataProperties)
        self.layoutDataPropertiesInfo = QtGui.QVBoxLayout()
        self.layoutDataProperties = QtGui.QGridLayout()
        self.layoutGroupBoxDataProperties.addLayout(self.layoutDataPropertiesInfo)
        self.layoutGroupBoxDataProperties.addLayout(self.layoutDataProperties)
        
        self.labelDataPropertiesInfo = QtGui.QLabel()
        self.labelDataPropertiesInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutDataPropertiesInfo.addWidget(self.labelDataPropertiesInfo)
        
        rowCount = 0
        
        self.labelDataDescription = QtGui.QLabel()
        self.labelDataDescription.setText('&Description:')
        self.lineEditDataDescription = QtGui.QLineEdit()
        self.lineEditDataDescription.setText(self.dataDescription)
        self.labelDataDescription.setBuddy(self.lineEditDataDescription)
        
        td = datetime.date.today()
        self.labelDataSpinBoxPeriod = QtGui.QLabel()
        self.labelDataSpinBoxPeriod.setText('&Period:')
        self.spinBoxDataPeriod = QtGui.QSpinBox()
        self.spinBoxDataPeriod.setRange(1, 9999)
        self.spinBoxDataPeriod.setValue(td.year)
        self.labelDataSpinBoxPeriod.setBuddy(self.spinBoxDataPeriod)
        
        if self.dataType == 'Land Use/Cover':
            # Description + Period
            self.layoutDataProperties.addWidget(self.labelDataDescription, rowCount, 0)
            self.layoutDataProperties.addWidget(self.lineEditDataDescription, rowCount, 1)
            rowCount += 1
            self.layoutDataProperties.addWidget(self.labelDataSpinBoxPeriod, rowCount, 0)
            self.layoutDataProperties.addWidget(self.spinBoxDataPeriod, rowCount, 1)
        else:
            # Description only
            self.layoutDataProperties.addWidget(self.labelDataDescription, rowCount, 0)
            self.layoutDataProperties.addWidget(self.lineEditDataDescription, rowCount, 1)
        
        self.labeldataFieldAttribute = QtGui.QLabel()
        self.labeldataFieldAttribute.setText('Field attribute:')
        self.comboBoxDataFieldAttribute = QtGui.QComboBox()
        self.comboBoxDataFieldAttribute.setDisabled(True)
        
        if self.isVectorFile:
            # For vector data files
            rowCount += 1
            self.layoutDataProperties.addWidget(self.labeldataFieldAttribute, rowCount, 0)
            self.layoutDataProperties.addWidget(self.comboBoxDataFieldAttribute, rowCount, 1)
        
        self.dataTable = QtGui.QTableWidget()
        self.dataTable.setDisabled(True)
        self.dataTable.verticalHeader().setVisible(False)
        
        self.labelDataMapping = QtGui.QLabel()
        self.labelDataMapping.setText('Data mapping:')
        self.lineEditDataMapping = QtGui.QLineEdit()
        self.lineEditDataMapping.setReadOnly(True)
        self.buttonSelectDataMapping = QtGui.QPushButton()
        self.buttonSelectDataMapping.setText('&Browse')
        self.buttonSelectDataMapping.setDisabled(True)
        
        rowCount += 1
        
        if self.dataType == 'Land Use/Cover':
            dataTableColumnSpan = 2
            if self.isVectorFile:
                self.layoutDataProperties.addWidget(self.labelDataMapping, rowCount, 0)
                self.layoutDataProperties.addWidget(self.lineEditDataMapping, rowCount, 1)
                self.layoutDataProperties.addWidget(self.buttonSelectDataMapping, rowCount, 2)
                dataTableColumnSpan = 3
                rowCount += 1
            self.layoutDataProperties.addWidget(self.dataTable, rowCount, 0, 1, dataTableColumnSpan)
        elif self.dataType == 'Planning Unit':
            self.layoutDataProperties.addWidget(self.dataTable, rowCount, 0, 1, 2)
        
        ######################################################################
        
        self.layoutButtonProcess = QtGui.QHBoxLayout()
        self.buttonProcessDissolve = QtGui.QPushButton()
        self.buttonProcessDissolve.setText('&Dissolve')
        self.buttonProcessDissolve.setVisible(False)
        self.buttonProcessSave = QtGui.QPushButton()
        self.buttonProcessSave.setText('&Save')
        self.layoutButtonProcess.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonProcess.addWidget(self.buttonProcessDissolve)
        self.layoutButtonProcess.addWidget(self.buttonProcessSave)
        
        if self.isVectorFile:
            self.buttonProcessDissolve.setVisible(True)
            self.buttonProcessSave.setDisabled(True)
        
        self.dialogLayout.addWidget(self.groupBoxDataProperties)
        self.dialogLayout.addLayout(self.layoutButtonProcess)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(800, 600)
        self.resize(parent.sizeHint())
    
    
    def getDataDescription(self):
        """Getter method.
        """
        return self.dataDescription
    
    
    def getDataPeriod(self):
        """Getter method.
        """
        return self.dataPeriod
    
    
    def getDataTableCsv(self):
        """Getter method.
        """
        return self.dataTableCsv
    
    
    def getDataFieldAttribute(self):
        """Getter method.
        """
        return self.dataFieldAttribute
    
    
    def getDataDissolvedShapefile(self):
        """Getter method.
        """
        return self.dataDissolvedShapefile
    
    
    def loadRasterDataTable(self):
        """Method for loading the raster properties to the data table.
        
        The raster loading process calls the following algorithm:
        1. r:lumensdatapropertiesraster
        """
        algName = 'r:lumensdatapropertiesraster'
        
        outputs = general.runalg(
            algName,
            self.dataFile,
            None,
        )
        
        outputsKey = 'data_table'
        
        if outputs and outputsKey in outputs and os.path.exists(outputs[outputsKey]):  
            with open(outputs[outputsKey], 'rb') as f:
                hasHeader = csv.Sniffer().has_header(f.read(1024))
                f.seek(0)
                reader = csv.reader(f)
                
                if hasHeader: # Set the column headers
                    headerRow = reader.next()
                    fields = [str(field) for field in headerRow]
                    
                    fields.append('Legend') # Additional columns ('Classified' only for Land Use/Cover types)
                    
                    if self.dataType == 'Land Use/Cover':
                        fields.append('Classified')
                    
                    self.dataTable.setColumnCount(len(fields))
                    self.dataTable.setHorizontalHeaderLabels(fields)
                
                dataTable = []
                
                for row in reader:
                    dataRow = [QtGui.QTableWidgetItem(field) for field in row]
                    dataTable.append(dataRow)
                
                self.dataTable.setRowCount(len(dataTable))
                
                tableRow = 0
                columnLegend = 0
                columnClassified = 0
                
                for dataRow in dataTable:
                    tableColumn = 0
                    for fieldTableItem in dataRow:
                        fieldTableItem.setFlags(fieldTableItem.flags() & ~QtCore.Qt.ItemIsEnabled)
                        self.dataTable.setItem(tableRow, tableColumn, fieldTableItem)
                        self.dataTable.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                        tableColumn += 1
                    
                    # Additional columns ('Classified' only for Land Use/Cover types)
                    fieldLegend = QtGui.QTableWidgetItem('Unidentified Landuse {0}'.format(tableRow + 1))
                    columnLegend = tableColumn
                    self.dataTable.setItem(tableRow, tableColumn, fieldLegend)
                    self.dataTable.horizontalHeader().setResizeMode(columnLegend, QtGui.QHeaderView.ResizeToContents)
                    
                    if self.dataType == 'Land Use/Cover':
                        tableColumn += 1
                        columnClassified = tableColumn
                        comboBoxClassified = QtGui.QComboBox()
                        for key, val in self.classifiedOptions.iteritems():
                            comboBoxClassified.addItem(val, key)
                        self.dataTable.setCellWidget(tableRow, tableColumn, comboBoxClassified)
                        self.dataTable.horizontalHeader().setResizeMode(columnClassified, QtGui.QHeaderView.ResizeToContents)
                    
                    tableRow += 1
                
                self.dataTable.setEnabled(True)
    
    
    def loadDataFieldAttributes(self):
        """Method for loading the shapefile's attributes.
        """
        registry = QgsProviderRegistry.instance()
        provider = registry.provider('ogr', self.dataFile)
        
        if not provider.isValid():
            return
        
        attributes = []
        
        for field in provider.fields():
            attributes.append(field.name())
        
        self.comboBoxDataFieldAttribute.clear()
        self.comboBoxDataFieldAttribute.addItems(sorted(attributes))
        self.comboBoxDataFieldAttribute.setEnabled(True)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def validDissolved(self):
        """Method for validating the form values before dissolving.
        """
        valid = False
        
        if self.dataType == 'Land Use/Cover' and self.isVectorFile and self.dataDescription and self.dataPeriod and self.dataFieldAttribute:
            valid = True
        elif self.dataType == 'Planning Unit' and self.isVectorFile and self.dataDescription and self.dataFieldAttribute:
            valid = True
        else:
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
        
        return valid
    
    
    def validForm(self):
        """Method for validating the form values.
        """
        valid = False
        
        if self.dataType == 'Land Use/Cover' and self.isRasterFile and self.dataDescription and self.dataPeriod and self.dataTableCsv:
            valid = True
        elif self.dataType == 'Land Use/Cover' and self.isVectorFile and self.dataDescription and self.dataPeriod and self.dataFieldAttribute and self.dataTableCsv:
            valid = True
        elif self.dataType == 'Planning Unit' and self.isRasterFile and self.dataDescription and self.dataTableCsv:
            valid = True
        elif self.dataType == 'Planning Unit' and self.isVectorFile and self.dataDescription and self.dataFieldAttribute and self.dataTableCsv:
            valid = True
        elif self.dataType == 'Factor' and self.isRasterFile and self.dataDescription:
            valid = True
        elif self.dataType == 'Table' and self.isCsvFile and self.dataDescription:
            valid = True
        else:
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
        
        return valid
    
    
    def setFormFields(self):
        """Set the required values from the form widgets.
        """
        self.dataDescription = unicode(self.lineEditDataDescription.text())
        self.dataPeriod = self.spinBoxDataPeriod.value()
        self.dataFieldAttribute = unicode(self.comboBoxDataFieldAttribute.currentText())
        self.dataTableCsv = DialogLumensBase.writeTableCsv(self.dataTable, True)
        
    
    def handlerProcessDissolve(self):
        """Slot method to pass the form values and execute the "Dissolve" R algorithm.
        
        The "Dissolve" process calls the following algorithm:
        1. r:lumensdissolve
        """
        self.setFormFields()
        
        if self.validDissolved():
            logging.getLogger(type(self).__name__).info('start: %s' % 'LUMENS Dissolve')
            self.buttonProcessDissolve.setDisabled(True)
                
            algName = 'r:lumensdissolve'
            
            outputs = general.runalg(
                algName,
                self.dataFile,
                self.dataFieldAttribute,
                None,
            )
            
            # Display ROut file in debug mode
            if self.parent.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.parent.main.appSettings['ROutFile'])
                dialog.exec_()
            
            outputsKey = 'admin_output'
            
            if outputs and outputsKey in outputs and os.path.exists(outputs[outputsKey]):
                self.dataDissolvedShapefile = outputs[outputsKey]
                
                registry = QgsProviderRegistry.instance()
                provider = registry.provider('ogr', outputs[outputsKey])
                
                if not provider.isValid():
                    logging.getLogger(type(self).__name__).error('LUMENS Dissolve: invalid shapefile')
                    return
                
                attributes = []
                for field in provider.fields():
                    attributes.append(field.name())
                
                # Additional columns ('Legend', 'Classified' only for Land Use/Cover types)
                if self.dataType == 'Land Use/Cover':
                    attributes.append('Legend')
                    attributes.append('Classified')
                
                features = provider.getFeatures()
                
                if features:
                    self.dataTable.setEnabled(True)
                    self.dataTable.setRowCount(provider.featureCount())
                    self.dataTable.setColumnCount(len(attributes))
                    self.dataTable.verticalHeader().setVisible(False)
                    self.dataTable.setHorizontalHeaderLabels(attributes)
                    
                    # Need a nicer way than manual looping
                    tableRow = 0
                    for feature in features:
                        tableColumn = 0
                        for attribute in attributes:
                            if attribute == 'Legend' or attribute == 'Classified': # Skip the additional column
                                continue
                            attributeValue = str(feature.attribute(attribute))
                            attributeValueTableItem = QtGui.QTableWidgetItem(attributeValue)
                            if tableColumn == 1 and self.dataType == 'Planning Unit': # Editable second column for Vector Planning Units
                                pass
                            else:
                                attributeValueTableItem.setFlags(attributeValueTableItem.flags() & ~QtCore.Qt.ItemIsEnabled)
                            self.dataTable.setItem(tableRow, tableColumn, attributeValueTableItem)
                            self.dataTable.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                            tableColumn += 1
                        
                        # Additional columns ('Legend', 'Classified' only for Land Use/Cover types)
                        if self.dataType == 'Land Use/Cover':
                            fieldLegend = QtGui.QTableWidgetItem('Unidentified Landuse {0}'.format(tableRow + 1))
                            columnLegend = tableColumn
                            self.dataTable.setItem(tableRow, tableColumn, fieldLegend)
                            self.dataTable.horizontalHeader().setResizeMode(columnLegend, QtGui.QHeaderView.ResizeToContents)
                            
                            tableColumn += 1
                            columnClassified = tableColumn
                            comboBoxClassified = QtGui.QComboBox()
                            for key, val in self.classifiedOptions.iteritems():
                                comboBoxClassified.addItem(val, key)
                            self.dataTable.setCellWidget(tableRow, tableColumn, comboBoxClassified)
                            self.dataTable.horizontalHeader().setResizeMode(columnClassified, QtGui.QHeaderView.ResizeToContents)
                        
                        tableRow += 1
                    
                    self.dataTable.resizeColumnsToContents()
                    self.buttonProcessSave.setEnabled(True)
            
            self.buttonSelectDataMapping.setEnabled(True)
            self.buttonProcessDissolve.setEnabled(True)
            logging.getLogger(type(self).__name__).info('end: %s' % 'LUMENS Dissolve')
        
    
    def handlerProcessSave(self):
        """Slot method for saving the form values before closing the dialog.
        """
        self.setFormFields()
        
        if self.validForm():
            self.accept()
    
    
    def handlerSelectDataMapping(self):
        """Slot method for selecting a data mapping file in CSV format.
        """
        dataMappingFile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Data Mapping File', QtCore.QDir.homePath(), 'Data Mapping File (*{0})'.format(self.parent.main.appSettings['selectCsvfileExt'])))
        
        if dataMappingFile:
            logging.getLogger(type(self).__name__).info('select data mapping file: %s', dataMappingFile)
            
            self.lineEditDataMapping.setText(dataMappingFile)
            
            self.processDataMapping(dataMappingFile)
    
    
    def processDataMapping(self, dataMappingFile):
        """Method for processing the data mapping file and mapping the data
        in the data table.
        
        Args:
            dataMappingFile (str): the file path of a data mapping file.
        """
        dataMapping = {}
        
        with open(dataMappingFile, 'rb') as f:
            hasHeader = csv.Sniffer().has_header(f.read(1024))
            f.seek(0)
            reader = csv.reader(f)
            
            if hasHeader: # Skip the header
                next(reader)
            
            for row in reader:
                dataMapping[str(row[0]).lower()] = str(row[1]).lower()
            
            fieldColumn = classifiedColumn = 0
            
            for headerColumn in range(self.dataTable.columnCount()):
                headerItem = self.dataTable.horizontalHeaderItem(headerColumn)
                headerText = headerItem.text()
                if headerText == unicode(self.comboBoxDataFieldAttribute.currentText()):
                    fieldColumn = headerColumn
                elif headerText == 'Classified':
                    classifiedColumn = headerColumn
            
            for tableRow in range(self.dataTable.rowCount()):
                fieldItem = self.dataTable.item(tableRow, fieldColumn)
                classifiedWidget = self.dataTable.cellWidget(tableRow, classifiedColumn)
                fieldItemText = fieldItem.text().lower()
                if fieldItemText in dataMapping:
                    classification = dataMapping[fieldItemText]
                    # Perform case insensitive search of the ComboBox
                    classifiedOptionIndex = classifiedWidget.findText(classification, QtCore.Qt.MatchFixedString)
                    # Found a data mapping match!
                    if classifiedOptionIndex >= 0:
                        classifiedWidget.setCurrentIndex(classifiedOptionIndex)
    
    
    def accept(self):
        """Overload method that is called when the dialog is accepted.
        """
        QtGui.QDialog.accept(self)
    
    
    def reject(self):
        """Overload method that is called when the dialog is rejected (canceled).
        """
        QtGui.QDialog.reject(self)
