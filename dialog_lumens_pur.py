#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from processing.tools import *
from PyQt4 import QtCore, QtGui


class DialogLumensPUR(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensPUR, self).__init__(parent)
        print 'debug: DialogLumensPUR init'
        
        self.main = parent
        self.dialogTitle = 'LUMENS Planning Unit Reconciliation'
        self.defaultReferenceClasses = {
            10: 'Conservation',
            20: 'Production',
            30: 'Other',
        }
        
        
        self.setupUi(self)
        
        self.buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
    
    
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
        self.layoutSetupReferenceOptions = QtGui.QGridLayout()
        self.layoutGroupBoxSetupReference.addLayout(self.layoutSetupReferenceOptions)
        self.layoutContentSetupReferenceMapping = QtGui.QVBoxLayout()
        self.contentSetupReferenceMapping = QtGui.QWidget()
        self.contentSetupReferenceMapping.setLayout(self.layoutContentSetupReferenceMapping)
        self.scrollSetupReferenceMapping = QtGui.QScrollArea()
        self.scrollSetupReferenceMapping.setWidget(self.contentSetupReferenceMapping)
        self.layoutGroupBoxSetupReference.addWidget(self.scrollSetupReferenceMapping)
        
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
        
        # 'Setup planning unit' GroupBox
        self.layoutContentGroupBoxSetupPlanningUnit = QtGui.QVBoxLayout()
        self.contentGroupBoxSetupPlanningUnit = QtGui.QWidget()
        self.contentGroupBoxSetupPlanningUnit.setLayout(self.layoutContentGroupBoxSetupPlanningUnit)
        self.scrollSetupPlanningUnit = QtGui.QScrollArea()
        self.scrollSetupPlanningUnit.setWidget(self.contentGroupBoxSetupPlanningUnit)
        
        self.groupBoxSetupPlanningUnit = QtGui.QGroupBox('Setup planning unit')
        self.layoutGroupBoxSetupPlanningUnit = QtGui.QVBoxLayout()
        self.layoutGroupBoxSetupPlanningUnit.addWidget(self.scrollSetupPlanningUnit)
        self.groupBoxSetupPlanningUnit.setLayout(self.layoutGroupBoxSetupPlanningUnit)
        
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
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())
    
    
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
        