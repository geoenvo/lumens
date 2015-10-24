#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, logging, subprocess
from qgis.core import *
from qgis.gui import QgsMapCanvas
from PyQt4 import QtGui, QtCore

##QgsApplication([], False, '/tmp')
QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX'], True) # The True value is important
QgsApplication.initQgis()

app = QtGui.QApplication(sys.argv)

splashLabel = QtGui.QLabel('<font color=blue size=72><b>{0}</b></font>'.format('Loading'))
splashLabel.setWindowFlags(QtCore.Qt.SplashScreen|QtCore.Qt.WindowStaysOnTopHint)
splashLabel.show()

# Get an iface object
canvas = QgsMapCanvas()
from processing.tests.qgis_interface import QgisInterface
iface = QgisInterface(canvas) # causes ERROR 4

# Initialize the Processing plugin passing an iface object
from processing.ProcessingPlugin import ProcessingPlugin
plugin = ProcessingPlugin(iface)

##import processing
from processing.core.ProcessingConfig import ProcessingConfig
from processing.core.Processing import Processing
ProcessingConfig.setSettingValue('ACTIVATE_R', True) # R provider is not activated by default
ProcessingConfig.setSettingValue('R_FOLDER', os.environ['RPATH'])
ProcessingConfig.setSettingValue('R_LIBS_USER', os.environ['RLIBS'])
ProcessingConfig.setSettingValue('R_SCRIPTS_FOLDER', os.environ['RSCRIPTS'])
Processing.initialize()
from processing.tools import *

splashLabel.close()

from utils import QPlainTextEditLogger
from dialog_lumens_createdatabase import DialogLumensCreateDatabase
from dialog_lumens_opendatabase import DialogLumensOpenDatabase
from dialog_lumens_importdatabase import DialogLumensImportDatabase
from dialog_lumens_addlandcoverraster import DialogLumensAddLandcoverRaster
from dialog_lumens_addpeat import DialogLumensAddPeat
from dialog_lumens_addfactordata import DialogLumensAddFactorData
from dialog_lumens_addplanningunit import DialogLumensAddPlanningUnit
from dialog_lumens_pur_createreferencedata import DialogLumensPURCreateReferenceData
from dialog_lumens_pur_prepareplanningunit import DialogLumensPURPreparePlanningUnit
from dialog_lumens_preques import DialogLumensPreQUES
from dialog_lumens_preques_trajectory import DialogLumensPreQUESTrajectory
from dialog_lumens_quesc import DialogLumensQUESC
from dialog_lumens_quesc_peat import DialogLumensQUESCPeat
from dialog_lumens_quesc_summarize import DialogLumensQUESCSummarize

__version__ = "0.1.00"




