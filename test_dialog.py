#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys

from PyQt4 import QtGui, QtCore

from dialog_lumens_base import DialogLumensBase
from dialog_lumens_pur import DialogLumensPUR

def main():
    app = QtGui.QApplication(sys.argv)
    
    dialog = DialogLumensBase(None)
    dialog = DialogLumensPUR(None)
    dialog.show()
    
    app.exec_()
    app.deleteLater()


#############################################################################


if __name__ == "__main__":
    main()