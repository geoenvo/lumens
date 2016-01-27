#!/usr/bin/env python
#-*- coding:utf-8 -*-

from qgis.core import *
from PyQt4 import QtCore, QtGui


class DialogLumensAddDataVectorAttributes(QtGui.QDialog):
    """
    """
    def __init__(self, parent, vectorFile):
        super(DialogLumensAddDataVectorAttributes, self).__init__(parent)
        self.vectorFile = vectorFile
        self.main = parent
        self.dialogTitle = 'LUMENS Select Vector Data Attributes'
        
        self.vectorIDField = None
        self.vectorNameField = None
        
        self.setupUi(self)
        
        self.loadVectorAttributes()
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.groupBoxVectorAttributes = QtGui.QGroupBox('Vector data attributes')
        self.layoutGroupBoxVectorAttributes = QtGui.QVBoxLayout()
        self.layoutGroupBoxVectorAttributes.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxVectorAttributes.setLayout(self.layoutGroupBoxVectorAttributes)
        self.layoutVectorAttributesInfo = QtGui.QVBoxLayout()
        self.layoutVectorAttributes = QtGui.QGridLayout()
        self.layoutGroupBoxVectorAttributes.addLayout(self.layoutVectorAttributesInfo)
        self.layoutGroupBoxVectorAttributes.addLayout(self.layoutVectorAttributes)
        
        self.labelVectorAttributesInfo = QtGui.QLabel()
        self.labelVectorAttributesInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutVectorAttributesInfo.addWidget(self.labelVectorAttributesInfo)
        
        self.labelVectorIDField = QtGui.QLabel()
        self.labelVectorIDField.setText('ID field:')
        self.layoutVectorAttributes.addWidget(self.labelVectorIDField, 0, 0)
        
        self.comboBoxVectorIDField = QtGui.QComboBox()
        self.comboBoxVectorIDField.setDisabled(True)
        self.layoutVectorAttributes.addWidget(self.comboBoxVectorIDField, 0, 1)
        
        self.labelVectorNameField = QtGui.QLabel()
        self.labelVectorNameField.setText('Name field:')
        self.layoutVectorAttributes.addWidget(self.labelVectorNameField, 1, 0)
        
        self.comboBoxVectorNameField = QtGui.QComboBox()
        self.comboBoxVectorNameField.setDisabled(True)
        self.layoutVectorAttributes.addWidget(self.comboBoxVectorNameField, 1, 1)
        
        ######################################################################
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        
        self.dialogLayout.addWidget(self.groupBoxVectorAttributes)
        self.dialogLayout.addWidget(self.buttonBox)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    def getVectorAttributes(self):
        """
        """
        return self.vectorIDField, self.vectorNameField
    
    
    def loadVectorAttributes(self):
        """
        """
        registry = QgsProviderRegistry.instance()
        provider = registry.provider('ogr', self.vectorFile)
        
        if not provider.isValid():
            return
        
        attributes = []
        
        for field in provider.fields():
            attributes.append(field.name())
        
        self.comboBoxVectorIDField.clear()
        self.comboBoxVectorIDField.addItems(sorted(attributes))
        self.comboBoxVectorIDField.setEnabled(True)
        
        self.comboBoxVectorNameField.clear()
        self.comboBoxVectorNameField.addItems(sorted(attributes))
        self.comboBoxVectorNameField.setEnabled(True)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def accept(self):
        """
        """
        self.vectorIDField = unicode(self.comboBoxVectorIDField.currentText())
        self.vectorNameField = unicode(self.comboBoxVectorNameField.currentText())
        
        if self.vectorIDField and self.vectorNameField:
            QtGui.QDialog.accept(self)
        else:
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
            return
    
    
    def reject(self):
        """
        """
        QtGui.QDialog.reject(self)
    