#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui


class DialogLayerAttributeTable(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, vectorLayer, parent):
        super(DialogLayerAttributeTable, self).__init__(parent)
        self.vectorLayer = vectorLayer
        self.main = parent
        
        self.dialogTitle = 'Attribute Table - ' + self.vectorLayer.name()
        
        self.setupUi(self)
        
        self.vectorLayerCache = QgsVectorLayerCache(self.vectorLayer, 10000)
        self.attrTableModel = QgsAttributeTableModel(self.vectorLayerCache)
        self.attrTableModel.loadLayer()
        self.attrTableFilterModel = QgsAttributeTableFilterModel(self.main.mapCanvas, self.attrTableModel)
        self.attributeTableView.setModel(self.attrTableFilterModel)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout(parent)
        self.attributeTableView = QgsAttributeTableView(parent)
        self.dialogLayout.addWidget(self.attributeTableView)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 400)
        self.resize(parent.sizeHint())

