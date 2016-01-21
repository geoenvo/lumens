#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, platform, sys, logging, subprocess, argparse

from qgis.core import *
from qgis.gui import *
from PyQt4 import QtGui, QtCore

import resource

QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX'], True) # The True value is important
QgsApplication.initQgis()

app = QtGui.QApplication(sys.argv)

##splashLabel = QtGui.QLabel('<font color=blue size=72><b>{0}</b></font>'.format('Loading'))
##splashLabel.setWindowFlags(QtCore.Qt.SplashScreen|QtCore.Qt.WindowStaysOnTopHint)
##splashLabel.show()

splashImage = QtGui.QPixmap('ui/images/splash.png')
splashScreen = QtGui.QSplashScreen(splashImage, QtCore.Qt.WindowStaysOnTopHint)
splashScreen.setMask(splashImage.mask())
splashScreen.show()

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

##splashLabel.close()

from utils import QPlainTextEditLogger, DetailedMessageBox
from dialog_layer_attribute_table import DialogLayerAttributeTable
from dialog_feature_selectexpression import DialogFeatureSelectExpression
from dialog_layer_attribute_dualview import DialogLayerAttributeDualView
from dialog_lumens_viewer import DialogLumensViewer

from dialog_lumens_createdatabase import DialogLumensCreateDatabase
from dialog_lumens_opendatabase import DialogLumensOpenDatabase
from dialog_lumens_importdatabase import DialogLumensImportDatabase
from dialog_lumens_adddata import DialogLumensAddData

from dialog_lumens_addlandcoverraster import DialogLumensAddLandcoverRaster
from dialog_lumens_addpeatdata import DialogLumensAddPeatData
from dialog_lumens_addfactordata import DialogLumensAddFactorData
from dialog_lumens_addplanningunitdata import DialogLumensAddPlanningUnitData

from dialog_lumens_pur import DialogLumensPUR

from dialog_lumens_pur_createreferencedata import DialogLumensPURCreateReferenceData
from dialog_lumens_pur_prepareplanningunit import DialogLumensPURPreparePlanningUnit
from dialog_lumens_pur_reconcileplanningunit import DialogLumensPURReconcilePlanningUnit
from dialog_lumens_pur_finalization import DialogLumensPURFinalization
from dialog_lumens_preques_landcoverchangeanalysis import DialogLumensPreQUESLandcoverChangeAnalysis
from dialog_lumens_preques_landcovertrajectoriesanalysis import DialogLumensPreQUESLandcoverTrajectoriesAnalysis

from dialog_lumens_ques import DialogLumensQUES

from dialog_lumens_quesc_carbonaccounting import DialogLumensQUESCCarbonAccounting
from dialog_lumens_quesc_peatlandcarbonaccounting import DialogLumensQUESCPeatlandCarbonAccounting
from dialog_lumens_quesc_summarizemultipleperiod import DialogLumensQUESCSummarizeMultiplePeriod
from dialog_lumens_quesb_analysis import DialogLumensQUESBAnalysis
from dialog_lumens_quesh_watershedmodelevaluation import DialogLumensQUESHWatershedModelEvaluation
from dialog_lumens_quesh_watershedindicators import DialogLumensQUESHWatershedIndicators
from dialog_lumens_quesh_dominanthru import DialogLumensQUESHDominantHRU
from dialog_lumens_quesh_multiplehru import DialogLumensQUESHMultipleHRU
from dialog_lumens_quesh_dominantlussl import DialogLumensQUESHDominantLUSSL

from dialog_lumens_ta_opportunitycost import DialogLumensTAOpportunityCost
from dialog_lumens_ta_regionaleconomy import DialogLumensTARegionalEconomy

from dialog_lumens_ta_abacusopportunitycostcurve import DialogLumensTAAbacusOpportunityCostCurve
from dialog_lumens_ta_opportunitycostcurve import DialogLumensTAOpportunityCostCurve
from dialog_lumens_ta_opportunitycostmap import DialogLumensTAOpportunityCostMap
from dialog_lumens_ta_resioda import DialogLumensTARegionalEconomySingleIODescriptiveAnalysis
from dialog_lumens_ta_retsioda import DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis
from dialog_lumens_ta_landdistribreq import DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis
from dialog_lumens_ta_impactlanduse import DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis
from dialog_lumens_ta_finaldemandscenario import DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis
from dialog_lumens_ta_gdpscenario import DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis

from dialog_lumens_sciendo import DialogLumensSCIENDO

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

