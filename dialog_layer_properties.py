#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui


class DialogLayerProperties(QtGui.QDialog):
    """
    """
    def __init__(self, layer, parent):
        super(DialogLayerProperties, self).__init__(parent)
        self.layer = layer
        self.main = parent
        self.dialogTitle = 'LUMENS Layer Properties - ' + self.layer.name()
        self.layerSymbolFillColor = self.labelColor = QtGui.QColor(0, 0, 0) # black
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLayerProperties init'
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
        
        self.loadLayerSettings()
        
        self.sliderLayerTransparency.sliderMoved.connect(self.handlerSliderLayerTransparencyMoved)
        self.spinBoxLayerTransparency.valueChanged.connect(self.handlerSpinBoxLayerTransparencyValueChanged)
        self.buttonLayerSymbolFillColor.clicked.connect(self.handlerSelectLayerSymbolFillColor)
        self.buttonLabelColor.clicked.connect(self.handlerSelectLabelColor)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.groupBoxLayerStyle = QtGui.QGroupBox('Style')
        self.layoutGroupBoxLayerStyle = QtGui.QVBoxLayout()
        self.layoutGroupBoxLayerStyle.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLayerStyle.setLayout(self.layoutGroupBoxLayerStyle)
        self.layoutLayerStyleInfo = QtGui.QVBoxLayout()
        self.layoutLayerStyle = QtGui.QGridLayout()
        self.layoutGroupBoxLayerStyle.addLayout(self.layoutLayerStyleInfo)
        self.layoutGroupBoxLayerStyle.addLayout(self.layoutLayerStyle)
        
        self.labelLayerStyleInfo = QtGui.QLabel()
        self.labelLayerStyleInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLayerStyleInfo.addWidget(self.labelLayerStyleInfo)
        
        self.labelLayerTransparency = QtGui.QLabel()
        self.labelLayerTransparency.setText('Transparency:')
        self.layoutLayerStyle.addWidget(self.labelLayerTransparency, 0, 0)
        
        self.sliderLayerTransparency = QtGui.QSlider()
        self.sliderLayerTransparency.setRange(0, 100)
        self.sliderLayerTransparency.setOrientation(QtCore.Qt.Horizontal)
        self.layoutLayerStyle.addWidget(self.sliderLayerTransparency, 0, 1)
        
        self.spinBoxLayerTransparency = QtGui.QSpinBox()
        self.spinBoxLayerTransparency.setRange(0, 100)
        self.layoutLayerStyle.addWidget(self.spinBoxLayerTransparency, 0, 2)
        
        self.labelLayerSymbolFillColor = QtGui.QLabel()
        self.labelLayerSymbolFillColor.setText('Fill color:')
        self.layoutLayerStyle.addWidget(self.labelLayerSymbolFillColor, 1, 0)
        
        self.buttonLayerSymbolFillColor = QtGui.QPushButton()
        self.buttonLayerSymbolFillColor.setFixedWidth(50)
        self.buttonLayerSymbolFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
        self.layoutLayerStyle.addWidget(self.buttonLayerSymbolFillColor, 1, 1)
        
        ######################################################################
        
        self.groupBoxLayerLabel = QtGui.QGroupBox('Label')
        self.layoutGroupBoxLayerLabel = QtGui.QVBoxLayout()
        self.layoutGroupBoxLayerLabel.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLayerLabel.setLayout(self.layoutGroupBoxLayerLabel)
        self.layoutLayerLabelInfo = QtGui.QVBoxLayout()
        self.layoutLayerLabel = QtGui.QGridLayout()
        self.layoutGroupBoxLayerLabel.addLayout(self.layoutLayerLabelInfo)
        self.layoutGroupBoxLayerLabel.addLayout(self.layoutLayerLabel)
        
        self.labelLayerLabelInfo = QtGui.QLabel()
        self.labelLayerLabelInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLayerLabelInfo.addWidget(self.labelLayerLabelInfo)
        
        self.labelLayerLabelEnabled = QtGui.QLabel()
        self.labelLayerLabelEnabled.setText('Enable label:')
        self.layoutLayerLabel.addWidget(self.labelLayerLabelEnabled, 0, 0)
        
        self.checkBoxLayerLabelEnabled = QtGui.QCheckBox()
        self.checkBoxLayerLabelEnabled.setChecked(False)
        self.layoutLayerLabel.addWidget(self.checkBoxLayerLabelEnabled, 0, 1)
        self.labelLayerLabelEnabled.setBuddy(self.checkBoxLayerLabelEnabled)
        
        self.labelLayerLabelAttribute = QtGui.QLabel()
        self.labelLayerLabelAttribute.setText('Label attribute:')
        self.layoutLayerLabel.addWidget(self.labelLayerLabelAttribute, 1, 0)
        
        self.comboBoxLayerAttribute = QtGui.QComboBox()
        self.comboBoxLayerAttribute.setDisabled(True)
        self.layoutLayerLabel.addWidget(self.comboBoxLayerAttribute, 1, 1)
        
        self.labelLayerLabelSize = QtGui.QLabel()
        self.labelLayerLabelSize.setText('Label size (points):')
        self.layoutLayerLabel.addWidget(self.labelLayerLabelSize, 2, 0)
        
        self.spinBoxLabelSize = QtGui.QSpinBox()
        self.spinBoxLabelSize.setRange(1, 100)
        self.spinBoxLabelSize.setValue(9)
        self.layoutLayerLabel.addWidget(self.spinBoxLabelSize, 2, 1)
        self.labelLayerLabelSize.setBuddy(self.spinBoxLabelSize)
        
        self.labelLayerLabelColor = QtGui.QLabel()
        self.labelLayerLabelColor.setText('Label color:')
        self.layoutLayerLabel.addWidget(self.labelLayerLabelColor, 3, 0)
        
        self.buttonLabelColor = QtGui.QPushButton()
        self.buttonLabelColor.setFixedWidth(50)
        self.buttonLabelColor.setStyleSheet('background-color: {0};'.format(self.labelColor.name()))
        self.layoutLayerLabel.addWidget(self.buttonLabelColor, 3, 1)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        
        self.dialogLayout.addWidget(self.groupBoxLayerStyle)
        self.dialogLayout.addWidget(self.groupBoxLayerLabel)
        self.dialogLayout.addWidget(self.buttonBox)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 400)
        self.resize(parent.sizeHint())
    
    
    def loadLayerSettings(self):
        """
        """
        # Get layer attributes
        provider = self.layer.dataProvider()
        
        if not provider.isValid():
            logging.getLogger(type(self).__name__).error('invalid layer')
            return
        
        attributes = []
        for field in provider.fields():
            attributes.append(field.name())
        
        self.comboBoxLayerAttribute.clear()
        self.comboBoxLayerAttribute.addItems(sorted(attributes))
        self.comboBoxLayerAttribute.setEnabled(True)
        
        # Get layer transparency setting
        self.sliderLayerTransparency.setValue(self.layer.layerTransparency())
        self.spinBoxLayerTransparency.setValue(self.layer.layerTransparency())
        
        # Get layer symbol fill color
        symbols = self.layer.rendererV2().symbols()
        self.layerSymbolFillColor = symbols[0].color()
        self.buttonLayerSymbolFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
        
        # Get layer label settings
        self.p = QgsPalLayerSettings()
        self.p.readFromLayer(self.layer)
        
        if self.p.enabled:
            self.checkBoxLayerLabelEnabled.setChecked(True)
            self.comboBoxLayerAttribute.setCurrentIndex(self.comboBoxLayerAttribute.findText(self.p.fieldName))
            self.spinBoxLabelSize.setValue(self.p.textFont.pointSize())
            self.labelColor = self.p.textColor
            self.buttonLabelColor.setStyleSheet('background-color: {0};'.format(self.labelColor.name()))
            
    
    #***********************************************************
    # 'Layer Properties' QPushButton handlers
    #***********************************************************
    def handlerSliderLayerTransparencyMoved(self, newPosition):
        """
        """
        self.spinBoxLayerTransparency.setValue(newPosition)
    
    
    def handlerSpinBoxLayerTransparencyValueChanged(self, newValue):
        """
        """
        self.sliderLayerTransparency.setValue(newValue)
    
    
    def handlerSelectLayerSymbolFillColor(self):
        """
        """
        dialog = QtGui.QColorDialog(self.layerSymbolFillColor)
        
        if dialog.exec_():
            self.layerSymbolFillColor = dialog.selectedColor()
            self.buttonLayerSymbolFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
    
    
    def handlerSelectLabelColor(self):
        """
        """
        dialog = QtGui.QColorDialog(self.labelColor)
        
        if dialog.exec_():
            self.labelColor = dialog.selectedColor()
            self.buttonLabelColor.setStyleSheet('background-color: {0};'.format(self.labelColor.name()))
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def accept(self):
        """
        """
        # Process layer transparency setting
        self.layer.setLayerTransparency(self.sliderLayerTransparency.value())
        
        # Process layer symbol fill color
        symbols = self.layer.rendererV2().symbols()
        symbol = symbols[0]
        symbol.setColor(self.layerSymbolFillColor)
        
        # Process layer label settings
        if self.checkBoxLayerLabelEnabled.isChecked():
            self.p.enabled = True
            
            self.p.fieldName = self.comboBoxLayerAttribute.currentText()
            self.p.placement = QgsPalLayerSettings.OverPoint
            self.p.displayAll = True
            self.p.textFont.setPointSize(self.spinBoxLabelSize.value())
            self.p.textColor = self.labelColor
            self.p.quadOffset = QgsPalLayerSettings.QuadrantBelow
            self.p.yOffset = 1
            self.p.labelOffsetInMapUnits = False
        else:
            self.p.enabled = False
        
        self.p.writeToLayer(self.layer)
        
        # Finally fresh the MapCanvas and close the dialog
        self.main.mapCanvas.refresh()
        
        QtGui.QDialog.accept(self)
    
    
    def reject(self):
        """
        """
        QtGui.QDialog.reject(self)
    