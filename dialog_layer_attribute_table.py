#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui


class DialogLayerAttributeTable(QtGui.QDialog):
    """Dialog class for showing the attribute table of a vector layer.
    """
    
    def __init__(self, vectorLayer, parent):
        """Constructor method for initializing a layer attribute table dialog window instance.
        
        Args:
            vectorLayer (QgsVectorLayer): a vector layer instance.
            parent: the dialog's parent instance.
        """
        super(DialogLayerAttributeTable, self).__init__(parent)
        
        self.vectorLayer = vectorLayer
        self.main = parent
        self.dialogTitle = 'Attribute Table - ' + self.vectorLayer.name()
        
        self.setupUi(self)
        
        # Initialize the Attribute Table View
        self.vectorLayerCache = QgsVectorLayerCache(self.vectorLayer, self.vectorLayer.featureCount())
        self.attributeTableModel = QgsAttributeTableModel(self.vectorLayerCache)
        self.attributeTableModel.loadLayer()
        self.attributeTableFilterModel = QgsAttributeTableFilterModel(self.main.mapCanvas, self.attributeTableModel)
        self.attributeTableView.setModel(self.attributeTableFilterModel)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout(parent)
        
        self.attributeTableView = QgsAttributeTableView()
        
        self.dialogLayout.addWidget(self.attributeTableView)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 400)
        self.resize(parent.sizeHint())
    
    