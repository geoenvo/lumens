#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, logging, subprocess, argparse

from qgis.core import *
from qgis.gui import *
from PyQt4 import QtGui, QtCore

import resource

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

from utils import QPlainTextEditLogger, DetailedMessageBox
from dialog_layer_attribute_table import DialogLayerAttributeTable
from dialog_feature_selectexpression import DialogFeatureSelectExpression
from dialog_layer_attribute_dualview import DialogLayerAttributeDualView

from dialog_lumens_createdatabase import DialogLumensCreateDatabase
from dialog_lumens_opendatabase import DialogLumensOpenDatabase
from dialog_lumens_importdatabase import DialogLumensImportDatabase
from dialog_lumens_addlandcoverraster import DialogLumensAddLandcoverRaster
from dialog_lumens_addpeatdata import DialogLumensAddPeatData
from dialog_lumens_addfactordata import DialogLumensAddFactorData
from dialog_lumens_addplanningunitdata import DialogLumensAddPlanningUnitData
from dialog_lumens_pur_createreferencedata import DialogLumensPURCreateReferenceData
from dialog_lumens_pur_prepareplanningunit import DialogLumensPURPreparePlanningUnit
from dialog_lumens_pur_reconcileplanningunit import DialogLumensPURReconcilePlanningUnit
from dialog_lumens_pur_finalization import DialogLumensPURFinalization
from dialog_lumens_preques_landcoverchangeanalysis import DialogLumensPreQUESLandcoverChangeAnalysis
from dialog_lumens_preques_landcovertrajectoriesanalysis import DialogLumensPreQUESLandcoverTrajectoriesAnalysis
from dialog_lumens_quesc_carbonaccounting import DialogLumensQUESCCarbonAccounting
from dialog_lumens_quesc_peatlandcarbonaccounting import DialogLumensQUESCPeatlandCarbonAccounting
from dialog_lumens_quesc_summarizemultipleperiod import DialogLumensQUESCSummarizeMultiplePeriod
from dialog_lumens_quesb_analysis import DialogLumensQUESBAnalysis
from dialog_lumens_ta_abacusopportunitycost import DialogLumensTAAbacusOpportunityCost
from dialog_lumens_ta_opportunitycost import DialogLumensTAOpportunityCost
from dialog_lumens_ta_opportunitycostmap import DialogLumensTAOpportunityCostMap
from dialog_lumens_ta_resioda import DialogLumensTARegionalEconomySingleIODescriptiveAnalysis
from dialog_lumens_ta_retsioda import DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis
from dialog_lumens_ta_landdistribreq import DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis
from dialog_lumens_ta_impactlanduse import DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis
from dialog_lumens_ta_finaldemandscenario import DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis
from dialog_lumens_ta_gdpscenario import DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis
from dialog_lumens_sciendo_driversanalysis import DialogLumensSCIENDODriversAnalysis
from dialog_lumens_sciendo_buildscenario import DialogLumensSCIENDOBuildScenario
from dialog_lumens_sciendo_historicalbaselineproj import DialogLumensSCIENDOHistoricalBaselineProjection
from dialog_lumens_sciendo_historicalbaselineannualproj import DialogLumensSCIENDOHistoricalBaselineAnnualProjection
from dialog_lumens_sciendo_calctransitionmatrix import DialogLumensSCIENDOCalculateTransitionMatrix
from dialog_lumens_sciendo_createrastercube import DialogLumensSCIENDOCreateRasterCube
from dialog_lumens_sciendo_calcweightevidence import DialogLumensSCIENDOCalculateWeightofEvidence
from dialog_lumens_sciendo_simulatelandusechange import DialogLumensSCIENDOSimulateLandUseChange
from dialog_lumens_sciendo_simulatewithscenario import DialogLumensSCIENDOSimulateWithScenario
from dialog_lumens_tools_reddabacussp import DialogLumensToolsREDDAbacusSP