class MainWindow(QtGui.QMainWindow):
    """
    """
    
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.appSettings = {
            'appDir': os.path.dirname(os.path.realpath(__file__)),
            'selectShapefileExt': '.shp',
            'selectRasterfileExt': '.tif',
            'selectCsvfileExt': '.csv',
            'selectProjectfileExt': '.lpj',
            'DialogLumensCreateDatabase': {
                'projectName': '',
                'outputFolder': '',
                'shapefile': '',
                'shapefileAttr': '',
                'projectDescription': '',
                'projectLocation': '',
                'projectProvince': '',
                'projectCountry': '',
                'projectSpatialRes': '',
            },
            'DialogLumensOpenDatabase': {
                'projectFile': '',
                'projectFolder': '',
            },
            'DialogLumensImportDatabase': {
                'workingDir': '',
                'projectFile': '',
            },
            'DialogLumensAddLandcoverRaster': {
                'rasterfile': '',
                'period': '',
                'description': '',
            },
            'DialogLumensAddPeat': {
                'rasterfile': '',
                'description': '',
            },
            'DialogLumensAddFactorData': {
                'rasterfile': '',
                'description': '',
            },
            'DialogLumensAddPlanningUnit': {
                'rasterfile': '',
                'csvfile': '',
                'description': '',
            },
            'DialogLumensPURCreateReferenceData': {
                'shapefile': '',
                'shapefileAttr': '',
                'dataTitle': '',
            },
            'DialogLumensPURPreparePlanningUnit': {
                'shapefile': '',
                'shapefileAttr': '',
                'planningUnitTitle': '',
                'planningUnitType': '',
            },
            'DialogLumensPreQUES': {
                'csvfile': '',
                'option': '',
                'nodata': '',
            },
            'DialogLumensPreQUESTrajectory': {
                'workingDir': '',
                'location': '',
                't1': '',
                't2': '',
                'landCoverT1': '',
                'landCoverT2': '',
                'planningUnit': '',
                'csvLandUse': '',
                'csvPlanningUnit': '',
            },
            'DialogLumensQUESC': {
                'csvfile': '',
                'nodata': '',
            },
            'DialogLumensQUESCPeat': {
                'csvfile': '',
            },
            'DialogLumensQUESCSummarize': {
                'checkbox': '',
            },
        }
        
        self.openDialogs = []
        
        self.setupUi()
        self.installEventFilter(self)
        
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_box.setFormatter(formatter)
        self.logger.addHandler(self.log_box)
        self.logger.setLevel(logging.DEBUG)
        
        self.buttonDialogLumensCreateDatabase.clicked.connect(self.handlerDialogLumensCreateDatabase)
        self.buttonDialogLumensOpenDatabase.clicked.connect(self.handlerDialogLumensOpenDatabase)
        self.buttonDialogLumensImportDatabase.clicked.connect(self.handlerDialogLumensImportDatabase)
        self.buttonLumensOpenDatabase.clicked.connect(self.handlerLumensOpenDatabase)
        self.buttonLumensCloseDatabase.clicked.connect(self.handlerLumensCloseDatabase)
        self.buttonDialogLumensAddLandcoverRaster.clicked.connect(self.handlerDialogLumensAddLandcoverRaster)
        self.buttonDialogLumensAddPeat.clicked.connect(self.handlerDialogLumensAddPeat)
        self.buttonDialogLumensAddFactorData.clicked.connect(self.handlerDialogLumensAddFactorData)
        self.buttonDialogLumensAddPlanningUnit.clicked.connect(self.handlerDialogLumensAddPlanningUnit)
        self.buttonDialogLumensPURCreateReferenceData.clicked.connect(self.handlerDialogLumensPURCreateReferenceData)
        self.buttonDialogLumensPURPreparePlanningUnit.clicked.connect(self.handlerDialogLumensPURPreparePlanningUnit)
        self.buttonDialogLumensPreQUES.clicked.connect(self.handlerDialogLumensPreQUES)
        self.buttonDialogLumensPreQUESTrajectory.clicked.connect(self.handlerDialogLumensPreQUESTrajectory)
        self.buttonDialogLumensQUESC.clicked.connect(self.handlerDialogLumensQUESC)
        self.buttonDialogLumensQUESCPeat.clicked.connect(self.handlerDialogLumensQUESCPeat)
        self.buttonDialogLumensQUESCSummarize.clicked.connect(self.handlerDialogLumensQUESCSummarize)
    
    
    def eventFilter(self, object, event):
        """
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            print "widget window has gained focus"
            if not self.appSettings['DialogLumensOpenDatabase']['projectFile']:
                self.buttonLumensCloseDatabase.setDisabled(True)
                self.buttonDialogLumensAddLandcoverRaster.setDisabled(True)
                self.buttonDialogLumensAddPeat.setDisabled(True)
                self.buttonDialogLumensAddFactorData.setDisabled(True)
                self.buttonDialogLumensAddPlanningUnit.setDisabled(True)
                self.buttonDialogLumensPURCreateReferenceData.setDisabled(True)
                self.buttonDialogLumensPURPreparePlanningUnit.setDisabled(True)
                self.buttonDialogLumensPreQUES.setDisabled(True)
                self.buttonDialogLumensPreQUESTrajectory.setDisabled(True)
                self.buttonDialogLumensQUESC.setDisabled(True)
                self.buttonDialogLumensQUESCPeat.setDisabled(True)
                self.buttonDialogLumensQUESCSummarize.setDisabled(True)
            else:
                self.buttonLumensCloseDatabase.setEnabled(True)
                self.buttonDialogLumensAddLandcoverRaster.setEnabled(True)
                self.buttonDialogLumensAddPeat.setEnabled(True)
                self.buttonDialogLumensAddFactorData.setEnabled(True)
                self.buttonDialogLumensAddPlanningUnit.setEnabled(True)
                self.buttonDialogLumensPURCreateReferenceData.setEnabled(True)
                self.buttonDialogLumensPURPreparePlanningUnit.setEnabled(True)
                self.buttonDialogLumensPreQUES.setEnabled(True)
                self.buttonDialogLumensPreQUESTrajectory.setEnabled(True)
                self.buttonDialogLumensQUESC.setEnabled(True)
                self.buttonDialogLumensQUESCPeat.setEnabled(True)
                self.buttonDialogLumensQUESCSummarize.setEnabled(True)
        elif event.type()== QtCore.QEvent.WindowDeactivate:
            print "widget window has lost focus"
        elif event.type()== QtCore.QEvent.FocusIn:
            print "widget has gained keyboard focus"
        elif event.type()== QtCore.QEvent.FocusOut:
            print "widget has lost keyboard focus"
        
        return False
    
    
    def setupUi(self):
        layout = QtGui.QVBoxLayout()
        
        layoutActiveProject = QtGui.QHBoxLayout()
        self.labelActiveProject = QtGui.QLabel(self)
        self.labelActiveProject.setText('Active project:')
        layoutActiveProject.addWidget(self.labelActiveProject)
        
        self.lineEditActiveProject = QtGui.QLineEdit(self)
        self.lineEditActiveProject.setReadOnly(True)
        layoutActiveProject.addWidget(self.lineEditActiveProject)
        
        layout.addLayout(layoutActiveProject)
        
        self.buttonLumensOpenDatabase = QtGui.QPushButton(self)
        self.buttonLumensOpenDatabase.setText('LUMENS Open Database')
        layout.addWidget(self.buttonLumensOpenDatabase)
        
        self.buttonLumensCloseDatabase = QtGui.QPushButton(self)
        self.buttonLumensCloseDatabase.setText('LUMENS Close Database')
        layout.addWidget(self.buttonLumensCloseDatabase)
        
        self.buttonDialogLumensCreateDatabase = QtGui.QPushButton(self)
        self.buttonDialogLumensCreateDatabase.setText('Dialog: LUMENS Create Database')
        layout.addWidget(self.buttonDialogLumensCreateDatabase)
        
        self.buttonDialogLumensOpenDatabase = QtGui.QPushButton(self)
        self.buttonDialogLumensOpenDatabase.setText('Dialog: LUMENS Open Database')
        layout.addWidget(self.buttonDialogLumensOpenDatabase)
        
        self.buttonDialogLumensImportDatabase = QtGui.QPushButton(self)
        self.buttonDialogLumensImportDatabase.setText('Dialog: LUMENS Import Database')
        layout.addWidget(self.buttonDialogLumensImportDatabase)
        
        self.buttonDialogLumensAddLandcoverRaster = QtGui.QPushButton(self)
        self.buttonDialogLumensAddLandcoverRaster.setText('Dialog: LUMENS Add Land Cover Raster')
        layout.addWidget(self.buttonDialogLumensAddLandcoverRaster)
        
        self.buttonDialogLumensAddPeat = QtGui.QPushButton(self)
        self.buttonDialogLumensAddPeat.setText('Dialog: LUMENS Add Peat')
        layout.addWidget(self.buttonDialogLumensAddPeat)
        
        self.buttonDialogLumensAddFactorData = QtGui.QPushButton(self)
        self.buttonDialogLumensAddFactorData.setText('Dialog: LUMENS Add Factor Data')
        layout.addWidget(self.buttonDialogLumensAddFactorData)
        
        self.buttonDialogLumensAddPlanningUnit = QtGui.QPushButton(self)
        self.buttonDialogLumensAddPlanningUnit.setText('Dialog: LUMENS Add Planning Unit')
        layout.addWidget(self.buttonDialogLumensAddPlanningUnit)
        
        self.buttonDialogLumensPURCreateReferenceData = QtGui.QPushButton(self)
        self.buttonDialogLumensPURCreateReferenceData.setText('Dialog: LUMENS PUR Create Reference Data')
        layout.addWidget(self.buttonDialogLumensPURCreateReferenceData)
        
        self.buttonDialogLumensPURPreparePlanningUnit = QtGui.QPushButton(self)
        self.buttonDialogLumensPURPreparePlanningUnit.setText('Dialog: LUMENS PUR Prepare Planning Unit')
        layout.addWidget(self.buttonDialogLumensPURPreparePlanningUnit)
        
        self.buttonDialogLumensPreQUES = QtGui.QPushButton(self)
        self.buttonDialogLumensPreQUES.setText('Dialog: LUMENS PreQUES')
        layout.addWidget(self.buttonDialogLumensPreQUES)
        
        self.buttonDialogLumensPreQUESTrajectory = QtGui.QPushButton(self)
        self.buttonDialogLumensPreQUESTrajectory.setText('Dialog: LUMENS PreQUES Trajectory')
        layout.addWidget(self.buttonDialogLumensPreQUESTrajectory)
        
        self.buttonDialogLumensQUESC = QtGui.QPushButton(self)
        self.buttonDialogLumensQUESC.setText('Dialog: LUMENS QUES-C')
        layout.addWidget(self.buttonDialogLumensQUESC)
        
        self.buttonDialogLumensQUESCPeat = QtGui.QPushButton(self)
        self.buttonDialogLumensQUESCPeat.setText('Dialog: LUMENS QUES-C Peat')
        layout.addWidget(self.buttonDialogLumensQUESCPeat)
        
        self.buttonDialogLumensQUESCSummarize = QtGui.QPushButton(self)
        self.buttonDialogLumensQUESCSummarize.setText('Dialog: LUMENS QUES-C Summarize Multiple Period')
        layout.addWidget(self.buttonDialogLumensQUESCSummarize)
        
        self.log_box = QPlainTextEditLogger(self)
        layout.addWidget(self.log_box.widget)
        
        contents = QtGui.QWidget()
        contents.setLayout(layout)
        
        self.setCentralWidget(contents)
        self.setWindowTitle('MainWindow')
        self.setMinimumSize(800, 400)
        self.resize(self.sizeHint())
    
    
    def openDialog(self, DialogClass):
        """Keep track of already opened dialog instances instead of creating new ones
        """
        dialog = None
        
        for dlg in self.openDialogs:
            if isinstance(dlg, DialogClass):
                dialog = dlg
                break
        
        if dialog:
            dialog.exec_()
        else:
            dialog = DialogClass(self)
            self.openDialogs.append(dialog)
            dialog.exec_()
    
    
    def handlerDialogLumensCreateDatabase(self):
        """
        """
        self.openDialog(DialogLumensCreateDatabase)
        
        """
        try:
            subprocess.check_call(['rscript', '--version'])
            logging.getLogger(__name__).info('subprocess ended')
        except subprocess.CalledProcessError as e:
            logging.getLogger(__name__).error('subprocess error: %s', e)
        """
    
    
    def handlerDialogLumensOpenDatabase(self):
        """
        """
        self.openDialog(DialogLumensOpenDatabase)
    
    
    def handlerDialogLumensImportDatabase(self):
        """
        """
        self.openDialog(DialogLumensImportDatabase)
    
    
    def handlerLumensOpenDatabase(self):
        """Select a .lpj database file and open it
        """
        lumensDatabase = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select LUMENS Database', QtCore.QDir.homePath(), 'LUMENS Database (*{0})'.format(self.appSettings['selectProjectfileExt'])))
        
        if lumensDatabase:
            logging.getLogger(type(self).__name__).info('select LUMENS database: %s', lumensDatabase)
            
            self.lumensOpenDatabase(lumensDatabase)
    
    
    def handlerLumensCloseDatabase(self):
        """
        """
        self.lumensCloseDatabase()
    
    def handlerDialogLumensAddLandcoverRaster(self):
        """
        """
        self.openDialog(DialogLumensAddLandcoverRaster)
    
    
    def handlerDialogLumensAddPeat(self):
        """
        """
        self.openDialog(DialogLumensAddPeat)
    
    
    def handlerDialogLumensAddFactorData(self):
        """
        """
        self.openDialog(DialogLumensAddFactorData)
    
    
    def handlerDialogLumensAddPlanningUnit(self):
        """
        """
        self.openDialog(DialogLumensAddPlanningUnit)
    
    
    def handlerDialogLumensPURCreateReferenceData(self):
        """
        """
        self.openDialog(DialogLumensPURCreateReferenceData)
    
    
    def handlerDialogLumensPURPreparePlanningUnit(self):
        """
        """
        self.openDialog(DialogLumensPURPreparePlanningUnit)
    
    
    def handlerDialogLumensPreQUES(self):
        """
        """
        self.openDialog(DialogLumensPreQUES)
    
    
    def handlerDialogLumensPreQUESTrajectory(self):
        """
        """
        self.openDialog(DialogLumensPreQUESTrajectory)
    
    
    def handlerDialogLumensQUESC(self):
        """
        """
        self.openDialog(DialogLumensQUESC)
    
    
    def handlerDialogLumensQUESCPeat(self):
        """
        """
        self.openDialog(DialogLumensQUESCPeat)
    
    
    def handlerDialogLumensQUESCSummarize(self):
        """
        """
        self.openDialog(DialogLumensQUESCSummarize)
    
    
    def lumensOpenDatabase(self, lumensDatabase):
        """
        """
        logging.getLogger(__name__).info('start: LUMENS Open Database')
        
        self.buttonLumensOpenDatabase.setDisabled(True)
        
        outputs = general.runalg(
            'modeler:lumens_open_database',
            lumensDatabase,
            None
        )
        
        if outputs:
            #print outputs
            # outputs['overview_ALG0'] => temporary raster file
            
            self.appSettings['DialogLumensOpenDatabase']['projectFile'] = lumensDatabase
            self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = os.path.dirname(lumensDatabase)
            
            self.lineEditActiveProject.setText(lumensDatabase)
            self.buttonLumensCloseDatabase.setEnabled(True)
            self.buttonDialogLumensAddLandcoverRaster.setEnabled(True)
            self.buttonDialogLumensAddPeat.setEnabled(True)
            self.buttonDialogLumensAddFactorData.setEnabled(True)
            self.buttonDialogLumensAddPlanningUnit.setEnabled(True)
            self.buttonDialogLumensPURCreateReferenceData.setEnabled(True)
            self.buttonDialogLumensPURPreparePlanningUnit.setEnabled(True)
            self.buttonDialogLumensPreQUES.setEnabled(True)
            self.buttonDialogLumensPreQUESTrajectory.setEnabled(True)
            self.buttonDialogLumensQUESC.setEnabled(True)
            self.buttonDialogLumensQUESCPeat.setEnabled(True)
            self.buttonDialogLumensQUESCSummarize.setEnabled(True)
        
        self.buttonLumensOpenDatabase.setEnabled(True)
        
        logging.getLogger(__name__).info('end: LUMENS Open Database')
    
    
    def lumensCloseDatabase(self):
        """
        """
        logging.getLogger(__name__).info('start: LUMENS Close Database')
        
        outputs = general.runalg('modeler:lumens_close_database')
        self.appSettings['DialogLumensOpenDatabase']['projectFile'] = ''
        self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = ''
        
        self.lineEditActiveProject.clear()
        self.buttonLumensCloseDatabase.setDisabled(True)
        self.buttonDialogLumensAddLandcoverRaster.setDisabled(True)
        self.buttonDialogLumensAddPeat.setDisabled(True)
        self.buttonDialogLumensAddFactorData.setDisabled(True)
        self.buttonDialogLumensAddPlanningUnit.setDisabled(True)
        self.buttonDialogLumensPURCreateReferenceData.setDisabled(True)
        self.buttonDialogLumensPURPreparePlanningUnit.setDisabled(True)
        self.buttonDialogLumensPreQUES.setDisabled(True)
        self.buttonDialogLumensPreQUESTrajectory.setDisabled(True)
        self.buttonDialogLumensQUESC.setDisabled(True)
        self.buttonDialogLumensQUESCPeat.setDisabled(True)
        self.buttonDialogLumensQUESCSummarize.setDisabled(True)
        
        logging.getLogger(__name__).info('end: LUMENS Close Database')




def main():
    window = MainWindow()
    window.show()
    window.raise_()
    
    app.exec_()
    
    QgsApplication.exitQgis()


if __name__ == "__main__":
    main()
    
    sys.exit(-1)
    