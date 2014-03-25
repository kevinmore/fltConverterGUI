# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configFileDialog.ui'
#
# Created: Tue Feb 11 12:17:52 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_configFileDialog(object):
    def setupUi(self, configFileDialog):
        configFileDialog.setObjectName("configFileDialog")
        configFileDialog.resize(746, 559)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Resources/havok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        configFileDialog.setWindowIcon(icon)
        self.verticalLayout_3 = QtGui.QVBoxLayout(configFileDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtGui.QSpacerItem(20, 46, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtGui.QTreeWidget(configFileDialog)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropOverwriteMode(False)
        self.treeWidget.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.treeWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeWidget.setAlternatingRowColors(False)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.setExpandsOnDoubleClick(False)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setVisible(True)
        self.verticalLayout.addWidget(self.treeWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_NewConfig = QtGui.QPushButton(configFileDialog)
        self.pushButton_NewConfig.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_NewConfig.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_NewConfig.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Resources/page.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_NewConfig.setIcon(icon1)
        self.pushButton_NewConfig.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_NewConfig.setAutoDefault(False)
        self.pushButton_NewConfig.setObjectName("pushButton_NewConfig")
        self.horizontalLayout.addWidget(self.pushButton_NewConfig)
        self.pushButton_DelConfig = QtGui.QPushButton(configFileDialog)
        self.pushButton_DelConfig.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_DelConfig.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_DelConfig.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Resources/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_DelConfig.setIcon(icon2)
        self.pushButton_DelConfig.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_DelConfig.setAutoDefault(False)
        self.pushButton_DelConfig.setObjectName("pushButton_DelConfig")
        self.horizontalLayout.addWidget(self.pushButton_DelConfig)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_CopyTag = QtGui.QPushButton(configFileDialog)
        self.pushButton_CopyTag.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_CopyTag.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_CopyTag.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Resources/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_CopyTag.setIcon(icon3)
        self.pushButton_CopyTag.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_CopyTag.setAutoDefault(False)
        self.pushButton_CopyTag.setObjectName("pushButton_CopyTag")
        self.horizontalLayout.addWidget(self.pushButton_CopyTag)
        self.line_6 = QtGui.QFrame(configFileDialog)
        self.line_6.setFrameShape(QtGui.QFrame.VLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout.addWidget(self.line_6)
        self.pushButton_AddTag = QtGui.QPushButton(configFileDialog)
        self.pushButton_AddTag.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_AddTag.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_AddTag.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Resources/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_AddTag.setIcon(icon4)
        self.pushButton_AddTag.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_AddTag.setAutoDefault(False)
        self.pushButton_AddTag.setObjectName("pushButton_AddTag")
        self.horizontalLayout.addWidget(self.pushButton_AddTag)
        self.pushButton_DelTag = QtGui.QPushButton(configFileDialog)
        self.pushButton_DelTag.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_DelTag.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_DelTag.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Resources/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_DelTag.setIcon(icon5)
        self.pushButton_DelTag.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_DelTag.setAutoDefault(False)
        self.pushButton_DelTag.setObjectName("pushButton_DelTag")
        self.horizontalLayout.addWidget(self.pushButton_DelTag)
        self.line_2 = QtGui.QFrame(configFileDialog)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.pushButton_UpTag = QtGui.QPushButton(configFileDialog)
        self.pushButton_UpTag.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_UpTag.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_UpTag.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Resources/arrowup.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_UpTag.setIcon(icon6)
        self.pushButton_UpTag.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_UpTag.setAutoDefault(False)
        self.pushButton_UpTag.setObjectName("pushButton_UpTag")
        self.horizontalLayout.addWidget(self.pushButton_UpTag)
        self.pushButton_DownTag = QtGui.QPushButton(configFileDialog)
        self.pushButton_DownTag.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_DownTag.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_DownTag.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Resources/arrowdown.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_DownTag.setIcon(icon7)
        self.pushButton_DownTag.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_DownTag.setAutoDefault(False)
        self.pushButton_DownTag.setObjectName("pushButton_DownTag")
        self.horizontalLayout.addWidget(self.pushButton_DownTag)
        self.line_3 = QtGui.QFrame(configFileDialog)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.pushButton_OutdentTag = QtGui.QPushButton(configFileDialog)
        self.pushButton_OutdentTag.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_OutdentTag.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_OutdentTag.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Resources/arrowleft.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_OutdentTag.setIcon(icon8)
        self.pushButton_OutdentTag.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_OutdentTag.setAutoDefault(False)
        self.pushButton_OutdentTag.setObjectName("pushButton_OutdentTag")
        self.horizontalLayout.addWidget(self.pushButton_OutdentTag)
        self.pushButton_IndentTag = QtGui.QPushButton(configFileDialog)
        self.pushButton_IndentTag.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_IndentTag.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_IndentTag.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/Resources/arrowright.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_IndentTag.setIcon(icon9)
        self.pushButton_IndentTag.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_IndentTag.setAutoDefault(False)
        self.pushButton_IndentTag.setObjectName("pushButton_IndentTag")
        self.horizontalLayout.addWidget(self.pushButton_IndentTag)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_ExpandAll = QtGui.QPushButton(configFileDialog)
        self.pushButton_ExpandAll.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_ExpandAll.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_ExpandAll.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/Resources/mailopened.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_ExpandAll.setIcon(icon10)
        self.pushButton_ExpandAll.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_ExpandAll.setAutoDefault(False)
        self.pushButton_ExpandAll.setObjectName("pushButton_ExpandAll")
        self.horizontalLayout.addWidget(self.pushButton_ExpandAll)
        self.pushButton_CollapseAll = QtGui.QPushButton(configFileDialog)
        self.pushButton_CollapseAll.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_CollapseAll.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_CollapseAll.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/Resources/mailclosed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_CollapseAll.setIcon(icon11)
        self.pushButton_CollapseAll.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_CollapseAll.setAutoDefault(False)
        self.pushButton_CollapseAll.setObjectName("pushButton_CollapseAll")
        self.horizontalLayout.addWidget(self.pushButton_CollapseAll)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget = QtGui.QTableWidget(configFileDialog)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_AddAttribute = QtGui.QPushButton(configFileDialog)
        self.pushButton_AddAttribute.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_AddAttribute.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_AddAttribute.setText("")
        self.pushButton_AddAttribute.setIcon(icon4)
        self.pushButton_AddAttribute.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_AddAttribute.setAutoDefault(False)
        self.pushButton_AddAttribute.setObjectName("pushButton_AddAttribute")
        self.horizontalLayout_2.addWidget(self.pushButton_AddAttribute)
        self.pushButton_DelAttribute = QtGui.QPushButton(configFileDialog)
        self.pushButton_DelAttribute.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_DelAttribute.setMaximumSize(QtCore.QSize(22, 22))
        self.pushButton_DelAttribute.setText("")
        self.pushButton_DelAttribute.setIcon(icon5)
        self.pushButton_DelAttribute.setIconSize(QtCore.QSize(14, 14))
        self.pushButton_DelAttribute.setAutoDefault(False)
        self.pushButton_DelAttribute.setObjectName("pushButton_DelAttribute")
        self.horizontalLayout_2.addWidget(self.pushButton_DelAttribute)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.line = QtGui.QFrame(configFileDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_SaveAs = QtGui.QPushButton(configFileDialog)
        self.pushButton_SaveAs.setAutoDefault(False)
        self.pushButton_SaveAs.setObjectName("pushButton_SaveAs")
        self.horizontalLayout_4.addWidget(self.pushButton_SaveAs)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.pushButton_Ok = QtGui.QPushButton(configFileDialog)
        self.pushButton_Ok.setAutoDefault(False)
        self.pushButton_Ok.setObjectName("pushButton_Ok")
        self.horizontalLayout_4.addWidget(self.pushButton_Ok)
        self.pushButton_Cancel = QtGui.QPushButton(configFileDialog)
        self.pushButton_Cancel.setAutoDefault(False)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout_4.addWidget(self.pushButton_Cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.retranslateUi(configFileDialog)
        QtCore.QObject.connect(self.pushButton_Ok, QtCore.SIGNAL("clicked()"), configFileDialog.accept)
        QtCore.QObject.connect(self.pushButton_Cancel, QtCore.SIGNAL("clicked()"), configFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(configFileDialog)

    def retranslateUi(self, configFileDialog):
        configFileDialog.setWindowTitle(QtGui.QApplication.translate("configFileDialog", "Config File", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_NewConfig.setToolTip(QtGui.QApplication.translate("configFileDialog", "Create a new config file.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_DelConfig.setToolTip(QtGui.QApplication.translate("configFileDialog", "Delete the current config file.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_CopyTag.setToolTip(QtGui.QApplication.translate("configFileDialog", "Copy the selected tag.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_AddTag.setToolTip(QtGui.QApplication.translate("configFileDialog", "Add a new tag.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_DelTag.setToolTip(QtGui.QApplication.translate("configFileDialog", "Delete the selected tag.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_UpTag.setToolTip(QtGui.QApplication.translate("configFileDialog", "Move up the selected tag.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_DownTag.setToolTip(QtGui.QApplication.translate("configFileDialog", "Move down the selected tag.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OutdentTag.setToolTip(QtGui.QApplication.translate("configFileDialog", "Outdent the selected tag.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_IndentTag.setToolTip(QtGui.QApplication.translate("configFileDialog", "Indent the selected tag.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ExpandAll.setToolTip(QtGui.QApplication.translate("configFileDialog", "Expand all.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_CollapseAll.setToolTip(QtGui.QApplication.translate("configFileDialog", "Collapse all.", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("configFileDialog", "Attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("configFileDialog", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_AddAttribute.setToolTip(QtGui.QApplication.translate("configFileDialog", "Add a row.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_DelAttribute.setToolTip(QtGui.QApplication.translate("configFileDialog", "Delete the selected row.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_SaveAs.setText(QtGui.QApplication.translate("configFileDialog", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Ok.setText(QtGui.QApplication.translate("configFileDialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("configFileDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import images_rc