# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_mem_screen.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_EditMemWindow(object):
    def setupUi(self, EditMemWindow):
        EditMemWindow.setObjectName("EditMemWindow")
        EditMemWindow.resize(800, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditMemWindow.sizePolicy().hasHeightForWidth())
        EditMemWindow.setSizePolicy(sizePolicy)
        EditMemWindow.setMinimumSize(QtCore.QSize(0, 0))
        EditMemWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        EditMemWindow.setTabletTracking(False)
        EditMemWindow.setStyleSheet("QWidget#centralwidget{background-image: url(:/images/Backgrnd_nowibk.png)}")
        self.centralwidget = QtWidgets.QWidget(EditMemWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(250, 10, 541, 401))
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.verticalHeader().setVisible(False)
        self.return_btn = QtWidgets.QPushButton(self.centralwidget)
        self.return_btn.setGeometry(QtCore.QRect(380, 420, 271, 41))
        self.return_btn.setObjectName("return_btn")
        EditMemWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(EditMemWindow)
        QtCore.QMetaObject.connectSlotsByName(EditMemWindow)

    def retranslateUi(self, EditMemWindow):
        _translate = QtCore.QCoreApplication.translate
        EditMemWindow.setWindowTitle(_translate("EditMemWindow", "Edit Members"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("EditMemWindow", "Image"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("EditMemWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("EditMemWindow", "Action"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("EditMemWindow", "Id"))
        self.return_btn.setText(_translate("EditMemWindow", "Return to main"))

from .assets import resources
