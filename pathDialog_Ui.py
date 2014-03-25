# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pathDialog.ui'
#
# Created: Thu Jan 16 15:50:14 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_pathDialog(object):
    def setupUi(self, pathDialog):
        pathDialog.setObjectName("pathDialog")
        pathDialog.resize(500, 260)
        pathDialog.setMinimumSize(QtCore.QSize(500, 260))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Resources/havok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pathDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(pathDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 46, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_AddPath = QtGui.QPushButton(pathDialog)
        self.pushButton_AddPath.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_AddPath.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_AddPath.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Resources/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_AddPath.setIcon(icon1)
        self.pushButton_AddPath.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_AddPath.setObjectName("pushButton_AddPath")
        self.horizontalLayout.addWidget(self.pushButton_AddPath)
        self.pushButton_DelPath = QtGui.QPushButton(pathDialog)
        self.pushButton_DelPath.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_DelPath.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_DelPath.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Resources/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_DelPath.setIcon(icon2)
        self.pushButton_DelPath.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_DelPath.setObjectName("pushButton_DelPath")
        self.horizontalLayout.addWidget(self.pushButton_DelPath)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtGui.QListWidget(pathDialog)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.buttonBox = QtGui.QDialogButtonBox(pathDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(pathDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), pathDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), pathDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(pathDialog)

    def retranslateUi(self, pathDialog):
        pathDialog.setWindowTitle(QtGui.QApplication.translate("pathDialog", "Path Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_AddPath.setToolTip(QtGui.QApplication.translate("pathDialog", "Add a new path.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_DelPath.setToolTip(QtGui.QApplication.translate("pathDialog", "Delete the selected path.", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
