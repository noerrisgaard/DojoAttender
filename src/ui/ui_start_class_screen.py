# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_class_screen.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StartNewClassWindow(object):
    def setupUi(self, StartNewClassWindow):
        StartNewClassWindow.setObjectName("StartNewClassWindow")
        StartNewClassWindow.setWindowModality(QtCore.Qt.NonModal)
        StartNewClassWindow.resize(800, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StartNewClassWindow.sizePolicy().hasHeightForWidth())
        StartNewClassWindow.setSizePolicy(sizePolicy)
        StartNewClassWindow.setMinimumSize(QtCore.QSize(0, 0))
        StartNewClassWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        StartNewClassWindow.setTabletTracking(False)
        StartNewClassWindow.setStyleSheet("QWidget#centralwidget{background-image: url(:/images/Backgrnd_nowibk.png)}\n"
"QListView#listWidget{background: transparent;}")
        self.centralwidget = QtWidgets.QWidget(StartNewClassWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setGeometry(QtCore.QRect(260, 10, 330, 450))
        self.video_label.setFrameShape(QtWidgets.QFrame.Box)
        self.video_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_label.setObjectName("video_label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(600, 4, 191, 411))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(228, 70, 37))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(228, 70, 37))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.groupBox.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setGeometry(QtCore.QRect(10, 21, 171, 381))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listWidget.setFont(font)
        self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setAutoScroll(False)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.setObjectName("listWidget")
        self.return_btn = QtWidgets.QPushButton(self.centralwidget)
        self.return_btn.setGeometry(QtCore.QRect(600, 420, 191, 41))
        self.return_btn.setObjectName("return_btn")
        StartNewClassWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(StartNewClassWindow)
        QtCore.QMetaObject.connectSlotsByName(StartNewClassWindow)

    def retranslateUi(self, StartNewClassWindow):
        _translate = QtCore.QCoreApplication.translate
        StartNewClassWindow.setWindowTitle(_translate("StartNewClassWindow", "Start new class"))
        self.video_label.setText(_translate("StartNewClassWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Loading videobuffer...</span></p></body></html>"))
        self.groupBox.setTitle(_translate("StartNewClassWindow", "Class"))
        self.return_btn.setText(_translate("StartNewClassWindow", "End registration"))

from .assets import resources
