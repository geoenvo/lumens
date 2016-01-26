#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys

from PyQt4 import QtGui, QtCore

##from dialog_lumens_base import DialogLumensBase
##from dialog_lumens_pur import DialogLumensPUR
##from dialog_lumens_pur_referenceclasses import DialogLumensPURReferenceClasses
from dialog_lumens_ta_opportunitycost import DialogLumensTAOpportunityCost
##from dialog_lumens_ta_regionaleconomy import DialogLumensTARegionalEconomy
##from dialog_lumens_sciendo import DialogLumensSCIENDO
##from dialog_lumens_ques import DialogLumensQUES

def main():
    app = QtGui.QApplication(sys.argv)
    
    ##dialog = DialogLumensBase(None)
    ##dialog = DialogLumensPUR(None)
    ##dialog = DialogLumensPURReferenceClasses(None)
    dialog = DialogLumensTAOpportunityCost(None)
    ##dialog = DialogLumensTARegionalEconomy(None)
    ##dialog = DialogLumensSCIENDO(None)
    ##dialog = DialogLumensQUES(None)
    
    dialog.show()
    
    app.exec_()
    app.deleteLater()


#############################################################################


if __name__ == "__main__":
    main()