# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'convertDialog.ui'
#
# Created: Wed Jan 08 14:54:27 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_convertDialog(object):
    def setupUi(self, convertDialog):
        convertDialog.setObjectName("convertDialog")
        convertDialog.resize(471, 357)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Resources/havok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        convertDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(convertDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(convertDialog)
        self.label.setStyleSheet("background-color: transparent; color: #ffaa00; font-size: 23pt;  qproperty-alignment: AlignCenter;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textBrowser = QtGui.QTextBrowser(convertDialog)
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.progressBar = QtGui.QProgressBar(convertDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(convertDialog)
        QtCore.QMetaObject.connectSlotsByName(convertDialog)

    def retranslateUi(self, convertDialog):
        convertDialog.setWindowTitle(QtGui.QApplication.translate("convertDialog", "Converting...", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("convertDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Initializing...</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