#############################################################################


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
        """
        super(MainWindow, self).__init__(parent)
        
        # Default settings for each LUMENS dialog
        self.appSettings = {
            'debug': False,
            'appDir': os.path.dirname(os.path.realpath(__file__)),
            'dataDir': 'data',
            'basemapDir': 'basemap',
            'vectorDir': 'vector',
            'defaultBasemapFile': 'basemap.tif',
            'defaultBasemapFilePath': '',
            'defaultVectorFile': 'landmarks.shp',
            'defaultVectorFilePath': '',
            'selectShapefileExt': '.shp',
            'selectRasterfileExt': '.tif',
            'selectCsvfileExt': '.csv',
            'selectProjectfileExt': '.lpj',
            'selectDatabasefileExt': '.dbf',
            'selectHTMLfileExt': '.html',
            'selectTextfileExt': '.txt',
            'selectCarfileExt': '.car',
            'extentSEA': QgsRectangle(95, -11, 140, 11), # Southeast Asia extent
            'defaultCRS': 4326, # EPSG 4326 - WGS 84
            
            'DialogFeatureSelectExpression': {
                'expression': '',
            },
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
            'DialogLumensAddPeatData': {
                'rasterfile': '',
                'description': '',
            },
            'DialogLumensAddFactorData': {
                'rasterfile': '',
                'description': '',
            },
            'DialogLumensAddPlanningUnitData': {
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
            'DialogLumensPURReconcilePlanningUnit': {
                'outputFile': '',
            },
            'DialogLumensPURFinalization': {
                'shapefile': '',
            },
            'DialogLumensPreQUESLandcoverChangeAnalysis': {
                'csvfile': '',
                'option': '',
                'nodata': '',
            },
            'DialogLumensPreQUESLandcoverTrajectoriesAnalysis': {
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
            'DialogLumensQUESCCarbonAccounting': {
                'csvfile': '',
                'nodata': '',
            },
            'DialogLumensQUESCPeatlandCarbonAccounting': {
                'csvfile': '',
            },
            'DialogLumensQUESCSummarizeMultiplePeriod': {
                'checkbox': '',
            },
            'DialogLumensQUESBAnalysis': {
                'csvLandCover': '',
                'samplingGridRes': '',
                'samplingWindowSize': '',
                'windowShape': '',
                'nodata': '',
                'csvClassDescriptors': '',
                'csvEdgeContrast': '',
                'csvZoneLookup': '',
                'refMapID': '',
                'outputTECIInitial': '',
                'outputTECIFinal': '',
                'outputHabitatLoss': '',
                'outputDegradedHabitat': '',
                'outputHabitatGain': '',
                'outputRecoveredHabitat': '',
            },
            'DialogLumensTAAbacusOpportunityCost': {
                'projectFile': '',
            },
            'DialogLumensTAOpportunityCost': {
                'workingDir': '',
                'QUESCDatabase': '',
                'csvNPVTable': '',
                'period1': '',
                'period2': '',
                'costThreshold': '',
                'outputOpportunityCostDatabase': '',
                'outputOpportunityCostReport': '',
            },
            'DialogLumensTAOpportunityCostMap': {
                'workingDir': '',
                'landUseT1': '',
                'landUseT2': '',
                'planningUnit': '',
                'csvCarbon': '',
                'csvProfitability': '',
                'csvPlanningUnit': '',
                'location': '',
                't1': '',
                't2': '',
            },
            'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis': {
                'workingDir': '',
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'labourRequirement': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis': {
                'workingDir': '',
                'intermediateConsumptionMatrixP1': '',
                'intermediateConsumptionMatrixP2': '',
                'valueAddedMatrixP1': '',
                'valueAddedMatrixP2': '',
                'finalConsumptionMatrixP1': '',
                'finalConsumptionMatrixP2': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'labourRequirementP1': '',
                'labourRequirementP2': '',
                'financialUnit': '',
                'areaName': '',
                'period1': '',
                'period2': '',
            },
            'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis': {
                'workingDir': '',
                'landCoverMap': '',
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'landDistributionMatrix': '',
                'landCoverComponent': '',
                'labourRequirement': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis': {
                'workingDir': '',
                'landCoverMapP1': '',
                'landCoverMapP2': '',
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'landDistributionMatrix': '',
                'landRequirementCoefficientMatrix': '',
                'landCoverComponent': '',
                'labourRequirement': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis': {
                'workingDir': '',
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'landDistributionMatrix': '',
                'landRequirementCoefficientMatrix': '',
                'landCoverComponent': '',
                'labourRequirement': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
                'finalDemandChangeScenario': '',
            },
            'DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis': {
                'workingDir': '',
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'landDistributionMatrix': '',
                'landRequirementCoefficientMatrix': '',
                'landCoverComponent': '',
                'labourRequirement': '',
                'gdpChangeScenario': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensSCIENDOHistoricalBaselineProjection': {
                'workingDir': '',
                'QUESCDatabase': '',
                't1': '',
                't2': '',
                'iteration': '',
            },
            'DialogLumensSCIENDOHistoricalBaselineAnnualProjection': {
                'iteration': '',
            },
            'DialogLumensSCIENDODriversAnalysis': {
                'landUseCoverChangeDrivers': '',
                'landUseCoverChangeType': '',
            },
            'DialogLumensSCIENDOBuildScenario': {
                'historicalBaselineCar': '',
            },
            'DialogLumensSCIENDOCalculateTransitionMatrix': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensSCIENDOCreateRasterCube': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensSCIENDOCalculateWeightofEvidence': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensSCIENDOSimulateLandUseChange': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensSCIENDOSimulateWithScenario': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensToolsREDDAbacusSP': {
                'carfile': '',
            },
        }
        
        # Process app arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--debug', action='store_true', help='Show the logging widget')
        
        args = parser.parse_args()
        
        if args.debug:
            self.appSettings['debug'] = True
        
        
        self.appSettings['defaultBasemapFilePath'] = os.path.join(self.appSettings['appDir'], self.appSettings['dataDir'], self.appSettings['basemapDir'], self.appSettings['defaultBasemapFile'])
        self.appSettings['defaultVectorFilePath'] = os.path.join(self.appSettings['appDir'], self.appSettings['dataDir'], self.appSettings['vectorDir'], self.appSettings['defaultVectorFile'])

        self.setupUi()
        
        self.installEventFilter(self)
        
        self.openDialogs = []
        
        # For holding QgsVectorLayer/QgsRasterLayer objects
        self.qgsLayerList = dict()
        
        # PyQT model+view for layers list
        self.layerListModel = QtGui.QStandardItemModel(self.layerListView)
        ##self.layerListModel.setSupportedDragActions(QtCore.Qt.MoveAction)
        self.layerListView.setModel(self.layerListModel)
        
        self.layerListView.clicked.connect(self.handlerSelectLayer)
        self.layerListModel.itemChanged.connect(self.handlerCheckLayer)
        
        # For checking drop events
        ##self.layerListView.viewport().installEventFilter(self)
        
        # Init the logger
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_box.setFormatter(formatter)
        self.logger.addHandler(self.log_box)
        self.logger.setLevel(logging.DEBUG)
        
        # App action handlers
        self.actionQuit.triggered.connect(QtGui.qApp.quit)
        self.actionZoomIn.triggered.connect(self.handlerZoomIn)
        self.actionZoomOut.triggered.connect(self.handlerZoomOut)
        self.actionZoomFull.triggered.connect(self.handlerZoomFull)
        self.actionZoomLayer.triggered.connect(self.handlerZoomLayer)
        self.actionZoomSelected.triggered.connect(self.handlerZoomSelected)
        self.actionPanSelected.triggered.connect(self.handlerPanSelected)
        self.actionPan.triggered.connect(self.handlerSetPanMode)
        self.actionSelect.triggered.connect(self.handlerSetSelectMode)
        self.actionInfo.triggered.connect(self.handlerSetInfoMode)
        self.actionAddLayer.triggered.connect(self.handlerAddLayer)
        self.actionDeleteLayer.triggered.connect(self.handlerDeleteLayer)
        self.actionRefresh.triggered.connect(self.handlerRefresh)
        self.mapCanvas.zoomLastStatusChanged.connect(self.handlerZoomLastStatus)
        self.mapCanvas.zoomNextStatusChanged.connect(self.handlerZoomNextStatus)
        self.actionZoomLast.triggered.connect(self.handlerZoomLast)
        self.actionZoomNext.triggered.connect(self.handlerZoomNext)
        self.actionLayerAttributeTable.triggered.connect(self.handlerLayerAttributeTable)
        self.actionFeatureSelectExpression.triggered.connect(self.handlerFeatureSelectExpression)
        
        # LUMENS action handlers
        # Database menu
        self.actionDialogLumensCreateDatabase.triggered.connect(self.handlerDialogLumensCreateDatabase)
        self.actionLumensOpenDatabase.triggered.connect(self.handlerLumensOpenDatabase)
        self.actionLumensCloseDatabase.triggered.connect(self.handlerLumensCloseDatabase)
        self.actionDialogLumensAddLandcoverRaster.triggered.connect(self.handlerDialogLumensAddLandcoverRaster)
        self.actionDialogLumensAddPeatData.triggered.connect(self.handlerDialogLumensAddPeatData)
        self.actionDialogLumensAddFactorData.triggered.connect(self.handlerDialogLumensAddFactorData)
        self.actionDialogLumensAddPlanningUnitData.triggered.connect(self.handlerDialogLumensAddPlanningUnitData)
        self.actionLumensDeleteData.triggered.connect(self.handlerLumensDeleteData)
        self.actionDialogLumensImportDatabase.triggered.connect(self.handlerDialogLumensImportDatabase)
        
        # PUR menu
        self.actionDialogLumensPURCreateReferenceData.triggered.connect(self.handlerDialogLumensPURCreateReferenceData)
        self.actionDialogLumensPURPreparePlanningUnit.triggered.connect(self.handlerDialogLumensPURPreparePlanningUnit)
        self.actionDialogLumensPURReconcilePlanningUnit.triggered.connect(self.handlerDialogLumensPURReconcilePlanningUnit)
        self.actionDialogLumensPURFinalization.triggered.connect(self.handlerDialogLumensPURFinalization)
        
        # QUES menu
        self.actionDialogLumensPreQUESLandcoverChangeAnalysis.triggered.connect(self.handlerDialogLumensPreQUESLandcoverChangeAnalysis)
        self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis.triggered.connect(self.handlerDialogLumensPreQUESLandcoverTrajectoriesAnalysis)
        self.actionDialogLumensQUESCCarbonAccounting.triggered.connect(self.handlerDialogLumensQUESCCarbonAccounting)
        self.actionDialogLumensQUESCPeatlandCarbonAccounting.triggered.connect(self.handlerDialogLumensQUESCPeatlandCarbonAccounting)
        self.actionDialogLumensQUESCSummarizeMultiplePeriod.triggered.connect(self.handlerDialogLumensQUESCSummarizeMultiplePeriod)
        self.actionDialogLumensQUESBAnalysis.triggered.connect(self.handlerDialogLumensQUESBAnalysis)
        
        # TA menu
        self.actionDialogLumensTAAbacusOpportunityCost.triggered.connect(self.handlerDialogLumensTAAbacusOpportunityCost)
        self.actionDialogLumensTAOpportunityCost.triggered.connect(self.handlerDialogLumensTAOpportunityCost)
        self.actionDialogLumensTAOpportunityCostMap.triggered.connect(self.handlerDialogLumensTAOpportunityCostMap)
        self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomySingleIODescriptiveAnalysis)
        self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis)
        self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis)
        self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.triggered.connect(self.handlerDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis)
        self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis)
        self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDODriversAnalysis.triggered.connect(self.handlerDialogLumensSCIENDODriversAnalysis)
        self.actionDialogLumensSCIENDOBuildScenario.triggered.connect(self.handlerDialogLumensSCIENDOBuildScenario)
        self.actionDialogLumensSCIENDOHistoricalBaselineProjection.triggered.connect(self.handlerDialogLumensSCIENDOHistoricalBaselineProjection)
        self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection.triggered.connect(self.handlerDialogLumensSCIENDOHistoricalBaselineAnnualProjection)
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix.triggered.connect(self.handlerDialogLumensSCIENDOCalculateTransitionMatrix)
        self.actionDialogLumensSCIENDOCreateRasterCube.triggered.connect(self.handlerDialogLumensSCIENDOCreateRasterCube)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence.triggered.connect(self.handlerDialogLumensSCIENDOCalculateWeightofEvidence)
        self.actionDialogLumensSCIENDOSimulateLandUseChange.triggered.connect(self.handlerDialogLumensSCIENDOSimulateLandUseChange)
        self.actionDialogLumensSCIENDOSimulateWithScenario.triggered.connect(self.handlerDialogLumensSCIENDOSimulateWithScenario)
        
        # Tools menu
        self.actionDialogLumensToolsREDDAbacusSP.triggered.connect(self.handlerDialogLumensToolsREDDAbacusSP)
    
    
    def eventFilter(self, source, event):
        """
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            print 'widget window has gained focus'
            if not self.appSettings['DialogLumensOpenDatabase']['projectFile']:
                self.actionLumensCloseDatabase.setDisabled(True)
                self.lumensDisableMenus()
            else:
                self.lumensEnableMenus()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            print 'widget window has lost focus'
        elif event.type() == QtCore.QEvent.FocusIn:
            print 'widget has gained keyboard focus'
        elif event.type() == QtCore.QEvent.FocusOut:
            print 'widget has lost keyboard focus'
        elif event.type() == QtCore.QEvent.Drop and source == self.layerListView.viewport():
            self.handlerDropLayer()
        
        return False
    
    
    def setupUi(self):
        """
        """
        self.setWindowTitle('LUMENS: Alpha')

        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setMinimumSize(800, 400)
        self.setCentralWidget(self.centralWidget)
        
        # Create the default menus
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.viewMenu = self.menubar.addMenu('&View')
        self.modeMenu = self.menubar.addMenu('&Mode')
        self.databaseMenu = self.menubar.addMenu('&Database')
        self.purMenu = self.menubar.addMenu('&PUR')
        self.quesMenu = self.menubar.addMenu('&QUES')
        self.taMenu = self.menubar.addMenu('&TA')
        self.sciendoMenu = self.menubar.addMenu('&SCIENDO')
        ###self.toolsMenu = self.menubar.addMenu('T&ools')

        self.toolBar = QtGui.QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        
        ##self.statusBar = QtGui.QStatusBar(self)
        ##self.statusBar.setFixedHeight(10)
        ##self.labelLayerCRS = QtGui.QLabel(self)
        ##self.labelLayerCRS.setText('...')
        ##self.statusBar.addPermanentWidget(self.labelLayerCRS)
        ##self.setStatusBar(self.statusBar)
        
        # Create the actions and assigned them to the menus
        self.actionQuit = QtGui.QAction('Quit', self)
        self.actionQuit.setShortcut(QtGui.QKeySequence.Quit)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomIn.png')
        self.actionZoomIn = QtGui.QAction(icon, 'Zoom In', self)
        self.actionZoomIn.setShortcut(QtGui.QKeySequence.ZoomIn)

        icon = QtGui.QIcon(':/ui/icons/iconActionZoomOut.png')
        self.actionZoomOut = QtGui.QAction(icon, 'Zoom Out', self)
        self.actionZoomOut.setShortcut(QtGui.QKeySequence.ZoomOut)

        icon = QtGui.QIcon(':/ui/icons/iconActionPan.png')
        self.actionPan = QtGui.QAction(icon, 'Pan', self)
        self.actionPan.setShortcut('Ctrl+1')
        self.actionPan.setCheckable(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionSelect.png')
        self.actionSelect = QtGui.QAction(icon, 'Select', self)
        self.actionSelect.setShortcut('Ctrl+2')
        self.actionSelect.setCheckable(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionInfo.png')
        self.actionInfo = QtGui.QAction(icon, 'Info', self)
        self.actionInfo.setShortcut('Ctrl+3')
        self.actionInfo.setCheckable(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionAdd.png')
        self.actionAddLayer = QtGui.QAction(icon, 'Add Layer', self)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionDelete.png')
        self.actionDeleteLayer = QtGui.QAction(icon, 'Delete Layer', self)
        self.actionDeleteLayer.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionRefresh.png')
        self.actionRefresh = QtGui.QAction(icon, 'Refresh', self)
        self.actionRefresh.setShortcut('Ctrl+R')
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomFull.png')
        self.actionZoomFull = QtGui.QAction(icon, 'Zoom Full', self)
        self.actionZoomFull.setShortcut('Ctrl+F')
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomLayer.png')
        self.actionZoomLayer = QtGui.QAction(icon, 'Zoom to Layer', self)
        self.actionZoomLayer.setShortcut('Ctrl+L')
        self.actionZoomLayer.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomSelected.png')
        self.actionZoomSelected = QtGui.QAction(icon, 'Zoom to Selected', self)
        self.actionZoomSelected.setShortcut('Ctrl+S')
        
        icon = QtGui.QIcon(':/ui/icons/iconActionPanSelected.png')
        self.actionPanSelected = QtGui.QAction(icon, 'Pan to Selected', self)
        self.actionPanSelected.setShortcut('Ctrl+P')
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomLast.png')
        self.actionZoomLast = QtGui.QAction(icon, 'Zoom Last', self)
        self.actionZoomLast.setShortcut('Ctrl+,')
        self.actionZoomLast.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomNext.png')
        self.actionZoomNext = QtGui.QAction(icon, 'Zoom Next', self)
        self.actionZoomNext.setShortcut('Ctrl+.')
        self.actionZoomNext.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionLayerAttributeTable.png')
        self.actionLayerAttributeTable = QtGui.QAction(icon, 'Layer Attribute Table', self)
        self.actionLayerAttributeTable.setShortcut('Ctrl+T')
        self.actionLayerAttributeTable.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionFeatureSelectExpression.png')
        self.actionFeatureSelectExpression = QtGui.QAction(icon, 'Select Features By Expression', self)
        self.actionFeatureSelectExpression.setShortcut('Ctrl+E')
        self.actionFeatureSelectExpression.setDisabled(True)
        
        self.fileMenu.addAction(self.actionQuit)
        
        self.viewMenu.addAction(self.actionZoomIn)
        self.viewMenu.addAction(self.actionZoomOut)
        self.viewMenu.addAction(self.actionPanSelected)
        self.viewMenu.addAction(self.actionZoomFull)
        self.viewMenu.addAction(self.actionZoomLayer)
        self.viewMenu.addAction(self.actionZoomSelected)
        self.viewMenu.addAction(self.actionZoomLast)
        self.viewMenu.addAction(self.actionZoomNext)
        self.viewMenu.addAction(self.actionRefresh)
        
        self.modeMenu.addAction(self.actionPan)
        self.modeMenu.addAction(self.actionSelect)
        self.modeMenu.addAction(self.actionInfo)
        
        self.toolBar.addAction(self.actionAddLayer)
        self.toolBar.addAction(self.actionDeleteLayer)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addAction(self.actionPanSelected)
        self.toolBar.addAction(self.actionZoomFull)
        self.toolBar.addAction(self.actionZoomLayer)
        self.toolBar.addAction(self.actionZoomSelected)
        self.toolBar.addAction(self.actionZoomLast)
        self.toolBar.addAction(self.actionZoomNext)
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionLayerAttributeTable)
        self.toolBar.addAction(self.actionFeatureSelectExpression)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPan)
        self.toolBar.addAction(self.actionSelect)
        self.toolBar.addAction(self.actionInfo)
        
        # Database menu
        self.actionDialogLumensCreateDatabase = QtGui.QAction('Create LUMENS database', self)
        self.actionLumensOpenDatabase = QtGui.QAction('Open LUMENS database', self)
        self.actionLumensCloseDatabase = QtGui.QAction('Close LUMENS database', self)
        self.actionDialogLumensAddLandcoverRaster = QtGui.QAction('Add land use/cover data', self)
        self.actionDialogLumensAddPeatData = QtGui.QAction('Add peat data', self)
        self.actionDialogLumensAddFactorData = QtGui.QAction('Add factor data', self)
        self.actionDialogLumensAddPlanningUnitData = QtGui.QAction('Add planning unit data', self)
        self.actionLumensDeleteData = QtGui.QAction('Delete LUMENS data', self)
        self.actionDialogLumensImportDatabase = QtGui.QAction('Import LUMENS database', self)
        
        self.databaseMenu.addAction(self.actionDialogLumensCreateDatabase)
        self.databaseMenu.addAction(self.actionLumensOpenDatabase)
        self.databaseMenu.addAction(self.actionLumensCloseDatabase)
        self.addDataMenu = self.databaseMenu.addMenu('Add data into LUMENS database')
        self.addDataMenu.addAction(self.actionDialogLumensAddLandcoverRaster)
        self.addDataMenu.addAction(self.actionDialogLumensAddPeatData)
        self.addDataMenu.addAction(self.actionDialogLumensAddFactorData)
        self.addDataMenu.addAction(self.actionDialogLumensAddPlanningUnitData)
        self.databaseMenu.addAction(self.actionLumensDeleteData)
        self.databaseMenu.addAction(self.actionDialogLumensImportDatabase)
        
        # PUR menu
        self.actionDialogLumensPURCreateReferenceData = QtGui.QAction('Create reference data', self)
        self.actionDialogLumensPURPreparePlanningUnit = QtGui.QAction('Prepare planning unit', self)
        self.actionDialogLumensPURReconcilePlanningUnit = QtGui.QAction('Reconcile planning unit', self)
        self.actionDialogLumensPURFinalization = QtGui.QAction('Finalization', self)
        
        self.functionsBasedReconciliationMenu = self.purMenu.addMenu('Functions-based Reconciliation')
        self.functionsBasedReconciliationMenu.addAction(self.actionDialogLumensPURCreateReferenceData)
        self.functionsBasedReconciliationMenu.addAction(self.actionDialogLumensPURPreparePlanningUnit)
        self.functionsBasedReconciliationMenu.addAction(self.actionDialogLumensPURReconcilePlanningUnit)
        self.functionsBasedReconciliationMenu.addAction(self.actionDialogLumensPURFinalization)
        
        # QUES menu
        self.actionDialogLumensPreQUESLandcoverChangeAnalysis = QtGui.QAction('Land cover change analysis', self)
        self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis = QtGui.QAction('Land cover trajectories analysis', self)
        self.actionDialogLumensQUESCCarbonAccounting = QtGui.QAction('Carbon accounting', self)
        self.actionDialogLumensQUESCPeatlandCarbonAccounting = QtGui.QAction('Peatland carbon accounting', self)
        self.actionDialogLumensQUESCSummarizeMultiplePeriod = QtGui.QAction('Summarize multiple period', self)
        self.actionDialogLumensQUESBAnalysis = QtGui.QAction('QUES-B Analysis', self)
        
        self.preQUESMenu = self.quesMenu.addMenu('Pre-QUES')
        self.QUESCMenu = self.quesMenu.addMenu('QUES-C')
        self.QUESBMenu = self.quesMenu.addMenu('QUES-B')
        self.QUESHMenu = self.quesMenu.addMenu('QUES-H')
        self.preQUESMenu.addAction(self.actionDialogLumensPreQUESLandcoverChangeAnalysis)
        self.preQUESMenu.addAction(self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis)
        self.QUESCMenu.addAction(self.actionDialogLumensQUESCCarbonAccounting)
        self.QUESCMenu.addAction(self.actionDialogLumensQUESCPeatlandCarbonAccounting)
        self.QUESCMenu.addAction(self.actionDialogLumensQUESCSummarizeMultiplePeriod)
        self.QUESBMenu.addAction(self.actionDialogLumensQUESBAnalysis)
        
        # TA menu
        self.actionDialogLumensTAAbacusOpportunityCost = QtGui.QAction('Abacus opportunity cost curve', self)
        self.actionDialogLumensTAOpportunityCost = QtGui.QAction('Opportunity cost curve', self)
        self.actionDialogLumensTAOpportunityCostMap = QtGui.QAction('Opportunity cost map', self)
        self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis = QtGui.QAction('Descriptive analysis of regional economy (single time series)', self)
        self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis = QtGui.QAction('Descriptive analysis of regional economy (multiple time series)', self)
        self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis = QtGui.QAction('Land requirement analysis', self)
        self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis = QtGui.QAction('Impact of land use change to regional economy', self)
        self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis = QtGui.QAction('Impact of regional economic scenario to land use change (final demand scenario)', self)
        self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis = QtGui.QAction('Impact of regional economic scenario to land use change (GDP scenario)', self)
        
        self.opportunityCostMenu = self.taMenu.addMenu('Opportunity cost')
        self.regionalEconomyMenu = self.taMenu.addMenu('Regional economy')
        self.opportunityCostMenu.addAction(self.actionDialogLumensTAAbacusOpportunityCost)
        self.opportunityCostMenu.addAction(self.actionDialogLumensTAOpportunityCost)
        self.opportunityCostMenu.addAction(self.actionDialogLumensTAOpportunityCostMap)
        self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis)
        self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis)
        self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis)
        self.regionalEconomyMenu.addAction(self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis)
        self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis)
        self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDODriversAnalysis = QtGui.QAction('Drivers analysis', self)
        self.actionDialogLumensSCIENDOBuildScenario = QtGui.QAction('Build scenario', self)
        self.actionDialogLumensSCIENDOHistoricalBaselineProjection = QtGui.QAction('Historical baseline projection', self)
        self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection = QtGui.QAction('Historical baseline annual projection', self)
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix = QtGui.QAction('Calculate transition matrix', self)
        self.actionDialogLumensSCIENDOCreateRasterCube = QtGui.QAction('Create raster cube of factors', self)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence = QtGui.QAction('Calculate weight of evidence', self)
        self.actionDialogLumensSCIENDOSimulateLandUseChange = QtGui.QAction('Simulate land use change', self)
        self.actionDialogLumensSCIENDOSimulateWithScenario = QtGui.QAction('Simulate with scenario', self)
        
        self.lowEmissionDevelopmentMenu = self.sciendoMenu.addMenu('Low emission development analysis')
        self.landUseChangeModelingMenu = self.sciendoMenu.addMenu('Land use change modeling')
        self.historicalBaselineMenu = self.lowEmissionDevelopmentMenu.addMenu('Historical baseline')
        self.historicalBaselineMenu.addAction(self.actionDialogLumensSCIENDOHistoricalBaselineProjection)
        self.historicalBaselineMenu.addAction(self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection)
        self.lowEmissionDevelopmentMenu.addAction(self.actionDialogLumensSCIENDODriversAnalysis)
        self.lowEmissionDevelopmentMenu.addAction(self.actionDialogLumensSCIENDOBuildScenario)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCalculateTransitionMatrix)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCreateRasterCube)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCalculateWeightofEvidence)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOSimulateLandUseChange)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOSimulateWithScenario)
        
        # Tools menu
        self.actionDialogLumensToolsREDDAbacusSP = QtGui.QAction('REDD Abacus SP', self)
        
        ###self.toolsMenu.addAction(self.actionDialogLumensToolsREDDAbacusSP)
        
        # Create the app window layouts
        self.layoutActiveProject = QtGui.QHBoxLayout()
        self.labelActiveProject = QtGui.QLabel(self)
        self.labelActiveProject.setText('Active project:')
        self.layoutActiveProject.addWidget(self.labelActiveProject)
        
        self.lineEditActiveProject = QtGui.QLineEdit(self)
        self.lineEditActiveProject.setReadOnly(True)
        self.layoutActiveProject.addWidget(self.lineEditActiveProject)
        
        ##self.contentSidebar = QtGui.QWidget()
        ##self.layoutSidebar = QtGui.QVBoxLayout()
        ##self.contentSidebar.setLayout(self.layoutSidebar)
        
        self.layerListView = QtGui.QListView(self)
        self.layerListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        ##self.layerListView.setMovement(QtGui.QListView.Snap)
        self.layerListView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.layerListView.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.layerListView.setDragDropOverwriteMode(False)
        self.layerListView.setAcceptDrops(True)
        self.layerListView.setDropIndicatorShown(True)
        self.layerListView.setDragEnabled(True)
        self.layerListView.setFixedWidth(200)
        
        ##self.layoutSidebar.setContentsMargins(0, 0, 0, 0)
        ##self.layoutSidebar.addWidget(self.layerListView)
        
        ##self.scrollSidebar = QtGui.QScrollArea()
        ##self.scrollSidebar.setFixedWidth(200)
        ##self.scrollSidebar.setWidget(self.contentSidebar)
        
        self.layoutBody = QtGui.QHBoxLayout()
        self.layoutBody.setContentsMargins(0, 0, 0, 0)
        self.layoutBody.setAlignment(QtCore.Qt.AlignLeft)
        ##self.layoutBody.addWidget(self.scrollSidebar)
        self.layoutBody.addWidget(self.layerListView)
        
        self.layoutMain = QtGui.QVBoxLayout()
        self.layoutMain.addLayout(self.layoutActiveProject)
        ###self.layoutMain.addLayout(self.layoutBody)
        self.contentBody = QtGui.QWidget()
        self.contentBody.setLayout(self.layoutBody)
        
        # A splitter between content body and the collapsible log box
        self.log_box = QPlainTextEditLogger(self)
        self.splitterMain = QtGui.QSplitter(self)
        self.splitterMain.setOrientation(QtCore.Qt.Vertical)
        ###self.layoutMain.addWidget(self.log_box.widget)
        self.splitterMain.addWidget(self.contentBody)
        self.splitterMain.addWidget(self.log_box.widget)
        
        # Show the logging widget only in debug mode
        if not self.appSettings['debug']:
            self.log_box.widget.setVisible(False)
        
        self.splitterMain.setStretchFactor(0, 5) # Bigger proportion for contentBody
        self.splitterMain.setStretchFactor(1, 1) # Smaller proportion for log box
        self.splitterMain.setCollapsible(0, False) # Don't collapse contentBody
        self.layoutMain.addWidget(self.splitterMain)
        
        self.centralWidget.setLayout(self.layoutMain)
        
        # Initialize the mapcanvas and map tools
        # Enable on the fly CRS projection
        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.useImageToRender(False)
        self.mapCanvas.mapRenderer().setProjectionsEnabled(True)
        self.mapCanvas.mapRenderer().setDestinationCrs(QgsCoordinateReferenceSystem(self.appSettings['defaultCRS'], QgsCoordinateReferenceSystem.EpsgCrsId))
        self.mapCanvas.setCanvasColor(QtCore.Qt.white)
        self.mapCanvas.enableAntiAliasing(True)
        ##self.mapCanvas.refresh()
        ##self.mapCanvas.show()
        
        # Initialize the map tools and assign to the related action
        self.panTool = PanTool(self.mapCanvas)
        self.panTool.setAction(self.actionPan)
        
        self.selectTool = SelectTool(self)
        self.selectTool.setAction(self.actionSelect)

        self.infoTool = InfoTool(self)
        self.infoTool.setAction(self.actionInfo)

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
    
    
    def handlerDialogLumensOpenDatabase(self):
        """
        """
        self.openDialog(DialogLumensOpenDatabase)
    
    
    def handlerLumensOpenDatabase(self):
        """Select a .lpj database file and open it
        """
        lumensDatabase = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select LUMENS Database', QtCore.QDir.homePath(), 'LUMENS Database (*{0})'.format(self.appSettings['selectProjectfileExt'])))
        
        if lumensDatabase:
            logging.getLogger(__name__).info('select LUMENS database: %s', lumensDatabase)
            
            self.lumensOpenDatabase(lumensDatabase)
    
    
    def lumensEnableMenus(self):
        """
        """
        self.actionLumensCloseDatabase.setEnabled(True)
        self.actionLumensDeleteData.setEnabled(True)
        
        self.actionDialogLumensAddLandcoverRaster.setEnabled(True)
        self.actionDialogLumensAddPeatData.setEnabled(True)
        self.actionDialogLumensAddFactorData.setEnabled(True)
        self.actionDialogLumensAddPlanningUnitData.setEnabled(True)
        
        self.actionDialogLumensPURCreateReferenceData.setEnabled(True)
        self.actionDialogLumensPURPreparePlanningUnit.setEnabled(True)
        self.actionDialogLumensPURReconcilePlanningUnit.setEnabled(True)
        self.actionDialogLumensPURFinalization.setEnabled(True)
        
        self.actionDialogLumensPreQUESLandcoverChangeAnalysis.setEnabled(True)
        self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setEnabled(True)
        self.actionDialogLumensQUESCCarbonAccounting.setEnabled(True)
        self.actionDialogLumensQUESCPeatlandCarbonAccounting.setEnabled(True)
        self.actionDialogLumensQUESCSummarizeMultiplePeriod.setEnabled(True)
        self.actionDialogLumensQUESBAnalysis.setEnabled(True)
        
        self.actionDialogLumensTAAbacusOpportunityCost.setEnabled(True)
        self.actionDialogLumensTAOpportunityCost.setEnabled(True)
        self.actionDialogLumensTAOpportunityCostMap.setEnabled(True)
        self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setEnabled(True)
        self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setEnabled(True)
        self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setEnabled(True)
        self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setEnabled(True)
        self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setEnabled(True)
        self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setEnabled(True)
        
        self.actionDialogLumensSCIENDODriversAnalysis.setEnabled(True)
        self.actionDialogLumensSCIENDOBuildScenario.setEnabled(True)
        self.actionDialogLumensSCIENDOHistoricalBaselineProjection.setEnabled(True)
        self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection.setEnabled(True)
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix.setEnabled(True)
        self.actionDialogLumensSCIENDOCreateRasterCube.setEnabled(True)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence.setEnabled(True)
        self.actionDialogLumensSCIENDOSimulateLandUseChange.setEnabled(True)
        self.actionDialogLumensSCIENDOSimulateWithScenario.setEnabled(True)
    
    
    def lumensDisableMenus(self):
        """
        """
        self.actionLumensDeleteData.setDisabled(True)
        self.actionDialogLumensAddLandcoverRaster.setDisabled(True)
        self.actionDialogLumensAddPeatData.setDisabled(True)
        self.actionDialogLumensAddFactorData.setDisabled(True)
        self.actionDialogLumensAddPlanningUnitData.setDisabled(True)
        
        self.actionDialogLumensPURCreateReferenceData.setDisabled(True)
        self.actionDialogLumensPURPreparePlanningUnit.setDisabled(True)
        self.actionDialogLumensPURReconcilePlanningUnit.setDisabled(True)
        self.actionDialogLumensPURFinalization.setDisabled(True)
        
        self.actionDialogLumensPreQUESLandcoverChangeAnalysis.setDisabled(True)
        self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setDisabled(True)
        self.actionDialogLumensQUESCCarbonAccounting.setDisabled(True)
        self.actionDialogLumensQUESCPeatlandCarbonAccounting.setDisabled(True)
        self.actionDialogLumensQUESCSummarizeMultiplePeriod.setDisabled(True)
        self.actionDialogLumensQUESBAnalysis.setDisabled(True)
        
        self.actionDialogLumensTAAbacusOpportunityCost.setDisabled(True)
        self.actionDialogLumensTAOpportunityCost.setDisabled(True)
        self.actionDialogLumensTAOpportunityCostMap.setDisabled(True)
        self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setDisabled(True)
        self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setDisabled(True)
        self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setDisabled(True)
        self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setDisabled(True)
        self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setDisabled(True)
        self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setDisabled(True)
        
        self.actionDialogLumensSCIENDODriversAnalysis.setDisabled(True)
        self.actionDialogLumensSCIENDOBuildScenario.setDisabled(True)
        self.actionDialogLumensSCIENDOHistoricalBaselineProjection.setDisabled(True)
        self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection.setDisabled(True)
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix.setDisabled(True)
        self.actionDialogLumensSCIENDOCreateRasterCube.setDisabled(True)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence.setDisabled(True)
        self.actionDialogLumensSCIENDOSimulateLandUseChange.setDisabled(True)
        self.actionDialogLumensSCIENDOSimulateWithScenario.setDisabled(True)
    
    
    def lumensOpenDatabase(self, lumensDatabase):
        """
        """
        logging.getLogger(__name__).info('start: LUMENS Open Database')
        
        self.actionLumensOpenDatabase.setDisabled(True)
        
        outputs = general.runalg(
            'modeler:lumens_open_database',
            lumensDatabase,
            None
        )
        
        if outputs:
            ##print outputs
            # outputs['overview_ALG0'] => temporary raster file
            
            self.appSettings['DialogLumensOpenDatabase']['projectFile'] = lumensDatabase
            self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = os.path.dirname(lumensDatabase)
            
            self.lineEditActiveProject.setText(os.path.normpath(lumensDatabase))
            
            self.lumensEnableMenus()
        
        self.actionLumensOpenDatabase.setEnabled(True)
        
        logging.getLogger(__name__).info('end: LUMENS Open Database')
    
    
    def handlerLumensCloseDatabase(self):
        """
        """
        self.lumensCloseDatabase()
    
    
    def lumensCloseDatabase(self):
        """
        """
        logging.getLogger(__name__).info('start: LUMENS Close Database')
        
        self.actionLumensCloseDatabase.setDisabled(True)
        
        outputs = general.runalg('modeler:lumens_close_database')
        
        self.appSettings['DialogLumensOpenDatabase']['projectFile'] = ''
        self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = ''
        
        self.lineEditActiveProject.clear()
        
        self.lumensDisableMenus()
        
        logging.getLogger(__name__).info('end: LUMENS Close Database')
    
    
    def handlerLumensDeleteData(self):
        """
        """
        logging.getLogger(type(self).__name__).info('start: lumensdeletedata')
        
        self.actionLumensDeleteData.setDisabled(True)
        outputs = general.runalg('r:lumensdeletedata')
        self.actionLumensDeleteData.setEnabled(True)
        
        logging.getLogger(__name__).info('end: lumensdeletedata')
    
    
    def handlerDialogLumensAddLandcoverRaster(self):
        """
        """
        self.openDialog(DialogLumensAddLandcoverRaster)
    
    
    def handlerDialogLumensAddPeatData(self):
        """
        """
        self.openDialog(DialogLumensAddPeatData)
    
    
    def handlerDialogLumensAddFactorData(self):
        """
        """
        self.openDialog(DialogLumensAddFactorData)
    
    
    def handlerDialogLumensAddPlanningUnitData(self):
        """
        """
        self.openDialog(DialogLumensAddPlanningUnitData)
    
    
    def handlerDialogLumensImportDatabase(self):
        """
        """
        self.openDialog(DialogLumensImportDatabase)
    
    
    def handlerDialogLumensPURCreateReferenceData(self):
        """
        """
        self.openDialog(DialogLumensPURCreateReferenceData)
    
    
    def handlerDialogLumensPURPreparePlanningUnit(self):
        """
        """
        self.openDialog(DialogLumensPURPreparePlanningUnit)
    
    
    def handlerDialogLumensPURReconcilePlanningUnit(self):
        """
        """
        self.openDialog(DialogLumensPURReconcilePlanningUnit)
    
    
    def handlerDialogLumensPURFinalization(self):
        """
        """
        self.openDialog(DialogLumensPURFinalization)
    
    
    def handlerDialogLumensPreQUESLandcoverChangeAnalysis(self):
        """
        """
        self.openDialog(DialogLumensPreQUESLandcoverChangeAnalysis)
    
    
    def handlerDialogLumensPreQUESLandcoverTrajectoriesAnalysis(self):
        """
        """
        self.openDialog(DialogLumensPreQUESLandcoverTrajectoriesAnalysis)
    
    
    def handlerDialogLumensQUESCCarbonAccounting(self):
        """
        """
        self.openDialog(DialogLumensQUESCCarbonAccounting)
    
    
    def handlerDialogLumensQUESCPeatlandCarbonAccounting(self):
        """
        """
        self.openDialog(DialogLumensQUESCPeatlandCarbonAccounting)
    
    
    def handlerDialogLumensQUESCSummarizeMultiplePeriod(self):
        """
        """
        self.openDialog(DialogLumensQUESCSummarizeMultiplePeriod)
    
    
    def handlerDialogLumensQUESBAnalysis(self):
        """
        """
        self.openDialog(DialogLumensQUESBAnalysis)
    
    
    def handlerDialogLumensTAAbacusOpportunityCost(self):
        """
        """
        self.openDialog(DialogLumensTAAbacusOpportunityCost)
    
    
    def handlerDialogLumensTAOpportunityCost(self):
        """
        """
        self.openDialog(DialogLumensTAOpportunityCost)
    
    
    def handlerDialogLumensTAOpportunityCostMap(self):
        """
        """
        self.openDialog(DialogLumensTAOpportunityCostMap)
    
    
    def handlerDialogLumensTARegionalEconomySingleIODescriptiveAnalysis(self):
        """
        """
        self.openDialog(DialogLumensTARegionalEconomySingleIODescriptiveAnalysis)
    
    
    def handlerDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis(self):
        """
        """
        self.openDialog(DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis)
    
    
    def handlerDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis(self):
        """
        """
        self.openDialog(DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis)
    
    
    def handlerDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis(self):
        """
        """
        self.openDialog(DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis)
    
    
    def handlerDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis(self):
        """
        """
        self.openDialog(DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis)
    
    
    def handlerDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis(self):
        """
        """
        self.openDialog(DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis)
    
    
    def handlerDialogLumensSCIENDODriversAnalysis(self):
        """
        """
        self.openDialog(DialogLumensSCIENDODriversAnalysis)
    
    
    def handlerDialogLumensSCIENDOBuildScenario(self):
        """
        """
        self.openDialog(DialogLumensSCIENDOBuildScenario)
    
    
    def handlerDialogLumensSCIENDOHistoricalBaselineProjection(self):
        """
        """
        self.openDialog(DialogLumensSCIENDOHistoricalBaselineProjection)
    
    
    def handlerDialogLumensSCIENDOHistoricalBaselineAnnualProjection(self):
        """
        """
        self.openDialog(DialogLumensSCIENDOHistoricalBaselineAnnualProjection)
    
    
    def handlerDialogLumensSCIENDOCalculateTransitionMatrix(self):
        """
        """
        self.openDialog(DialogLumensSCIENDOCalculateTransitionMatrix)
    
    
    def handlerDialogLumensSCIENDOCreateRasterCube(self):
        """
        """
        self.openDialog(DialogLumensSCIENDOCreateRasterCube)
    
    
    def handlerDialogLumensSCIENDOCalculateWeightofEvidence(self):
        """
        """
        self.openDialog(DialogLumensSCIENDOCalculateWeightofEvidence)
    
    
    def handlerDialogLumensSCIENDOSimulateLandUseChange(self):
        """
        """
        self.openDialog(DialogLumensSCIENDOSimulateLandUseChange)
    
    
    def handlerDialogLumensSCIENDOSimulateWithScenario(self):
        """
        """
        self.openDialog(DialogLumensSCIENDOSimulateWithScenario)
    
    
    def handlerDialogLumensToolsREDDAbacusSP(self):
        """
        """
        self.openDialog(DialogLumensToolsREDDAbacusSP)
    
    
    def checkDefaultBasemap(self):
        """
        """
        if os.path.isfile(self.appSettings['defaultBasemapFilePath']):
            return True
        else:
            return False
    
    
    def checkDefaultVector(self):
        """
        """
        if os.path.isfile(self.appSettings['defaultVectorFilePath']):
            return True
        else:
            return False
    
    
    def handlerZoomIn(self):
        """
        """
        self.mapCanvas.zoomIn()
    
    
    def handlerZoomOut(self):
        """
        """
        self.mapCanvas.zoomOut()
    
    
    def handlerZoomFull(self):
        """
        """
        self.mapCanvas.zoomToFullExtent()
    
    
    def handlerZoomLayer(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        self.mapCanvas.setExtent(self.qgsLayerList[layerItemData['layer']].extent())
        self.mapCanvas.refresh()
    
    
    def handlerZoomSelected(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        if layerItemData['layerType'] == 'vector':
            self.mapCanvas.setCurrentLayer(self.qgsLayerList[layerItemData['layer']])
            self.mapCanvas.zoomToSelected()
    
    
    def handlerPanSelected(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        if layerItemData['layerType'] == 'vector':
            self.mapCanvas.setCurrentLayer(self.qgsLayerList[layerItemData['layer']])
            self.mapCanvas.panToSelected()
    
    
    def handlerSetPanMode(self):
        """
        """
        self.actionPan.setChecked(True)
        self.actionSelect.setChecked(False)
        self.actionInfo.setChecked(False)
        self.mapCanvas.setMapTool(self.panTool)
    
    
    def handlerSetSelectMode(self):
        """
        """
        self.actionSelect.setChecked(True)
        self.actionPan.setChecked(False)
        self.actionInfo.setChecked(False)
        self.mapCanvas.setMapTool(self.selectTool)
    
    
    def handlerSetInfoMode(self):
        """
        """
        self.actionInfo.setChecked(True)
        self.actionPan.setChecked(False)
        self.actionSelect.setChecked(False)
        self.mapCanvas.setMapTool(self.infoTool)
    
    
    def loadDefaultLayers(self):
        """Replaces loadMap()
        """
        self.addLayer(self.appSettings['defaultBasemapFilePath'])
        ##self.addLayer(self.appSettings['defaultVectorFilePath'])
        self.mapCanvas.setExtent(self.appSettings['extentSEA'])
        ###self.mapCanvas.refresh()
        self.layoutBody.addWidget(self.mapCanvas)
    
    
    def loadMap(self):
        """DEBUG on-the-fly projection
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(cur_dir, 'data', 'basemap', 'basemap.tif')
        self.basemap_layer = QgsRasterLayer(filename, 'basemap')
        QgsMapLayerRegistry.instance().addMapLayer(self.basemap_layer)
        
        filename = os.path.join(cur_dir, 'data', 'vector', 'Paser_rtrwp2014_utm50s.shp')
        self.landmark_layer = QgsVectorLayer(filename, 'landmarks', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(self.landmark_layer)

        self.mapCanvas.setExtent(self.appSettings['extentSEA'])
        
        layers = []
        
        layers.append(QgsMapCanvasLayer(self.landmark_layer))
        layers.append(QgsMapCanvasLayer(self.basemap_layer))
        
        self.mapCanvas.setLayerSet(layers)
        
        self.layoutBody.addWidget(self.mapCanvas)
    
    
    def showVisibleLayers(self):
        """Find checked layers in layerlistmodel and add them to the mapcanvas layerset
        """
        layers = []
        i = 0
        
        while self.layerListModel.item(i):
            layerItem = self.layerListModel.item(i)
            layerItemData = layerItem.data()
            if layerItem.checkState():
                logging.getLogger(__name__).info('showing layer: %s', layerItem.text())
                layers.append(QgsMapCanvasLayer(self.qgsLayerList[layerItemData['layer']]))
            i += 1
        
        if i > 0:
            logging.getLogger(__name__).info('===========================================')
        
        self.mapCanvas.setLayerSet(layers)
    
    
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def handlerSelectLayer(self, layerItemIndex):
        """
        """
        self.actionDeleteLayer.setEnabled(True)
        
        # Check if selected layer is a vector
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        self.mapCanvas.setCurrentLayer(self.qgsLayerList[layerItemData['layer']])
        
        if layerItemData['layerType'] == 'vector':
            self.actionZoomLayer.setEnabled(True)
            self.actionLayerAttributeTable.setEnabled(True)
            self.actionFeatureSelectExpression.setEnabled(True)
        else:
            self.actionZoomLayer.setDisabled(True)
            self.actionLayerAttributeTable.setDisabled(True)
            self.actionFeatureSelectExpression.setDisabled(True)
        
        self.printDebugInfo()
    
    
    def handlerLayerAttributeTable(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        ##dialog = DialogLayerAttributeTable(self.qgsLayerList[layerItemData['layer']], self)
        dialog = DialogLayerAttributeDualView(self.qgsLayerList[layerItemData['layer']], self)
        dialog.exec_()
    
    
    def handlerFeatureSelectExpression(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        dialog = DialogFeatureSelectExpression(self.qgsLayerList[layerItemData['layer']], self)
        dialog.exec_()
    
    
    def handlerDropLayer(self):
        """On dropping a layer in the layer list
        """
        pass
    
    
    def handlerCheckLayer(self, layerItem):
        """
        """
        ##print 'DEBUG rowcount'
        ##print self.layerListModel.rowCount()
        
        # WORKAROUND for drag and drop reordering causing (count + 1) items in model
        QtCore.QTimer.singleShot(1, self.showVisibleLayers)
        
        """
        layerData = layerItem.data()
        if layerItem.checkState():
            QtGui.QMessageBox.information(self, 'Layer', 'Checked ' + layerData['layerName'])
        else:
            QtGui.QMessageBox.information(self, 'Layer', 'Unchecked ' + layerData['layerName'])
        """
    
    
    def handlerAddLayer(self):
        """
        """
        layerFormats = [self.appSettings['selectShapefileExt'], self.appSettings['selectRasterfileExt']]
        filterFormats = ' '.join(['*' + ext for ext in layerFormats])
        
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Vector/Raster File', QtCore.QDir.homePath(), 'Vector/Raster File ({0})'.format(filterFormats)))
        
        if file:
            self.addLayer(file)
    
    
    def addLayer(self, layerFile):
        """
        """
        if os.path.isfile(layerFile):
            layerName = os.path.basename(layerFile)
            
            # Check for existing layers with same file name
            existingLayerItems = self.layerListModel.findItems(layerName)
                
            for existingLayerItem in existingLayerItems:
                existingLayerData = existingLayerItem.data()
                if os.path.abspath(layerFile) == os.path.abspath(existingLayerData['layerFile']):
                    QtGui.QMessageBox.warning(self, 'Duplicate Layer', 'Layer "{0}" has already been added.\nPlease select another file.'.format(layerName))
                    return
            
            layer = None
            layerType = None
            fileExt = os.path.splitext(layerName)[1].lower()
            
            if  fileExt == '.shp':
                layerType = 'vector'
                layer = QgsVectorLayer(layerFile, layerName, 'ogr')
            elif fileExt == '.tif':
                layerType = 'raster'
                layer = QgsRasterLayer(layerFile, layerName)
            
            if not layer.isValid():
                print 'ERROR: Invalid layer!'
                return
            
            layerItemData = {
                'layerFile': layerFile,
                'layerName': layerName,
                'layerType': layerType,
                'layer': layerName,
            }
            
            # Can't keep raster/vector object in layerItemData because of object copy error upon drag-drop
            self.qgsLayerList[layerName] = layer
            
            layerItem = QtGui.QStandardItem(layerName)
            layerItem.setData(layerItemData)
            layerItem.setToolTip(layerFile)
            layerItem.setEditable(False)
            layerItem.setCheckable(True)
            layerItem.setDragEnabled(True)
            layerItem.setDropEnabled(False)
            layerItem.setCheckState(QtCore.Qt.Checked)
            self.layerListModel.appendRow(layerItem)
            
            QgsMapLayerRegistry.instance().addMapLayer(self.qgsLayerList[layerName])
            # FIX 20151118:
            # since on-the-fly CRS reprojection is enabled no need to set layer CRS
            # setting canvas extent to layer extent causes canvas to turn blank
            ###self.qgsLayerList[layerName].setCrs(QgsCoordinateReferenceSystem(self.appSettings['defaultCRS'], QgsCoordinateReferenceSystem.EpsgCrsId))
            ###self.mapCanvas.setExtent(self.qgsLayerList[layerName].extent())
            self.showVisibleLayers()
    
    
    def handlerDeleteLayer(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        del self.qgsLayerList[layerItemData['layer']]
        ##QtGui.QMessageBox.information(self, 'Layer', layerItemData)
        self.layerListModel.removeRow(layerItemIndex.row())
        
        self.showVisibleLayers()
        
        if not self.layerListModel.rowCount():
            self.actionDeleteLayer.setDisabled(True)
            self.actionZoomLayer.setDisabled(True)
            return
        
        # Check type of next selected item
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        
        if layerItemData['layerType'] == 'vector':
            self.actionZoomLayer.setEnabled(True)
            self.actionLayerAttributeTable.setEnabled(True)
            self.actionFeatureSelectExpression.setEnabled(True)
        else:
            self.actionZoomLayer.setDisabled(True)
            self.actionLayerAttributeTable.setDisabled(True)
            self.actionFeatureSelectExpression.setDisabled(True)
    
    
    def handlerRefresh(self):
        """
        """
        self.mapCanvas.refresh()
    
    
    def handlerZoomLast(self):
        """
        """
        self.mapCanvas.zoomToPreviousExtent()
    
    
    def handlerZoomNext(self):
        """
        """
        self.mapCanvas.zoomToNextExtent()
    
    
    def handlerZoomLastStatus(self, status):
        """
        """
        if status:
            self.actionZoomLast.setEnabled(True)
        else:
            self.actionZoomLast.setDisabled(True)
    
    
    def handlerZoomNextStatus(self, status):
        """
        """
        if status:
            self.actionZoomNext.setEnabled(True)
        else:
            self.actionZoomNext.setDisabled(True)
    
    
    def printDebugInfo(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        
        logging.getLogger(__name__).info('DEBUG INFO ===================================')
        logging.getLogger(__name__).info('MapCanvas layer count: ' + str(self.mapCanvas.layerCount()))
        logging.getLogger(__name__).info('MapCanvas destination CRS: ' + self.mapCanvas.mapRenderer().destinationCrs().authid())
        logging.getLogger(__name__).info('On-the-fly projection enabled: ' + str(self.mapCanvas.hasCrsTransformEnabled()))
        logging.getLogger(__name__).info('Selected layer CRS: ' + self.qgsLayerList[layerItemData['layer']].crs().authid())


#############################################################################


class SelectTool(QgsMapToolIdentify):
    def __init__(self, window):
        QgsMapToolIdentify.__init__(self, window.mapCanvas)
        self.window = window
        self.setCursor(QtCore.Qt.ArrowCursor)
    
    
    def canvasReleaseEvent(self, event):
        """
        """
        found_features = self.identify(event.x(), event.y(), self.TopDownStopAtFirst, self.VectorLayer)
        if len(found_features) > 0:
            layer = found_features[0].mLayer
            feature = found_features[0].mFeature
            geometry = feature.geometry()

            if event.modifiers() & QtCore.Qt.ShiftModifier:
                layer.select(feature.id())
            else:
                layer.setSelectedFeatures([feature.id()])
        else:
            for layerName, layer in self.window.qgsLayerList.iteritems():
                if layer.type() == QgsMapLayer.VectorLayer:
                    layer.removeSelection()


#############################################################################


class InfoTool(QgsMapToolIdentify):
    def __init__(self, window):
        QgsMapToolIdentify.__init__(self, window.mapCanvas)
        self.window = window
    
    
    def canvasReleaseEvent(self, event):
        """
        """
        found_features = self.identify(event.x(), event.y(), self.TopDownStopAtFirst, self.VectorLayer)
        
        if len(found_features) > 0:
            layer = found_features[0].mLayer
            feature = found_features[0].mFeature
            geometry = feature.geometry()
            
            info = []
            
            layerDataProvider = layer.dataProvider()
            
            if not layerDataProvider.isValid():
                print 'ERROR: Invalid data provider!'
                return
            
            for field in layerDataProvider.fields():
                info.append(field.name() + ':\t' + str(feature.attribute(field.name())))
            
            msgBoxFeatureInfo = DetailedMessageBox(self.window)
            msgBoxFeatureInfo.setWindowTitle('Feature Info')
            msgBoxFeatureInfo.setText(layer.name())
            msgBoxFeatureInfo.setDetailedText("\n".join(info))
            ##msgBoxFeatureInfo.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            ##msgBoxFeatureInfo.setSizeGripEnabled(True)
            msgBoxFeatureInfo.exec_()


#############################################################################


class PanTool(QgsMapTool):
    def __init__(self, mapCanvas):
        QgsMapTool.__init__(self, mapCanvas)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.dragging = False
    
    
    def canvasMoveEvent(self, event):
        """
        """
        if event.buttons() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.canvas().panAction(event)
    
    
    def canvasReleaseEvent(self, event):
        """
        """
        if event.button() == QtCore.Qt.LeftButton and self.dragging:
            self.canvas().panActionEnd(event.pos())
            self.dragging = False


#############################################################################


def main():
    window = MainWindow()
    window.show()
    window.raise_()
    
    if window.checkDefaultBasemap():
        window.loadDefaultLayers()
        ##window.loadMap() # DEBUG on-the-fly projection
    
    # Pan mode by default
    window.handlerSetPanMode()
    
    app.setWindowIcon(QtGui.QIcon('ui/icons/app.ico'))
    app.exec_()
    app.deleteLater()
    
    QgsApplication.exitQgis()


#############################################################################


if __name__ == "__main__":
    main()

