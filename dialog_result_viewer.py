#!/usr/bin/env python
#-*- coding:utf-8 -*-

import csv
from PyQt4 import QtCore, QtGui


class DialogResultViewer(QtGui.QDialog):
    """
    """
    
    
    def __init__(self, contentTitle, contentType, contentSource, parent):
        super(DialogResultViewer, self).__init__(parent)
        self.main = parent
        
        self.dialogTitle = 'Result Viewer - ' + contentTitle
        
        self.setupUi(self)
        
        self.loadContent(contentType, contentSource)
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout(parent)
        
        self.tableModel = QtGui.QStandardItemModel(parent)
        
        self.tableContent = QtGui.QTableView()
        self.tableContent.setModel(self.tableModel)
        self.tableContent.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableContent.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableContent.verticalHeader().setVisible(False)
        self.tableContent.horizontalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
        
        self.dialogLayout.addWidget(self.tableContent)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 600)
        self.resize(parent.sizeHint())
    
    
    def loadContent(self, contentType, contentSource):
        """
        """
        if contentType == 'csv':
            with open(contentSource, 'rb') as csvFile:
                for row in csv.reader(csvFile):
                    items = [QtGui.QStandardItem(field) for field in row]
                    self.tableContent.model().appendRow(items)
            
            self.tableContent.horizontalHeader().resizeSections()
    