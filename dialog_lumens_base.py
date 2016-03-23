#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, csv
from PyQt4 import QtGui

from dialog_lumens_viewer import DialogLumensViewer


class DialogLumensBase:
    """Base class for LUMENS dialogs.
    """
    
    def __init__(self, parent):
        self.main = parent
    
    
    def populateAddedDataComboBox(self, addedData, comboBox):
        """Method for populating a combobox with data previously added to the project.
        """
        if len(addedData):
            comboBox.clear()
            
            # Sort by key name
            for key in sorted(addedData):
                comboBox.addItem(key, addedData[key])
            
            comboBox.setEnabled(True)
    
    
    def handlerDialogHelp(self, dialogName):
        """Slot method for opening the dialog html help document.
        
        Args:
            dialogName (str): the name of the dialog.
        """
        helpDialogFile = None
        
        if dialogName == 'PUR':
            helpDialogFile = 'helpDialogPURFile'
        elif dialogName == 'QUES':
            helpDialogFile = 'helpDialogQUESFile'
        elif dialogName == 'TA':
            helpDialogFile = 'helpDialogTAFile'
        elif dialogName == 'SCIENDO':
            helpDialogFile = 'helpDialogSCIENDOFile'
        else:
            helpDialogFile = 'helpLUMENSFile'
        
        filePath = os.path.join(self.main.appSettings['appDir'], self.main.appSettings['folderHelp'], self.main.appSettings[helpDialogFile])
        
        if os.path.exists(filePath):
            dialog = DialogLumensViewer(self, 'LUMENS Help - {0}'.format(dialogName), 'html', filePath)
            dialog.exec_()
        else:
            QtGui.QMessageBox.critical(self, 'LUMENS Help Not Found', "Unable to open '{0}'.".format(filePath))
    
    
    def validForm(self, formName=False):
        """Method for validating the form values.
        
        Args:
            formName (str): the name of the form to validate. If false then use the class name.
        """
        settingsIndex = type(self).__name__
        
        if formName:
            settingsIndex = formName
            logging.getLogger(type(self).__name__).info('form validate: %s', formName)
            logging.getLogger(type(self).__name__).info('form values: %s', self.main.appSettings[formName])
        else:
            logging.getLogger(type(self).__name__).info('form validate: %s', type(self).__name__)
            logging.getLogger(type(self).__name__).info('form values: %s', self.main.appSettings[type(self).__name__])
        
        valid = True
        
        for key, val in self.main.appSettings[settingsIndex].iteritems():
            if val == 0: # for values set specific to 0
                continue
            elif not val:
                valid = False
        
        if not valid:
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
        
        return valid
    
    
    def outputsMessageBox(self, algName, outputs, successMessage, errorMessage):
        """Display a messagebox based on the processing result.
        
        Args:
            algName (str): the name of the executed algorithm.
            outputs (dict): the output of the executed algorithm.
            successMessage (str): the success message to be display in a message box.
            errorMessage (str): the error message to be display in a message box.
        """
        success = False
        outputMessage = 'Algorithm "{0}"'.format(algName)
        
        # R script key
        statusOutputKey = 'statusoutput'
        
        # Modeler script key
        if algName.lower().startswith('modeler:'):
            statusOutputKey = 'statusoutput_ALG1'
        
        if outputs and statusOutputKey in outputs:
          if os.path.exists(outputs[statusOutputKey]):
              with open(outputs[statusOutputKey], 'rb') as f:
                  hasHeader = csv.Sniffer().has_header(f.read(1024))
                  f.seek(0)
                  reader = csv.reader(f)
                  if hasHeader: # Skip the header
                      next(reader)
                  for row in reader: # Just read the first row
                      verb = 'failed'
                      statusCode = row[0]
                      statusMessage = row[1]
                      if int(statusCode) == 1:
                          success = True
                          verb = 'succeeded'
                      outputMessage = '{0} {1} with status message: {2}'.format(outputMessage, verb, statusMessage)
                      break
          else:
              outputMessage = '{0} failed.'.format(outputMessage)
        
        if success:
            logging.getLogger(type(self).__name__).info(outputMessage)
            QtGui.QMessageBox.information(self, 'Success', successMessage)
            return True
        
        logging.getLogger(type(self).__name__).error(outputMessage)
        QtGui.QMessageBox.critical(self, 'Error', errorMessage)
        return False
    
