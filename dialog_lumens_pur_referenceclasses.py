#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from PyQt4 import QtCore, QtGui
import resource


class DialogLumensPURReferenceClasses(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, parent):
        super(DialogLumensPURReferenceClasses, self).__init__(parent)
        print 'DEBUG: DialogLumensPURReferenceClasses init'
        
        self.main = parent
        self.dialogTitle = 'LUMENS Edit Reference Classes'
        self.tableRowCount = 0
        self.referenceClasses = {}
        
        self.setupUi(self)
        self.initReferenceClassesTable()
        
        self.buttonAddRow.clicked.connect(self.handlerButtonAddRow)
        self.buttonBox.accepted.connect(self.handlerButtonSave)
        self.buttonBox.rejected.connect(self.handlerButtonCancel)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        
        # 'Setup planning unit' GroupBox
        self.groupBoxEditReferenceClasses = QtGui.QGroupBox('Reference classes')
        self.layoutGroupBoxEditReferenceClasses = QtGui.QVBoxLayout()
        self.groupBoxEditReferenceClasses.setLayout(self.layoutGroupBoxEditReferenceClasses)
        self.dialogLayout.addWidget(self.groupBoxEditReferenceClasses)
        
        self.contentButtonEditReferenceClasses = QtGui.QWidget()
        self.layoutButtonEditReferenceClasses = QtGui.QHBoxLayout()
        self.layoutButtonEditReferenceClasses.setContentsMargins(0, 0, 0, 0)
        self.contentButtonEditReferenceClasses.setLayout(self.layoutButtonEditReferenceClasses)
        self.layoutButtonEditReferenceClasses.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.buttonAddRow = QtGui.QPushButton()
        self.buttonAddRow.setText('Add Reference Class')
        self.buttonAddRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonEditReferenceClasses.addWidget(self.buttonAddRow)
        
        self.layoutContentGroupBoxEditReferenceClasses = QtGui.QVBoxLayout()
        self.layoutContentGroupBoxEditReferenceClasses.setContentsMargins(5, 5, 5, 5)
        self.contentGroupBoxEditReferenceClasses = QtGui.QWidget()
        self.contentGroupBoxEditReferenceClasses.setLayout(self.layoutContentGroupBoxEditReferenceClasses)
        self.scrollEditReferenceClasses = QtGui.QScrollArea()
        self.scrollEditReferenceClasses.setWidgetResizable(True);
        self.scrollEditReferenceClasses.setWidget(self.contentGroupBoxEditReferenceClasses)
        self.layoutEditReferenceClassesInfo = QtGui.QVBoxLayout()
        self.labelEditReferenceClassesInfo = QtGui.QLabel()
        self.labelEditReferenceClassesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutEditReferenceClassesInfo.addWidget(self.labelEditReferenceClassesInfo)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save|QtGui.QDialogButtonBox.Cancel)
        
        self.layoutGroupBoxEditReferenceClasses.addLayout(self.layoutEditReferenceClassesInfo)
        self.layoutGroupBoxEditReferenceClasses.addWidget(self.contentButtonEditReferenceClasses)
        self.layoutGroupBoxEditReferenceClasses.addWidget(self.scrollEditReferenceClasses)
        self.dialogLayout.addWidget(self.buttonBox)
        
        self.layoutTableReferenceClasses = QtGui.QVBoxLayout()
        self.layoutTableReferenceClasses.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentGroupBoxEditReferenceClasses.addLayout(self.layoutTableReferenceClasses)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 300)
        self.resize(parent.sizeHint())
    
    
    def getReferenceClasses(self):
        """
        """
        return self.referenceClasses
    
    
    def initReferenceClassesTable(self):
        """
        """
        referenceClasses = self.main.referenceClasses
        
        if referenceClasses:
            for key, val in referenceClasses.iteritems():
                self.addRow(key, val)
    
    
    def showEvent(self, event):
        """Called when the widget is shown
        """
        super(DialogLumensPURReferenceClasses, self).showEvent(event)
    
    
    def addRow(self, id=None, title=None):
        """Add a planning unit table row
        """
        self.tableRowCount = self.tableRowCount + 1
        
        layoutRow = QtGui.QHBoxLayout()
        
        buttonDeleteReferenceClass = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionClear.png')
        buttonDeleteReferenceClass.setIcon(icon)
        buttonDeleteReferenceClass.setObjectName('buttonDeleteReferenceClass_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(buttonDeleteReferenceClass)
        
        lineEditReferenceClassID = QtGui.QLineEdit()
        lineEditReferenceClassID.setObjectName('lineEditReferenceClassID_{0}'.format(str(self.tableRowCount)))
        lineEditReferenceClassID.setText(str(self.tableRowCount))
        layoutRow.addWidget(lineEditReferenceClassID)
        
        lineEditReferenceClassTitle = QtGui.QLineEdit()
        lineEditReferenceClassTitle.setText('title')
        lineEditReferenceClassTitle.setObjectName('lineEditReferenceClassTitle_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(lineEditReferenceClassTitle)
        
        if id:
            lineEditReferenceClassID.setText(str(id))
        if title:
            lineEditReferenceClassTitle.setText(str(title))
        
        self.layoutTableReferenceClasses.addLayout(layoutRow)
        
        buttonDeleteReferenceClass.clicked.connect(self.handlerDeleteReferenceClass)
    
    
    def clearLayout(self, layout):
        """Clear a layout and all its child widgets
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtGui.QWidgetItem):
                item.widget().deleteLater() # use this to properly delete the widget
            elif isinstance(item, QtGui.QSpacerItem):
                pass
            else:
                self.clearLayout(item.layout())
            
            layout.removeItem(item)
    
    
    def handlerButtonAddRow(self):
        """
        """
        self.addRow()
    
    
    def handlerDeleteReferenceClass(self):
        """
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        layoutRow = self.layoutTableReferenceClasses.itemAt(int(tableRow) - 1).layout()
        self.clearLayout(layoutRow)
    
    
    def handlerButtonSave(self):
        """
        """
        self.referenceClasses = {}
        
        for tableRow in range(1, self.tableRowCount + 1):
            lineEditReferenceClassID = self.findChild(QtGui.QLineEdit, 'lineEditReferenceClassID_' + str(tableRow))
            
            if not lineEditReferenceClassID: # Row has been deleted
                print 'DEBUG: skipping a deleted row.'
                continue
            
            lineEditReferenceClassTitle = self.findChild(QtGui.QLineEdit, 'lineEditReferenceClassTitle_' + str(tableRow))
            
            try:
                referenceClassID = int(unicode(lineEditReferenceClassID.text()))
                
                if self.referenceClasses.has_key(referenceClassID):
                    print 'DEBUG ERROR found duplicate reference class ID.'
                    return
                else:
                    self.referenceClasses[referenceClassID] = unicode(lineEditReferenceClassTitle.text())
            except ValueError as verr:
                print 'DEBUG: ERROR reference class ID must be an integer!'
                return
        
        if self.referenceClasses:
            self.close()
            self.setResult(QtGui.QDialog.Accepted)
        else:
            print 'DEBUG: ERROR no reference classes set.'
    
    
    def handlerButtonCancel(self):
        """
        """
        self.close()
        self.setResult(QtGui.QDialog.Rejected)
    