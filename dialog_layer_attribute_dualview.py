#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui


class DialogLayerAttributeDualView(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, vectorLayer, parent):
        super(DialogLayerAttributeDualView, self).__init__(parent)
        self.vectorLayer = vectorLayer
        self.vectorLayer.startEditing()
        self.main = parent
        
        self.dialogTitle = 'Attribute Editor - ' + self.vectorLayer.name()
        
        self.setupUi(self)
        
        self.dualView.init(self.vectorLayer, self.main.mapCanvas, QgsDistanceArea())
        self.dualView.setView(QgsDualView.AttributeEditor)
    
    
    def closeEvent(self, event):
        """Called when the widget is closed
        """
        ##super(DialogLayerAttributeDualView, self).closeEvent(event)
        
        if self.vectorLayer.isModified():
            reply = QtGui.QMessageBox.question(
                self,
                'Save layer changes',
                'Do you want to save the changes made to layer {0}?'.format(self.vectorLayer.name()),
                QtGui.QMessageBox.Save|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Cancel
            )
            
            if reply == QtGui.QMessageBox.Save:
                self.vectorLayer.commitChanges() # save changes to layer
                event.accept()
            elif reply == QtGui.QMessageBox.No:
                event.accept()
            elif reply == QtGui.QMessageBox.Cancel:
                event.ignore()
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout(parent)
        self.dualView = QgsDualView()
        self.dialogLayout.addWidget(self.dualView)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 400)
        self.resize(parent.sizeHint())

