# -*- coding: utf-8 -*-
"""第一个程序"""
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
import sys

class myDialog(QDialog):
    """docstring for myDialog"""
    def __init__(self, arg=None):
        super(myDialog, self).__init__(arg)
        self.setWindowTitle("first window")
        #设置对话框为黑色背景
        color = QColor(0, 0, 0)
        self.setStyleSheet('QDialog{background-color:%s}'%color.name())
        self.resize(400,300);

app = QApplication(sys.argv)
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()
