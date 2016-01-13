#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_viewer import DialogLumensViewer


class DialogLumensCreateDatabase(QtGui.QDialog):
    """
    """
    def __init__(self, parent):
        super(DialogLumensCreateDatabase, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS Create Database'
        
        self.main.appSettings['DialogLumensCreateDatabase']['outputFolder'] = os.path.join(self.main.appSettings['appDir'], 'output')
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensCreateDatabase init'
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
        
        self.buttonSelectOutputFolder.clicked.connect(self.handlerSelectOutputFolder)
        self.buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
        self.buttonProcessCreateDatabase.clicked.connect(self.handlerProcessCreateDatabase)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.groupBoxDatabaseDetails = QtGui.QGroupBox('Database details')
        self.layoutGroupBoxDatabaseDetails = QtGui.QVBoxLayout()
        self.layoutGroupBoxDatabaseDetails.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDatabaseDetails.setLayout(self.layoutGroupBoxDatabaseDetails)
        self.layoutDatabaseDetailsInfo = QtGui.QVBoxLayout()
        self.layoutDatabaseDetails = QtGui.QGridLayout()
        self.layoutGroupBoxDatabaseDetails.addLayout(self.layoutDatabaseDetailsInfo)
        self.layoutGroupBoxDatabaseDetails.addLayout(self.layoutDatabaseDetails)
        
        self.labelDatabaseDetailsInfo = QtGui.QLabel()
        self.labelDatabaseDetailsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutDatabaseDetailsInfo.addWidget(self.labelDatabaseDetailsInfo)
        
        self.labelProjectName = QtGui.QLabel()
        self.labelProjectName.setText('Project &name:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectName, 0, 0)
        
        self.lineEditProjectName = QtGui.QLineEdit()
        self.lineEditProjectName.setText('project_name')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectName, 0, 1)
        
        self.labelProjectName.setBuddy(self.lineEditProjectName)
        
        self.labelOutputFolder = QtGui.QLabel()
        self.labelOutputFolder.setText('Output folder:')
        self.layoutDatabaseDetails.addWidget(self.labelOutputFolder, 1, 0)
        
        self.lineEditOutputFolder = QtGui.QLineEdit()
        self.lineEditOutputFolder.setReadOnly(True)
        self.lineEditOutputFolder.setText(self.main.appSettings['DialogLumensCreateDatabase']['outputFolder'])
        self.layoutDatabaseDetails.addWidget(self.lineEditOutputFolder, 1, 1)
        
        self.buttonSelectOutputFolder = QtGui.QPushButton()
        self.buttonSelectOutputFolder.setText('&Browse')
        self.layoutDatabaseDetails.addWidget(self.buttonSelectOutputFolder, 1, 2)
        
        self.labelShapefile = QtGui.QLabel()
        self.labelShapefile.setText('Shapefile:')
        self.layoutDatabaseDetails.addWidget(self.labelShapefile, 2, 0)
        
        self.lineEditShapefile = QtGui.QLineEdit()
        self.lineEditShapefile.setReadOnly(True)
        self.layoutDatabaseDetails.addWidget(self.lineEditShapefile, 2, 1)
        
        self.buttonSelectShapefile = QtGui.QPushButton()
        self.buttonSelectShapefile.setText('&Browse')
        self.layoutDatabaseDetails.addWidget(self.buttonSelectShapefile, 2, 2)
        
        self.labelShapefileAttr = QtGui.QLabel()
        self.labelShapefileAttr.setText('Shapefile &attribute:')
        self.layoutDatabaseDetails.addWidget(self.labelShapefileAttr, 3, 0)
        
        self.comboBoxShapefileAttr = QtGui.QComboBox(parent)
        self.comboBoxShapefileAttr.setDisabled(True)
        self.layoutDatabaseDetails.addWidget(self.comboBoxShapefileAttr, 3, 1)
        
        self.labelShapefileAttr.setBuddy(self.comboBoxShapefileAttr)
        
        self.labelProjectDescription = QtGui.QLabel()
        self.labelProjectDescription.setText('Project &description:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectDescription, 4, 0)
        
        self.lineEditProjectDescription = QtGui.QLineEdit(parent)
        self.lineEditProjectDescription.setText('description')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectDescription, 4, 1)
        
        self.labelProjectDescription.setBuddy(self.lineEditProjectDescription)
        
        self.labelProjectLocation = QtGui.QLabel()
        self.labelProjectLocation.setText('Project &location:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectLocation, 5, 0)
        
        self.lineEditProjectLocation = QtGui.QLineEdit()
        self.lineEditProjectLocation.setText('location')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectLocation, 5, 1)
        
        self.labelProjectLocation.setBuddy(self.lineEditProjectLocation)
        
        self.labelProjectProvince = QtGui.QLabel()
        self.labelProjectProvince.setText('Project &province:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectProvince, 6, 0)
        
        self.lineEditProjectProvince = QtGui.QLineEdit()
        self.lineEditProjectProvince.setText('province')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectProvince, 6, 1)
        
        self.labelProjectProvince.setBuddy(self.lineEditProjectProvince)
        
        self.labelProjectCountry = QtGui.QLabel()
        self.labelProjectCountry.setText('Project &country:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectCountry, 7, 0)
        
        self.lineEditProjectCountry = QtGui.QLineEdit()
        self.lineEditProjectCountry.setText('country')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectCountry, 7, 1)
        
        self.labelProjectCountry.setBuddy(self.lineEditProjectCountry)
        
        self.labelProjectSpatialRes = QtGui.QLabel()
        self.labelProjectSpatialRes.setText('Project spatial &res:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectSpatialRes, 8, 0)
        
        self.spinBoxProjectSpatialRes = QtGui.QSpinBox()
        self.spinBoxProjectSpatialRes.setRange(1, 9999)
        self.spinBoxProjectSpatialRes.setValue(100)
        self.layoutDatabaseDetails.addWidget(self.spinBoxProjectSpatialRes, 8, 1)
        
        self.labelProjectSpatialRes.setBuddy(self.spinBoxProjectSpatialRes)
        
        self.layoutButtonCreateDatabase = QtGui.QHBoxLayout()
        self.buttonProcessCreateDatabase = QtGui.QPushButton()
        self.buttonProcessCreateDatabase.setText('&Process')
        self.layoutButtonCreateDatabase.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonCreateDatabase.addWidget(self.buttonProcessCreateDatabase)
        
        self.dialogLayout.addWidget(self.groupBoxDatabaseDetails)
        self.dialogLayout.addLayout(self.layoutButtonCreateDatabase)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensCreateDatabase, self).showEvent(event)
        self.loadSelectedVectorLayer()
    
    
    def closeEvent(self, event):
        """Called when the widget is closed
        """
        super(DialogLumensCreateDatabase, self).closeEvent(event)
    
    
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
    
    
    #***********************************************************
    # 'Create Database' QPushButton handlers
    #***********************************************************
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
                logging.getLogger(type(self).__name__).error('select shapefile: invalid shapefile')
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            self.comboBoxShapefileAttr.clear()
            self.comboBoxShapefileAttr.addItems(sorted(attributes))
            self.comboBoxShapefileAttr.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('select shapefile: %s', shapefile)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets
        """
        self.main.appSettings[type(self).__name__]['projectName'] = unicode(self.lineEditProjectName.text())
        # BUG in R script execution? outputFolder path separator must be forward slash
        self.main.appSettings[type(self).__name__]['outputFolder'] = unicode(self.lineEditOutputFolder.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['shapefile'] = unicode(self.lineEditShapefile.text())
        self.main.appSettings[type(self).__name__]['shapefileAttr'] = unicode(self.comboBoxShapefileAttr.currentText())
        self.main.appSettings[type(self).__name__]['projectDescription'] = unicode(self.lineEditProjectDescription.text())
        self.main.appSettings[type(self).__name__]['projectLocation'] = unicode(self.lineEditProjectLocation.text())
        self.main.appSettings[type(self).__name__]['projectProvince'] = unicode(self.lineEditProjectProvince.text())
        self.main.appSettings[type(self).__name__]['projectCountry'] = unicode(self.lineEditProjectCountry.text())
        self.main.appSettings[type(self).__name__]['projectSpatialRes'] = self.spinBoxProjectSpatialRes.value()
    
    
    def validForm(self):
        """
        """
        logging.getLogger(type(self).__name__).info('form validate: %s', type(self).__name__)
        logging.getLogger(type(self).__name__).info('form values: %s', self.main.appSettings[type(self).__name__])
        
        valid = True
        
        for key, val in self.main.appSettings[type(self).__name__].iteritems():
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
    
    
    def handlerProcessCreateDatabase(self):
        """LUMENS Create Database R algorithm
        """
        self.setAppSettings()
        
        if self.validForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonProcessCreateDatabase.setDisabled(True)
            
            ### 20160112 new R scripts
            ### 1. modeler:lumens_create_database_1(projectname, outputfolder, projectdescription, projectlocation, projectprovince, projectcountry, shapefile, shapefileattribute, projectspatialresolution)
            ### 2. r:LUMENS_create_database_2(proj.file, p.admin.df)
            ### replaces: modeler:lumens_create_database
            
            """
            ###OBSOLETE
            algName = 'modeler:lumens_create_database'
            
            outputs = general.runalg(
                algName,
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
            """
            
            algName = 'modeler:lumens_create_database_1'
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[type(self).__name__]['projectName'],
                self.main.appSettings[type(self).__name__]['outputFolder'],
                self.main.appSettings[type(self).__name__]['projectDescription'],
                self.main.appSettings[type(self).__name__]['projectLocation'],
                self.main.appSettings[type(self).__name__]['projectProvince'],
                self.main.appSettings[type(self).__name__]['projectCountry'],
                self.main.appSettings[type(self).__name__]['shapefile'],
                self.main.appSettings[type(self).__name__]['shapefileAttr'],
                self.main.appSettings[type(self).__name__]['projectSpatialRes'],
                None,
            )
            
            # Construct the project .lpj filepath
            lumensDatabase = os.path.join(
                self.main.appSettings[type(self).__name__]['outputFolder'],
                self.main.appSettings[type(self).__name__]['projectName'],
                "{0}{1}".format(self.main.appSettings[type(self).__name__]['projectName'], self.main.appSettings['selectProjectfileExt'])
            )
            
            algName = 'r:lumenscreatedatabase2'
            
            if outputs and outputs['p.admin.df_ALG2']:
                dialog = DialogLumensViewer(self, 'Attribute Table', 'csv', outputs['p.admin.df_ALG2'], True)
                dialog.exec_()
                
                # Create a temp csv file from the csv dialog
                tableData = dialog.getTableData()
                tableCsv = dialog.getTableCsv(tableData)
                
                outputs = general.runalg(
                    algName,
                    lumensDatabase,
                    tableCsv,
                )
            
            self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessCreateDatabase.setEnabled(True)
            
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            # If LUMENS database file exists, open it and close this dialog
            if os.path.exists(lumensDatabase):
                self.main.lumensOpenDatabase(lumensDatabase)
                self.close()
            else:
                logging.getLogger(type(self).__name__).error('modeler:lumens_create_database failed...')
            