#!/usr/bin/env python
#-*- coding:utf-8 -*-

import csv
from PyQt4 import QtCore, QtGui, QtWebKit


class DialogResultViewer(QtGui.QDialog):
    """
    """
    def __init__(self, parent, contentTitle, contentType, contentSource, editableTable=False):
        super(DialogResultViewer, self).__init__(parent)
        self.main = parent
        
        self.contentType = contentType
        self.contentSource = contentSource
        self.editableTable = editableTable
        
        self.dialogTitle = 'Result Viewer - ' + contentTitle
        
        self.setupUi(self)
        
        self.loadContent()
    
    
    def setupUi(self, parent):
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 600)
        self.resize(parent.sizeHint())
    
    
    def getTableData(self):
        """Return table data as list of lists
        """
        tableData = []
        
        for tableRow in range(self.tableModel.rowCount()):
            dataRow = []
            
            for tableColumn in range (self.tableModel.columnCount()):
                item = self.tableModel.item(tableRow, tableColumn)
                dataRow.append(item.text())
            
            tableData.append(dataRow)
        
        return tableData
        
    
    def closeEvent(self, event):
        """Called when the widget is closed
        """
        super(DialogResultViewer, self).closeEvent(event)
        
        # Set result code
        self.done(1)
        
        event.accept()
    
    
    def loadContent(self):
        """
        """
        if self.contentType == 'csv':
            self.tableModel = QtGui.QStandardItemModel()
        
            self.tableContent = QtGui.QTableView()
            self.tableContent.setModel(self.tableModel)
            
            if not self.editableTable:
                self.tableContent.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
                self.tableContent.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            
            self.tableContent.verticalHeader().setVisible(False)
            self.tableContent.horizontalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
            
            self.dialogLayout.addWidget(self.tableContent)
            
            with open(self.contentSource, 'rb') as csvFile:
                for row in csv.reader(csvFile):
                    items = [QtGui.QStandardItem(field) for field in row]
                    self.tableContent.model().appendRow(items)
            
            self.tableContent.horizontalHeader().resizeSections()
        elif self.contentType == 'html':
            self.webContent = QtWebKit.QWebView()
            self.dialogLayout.addWidget(self.webContent)
            
            self.webContent.load(QtCore.QUrl.fromLocalFile(self.contentSource))
            self.setMinimumSize(800, 600)
    