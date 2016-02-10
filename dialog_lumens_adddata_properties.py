#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, csv, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *

class DialogLumensAddDataProperties(QtGui.QDialog):
    """
    """
    def __init__(self, parent, dataType, dataFile):
        super(DialogLumensAddDataProperties, self).__init__(parent)
        self.dataType = dataType
        self.dataFile = dataFile
        self.main = parent
        self.dialogTitle = 'LUMENS Data Properties'
        
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
        
        if self.dataFile.lower().endswith(self.main.main.appSettings['selectRasterfileExt']):
            self.isRasterFile = True
        elif self.dataFile.lower().endswith(self.main.main.appSettings['selectShapefileExt']):
            self.isVectorFile = True
        elif self.dataFile.lower().endswith(self.main.main.appSettings['selectCsvfileExt']):
            self.isCsvFile = True
        
        self.setupUi(self)
        
        if self.dataFile.lower().endswith(self.main.main.appSettings['selectShapefileExt']):
            self.loadDataFieldAttributes()
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
    
    def setupUi(self, parent):
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
        self.lineEditDataDescription.setText('description')
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
        
        if self.dataType == 'Land Use/Cover' or self.dataType == 'Planning Unit':
            # Table
            rowCount += 1
            self.layoutDataProperties.addWidget(self.dataTable, rowCount, 0, 1, 2)
            
            if self.isRasterFile:
                self.loadRasterDataTable()
        
        ######################################################################
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        
        self.dialogLayout.addWidget(self.groupBoxDataProperties)
        self.dialogLayout.addWidget(self.buttonBox)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(800, 600)
        self.resize(parent.sizeHint())
    
    
    def getDataDescription(self):
        """
        """
        return self.dataDescription
    
    
    def getDataPeriod(self):
        """
        """
        return self.dataPeriod
    
    
    def getDataFieldAttributes(self):
        """
        """
        return self.dataFieldAttribute
    
    
    def loadRasterDataTable(self):
        """
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
                  fieldLegend = QtGui.QTableWidgetItem('Unidentified Landuse {0}'.format(fieldTableItem.text()))
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
        """
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
    def accept(self):
        """
        """
        self.dataDescription = unicode(self.lineEditDataDescription.text())
        self.dataPeriod = self.spinBoxDataPeriod.value()
        self.dataFieldAttribute = unicode(self.comboBoxDataFieldAttribute.currentText())
        # dataTable
        
        if self.dataType == 'Land Use/Cover' and self.isRasterFile and self.dataDescription and self.dataPeriod:
            QtGui.QDialog.accept(self)
        elif self.dataType == 'Land Use/Cover' and self.isVectorFile and self.dataDescription and self.dataPeriod and self.dataFieldAttribute:
            QtGui.QDialog.accept(self)
        elif self.dataType == 'Planning Unit' and self.isRasterFile and self.dataDescription:
            QtGui.QDialog.accept(self)
        elif self.dataType == 'Planning Unit' and self.isVectorFile and self.dataDescription and self.dataFieldAttribute:
            QtGui.QDialog.accept(self)
        elif self.dataType == 'Factor' and self.isRasterFile and self.dataDescription:
            QtGui.QDialog.accept(self)
        elif self.dataType == 'Table' and self.isCsvFile and self.dataDescription:
            QtGui.QDialog.accept(self)
        else:
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
            return
    
    
    def reject(self):
        """
        """
        QtGui.QDialog.reject(self)
    