#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui


class DialogLayerProperties(QtGui.QDialog):
    """LUMENS dialog class for editing layer properties. 
    """
    
    def __init__(self, layer, parent):
        """Constructor method for initializing a LUMENS layer properties dialog window instance.
        
        Args:
            layer (QgsVectorLayer): a vector layer instance.
            parent: the dialog's parent instance.
        """
        super(DialogLayerProperties, self).__init__(parent)
        self.layer = layer
        self.main = parent
        self.dialogTitle = 'LUMENS Layer Properties - ' + self.layer.name()
        self.layerSymbolFillColor = self.styleCategorizedColor = self.labelColor = QtGui.QColor(0, 0, 0) # black
        
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
        
        self.comboBoxStyleType.currentIndexChanged.connect(self.handlerChangeStyleType)
        self.handlerChangeStyleType(0)
        self.buttonAddStyleCategorized.clicked.connect(self.handlerAddStyleCategorized)
        self.buttonDeleteStyleCategorized.clicked.connect(self.handlerDeleteStyleCategorized)
        self.buttonDeleteAllStyleCategorized.clicked.connect(self.handlerDeleteAllStyleCategorized)
        self.sliderLayerTransparency.sliderMoved.connect(self.handlerSliderLayerTransparencyMoved)
        self.spinBoxLayerTransparency.valueChanged.connect(self.handlerSpinBoxLayerTransparencyValueChanged)
        self.buttonLayerSymbolFillColor.clicked.connect(self.handlerSelectFillColor)
        self.buttonStyleCategorizedFillColor.clicked.connect(self.handlerSelectFillColor)
        self.buttonLabelColor.clicked.connect(self.handlerSelectLabelColor)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.groupBoxLayerStyle = QtGui.QGroupBox('Style')
        self.layoutGroupBoxLayerStyle = QtGui.QVBoxLayout()
        self.layoutGroupBoxLayerStyle.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLayerStyle.setLayout(self.layoutGroupBoxLayerStyle)
        
        self.layoutLayerStyleInfo = QtGui.QVBoxLayout()
        self.layoutLayerStyle = QtGui.QVBoxLayout()
        self.layoutGroupBoxLayerStyle.addLayout(self.layoutLayerStyleInfo)
        
        styleTypes = ['Single', 'Categorized']
        self.comboBoxStyleType = QtGui.QComboBox()
        self.comboBoxStyleType.addItems(styleTypes)
        
        self.layoutGroupBoxLayerStyle.addWidget(self.comboBoxStyleType)
        self.layoutGroupBoxLayerStyle.addLayout(self.layoutLayerStyle)
        
        self.groupBoxLayerTransparency = QtGui.QGroupBox('Transparency')
        self.layoutGroupBoxLayerTransparency = QtGui.QGridLayout()
        self.groupBoxLayerTransparency.setLayout(self.layoutGroupBoxLayerTransparency)
        
        self.styleTabWidget = QtGui.QTabWidget()
        self.styleTabWidget.setTabPosition(QtGui.QTabWidget.North)
        
        self.tabStyleSingle = QtGui.QWidget()
        self.layoutGroupBoxStyleSingle = QtGui.QGridLayout()
        self.layoutGroupBoxStyleSingle.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.tabStyleSingle.setLayout(self.layoutGroupBoxStyleSingle)
        
        self.tabStyleCategorized = QtGui.QWidget()
        self.layoutGroupBoxStyleCategorized = QtGui.QGridLayout()
        self.layoutGroupBoxStyleCategorized.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.tabStyleCategorized.setLayout(self.layoutGroupBoxStyleCategorized)
        
        self.styleTabWidget.addTab(self.tabStyleSingle, 'Single')
        self.styleTabWidget.addTab(self.tabStyleCategorized, 'Categorized')
        
        self.layoutLayerStyle.addWidget(self.groupBoxLayerTransparency)
        self.layoutLayerStyle.addWidget(self.styleTabWidget)
        
        self.labelLayerStyleInfo = QtGui.QLabel()
        self.labelLayerStyleInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLayerStyleInfo.addWidget(self.labelLayerStyleInfo)
        
        # Transparency groupbox widgets
        self.labelLayerTransparency = QtGui.QLabel()
        self.labelLayerTransparency.setText('Transparency:')
        self.layoutGroupBoxLayerTransparency.addWidget(self.labelLayerTransparency, 0, 0)
        
        self.sliderLayerTransparency = QtGui.QSlider()
        self.sliderLayerTransparency.setRange(0, 100)
        self.sliderLayerTransparency.setOrientation(QtCore.Qt.Horizontal)
        self.layoutGroupBoxLayerTransparency.addWidget(self.sliderLayerTransparency, 0, 1)
        
        self.spinBoxLayerTransparency = QtGui.QSpinBox()
        self.spinBoxLayerTransparency.setRange(0, 100)
        self.layoutGroupBoxLayerTransparency.addWidget(self.spinBoxLayerTransparency, 0, 2)
        
        # Single style groupbox widgets
        self.labelLayerSymbolFillColor = QtGui.QLabel()
        self.labelLayerSymbolFillColor.setText('Fill color:')
        self.layoutGroupBoxStyleSingle.addWidget(self.labelLayerSymbolFillColor, 0, 0)
        
        self.buttonLayerSymbolFillColor = QtGui.QPushButton()
        self.buttonLayerSymbolFillColor.setObjectName('buttonLayerSymbolFillColor')
        self.buttonLayerSymbolFillColor.setFixedWidth(50)
        self.buttonLayerSymbolFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
        self.layoutGroupBoxStyleSingle.addWidget(self.buttonLayerSymbolFillColor, 0, 1)
        
        # Categorized style groupbox widgets
        self.labelStyleCategorizedAttribute = QtGui.QLabel()
        self.labelStyleCategorizedAttribute.setText('Attribute:')
        self.layoutGroupBoxStyleCategorized.addWidget(self.labelStyleCategorizedAttribute, 0, 0)
        
        self.comboBoxStyleCategorizedAttribute = QtGui.QComboBox()
        self.comboBoxStyleCategorizedAttribute.setDisabled(True)
        self.layoutGroupBoxStyleCategorized.addWidget(self.comboBoxStyleCategorizedAttribute, 0, 1)
        
        self.labelStyleCategorizedFillColor = QtGui.QLabel()
        self.labelStyleCategorizedFillColor.setText('Fill color:')
        self.layoutGroupBoxStyleCategorized.addWidget(self.labelStyleCategorizedFillColor, 1, 0)
        
        self.buttonStyleCategorizedFillColor = QtGui.QPushButton()
        self.buttonStyleCategorizedFillColor.setObjectName('buttonStyleCategorizedFillColor')
        self.buttonStyleCategorizedFillColor.setFixedWidth(50)
        self.buttonStyleCategorizedFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
        self.layoutGroupBoxStyleCategorized.addWidget(self.buttonStyleCategorizedFillColor, 1, 1)
        
        self.labelStyleCategorizedValue = QtGui.QLabel()
        self.labelStyleCategorizedValue.setText('Value:')
        self.layoutGroupBoxStyleCategorized.addWidget(self.labelStyleCategorizedValue, 2, 0)
        
        self.lineEditStyleCategorizedValue = QtGui.QLineEdit()
        self.layoutGroupBoxStyleCategorized.addWidget(self.lineEditStyleCategorizedValue, 2, 1)
        
        self.labelStyleCategorizedLabel = QtGui.QLabel()
        self.labelStyleCategorizedLabel.setText('Label:')
        self.layoutGroupBoxStyleCategorized.addWidget(self.labelStyleCategorizedLabel, 3, 0)
        
        self.lineEditStyleCategorizedLabel = QtGui.QLineEdit()
        self.layoutGroupBoxStyleCategorized.addWidget(self.lineEditStyleCategorizedLabel, 3, 1)
        
        self.layoutButtonStyleCategorized = QtGui.QHBoxLayout()
        self.layoutButtonStyleCategorized.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutButtonStyleCategorized.setSpacing(10)
        
        self.buttonAddStyleCategorized = QtGui.QPushButton()
        self.buttonAddStyleCategorized.setText('Add')
        self.buttonAddStyleCategorized.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleCategorized.addWidget(self.buttonAddStyleCategorized)
        
        self.buttonDeleteStyleCategorized = QtGui.QPushButton()
        self.buttonDeleteStyleCategorized.setText('Delete')
        self.buttonDeleteStyleCategorized.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleCategorized.addWidget(self.buttonDeleteStyleCategorized)
        
        self.buttonDeleteAllStyleCategorized = QtGui.QPushButton()
        self.buttonDeleteAllStyleCategorized.setText('Delete All')
        self.buttonDeleteAllStyleCategorized.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleCategorized.addWidget(self.buttonDeleteAllStyleCategorized)
        
        self.layoutGroupBoxStyleCategorized.addLayout(self.layoutButtonStyleCategorized, 4, 1)
        
        self.tableStyleCategorized = QtGui.QTableWidget()
        headersTableStyleCategorized = ['Color', 'Value', 'Label']
        self.tableStyleCategorized.setColumnCount(len(headersTableStyleCategorized))
        self.tableStyleCategorized.setHorizontalHeaderLabels(headersTableStyleCategorized)
        self.tableStyleCategorized.verticalHeader().setVisible(False)
        self.layoutGroupBoxStyleCategorized.addWidget(self.tableStyleCategorized, 5, 0, 1, 2)
        
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
        """Method for loading the layer settings and updating the form widgets.
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
        
        self.comboBoxStyleCategorizedAttribute.clear()
        self.comboBoxStyleCategorizedAttribute.addItems(sorted(attributes))
        self.comboBoxStyleCategorizedAttribute.setEnabled(True)
        
        # Get layer transparency setting
        self.sliderLayerTransparency.setValue(self.layer.layerTransparency())
        self.spinBoxLayerTransparency.setValue(self.layer.layerTransparency())
        
        # Get layer symbol fill color
        symbols = self.layer.rendererV2().symbols()
        self.layerSymbolFillColor = symbols[0].color()
        self.styleCategorizedColor = symbols[0].color()
        self.buttonLayerSymbolFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
        self.buttonStyleCategorizedFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
        
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
        """Slot method when the transparency slider is moved.
        
        Args:
            newPosition (int): the new position on the slider.
        """
        self.spinBoxLayerTransparency.setValue(newPosition)
    
    
    def handlerSpinBoxLayerTransparencyValueChanged(self, newValue):
        """Slot method when the transparency spinbox value is changed.
        
        Args:
            newValue (int): the new spinbox value.
        """
        self.sliderLayerTransparency.setValue(newValue)
    
    
    def handlerSelectFillColor(self):
        """Slot method when the fill color button is clicked.
        """
        dialog = QtGui.QColorDialog(self.layerSymbolFillColor)
        
        if dialog.exec_():
            selectedColor = dialog.selectedColor()
            sender = self.sender()
            if sender.objectName() == 'buttonLayerSymbolFillColor':
                self.layerSymbolFillColor = selectedColor
            elif sender.objectName == 'buttonStyleCategorizedFillColor':
                self.styleCategorizedColor = selectedColor
            sender.setStyleSheet('background-color: {0};'.format(selectedColor.name()))
    
    
    def handlerSelectLabelColor(self):
        """Slot method when the label color button is clicked.
        """
        dialog = QtGui.QColorDialog(self.labelColor)
        
        if dialog.exec_():
            self.labelColor = dialog.selectedColor()
            self.buttonLabelColor.setStyleSheet('background-color: {0};'.format(self.labelColor.name()))
    
    
    def handlerChangeStyleType(self, currentIndex):
        """Slot method for selecting the style tab.
        
        Args:
            currentIndex (int): the index number of the selected combobox item.
        """
        styleType = self.comboBoxStyleType.currentText()
        if styleType == 'Single':
            self.styleTabWidget.setCurrentWidget(self.tabStyleSingle)
        elif styleType == 'Categorized':
            self.styleTabWidget.setCurrentWidget(self.tabStyleCategorized)
    
    
    def handlerAddStyleCategorized(self):
        """Slot method for adding a categorized style.
        """
        value = QtGui.QTableWidgetItem(self.lineEditStyleCategorizedValue.text())
        label = QtGui.QTableWidgetItem(self.lineEditStyleCategorizedLabel.text())
        if value.text() == '' and label.text() == '':
            return
        currentRowCount = self.tableStyleCategorized.rowCount()
        color = QtGui.QTableWidgetItem('')
        color.setBackground(QtGui.QBrush(self.styleCategorizedColor))
        color.setFlags(color.flags() & ~QtCore.Qt.ItemIsEditable)
        value.setFlags(value.flags() & ~QtCore.Qt.ItemIsEditable)
        label.setFlags(label.flags() & ~QtCore.Qt.ItemIsEditable)
        self.tableStyleCategorized.insertRow(currentRowCount)
        self.tableStyleCategorized.setItem(currentRowCount, 0, color)
        self.tableStyleCategorized.setItem(currentRowCount, 1, value)
        self.tableStyleCategorized.setItem(currentRowCount, 2, label)
        self.lineEditStyleCategorizedValue.setText('')
        self.lineEditStyleCategorizedLabel.setText('')
    
    
    def handlerDeleteStyleCategorized(self):
        """Slot method for deleting a categorized style.
        """
        currentRow = self.tableStyleCategorized.currentRow()
        self.tableStyleCategorized.removeRow(currentRow)
    
    
    def handlerDeleteAllStyleCategorized(self):
        """Slot method for deleting all categorized styles.
        """
        reply = QtGui.QMessageBox.question(
            self,
            'Delete All',
            'Do you want to delete all?',
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.tableStyleCategorized.setRowCount(0)
        elif reply == QtGui.QMessageBox.Cancel:
            pass
            
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def accept(self):
        """Overload method when the dialog is accepted.
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
        """Overload method when the dialog is rejected/closed.
        """
        QtGui.QDialog.reject(self)
    