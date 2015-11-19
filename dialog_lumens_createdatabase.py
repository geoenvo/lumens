#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_base import DialogLumensBase


class DialogLumensCreateDatabase(DialogLumensBase):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensCreateDatabase, self).__init__(parent)
        
        self.dialogTitle = 'LUMENS Create Database'
        
        self.main.appSettings['DialogLumensCreateDatabase']['outputFolder'] = os.path.join(self.main.appSettings['appDir'], 'output')
        
        self.setupUi(self)
        
        self.buttonSelectOutputFolder.clicked.connect(self.handlerSelectOutputFolder)
        self.buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
        self.buttonLumensDialogSubmit.clicked.connect(self.handlerLumensDialogSubmit)
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensCreateDatabase, self).showEvent(event)
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
            
            self.comboBoxShapefileAttr.clear()
            self.comboBoxShapefileAttr.addItems(sorted(attributes))
            self.comboBoxShapefileAttr.setEnabled(True)
    
    
    def setupUi(self, parent):
        super(DialogLumensCreateDatabase, self).setupUi(self)
        
        layoutLumensDialog = QtGui.QGridLayout()
        
        self.labelProjectName = QtGui.QLabel(parent)
        self.labelProjectName.setText('Project &name:')
        layoutLumensDialog.addWidget(self.labelProjectName, 0, 0)
        
        self.lineEditProjectName = QtGui.QLineEdit(parent)
        self.lineEditProjectName.setText('project_name')
        layoutLumensDialog.addWidget(self.lineEditProjectName, 0, 1)
        
        self.labelProjectName.setBuddy(self.lineEditProjectName)
        
        self.labelOutputFolder = QtGui.QLabel(parent)
        self.labelOutputFolder.setText('Output folder:')
        layoutLumensDialog.addWidget(self.labelOutputFolder, 1, 0)
        
        self.lineEditOutputFolder = QtGui.QLineEdit(parent)
        self.lineEditOutputFolder.setReadOnly(True)
        self.lineEditOutputFolder.setText(self.main.appSettings['DialogLumensCreateDatabase']['outputFolder'])
        layoutLumensDialog.addWidget(self.lineEditOutputFolder, 1, 1)
        
        self.buttonSelectOutputFolder = QtGui.QPushButton(parent)
        self.buttonSelectOutputFolder.setText('Select &Output Folder')
        layoutLumensDialog.addWidget(self.buttonSelectOutputFolder, 2, 0, 1, 2)
        
        self.labelShapefile = QtGui.QLabel(parent)
        self.labelShapefile.setText('Shapefile:')
        layoutLumensDialog.addWidget(self.labelShapefile, 3, 0)
        
        self.lineEditShapefile = QtGui.QLineEdit(parent)
        self.lineEditShapefile.setReadOnly(True)
        layoutLumensDialog.addWidget(self.lineEditShapefile, 3, 1)
        
        self.buttonSelectShapefile = QtGui.QPushButton(parent)
        self.buttonSelectShapefile.setText('Select &Shapefile')
        layoutLumensDialog.addWidget(self.buttonSelectShapefile, 4, 0, 1, 2)
        
        self.labelShapefileAttr = QtGui.QLabel(parent)
        self.labelShapefileAttr.setText('Shapefile &attribute:')
        layoutLumensDialog.addWidget(self.labelShapefileAttr, 5, 0)
        
        self.comboBoxShapefileAttr = QtGui.QComboBox(parent)
        self.comboBoxShapefileAttr.setDisabled(True)
        layoutLumensDialog.addWidget(self.comboBoxShapefileAttr, 5, 1)
        
        self.labelShapefileAttr.setBuddy(self.comboBoxShapefileAttr)
        
        self.labelProjectDescription = QtGui.QLabel(parent)
        self.labelProjectDescription.setText('Project &description:')
        layoutLumensDialog.addWidget(self.labelProjectDescription, 6, 0)
        
        self.lineEditProjectDescription = QtGui.QLineEdit(parent)
        self.lineEditProjectDescription.setText('description')
        layoutLumensDialog.addWidget(self.lineEditProjectDescription, 6, 1)
        
        self.labelProjectDescription.setBuddy(self.lineEditProjectDescription)
        
        self.labelProjectLocation = QtGui.QLabel(parent)
        self.labelProjectLocation.setText('Project &location:')
        layoutLumensDialog.addWidget(self.labelProjectLocation, 7, 0)
        
        self.lineEditProjectLocation = QtGui.QLineEdit(parent)
        self.lineEditProjectLocation.setText('location')
        layoutLumensDialog.addWidget(self.lineEditProjectLocation, 7, 1)
        
        self.labelProjectLocation.setBuddy(self.lineEditProjectLocation)
        
        self.labelProjectProvince = QtGui.QLabel(parent)
        self.labelProjectProvince.setText('Project &province:')
        layoutLumensDialog.addWidget(self.labelProjectProvince, 8, 0)
        
        self.lineEditProjectProvince = QtGui.QLineEdit(parent)
        self.lineEditProjectProvince.setText('province')
        layoutLumensDialog.addWidget(self.lineEditProjectProvince, 8, 1)
        
        self.labelProjectProvince.setBuddy(self.lineEditProjectProvince)
        
        self.labelProjectCountry = QtGui.QLabel(parent)
        self.labelProjectCountry.setText('Project &country:')
        layoutLumensDialog.addWidget(self.labelProjectCountry, 9, 0)
        
        self.lineEditProjectCountry = QtGui.QLineEdit(parent)
        self.lineEditProjectCountry.setText('country')
        layoutLumensDialog.addWidget(self.lineEditProjectCountry, 9, 1)
        
        self.labelProjectCountry.setBuddy(self.lineEditProjectCountry)
        
        self.labelProjectSpatialRes = QtGui.QLabel(parent)
        self.labelProjectSpatialRes.setText('Project spatial &res:')
        layoutLumensDialog.addWidget(self.labelProjectSpatialRes, 10, 0)
        
        self.spinBoxProjectSpatialRes = QtGui.QSpinBox(parent)
        self.spinBoxProjectSpatialRes.setRange(1, 9999)
        self.spinBoxProjectSpatialRes.setValue(100)
        layoutLumensDialog.addWidget(self.spinBoxProjectSpatialRes, 10, 1)
        
        self.labelProjectSpatialRes.setBuddy(self.spinBoxProjectSpatialRes)
        
        self.buttonLumensDialogSubmit = QtGui.QPushButton(parent)
        self.buttonLumensDialogSubmit.setText(self.dialogTitle)
        layoutLumensDialog.addWidget(self.buttonLumensDialogSubmit, 11, 0, 1, 2)
        
        self.dialogLayout.addLayout(layoutLumensDialog)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 400)
        self.resize(parent.sizeHint())
    
    
    def handlerSelectOutputFolder(self):
        """Select a folder as output dir
        """
        outputFolder = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Output Folder'))
        
        if outputFolder:
            self.lineEditOutputFolder.setText(outputFolder)
            
            logging.getLogger(type(self).__name__).info('select output folder: %s', outputFolder)
    
    
    def handlerSelectShapefile(self):
        """Select a shp file and load the attributes in the shapefile attribute combobox
        """
        shapefile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Shapefile', QtCore.QDir.homePath(), 'Shapefile (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if shapefile:
            self.lineEditShapefile.setText(shapefile)
            
            registry = QgsProviderRegistry.instance()
            provider = registry.provider('ogr', shapefile)
            
            if not provider.isValid():
                logging.getLogger(type(self).__name__).error('invalid shapefile')
                
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            self.comboBoxShapefileAttr.clear()
            self.comboBoxShapefileAttr.addItems(sorted(attributes))
            self.comboBoxShapefileAttr.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('select shapefile: %s', shapefile)
    
    
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['projectName'] = unicode(self.lineEditProjectName.text())
        # BUG? outputFolder path separator must be forward slash
        self.main.appSettings[type(self).__name__]['outputFolder'] = unicode(self.lineEditOutputFolder.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['shapefile'] = unicode(self.lineEditShapefile.text())
        self.main.appSettings[type(self).__name__]['shapefileAttr'] = unicode(self.comboBoxShapefileAttr.currentText())
        self.main.appSettings[type(self).__name__]['projectDescription'] = unicode(self.lineEditProjectDescription.text())
        self.main.appSettings[type(self).__name__]['projectLocation'] = unicode(self.lineEditProjectLocation.text())
        self.main.appSettings[type(self).__name__]['projectProvince'] = unicode(self.lineEditProjectProvince.text())
        self.main.appSettings[type(self).__name__]['projectCountry'] = unicode(self.lineEditProjectCountry.text())
        self.main.appSettings[type(self).__name__]['projectSpatialRes'] = self.spinBoxProjectSpatialRes.value()
    
    
    def handlerLumensDialogSubmit(self):
        """LUMENS Create Database R algorithm
        """
        self.setAppSettings()
        
        if self.validDialogForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonLumensDialogSubmit.setDisabled(True)
            
            outputs = general.runalg(
                'modeler:lumens_create_database',
                self.main.appSettings[type(self).__name__]['projectName'],
                self.main.appSettings[type(self).__name__]['outputFolder'],
                self.main.appSettings[type(self).__name__]['projectDescription'],
                self.main.appSettings[type(self).__name__]['projectLocation'],
                self.main.appSettings[type(self).__name__]['projectProvince'],
                self.main.appSettings[type(self).__name__]['projectCountry'],
                self.main.appSettings[type(self).__name__]['shapefile'],
                self.main.appSettings[type(self).__name__]['shapefileAttr'],
                self.main.appSettings[type(self).__name__]['projectSpatialRes']
            )
            
            self.buttonLumensDialogSubmit.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            lumensDatabase = os.path.join(
                self.main.appSettings[type(self).__name__]['outputFolder'],
                self.main.appSettings[type(self).__name__]['projectName'],
                "{0}{1}".format(self.main.appSettings[type(self).__name__]['projectName'], self.main.appSettings['selectProjectfileExt'])
            )
            
            # if LUMENS database file exists, open it and close dialog
            if os.path.exists(lumensDatabase):
                self.main.lumensOpenDatabase(lumensDatabase)
                self.close()
            else:
                logging.getLogger(type(self).__name__).error('modeler:lumens_create_database failed...')
            