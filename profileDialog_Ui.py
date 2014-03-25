# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profileDialog.ui'
#
# Created: Tue Jan 14 12:20:34 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_profileDialog(object):
    def setupUi(self, profileDialog):
        profileDialog.setObjectName("profileDialog")
        profileDialog.resize(260, 146)
        profileDialog.setMinimumSize(QtCore.QSize(260, 136))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Resources/havok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        profileDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(profileDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(profileDialog)
        self.label.setMinimumSize(QtCore.QSize(90, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(profileDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(profileDialog)
        self.label_2.setMinimumSize(QtCore.QSize(90, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(profileDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_LoadBatch = QtGui.QPushButton(profileDialog)
        self.pushButton_LoadBatch.setObjectName("pushButton_LoadBatch")
        self.horizontalLayout_3.addWidget(self.pushButton_LoadBatch)
        self.buttonBox = QtGui.QDialogButtonBox(profileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(profileDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), profileDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), profileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(profileDialog)

    def retranslateUi(self, profileDialog):
        profileDialog.setWindowTitle(QtGui.QApplication.translate("profileDialog", "New profile", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("profileDialog", "Copy from:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("profileDialog", "New profile name:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_LoadBatch.setToolTip(QtGui.QApplication.translate("profileDialog", "Load a batch file", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_LoadBatch.setText(QtGui.QApplication.translate("profileDialog", "Load .bat", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
