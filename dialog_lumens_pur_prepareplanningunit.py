#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from utils import QPlainTextEditLogger
from processing.tools import *
from dialog_lumens_base import DialogLumensBase




class DialogLumensPURPreparePlanningUnit(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensPURPreparePlanningUnit, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS PUR Prepare Planning Unit'
        self.tableRowCount = 0
        self.tableData = []
        
        self.setupUi(self)
        
        self.buttonAddRow.clicked.connect(self.handlerButtonAddRow)
        self.buttonClearAll.clicked.connect(self.handlerButtonClearAll)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def setupUi(self, parent):
        super(DialogLumensPURPreparePlanningUnit, self).setupUi(self)
        
        self.layoutTable = QtGui.QVBoxLayout()
        
        self.dialogLayout.addLayout(self.layoutTable)
        
        layoutButton = QtGui.QHBoxLayout()
        
        self.buttonAddRow = QtGui.QPushButton(parent)
        self.buttonAddRow.setText('Add Row')
        layoutButton.addWidget(self.buttonAddRow)
        
        self.buttonClearAll = QtGui.QPushButton(parent)
        self.buttonClearAll.setText('Clear All')
        layoutButton.addWidget(self.buttonClearAll)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutButton.addWidget(self.buttonLumensDialogSubmit)
        
        self.dialogLayout.addLayout(layoutButton)
        
        self.setLayout(self.dialogLayout)
        
        # add 3 planning unit rows
        self.addRow()
        self.addRow()
        self.addRow()
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(800, 200)
        self.resize(parent.sizeHint())
    
    
    def addRow(self):
        """Add a planning unit row
        """
        self.tableRowCount = self.tableRowCount + 1
        
        layoutRow = QtGui.QHBoxLayout()
        
        lineEditShapefile = QtGui.QLineEdit()
        lineEditShapefile.setReadOnly(True)
        lineEditShapefile.setObjectName('lineEditShapefile_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(lineEditShapefile)
        
        buttonSelectShapefile = QtGui.QPushButton()
        buttonSelectShapefile.setText('Select Shapefile')
        buttonSelectShapefile.setObjectName('buttonSelectShapefile_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(buttonSelectShapefile)
        
        comboBoxShapefileAttr = QtGui.QComboBox()
        comboBoxShapefileAttr.setDisabled(True)
        comboBoxShapefileAttr.setObjectName('comboBoxShapefileAttr_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(comboBoxShapefileAttr)
        
        lineEditPlanningUnitTitle = QtGui.QLineEdit()
        lineEditPlanningUnitTitle.setObjectName('lineEditPlanningUnitTitle_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(lineEditPlanningUnitTitle)
        
        comboBoxPlanningUnitType = QtGui.QComboBox()
        comboBoxPlanningUnitType.addItems(['Reconciliation', 'Additional'])
        comboBoxPlanningUnitType.setObjectName('comboBoxPlanningUnitType_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(comboBoxPlanningUnitType)
        
        self.layoutTable.addLayout(layoutRow)
        
        buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
    
    
    def clearRows(self):
        """
        """
        for i in reversed(range(self.layoutTable.count())): 
            layoutRow = self.layoutTable.itemAt(i).layout()
            self.clearLayout(layoutRow)
        
        self.tableRowCount = 0
        
        self.addRow()
        self.addRow()
        self.addRow()
    
    
    def handlerButtonAddRow(self):
        """
        """
        self.addRow()
    
    
    def handlerButtonClearAll(self):
        """
        """
        self.clearRows()
    
    
    def handlerSelectShapefile(self):
        """Select a shp file and load the attributes in the shapefile attribute combobox
        """
        shapefile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Shapefile', QtCore.QDir.homePath(), 'Shapefile (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if shapefile:
            buttonSender = self.sender()
            objectName = buttonSender.objectName()
            tableRow = objectName.split('_')[1]
            
            lineEditShapefile = self.findChild(QtGui.QLineEdit, 'lineEditShapefile_' + tableRow)
            lineEditShapefile.setText(shapefile)
            
            registry = QgsProviderRegistry.instance()
            provider = registry.provider('ogr', shapefile)
            
            if not provider.isValid():
                logging.getLogger(type(self).__name__).error('invalid shapefile')
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            comboBoxShapefileAttr = self.findChild(QtGui.QComboBox, 'comboBoxShapefileAttr_' + tableRow)
            comboBoxShapefileAttr.clear()
            comboBoxShapefileAttr.addItems(sorted(attributes))
            comboBoxShapefileAttr.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('select shapefile: %s', shapefile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        if self.tableRowCount > 0:
            self.tableData = []
            
            for tableRow in range (1, self.tableRowCount + 1):
                widgetShapefile = self.findChild(QtGui.QLineEdit, 'lineEditShapefile_' + str(tableRow))
                widgetShapefileAttr = self.findChild(QtGui.QComboBox, 'comboBoxShapefileAttr_' + str(tableRow))
                widgetPlanningUnitTitle = self.findChild(QtGui.QLineEdit, 'lineEditPlanningUnitTitle_' + str(tableRow))
                widgetPlanningUnitType = self.findChild(QtGui.QComboBox, 'comboBoxPlanningUnitType_' + str(tableRow))
                
                shapefile = unicode(widgetShapefile.text())
                shapefileAttr = unicode(widgetShapefileAttr.currentText())
                planningUnitTitle = unicode(widgetPlanningUnitTitle.text())
                planningUnitType = unicode(widgetPlanningUnitType.currentText())
                
                if shapefile and shapefileAttr and planningUnitTitle and planningUnitType:
                    if unicode(widgetPlanningUnitType.currentText()) == 'Reconciliation':
                        planningUnitType = 0
                    else:
                        planningUnitType = 1
                    
                    tableRowData = {
                        'shapefile': shapefile,
                        'shapefileAttr': shapefileAttr,
                        'planningUnitTitle': planningUnitTitle,
                        'planningUnitType': planningUnitType,
                    }
                    
                    self.tableData.append(tableRowData)
            
            if self.tableData:
                return True
            else:
                QtGui.QMessageBox.critical(self, 'Error', 'Please complete the fields.')
                return False
        else:
            QtGui.QMessageBox.critical(self, 'Error', 'No planning units set.')
            return False
    
    
    def handlerLumensDialogSubmit(self):
        """
        """
        if self.setAppSettings():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            for tableRowData in self.tableData:
                outputs = general.runalg(
                    'r:purstep2prepareplanningunit',
                    tableRowData['shapefile'],
                    tableRowData['shapefileAttr'],
                    tableRowData['planningUnitTitle'],
                    tableRowData['planningUnitType'],
                )
            
            print self.tableData
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            self.close()
            