# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reg_new_mem_screen.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RegNewMemWindow(object):
    def setupUi(self, RegNewMemWindow):
        RegNewMemWindow.setObjectName("RegNewMemWindow")
        RegNewMemWindow.resize(800, 480)
        RegNewMemWindow.setStyleSheet("QWidget#centralwidget{background-image: url(:/images/Backgrnd.png)}")
        self.centralwidget = QtWidgets.QWidget(RegNewMemWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setGeometry(QtCore.QRect(260, 10, 330, 450))
        self.video_label.setFrameShape(QtWidgets.QFrame.Box)
        self.video_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)
        self.video_label.setObjectName("video_label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(600, 210, 191, 111))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 46, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 46, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.groupBox.setPalette(palette)
        self.groupBox.setObjectName("groupBox")
        self.regmem_btn = QtWidgets.QPushButton(self.groupBox)
        self.regmem_btn.setGeometry(QtCore.QRect(10, 60, 171, 41))
        self.regmem_btn.setObjectName("regmem_btn")
        self.mem_name_input = QtWidgets.QLineEdit(self.groupBox)
        self.mem_name_input.setGeometry(QtCore.QRect(10, 20, 171, 31))
        self.mem_name_input.setObjectName("mem_name_input")
        self.return_btn = QtWidgets.QPushButton(self.centralwidget)
        self.return_btn.setGeometry(QtCore.QRect(600, 420, 191, 41))
        self.return_btn.setObjectName("return_btn")
        RegNewMemWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RegNewMemWindow)
        QtCore.QMetaObject.connectSlotsByName(RegNewMemWindow)

    def retranslateUi(self, RegNewMemWindow):
        _translate = QtCore.QCoreApplication.translate
        RegNewMemWindow.setWindowTitle(_translate("RegNewMemWindow", "Register members"))
        self.video_label.setText(_translate("RegNewMemWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Loading videobuffer...</span></p></body></html>"))
        self.groupBox.setTitle(_translate("RegNewMemWindow", "Member registration"))
        self.regmem_btn.setText(_translate("RegNewMemWindow", "Register member"))
        self.mem_name_input.setPlaceholderText(_translate("RegNewMemWindow", "Member name"))
        self.return_btn.setText(_translate("RegNewMemWindow", "Return to main"))

from .assets import resources
