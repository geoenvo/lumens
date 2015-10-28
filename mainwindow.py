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
            'selectDatabasefileExt': '.dbf',
            'selectHTMLfileExt': '.html',
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
        self.buttonLumensDeleteData.clicked.connect(self.handlerLumensDeleteData)
        self.buttonDialogLumensAddLandcoverRaster.clicked.connect(self.handlerDialogLumensAddLandcoverRaster)
        self.buttonDialogLumensAddPeat.clicked.connect(self.handlerDialogLumensAddPeat)
        self.buttonDialogLumensAddFactorData.clicked.connect(self.handlerDialogLumensAddFactorData)
        self.buttonDialogLumensAddPlanningUnit.clicked.connect(self.handlerDialogLumensAddPlanningUnit)
        self.buttonDialogLumensPURCreateReferenceData.clicked.connect(self.handlerDialogLumensPURCreateReferenceData)
        self.buttonDialogLumensPURPreparePlanningUnit.clicked.connect(self.handlerDialogLumensPURPreparePlanningUnit)
        self.buttonDialogLumensPURReconcilePlanningUnit.clicked.connect(self.handlerDialogLumensPURReconcilePlanningUnit)
        self.buttonDialogLumensPURFinalization.clicked.connect(self.handlerDialogLumensPURFinalization)
        self.buttonDialogLumensPreQUESLandcoverChangeAnalysis.clicked.connect(self.handlerDialogLumensPreQUESLandcoverChangeAnalysis)
        self.buttonDialogLumensPreQUESLandcoverTrajectoriesAnalysis.clicked.connect(self.handlerDialogLumensPreQUESLandcoverTrajectoriesAnalysis)
        self.buttonDialogLumensQUESCCarbonAccounting.clicked.connect(self.handlerDialogLumensQUESCCarbonAccounting)
        self.buttonDialogLumensQUESCPeatlandCarbonAccounting.clicked.connect(self.handlerDialogLumensQUESCPeatlandCarbonAccounting)
        self.buttonDialogLumensQUESCSummarizeMultiplePeriod.clicked.connect(self.handlerDialogLumensQUESCSummarizeMultiplePeriod)
        self.buttonDialogLumensQUESBAnalysis.clicked.connect(self.handlerDialogLumensQUESBAnalysis)
        self.buttonDialogLumensTAAbacusOpportunityCost.clicked.connect(self.handlerDialogLumensTAAbacusOpportunityCost)
        self.buttonDialogLumensTAOpportunityCost.clicked.connect(self.handlerDialogLumensTAOpportunityCost)
        self.buttonDialogLumensTAOpportunityCostMap.clicked.connect(self.handlerDialogLumensTAOpportunityCostMap)
        self.buttonDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.clicked.connect(self.handlerDialogLumensTARegionalEconomySingleIODescriptiveAnalysis)
        self.buttonDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.clicked.connect(self.handlerDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis)
        self.buttonDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.clicked.connect(self.handlerDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis)
        self.buttonDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.clicked.connect(self.handlerDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis)
        self.buttonDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.clicked.connect(self.handlerDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis)
        self.buttonDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.clicked.connect(self.handlerDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis)
    
    
    def eventFilter(self, object, event):
        """
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            print "widget window has gained focus"
            if not self.appSettings['DialogLumensOpenDatabase']['projectFile']:
                self.buttonLumensCloseDatabase.setDisabled(True)
                self.buttonLumensDeleteData.setDisabled(True)
                self.buttonDialogLumensAddLandcoverRaster.setDisabled(True)
                self.buttonDialogLumensAddPeat.setDisabled(True)
                self.buttonDialogLumensAddFactorData.setDisabled(True)
                self.buttonDialogLumensAddPlanningUnit.setDisabled(True)
                self.buttonDialogLumensPURCreateReferenceData.setDisabled(True)
                self.buttonDialogLumensPURPreparePlanningUnit.setDisabled(True)
                self.buttonDialogLumensPURReconcilePlanningUnit.setDisabled(True)
                self.buttonDialogLumensPURFinalization.setDisabled(True)
                self.buttonDialogLumensPreQUESLandcoverChangeAnalysis.setDisabled(True)
                self.buttonDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setDisabled(True)
                self.buttonDialogLumensQUESCCarbonAccounting.setDisabled(True)
                self.buttonDialogLumensQUESCPeatlandCarbonAccounting.setDisabled(True)
                self.buttonDialogLumensQUESCSummarizeMultiplePeriod.setDisabled(True)
                self.buttonDialogLumensQUESBAnalysis.setDisabled(True)
                self.buttonDialogLumensTAAbacusOpportunityCost.setDisabled(True)
                self.buttonDialogLumensTAOpportunityCost.setDisabled(True)
                self.buttonDialogLumensTAOpportunityCostMap.setDisabled(True)
                self.buttonDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setDisabled(True)
                self.buttonDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setDisabled(True)
                self.buttonDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setDisabled(True)
                self.buttonDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setDisabled(True)
                self.buttonDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setDisabled(True)
                self.buttonDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setDisabled(True)
            else:
                self.buttonLumensCloseDatabase.setEnabled(True)
                self.buttonLumensDeleteData.setEnabled(True)
                self.buttonDialogLumensAddLandcoverRaster.setEnabled(True)
                self.buttonDialogLumensAddPeat.setEnabled(True)
                self.buttonDialogLumensAddFactorData.setEnabled(True)
                self.buttonDialogLumensAddPlanningUnit.setEnabled(True)
                self.buttonDialogLumensPURCreateReferenceData.setEnabled(True)
                self.buttonDialogLumensPURPreparePlanningUnit.setEnabled(True)
                self.buttonDialogLumensPURReconcilePlanningUnit.setEnabled(True)
                self.buttonDialogLumensPURFinalization.setEnabled(True)
                self.buttonDialogLumensPreQUESLandcoverChangeAnalysis.setEnabled(True)
                self.buttonDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setEnabled(True)
                self.buttonDialogLumensQUESCCarbonAccounting.setEnabled(True)
                self.buttonDialogLumensQUESCPeatlandCarbonAccounting.setEnabled(True)
                self.buttonDialogLumensQUESCSummarizeMultiplePeriod.setEnabled(True)
                self.buttonDialogLumensQUESBAnalysis.setEnabled(True)
                self.buttonDialogLumensTAAbacusOpportunityCost.setEnabled(True)
                self.buttonDialogLumensTAOpportunityCost.setEnabled(True)
                self.buttonDialogLumensTAOpportunityCostMap.setEnabled(True)
                self.buttonDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setEnabled(True)
                self.buttonDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setEnabled(True)
                self.buttonDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setEnabled(True)
                self.buttonDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setEnabled(True)
                self.buttonDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setEnabled(True)
                self.buttonDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setEnabled(True)
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
        
        self.buttonLumensDeleteData = QtGui.QPushButton(self)
        self.buttonLumensDeleteData.setText('LUMENS Delete Data')
        layout.addWidget(self.buttonLumensDeleteData)
        
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
        
        self.buttonDialogLumensPURReconcilePlanningUnit = QtGui.QPushButton(self)
        self.buttonDialogLumensPURReconcilePlanningUnit.setText('Dialog: LUMENS PUR Reconcile Planning Unit')
        layout.addWidget(self.buttonDialogLumensPURReconcilePlanningUnit)
        
        self.buttonDialogLumensPURFinalization = QtGui.QPushButton(self)
        self.buttonDialogLumensPURFinalization.setText('Dialog: LUMENS PUR Finalization')
        layout.addWidget(self.buttonDialogLumensPURFinalization)
        
        self.buttonDialogLumensPreQUESLandcoverChangeAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensPreQUESLandcoverChangeAnalysis.setText('Dialog: LUMENS PreQUES Land Cover Change Analysis')
        layout.addWidget(self.buttonDialogLumensPreQUESLandcoverChangeAnalysis)
        
        self.buttonDialogLumensPreQUESLandcoverTrajectoriesAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setText('Dialog: LUMENS PreQUES Land Cover Trajectories Analysis')
        layout.addWidget(self.buttonDialogLumensPreQUESLandcoverTrajectoriesAnalysis)
        
        self.buttonDialogLumensQUESCCarbonAccounting = QtGui.QPushButton(self)
        self.buttonDialogLumensQUESCCarbonAccounting.setText('Dialog: LUMENS QUES-C Carbon Accounting')
        layout.addWidget(self.buttonDialogLumensQUESCCarbonAccounting)
        
        self.buttonDialogLumensQUESCPeatlandCarbonAccounting = QtGui.QPushButton(self)
        self.buttonDialogLumensQUESCPeatlandCarbonAccounting.setText('Dialog: LUMENS QUES-C Peatland Carbon Accounting')
        layout.addWidget(self.buttonDialogLumensQUESCPeatlandCarbonAccounting)
        
        self.buttonDialogLumensQUESCSummarizeMultiplePeriod = QtGui.QPushButton(self)
        self.buttonDialogLumensQUESCSummarizeMultiplePeriod.setText('Dialog: LUMENS QUES-C Summarize Multiple Period')
        layout.addWidget(self.buttonDialogLumensQUESCSummarizeMultiplePeriod)
        
        self.buttonDialogLumensQUESBAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensQUESBAnalysis.setText('Dialog: LUMENS QUES-B Analysis')
        layout.addWidget(self.buttonDialogLumensQUESBAnalysis)
        
        self.buttonDialogLumensTAAbacusOpportunityCost = QtGui.QPushButton(self)
        self.buttonDialogLumensTAAbacusOpportunityCost.setText('Dialog: LUMENS TA Abacus Opportunity Cost')
        layout.addWidget(self.buttonDialogLumensTAAbacusOpportunityCost)
        
        self.buttonDialogLumensTAOpportunityCost = QtGui.QPushButton(self)
        self.buttonDialogLumensTAOpportunityCost.setText('Dialog: LUMENS TA Opportunity Cost')
        layout.addWidget(self.buttonDialogLumensTAOpportunityCost)
        
        self.buttonDialogLumensTAOpportunityCostMap = QtGui.QPushButton(self)
        self.buttonDialogLumensTAOpportunityCostMap.setText('Dialog: LUMENS TA Opportunity Cost Map')
        layout.addWidget(self.buttonDialogLumensTAOpportunityCostMap)
        
        self.buttonDialogLumensTARegionalEconomySingleIODescriptiveAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setText('Dialog: LUMENS TA Regional Economy Single I-O Descriptive Analysis')
        layout.addWidget(self.buttonDialogLumensTARegionalEconomySingleIODescriptiveAnalysis)
        
        self.buttonDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setText('Dialog: LUMENS TA Regional Economy Time Series I-O Descriptive Analysis')
        layout.addWidget(self.buttonDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis)
        
        self.buttonDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setText('Dialog: LUMENS TA Regional Economy Land Distribution & Requirement Analysis')
        layout.addWidget(self.buttonDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis)
        
        self.buttonDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setText('Dialog: LUMENS TA Impact of Land Use to Regional Economy Indicator Analysis')
        layout.addWidget(self.buttonDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis)
        
        self.buttonDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setText('Dialog: LUMENS TA Regional Economy Final Demand Change Multiplier Analysis')
        layout.addWidget(self.buttonDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis)
        
        self.buttonDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis = QtGui.QPushButton(self)
        self.buttonDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setText('Dialog: LUMENS TA Regional Economy GDP Change Multiplier Analysis')
        layout.addWidget(self.buttonDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis)
        
        self.log_box = QPlainTextEditLogger(self)
        layout.addWidget(self.log_box.widget)
        
        contents = QtGui.QWidget()
        contents.setLayout(layout)
        
        scrollArea = QtGui.QScrollArea()
        scrollArea.setFixedHeight(640)
        scrollArea.setWidget(contents)
        
        self.setCentralWidget(scrollArea)
        self.setWindowTitle('LUMENS: Alpha')
        self.setFixedWidth(425)
        ##self.setMinimumSize(800, 400)
        ##self.resize(self.sizeHint())
    
    
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
    
    
    def handlerLumensDeleteData(self):
        """
        """
        logging.getLogger(type(self).__name__).info('start: lumensdeletedata')
            
        self.buttonLumensDeleteData.setDisabled(True)
        
        outputs = general.runalg('r:lumensdeletedata')
        
        self.buttonLumensDeleteData.setEnabled(True)
        
        logging.getLogger(type(self).__name__).info('end: lumensdeletedata')
    
    
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
            self.buttonLumensDeleteData.setEnabled(True)
            self.buttonDialogLumensAddLandcoverRaster.setEnabled(True)
            self.buttonDialogLumensAddPeat.setEnabled(True)
            self.buttonDialogLumensAddFactorData.setEnabled(True)
            self.buttonDialogLumensAddPlanningUnit.setEnabled(True)
            self.buttonDialogLumensPURCreateReferenceData.setEnabled(True)
            self.buttonDialogLumensPURPreparePlanningUnit.setEnabled(True)
            self.buttonDialogLumensPURReconcilePlanningUnit.setEnabled(True)
            self.buttonDialogLumensPURFinalization.setEnabled(True)
            self.buttonDialogLumensPreQUESLandcoverChangeAnalysis.setEnabled(True)
            self.buttonDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setEnabled(True)
            self.buttonDialogLumensQUESCCarbonAccounting.setEnabled(True)
            self.buttonDialogLumensQUESCPeatlandCarbonAccounting.setEnabled(True)
            self.buttonDialogLumensQUESCSummarizeMultiplePeriod.setEnabled(True)
            self.buttonDialogLumensQUESBAnalysis.setEnabled(True)
            self.buttonDialogLumensTAAbacusOpportunityCost.setEnabled(True)
            self.buttonDialogLumensTAOpportunityCost.setEnabled(True)
            self.buttonDialogLumensTAOpportunityCostMap.setEnabled(True)
            self.buttonDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setEnabled(True)
            self.buttonDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setEnabled(True)
            self.buttonDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setEnabled(True)
            self.buttonDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setEnabled(True)
            self.buttonDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setEnabled(True)
            self.buttonDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setEnabled(True)
        
        self.buttonLumensOpenDatabase.setEnabled(True)
        
        logging.getLogger(__name__).info('end: LUMENS Open Database')
    
    
    def lumensCloseDatabase(self):
        """
        """
        logging.getLogger(__name__).info('start: LUMENS Close Database')
        
        self.buttonLumensCloseDatabase.setDisabled(True)
        
        outputs = general.runalg('modeler:lumens_close_database')
        
        self.appSettings['DialogLumensOpenDatabase']['projectFile'] = ''
        self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = ''
        
        self.lineEditActiveProject.clear()
        self.buttonLumensDeleteData.setDisabled(True)
        self.buttonDialogLumensAddLandcoverRaster.setDisabled(True)
        self.buttonDialogLumensAddPeat.setDisabled(True)
        self.buttonDialogLumensAddFactorData.setDisabled(True)
        self.buttonDialogLumensAddPlanningUnit.setDisabled(True)
        self.buttonDialogLumensPURCreateReferenceData.setDisabled(True)
        self.buttonDialogLumensPURPreparePlanningUnit.setDisabled(True)
        self.buttonDialogLumensPURReconcilePlanningUnit.setDisabled(True)
        self.buttonDialogLumensPURFinalization.setDisabled(True)
        self.buttonDialogLumensPreQUESLandcoverChangeAnalysis.setDisabled(True)
        self.buttonDialogLumensPreQUESLandcoverTrajectoriesAnalysis.setDisabled(True)
        self.buttonDialogLumensQUESCCarbonAccounting.setDisabled(True)
        self.buttonDialogLumensQUESCPeatlandCarbonAccounting.setDisabled(True)
        self.buttonDialogLumensQUESCSummarizeMultiplePeriod.setDisabled(True)
        self.buttonDialogLumensQUESBAnalysis.setDisabled(True)
        self.buttonDialogLumensTAAbacusOpportunityCost.setDisabled(True)
        self.buttonDialogLumensTAOpportunityCost.setDisabled(True)
        self.buttonDialogLumensTAOpportunityCostMap.setDisabled(True)
        self.buttonDialogLumensTARegionalEconomySingleIODescriptiveAnalysis.setDisabled(True)
        self.buttonDialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis.setDisabled(True)
        self.buttonDialogLumensTARegionalEconomyLandDistributionRequirementAnalysis.setDisabled(True)
        self.buttonDialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis.setDisabled(True)
        self.buttonDialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis.setDisabled(True)
        self.buttonDialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis.setDisabled(True)
        
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
    