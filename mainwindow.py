#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, logging, subprocess

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

from utils import QPlainTextEditLogger
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
from dialog_lumens_sciendo_calctransitionmatrix import DialogLumensSCIENDOCalculateTransitionMatrix
from dialog_lumens_sciendo_createrastercube import DialogLumensSCIENDOCreateRasterCube
from dialog_lumens_sciendo_calcweightevidence import DialogLumensSCIENDOCalculateWeightofEvidence
from dialog_lumens_sciendo_simulatelandusechange import DialogLumensSCIENDOSimulateLandUseChange
from dialog_lumens_sciendo_simulatewithscenario import DialogLumensSCIENDOSimulateWithScenario


#############################################################################


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
        """
        super(MainWindow, self).__init__(parent)
        
        self.appSettings = {
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
        }
        
        self.appSettings['defaultBasemapFilePath'] = os.path.join(self.appSettings['appDir'], self.appSettings['dataDir'], self.appSettings['basemapDir'], self.appSettings['defaultBasemapFile'])
        self.appSettings['defaultVectorFilePath'] = os.path.join(self.appSettings['appDir'], self.appSettings['dataDir'], self.appSettings['vectorDir'], self.appSettings['defaultVectorFile'])

        self.setupUi()
        
        self.installEventFilter(self)
        
        self.openDialogs = []
        
        self.layerListModel = QtGui.QStandardItemModel(self.layerListView)
        self.layerListView.setModel(self.layerListModel)
        
        self.layerListView.clicked.connect(self.handlerSelectLayer)
        self.layerListModel.itemChanged.connect(self.handlerCheckLayer)
        
        # Init the logger
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_box.setFormatter(formatter)
        self.logger.addHandler(self.log_box)
        self.logger.setLevel(logging.DEBUG)
        
        # App action handlers
        self.actionQuit.triggered.connect(QtGui.qApp.quit)
        self.actionShowBasemapLayer.triggered.connect(self.handlerShowBasemapLayer)
        self.actionShowVectorLayer.triggered.connect(self.handlerShowVectorLayer)
        self.actionZoomIn.triggered.connect(self.handlerZoomIn)
        self.actionZoomOut.triggered.connect(self.handlerZoomOut)
        self.actionPan.triggered.connect(self.handlerSetPanMode)
        self.actionExplore.triggered.connect(self.handlerSetExploreMode)
        self.actionAddLayer.triggered.connect(self.handlerAddLayer)
        self.actionDeleteLayer.triggered.connect(self.handlerDeleteLayer)
        
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
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix.triggered.connect(self.handlerDialogLumensSCIENDOCalculateTransitionMatrix)
        self.actionDialogLumensSCIENDOCreateRasterCube.triggered.connect(self.handlerDialogLumensSCIENDOCreateRasterCube)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence.triggered.connect(self.handlerDialogLumensSCIENDOCalculateWeightofEvidence)
        self.actionDialogLumensSCIENDOSimulateLandUseChange.triggered.connect(self.handlerDialogLumensSCIENDOSimulateLandUseChange)
        self.actionDialogLumensSCIENDOSimulateWithScenario.triggered.connect(self.handlerDialogLumensSCIENDOSimulateWithScenario)
    
    
    def eventFilter(self, object, event):
        """
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            print 'widget window has gained focus'
            if not self.appSettings['DialogLumensOpenDatabase']['projectFile']:
                self.actionLumensCloseDatabase.setDisabled(True)
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
                self.actionDialogLumensSCIENDOCalculateTransitionMatrix.setDisabled(True)
                self.actionDialogLumensSCIENDOCreateRasterCube.setDisabled(True)
                self.actionDialogLumensSCIENDOCalculateWeightofEvidence.setDisabled(True)
                self.actionDialogLumensSCIENDOSimulateLandUseChange.setDisabled(True)
                self.actionDialogLumensSCIENDOSimulateWithScenario.setDisabled(True)
            else:
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
                self.actionDialogLumensSCIENDOCalculateTransitionMatrix.setEnabled(True)
                self.actionDialogLumensSCIENDOCreateRasterCube.setEnabled(True)
                self.actionDialogLumensSCIENDOCalculateWeightofEvidence.setEnabled(True)
                self.actionDialogLumensSCIENDOSimulateLandUseChange.setEnabled(True)
                self.actionDialogLumensSCIENDOSimulateWithScenario.setEnabled(True)
        elif event.type()== QtCore.QEvent.WindowDeactivate:
            print 'widget window has lost focus'
        elif event.type()== QtCore.QEvent.FocusIn:
            print 'widget has gained keyboard focus'
        elif event.type()== QtCore.QEvent.FocusOut:
            print 'widget has lost keyboard focus'
        
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
        self.fileMenu = self.menubar.addMenu('File')
        self.viewMenu = self.menubar.addMenu('View')
        self.modeMenu = self.menubar.addMenu('Mode')
        self.databaseMenu = self.menubar.addMenu('Database')
        self.purMenu = self.menubar.addMenu('PUR')
        self.quesMenu = self.menubar.addMenu('QUES')
        self.taMenu = self.menubar.addMenu('TA')
        self.sciendoMenu = self.menubar.addMenu('SCIENDO')

        self.toolBar = QtGui.QToolBar(self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        
        # Create the actions and assigned them to the menus
        self.actionQuit = QtGui.QAction('Quit', self)
        self.actionQuit.setShortcut(QtGui.QKeySequence.Quit)
        
        self.actionShowBasemapLayer = QtGui.QAction('Basemap', self)
        self.actionShowBasemapLayer.setShortcut('Ctrl+B')
        self.actionShowBasemapLayer.setCheckable(True)
        
        self.actionShowVectorLayer = QtGui.QAction('Landmarks', self)
        self.actionShowVectorLayer.setShortcut('Ctrl+L')
        self.actionShowVectorLayer.setCheckable(True)
        
        self.actionShowBasemapLayer.setChecked(True)
        self.actionShowVectorLayer.setChecked(True)

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

        icon = QtGui.QIcon(':/ui/icons/iconActionExplore.png')
        self.actionExplore = QtGui.QAction(icon, 'Explore', self)
        self.actionExplore.setShortcut('Ctrl+2')
        self.actionExplore.setCheckable(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionAdd.png')
        self.actionAddLayer = QtGui.QAction(icon, 'Add Layer', self)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionDelete.png')
        self.actionDeleteLayer = QtGui.QAction(icon, 'Delete Layer', self)
        self.actionDeleteLayer.setDisabled(True)
        
        self.fileMenu.addAction(self.actionQuit)
        
        self.viewMenu.addAction(self.actionZoomIn)
        self.viewMenu.addAction(self.actionZoomOut)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.actionShowBasemapLayer)
        self.viewMenu.addAction(self.actionShowVectorLayer)
        
        self.modeMenu.addAction(self.actionPan)
        self.modeMenu.addAction(self.actionExplore)

        self.toolBar.addAction(self.actionAddLayer)
        self.toolBar.addAction(self.actionDeleteLayer)
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addAction(self.actionPan)
        self.toolBar.addAction(self.actionExplore)
        
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
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix = QtGui.QAction('Calculate transition matrix', self)
        self.actionDialogLumensSCIENDOCreateRasterCube = QtGui.QAction('Create raster cube of factors', self)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence = QtGui.QAction('Calculate weight of evidence', self)
        self.actionDialogLumensSCIENDOSimulateLandUseChange = QtGui.QAction('Simulate land use change', self)
        self.actionDialogLumensSCIENDOSimulateWithScenario = QtGui.QAction('Simulate with scenario', self)
        
        self.lowEmissionDevelopmentMenu = self.sciendoMenu.addMenu('Low emission development analysis')
        self.landUseChangeModelingMenu = self.sciendoMenu.addMenu('Land use change modeling')
        self.historicalBaselineMenu = self.lowEmissionDevelopmentMenu.addMenu('Historical baseline')
        self.historicalBaselineMenu.addAction(self.actionDialogLumensSCIENDOHistoricalBaselineProjection)
        self.lowEmissionDevelopmentMenu.addAction(self.actionDialogLumensSCIENDODriversAnalysis)
        self.lowEmissionDevelopmentMenu.addAction(self.actionDialogLumensSCIENDOBuildScenario)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCalculateTransitionMatrix)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCreateRasterCube)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOCalculateWeightofEvidence)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOSimulateLandUseChange)
        self.landUseChangeModelingMenu.addAction(self.actionDialogLumensSCIENDOSimulateWithScenario)
        
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
        self.layoutMain.addLayout(self.layoutBody)
        
        self.log_box = QPlainTextEditLogger(self)
        self.layoutMain.addWidget(self.log_box.widget)
        
        self.centralWidget.setLayout(self.layoutMain)
        
        # Initialize the mapcanvas and map tools
        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.useImageToRender(False)
        self.mapCanvas.setCanvasColor(QtCore.Qt.white)
        ##self.mapCanvas.show()

        self.panTool = PanTool(self.mapCanvas)
        self.panTool.setAction(self.actionPan)

        self.exploreTool = ExploreTool(self)
        self.exploreTool.setAction(self.actionExplore)

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
            logging.getLogger(type(self).__name__).info('select LUMENS database: %s', lumensDatabase)
            
            self.lumensOpenDatabase(lumensDatabase)
    
    
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
            #print outputs
            # outputs['overview_ALG0'] => temporary raster file
            
            self.appSettings['DialogLumensOpenDatabase']['projectFile'] = lumensDatabase
            self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = os.path.dirname(lumensDatabase)
            
            self.lineEditActiveProject.setText(lumensDatabase)
            
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
            self.actionDialogLumensSCIENDOCalculateTransitionMatrix.setEnabled(True)
            self.actionDialogLumensSCIENDOCreateRasterCube.setEnabled(True)
            self.actionDialogLumensSCIENDOCalculateWeightofEvidence.setEnabled(True)
            self.actionDialogLumensSCIENDOSimulateLandUseChange.setEnabled(True)
            self.actionDialogLumensSCIENDOSimulateWithScenario.setEnabled(True)
        
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
        self.actionDialogLumensSCIENDOCalculateTransitionMatrix.setDisabled(True)
        self.actionDialogLumensSCIENDOCreateRasterCube.setDisabled(True)
        self.actionDialogLumensSCIENDOCalculateWeightofEvidence.setDisabled(True)
        self.actionDialogLumensSCIENDOSimulateLandUseChange.setDisabled(True)
        self.actionDialogLumensSCIENDOSimulateWithScenario.setDisabled(True)
        
        logging.getLogger(__name__).info('end: LUMENS Close Database')
    
    
    def handlerLumensDeleteData(self):
        """
        """
        logging.getLogger(type(self).__name__).info('start: lumensdeletedata')
            
        self.actionLumensDeleteData.setDisabled(True)
        
        outputs = general.runalg('r:lumensdeletedata')
        
        self.actionLumensDeleteData.setEnabled(True)
        
        logging.getLogger(type(self).__name__).info('end: lumensdeletedata')
    
    
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
    
    
    def checkDefaultBasemap(self):
        """
        """
        if os.path.isfile(self.appSettings['defaultBasemapFilePath']):
            return True
        else:
            self.actionShowBasemapLayer.setChecked(False)
            self.actionShowBasemapLayer.setDisabled(True)
            return False
    
    
    def checkDefaultVector(self):
        """
        """
        if os.path.isfile(self.appSettings['defaultVectorFilePath']):
            return True
        else:
            self.actionShowVectorLayer.setChecked(False)
            self.actionShowVectorLayer.setDisabled(True)
            return False
    
    
    def loadMap(self):
        """
        """
        self.basemap_layer = QgsRasterLayer(self.appSettings['defaultBasemapFilePath'], 'basemap')
        QgsMapLayerRegistry.instance().addMapLayer(self.basemap_layer)
        
        if self.checkDefaultVector():
            self.vector_layer = QgsVectorLayer(self.appSettings['defaultVectorFilePath'], 'vector', 'ogr')
            QgsMapLayerRegistry.instance().addMapLayer(self.vector_layer)

            symbol = QgsSymbolV2.defaultSymbol(self.vector_layer.geometryType())
            renderer = QgsRuleBasedRendererV2(symbol)
            root_rule = renderer.rootRule()
            default_rule = root_rule.children()[0]

            rule = default_rule.clone()
            rule.setFilterExpression("(SCALERANK >= 0) and (SCALERANK <= 1)")
            rule.setScaleMinDenom(0)
            rule.setScaleMaxDenom(99999999)
            root_rule.appendChild(rule)

            rule = default_rule.clone()
            rule.setFilterExpression("(SCALERANK >= 2) and (SCALERANK <= 4)")
            rule.setScaleMinDenom(0)
            rule.setScaleMaxDenom(10000000)
            root_rule.appendChild(rule)

            rule = default_rule.clone()
            rule.setFilterExpression("(SCALERANK >= 5) and (SCALERANK <= 7)")
            rule.setScaleMinDenom(0)
            rule.setScaleMaxDenom(5000000)
            root_rule.appendChild(rule)

            rule = default_rule.clone()
            rule.setFilterExpression("(SCALERANK >= 7) and (SCALERANK <= 10)")
            rule.setScaleMinDenom(0)
            rule.setScaleMaxDenom(2000000)
            root_rule.appendChild(rule)

            root_rule.removeChildAt(0)
            self.vector_layer.setRendererV2(renderer)

            p = QgsPalLayerSettings()
            p.readFromLayer(self.vector_layer)
            p.enabled = True
            p.fieldName = "NAME"
            p.placement = QgsPalLayerSettings.OverPoint
            p.displayAll = True
            expr = ('CASE WHEN SCALERANK IN (0,1) THEN 18 ' +
                    'WHEN SCALERANK IN (2, 3, 4) THEN 14 ' +
                    'WHEN SCALERANK IN (5, 6, 7) THEN 12 ' +
                    'WHEN SCALERANK IN (8, 9, 10) THEN 10 ' +
                    'ELSE 9 END')
            p.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, expr, '')
            p.quadOffset = QgsPalLayerSettings.QuadrantBelow
            p.yOffset = 1
            p.labelOffsetInMapUnits = False
            p.writeToLayer(self.vector_layer)

            labelingEngine = QgsPalLabeling()
            self.mapCanvas.mapRenderer().setLabelingEngine(labelingEngine)
        
        self.showVisibleMapLayers()
        
        ###self.addLayer([self.appSettings['defaultBasemapFilePath']])
        ###self.addLayer([self.appSettings['defaultVectorFilePath']])
        
        self.layoutBody.addWidget(self.mapCanvas)
        ##self.centralWidget.setLayout(self.layoutBody)
    
    
    def showVisibleMapLayers(self, mapCanvasLayers=None):
        """
        """
        layers = []
        
        if mapCanvasLayers:
            for mapCanvasLayer in mapCanvasLayers:
                layers.append(QgsMapCanvasLayer(mapCanvasLayer))
        
        if self.actionShowVectorLayer.isChecked():
            layers.append(QgsMapCanvasLayer(self.vector_layer))
            self.mapCanvas.setExtent(QgsRectangle(95, -11, 140, 11))
        if self.actionShowBasemapLayer.isChecked():
            layers.append(QgsMapCanvasLayer(self.basemap_layer))
            self.mapCanvas.setExtent(QgsRectangle(95, -11, 140, 11))
        
        self.mapCanvas.setLayerSet(layers)
    
    
    def handlerShowBasemapLayer(self):
        """
        """
        self.showVisibleMapLayers()
    
    
    def handlerShowVectorLayer(self):
        """
        """
        self.showVisibleMapLayers()
    
    
    def handlerZoomIn(self):
        """
        """
        self.mapCanvas.zoomIn()
    
    
    def handlerZoomOut(self):
        """
        """
        self.mapCanvas.zoomOut()
    
    
    def handlerSetPanMode(self):
        """
        """
        self.actionPan.setChecked(True)
        self.actionExplore.setChecked(False)
        self.mapCanvas.setMapTool(self.panTool)
    
    
    def handlerSetExploreMode(self):
        """
        """
        self.actionPan.setChecked(False)
        self.actionExplore.setChecked(True)
        self.mapCanvas.setMapTool(self.exploreTool)
    
    
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def handlerSelectLayer(self, layerItemIndex):
        """
        """
        self.actionDeleteLayer.setEnabled(True)
    
    
    def handlerCheckLayer(self, layerItem):
        """TODO
        """
        if layerItem.checkState():
            QtGui.QMessageBox.information(self, 'Layer', 'Checked ' + layerItem.data())
        else:
            QtGui.QMessageBox.information(self, 'Layer', 'Unchecked ' + layerItem.data())
    
    
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
            fileName = os.path.basename(layerFile)
            
            # check for existing layers with same file name
            existingLayerItems = self.layerListModel.findItems(fileName)
                
            for existingLayerItem in existingLayerItems:
                if os.path.abspath(layerFile) == os.path.abspath(existingLayerItem.data()):
                    QtGui.QMessageBox.warning(self, 'Duplicate Layer', 'Layer "{0}" has already been added.\nPlease select another file.'.format(fileName))
                    return
            
            layer = None
            fileType = None
            fileExt = os.path.splitext(fileName)[1].lower()
            
            if  fileExt == '.shp':
                fileType = 'vector'
                layer = QgsVectorLayer(layerFile, fileName, 'ogr')
            elif fileExt == '.tif':
                fileType = 'raster'
                layer = QgsRasterLayer(layerFile, fileName)
            
            if not layer.isValid():
                print 'ERROR: Invalid layer!'
                return
            
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.mapCanvas.setExtent(layer.extent())
            self.showVisibleMapLayers([layer])
            
            layerItem = QtGui.QStandardItem(fileName)
            layerItem.setData(layerFile)
            layerItem.setToolTip(layerFile)
            layerItem.setEditable(False)
            layerItem.setCheckable(True)
            layerItem.setCheckState(QtCore.Qt.Checked)
            self.layerListModel.appendRow(layerItem)
    
    
    def handlerDeleteLayer(self):
        """
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        #layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        #QtGui.QMessageBox.information(self, 'Layer', layerItem.data())
        self.layerListModel.removeRow(layerItemIndex.row())
        
        if not self.layerListModel.rowCount():
            self.actionDeleteLayer.setDisabled(True)
        


#############################################################################


class ExploreTool(QgsMapToolIdentify):
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

            name = feature.attribute("NAME")
            if name != None: info.append(name)

            admin_0 = feature.attribute("ADM0NAME")
            admin_1 = feature.attribute("ADM1NAME")
            if admin_0 and admin_1:
                info.append(admin_1 + ", " + admin_0)

            timezone = feature.attribute("TIMEZONE")
            if timezone != None:
                info.append("Timezone: " + timezone)

            longitude = geometry.asPoint().x()
            latitude  = geometry.asPoint().y()
            info.append("Lat/Long: %0.4f, %0.4f" % (latitude, longitude))

            QtGui.QMessageBox.information(self.window, "Feature Info", "\n".join(info))


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
        window.loadMap()
        window.handlerSetPanMode()
    
    app.exec_()
    app.deleteLater()
    QgsApplication.exitQgis()


#############################################################################


if __name__ == "__main__":
    main()

