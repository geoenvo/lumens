#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from processing.tools import *
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
        self.tableReferenceMappingData = {}
        self.tablePlanningUnitRowCount = 0
        self.tablePlanningUnitData = []
        
        self.setupUi(self)
        
        self.buttonProcessSetup.clicked.connect(self.handlerProcessSetup)
        # 'Setup reference' buttons
        self.buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
        self.buttonEditReferenceClasses.clicked.connect(self.handlerEditReferenceClasses)
        self.comboBoxShapefileAttribute.currentIndexChanged.connect(self.handlerChangeShapefileAttribute)
        # 'Setup planning unit' buttons
        self.buttonAddPlanningUnitRow.clicked.connect(self.handlerButtonAddPlanningUnitRow)
        self.buttonClearAllPlanningUnits.clicked.connect(self.handlerButtonClearAllPlanningUnits)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        
        self.tabSetup = QtGui.QWidget()
        self.tabReconcile = QtGui.QWidget()
        self.tabResult = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabSetup, 'Setup')
        self.tabWidget.addTab(self.tabReconcile, 'Reconcile')
        self.tabWidget.addTab(self.tabResult, 'Result')
        
        self.layoutTabSetup = QtGui.QVBoxLayout()
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
        self.layoutGroupBoxSetupReference.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxSetupReference.setLayout(self.layoutGroupBoxSetupReference)
        self.layoutSetupReferenceInfo = QtGui.QVBoxLayout()
        self.layoutSetupReferenceOptions = QtGui.QGridLayout()
        self.layoutGroupBoxSetupReference.addLayout(self.layoutSetupReferenceInfo)
        self.layoutGroupBoxSetupReference.addLayout(self.layoutSetupReferenceOptions)
        
        self.labelSetupReferenceInfo = QtGui.QLabel()
        self.labelSetupReferenceInfo.setText('Lorem ipsum dolor sit amet...\n')
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
        self.layoutGroupBoxSetupPlanningUnit.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxSetupPlanningUnit.setLayout(self.layoutGroupBoxSetupPlanningUnit)
        
        self.layoutSetupPlanningUnitInfo = QtGui.QVBoxLayout()
        self.labelSetupPlanningUnitInfo = QtGui.QLabel()
        self.labelSetupPlanningUnitInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutSetupPlanningUnitInfo.addWidget(self.labelSetupPlanningUnitInfo)
        
        self.layoutButtonSetupPlanningUnit = QtGui.QHBoxLayout()
        self.layoutButtonSetupPlanningUnit.setContentsMargins(0, 0, 0, 0)
        self.layoutButtonSetupPlanningUnit.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.buttonAddPlanningUnitRow = QtGui.QPushButton()
        self.buttonAddPlanningUnitRow.setText('Add Planning Unit')
        self.buttonAddPlanningUnitRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonSetupPlanningUnit.addWidget(self.buttonAddPlanningUnitRow)
        self.buttonClearAllPlanningUnits = QtGui.QPushButton()
        self.buttonClearAllPlanningUnits.setText('Clear All')
        self.buttonClearAllPlanningUnits.setVisible(False) # BUG, hide it
        self.buttonClearAllPlanningUnits.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonSetupPlanningUnit.addWidget(self.buttonClearAllPlanningUnits)
        
        self.layoutContentGroupBoxSetupPlanningUnit = QtGui.QVBoxLayout()
        self.layoutContentGroupBoxSetupPlanningUnit.setContentsMargins(5, 5, 5, 5)
        self.contentGroupBoxSetupPlanningUnit = QtGui.QWidget()
        self.contentGroupBoxSetupPlanningUnit.setLayout(self.layoutContentGroupBoxSetupPlanningUnit)
        self.scrollSetupPlanningUnit = QtGui.QScrollArea()
        ##self.scrollSetupPlanningUnit.setStyleSheet('QScrollArea > QWidget > QWidget { background: white; }')
        self.scrollSetupPlanningUnit.setWidgetResizable(True);
        self.scrollSetupPlanningUnit.setWidget(self.contentGroupBoxSetupPlanningUnit)
        
        self.layoutGroupBoxSetupPlanningUnit.addLayout(self.layoutSetupPlanningUnitInfo)
        self.layoutGroupBoxSetupPlanningUnit.addLayout(self.layoutButtonSetupPlanningUnit)
        self.layoutGroupBoxSetupPlanningUnit.addWidget(self.scrollSetupPlanningUnit)
        
        self.layoutTablePlanningUnit = QtGui.QVBoxLayout()
        self.layoutTablePlanningUnit.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentGroupBoxSetupPlanningUnit.addLayout(self.layoutTablePlanningUnit)
        
        # Create 3 default planning units
        self.addPlanningUnitRow()
        self.addPlanningUnitRow()
        self.addPlanningUnitRow()
        
        # Process tab button
        self.layoutButtonSetup = QtGui.QHBoxLayout()
        self.buttonProcessSetup = QtGui.QPushButton()
        self.buttonProcessSetup.setText('&Process')
        self.layoutButtonSetup.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonSetup.addWidget(self.buttonProcessSetup)
        
        self.layoutTabSetup.addWidget(self.groupBoxSetupReference)
        self.layoutTabSetup.addWidget(self.groupBoxSetupPlanningUnit)
        self.layoutTabSetup.addLayout(self.layoutButtonSetup)
        
        self.tabSetup.setLayout(self.layoutTabSetup)
        
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
        self.setMinimumSize(700, 480)
        self.resize(parent.sizeHint())
    
    
    def populateTableReferenceMapping(self, shapefileAttribute):
        """Populate the reference mapping table from the selected shapefile attribute
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
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensPUR, self).showEvent(event)
        self.loadSelectedVectorLayer()
    
    
    def loadSelectedVectorLayer(self):
        """Load the attributes of the selected layer into the shapefile attribute combobox
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
    
    
    def addPlanningUnitRow(self):
        """Add a planning unit table row
        """
        self.tablePlanningUnitRowCount = self.tablePlanningUnitRowCount + 1
        
        layoutRow = QtGui.QHBoxLayout()
        
        buttonDeleteShapefile = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionClear.png')
        buttonDeleteShapefile.setIcon(icon)
        buttonDeleteShapefile.setObjectName('buttonDeleteShapefile_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(buttonDeleteShapefile)
        
        lineEditShapefile = QtGui.QLineEdit()
        lineEditShapefile.setReadOnly(True)
        lineEditShapefile.setObjectName('lineEditShapefile_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(lineEditShapefile)
        
        buttonSelectShapefile = QtGui.QPushButton()
        buttonSelectShapefile.setText('Select Shapefile')
        buttonSelectShapefile.setObjectName('buttonSelectShapefile_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(buttonSelectShapefile)
        
        comboBoxShapefileAttribute = QtGui.QComboBox()
        comboBoxShapefileAttribute.setDisabled(True)
        comboBoxShapefileAttribute.setObjectName('comboBoxShapefileAttribute_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(comboBoxShapefileAttribute)
        
        lineEditPlanningUnitTitle = QtGui.QLineEdit()
        lineEditPlanningUnitTitle.setText('planning unit title')
        lineEditPlanningUnitTitle.setObjectName('lineEditPlanningUnitTitle_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(lineEditPlanningUnitTitle)
        
        comboBoxReferenceClasses = QtGui.QComboBox()
        for key, val in self.referenceClasses.iteritems():
            comboBoxReferenceClasses.addItem(val, key)
        comboBoxReferenceClasses.setObjectName('comboBoxReferenceClasses_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(comboBoxReferenceClasses)
        
        comboBoxPlanningUnitType = QtGui.QComboBox()
        comboBoxPlanningUnitType.addItems(['Reconciliation', 'Additional'])
        comboBoxPlanningUnitType.setObjectName('comboBoxPlanningUnitType_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(comboBoxPlanningUnitType)
        
        self.layoutTablePlanningUnit.addLayout(layoutRow)
        
        buttonSelectShapefile.clicked.connect(self.handlerSelectPlanningUnitShapefile)
        buttonDeleteShapefile.clicked.connect(self.handlerDeletePlanningUnitShapefile)
    
    
    def clearPlanningUnitRows(self):
        """BUG: handlerDeletePlanningUnitShapefile() cannot be triggered after calling clearRow()
        """
        for i in reversed(range(self.layoutTablePlanningUnit.count())): 
            layoutRow = self.layoutTablePlanningUnit.itemAt(i).layout()
            self.clearLayout(layoutRow)
        
        self.tablePlanningUnitRowCount = 0
        
        self.addPlanningUnitRow()
        self.addPlanningUnitRow()
        self.addPlanningUnitRow()
    
    
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
        """Reload the Reference Classes comboboxes with the new values
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
    
    
    def setAppSettings(self):
        """
        """
        # 'Setup reference' GroupBox values
        self.main.appSettings[type(self).__name__]['shapefile'] = unicode(self.lineEditShapefile.text())
        self.main.appSettings[type(self).__name__]['shapefileAttr'] = unicode(self.comboBoxShapefileAttribute.currentText())
        self.main.appSettings[type(self).__name__]['dataTitle'] = unicode(self.lineEditDataTitle.text())
        self.main.appSettings[type(self).__name__]['referenceClasses'] = self.referenceClasses
        
        self.tableReferenceMappingData = {}
        for tableRow in range(0, self.tableReferenceMapping.rowCount()):
            attributeValue = self.tableReferenceMapping.item(tableRow, 0).text()
            comboBoxReferenceClasses = self.tableReferenceMapping.cellWidget(tableRow, 1)
            referenceClassID = comboBoxReferenceClasses.itemData(comboBoxReferenceClasses.currentIndex())
            self.tableReferenceMappingData[attributeValue] = referenceClassID
        
        self.main.appSettings[type(self).__name__]['referenceMapping'] = self.tableReferenceMappingData
        
        # 'Setup planning unit' GroupBox values
        self.tablePlanningUnitData = []
        for tableRow in range(1, self.tablePlanningUnitRowCount + 1):
            lineEditShapefile = self.findChild(QtGui.QLineEdit, 'lineEditShapefile_' + str(tableRow))
            
            if not lineEditShapefile: # Row has been deleted
                print 'DEBUG: skipping a deleted row.'
                continue
            
            comboBoxShapefileAttribute = self.findChild(QtGui.QComboBox, 'comboBoxShapefileAttribute_' + str(tableRow))
            lineEditPlanningUnitTitle = self.findChild(QtGui.QLineEdit, 'lineEditPlanningUnitTitle_' + str(tableRow))
            comboBoxReferenceClasses = self.findChild(QtGui.QComboBox, 'comboBoxReferenceClasses_' + str(tableRow))
            comboBoxPlanningUnitType = self.findChild(QtGui.QComboBox, 'comboBoxPlanningUnitType_' + str(tableRow))
            
            shapefile = unicode(lineEditShapefile.text())
            shapefileAttr = unicode(comboBoxShapefileAttribute.currentText())
            planningUnitTitle = unicode(lineEditPlanningUnitTitle.text())
            referenceClassID = comboBoxReferenceClasses.itemData(comboBoxReferenceClasses.currentIndex())
            planningUnitType = unicode(comboBoxPlanningUnitType.currentText())
            
            if shapefile and shapefileAttr and planningUnitTitle and referenceClassID and planningUnitType:
                if planningUnitType == 'Reconciliation':
                    planningUnitType = 0
                else:
                    planningUnitType = 1
                
                tableRowData = {
                    'shapefile': shapefile,
                    'shapefileAttr': shapefileAttr,
                    'planningUnitTitle': planningUnitTitle,
                    'referenceClassID': referenceClassID,
                    'planningUnitType': planningUnitType,
                }
                
                self.tablePlanningUnitData.append(tableRowData)
            else:
                print 'DEBUG: ERROR incomplete planning unit details.'
        
        self.main.appSettings[type(self).__name__]['planningUnits'] = self.tablePlanningUnitData
        
        print 'DEBUG: appSettings["DialogLumensPUR"]'
        print self.main.appSettings[type(self).__name__]
        
    
    def handlerButtonAddPlanningUnitRow(self):
        """
        """
        self.addPlanningUnitRow()
    
    
    def handlerButtonClearAllPlanningUnits(self):
        """
        """
        self.clearPlanningUnitRows()
    
    
    def handlerSelectPlanningUnitShapefile(self):
        """
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Shapefile', QtCore.QDir.homePath(), 'Shapefile (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if file:
            self.lineEditShapefile.setText(file)
            
            buttonSender = self.sender()
            objectName = buttonSender.objectName()
            tableRow = objectName.split('_')[1]
            
            lineEditShapefile = self.contentGroupBoxSetupPlanningUnit.findChild(QtGui.QLineEdit, 'lineEditShapefile_' + tableRow)
            lineEditShapefile.setText(file)
            
            registry = QgsProviderRegistry.instance()
            provider = registry.provider('ogr', file)
            
            if not provider.isValid():
                logging.getLogger(type(self).__name__).error('invalid shapefile')
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            comboBoxShapefileAttribute = self.contentGroupBoxSetupPlanningUnit.findChild(QtGui.QComboBox, 'comboBoxShapefileAttribute_' + tableRow)
            comboBoxShapefileAttribute.clear()
            comboBoxShapefileAttribute.addItems(sorted(attributes))
            comboBoxShapefileAttribute.setEnabled(True)
    
    
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
        
    
    def handlerProcessSetup(self):
        """
        """
        self.setAppSettings()
    