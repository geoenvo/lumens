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
        ##self.vectorLayer.setReadOnly(False)
        ##self.vectorLayer.startEditing()
        self.main = parent
        
        self.dialogTitle = 'Attribute Editor - ' + self.vectorLayer.name()
        
        self.setupUi(self)
        
        self.dualView.init(self.vectorLayer, self.main.mapCanvas, QgsDistanceArea())
        self.dualView.setView(QgsDualView.AttributeEditor)
        
        self.actionToggleEditLayer.triggered.connect(self.handlerToggleEditLayer)
    
    
    def closeEvent(self, event):
        """Called when the widget is closed
        """
        ##super(DialogLayerAttributeDualView, self).closeEvent(event)
        
        reply = self.confirmSaveLayer()
        
        if reply == QtGui.QMessageBox.Save:
            event.accept()
        elif reply == QtGui.QMessageBox.No:
            event.accept()
        elif reply == QtGui.QMessageBox.Cancel:
            event.ignore()
        elif reply == None:
            # Click toggle edit button => close dialog => (layer was not modified)
            self.vectorLayer.rollBack()
            self.vectorLayer.setReadOnly()
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout(parent)
        
        self.toolBar = QtGui.QToolBar(self)
        self.dialogLayout.addWidget(self.toolBar)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionToggleEdit.png')
        self.actionToggleEditLayer = QtGui.QAction(icon, 'Toggle Edit Layer', self)
        self.actionToggleEditLayer.setCheckable(True)
        self.toolBar.addAction(self.actionToggleEditLayer)
        
        self.dualView = QgsDualView()
        self.dialogLayout.addWidget(self.dualView)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 400)
        self.resize(parent.sizeHint())
    
    
    def confirmSaveLayer(self):
        """
        """
        reply = None
        
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
                self.vectorLayer.setReadOnly()
            elif reply == QtGui.QMessageBox.No:
                self.vectorLayer.rollBack()
                self.vectorLayer.setReadOnly()
            elif reply == QtGui.QMessageBox.Cancel:
                pass
            
        return reply
    
    
    def handlerToggleEditLayer(self):
        """
        """
        if self.actionToggleEditLayer.isChecked():
            self.vectorLayer.setReadOnly(False)
            self.vectorLayer.startEditing()
        else:
            reply = self.confirmSaveLayer()
            
            print reply
            
            if reply == QtGui.QMessageBox.Cancel:
                self.actionToggleEditLayer.setChecked(True) # Keep toggle edit button checked
            elif reply == None:
                # Click toggle edit button => select one feature => click toggle edit button => (layer was not modified)
                self.vectorLayer.rollBack()
                self.vectorLayer.setReadOnly()
