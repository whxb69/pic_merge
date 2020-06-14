# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QListView,QListWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon(r'src\concept.png'))
        desktop = QtWidgets.QApplication.desktop()
        self.screenWidth = desktop.width() * 0.6
        self.screenHeight = desktop.height() * 0.6
        MainWindow.resize(self.screenWidth , self.screenHeight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)

        self.plist = QListWidget(self)
        self.plist.setGeometry(20,20,0.45*self.screenWidth,0.95*self.screenHeight)
        self.plist.setViewMode(QListWidget.IconMode)
        self.plist.setMovement(QListWidget.Free)
        self.plist.setSpacing(10)
        self.plist.setAcceptDrops(False)
        self.plist.setDragEnabled(True)

        # self.rlist = QListWidget(self)
        # self.rlist.setGeometry(0.45*self.screenWidth+50,0.15*self.screenHeight,
        #                         0.42*self.screenWidth,0.42*self.screenWidth)
        # self.rlist.setViewMode(QListWidget.IconMode)
        # self.rlist.setMovement(QListWidget.Static)
        # self.rlist.setSpacing(2)
        # self.rlist.setAcceptDrops(True)

        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
