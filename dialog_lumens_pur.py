#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
"""
from qgis.core import *
from processing.tools import *
"""
from PyQt4 import QtCore, QtGui
from dialog_lumens_pur_referenceclasses import DialogLumensPURReferenceClasses
import resource


class DialogLumensPUR(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensPUR, self).__init__(parent)
        print 'DEBUG: DialogLumensPUR init'
        
        self.main = parent
        self.dialogTitle = 'LUMENS Planning Unit Reconciliation'
        self.referenceClasses = {
            1: 'Conservation',
            2: 'Production',
            3: 'Other',
        }
        self.tableRowCount = 0 # Planning Unit table row count
        
        self.setupUi(self)
        
        # 'Setup reference' buttons
        self.buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
        self.buttonEditReferenceClasses.clicked.connect(self.handlerEditReferenceClasses)
        self.comboBoxShapefileAttribute.currentIndexChanged.connect(self.handlerChangeShapefileAttribute)
        # 'Setup planning unit' buttons
        self.buttonAddRow.clicked.connect(self.handlerButtonAddRow)
        self.buttonClearAll.clicked.connect(self.handlerButtonClearAll)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabCreateReferenceData = QtGui.QWidget()
        self.tabReconcile = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabCreateReferenceData, 'Create reference data')
        self.tabWidget.addTab(self.tabReconcile, 'Reconcile')
        self.tabWidget.addTab(self.tabResult, 'Result')
        
        self.layoutTabCreateReferenceData = QtGui.QVBoxLayout()
        self.layoutTabReconcile = QtGui.QVBoxLayout()
        self.layoutTabResult = QtGui.QVBoxLayout()
        
        self.dialogLayout.addWidget(self.tabWidget)
        ##self.dialogLayout.setContentsMargins(10, 10, 10, 10)
        
        #***********************************************************
        # Setup 'Create reference data' tab
        #***********************************************************
        
        # 'Setup reference' GroupBox
        self.groupBoxSetupReference = QtGui.QGroupBox('Setup reference')
        self.layoutGroupBoxSetupReference = QtGui.QVBoxLayout()
        self.groupBoxSetupReference.setLayout(self.layoutGroupBoxSetupReference)
        self.layoutSetupReferenceInfo = QtGui.QVBoxLayout()
        self.layoutSetupReferenceOptions = QtGui.QGridLayout()
        self.layoutGroupBoxSetupReference.addLayout(self.layoutSetupReferenceInfo)
        self.layoutGroupBoxSetupReference.addLayout(self.layoutSetupReferenceOptions)
        
        self.labelSetupReferenceInfo = QtGui.QLabel()
        self.labelSetupReferenceInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutSetupReferenceInfo.addWidget(self.labelSetupReferenceInfo)
        self.labelShapefile = QtGui.QLabel()
        self.labelShapefile.setText('Reference data:')
        self.layoutSetupReferenceOptions.addWidget(self.labelShapefile, 0, 0)
        self.lineEditShapefile = QtGui.QLineEdit()
        self.lineEditShapefile.setReadOnly(True)
        self.layoutSetupReferenceOptions.addWidget(self.lineEditShapefile, 0, 1)
        self.buttonSelectShapefile = QtGui.QPushButton()
        self.buttonSelectShapefile.setText('&Browse')
        self.layoutSetupReferenceOptions.addWidget(self.buttonSelectShapefile, 0, 2)
        self.labelReferenceClasses = QtGui.QLabel()
        self.labelReferenceClasses.setText('Reference classes:')
        self.layoutSetupReferenceOptions.addWidget(self.labelReferenceClasses, 1, 0)
        self.buttonEditReferenceClasses = QtGui.QPushButton()
        self.buttonEditReferenceClasses.setText('Edit Classes')
        self.buttonEditReferenceClasses.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutSetupReferenceOptions.addWidget(self.buttonEditReferenceClasses, 1, 1)
        self.labelShapefileAttribute = QtGui.QLabel()
        self.labelShapefileAttribute.setText('Reference &attribute:')
        self.layoutSetupReferenceOptions.addWidget(self.labelShapefileAttribute, 2, 0)
        self.comboBoxShapefileAttribute = QtGui.QComboBox()
        self.comboBoxShapefileAttribute.setDisabled(True)
        self.layoutSetupReferenceOptions.addWidget(self.comboBoxShapefileAttribute, 2, 1)
        self.labelShapefileAttribute.setBuddy(self.comboBoxShapefileAttribute)
        self.labelDataTitle = QtGui.QLabel()
        self.labelDataTitle.setText('Data &title:')
        self.layoutSetupReferenceOptions.addWidget(self.labelDataTitle, 3, 0)
        self.lineEditDataTitle = QtGui.QLineEdit()
        self.lineEditDataTitle.setText('title')
        self.layoutSetupReferenceOptions.addWidget(self.lineEditDataTitle, 3, 1)
        self.labelDataTitle.setBuddy(self.lineEditDataTitle)
        
        self.tableReferenceMapping = QtGui.QTableWidget()
        self.tableReferenceMapping.setRowCount(20)
        self.tableReferenceMapping.setColumnCount(2)
        self.tableReferenceMapping.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableReferenceMapping.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableReferenceMapping.verticalHeader().setVisible(False)
        self.tableReferenceMapping.setHorizontalHeaderLabels(['Attribute value', 'Reference class'])
        self.tableReferenceMapping.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        
        attribute = QtGui.QTableWidgetItem('ATTRIBUTE_VALUE')
        comboBoxReferenceClasses = QtGui.QComboBox()
        
        for key, val in self.referenceClasses.iteritems():
            comboBoxReferenceClasses.addItem(val, key)
        
        self.tableReferenceMapping.setItem(0, 0, attribute)
        self.tableReferenceMapping.setCellWidget(0, 1, comboBoxReferenceClasses)
        self.layoutGroupBoxSetupReference.addWidget(self.tableReferenceMapping)
        
        #######################################################################
        
        # 'Setup planning unit' GroupBox
        self.groupBoxSetupPlanningUnit = QtGui.QGroupBox('Setup planning unit')
        self.layoutGroupBoxSetupPlanningUnit = QtGui.QVBoxLayout()
        self.groupBoxSetupPlanningUnit.setLayout(self.layoutGroupBoxSetupPlanningUnit)
        
        self.contentButtonSetupPlanningUnit = QtGui.QWidget()
        ##self.contentButtonSetupPlanningUnit.setFixedHeight(25)
        self.layoutButtonSetupPlanningUnit = QtGui.QHBoxLayout()
        self.layoutButtonSetupPlanningUnit.setContentsMargins(0,0,0,0)
        self.contentButtonSetupPlanningUnit.setLayout(self.layoutButtonSetupPlanningUnit)
        self.layoutButtonSetupPlanningUnit.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.buttonAddRow = QtGui.QPushButton()
        self.buttonAddRow.setText('Add Planning Unit')
        self.buttonAddRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonSetupPlanningUnit.addWidget(self.buttonAddRow)
        self.buttonClearAll = QtGui.QPushButton()
        self.buttonClearAll.setText('Clear All')
        self.buttonClearAll.setVisible(False) # BUGGY
        self.buttonClearAll.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonSetupPlanningUnit.addWidget(self.buttonClearAll)
        ##self.layoutContentGroupBoxSetupPlanningUnit.addWidget(self.contentButtonSetupPlanningUnit)
        
        self.layoutContentGroupBoxSetupPlanningUnit = QtGui.QVBoxLayout()
        self.layoutContentGroupBoxSetupPlanningUnit.setContentsMargins(5, 5, 5, 5)
        self.contentGroupBoxSetupPlanningUnit = QtGui.QWidget()
        self.contentGroupBoxSetupPlanningUnit.setLayout(self.layoutContentGroupBoxSetupPlanningUnit)
        self.scrollSetupPlanningUnit = QtGui.QScrollArea()
        ##self.scrollSetupPlanningUnit.setStyleSheet('QScrollArea > QWidget > QWidget { background: white; }')
        self.scrollSetupPlanningUnit.setWidgetResizable(True);
        self.scrollSetupPlanningUnit.setWidget(self.contentGroupBoxSetupPlanningUnit)
        self.layoutSetupPlanningUnitInfo = QtGui.QVBoxLayout()
        self.labelSetupPlanningUnitInfo = QtGui.QLabel()
        self.labelSetupPlanningUnitInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutSetupPlanningUnitInfo.addWidget(self.labelSetupPlanningUnitInfo)
        
        self.layoutGroupBoxSetupPlanningUnit.addLayout(self.layoutSetupPlanningUnitInfo)
        self.layoutGroupBoxSetupPlanningUnit.addWidget(self.contentButtonSetupPlanningUnit)
        self.layoutGroupBoxSetupPlanningUnit.addWidget(self.scrollSetupPlanningUnit)
        
        self.layoutTablePlanningUnit = QtGui.QVBoxLayout()
        self.layoutTablePlanningUnit.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentGroupBoxSetupPlanningUnit.addLayout(self.layoutTablePlanningUnit)
        
        self.addRow()
        self.addRow()
        self.addRow()
        
        # Process tab button
        self.layoutButtonCreateReferenceData = QtGui.QHBoxLayout()
        self.buttonProcessCreateReferenceData = QtGui.QPushButton()
        self.buttonProcessCreateReferenceData.setText('&Process')
        self.layoutButtonCreateReferenceData.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonCreateReferenceData.addWidget(self.buttonProcessCreateReferenceData)
        
        self.layoutTabCreateReferenceData.addWidget(self.groupBoxSetupReference)
        self.layoutTabCreateReferenceData.addWidget(self.groupBoxSetupPlanningUnit)
        self.layoutTabCreateReferenceData.addLayout(self.layoutButtonCreateReferenceData)
        
        self.tabCreateReferenceData.setLayout(self.layoutTabCreateReferenceData)
        
        #***********************************************************
        # Setup 'Reconcile' tab
        #***********************************************************
        self.tabReconcile.setLayout(self.layoutTabReconcile)
        
        #***********************************************************
        # Setup 'Result' tab
        #***********************************************************
        self.tabResult.setLayout(self.layoutTabResult)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(680, 480)
        self.resize(parent.sizeHint())
    
    
    def populateTableReferenceMapping(self, shapefileAttribute):
        """Populate the reference mapping table from the selected shapefile attribute
        """
        pass
        """
        registry = QgsProviderRegistry.instance()
        provider = registry.provider('ogr', unicode(self.lineEditShapefile.text()))
        
        if not provider.isValid():
            logging.getLogger(type(self).__name__).error('invalid shapefile')
            return
        
        attributeValues = []
        features = provider.getFeatures()
        
        if features:
            for feature in features:
                attributeValue = str(feature.attribute(shapefileAttribute))
                attributeValues.append(attributeValue)
            
            # Clear the table first
            self.tableReferenceMapping.setRowCount(0)
            self.tableReferenceMapping.setRowCount(len(attributeValues))
            
            row = 0
            for attributeValue in sorted(attributeValues):
                comboboxReferenceClasses = QtGui.QComboBox()
                for key, val in self.referenceClasses.iteritems():
                    comboboxReferenceClasses.addItem(val, key)
                
                self.tableReferenceMapping.setItem(row, 0, QtGui.QTableWidgetItem(attributeValue))
                self.tableReferenceMapping.setCellWidget(row, 1, comboboxReferenceClasses)
                row = row + 1
        """
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensPUR, self).showEvent(event)
        self.loadSelectedVectorLayer()
    
    
    def loadSelectedVectorLayer(self):
        """Load the attributes of the selected layer into the shapefile attribute combobox
        """
        pass
        """
        selectedIndexes = self.main.layerListView.selectedIndexes()
        
        if not selectedIndexes:
            return
        
        layerItemIndex = selectedIndexes[0]
        layerItem = self.main.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        
        if layerItemData['layerType'] == 'vector':
            provider = self.main.qgsLayerList[layerItemData['layer']].dataProvider()
            
            if not provider.isValid():
                logging.getLogger(type(self).__name__).error('invalid shapefile')
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            self.lineEditShapefile.setText(layerItemData['layerFile'])
            
            self.comboBoxShapefileAttribute.clear()
            self.comboBoxShapefileAttribute.addItems(sorted(attributes))
            self.comboBoxShapefileAttribute.setEnabled(True)
        """
    
    
    def addRow(self):
        """Add a planning unit table row
        """
        self.tableRowCount = self.tableRowCount + 1
        
        layoutRow = QtGui.QHBoxLayout()
        
        buttonDeleteShapefile = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionClear.png')
        buttonDeleteShapefile.setIcon(icon)
        buttonDeleteShapefile.setObjectName('buttonDeleteShapefile_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(buttonDeleteShapefile)
        
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
        lineEditPlanningUnitTitle.setText('planning unit title')
        lineEditPlanningUnitTitle.setObjectName('lineEditPlanningUnitTitle_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(lineEditPlanningUnitTitle)
        
        comboBoxReferenceClasses = QtGui.QComboBox()
        for key, val in self.referenceClasses.iteritems():
            comboBoxReferenceClasses.addItem(val, key)
        comboBoxReferenceClasses.setObjectName('comboBoxReferenceClasses_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(comboBoxReferenceClasses)
        
        comboBoxPlanningUnitType = QtGui.QComboBox()
        comboBoxPlanningUnitType.addItems(['Reconciliation', 'Additional'])
        comboBoxPlanningUnitType.setObjectName('comboBoxPlanningUnitType_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(comboBoxPlanningUnitType)
        
        self.layoutTablePlanningUnit.addLayout(layoutRow)
        
        buttonSelectShapefile.clicked.connect(self.handlerSelectPlanningUnitShapefile)
        buttonDeleteShapefile.clicked.connect(self.handlerDeletePlanningUnitShapefile)
    
    
    def clearRows(self):
        """BUG: handlerDeletePlanningUnitShapefile() cannot be triggered after calling clearRow()
        """
        for i in reversed(range(self.layoutTablePlanningUnit.count())): 
            layoutRow = self.layoutTablePlanningUnit.itemAt(i).layout()
            self.clearLayout(layoutRow)
        
        self.tableRowCount = 0
        
        self.addRow()
        self.addRow()
        self.addRow()
    
    
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
    
    
    def updateReferenceClasses(self, newReferenceClasses):
        """
        """
        self.referenceClasses = newReferenceClasses
        
        # Update reference classes in 'Setup reference data' groupbox
        for comboBoxReferenceClasses in self.tableReferenceMapping.findChildren(QtGui.QComboBox):
            comboBoxReferenceClasses.clear()
            for key, val in self.referenceClasses.iteritems():
                comboBoxReferenceClasses.addItem(val, key)
                
        # Update reference classes in 'Setup planning unit' groupbox
        for comboBoxReferenceClasses in self.contentGroupBoxSetupPlanningUnit.findChildren(QtGui.QComboBox):
            if 'comboBoxReferenceClasses' in comboBoxReferenceClasses.objectName():
                comboBoxReferenceClasses.clear()
                for key, val in self.referenceClasses.iteritems():
                    comboBoxReferenceClasses.addItem(val, key)
    
    
    def handlerButtonAddRow(self):
        """
        """
        self.addRow()
    
    
    def handlerButtonClearAll(self):
        """
        """
        self.clearRows()
    
    
    def handlerSelectPlanningUnitShapefile(self):
        """
        """
        pass
    
    
    def handlerDeletePlanningUnitShapefile(self):
        """
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        layoutRow = self.layoutTablePlanningUnit.itemAt(int(tableRow) - 1).layout()
        self.clearLayout(layoutRow)
    
    
    def handlerSelectShapefile(self):
        """Select a shp file and load the attributes in the shapefile attribute combobox
        """
        pass
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Shapefile', QtCore.QDir.homePath(), 'Shapefile (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if file:
            self.lineEditShapefile.setText(file)
            
            registry = QgsProviderRegistry.instance()
            provider = registry.provider('ogr', file)
            
            if not provider.isValid():
                logging.getLogger(type(self).__name__).error('invalid shapefile')
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            self.comboBoxShapefileAttribute.clear()
            self.comboBoxShapefileAttribute.addItems(sorted(attributes))
            self.comboBoxShapefileAttribute.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('select shapefile: %s', file)
        """
    
    
    def handlerChangeShapefileAttribute(self, currentIndex):
        """
        """
        shapefileAttribute = self.comboBoxShapefileAttribute.currentText()
        self.populateTableReferenceMapping(shapefileAttribute)
    
    
    def handlerEditReferenceClasses(self):
        """
        """
        dialog = DialogLumensPURReferenceClasses(self)
        
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.updateReferenceClasses(dialog.getReferenceClasses())
        
    