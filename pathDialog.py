from PySide.QtCore import *
from PySide.QtGui import *
import os
import glob

import pathDialog_Ui


class PathDialog(QDialog, pathDialog_Ui.Ui_pathDialog):
    def __init__(self, mainDialog, combobox, parent=None):
        super(PathDialog, self).__init__(parent)
        self.setupUi(self)
        self.mainDialog = mainDialog

        # warning styles
        self.warningStyle = "border: 2px solid #c63c26"
        self.normalStyle = ""

        # split the paths and add it to the list widget
        paths = combobox.currentText().split(";")
        for each in paths:
            if each != "":
                path = QListWidgetItem(each)
                path.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                self.listWidget.addItem(path)

        self.pushButton_AddPath.clicked.connect(self.addPath)
        self.pushButton_DelPath.clicked.connect(lambda: self.listWidget.takeItem(self.listWidget.currentRow()))

    def validatePath(self):
        if self.listWidget.count() == 0:
            return True
        for row in range(0, self.listWidget.count()):
            path = self.listWidget.item(row).text()
            if os.path.exists(path):
                self.listWidget.setStyleSheet(self.normalStyle)
                return True
            else:
                self.listWidget.setStyleSheet(self.warningStyle)
                return False

    def addPath(self):
        path = QFileDialog.getExistingDirectory(self, "Please choose a folder for the OpenFlight path...",
                                                dir=self.mainDialog.other_dir, options=QFileDialog.ShowDirsOnly)
        # validate the path
        if len(path) > 0:
            # assign the path to the variable for later use
            self.mainDialog.other_dir = path

            # add item to the list widget
            item = QListWidgetItem(path)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.listWidget.addItem(item)

    def accept(self):
        if not self.validatePath():
            return
        pathStr = ""
        paths = []
        for row in range(0, self.listWidget.count()):
            pathStr += self.listWidget.item(row).text() + ";"
            paths.append(self.listWidget.item(row).text())

        # reset the openfilght path combo box in the mainDialog
        self.mainDialog.comboBox_OpenFlightPath.clear()
        self.mainDialog.comboBox_OpenFlightPath.addItem(pathStr)

        # fill in the texture input path automatically
        self.mainDialog.comboBox_TextureInput.clear()
        self.mainDialog.comboBox_TextureInput.addItem(pathStr)

        # list all the .flt files in the input file checkbox
        for path in paths:
            inputFiles = glob.glob(path + "/*.flt")
            self.mainDialog.fltCount = len(inputFiles)
            for each in inputFiles:
                self.mainDialog.comboBox_InputFile.addItem(os.path.split(each)[1])

        # look for the config files in that folder and it's parent folder if it exists
        self.mainDialog.comboBox_ConfigFile.clear()
        for path in paths:
            configFiles = glob.glob(path + "/*config*.xml")
            configFiles += glob.glob(os.path.dirname(file[0]) + "/*config*.xml")
            self.mainDialog.comboBox_ConfigFile.addItems(configFiles)

        # create a folder using the first path
        if self.listWidget.count() > 0:
            self.mainDialog.comboBox_WorkPath.clear()
            self.mainDialog.comboBox_WorkPath.addItem(0, paths[0] + "/VisionExport")
            self.mainDialog.lineEdit_TextureOutput.setText("textures")
            self.mainDialog.lineEdit_MeshOutput.setText("meshes")
            self.mainDialog.lineEdit_LayerOutput.setText("DefaultScene")
            self.mainDialog.lineEdit_PhysicsOutput.setText("physicsData")

        QDialog.accept(self)
