from PySide.QtCore import *
from PySide.QtGui import *
import os
import glob

import profileDialog_Ui


class ProfileDialog(QDialog, profileDialog_Ui.Ui_profileDialog):
    def __init__(self, mainDialog, type, parent=None):
        super(ProfileDialog, self).__init__(parent)
        self.setupUi(self)
        self.mainDialog = mainDialog
        self.batchFile = None
        self.type = type
        if type == "add":
            # copy the items from the main dialog
            for i in range(0, mainDialog.comboBox_Profile.count()):
                self.comboBox.addItem(mainDialog.comboBox_Profile.itemText(i))
                # select the current profile
            profile = mainDialog.comboBox_Profile.currentText()
            self.comboBox.setCurrentIndex(self.comboBox.findText(profile))
            self.pushButton_LoadBatch.clicked.connect(self.loadBatchFile)

        elif type == "rename":
            self.setWindowTitle("Rename the profile")
            self.label.hide()
            self.comboBox.hide()
            self.pushButton_LoadBatch.hide()
            self.lineEdit.setText(mainDialog.comboBox_Profile.currentText())
            self.lineEdit.selectAll()

        self.lineEdit.setFocus()

    def loadBatchFile(self):
        fileObj = QFileDialog.getOpenFileName(self, "Please choose a batch file...", dir=self.mainDialog.other_dir,
                                              filter="Batch File (*.bat)")
        batchFile = fileObj[0]
        #validate
        if len(batchFile) > 0:
            fileName = os.path.basename(batchFile)
            # create a new profile
            self.comboBox.insertItem(0, fileName)
            self.comboBox.setCurrentIndex(0)
            self.lineEdit.setText(os.path.splitext(fileName)[0])
            self.batchFile = batchFile

    def accept(self):
        # validate the new profile name
        if self.mainDialog.validateName(self.lineEdit):
            dst = self.lineEdit.text()
            # find the original file if there is one
            try:
                if self.type == "add":
                    if self.batchFile:
                        # load from batch file
                        self.mainDialog.comboBox_Profile.insertItem(0, self.lineEdit.text())
                        self.mainDialog.comboBox_Profile.setCurrentIndex(0)
                        command = self.mainDialog.parseBatchFile(self.batchFile, {})[1]
                        self.mainDialog.setArguments(command)
                    else:
                        # copy from an existing profile
                        src = os.path.abspath(glob.glob("Profiles/" + self.comboBox.currentText() + ".ini")[0])
                        profile = open(src, "r")
                        content = profile.read()
                        profile.close()
                        open("Profiles/" + dst + ".ini", "w").write(content)
                elif self.type == "rename":
                    src = os.path.abspath(
                        glob.glob("Profiles/" + self.mainDialog.comboBox_Profile.currentText() + ".ini")[0])
                    os.rename(src, os.path.dirname(src) + "/" + dst + ".ini")
            except IndexError:
                self.mainDialog.writeProfile(dst)
                self.mainDialog.updateProfiles()
                # select the new profile in the main dialog
                index = self.mainDialog.comboBox_Profile.findText(dst)
                self.mainDialog.comboBox_Profile.setCurrentIndex(index)

            if not self.batchFile:
                self.mainDialog.updateProfiles()
                # select the new profile in the main dialog
                index = self.mainDialog.comboBox_Profile.findText(dst)
                self.mainDialog.comboBox_Profile.setCurrentIndex(index)

            QDialog.accept(self)