__version__ = '1.0.0'

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
        """
        super(MainWindow, self).__init__(parent)
        
        # Default settings for each LUMENS dialog
        self.appSettings = {
            'debug': False,
            'appDir': os.path.dirname(os.path.realpath(__file__)),
            'appSettingsFile': 'settings.ini',
            'ROutFile': os.path.join(system.userFolder(), 'processing_script.r.Rout'),
            'guideFile': 'guide.pdf',
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
            'defaultExtent': QgsRectangle(95, -11, 140, 11), # Southeast Asia extent
            'defaultCRS': 4326, # EPSG 4326 - WGS 84
            'folderPUR': 'PUR', # Used for template path
            'folderQUES': 'QUES',
            'folderTA': 'TA',
            'folderSCIENDO': 'SCIENDO',
            'acceptedDocumentFormats': ('.doc', 'docx', '.rtf', '.xls', '.xlsx', '.txt', '.log', '.csv'),
            'acceptedWebFormats': ('.html', '.htm'),
            'acceptedSpatialFormats': ('.shp', '.tif'),
            
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
            'DialogLumensPUR': {
                'shapefile': '',
                'shapefileAttr': '',
                'dataTitle': '',
                'referenceClasses': '',
                'referenceMapping': '',
                'planningUnits': '',
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
                'csvLandUse': '',
                'nodata': '',
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
            'DialogLumensQUESHWatershedModelEvaluation': {
                'dateInitial': '',
                'dateFinal': '',
                'SWATModel': '',
                'location': '',
                'outletReachSubBasinID': '',
                'observedDebitFile': '',
                'outputWatershedModelEvaluation': '',
            },
            'DialogLumensQUESHWatershedIndicators': {
                'SWATTXTINOUTDir': '',
                'dateInitial': '',
                'dateFinal': '',
                'subWatershedPolygon': '',
                'location': '',
                'subWatershedOutput': '',
                'outputInitialYearSubWatershedLevelIndicators': '',
                'outputFinalYearSubWatershedLevelIndicators': '',
            },
            'DialogLumensQUESHDominantHRU': {
                'landUseMap': '',
                'soilMap': '',
                'slopeMap': '',
                'subcatchmentMap': '',
                'landUseClassification': '',
                'soilClassification': '',
                'slopeClassification': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensQUESHDominantLUSSL': {
                'landUseMap': '',
                'soilMap': '',
                'slopeMap': '',
                'subcatchmentMap': '',
                'landUseClassification': '',
                'soilClassification': '',
                'slopeClassification': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensQUESHMultipleHRU': {
                'landUseMap': '',
                'soilMap': '',
                'slopeMap': '',
                'subcatchmentMap': '',
                'landUseClassification': '',
                'soilClassification': '',
                'slopeClassification': '',
                'areaName': '',
                'period': '',
                'landUseThreshold': '',
                'soilThreshold': '',
                'slopeThreshold': '',
            },
            'DialogLumensTAAbacusOpportunityCostCurve': {
                'projectFile': '',
            },
            'DialogLumensTAOpportunityCostCurve': {
                'csvNPVTable': '',
                'costThreshold': '',
                'outputOpportunityCostDatabase': '',
                'outputOpportunityCostReport': '',
            },
            'DialogLumensTAOpportunityCostMap': {
                'csvProfitability': '',
            },
            'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis': {
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
        
        self.appSettings['defaultBasemapFilePath'] = os.path.join(self.appSettings['appDir'], self.appSettings['dataDir'], self.appSettings['basemapDir'], self.appSettings['defaultBasemapFile'])
        self.appSettings['defaultVectorFilePath'] = os.path.join(self.appSettings['appDir'], self.appSettings['dataDir'], self.appSettings['vectorDir'], self.appSettings['defaultVectorFile'])
        
        # For keeping track of open dialogs
        self.openDialogs = []
        
        # Recently opened LUMENS project databases
        self.recentProjects = []
        
        # Process app arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--debug', action='store_true', help='Show the logging widget')
        
        args = parser.parse_args()
        
        if args.debug:
            self.appSettings['debug'] = True
        
        # Load the app settings
        self.loadSettings()
        
        # Build the mainwindow UI!
        self.setupUi()
        
        if args.debug:
            # Init the logger for mainwindow
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.log_box.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.addHandler(self.log_box)
            self.logger.setLevel(logging.DEBUG)
        
        self.installEventFilter(self)
        
        # File menu updating
        self.fileMenu.aboutToShow.connect(self.updateFileMenu)
        
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
        
        # Project treeview doubleclick item handling
        self.projectTreeView.doubleClicked.connect(self.handlerDoubleClickProjectTree)
        
        # App action handlers
        self.actionQuit.triggered.connect(self.close)
        self.actionToggleSidebar.triggered.connect(self.handlerToggleSidebar)
        self.actionToggleToolbar.triggered.connect(self.handlerToggleToolbar)
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
        self.mapCanvas.xyCoordinates.connect(self.handlerUpdateCoordinates)
        self.actionZoomLast.triggered.connect(self.handlerZoomLast)
        self.actionZoomNext.triggered.connect(self.handlerZoomNext)
        self.actionLayerAttributeTable.triggered.connect(self.handlerLayerAttributeTable)
        self.actionFeatureSelectExpression.triggered.connect(self.handlerFeatureSelectExpression)
        self.layerListView.customContextMenuRequested.connect(self.handlerLayerItemContextMenu)
        
        # Dashboard tab
        self.radioQUESHHRUDefinition.toggled.connect(lambda:self.handlerToggleQUESH(self.radioQUESHHRUDefinition))
        self.radioQUESHWatershedModelEvaluation.toggled.connect(lambda:self.handlerToggleQUESH(self.radioQUESHWatershedModelEvaluation))
        self.radioQUESHWatershedIndicators.toggled.connect(lambda:self.handlerToggleQUESH(self.radioQUESHWatershedIndicators))
        self.radioQUESHHRUDefinition.click()
        self.radioTAOpportunityCostAbacus.toggled.connect(lambda:self.handlerToggleTAOpportunityCost(self.radioTAOpportunityCostAbacus))
        self.radioTAOpportunityCostCurve.toggled.connect(lambda:self.handlerToggleTAOpportunityCost(self.radioTAOpportunityCostCurve))
        self.radioTAOpportunityCostMap.toggled.connect(lambda:self.handlerToggleTAOpportunityCost(self.radioTAOpportunityCostMap))
        self.radioTAOpportunityCostAbacus.click()
        self.radioTARegionalEconomyDescriptiveAnalysis.toggled.connect(lambda:self.handlerToggleTARegionalEconomy(self.radioTARegionalEconomyDescriptiveAnalysis))
        self.radioTARegionalEconomyRegionalEconomicScenarioImpact.toggled.connect(lambda:self.handlerToggleTARegionalEconomy(self.radioTARegionalEconomyRegionalEconomicScenarioImpact))
        self.radioTARegionalEconomyLandRequirementAnalysis.toggled.connect(lambda:self.handlerToggleTARegionalEconomy(self.radioTARegionalEconomyLandRequirementAnalysis))
        self.radioTARegionalEconomyLandUseChangeImpact.toggled.connect(lambda:self.handlerToggleTARegionalEconomy(self.radioTARegionalEconomyLandUseChangeImpact))
        self.radioTARegionalEconomyDescriptiveAnalysis.click()
        
        # LUMENS action handlers
        # Database menu
        self.actionDialogLumensCreateDatabase.triggered.connect(self.handlerDialogLumensCreateDatabase)
        self.actionLumensOpenDatabase.triggered.connect(self.handlerLumensOpenDatabase)
        self.actionLumensCloseDatabase.triggered.connect(self.handlerLumensCloseDatabase)
        self.actionLumensDatabaseStatus.triggered.connect(self.handlerLumensDatabaseStatus)
        self.actionDialogLumensAddData.triggered.connect(self.handlerDialogLumensAddData)
        
        self.actionDialogLumensAddLandcoverRaster.triggered.connect(self.handlerDialogLumensAddLandcoverRaster)
        self.actionDialogLumensAddPeatData.triggered.connect(self.handlerDialogLumensAddPeatData)
        self.actionDialogLumensAddFactorData.triggered.connect(self.handlerDialogLumensAddFactorData)
        self.actionDialogLumensAddPlanningUnitData.triggered.connect(self.handlerDialogLumensAddPlanningUnitData)
        self.actionLumensDeleteData.triggered.connect(self.handlerLumensDeleteData)
        self.actionDialogLumensImportDatabase.triggered.connect(self.handlerDialogLumensImportDatabase)
        
        # PUR menu
        self.actionDialogLumensPUR.triggered.connect(self.handlerDialogLumensPUR)
        
        self.actionDialogLumensPURCreateReferenceData.triggered.connect(self.handlerDialogLumensPURCreateReferenceData)
        self.actionDialogLumensPURPreparePlanningUnit.triggered.connect(self.handlerDialogLumensPURPreparePlanningUnit)
        self.actionDialogLumensPURReconcilePlanningUnit.triggered.connect(self.handlerDialogLumensPURReconcilePlanningUnit)
        self.actionDialogLumensPURFinalization.triggered.connect(self.handlerDialogLumensPURFinalization)
        
        # QUES menu
        self.actionDialogLumensQUES.triggered.connect(self.handlerDialogLumensQUES)
        
        self.actionDialogLumensPreQUESLandcoverChangeAnalysis.triggered.connect(self.handlerDialogLumensPreQUESLandcoverChangeAnalysis)
        self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis.triggered.connect(self.handlerDialogLumensPreQUESLandcoverTrajectoriesAnalysis)
        self.actionDialogLumensQUESCCarbonAccounting.triggered.connect(self.handlerDialogLumensQUESCCarbonAccounting)
        self.actionDialogLumensQUESCPeatlandCarbonAccounting.triggered.connect(self.handlerDialogLumensQUESCPeatlandCarbonAccounting)
        self.actionDialogLumensQUESCSummarizeMultiplePeriod.triggered.connect(self.handlerDialogLumensQUESCSummarizeMultiplePeriod)
        self.actionDialogLumensQUESBAnalysis.triggered.connect(self.handlerDialogLumensQUESBAnalysis)
        self.actionDialogLumensQUESHWatershedModelEvaluation.triggered.connect(self.handlerDialogLumensQUESHWatershedModelEvaluation)
        self.actionDialogLumensQUESHWatershedIndicators.triggered.connect(self.handlerDialogLumensQUESHWatershedIndicators)
        self.actionDialogLumensQUESHDominantHRU.triggered.connect(self.handlerDialogLumensQUESHDominantHRU)
        self.actionDialogLumensQUESHDominantLUSSL.triggered.connect(self.handlerDialogLumensQUESHDominantLUSSL)
        self.actionDialogLumensQUESHMultipleHRU.triggered.connect(self.handlerDialogLumensQUESHMultipleHRU)
        
        # TA menu
        self.actionDialogLumensTAOpportunityCost.triggered.connect(self.handlerDialogLumensTAOpportunityCost)
        self.actionDialogLumensTARegionalEconomy.triggered.connect(self.handlerDialogLumensTARegionalEconomy)
        
        self.actionDialogLumensTAAbacusOpportunityCostCurve.triggered.connect(self.handlerDialogLumensTAAbacusOpportunityCostCurve)
        self.actionDialogLumensTAOpportunityCostCurve.triggered.connect(self.handlerDialogLumensTAOpportunityCostCurve)
        self.actionDialogLumensTAOpportunityCostMap.triggered.connect(self.handlerDialogLumensTAOpportunityCostMap)
        self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomySingleIODescriptiveAnalysis)
        self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis)
        self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis)
        self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.triggered.connect(self.handlerDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis)
        self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis)
        self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.triggered.connect(self.handlerDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDO.triggered.connect(self.handlerDialogLumensSCIENDO)
        
        self.actionDialogLumensSCIENDODriversAnalysis.triggered.connect(self.handlerDialogLumensSCIENDODriversAnalysis)
        self.actionDialogLumensSCIENDOBuildScenario.triggered.connect(self.handlerDialogLumensSCIENDOBuildScenario)
        self.actionDialogLumensSCIENDOHistoricalBaselineProjection.triggered.connect(self.handlerDialogLumensSCIENDOHistoricalBaselineProjection)
        self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection.triggered.connect(self.handlerDialogLumensSCIENDOHistoricalBaselineAnnualProjection)
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix.triggered.connect(self.handlerDialogLumensSCIENDOCalculateTransitionMatrix)
        self.actionDialogLumensSCIENDOCreateRasterCube.triggered.connect(self.handlerDialogLumensSCIENDOCreateRasterCube)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence.triggered.connect(self.handlerDialogLumensSCIENDOCalculateWeightofEvidence)
        self.actionDialogLumensSCIENDOSimulateLandUseChange.triggered.connect(self.handlerDialogLumensSCIENDOSimulateLandUseChange)
        self.actionDialogLumensSCIENDOSimulateWithScenario.triggered.connect(self.handlerDialogLumensSCIENDOSimulateWithScenario)
        
        # Dashboard tab QPushButtons
        self.buttonProcessPURTemplate.clicked.connect(self.handlerProcessPURTemplate)
        self.buttonProcessPreQUESTemplate.clicked.connect(self.handlerProcessPreQUESTemplate)
        self.buttonProcessQUESCTemplate.clicked.connect(self.handlerProcessQUESCTemplate)
        self.buttonProcessQUESBTemplate.clicked.connect(self.handlerProcessQUESBTemplate)
        self.buttonProcessQUESHTemplate.clicked.connect(self.handlerProcessQUESHTemplate)
        self.buttonProcessTAOpportunityCostTemplate.clicked.connect(self.handlerProcessTAOpportunityCostTemplate)
        self.buttonProcessTARegionalEconomyTemplate.clicked.connect(self.handlerProcessTARegionalEconomyTemplate)
        self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        self.buttonProcessSCIENDOLandUseChangeModelingTemplate.clicked.connect(self.handlerProcessSCIENDOLandUseChangeModelingTemplate)
        
        # About menu
        self.actionDialogLumensGuide.triggered.connect(self.handlerDialogLumensGuide)
        self.actionDialogLumensAbout.triggered.connect(self.handlerDialogLumensAbout)
        
        # Tools menu
        self.actionDialogLumensToolsREDDAbacusSP.triggered.connect(self.handlerDialogLumensToolsREDDAbacusSP)
    
    
    def setupUi(self):
        """
        """
        self.setWindowTitle('LUMENS v {0}'.format(__version__))

        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setMinimumSize(1024, 600)
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
        self.aboutMenu = self.menubar.addMenu('&About')
        ###self.toolsMenu = self.menubar.addMenu('T&ools')

        self.toolBar = QtGui.QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        
        self.statusBar = QtGui.QStatusBar(self)
        self.statusBar.setSizeGripEnabled(False)
        ##self.statusBar.setStyleSheet('QStatusBar { background: green; } QStatusBar::item { background: blue; margin-right: 11px; }')
        ##self.statusBar.setFixedHeight(10)
        ##self.labelLayerCRS = QtGui.QLabel(self)
        ##self.labelLayerCRS.setText('...')
        ##self.statusBar.addPermanentWidget(self.labelLayerCRS)
        self.labelMapCanvasCoordinate = QtGui.QLabel(self)
        self.labelMapCanvasCoordinate.setStyleSheet('QLabel { margin-right: 11px; }')
        self.labelMapCanvasCoordinate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.statusBar.addPermanentWidget(self.labelMapCanvasCoordinate)
        self.setStatusBar(self.statusBar)
        
        # Create the actions and assigned them to the menus
        self.actionQuit = QtGui.QAction('Quit', self)
        self.actionQuit.setShortcut(QtGui.QKeySequence.Quit)
        
        self.actionToggleSidebar = QtGui.QAction('Sidebar', self)
        self.actionToggleSidebar.setCheckable(True)
        self.actionToggleSidebar.setChecked(True)
        
        self.actionToggleToolbar = QtGui.QAction('Toolbar', self)
        self.actionToggleToolbar.setCheckable(True)
        self.actionToggleToolbar.setChecked(True)
        
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
        
        self.viewMenu.addAction(self.actionToggleSidebar)
        self.viewMenu.addAction(self.actionToggleToolbar)
        self.viewMenu.addSeparator()
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
        self.actionLumensDatabaseStatus = QtGui.QAction('LUMENS database status', self)
        self.actionDialogLumensAddData = QtGui.QAction('Add data to LUMENS database', self)
        self.actionLumensDeleteData = QtGui.QAction('Delete LUMENS data', self)
        self.actionDialogLumensImportDatabase = QtGui.QAction('Import LUMENS database', self)
        
        self.actionDialogLumensAddLandcoverRaster = QtGui.QAction('Add land use/cover data', self)
        self.actionDialogLumensAddPeatData = QtGui.QAction('Add peat data', self)
        self.actionDialogLumensAddFactorData = QtGui.QAction('Add factor data', self)
        self.actionDialogLumensAddPlanningUnitData = QtGui.QAction('Add planning unit data', self)
        
        self.databaseMenu.addAction(self.actionDialogLumensCreateDatabase)
        self.databaseMenu.addAction(self.actionLumensOpenDatabase)
        self.databaseMenu.addAction(self.actionLumensCloseDatabase)
        self.databaseMenu.addAction(self.actionLumensDatabaseStatus)
        self.databaseMenu.addAction(self.actionDialogLumensAddData)
        ####self.addDataMenu = self.databaseMenu.addMenu('Add data to LUMENS database')
        ####self.addDataMenu.addAction(self.actionDialogLumensAddLandcoverRaster)
        ####self.addDataMenu.addAction(self.actionDialogLumensAddPeatData)
        ####self.addDataMenu.addAction(self.actionDialogLumensAddFactorData)
        ####self.addDataMenu.addAction(self.actionDialogLumensAddPlanningUnitData)
        self.databaseMenu.addAction(self.actionLumensDeleteData)
        self.databaseMenu.addAction(self.actionDialogLumensImportDatabase)
        
        # PUR menu
        self.actionDialogLumensPUR = QtGui.QAction('Planning Unit Reconciliation', self)
        
        self.actionDialogLumensPURCreateReferenceData = QtGui.QAction('Create reference data', self)
        self.actionDialogLumensPURPreparePlanningUnit = QtGui.QAction('Prepare planning unit', self)
        self.actionDialogLumensPURReconcilePlanningUnit = QtGui.QAction('Reconcile planning unit', self)
        self.actionDialogLumensPURFinalization = QtGui.QAction('Finalization', self)
        
        ####self.functionsBasedReconciliationMenu = self.purMenu.addMenu('Functions-based Reconciliation')
        self.purMenu.addAction(self.actionDialogLumensPUR)
        ####self.functionsBasedReconciliationMenu.addAction(self.actionDialogLumensPURCreateReferenceData)
        ####self.functionsBasedReconciliationMenu.addAction(self.actionDialogLumensPURPreparePlanningUnit)
        ####self.functionsBasedReconciliationMenu.addAction(self.actionDialogLumensPURReconcilePlanningUnit)
        ####self.functionsBasedReconciliationMenu.addAction(self.actionDialogLumensPURFinalization)
        
        # QUES menu
        self.actionDialogLumensQUES = QtGui.QAction('Quantification Environmental Services', self)
        
        self.actionDialogLumensPreQUESLandcoverChangeAnalysis = QtGui.QAction('Land cover change analysis', self)
        self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis = QtGui.QAction('Land cover trajectories analysis', self)
        self.actionDialogLumensQUESCCarbonAccounting = QtGui.QAction('Carbon accounting', self)
        self.actionDialogLumensQUESCPeatlandCarbonAccounting = QtGui.QAction('Peatland carbon accounting', self)
        self.actionDialogLumensQUESCSummarizeMultiplePeriod = QtGui.QAction('Summarize multiple period', self)
        self.actionDialogLumensQUESBAnalysis = QtGui.QAction('QUES-B Analysis', self)
        self.actionDialogLumensQUESHWatershedModelEvaluation = QtGui.QAction('Watershed model evaluation', self)
        self.actionDialogLumensQUESHWatershedIndicators = QtGui.QAction('Watershed indicators', self)
        self.actionDialogLumensQUESHDominantHRU = QtGui.QAction('Dominant HRU', self)
        self.actionDialogLumensQUESHDominantLUSSL = QtGui.QAction('Dominant land use, soil, and slope', self)
        self.actionDialogLumensQUESHMultipleHRU = QtGui.QAction('Multiple HRU', self)
        
        ####self.preQUESMenu = self.quesMenu.addMenu('Pre-QUES')
        ####self.QUESCMenu = self.quesMenu.addMenu('QUES-C')
        ####self.QUESBMenu = self.quesMenu.addMenu('QUES-B')
        ####self.QUESHMenu = self.quesMenu.addMenu('QUES-H')
        self.quesMenu.addAction(self.actionDialogLumensQUES)
        ####self.HRUDefMenu = self.QUESHMenu.addMenu('Hydrological Response Unit Definition')
        ####self.preQUESMenu.addAction(self.actionDialogLumensPreQUESLandcoverChangeAnalysis)
        ####self.preQUESMenu.addAction(self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis)
        ####self.QUESCMenu.addAction(self.actionDialogLumensQUESCCarbonAccounting)
        ####self.QUESCMenu.addAction(self.actionDialogLumensQUESCPeatlandCarbonAccounting)
        ####self.QUESCMenu.addAction(self.actionDialogLumensQUESCSummarizeMultiplePeriod)
        ####self.QUESBMenu.addAction(self.actionDialogLumensQUESBAnalysis)
        ####self.QUESHMenu.addAction(self.actionDialogLumensQUESHWatershedModelEvaluation)
        ####self.QUESHMenu.addAction(self.actionDialogLumensQUESHWatershedIndicators)
        ####self.HRUDefMenu.addAction(self.actionDialogLumensQUESHDominantHRU)
        ####self.HRUDefMenu.addAction(self.actionDialogLumensQUESHDominantLUSSL)
        ####self.HRUDefMenu.addAction(self.actionDialogLumensQUESHMultipleHRU)
        
        # TA menu
        self.actionDialogLumensTAOpportunityCost = QtGui.QAction('Trade-off Analysis [Opportunity Cost]', self)
        self.actionDialogLumensTARegionalEconomy = QtGui.QAction('Trade-off Analysis [Regional Economy]', self)
        
        self.actionDialogLumensTAAbacusOpportunityCostCurve = QtGui.QAction('Abacus opportunity cost curve', self)
        self.actionDialogLumensTAOpportunityCostCurve = QtGui.QAction('Opportunity cost curve', self)
        self.actionDialogLumensTAOpportunityCostMap = QtGui.QAction('Opportunity cost map', self)
        self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis = QtGui.QAction('Descriptive analysis of regional economy (single time series)', self)
        self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis = QtGui.QAction('Descriptive analysis of regional economy (multiple time series)', self)
        self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis = QtGui.QAction('Land requirement analysis', self)
        self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis = QtGui.QAction('Impact of land use change to regional economy', self)
        self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis = QtGui.QAction('Impact of regional economic scenario to land use change (final demand scenario)', self)
        self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis = QtGui.QAction('Impact of regional economic scenario to land use change (GDP scenario)', self)
        
        ####self.opportunityCostMenu = self.taMenu.addMenu('Opportunity cost')
        ####self.regionalEconomyMenu = self.taMenu.addMenu('Regional economy')
        self.taMenu.addAction(self.actionDialogLumensTAOpportunityCost)
        self.taMenu.addAction(self.actionDialogLumensTARegionalEconomy)
        ####self.opportunityCostMenu.addAction(self.actionDialogLumensTAAbacusOpportunityCostCurve)
        ####self.opportunityCostMenu.addAction(self.actionDialogLumensTAOpportunityCostCurve)
        ####self.opportunityCostMenu.addAction(self.actionDialogLumensTAOpportunityCostMap)
        ####self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis)
        ####self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis)
        ####self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis)
        ####self.regionalEconomyMenu.addAction(self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis)
        ####self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis)
        ####self.regionalEconomyMenu.addAction(self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDO = QtGui.QAction('SCIENDO', self)
        
        self.actionDialogLumensSCIENDODriversAnalysis = QtGui.QAction('Drivers analysis', self)
        self.actionDialogLumensSCIENDOBuildScenario = QtGui.QAction('Build scenario', self)
        self.actionDialogLumensSCIENDOHistoricalBaselineProjection = QtGui.QAction('Historical baseline projection', self)
        self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection = QtGui.QAction('Historical baseline annual projection', self)
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix = QtGui.QAction('Calculate transition matrix', self)
        self.actionDialogLumensSCIENDOCreateRasterCube = QtGui.QAction('Create raster cube of factors', self)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence = QtGui.QAction('Calculate weight of evidence', self)
        self.actionDialogLumensSCIENDOSimulateLandUseChange = QtGui.QAction('Simulate land use change', self)
        self.actionDialogLumensSCIENDOSimulateWithScenario = QtGui.QAction('Simulate with scenario', self)
        
        ####self.lowEmissionDevelopmentMenu = self.sciendoMenu.addMenu('Low emission development analysis')
        ####self.landUseChangeModelingMenu = self.sciendoMenu.addMenu('Land use change modeling')
        self.sciendoMenu.addAction(self.actionDialogLumensSCIENDO)
        ####self.historicalBaselineMenu = self.lowEmissionDevelopmentMenu.addMenu('Historical baseline')
        ####self.historicalBaselineMenu.addAction(self.actionDialogLumensSCIENDOHistoricalBaselineProjection)
        ####self.historicalBaselineMenu.addAction(self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection)
        ####self.lowEmissionDevelopmentMenu.addAction(self.actionDialogLumensSCIENDODriversAnalysis)
        ####self.lowEmissionDevelopmentMenu.addAction(self.actionDialogLumensSCIENDOBuildScenario)
        ####self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCalculateTransitionMatrix)
        ####self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCreateRasterCube)
        ####self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCalculateWeightofEvidence)
        ####self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOSimulateLandUseChange)
        ####self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOSimulateWithScenario)
        
        # About menu
        self.actionDialogLumensAbout = QtGui.QAction('About LUMENS', self)
        self.actionDialogLumensGuide = QtGui.QAction('Open Guide', self)
        
        self.aboutMenu.addAction(self.actionDialogLumensGuide)
        self.aboutMenu.addSeparator()
        self.aboutMenu.addAction(self.actionDialogLumensAbout)
        
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
        ##self.layerListView.setFixedWidth(200)
        
        self.layerListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        ##self.layoutSidebar.setContentsMargins(0, 0, 0, 0)
        ##self.layoutSidebar.addWidget(self.layerListView)
        
        ##self.scrollSidebar = QtGui.QScrollArea()
        ##self.scrollSidebar.setFixedWidth(200)
        ##self.scrollSidebar.setWidget(self.contentSidebar)
        
        self.projectModel = QtGui.QFileSystemModel()
        self.projectModel.setRootPath(QtCore.QDir.rootPath())
        
        self.projectTreeView = QtGui.QTreeView()
        self.projectTreeView.setModel(self.projectModel)
        self.projectTreeView.setRootIndex(self.projectModel.index(QtCore.QDir.rootPath()))
        self.projectTreeView.hideColumn(1) # Hide all columns except name
        self.projectTreeView.hideColumn(2)
        self.projectTreeView.hideColumn(3)
        
        self.sidebarTabWidget = QtGui.QTabWidget()
        self.sidebarTabWidget.setTabPosition(QtGui.QTabWidget.West)
        
        self.dashboardTabWidget = QtGui.QTabWidget()
        
        self.tabLayers = QtGui.QWidget()
        self.tabDashboard = QtGui.QWidget()
        self.tabProject = QtGui.QWidget()
        
        self.layoutTabLayers = QtGui.QVBoxLayout()
        self.layoutTabDashboard = QtGui.QVBoxLayout()
        self.layoutTabProject = QtGui.QVBoxLayout()
        
        self.tabLayers.setLayout(self.layoutTabLayers)
        self.tabDashboard.setLayout(self.layoutTabDashboard)
        self.tabProject.setLayout(self.layoutTabProject)
        
        self.sidebarTabWidget.addTab(self.tabLayers, 'Layers')
        self.sidebarTabWidget.addTab(self.tabDashboard, 'Dashboard')
        self.sidebarTabWidget.addTab(self.tabProject, 'Project')
        
        #***********************************************************
        # Setup 'Dashboard' tab
        #***********************************************************
        self.tabDashboardPUR = QtGui.QWidget()
        self.tabDashboardQUES = QtGui.QWidget()
        self.tabDashboardTA = QtGui.QWidget()
        self.tabDashboardSCIENDO = QtGui.QWidget()
        
        self.layoutDashboardPUR = QtGui.QGridLayout()
        self.layoutDashboardQUES = QtGui.QVBoxLayout()
        self.layoutDashboardTA = QtGui.QVBoxLayout()
        self.layoutDashboardSCIENDO = QtGui.QVBoxLayout()
        
        self.layoutDashboardPUR.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutDashboardQUES.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutDashboardTA.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutDashboardSCIENDO.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        
        self.tabDashboardPUR.setLayout(self.layoutDashboardPUR)
        self.tabDashboardQUES.setLayout(self.layoutDashboardQUES)
        self.tabDashboardTA.setLayout(self.layoutDashboardTA)
        self.tabDashboardSCIENDO.setLayout(self.layoutDashboardSCIENDO)
        
        self.dashboardTabWidget.addTab(self.tabDashboardPUR, 'PUR')
        self.dashboardTabWidget.addTab(self.tabDashboardQUES, 'QUES')
        self.dashboardTabWidget.addTab(self.tabDashboardTA, 'TA')
        self.dashboardTabWidget.addTab(self.tabDashboardSCIENDO, 'SCIENDO')
        
        # QUES sub tabs
        self.QUESTabWidget = QtGui.QTabWidget()
        self.QUESTabWidget.setTabPosition(QtGui.QTabWidget.East)
        
        self.subtabPreQUES = QtGui.QWidget()
        self.subtabQUESC = QtGui.QWidget()
        self.subtabQUESB = QtGui.QWidget()
        self.subtabQUESH = QtGui.QWidget()
        
        self.layoutSubtabPreQUES = QtGui.QGridLayout()
        self.layoutSubtabQUESC = QtGui.QGridLayout()
        self.layoutSubtabQUESB = QtGui.QGridLayout()
        self.layoutSubtabQUESH = QtGui.QGridLayout()
        
        self.layoutSubtabPreQUES.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutSubtabQUESC.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutSubtabQUESB.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutSubtabQUESH.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        
        self.subtabPreQUES.setLayout(self.layoutSubtabPreQUES)
        self.subtabQUESC.setLayout(self.layoutSubtabQUESC)
        self.subtabQUESB.setLayout(self.layoutSubtabQUESB)
        self.subtabQUESH.setLayout(self.layoutSubtabQUESH)
        
        self.QUESTabWidget.addTab(self.subtabPreQUES, 'Pre-QUES')
        self.QUESTabWidget.addTab(self.subtabQUESC, 'QUES-C')
        self.QUESTabWidget.addTab(self.subtabQUESB, 'QUES-B')
        self.QUESTabWidget.addTab(self.subtabQUESH, 'QUES-H')
        
        self.layoutDashboardQUES.addWidget(self.QUESTabWidget)
        
        # TA sub tabs
        self.TATabWidget = QtGui.QTabWidget()
        self.TATabWidget.setTabPosition(QtGui.QTabWidget.East)
        
        self.subtabTAOpportunityCost = QtGui.QWidget()
        self.subtabTARegionalEconomy = QtGui.QWidget()
        
        self.layoutSubtabTAOpportunityCost = QtGui.QVBoxLayout()
        self.layoutSubtabTARegionalEconomy = QtGui.QVBoxLayout()
        
        self.layoutSubtabTAOpportunityCost.setAlignment(QtCore.Qt.AlignTop)
        self.layoutSubtabTARegionalEconomy.setAlignment(QtCore.Qt.AlignTop)
        
        self.subtabTAOpportunityCost.setLayout(self.layoutSubtabTAOpportunityCost)
        self.subtabTARegionalEconomy.setLayout(self.layoutSubtabTARegionalEconomy)
        
        self.TATabWidget.addTab(self.subtabTAOpportunityCost, 'Opportunity Cost')
        self.TATabWidget.addTab(self.subtabTARegionalEconomy, 'Regional Economy')
        
        self.layoutDashboardTA.addWidget(self.TATabWidget)
        
        # SCIENDO sub tabs
        self.SCIENDOTabWidget = QtGui.QTabWidget()
        self.SCIENDOTabWidget.setTabPosition(QtGui.QTabWidget.East)
        
        self.subtabSCIENDOLowEmissionDevelopmentAnalysis = QtGui.QWidget()
        self.subtabSCIENDOLandUseChangeModeling = QtGui.QWidget()
        
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis = QtGui.QVBoxLayout()
        self.layoutSubtabSCIENDOLandUseChangeModeling = QtGui.QVBoxLayout()
        
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.setAlignment(QtCore.Qt.AlignTop)
        self.layoutSubtabSCIENDOLandUseChangeModeling.setAlignment(QtCore.Qt.AlignTop)
        
        self.subtabSCIENDOLowEmissionDevelopmentAnalysis.setLayout(self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis)
        self.subtabSCIENDOLandUseChangeModeling.setLayout(self.layoutSubtabSCIENDOLandUseChangeModeling)
        
        self.SCIENDOTabWidget.addTab(self.subtabSCIENDOLowEmissionDevelopmentAnalysis, 'Low Emission Development Analysis')
        self.SCIENDOTabWidget.addTab(self.subtabSCIENDOLandUseChangeModeling, 'Land Use Change Modeling')
        
        self.layoutDashboardSCIENDO.addWidget(self.SCIENDOTabWidget)
        
        # PUR dashboard widgets
        self.groupBoxPURTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxPURTemplate = QtGui.QVBoxLayout()
        self.groupBoxPURTemplate.setLayout(self.layoutGroupBoxPURTemplate)
        
        self.layoutPURTemplate = QtGui.QHBoxLayout()
        
        # PUR template
        self.labelPURTemplate = QtGui.QLabel()
        self.labelPURTemplate.setText('Template name:')
        self.layoutPURTemplate.addWidget(self.labelPURTemplate)
        
        self.comboBoxPURTemplate = QtGui.QComboBox()
        self.comboBoxPURTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxPURTemplate.setDisabled(True)
        self.comboBoxPURTemplate.addItem('No template found')
        self.layoutPURTemplate.addWidget(self.comboBoxPURTemplate)
        
        self.layoutGroupBoxPURTemplate.addLayout(self.layoutPURTemplate)
        
        self.buttonProcessPURTemplate = QtGui.QPushButton()
        self.buttonProcessPURTemplate.setText('Process')
        self.buttonProcessPURTemplate.setDisabled(True)
        
        self.layoutDashboardPUR.addWidget(self.groupBoxPURTemplate)
        self.layoutDashboardPUR.addWidget(self.buttonProcessPURTemplate)
        
        #####################################################################
        
        # Pre-QUES sub tab dashboard widgets
        self.groupBoxPreQUESTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxPreQUESTemplate = QtGui.QVBoxLayout()
        self.groupBoxPreQUESTemplate.setLayout(self.layoutGroupBoxPreQUESTemplate)
        
        self.layoutPreQUESTemplate = QtGui.QHBoxLayout()
        
        # Pre-QUES template
        self.labelPreQUESTemplate = QtGui.QLabel()
        self.labelPreQUESTemplate.setText('Template name:')
        self.layoutPreQUESTemplate.addWidget(self.labelPreQUESTemplate)
        
        self.comboBoxPreQUESTemplate = QtGui.QComboBox()
        self.comboBoxPreQUESTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxPreQUESTemplate.setDisabled(True)
        self.comboBoxPreQUESTemplate.addItem('No template found')
        self.layoutPreQUESTemplate.addWidget(self.comboBoxPreQUESTemplate)
        
        self.layoutGroupBoxPreQUESTemplate.addLayout(self.layoutPreQUESTemplate)
        
        self.buttonProcessPreQUESTemplate = QtGui.QPushButton()
        self.buttonProcessPreQUESTemplate.setText('Process')
        self.buttonProcessPreQUESTemplate.setDisabled(True)
        
        self.layoutSubtabPreQUES.addWidget(self.groupBoxPreQUESTemplate)
        self.layoutSubtabPreQUES.addWidget(self.buttonProcessPreQUESTemplate)
        
        #####################################################################
        
        # QUES-C sub tab dashboard widgets
        self.groupBoxQUESCFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxQUESCFeatures = QtGui.QVBoxLayout()
        self.groupBoxQUESCFeatures.setLayout(self.layoutGroupBoxQUESCFeatures)
        
        self.labelQUESCFeaturesInfo = QtGui.QLabel()
        self.labelQUESCFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxQUESCFeatures.addWidget(self.labelQUESCFeaturesInfo)
        
        self.checkBoxQUESCCarbonAccounting = QtGui.QCheckBox('Carbon Accounting')
        self.checkBoxQUESCPeatlandCarbonAccounting = QtGui.QCheckBox('Peatland Carbon Accounting')
        self.checkBoxQUESCSummarizeMultiplePeriod = QtGui.QCheckBox('Summarize Multiple Period')
        
        self.layoutGroupBoxQUESCFeatures.addWidget(self.checkBoxQUESCCarbonAccounting)
        self.layoutGroupBoxQUESCFeatures.addWidget(self.checkBoxQUESCPeatlandCarbonAccounting)
        self.layoutGroupBoxQUESCFeatures.addWidget(self.checkBoxQUESCSummarizeMultiplePeriod)
        
        self.groupBoxQUESCTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxQUESCTemplate = QtGui.QVBoxLayout()
        self.groupBoxQUESCTemplate.setLayout(self.layoutGroupBoxQUESCTemplate)
        
        self.layoutQUESCTemplate = QtGui.QHBoxLayout()
        
        # QUES-C template
        self.labelQUESCTemplate = QtGui.QLabel()
        self.labelQUESCTemplate.setText('Template name:')
        self.layoutQUESCTemplate.addWidget(self.labelQUESCTemplate)
        
        self.comboBoxQUESCTemplate = QtGui.QComboBox()
        self.comboBoxQUESCTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxQUESCTemplate.setDisabled(True)
        self.comboBoxQUESCTemplate.addItem('No template found')
        self.layoutQUESCTemplate.addWidget(self.comboBoxQUESCTemplate)
        
        self.layoutGroupBoxQUESCTemplate.addLayout(self.layoutQUESCTemplate)
        
        self.buttonProcessQUESCTemplate = QtGui.QPushButton()
        self.buttonProcessQUESCTemplate.setText('Process')
        self.buttonProcessQUESCTemplate.setDisabled(True)
        
        self.layoutSubtabQUESC.addWidget(self.groupBoxQUESCFeatures)
        self.layoutSubtabQUESC.addWidget(self.groupBoxQUESCTemplate)
        self.layoutSubtabQUESC.addWidget(self.buttonProcessQUESCTemplate)
        
        #####################################################################
        
        # QUES-B sub tab dashboard widgets
        self.groupBoxQUESBTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxQUESBTemplate = QtGui.QVBoxLayout()
        self.groupBoxQUESBTemplate.setLayout(self.layoutGroupBoxQUESBTemplate)
        
        self.layoutQUESBTemplate = QtGui.QHBoxLayout()
        
        # QUES-B template
        self.labelQUESBTemplate = QtGui.QLabel()
        self.labelQUESBTemplate.setText('Template name:')
        self.layoutQUESBTemplate.addWidget(self.labelQUESBTemplate)
        
        self.comboBoxQUESBTemplate = QtGui.QComboBox()
        self.comboBoxQUESBTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxQUESBTemplate.setDisabled(True)
        self.comboBoxQUESBTemplate.addItem('No template found')
        self.layoutQUESBTemplate.addWidget(self.comboBoxQUESBTemplate)
        
        self.layoutGroupBoxQUESBTemplate.addLayout(self.layoutQUESBTemplate)
        
        self.buttonProcessQUESBTemplate = QtGui.QPushButton()
        self.buttonProcessQUESBTemplate.setText('Process')
        self.buttonProcessQUESBTemplate.setDisabled(True)
        
        self.layoutSubtabQUESB.addWidget(self.groupBoxQUESBTemplate)
        self.layoutSubtabQUESB.addWidget(self.buttonProcessQUESBTemplate)
        
        #####################################################################
        
        # QUES-H sub tab dashboard widgets
        self.groupBoxQUESHFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxQUESHFeatures = QtGui.QVBoxLayout()
        self.groupBoxQUESHFeatures.setLayout(self.layoutGroupBoxQUESHFeatures)
        
        self.labelQUESHFeaturesInfo = QtGui.QLabel()
        self.labelQUESHFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxQUESHFeatures.addWidget(self.labelQUESHFeaturesInfo)
        
        self.radioQUESHHRUDefinition = QtGui.QRadioButton('Hydrological Response Unit Definition')
        self.radioQUESHWatershedModelEvaluation = QtGui.QRadioButton('Watershed Model Evaluation')
        self.radioQUESHWatershedIndicators = QtGui.QRadioButton('Watershed Indicators')
        
        self.layoutGroupBoxQUESHFeatures.addWidget(self.radioQUESHHRUDefinition)
        self.layoutGroupBoxQUESHFeatures.addWidget(self.radioQUESHWatershedModelEvaluation)
        self.layoutGroupBoxQUESHFeatures.addWidget(self.radioQUESHWatershedIndicators)
        
        self.groupBoxHRUDefinitionFunction = QtGui.QGroupBox('Function')
        self.layoutGroupBoxHRUDefinitionFunction = QtGui.QVBoxLayout()
        self.groupBoxHRUDefinitionFunction.setLayout(self.layoutGroupBoxHRUDefinitionFunction)
        
        self.labelHRUDefinitionFunction = QtGui.QLabel()
        self.labelHRUDefinitionFunction.setText('Lorem ipsum dolot sit amet...')
        self.layoutGroupBoxHRUDefinitionFunction.addWidget(self.labelHRUDefinitionFunction)
        
        self.checkBoxHRUDefinitionDominantHRU = QtGui.QCheckBox('Dominant HRU')
        self.checkBoxHRUDefinitionDominantHRU.setChecked(False)
        self.checkBoxHRUDefinitionDominantLUSSL = QtGui.QCheckBox('Dominant Land Use, Soil, and Slope')
        self.checkBoxHRUDefinitionDominantLUSSL.setChecked(False)
        self.checkBoxHRUDefinitionMultipleHRU = QtGui.QCheckBox('Multiple HRU')
        self.checkBoxHRUDefinitionMultipleHRU.setChecked(False)
        
        self.layoutGroupBoxHRUDefinitionFunction.addWidget(self.checkBoxHRUDefinitionDominantHRU)
        self.layoutGroupBoxHRUDefinitionFunction.addWidget(self.checkBoxHRUDefinitionDominantLUSSL)
        self.layoutGroupBoxHRUDefinitionFunction.addWidget(self.checkBoxHRUDefinitionMultipleHRU)
        self.groupBoxHRUDefinitionFunction.setDisabled(True)
        
        self.groupBoxQUESHTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxQUESHTemplate = QtGui.QVBoxLayout()
        self.groupBoxQUESHTemplate.setLayout(self.layoutGroupBoxQUESHTemplate)
        
        self.layoutQUESHHRUDefinitionTemplate = QtGui.QHBoxLayout()
        self.layoutQUESHWatershedModelEvaluationTemplate = QtGui.QHBoxLayout()
        self.layoutQUESHWatershedIndicatorsTemplate = QtGui.QHBoxLayout()
        
        # 'HRU Definition' template
        self.labelHRUDefinitionTemplate = QtGui.QLabel()
        self.labelHRUDefinitionTemplate.setText('Template name:')
        self.layoutQUESHHRUDefinitionTemplate.addWidget(self.labelHRUDefinitionTemplate)
        
        self.comboBoxHRUDefinitionTemplate = QtGui.QComboBox()
        self.comboBoxHRUDefinitionTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxHRUDefinitionTemplate.setDisabled(True)
        self.comboBoxHRUDefinitionTemplate.addItem('No template found')
        self.layoutQUESHHRUDefinitionTemplate.addWidget(self.comboBoxHRUDefinitionTemplate)
        
        # 'Watershed Model Evaluation' template
        self.labelWatershedModelEvaluationTemplate = QtGui.QLabel()
        self.labelWatershedModelEvaluationTemplate.setText('Template name:')
        self.layoutQUESHWatershedModelEvaluationTemplate.addWidget(self.labelWatershedModelEvaluationTemplate)
        
        self.comboBoxWatershedModelEvaluationTemplate = QtGui.QComboBox()
        self.comboBoxWatershedModelEvaluationTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxWatershedModelEvaluationTemplate.setDisabled(True)
        self.comboBoxWatershedModelEvaluationTemplate.addItem('No template found')
        self.layoutQUESHWatershedModelEvaluationTemplate.addWidget(self.comboBoxWatershedModelEvaluationTemplate)
        
        # 'Watershed Indicators' template
        self.labelWatershedIndicatorsTemplate = QtGui.QLabel()
        self.labelWatershedIndicatorsTemplate.setText('Template name:')
        self.layoutQUESHWatershedIndicatorsTemplate.addWidget(self.labelWatershedIndicatorsTemplate)
        
        self.comboBoxWatershedIndicatorsTemplate = QtGui.QComboBox()
        self.comboBoxWatershedIndicatorsTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxWatershedIndicatorsTemplate.setDisabled(True)
        self.comboBoxWatershedIndicatorsTemplate.addItem('No template found')
        self.layoutQUESHWatershedIndicatorsTemplate.addWidget(self.comboBoxWatershedIndicatorsTemplate)
        
        self.layoutGroupBoxQUESHTemplate.addLayout(self.layoutQUESHHRUDefinitionTemplate)
        self.layoutGroupBoxQUESHTemplate.addLayout(self.layoutQUESHWatershedModelEvaluationTemplate)
        self.layoutGroupBoxQUESHTemplate.addLayout(self.layoutQUESHWatershedIndicatorsTemplate)
        
        # Hide the templates first until a feature is selected
        for i in range(self.layoutQUESHHRUDefinitionTemplate.count()):
            item = self.layoutQUESHHRUDefinitionTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutQUESHWatershedModelEvaluationTemplate.count()):
            item = self.layoutQUESHWatershedModelEvaluationTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutQUESHWatershedIndicatorsTemplate.count()):
            item = self.layoutQUESHWatershedIndicatorsTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        self.buttonProcessQUESHTemplate = QtGui.QPushButton()
        self.buttonProcessQUESHTemplate.setText('Process')
        self.buttonProcessQUESHTemplate.setDisabled(True)
        
        self.layoutSubtabQUESH.addWidget(self.groupBoxQUESHFeatures)
        self.layoutSubtabQUESH.addWidget(self.groupBoxHRUDefinitionFunction)
        self.layoutSubtabQUESH.addWidget(self.groupBoxQUESHTemplate)
        self.layoutSubtabQUESH.addWidget(self.buttonProcessQUESHTemplate)
        
        #####################################################################
        
        # TA 'Opportunity Cost' sub tab dashboard widgets
        self.groupBoxTAOpportunityCostFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxTAOpportunityCostFeatures = QtGui.QVBoxLayout()
        self.groupBoxTAOpportunityCostFeatures.setLayout(self.layoutGroupBoxTAOpportunityCostFeatures)
        
        self.labelTAOpportunityCostFeaturesInfo = QtGui.QLabel()
        self.labelTAOpportunityCostFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxTAOpportunityCostFeatures.addWidget(self.labelTAOpportunityCostFeaturesInfo)
        
        self.radioTAOpportunityCostAbacus = QtGui.QRadioButton('Abacus Opportunity Cost')
        self.radioTAOpportunityCostCurve = QtGui.QRadioButton('Opportunity Cost Curve')
        self.radioTAOpportunityCostMap = QtGui.QRadioButton('Opportunity Cost Map')
        
        self.layoutGroupBoxTAOpportunityCostFeatures.addWidget(self.radioTAOpportunityCostAbacus)
        self.layoutGroupBoxTAOpportunityCostFeatures.addWidget(self.radioTAOpportunityCostCurve)
        self.layoutGroupBoxTAOpportunityCostFeatures.addWidget(self.radioTAOpportunityCostMap)
        
        self.groupBoxTAOpportunityCostTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxTAOpportunityCostTemplate = QtGui.QVBoxLayout()
        self.groupBoxTAOpportunityCostTemplate.setLayout(self.layoutGroupBoxTAOpportunityCostTemplate)
        
        self.layoutTAAbacusOpportunityCostTemplate = QtGui.QHBoxLayout()
        self.layoutTAOpportunityCostCurveTemplate = QtGui.QHBoxLayout()
        self.layoutTAOpportunityCostMapTemplate = QtGui.QHBoxLayout()
        
        # TA 'Abacus Opportunity Cost' template
        self.labelAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.labelAbacusOpportunityCostTemplate.setText('Template name:')
        self.layoutTAAbacusOpportunityCostTemplate.addWidget(self.labelAbacusOpportunityCostTemplate)
        
        self.comboBoxAbacusOpportunityCostTemplate = QtGui.QComboBox()
        self.comboBoxAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
        self.comboBoxAbacusOpportunityCostTemplate.addItem('No template found')
        self.layoutTAAbacusOpportunityCostTemplate.addWidget(self.comboBoxAbacusOpportunityCostTemplate)
        
        # TA 'Opportunity Cost Curve' template
        self.labelOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelOpportunityCostCurveTemplate.setText('Template name:')
        self.layoutTAOpportunityCostCurveTemplate.addWidget(self.labelOpportunityCostCurveTemplate)
        
        self.comboBoxOpportunityCostCurveTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        self.comboBoxOpportunityCostCurveTemplate.addItem('No template found')
        self.layoutTAOpportunityCostCurveTemplate.addWidget(self.comboBoxOpportunityCostCurveTemplate)
        
        # TA 'Opportunity Cost Map' template
        self.labelOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelOpportunityCostMapTemplate.setText('Template name:')
        self.layoutTAOpportunityCostMapTemplate.addWidget(self.labelOpportunityCostMapTemplate)
        
        self.comboBoxOpportunityCostMapTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        self.comboBoxOpportunityCostMapTemplate.addItem('No template found')
        self.layoutTAOpportunityCostMapTemplate.addWidget(self.comboBoxOpportunityCostMapTemplate)
        
        self.layoutGroupBoxTAOpportunityCostTemplate.addLayout(self.layoutTAAbacusOpportunityCostTemplate)
        self.layoutGroupBoxTAOpportunityCostTemplate.addLayout(self.layoutTAOpportunityCostCurveTemplate)
        self.layoutGroupBoxTAOpportunityCostTemplate.addLayout(self.layoutTAOpportunityCostMapTemplate)
        
        # Hide the templates first until a feature is selected
        for i in range(self.layoutTAAbacusOpportunityCostTemplate.count()):
            item = self.layoutTAAbacusOpportunityCostTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTAOpportunityCostCurveTemplate.count()):
            item = self.layoutTAOpportunityCostCurveTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTAOpportunityCostMapTemplate.count()):
            item = self.layoutTAOpportunityCostMapTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        self.buttonProcessTAOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonProcessTAOpportunityCostTemplate.setText('Process')
        self.buttonProcessTAOpportunityCostTemplate.setDisabled(True)
        
        self.layoutSubtabTAOpportunityCost.addWidget(self.groupBoxTAOpportunityCostFeatures)
        self.layoutSubtabTAOpportunityCost.addWidget(self.groupBoxTAOpportunityCostTemplate)
        self.layoutSubtabTAOpportunityCost.addWidget(self.buttonProcessTAOpportunityCostTemplate)
        
        #####################################################################
        
        # TA 'Regional Economy' sub tab dashboard widgets
        self.groupBoxTARegionalEconomyFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxTARegionalEconomyFeatures = QtGui.QVBoxLayout()
        self.groupBoxTARegionalEconomyFeatures.setLayout(self.layoutGroupBoxTARegionalEconomyFeatures)
        
        self.labelTARegionalEconomyFeaturesInfo = QtGui.QLabel()
        self.labelTARegionalEconomyFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.labelTARegionalEconomyFeaturesInfo)
        
        self.radioTARegionalEconomyDescriptiveAnalysis = QtGui.QRadioButton('Descriptive Analysis of Regional Economy')
        self.radioTARegionalEconomyRegionalEconomicScenarioImpact = QtGui.QRadioButton('Regional Economic Scenario Impact')
        self.radioTARegionalEconomyLandRequirementAnalysis = QtGui.QRadioButton('Land Requirement Analysis')
        self.radioTARegionalEconomyLandUseChangeImpact = QtGui.QRadioButton('Land Use Change Impact')
        
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.radioTARegionalEconomyDescriptiveAnalysis)
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.radioTARegionalEconomyRegionalEconomicScenarioImpact)
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.radioTARegionalEconomyLandRequirementAnalysis)
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.radioTARegionalEconomyLandUseChangeImpact)
        
        self.groupBoxDescriptiveAnalysisPeriod = QtGui.QGroupBox('Period')
        self.layoutGroupBoxDescriptiveAnalysisPeriod = QtGui.QVBoxLayout()
        self.groupBoxDescriptiveAnalysisPeriod.setLayout(self.layoutGroupBoxDescriptiveAnalysisPeriod)
        
        self.labelDescriptiveAnalysisPeriod = QtGui.QLabel()
        self.labelDescriptiveAnalysisPeriod.setText('Lorem ipsum dolot sit amet...')
        self.layoutGroupBoxDescriptiveAnalysisPeriod.addWidget(self.labelDescriptiveAnalysisPeriod)
        
        self.checkBoxDescriptiveAnalysisMultiplePeriod = QtGui.QCheckBox('Multiple Period')
        self.checkBoxDescriptiveAnalysisMultiplePeriod.setChecked(False)
        
        self.layoutGroupBoxDescriptiveAnalysisPeriod.addWidget(self.checkBoxDescriptiveAnalysisMultiplePeriod)
        self.groupBoxDescriptiveAnalysisPeriod.setDisabled(True)
        
        self.groupBoxRegionalEconomicScenarioImpactType = QtGui.QGroupBox('Scenario type')
        self.layoutGroupBoxRegionalEconomicScenarioImpactType = QtGui.QVBoxLayout()
        self.groupBoxRegionalEconomicScenarioImpactType.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactType)
        
        self.labelRegionalEconomicScenarioImpactType = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactType.setText('Lorem ipsum dolot sit amet...')
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactType)
        
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand = QtGui.QCheckBox('Final Demand Scenario')
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand.setChecked(True)
        self.checkBoxRegionalEconomicScenarioImpactGDP = QtGui.QCheckBox('GDP Scenario')
        self.checkBoxRegionalEconomicScenarioImpactGDP.setChecked(False)
        
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactFinalDemand)
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactGDP)
        self.groupBoxRegionalEconomicScenarioImpactType.setDisabled(True)
        
        self.groupBoxTARegionalEconomyTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxTARegionalEconomyTemplate = QtGui.QVBoxLayout()
        self.groupBoxTARegionalEconomyTemplate.setLayout(self.layoutGroupBoxTARegionalEconomyTemplate)
        
        self.layoutTARegionalEconomyDescriptiveAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate = QtGui.QHBoxLayout()
        self.layoutTARegionalEconomyLandRequirementAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutTARegionalEconomyLandUseChangeImpactTemplate = QtGui.QHBoxLayout()
        
        # 'Descriptive Analysis' template
        self.labelDescriptiveAnalysisTemplate = QtGui.QLabel()
        self.labelDescriptiveAnalysisTemplate.setText('Template name:')
        self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.addWidget(self.labelDescriptiveAnalysisTemplate)
        
        self.comboBoxDescriptiveAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxDescriptiveAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
        self.comboBoxDescriptiveAnalysisTemplate.addItem('No template found')
        self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.addWidget(self.comboBoxDescriptiveAnalysisTemplate)
        
        # 'Regional Economic Scenario Impact' template
        self.labelRegionalEconomicScenarioImpactTemplate = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactTemplate.setText('Template name:')
        self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.addWidget(self.labelRegionalEconomicScenarioImpactTemplate)
        
        self.comboBoxRegionalEconomicScenarioImpactTemplate = QtGui.QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.addItem('No template found')
        self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.addWidget(self.comboBoxRegionalEconomicScenarioImpactTemplate)
        
        # 'Land Requirement Analysis' template
        self.labelLandRequirementAnalysisTemplate = QtGui.QLabel()
        self.labelLandRequirementAnalysisTemplate.setText('Template name:')
        self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.addWidget(self.labelLandRequirementAnalysisTemplate)
        
        self.comboBoxLandRequirementAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLandRequirementAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
        self.comboBoxLandRequirementAnalysisTemplate.addItem('No template found')
        self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.addWidget(self.comboBoxLandRequirementAnalysisTemplate)
        
        # 'Land Use Change Impact Analysis' template
        self.labelLandUseChangeImpactTemplate = QtGui.QLabel()
        self.labelLandUseChangeImpactTemplate.setText('Template name:')
        self.layoutTARegionalEconomyLandUseChangeImpactTemplate.addWidget(self.labelLandUseChangeImpactTemplate)
        
        self.comboBoxLandUseChangeImpactTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
        self.comboBoxLandUseChangeImpactTemplate.addItem('No template found')
        self.layoutTARegionalEconomyLandUseChangeImpactTemplate.addWidget(self.comboBoxLandUseChangeImpactTemplate)
        
        self.layoutGroupBoxTARegionalEconomyTemplate.addLayout(self.layoutTARegionalEconomyDescriptiveAnalysisTemplate)
        self.layoutGroupBoxTARegionalEconomyTemplate.addLayout(self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate)
        self.layoutGroupBoxTARegionalEconomyTemplate.addLayout(self.layoutTARegionalEconomyLandRequirementAnalysisTemplate)
        self.layoutGroupBoxTARegionalEconomyTemplate.addLayout(self.layoutTARegionalEconomyLandUseChangeImpactTemplate)
        
        # Hide the templates first until a feature is selected
        for i in range(self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.count()):
            item = self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.count()):
            item = self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.count()):
            item = self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyLandUseChangeImpactTemplate.count()):
            item = self.layoutTARegionalEconomyLandUseChangeImpactTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        self.buttonProcessTARegionalEconomyTemplate = QtGui.QPushButton()
        self.buttonProcessTARegionalEconomyTemplate.setText('Process')
        self.buttonProcessTARegionalEconomyTemplate.setDisabled(True)
        
        self.layoutSubtabTARegionalEconomy.addWidget(self.groupBoxTARegionalEconomyFeatures)
        self.layoutSubtabTARegionalEconomy.addWidget(self.groupBoxDescriptiveAnalysisPeriod)
        self.layoutSubtabTARegionalEconomy.addWidget(self.groupBoxRegionalEconomicScenarioImpactType)
        self.layoutSubtabTARegionalEconomy.addWidget(self.groupBoxTARegionalEconomyTemplate)
        self.layoutSubtabTARegionalEconomy.addWidget(self.buttonProcessTARegionalEconomyTemplate)
        
        #####################################################################
        
        # SCIENDO 'Low Emission Development Analysis' sub tab dashboard widgets
        self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures = QtGui.QVBoxLayout()
        self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.setLayout(self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures)
        
        self.labelSCIENDOLowEmissionDevelopmentAnalysisFeaturesInfo = QtGui.QLabel()
        self.labelSCIENDOLowEmissionDevelopmentAnalysisFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.labelSCIENDOLowEmissionDevelopmentAnalysisFeaturesInfo)
        
        self.checkBoxSCIENDOHistoricalBaselineProjection = QtGui.QCheckBox('Historical Baseline Projection')
        self.checkBoxSCIENDOHistoricalBaselineAnnualProjection = QtGui.QCheckBox('Historical Baseline Annual Projection')
        self.checkBoxSCIENDODriversAnalysis = QtGui.QCheckBox('Drivers Analysis')
        self.checkBoxSCIENDOBuildScenario = QtGui.QCheckBox('Build Scenario')
        
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.checkBoxSCIENDOHistoricalBaselineProjection)
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.checkBoxSCIENDOHistoricalBaselineAnnualProjection)
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.checkBoxSCIENDODriversAnalysis)
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.checkBoxSCIENDOBuildScenario)
        
        self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate = QtGui.QVBoxLayout()
        self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate.setLayout(self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        
        self.layoutSCIENDOLowEmissionDevelopmentAnalysisTemplate = QtGui.QHBoxLayout()
        
        # 'Low Emission Development Analysis' template
        self.labelLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLowEmissionDevelopmentAnalysisTemplate.setText('Template name:')
        self.layoutSCIENDOLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLowEmissionDevelopmentAnalysisTemplate)
        
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItem('No template found')
        self.layoutSCIENDOLowEmissionDevelopmentAnalysisTemplate.addWidget(self.comboBoxLowEmissionDevelopmentAnalysisTemplate)
        
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        
        self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setText('Process')
        self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures)
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.addWidget(self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        
        #####################################################################
        
        # SCIENDO 'Land Use Change Modeling' sub tab dashboard widgets
        self.groupBoxSCIENDOLandUseChangeModelingFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures = QtGui.QVBoxLayout()
        self.groupBoxSCIENDOLandUseChangeModelingFeatures.setLayout(self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures)
        
        self.labelSCIENDOLandUseChangeModelingFeaturesInfo = QtGui.QLabel()
        self.labelSCIENDOLandUseChangeModelingFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.labelSCIENDOLandUseChangeModelingFeaturesInfo)
        
        self.checkBoxSCIENDOCalculateTransitionMatrix = QtGui.QCheckBox('Calculate Transition Matrix')
        self.checkBoxSCIENDOCreateRasterCubeOfFactors = QtGui.QCheckBox('Create Raster Cube of Factors')
        self.checkBoxSCIENDOCalculateWeightOfEvidence = QtGui.QCheckBox('Calculate Weight of Evidence')
        self.checkBoxSCIENDOSimulateLandUseChange = QtGui.QCheckBox('Simulate Land Use Change')
        self.checkBoxSCIENDOSimulateWithScenario = QtGui.QCheckBox('Simulate With Scenario')
        
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOCalculateTransitionMatrix)
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOCreateRasterCubeOfFactors)
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOCalculateWeightOfEvidence)
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOSimulateLandUseChange)
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOSimulateWithScenario)
        
        self.groupBoxSCIENDOLandUseChangeModelingTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxSCIENDOLandUseChangeModelingTemplate = QtGui.QVBoxLayout()
        self.groupBoxSCIENDOLandUseChangeModelingTemplate.setLayout(self.layoutGroupBoxSCIENDOLandUseChangeModelingTemplate)
        
        self.layoutSCIENDOLandUseChangeModelingTemplate = QtGui.QHBoxLayout()
        
        # 'Land Use Change Modeling' template
        self.labelLandUseChangeModelingTemplate = QtGui.QLabel()
        self.labelLandUseChangeModelingTemplate.setText('Template name:')
        self.layoutSCIENDOLandUseChangeModelingTemplate.addWidget(self.labelLandUseChangeModelingTemplate)
        
        self.comboBoxLandUseChangeModelingTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
        self.comboBoxLandUseChangeModelingTemplate.addItem('No template found')
        self.layoutSCIENDOLandUseChangeModelingTemplate.addWidget(self.comboBoxLandUseChangeModelingTemplate)
        
        self.layoutGroupBoxSCIENDOLandUseChangeModelingTemplate.addLayout(self.layoutSCIENDOLandUseChangeModelingTemplate)
        
        self.buttonProcessSCIENDOLandUseChangeModelingTemplate = QtGui.QPushButton()
        self.buttonProcessSCIENDOLandUseChangeModelingTemplate.setText('Process')
        self.buttonProcessSCIENDOLandUseChangeModelingTemplate.setDisabled(True)
        
        self.layoutSubtabSCIENDOLandUseChangeModeling.addWidget(self.groupBoxSCIENDOLandUseChangeModelingFeatures)
        self.layoutSubtabSCIENDOLandUseChangeModeling.addWidget(self.groupBoxSCIENDOLandUseChangeModelingTemplate)
        self.layoutSubtabSCIENDOLandUseChangeModeling.addWidget(self.buttonProcessSCIENDOLandUseChangeModelingTemplate)
        
        #***********************************************************
        # End 'Dashboard' tab setup
        #***********************************************************
        
        self.layoutTabLayers.addWidget(self.layerListView)
        self.layoutTabDashboard.addWidget(self.dashboardTabWidget)
        self.layoutTabProject.addWidget(self.projectTreeView)
        
        self.splitterBody = QtGui.QSplitter(self)
        self.splitterBody.setOrientation(QtCore.Qt.Horizontal)
        
        self.splitterBody.setStretchFactor(0, 1)
        self.splitterBody.setStretchFactor(1, 5)
        
        self.splitterBody.addWidget(self.sidebarTabWidget)
        self.splitterBody.setCollapsible(0, False)
        
        self.layoutBody = QtGui.QHBoxLayout()
        self.layoutBody.setContentsMargins(0, 0, 0, 0)
        self.layoutBody.setAlignment(QtCore.Qt.AlignLeft)
        ##self.layoutBody.addWidget(self.scrollSidebar)
        ##self.layoutBody.addWidget(self.layerListView)
        ##self.layoutBody.addWidget(self.sidebarTabWidget)
        self.layoutBody.addWidget(self.splitterBody)
        
        self.layoutMain = QtGui.QVBoxLayout()
        self.layoutMain.setContentsMargins(11, 11, 11, 0) # Reduce gap with statusbar
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

        self.setMinimumSize(1024, 600)
        self.resize(self.sizeHint())
    
    
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
    
    
    def closeEvent(self, event):
        """Save app settings on window close
        """
        settings = QtCore.QSettings(self.appSettings['appSettingsFile'], QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        settings.setValue('recentProjects', self.recentProjects)
    
    
    def addRecentProject(self, projectFile):
        """Add a project file to the recent project list
        """
        if projectFile is None:
            return
        if projectFile not in self.recentProjects:
            self.recentProjects.insert(0, projectFile)
            while len(self.recentProjects) > 10:
                self.recentProjects.pop()
    
    
    def loadSettings(self):
        """Load app settings from .ini file
        """
        settings = QtCore.QSettings(self.appSettings['appSettingsFile'], QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        recentProjects = settings.value('recentProjects')
        if recentProjects:
            self.recentProjects = recentProjects
    
    
    def updateFileMenu(self):
        """Handle updating the file menu actions
        """
        recentProjects = []
        
        self.fileMenu.clear()
        
        # Populate file menu with recently opened project databases
        for projectFile in self.recentProjects:
            if os.path.exists(projectFile):
                recentProjects.append(projectFile)
        
        if recentProjects:
            self.fileMenu.addSeparator()
            
            for i, projectFile in enumerate(recentProjects):
                action = QtGui.QAction('&{0} {1}'.format(i + 1, os.path.basename(projectFile)), self)
                action.setData(projectFile)
                action.triggered.connect(self.lumensOpenDatabase)
                self.fileMenu.addAction(action)
            
            self.fileMenu.addSeparator()
        
        self.fileMenu.addAction(self.actionQuit)
    
    
    def openDialog(self, DialogClass, showDialog=True):
        """Keep track of already opened dialog instances instead of creating new ones
        """
        dialog = None
        
        for dlg in self.openDialogs:
            if isinstance(dlg, DialogClass):
                dialog = dlg
                break
        
        if not dialog:
            dialog = DialogClass(self)
            self.openDialogs.append(dialog)
        
        if showDialog:
            dialog.exec_()
        else:
            return dialog
    
    
    def closeDialogs(self):
        """Close all opened dialogs and mark for deletion by Qt
        """
        for dlg in self.openDialogs:
            dlg.deleteLater()
        
        self.openDialogs = []
    
    
    def lumensEnableMenus(self):
        """Enable menus that require an open project database
        """
        # Database menu
        self.actionLumensCloseDatabase.setEnabled(True)
        self.actionLumensDatabaseStatus.setEnabled(True)
        self.actionLumensDeleteData.setEnabled(True)
        self.actionDialogLumensAddData.setEnabled(True)
        
        self.actionDialogLumensAddLandcoverRaster.setEnabled(True)
        self.actionDialogLumensAddPeatData.setEnabled(True)
        self.actionDialogLumensAddFactorData.setEnabled(True)
        self.actionDialogLumensAddPlanningUnitData.setEnabled(True)
        
        # PUR menu
        self.actionDialogLumensPUR.setEnabled(True)
        
        self.actionDialogLumensPURCreateReferenceData.setEnabled(True)
        self.actionDialogLumensPURPreparePlanningUnit.setEnabled(True)
        self.actionDialogLumensPURReconcilePlanningUnit.setEnabled(True)
        self.actionDialogLumensPURFinalization.setEnabled(True)
        
        # QUES menu
        self.actionDialogLumensQUES.setEnabled(True)
        
        self.actionDialogLumensPreQUESLandcoverChangeAnalysis.setEnabled(True)
        self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setEnabled(True)
        self.actionDialogLumensQUESCCarbonAccounting.setEnabled(True)
        self.actionDialogLumensQUESCPeatlandCarbonAccounting.setEnabled(True)
        self.actionDialogLumensQUESCSummarizeMultiplePeriod.setEnabled(True)
        self.actionDialogLumensQUESBAnalysis.setEnabled(True)
        self.actionDialogLumensQUESHWatershedModelEvaluation.setEnabled(True)
        self.actionDialogLumensQUESHWatershedIndicators.setEnabled(True)
        self.actionDialogLumensQUESHDominantHRU.setEnabled(True)
        self.actionDialogLumensQUESHDominantLUSSL.setEnabled(True)
        self.actionDialogLumensQUESHMultipleHRU.setEnabled(True)
        
        # TA menu
        self.actionDialogLumensTAOpportunityCost.setEnabled(True)
        self.actionDialogLumensTARegionalEconomy.setEnabled(True)
        
        self.actionDialogLumensTAAbacusOpportunityCostCurve.setEnabled(True)
        self.actionDialogLumensTAOpportunityCostCurve.setEnabled(True)
        self.actionDialogLumensTAOpportunityCostMap.setEnabled(True)
        self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setEnabled(True)
        self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setEnabled(True)
        self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setEnabled(True)
        self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setEnabled(True)
        self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setEnabled(True)
        self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setEnabled(True)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDO.setEnabled(True)
        
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
        """Disable menus that require an open project database
        """
        # Database menu
        self.actionLumensDatabaseStatus.setDisabled(True)
        self.actionDialogLumensAddData.setDisabled(True)
        self.actionLumensDeleteData.setDisabled(True)
        
        self.actionDialogLumensAddLandcoverRaster.setDisabled(True)
        self.actionDialogLumensAddPeatData.setDisabled(True)
        self.actionDialogLumensAddFactorData.setDisabled(True)
        self.actionDialogLumensAddPlanningUnitData.setDisabled(True)
        
        # PUR menu
        self.actionDialogLumensPUR.setDisabled(True)
        
        self.actionDialogLumensPURCreateReferenceData.setDisabled(True)
        self.actionDialogLumensPURPreparePlanningUnit.setDisabled(True)
        self.actionDialogLumensPURReconcilePlanningUnit.setDisabled(True)
        self.actionDialogLumensPURFinalization.setDisabled(True)
        
        # QUES menu
        self.actionDialogLumensQUES.setDisabled(True)
        
        self.actionDialogLumensPreQUESLandcoverChangeAnalysis.setDisabled(True)
        self.actionDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setDisabled(True)
        self.actionDialogLumensQUESCCarbonAccounting.setDisabled(True)
        self.actionDialogLumensQUESCPeatlandCarbonAccounting.setDisabled(True)
        self.actionDialogLumensQUESCSummarizeMultiplePeriod.setDisabled(True)
        self.actionDialogLumensQUESBAnalysis.setDisabled(True)
        self.actionDialogLumensQUESHWatershedModelEvaluation.setDisabled(True)
        self.actionDialogLumensQUESHWatershedIndicators.setDisabled(True)
        self.actionDialogLumensQUESHDominantHRU.setDisabled(True)
        self.actionDialogLumensQUESHDominantLUSSL.setDisabled(True)
        self.actionDialogLumensQUESHMultipleHRU.setDisabled(True)
        
        # TA menu
        self.actionDialogLumensTAOpportunityCost.setDisabled(True)
        self.actionDialogLumensTARegionalEconomy.setDisabled(True)
        
        self.actionDialogLumensTAAbacusOpportunityCostCurve.setDisabled(True)
        self.actionDialogLumensTAOpportunityCostCurve.setDisabled(True)
        self.actionDialogLumensTAOpportunityCostMap.setDisabled(True)
        self.actionDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setDisabled(True)
        self.actionDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setDisabled(True)
        self.actionDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setDisabled(True)
        self.actionDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setDisabled(True)
        self.actionDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setDisabled(True)
        self.actionDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setDisabled(True)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDO.setDisabled(True)
        
        self.actionDialogLumensSCIENDODriversAnalysis.setDisabled(True)
        self.actionDialogLumensSCIENDOBuildScenario.setDisabled(True)
        self.actionDialogLumensSCIENDOHistoricalBaselineProjection.setDisabled(True)
        self.actionDialogLumensSCIENDOHistoricalBaselineAnnualProjection.setDisabled(True)
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix.setDisabled(True)
        self.actionDialogLumensSCIENDOCreateRasterCube.setDisabled(True)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence.setDisabled(True)
        self.actionDialogLumensSCIENDOSimulateLandUseChange.setDisabled(True)
        self.actionDialogLumensSCIENDOSimulateWithScenario.setDisabled(True)
    
    
    def loadModuleTemplates(self):
        """
        """
        dialogLumensPUR = self.openDialog(DialogLumensPUR, False)
        dialogLumensQUES = self.openDialog(DialogLumensQUES, False)
        dialogLumensTAOpportunityCost = self.openDialog(DialogLumensTAOpportunityCost, False)
        dialogLumensTARegionalEconomy = self.openDialog(DialogLumensTARegionalEconomy, False)
        dialogLumensSCIENDO = self.openDialog(DialogLumensSCIENDO, False)
        
        dialogLumensPUR.loadTemplateFiles()
        dialogLumensQUES.loadTemplateFiles()
        dialogLumensTAOpportunityCost.loadTemplateFiles()
        dialogLumensTARegionalEconomy.loadTemplateFiles()
        dialogLumensSCIENDO.loadTemplateFiles()
    
    
    def clearModuleTemplates(self):
        """
        """
        # PUR
        self.comboBoxPURTemplate.clear()
        self.comboBoxPURTemplate.addItem('No template found')
        self.comboBoxPURTemplate.setDisabled(True)
        
        # QUES
        self.comboBoxPreQUESTemplate.clear()
        self.comboBoxPreQUESTemplate.addItem('No template found')
        self.comboBoxPreQUESTemplate.setDisabled(True)
        
        self.comboBoxQUESCTemplate.clear()
        self.comboBoxQUESCTemplate.addItem('No template found')
        self.comboBoxQUESCTemplate.setDisabled(True)
        
        self.comboBoxQUESBTemplate.clear()
        self.comboBoxQUESBTemplate.addItem('No template found')
        self.comboBoxQUESBTemplate.setDisabled(True)
        
        self.comboBoxHRUDefinitionTemplate.clear()
        self.comboBoxHRUDefinitionTemplate.addItem('No template found')
        self.comboBoxHRUDefinitionTemplate.setDisabled(True)
        
        self.comboBoxWatershedModelEvaluationTemplate.clear()
        self.comboBoxWatershedModelEvaluationTemplate.addItem('No template found')
        self.comboBoxWatershedModelEvaluationTemplate.setDisabled(True)
        
        self.comboBoxWatershedIndicatorsTemplate.clear()
        self.comboBoxWatershedIndicatorsTemplate.addItem('No template found')
        self.comboBoxWatershedIndicatorsTemplate.setDisabled(True)
        
        # TA
        self.comboBoxAbacusOpportunityCostTemplate.clear()
        self.comboBoxAbacusOpportunityCostTemplate.addItem('No template found')
        self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
        
        self.comboBoxOpportunityCostCurveTemplate.clear()
        self.comboBoxOpportunityCostCurveTemplate.addItem('No template found')
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        
        self.comboBoxOpportunityCostMapTemplate.clear()
        self.comboBoxOpportunityCostMapTemplate.addItem('No template found')
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        
        self.comboBoxDescriptiveAnalysisTemplate.clear()
        self.comboBoxDescriptiveAnalysisTemplate.addItem('No template found')
        self.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
        
        self.comboBoxRegionalEconomicScenarioImpactTemplate.clear()
        self.comboBoxRegionalEconomicScenarioImpactTemplate.addItem('No template found')
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        
        self.comboBoxLandRequirementAnalysisTemplate.clear()
        self.comboBoxLandRequirementAnalysisTemplate.addItem('No template found')
        self.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
        
        self.comboBoxLandUseChangeImpactTemplate.clear()
        self.comboBoxLandUseChangeImpactTemplate.addItem('No template found')
        self.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
        
        # SCIENDO
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.clear()
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItem('No template found')
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        
        self.comboBoxLandUseChangeModelingTemplate.clear()
        self.comboBoxLandUseChangeModelingTemplate.addItem('No template found')
        self.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
        
    
    def lumensOpenDatabase(self, lumensDatabase=False):
        """Open a LUMENS project database
        """
        if lumensDatabase is False: # Recent projects
            action = self.sender()
            if isinstance(action, QtGui.QAction):
                lumensDatabase = unicode(action.data())
            else:
                return
        
        # Close the currently opened database first
        if self.appSettings['DialogLumensOpenDatabase']['projectFile']:
            self.lumensCloseDatabase()
        
        logging.getLogger(type(self).__name__).info('start: LUMENS Open Database')
        
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
            self.projectTreeView.setRootIndex(self.projectModel.index(self.appSettings['DialogLumensOpenDatabase']['projectFolder']))
            self.addRecentProject(lumensDatabase)
            
            self.lumensEnableMenus()
            self.loadModuleTemplates()
        
        self.actionLumensOpenDatabase.setEnabled(True)
        
        logging.getLogger(type(self).__name__).info('end: LUMENS Open Database')
    
    
    def lumensCloseDatabase(self):
        """Close a LUMENS project database
        """
        logging.getLogger(type(self).__name__).info('start: LUMENS Close Database')
        
        self.actionLumensCloseDatabase.setDisabled(True)
        
        outputs = general.runalg('modeler:lumens_close_database')
        
        self.appSettings['DialogLumensOpenDatabase']['projectFile'] = ''
        self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = ''
        
        self.lineEditActiveProject.clear()
        self.projectTreeView.setRootIndex(self.projectModel.index(QtCore.QDir.rootPath()))
        
        self.closeDialogs()
        self.lumensDisableMenus()
        self.clearModuleTemplates()
        
        logging.getLogger(type(self).__name__).info('end: LUMENS Close Database')
    
    
    def lumensDatabaseStatus(self):
        """Display the project database stats in a popup dialog
        """
        logging.getLogger(type(self).__name__).info('start: lumensdatabasestatus')
        
        self.actionLumensDatabaseStatus.setDisabled(True)
        outputs = general.runalg('r:lumensdatabasestatus', None)
        
        if outputs:
            dialog = DialogLumensViewer(self, 'Database Status', 'csv', outputs['database_status'])
            dialog.exec_()
        
        self.actionLumensDatabaseStatus.setEnabled(True)
        
        logging.getLogger(type(self).__name__).info('end: lumensdatabasestatus')
    
    
    def lumensDeleteData(self):
        """
        """
        logging.getLogger(type(self).__name__).info('start: lumensdeletedata')
        
        self.actionLumensDeleteData.setDisabled(True)
        outputs = general.runalg('r:lumensdeletedata')
        self.actionLumensDeleteData.setEnabled(True)
        
        logging.getLogger(type(self).__name__).info('end: lumensdeletedata')
    
    
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
    
    
    def loadDefaultLayers(self):
        """Replaces loadMap()
        """
        self.addLayer(self.appSettings['defaultBasemapFilePath'])
        ##self.addLayer(self.appSettings['defaultVectorFilePath'])
        self.mapCanvas.setExtent(self.appSettings['defaultExtent'])
        ###self.mapCanvas.refresh()
        ##self.layoutBody.addWidget(self.mapCanvas)
        self.splitterBody.addWidget(self.mapCanvas)
        self.splitterBody.setCollapsible(1, False)
    
    
    def loadMapCanvas(self):
        """
        """
        self.mapCanvas.setExtent(self.appSettings['defaultExtent'])
        ##self.layoutBody.addWidget(self.mapCanvas)
        self.splitterBody.addWidget(self.mapCanvas)
        self.splitterBody.setCollapsible(1, False)
    
    
    def loadMap(self):
        """OBSOLETE DEBUG on-the-fly projection
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(cur_dir, 'data', 'basemap', 'basemap.tif')
        self.basemap_layer = QgsRasterLayer(filename, 'basemap')
        QgsMapLayerRegistry.instance().addMapLayer(self.basemap_layer)
        
        filename = os.path.join(cur_dir, 'data', 'vector', 'Paser_rtrwp2014_utm50s.shp')
        self.landmark_layer = QgsVectorLayer(filename, 'landmarks', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(self.landmark_layer)

        self.mapCanvas.setExtent(self.appSettings['defaultExtent'])
        
        layers = []
        
        layers.append(QgsMapCanvasLayer(self.landmark_layer))
        layers.append(QgsMapCanvasLayer(self.basemap_layer))
        
        self.mapCanvas.setLayerSet(layers)
        
        ##self.layoutBody.addWidget(self.mapCanvas)
        self.splitterBody.addWidget(self.mapCanvas)
        self.splitterBody.setCollapsible(1, False)
    
    
    def addLayer(self, layerFile):
        """Add a spatial data file to the layer list and display it
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
    
    
    def getSelectedLayerData(self):
        """Get the data of the selected layer
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        return layerItemData
    
    
    def printDebugInfo(self):
        """
        """
        layerItemData = self.getSelectedLayerData()
        
        logging.getLogger(type(self).__name__).info('DEBUG INFO ===================================')
        logging.getLogger(type(self).__name__).info('MapCanvas layer count: ' + str(self.mapCanvas.layerCount()))
        logging.getLogger(type(self).__name__).info('MapCanvas destination CRS: ' + self.mapCanvas.mapRenderer().destinationCrs().authid())
        logging.getLogger(type(self).__name__).info('On-the-fly projection enabled: ' + str(self.mapCanvas.hasCrsTransformEnabled()))
        logging.getLogger(type(self).__name__).info('Selected layer CRS: ' + self.qgsLayerList[layerItemData['layer']].crs().authid())
    
    
    def showVisibleLayers(self):
        """Find checked layers in layerlistmodel and add them to the mapcanvas layerset
        """
        layers = []
        i = 0
        
        while self.layerListModel.item(i):
            layerItem = self.layerListModel.item(i)
            layerItemData = layerItem.data()
            if layerItem.checkState():
                logging.getLogger(type(self).__name__).info('showing layer: %s', layerItem.text())
                layers.append(QgsMapCanvasLayer(self.qgsLayerList[layerItemData['layer']]))
            i += 1
        
        if i > 0:
            logging.getLogger(type(self).__name__).info('===========================================')
        
        self.mapCanvas.setLayerSet(layers)
    
    
    def handlerLayerItemContextMenu(self, pos):
        """Construct the layer item context menu
        """
        self.contextMenu = QtGui.QMenu()
        self.contextMenu.addAction(self.actionDeleteLayer)
        self.contextMenu.addAction(self.actionZoomLayer)
        self.contextMenu.addAction(self.actionLayerAttributeTable)
        self.contextMenu.addAction(self.actionFeatureSelectExpression)
        
        parentPosition = self.layerListView.mapToGlobal(QtCore.QPoint(0, 0))
        self.contextMenu.move(parentPosition + pos)
        self.contextMenu.show()
    
    
    def handlerProcessPURTemplate(self):
        """
        """
        templateFile = self.comboBoxPURTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessPURTemplate.setDisabled(True)
            
            dialogLumensPUR = self.openDialog(DialogLumensPUR, False)
            dialogLumensPUR.loadTemplate('Setup', templateFile)
            dialogLumensPUR.handlerProcessSetup()
            
            self.buttonProcessPURTemplate.setEnabled(True)
    
    
    def handlerProcessPreQUESTemplate(self):
        """
        """
        templateFile = self.comboBoxPreQUESTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessPreQUESTemplate.setDisabled(True)
            
            dialogLumensQUES = self.openDialog(DialogLumensQUES, False)
            dialogLumensQUES.loadTemplate('Pre-QUES', templateFile)
            dialogLumensQUES.handlerProcessPreQUES()
            
            self.buttonProcessPreQUESTemplate.setEnabled(True)
    
    
    def handlerProcessQUESCTemplate(self):
        """
        """
        templateFile = self.comboBoxQUESCTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessQUESCTemplate.setDisabled(True)
            
            dialogLumensQUES = self.openDialog(DialogLumensQUES, False)
            dialogLumensQUES.loadTemplate('QUES-C', templateFile)
            
            # Update the checkbox status in the dialog too
            if self.checkBoxQUESCCarbonAccounting.isChecked():
                dialogLumensQUES.checkBoxCarbonAccounting.setChecked(True)
            
            if self.checkBoxQUESCPeatlandCarbonAccounting.isChecked():
                dialogLumensQUES.checkBoxPeatlandCarbonAccounting.setChecked(True)
            
            if self.checkBoxQUESCSummarizeMultiplePeriod.isChecked():
                dialogLumensQUES.checkBoxSummarizeMultiplePeriod.setChecked(True)
            
            dialogLumensQUES.handlerProcessQUESC()
            
            self.buttonProcessPreQUESTemplate.setEnabled(True)
    
    
    def handlerProcessQUESBTemplate(self):
        """
        """
        templateFile = self.comboBoxQUESBTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessQUESBTemplate.setDisabled(True)
            
            dialogLumensQUES = self.openDialog(DialogLumensQUES, False)
            dialogLumensQUES.loadTemplate('QUES-B', templateFile)
            dialogLumensQUES.handlerProcessQUESB()
            
            self.buttonProcessQUESBTemplate.setEnabled(True)
    
    
    def handlerProcessQUESHTemplate(self):
        """
        """
        templateFile = None
        tabName = None
        QUESHHRUDefinition = QUESHWatershedModelEvaluation = QUESHWatershedIndicators = False
        
        if radioQUESHHRUDefinition.isChecked():
            QUESHHRUDefinition = True
            tabName = 'Hydrological Response Unit Definition'
            templateFile = self.comboBoxHRUDefinitionTemplate.currentText()
        elif radioQUESHWatershedModelEvaluation.isChecked():
            QUESHWatershedModelEvaluation = True
            tabName = 'Watershed Model Evaluation'
            templateFile = self.comboBoxWatershedModelEvaluationTemplate.currentText()
        elif radioQUESHWatershedIndicators.isChecked():
            QUESHWatershedIndicators = True
            tabName = 'Watershed Indicators'
            templateFile = self.comboBoxWatershedIndicatorsTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessQUESHTemplate.setDisabled(True)
            
            dialogLumensQUES = self.openDialog(DialogLumensQUES, False)
            dialogLumensQUES.loadTemplate(tabName, templateFile)
            
            if QUESHHRUDefinition:
                # Update the checkbox status in the dialog too
                if self.checkBoxHRUDefinitionDominantHRU.isChecked():
                    dialogLumensQUES.checkBoxDominantHRU.setChecked(True)
                
                if self.checkBoxHRUDefinitionDominantLUSSL.isChecked():
                    dialogLumensQUES.checkBoxDominantLUSSL.setChecked(True)
                
                if self.checkBoxHRUDefinitionMultipleHRU.isChecked():
                    dialogLumensQUES.checkBoxMultipleHRU.setChecked(True)
            
                dialogLumensQUES.handlerProcessQUESHHRUDefinition()
            elif QUESHWatershedModelEvaluation:
                dialogLumensQUES.handlerProcessQUESHWatershedModelEvaluation()
            elif QUESHWatershedIndicators:
                dialogLumensQUES.handlerProcessQUESHWatershedIndicators()
            
            self.buttonProcessQUESHTemplate.setEnabled(True)
    
    
    def handlerProcessTAOpportunityCostTemplate(self):
        """
        """
        templateFile = None
        tabName = None
        TAAbacusOpportunityCost = TAOpportunityCostCurve = TAOpportunityCostMap = False
        
        if radioTAOpportunityCostAbacus.isChecked():
            TAAbacusOpportunityCost = True
            tabName = 'Abacus Opportunity Cost'
            templateFile = self.comboBoxAbacusOpportunityCostTemplate.currentText()
        elif radioTAOpportunityCostCurve.isChecked():
            TAOpportunityCostCurve = True
            tabName = 'Opportunity Cost Curve'
            templateFile = self.comboBoxOpportunityCostCurveTemplate.currentText()
        elif radioTAOpportunityCostMap.isChecked():
            TAOpportunityCostMap = True
            tabName = 'Opportunity Cost Map'
            templateFile = self.comboBoxOpportunityCostMapTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessTAOpportunityCostTemplate.setDisabled(True)
            
            dialogLumensTA = self.openDialog(DialogLumensTAOpportunityCost, False)
            dialogLumensTA.loadTemplate(tabName, templateFile)
            
            if TAAbacusOpportunityCost:
                dialogLumensTA.handlerProcessAbacusOpportunityCost()
            elif QUESHWatershedModelEvaluation:
                dialogLumensTA.handlerProcessOpportunityCostCurve()
            elif QUESHWatershedIndicators:
                dialogLumensTA.handlerProcessOpportunityCostMap()
            
            self.buttonProcessTAOpportunityCostTemplate.setEnabled(True)
        
    
    def handlerProcessTARegionalEconomyTemplate(self):
        """
        """
        templateFile = None
        tabName = None
        TADescriptiveAnalysis = TARegionalEconomicScenarioImpact = TALandRequirementAnalysis = TALandUseChangeImpact = False
        
        if radioTARegionalEconomyDescriptiveAnalysis.isChecked():
            TADescriptiveAnalysis = True
            tabName = 'Descriptive Analysis of Regional Economy'
            templateFile = self.comboBoxDescriptiveAnalysisTemplate.currentText()
        elif radioTARegionalEconomyRegionalEconomicScenarioImpact.isChecked():
            TARegionalEconomicScenarioImpact = True
            tabName = 'Regional Economic Scenario Impact'
            templateFile = self.comboBoxRegionalEconomicScenarioImpactTemplate.currentText()
        elif radioTARegionalEconomyLandRequirementAnalysis.isChecked():
            TALandRequirementAnalysis = True
            tabName = 'Land Requirement Analysis'
            templateFile = self.comboBoxLandRequirementAnalysisTemplate.currentText()
        elif radioTARegionalEconomyLandUseChangeImpact.isChecked():
            TALandUseChangeImpact = True
            tabName = 'Land Use Change Impact'
            templateFile = self.comboBoxLandUseChangeImpactTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessTARegionalEconomyTemplate.setDisabled(True)
            
            dialogLumensTA = self.openDialog(DialogLumensTARegionalEconomy, False)
            dialogLumensTA.loadTemplate(tabName, templateFile)
            
            if TADescriptiveAnalysis:
                # Update the checkbox status in the dialog too
                if self.checkBoxDescriptiveAnalysisMultiplePeriod.isChecked():
                    dialogLumensTA.checkBoxMultiplePeriod.setChecked(True)
                
                dialogLumensTA.handlerProcessDescriptiveAnalysis()
            elif TARegionalEconomicScenarioImpact:
                # Update the checkbox status in the dialog too
                if self.checkBoxRegionalEconomicScenarioImpactFinalDemand.isChecked():
                    dialogLumensTA.checkBoxRegionalEconomicScenarioImpactFinalDemand.setChecked(True)
                
                if self.checkBoxRegionalEconomicScenarioImpactGDP.isChecked():
                    dialogLumensTA.checkBoxRegionalEconomicScenarioImpactGDP.setChecked(True)
            
                dialogLumensTA.handlerProcessRegionalEconomicScenarioImpact()
            elif TALandRequirementAnalysis:
                dialogLumensTA.handlerProcessLandRequirementAnalysis()
            elif TALandUseChangeImpact:
                dialogLumensTA.handlerProcessLandUseChangeImpact()
            
            self.buttonProcessTARegionalEconomyTemplate.setEnabled(True)
    
    
    def handlerProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate(self):
        """
        """
        templateFile = self.comboBoxLowEmissionDevelopmentAnalysisTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            
            dialogLumensSCIENDO = self.openDialog(DialogLumensSCIENDO, False)
            DialogLumensSCIENDO.loadTemplate('Low Emission Development Analysis', templateFile)
            
            # Update the checkbox status in the dialog too
            if self.checkBoxSCIENDOHistoricalBaselineProjection.isChecked():
                dialogLumensSCIENDO.checkBoxHistoricalBaselineProjection.setChecked(True)
            
            if self.checkBoxSCIENDOHistoricalBaselineAnnualProjection.isChecked():
                dialogLumensSCIENDO.checkBoxHistoricalBaselineAnnualProjection.setChecked(True)
            
            if self.checkBoxSCIENDODriversAnalysis.isChecked():
                dialogLumensSCIENDO.checkBoxDriversAnalysis.setChecked(True)
            
            if self.checkBoxSCIENDOBuildScenario.isChecked():
                dialogLumensSCIENDO.checkBoxBuildScenario.setChecked(True)
            
            dialogLumensSCIENDO.handlerProcessLowEmissionDevelopmentAnalysis()
            
            self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
    
    
    def handlerProcessSCIENDOLandUseChangeModelingTemplate(self):
        """
        """
        templateFile = self.comboBoxLandUseChangeModelingTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessSCIENDOLandUseChangeModelingTemplate.setDisabled(True)
            
            dialogLumensSCIENDO = self.openDialog(DialogLumensSCIENDO, False)
            DialogLumensSCIENDO.loadTemplate('Land Use Change Modeling', templateFile)
            
            # Update the checkbox status in the dialog too
            if self.checkBoxSCIENDOCalculateTransitionMatrix.isChecked():
                dialogLumensSCIENDO.checkBoxCalculateTransitionMatrix.setChecked(True)
            
            if self.checkBoxSCIENDOCreateRasterCubeOfFactors.isChecked():
                dialogLumensSCIENDO.checkBoxCreateRasterCubeOfFactors.setChecked(True)
            
            if self.checkBoxSCIENDOCalculateWeightOfEvidence.isChecked():
                dialogLumensSCIENDO.checkBoxCalculateWeightOfEvidence.setChecked(True)
            
            if self.checkBoxSCIENDOSimulateLandUseChange.isChecked():
                dialogLumensSCIENDO.checkBoxSimulateLandUseChange.setChecked(True)
            
            if self.checkBoxSCIENDOSimulateWithScenario.isChecked():
                dialogLumensSCIENDO.checkBoxSimulateWithScenario.setChecked(True)
            
            dialogLumensSCIENDO.handlerProcessLandUseChangeModeling()
            
            self.buttonProcessSCIENDOLandUseChangeModelingTemplate.setEnabled(True)
    
    
    def handlerToggleQUESH(self, radio):
        """
        """
        for i in range(self.layoutQUESHHRUDefinitionTemplate.count()):
            item = self.layoutQUESHHRUDefinitionTemplate.itemAt(i)
            item.widget().setVisible(False)
    
        for i in range(self.layoutQUESHWatershedModelEvaluationTemplate.count()):
            item = self.layoutQUESHWatershedModelEvaluationTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutQUESHWatershedIndicatorsTemplate.count()):
            item = self.layoutQUESHWatershedIndicatorsTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        self.groupBoxHRUDefinitionFunction.setDisabled(True)
        
        if radio.text() == 'Hydrological Response Unit Definition':
            if radio.isChecked():
                self.groupBoxHRUDefinitionFunction.setDisabled(False)
                
                for i in range(self.layoutQUESHHRUDefinitionTemplate.count()):
                    item = self.layoutQUESHHRUDefinitionTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Watershed Model Evaluation':
            if radio.isChecked():
                for i in range(self.layoutQUESHWatershedModelEvaluationTemplate.count()):
                    item = self.layoutQUESHWatershedModelEvaluationTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Watershed Indicators':
            if radio.isChecked():
                for i in range(self.layoutQUESHWatershedIndicatorsTemplate.count()):
                    item = self.layoutQUESHWatershedIndicatorsTemplate.itemAt(i)
                    item.widget().setVisible(True)
        
    
    def handlerToggleTAOpportunityCost(self, radio):
        """
        """
        for i in range(self.layoutTAAbacusOpportunityCostTemplate.count()):
            item = self.layoutTAAbacusOpportunityCostTemplate.itemAt(i)
            item.widget().setVisible(False)
    
        for i in range(self.layoutTAOpportunityCostCurveTemplate.count()):
            item = self.layoutTAOpportunityCostCurveTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTAOpportunityCostMapTemplate.count()):
            item = self.layoutTAOpportunityCostMapTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        if radio.text() == 'Abacus Opportunity Cost':
            if radio.isChecked():
                for i in range(self.layoutTAAbacusOpportunityCostTemplate.count()):
                    item = self.layoutTAAbacusOpportunityCostTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Opportunity Cost Curve':
            if radio.isChecked():
                for i in range(self.layoutTAOpportunityCostCurveTemplate.count()):
                    item = self.layoutTAOpportunityCostCurveTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Opportunity Cost Map':
            if radio.isChecked():
                for i in range(self.layoutTAOpportunityCostMapTemplate.count()):
                    item = self.layoutTAOpportunityCostMapTemplate.itemAt(i)
                    item.widget().setVisible(True)
    
    
    def handlerToggleTARegionalEconomy(self, radio):
        """
        """
        for i in range(self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.count()):
            item = self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.itemAt(i)
            item.widget().setVisible(False)
    
        for i in range(self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.count()):
            item = self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.count()):
            item = self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyLandUseChangeImpactTemplate.count()):
            item = self.layoutTARegionalEconomyLandUseChangeImpactTemplate.itemAt(i)
            item.widget().setVisible(False)
            
        self.groupBoxDescriptiveAnalysisPeriod.setDisabled(True)
        self.groupBoxRegionalEconomicScenarioImpactType.setDisabled(True)
        
        if radio.text() == 'Descriptive Analysis of Regional Economy':
            if radio.isChecked():
                self.groupBoxDescriptiveAnalysisPeriod.setDisabled(False)
                
                for i in range(self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.count()):
                    item = self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Regional Economic Scenario Impact':
            if radio.isChecked():
                self.groupBoxRegionalEconomicScenarioImpactType.setDisabled(False)
                
                for i in range(self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.count()):
                    item = self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Land Requirement Analysis':
            if radio.isChecked():
                for i in range(self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.count()):
                    item = self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Land Use Change Impact':
            if radio.isChecked():
                for i in range(self.layoutTARegionalEconomyLandUseChangeImpactTemplate.count()):
                    item = self.layoutTARegionalEconomyLandUseChangeImpactTemplate.itemAt(i)
                    item.widget().setVisible(True)
    
    
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
            logging.getLogger(type(self).__name__).info('select LUMENS database: %s', lumensDatabase)
            
            self.lumensOpenDatabase(lumensDatabase)
    
    
    def handlerLumensDeleteData(self):
        """
        """
        self.lumensDeleteData()
    
    
    def handlerLumensCloseDatabase(self):
        """
        """
        self.lumensCloseDatabase()
    
    
    def handlerLumensDatabaseStatus(self):
        """
        """
        self.lumensDatabaseStatus()
    
    
    def handlerDialogLumensAddData(self):
        """
        """
        self.openDialog(DialogLumensAddData)
    
    
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
    
    
    def handlerDialogLumensPUR(self):
        """
        """
        self.openDialog(DialogLumensPUR)
    
    
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
    
    
    def handlerDialogLumensQUES(self):
        """
        """
        self.openDialog(DialogLumensQUES)
    
    
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
    
    
    def handlerDialogLumensQUESHWatershedModelEvaluation(self):
        """
        """
        self.openDialog(DialogLumensQUESHWatershedModelEvaluation)
    
    
    def handlerDialogLumensQUESHWatershedIndicators(self):
        """
        """
        self.openDialog(DialogLumensQUESHWatershedIndicators)
    
    
    def handlerDialogLumensQUESHDominantHRU(self):
        """
        """
        self.openDialog(DialogLumensQUESHDominantHRU)
    
    
    def handlerDialogLumensQUESHDominantLUSSL(self):
        """
        """
        self.openDialog(DialogLumensQUESHDominantLUSSL)
    
    
    def handlerDialogLumensQUESHMultipleHRU(self):
        """
        """
        self.openDialog(DialogLumensQUESHMultipleHRU)
    
    
    def handlerDialogLumensTAOpportunityCost(self):
        """
        """
        self.openDialog(DialogLumensTAOpportunityCost)
    
    
    def handlerDialogLumensTARegionalEconomy(self):
        """
        """
        self.openDialog(DialogLumensTARegionalEconomy)
    
    
    def handlerDialogLumensTAAbacusOpportunityCostCurve(self):
        """
        """
        self.openDialog(DialogLumensTAAbacusOpportunityCostCurve)
    
    
    def handlerDialogLumensTAOpportunityCostCurve(self):
        """
        """
        self.openDialog(DialogLumensTAOpportunityCostCurve)
    
    
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
    
    
    def handlerDialogLumensSCIENDO(self):
        """
        """
        self.openDialog(DialogLumensSCIENDO)
    
    
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
    
    
    def handlerDialogLumensGuide(self):
        """
        """
        filePath = os.path.join(self.appSettings['appDir'], self.appSettings['guideFile'])
        
        if os.path.exists(filePath):
            if sys.platform == 'win32':
                os.startfile(filePath) # Open the document file in Windows
        else:
            QtGui.QMessageBox.critical(self, 'LUMENS Guide Not Found', "Unable to open '{0}'.".format(filePath))
    
    
    def handlerDialogLumensAbout(self):
        """
        """
        QtGui.QMessageBox.about(self, 'LUMENS',
            """<b>LUMENS</b> v {0}
            <p>Copyright &copy; 2015-2016 ICRAF. 
            All rights reserved.
            <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
            __version__, platform.python_version(),
            QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR,
            platform.system()))
    
    
    def handlerDialogLumensToolsREDDAbacusSP(self):
        """
        """
        self.openDialog(DialogLumensToolsREDDAbacusSP)
    
    
    def handlerToggleSidebar(self):
        """
        """
        if not self.actionToggleSidebar.isChecked():
            self.sidebarTabWidget.setVisible(False)
        else:
            self.sidebarTabWidget.setVisible(True)
    
    
    def handlerToggleToolbar(self):
        """
        """
        if not self.actionToggleToolbar.isChecked():
            self.toolBar.setVisible(False)
        else:
            self.toolBar.setVisible(True)
    
    
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
        layerItemData = self.getSelectedLayerData()
        ##self.mapCanvas.setExtent(self.qgsLayerList[layerItemData['layer']].extent())
        ##self.mapCanvas.refresh()
        # Hack to fix blank map canvas from 2 lines above
        self.qgsLayerList[layerItemData['layer']].selectAll()
        self.mapCanvas.zoomToSelected()
        self.qgsLayerList[layerItemData['layer']].removeSelection()
    
    
    def handlerZoomSelected(self):
        """
        """
        layerItemData = self.getSelectedLayerData()
        if layerItemData['layerType'] == 'vector':
            self.mapCanvas.setCurrentLayer(self.qgsLayerList[layerItemData['layer']])
            self.mapCanvas.zoomToSelected()
    
    
    def handlerPanSelected(self):
        """
        """
        layerItemData = self.getSelectedLayerData()
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
        layerItemData = self.getSelectedLayerData()
        ##dialog = DialogLayerAttributeTable(self.qgsLayerList[layerItemData['layer']], self)
        dialog = DialogLayerAttributeDualView(self.qgsLayerList[layerItemData['layer']], self)
        dialog.exec_()
    
    
    def handlerFeatureSelectExpression(self):
        """
        """
        layerItemData = self.getSelectedLayerData()
        # Try using QGIS's select feature dialog
        ##dialog = DialogFeatureSelectExpression(self.qgsLayerList[layerItemData['layer']], self)
        dialog = QgsExpressionSelectionDialog(self.qgsLayerList[layerItemData['layer']], '', self)
        dialog.exec_()
    
    
    def handlerDoubleClickProjectTree(self, index):
        """
        """
        indexItem = self.projectTreeView.model().index(index.row(), 0, index.parent())

        # Path or filename selected
        fileName = self.projectTreeView.model().fileName(indexItem)
        # Full path/filename selected
        filePath = self.projectTreeView.model().filePath(indexItem)
        
        ext = os.path.splitext(filePath)[-1].lower()
        
        if ext in self.appSettings['acceptedDocumentFormats']:
            if sys.platform == 'win32':
                os.startfile(filePath) # Open the document file in Windows
        elif ext in self.appSettings['acceptedSpatialFormats']:
            self.addLayer(filePath) # Add the spatial data file to the layer list
        elif ext in self.appSettings['acceptedWebFormats']: # Open web documents in internal viewer
            dialog = DialogLumensViewer(self, os.path.basename(filePath), 'html', filePath)
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
    
    
    def handlerDeleteLayer(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItemData = self.getSelectedLayerData()
        del self.qgsLayerList[layerItemData['layer']]
        ##QtGui.QMessageBox.information(self, 'Layer', layerItemData)
        self.layerListModel.removeRow(layerItemIndex.row())
        
        self.showVisibleLayers()
        
        if not self.layerListModel.rowCount():
            self.actionDeleteLayer.setDisabled(True)
            self.actionZoomLayer.setDisabled(True)
            return
        
        # Check type of next selected item
        layerItemData = self.getSelectedLayerData()
        
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
    
    
    def handlerUpdateCoordinates(self, point):
        """
        """
        if self.mapCanvas.mapUnits() == QGis.DegreesMinutesSeconds:
            self.labelMapCanvasCoordinate.setText(point.toDegreesMinutesSeconds(3))
        else:
            print self.labelMapCanvasCoordinate.setText(point.toString(3))


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
    splashScreen.finish(window)
    window.raise_()
    
    if window.checkDefaultBasemap():
        window.loadDefaultLayers()
        ##window.loadMap() # DEBUG on-the-fly projection
    else:
        window.loadMapCanvas()
    
    # Pan mode by default
    window.handlerSetPanMode()
    
    app.setWindowIcon(QtGui.QIcon('ui/icons/app.ico'))
    app.exec_()
    app.deleteLater()
    
    QgsApplication.exitQgis()


#############################################################################


if __name__ == "__main__":
    main()

