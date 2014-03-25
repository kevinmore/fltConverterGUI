from PySide.QtCore import *
from PySide.QtGui import *

import glob
import sys
import os
import re

from pathDialog import *
from convertDialog import *
from profileDialog import *
from configFileDialog import *

import mainDialog_Ui

class MainGui(QDialog, mainDialog_Ui.Ui_mainDialog):
    def __init__(self, parent=None):
        super(MainGui, self).__init__(parent)
        self.setupUi(self)
        self.toggleShow()

        self.setAcceptDrops(True)
        self.fltCount = 1
        # create default path strings
        self.con_dir = "."
        self.other_dir = "."
        # widget border styles
        self.warningStyle = "border: 1px solid #c63c26"
        self.hintStyle = "border: 2px solid #7fb80e"
        self.normalStyle = ""

        # search the profiles
        self.updateProfiles()

        # read settings, NOTE: most values are None when first time running the program
        # a try..except.. block is necessary
        self.settings = None
        try:
            self.readSettings()
        except Exception:
            pass

        # profile combo box
        self.comboBox_Profile.currentIndexChanged.connect(lambda: self.readProfile(self.comboBox_Profile.currentText()))
        self.pushButton_renameProfile.clicked.connect(self.renameProfile)
        self.pushButton_AddProfile.clicked.connect(self.addProfile)
        self.pushButton_DelProfile.clicked.connect(self.deleteProfile)

        self.comboBox_InputFile.currentIndexChanged.connect(self.filterInput)

        self.pushButton_Converter.clicked.connect(self.chooseConverter)
        self.pushButton_InputFile.clicked.connect(self.chooseInputFile)
        self.pushButton__OpenFlightPath.clicked.connect(self.chooseOpenFlightPath)
        self.pushButton_TextureInput.clicked.connect(self.chooseTextureInputPath)
        self.pushButton_ConfigFile.clicked.connect(self.chooseConfigFile)
        self.pushButton_ReadConfigFile.clicked.connect(self.readConfigFile)
        self.pushButton_WorkPath.clicked.connect(self.chooseWorkPath)

        self.checkBox_ConvertToDDS.toggled.connect(self.ddsLogic)
        self.pushButton_LogFile.clicked.connect(self.chooseLogFile)

        self.resetButton.clicked.connect(self.resetGUI)
        self.showButton.clicked.connect(self.toggleShow)
        self.saveButton.clicked.connect(self.saveAs)
        self.convertButton.clicked.connect(self.converting)

    # simple method to convert string to bool
    def toBool(self, str):
        return str.lower() == "true"

    def readSettings(self):
        self.mainSettings = QSettings("Havok", "OpenFlight Converter")
        self.lastProfile = self.mainSettings.value("lastProfile")
        index = self.comboBox_Profile.findText(self.lastProfile)
        # if the last profile exists, in other words, the user hasn't deleted it
        if index > -1:
            self.comboBox_Profile.setCurrentIndex(index)
            self.readProfile(self.lastProfile)

    def writeSettings(self):
        self.mainSettings = QSettings("Havok", "OpenFlight Converter")
        profile = self.comboBox_Profile.currentText()
        if profile == "":
            profile = "default"
        self.mainSettings.setValue("lastProfile", profile)
        self.writeProfile(profile)

    def updateProfiles(self):
        self.comboBox_Profile.clear()
        profiles = glob.glob("Profiles/*.ini")
        if not profiles:
            self.comboBox_Profile.addItem("default")

        for each in profiles:
            self.comboBox_Profile.addItem(os.path.splitext(os.path.basename(os.path.abspath(each)))[0])

    def renameProfile(self):
        # open a profile dialog
        if self.comboBox_Profile.currentText() != "default":
            self.profileDialog = ProfileDialog(self, "rename")
            self.profileDialog.exec_()

    def addProfile(self):
        # write the current profile
        self.writeProfile(self.comboBox_Profile.currentText())
        # open a profile dialog
        self.profileDialog = ProfileDialog(self, "add")
        self.profileDialog.exec_()

    def deleteProfile(self):
        profileName = self.comboBox_Profile.currentText()
        try:
            profile = os.path.abspath(glob.glob("Profiles/" + profileName + ".ini")[0])
            # it's not allowed to remove the default profile
            if profileName != "default":
                os.remove(profile)
        except IndexError:
            pass
        self.updateProfiles()

    def readProfile(self, profile):
        potentialFiles = glob.glob("Profiles/" + profile + ".ini")
        if not potentialFiles:
            return
        self.resetGUI()
        self.settings = QSettings("Profiles" + "/" + profile + ".ini", QSettings.IniFormat)
        # most values are None for a empty profile
        try:

            self.con_dir = self.settings.value("con_dir")
            self.other_dir = self.settings.value("dir")
            self.fltCount = self.settings.value("fltCount")
            if self.fltCount is None or self.fltCount == 0:
                self.fltCount = 1

            # search the converters
            if self.con_dir is None:
                self.con_dir = "."
            converters = glob.glob(self.con_dir + "/vFltConverter*.exe")
            for each in converters:
                self.comboBox_Converter.addItem(os.path.abspath(each))

            if len(self.settings.value("openflightPath")) > 0:
                self.comboBox_OpenFlightPath.addItem(self.settings.value("openflightPath"))
                self.fltCount = 1
                # list all the .flt files in the input file checkbox
                paths = self.settings.value("openflightPath").split(";")
                for path in paths:
                    inputFiles = glob.glob(path + "/*.flt")
                    self.fltCount += len(inputFiles)
                    for each in inputFiles:
                        self.comboBox_InputFile.addItem(os.path.basename(each))

            if len(self.settings.value("inputFile")) > 0:
                self.comboBox_InputFile.setCurrentIndex(
                    self.comboBox_InputFile.findText(self.settings.value("inputFile")))

            if len(self.settings.value("textureInputPath")) > 0:
                self.comboBox_TextureInput.addItem(self.settings.value("textureInputPath"))
            if len(self.settings.value("configFile")) > 0:
                self.comboBox_ConfigFile.addItem(self.settings.value("configFile"))
            if len(self.settings.value("workPath")) > 0:
                self.comboBox_WorkPath.addItem(self.settings.value("workPath"))
            if len(self.settings.value("textureOutputPath")) > 0:
                self.lineEdit_TextureOutput.setText(self.settings.value("textureOutputPath"))
            if len(self.settings.value("meshOutputPath")) > 0:
                self.lineEdit_MeshOutput.setText(self.settings.value("meshOutputPath"))
            if len(self.settings.value("layerOutputPath")) > 0:
                self.lineEdit_LayerOutput.setText(self.settings.value("layerOutputPath"))
            if len(self.settings.value("physicsOutputPath")) > 0:
                self.lineEdit_PhysicsOutput.setText(self.settings.value("physicsOutputPath"))
            if len(self.settings.value("logFile")) > 0:
                self.comboBox_LogFile.addItem(self.settings.value("logFile"))

            self.checkBox_Prefab.setChecked(self.toBool(self.settings.value("b_prefab")))
            self.checkBox_GenerateCollisionData.setChecked(
                self.toBool(self.settings.value("b_generate_collision_data")))
            self.checkBox_MakePivotingZones.setChecked(self.toBool(self.settings.value("b_make_pivoting_zones")))
            self.radioButton_Binary.setChecked(self.toBool(self.settings.value("b_export_binary")))
            self.radioButton_vForge.setChecked(self.toBool(self.settings.value("b_export_vForge")))
            self.checkBox_ConvertToDDS.setChecked(self.toBool(self.settings.value("b_convert_to_dds")))
            self.checkBox_FlipExistingDDS.setChecked(self.toBool(self.settings.value("b_flip_existing_dds")))
            self.checkBox_HighQualityDDS.setChecked(self.toBool(self.settings.value("b_high_quality_dds")))
            self.checkBox_FlipV.setChecked(self.toBool(self.settings.value("b_flip_v")))
            self.checkBox_CenterMeshes.setChecked(self.toBool(self.settings.value("b_center_mesh")))
            self.checkBox_KeepExported.setChecked(self.toBool(self.settings.value("b_keep_exported")))
            self.checkBox_NoMainLayer.setChecked(self.toBool(self.settings.value("b_no_main_layer")))
            self.checkBox_Audit.setChecked(self.toBool(self.settings.value("b_audit")))
            self.checkBox_SkipLOD.setChecked(self.toBool(self.settings.value("b_skip_lod")))
            self.lineEdit_SkipLOD.setText(self.settings.value("skipLOD"))
            self.checkBox_TerrainLOD.setChecked(self.toBool(self.settings.value("b_terrain_lod")))
            self.lineEdit_TerrainLOD.setText(self.settings.value("terrain_LOD"))
            self.checkBox_EnableLog.setChecked(self.toBool(self.settings.value("b_enable_log")))
            self.checkBox_ZoneReg.setChecked(self.toBool(self.settings.value("b_zone_reg")))
            self.lineEdit_ZoneReg.setText(self.settings.value("zoneReg"))
            self.checkBox_AdditionalCommands.setChecked(self.toBool(self.settings.value("b_addi_cmd")))
            self.lineEdit_AdditionalCommands.setText(self.settings.value("addi_cmd"))
        except Exception:
            pass
        self.filterInput()

    def writeProfile(self, profile):
        self.settings = QSettings("Profiles" + "/" + profile + ".ini", QSettings.IniFormat)
        # get the last used directory
        self.settings.setValue("dir", self.other_dir)
        self.settings.setValue("con_dir", self.con_dir)

        self.settings.setValue("fltCount", self.fltCount)

        args = self.getArguments()
        self.settings.setValue("inputFile", args["inputFile"])
        self.settings.setValue("openflightPath", args["openflightPath"])
        self.settings.setValue("textureInputPath", args["textureInputPath"])
        self.settings.setValue("configFile", args["configFile"])
        self.settings.setValue("workPath", args["workPath"])
        self.settings.setValue("textureOutputPath", args["textureOutputPath"])
        self.settings.setValue("meshOutputPath", args["meshOutputPath"])
        self.settings.setValue("layerOutputPath", args["layerOutputPath"])
        self.settings.setValue("physicsOutputPath", args["physicsOutputPath"])
        self.settings.setValue("b_prefab", args["b_prefab"])
        self.settings.setValue("b_generate_collision_data", args["b_generate_collision_data"])
        self.settings.setValue("b_make_pivoting_zones", args["b_make_pivoting_zones"])
        self.settings.setValue("b_export_binary", args["b_export_binary"])
        self.settings.setValue("b_export_vForge", args["b_export_vForge"])
        self.settings.setValue("b_convert_to_dds", args["b_convert_to_dds"])
        self.settings.setValue("b_flip_existing_dds", args["b_flip_existing_dds"])
        self.settings.setValue("b_high_quality_dds", args["b_high_quality_dds"])
        self.settings.setValue("b_flip_v", args["b_flip_v"])
        self.settings.setValue("b_center_mesh", args["b_center_mesh"])
        self.settings.setValue("b_keep_exported", args["b_keep_exported"])
        self.settings.setValue("b_no_main_layer", args["b_no_main_layer"])
        self.settings.setValue("b_audit", args["b_audit"])
        self.settings.setValue("b_skip_lod", args["b_skip_lod"])
        self.settings.setValue("skipLOD", args["skipLOD"])
        self.settings.setValue("b_terrain_lod", args["b_terrain_lod"])
        self.settings.setValue("terrain_LOD", args["terrain_LOD"])
        self.settings.setValue("b_enable_log", args["b_enable_log"])
        self.settings.setValue("logFile", args["logFile"])
        self.settings.setValue("b_zone_reg", args["b_zone_reg"])
        self.settings.setValue("zoneReg", args["zoneReg"])
        self.settings.setValue("b_addi_cmd", args["b_addi_cmd"])
        self.settings.setValue("addi_cmd", args["addi_cmd"])

    def filterInput(self):
        inputFile = self.comboBox_InputFile.currentText()
        if not inputFile:
            return
        # using regex here
        pattern = re.compile(r"flight\d*_\d*\.flt")
        match = pattern.match(inputFile)
        # enable the default zone regex
        if match or inputFile.find("master") > -1:
            self.checkBox_ZoneReg.setChecked(False)
            self.lineEdit_ZoneReg.clear()
        else:
            self.checkBox_ZoneReg.setChecked(True)
            self.lineEdit_ZoneReg.setText(".*?")


    def chooseConverter(self):
        fileObj = QFileDialog.getOpenFileName(self, "Please choose a converter...", dir=self.con_dir,
                                              filter="Converter (vFltConverter*.exe)")
        converter = fileObj[0]
        # check if the converter file is valid
        if len(converter) > 0:
            self.comboBox_Converter.insertItem(0, converter)
            self.comboBox_Converter.setCurrentIndex(0)
            self.con_dir = os.path.split(converter)[0]

    def chooseInputFile(self):
        fileObj = QFileDialog.getOpenFileName(self, "Please choose an input file...", dir=self.other_dir,
                                              filter="Input File (*.flt)")
        fileName = fileObj[0]
        #validate
        if len(fileName) > 0:
            file = os.path.split(fileName)
            self.other_dir = file[0]
            # fill in the path comboboxes automatically
            self.comboBox_InputFile.clear()
            self.comboBox_InputFile.insertItem(0, file[1])
            self.comboBox_InputFile.setCurrentIndex(0)
            self.comboBox_OpenFlightPath.insertItem(0, file[0])
            self.comboBox_OpenFlightPath.setCurrentIndex(0)
            self.comboBox_TextureInput.insertItem(0, file[0])
            self.comboBox_TextureInput.setCurrentIndex(0)

            # list all the .flt files in the input file checkbox
            inputFiles = glob.glob(file[0] + "/*.flt")
            self.fltCount = len(inputFiles)
            for each in inputFiles:
                if os.path.basename(each) != file[1]:
                    self.comboBox_InputFile.addItem(os.path.basename(each))

            # look for the config files in that folder and it's parent folder if it exists
            configFiles = glob.glob(file[0] + "/*config*.xml")
            configFiles += glob.glob(os.path.dirname(file[0]) + "/*config*.xml")
            self.comboBox_ConfigFile.clear()
            self.comboBox_ConfigFile.addItems(configFiles)

            self.comboBox_WorkPath.insertItem(0, file[0] + "/VisionExport")
            self.comboBox_WorkPath.setCurrentIndex(0)
            self.lineEdit_TextureOutput.setText("textures")
            self.lineEdit_MeshOutput.setText("meshes")
            self.lineEdit_LayerOutput.setText("DefaultScene")
            self.lineEdit_PhysicsOutput.setText("physicsData")

    def chooseOpenFlightPath(self):
        # open a path dialog
        self.pathDialog = PathDialog(self, self.comboBox_OpenFlightPath)
        self.pathDialog.exec_()


    def chooseTextureInputPath(self):
        # open a path dialog
        self.pathDialog = PathDialog(self, self.comboBox_TextureInput)
        self.pathDialog.exec_()

    def chooseConfigFile(self):
        fileObj = QFileDialog.getOpenFileName(self, "Please choose a config file..", dir=self.other_dir,
                                              filter="Config files (*.xml)")
        configFile = fileObj[0]
        # validate the file
        if len(configFile) > 0:
            self.comboBox_ConfigFile.insertItem(0, configFile)
            self.comboBox_ConfigFile.setCurrentIndex(0)

    def readConfigFile(self):
        # open a converting dialog
        self.configFileDialog = ConfigFileDialog(self, self.comboBox_ConfigFile.currentText())
        self.configFileDialog.exec_()

    def chooseWorkPath(self):
        path = QFileDialog.getExistingDirectory(self, "Please choose a folder for the work path...", dir=self.comboBox_WorkPath.currentText(),
                                                options=QFileDialog.ShowDirsOnly)
        # validate the path
        if len(path) > 0:
            self.comboBox_WorkPath.insertItem(0, path)
            self.comboBox_WorkPath.setCurrentIndex(0)
            # fill the mesh, texture, layer, physics output path automatically
            self.lineEdit_TextureOutput.setText("textures")
            self.lineEdit_MeshOutput.setText("meshes")
            self.lineEdit_LayerOutput.setText("DefaultScene")
            self.lineEdit_PhysicsOutput.setText("physicsData")

            # update the path to the variable
            self.other_dir = path

    def chooseLogFile(self):
        fileObj = QFileDialog.getSaveFileName(self, "Save a log file..", dir=self.other_dir, filter="Log files (*.txt)")
        logFile = fileObj[0]
        # validate the file
        if len(logFile) > 0:
            self.comboBox_LogFile.insertItem(0, logFile)
            self.comboBox_LogFile.setCurrentIndex(0)

    def ddsLogic(self):
        if not self.checkBox_ConvertToDDS.isChecked():
            self.checkBox_FlipExistingDDS.setChecked(False)
            self.checkBox_HighQualityDDS.setChecked(False)

    def saveAs(self):
        if self.validate():
            self.writeSettings()
            fileObj = QFileDialog.getSaveFileName(self, "Save the file as...", filter="Batch files (*.bat)")
            fileName = fileObj[0]
            if len(fileName) > 0:
                open(fileName, "w").write(self.prepareCommand())

    def converting(self):
        if self.validate():
            self.writeSettings()
            # disable the run button first
            self.convertButton.setEnabled(False)
            # open a converting dialog
            self.convertDialog = ConvertDialog(self)
            self.convertDialog.exec_()

    def validate(self):

        # validate files
        f0 = self.validateFile(self.comboBox_Converter)
        f1 = self.validateFile(self.comboBox_Converter)
        f2 = self.validateInputFile(self.comboBox_InputFile)
        f3 = self.validateFile(self.comboBox_ConfigFile)

        # validate paths
        f4 = self.validatePath(self.comboBox_OpenFlightPath)
        f5 = self.validatePath(self.comboBox_TextureInput)

        # validate the folder names
        f6 = self.validateName(self.lineEdit_LayerOutput)
        f7 = self.validateName(self.lineEdit_MeshOutput)
        f8 = self.validateName(self.lineEdit_PhysicsOutput)
        f9 = self.validateName(self.lineEdit_TextureOutput)

        return f0 and f1 and f2 and f3 and f4 and f5 and f6 and f7 and f8 and f9

    def validateFile(self, widget):
        if os.path.isfile(widget.currentText()):
            widget.setStyleSheet(self.normalStyle)
            return True
        else:
            widget.setStyleSheet(self.warningStyle)
            return False

    def validateInputFile(self, widget):
        paths = self.comboBox_OpenFlightPath.currentText().split(";")
        for each in paths:
            if os.path.isfile(each + "/" + widget.currentText()):
                widget.setStyleSheet(self.normalStyle)
                return True
            else:
                widget.setStyleSheet(self.warningStyle)
                return False

    def validatePath(self, widget):
        paths = widget.currentText().split(";")
        for each in paths:
            if os.path.exists(each):
                widget.setStyleSheet(self.normalStyle)
                return True
            else:
                widget.setStyleSheet(self.warningStyle)
                return False

    def validateName(self, widget):
        if widget.text() == "":
            widget.setStyleSheet(self.warningStyle)
            return False

        invalidChars = {"/", "\\", ":", "*", "?", "\"", "<", ">", "|"}
        for each in widget.text():
            if each in invalidChars:
                widget.setStyleSheet(self.warningStyle)
                return False
            else:
                widget.setStyleSheet(self.normalStyle)
                return True

    def getArguments(self):
        # read path settings
        converter = self.comboBox_Converter.currentText()
        self.converterName = os.path.split(converter)[1]

        openflightPath = self.comboBox_OpenFlightPath.currentText()
        textureInputPath = self.comboBox_TextureInput.currentText()
        configFile = self.comboBox_ConfigFile.currentText()
        workPath = self.comboBox_WorkPath.currentText()
        textureOutputPath = self.lineEdit_TextureOutput.text()
        meshOutputPath = self.lineEdit_MeshOutput.text()
        layerOutputPath = self.lineEdit_LayerOutput.text()
        physicsOutputPath = self.lineEdit_PhysicsOutput.text()

        # read exporting options
        b_prefab = self.checkBox_Prefab.isChecked()
        b_generate_collision_data = self.checkBox_GenerateCollisionData.isChecked()
        b_make_pivoting_zones = self.checkBox_MakePivotingZones.isChecked()
        b_export_binary = self.radioButton_Binary.isChecked()
        b_export_vForge = self.radioButton_vForge.isChecked()
        b_convert_to_dds = self.checkBox_ConvertToDDS.isChecked()
        b_flip_existing_dds = self.checkBox_FlipExistingDDS.isChecked()
        b_high_quality_dds = self.checkBox_HighQualityDDS.isChecked()
        b_flip_v = self.checkBox_FlipV.isChecked()
        b_center_mesh = self.checkBox_CenterMeshes.isChecked()
        b_keep_exported = self.checkBox_KeepExported.isChecked()
        b_no_main_layer = self.checkBox_NoMainLayer.isChecked()
        b_audit = self.checkBox_Audit.isChecked()
        inputFile = self.comboBox_InputFile.currentText()

        b_skip_lod = self.checkBox_SkipLOD.isChecked()
        skipLOD = ""
        if b_skip_lod:
            skipLOD = self.lineEdit_SkipLOD.text()

        b_terrain_lod = self.checkBox_TerrainLOD.isChecked()
        terrain_LOD = ""
        if b_terrain_lod:
            terrain_LOD = self.lineEdit_TerrainLOD.text()

        b_enable_log = self.checkBox_EnableLog.isChecked()
        logFile = ""
        if b_enable_log:
            logFile = self.comboBox_LogFile.currentText()

        b_zone_reg = self.checkBox_ZoneReg.isChecked()
        zoneReg = ""
        if b_zone_reg:
            zoneReg = self.lineEdit_ZoneReg.text()

        b_addi_cmd = self.checkBox_AdditionalCommands.isChecked()
        addi_cmd = []
        if b_addi_cmd:
            addi_cmd = self.lineEdit_AdditionalCommands.text().split(";")


        args = {"converter": converter, "openflightPath": openflightPath, "textureInputPath": textureInputPath,
                "configFile": configFile, "workPath": workPath, "textureOutputPath": textureOutputPath,
                "meshOutputPath": meshOutputPath, "layerOutputPath": layerOutputPath,
                "physicsOutputPath": physicsOutputPath,
                "b_prefab": b_prefab, "b_generate_collision_data": b_generate_collision_data,
                "b_make_pivoting_zones": b_make_pivoting_zones,
                "b_export_binary": b_export_binary, "b_export_vForge": b_export_vForge,
                "b_convert_to_dds": b_convert_to_dds,
                "b_flip_existing_dds": b_flip_existing_dds, "b_high_quality_dds": b_high_quality_dds,
                "b_flip_v": b_flip_v,
                "b_center_mesh": b_center_mesh, "b_keep_exported": b_keep_exported, "b_no_main_layer": b_no_main_layer,
                "b_audit": b_audit, "inputFile": inputFile,
                "b_skip_lod": b_skip_lod, "skipLOD": skipLOD, "b_terrain_lod": b_terrain_lod,
                "terrain_LOD": terrain_LOD,
                "b_enable_log": b_enable_log, "logFile": logFile, "b_zone_reg": b_zone_reg, "zoneReg": zoneReg,
                "b_addi_cmd":b_addi_cmd, "addi_cmd": addi_cmd}

        return args

    def setArguments(self, command):
        if len(command) == 0:
            QMessageBox.warning(self, "Can't parse the file", "Please make sure the batch file contains the converter command line.")
            self.comboBox_Profile.removeItem(self.comboBox_Profile.currentIndex())
            return
        self.resetGUI()
        elements = command.rstrip("\n").split(" ")  # a bit weired here, the command string still has an empty line after doing this
        # polish the list, make sure there is no element in the wrong format
        if elements[len(elements) - 1] == "":
            elements.remove(elements[len(elements) - 1])
        elements[len(elements) - 1] = elements[len(elements) - 1].rstrip("\n")

        # add the file extension if there is none
        if elements[0].find(".exe") == -1:
            elements[0] += ".exe"
        self.comboBox_Converter.addItem(elements[0])
        self.con_dir = os.path.dirname(elements[0])

        if elements[1].find(".flt") == -1:
            elements[0] += ".flt"
        self.comboBox_InputFile.addItem(elements[1].strip("/"))

        for index, each in enumerate(elements):
            if each == "-workPath":
                self.comboBox_WorkPath.addItem(elements[index + 1])
            elif each == "-openflightPath":
                self.comboBox_OpenFlightPath.addItem(elements[index + 1])
                # list all the .flt files in the input file checkbox
                inputFiles = glob.glob(elements[index + 1] + "/*.flt")
                self.fltCount = len(inputFiles)
                for each in inputFiles:
                    if os.path.basename(each) != elements[1].strip("/"):
                        self.comboBox_InputFile.addItem(os.path.basename(each))
            elif each == "-layerOutputPath":
                self.lineEdit_LayerOutput.setText(elements[index + 1])
            elif each == "-textureInputPath":
                self.comboBox_TextureInput.addItem(elements[index + 1])
            elif each == "-meshOutputPath":
                self.lineEdit_MeshOutput.setText(elements[index + 1])
            elif each == "-physicsOutputPath":
                self.lineEdit_PhysicsOutput.setText(elements[index + 1])
            elif each == "-textureOutputPath":
                self.lineEdit_TextureOutput.setText(elements[index + 1])
            elif each == "-configuration":
                if elements[index + 1].find(".xml") == -1:
                    elements[index + 1] += ".xml"
                self.comboBox_ConfigFile.addItem(elements[index + 1])
            elif each == "-prefab":
                self.checkBox_Prefab.setChecked(True)
            elif each == "-C":
                self.checkBox_GenerateCollisionData.setChecked(True)
            elif each == "-ZP":
                self.checkBox_MakePivotingZones.setChecked(True)
            elif each == "-Binary":
                self.radioButton_Binary.setChecked(True)
            elif each == "-convertToDDS":
                self.checkBox_ConvertToDDS.setChecked(True)
            elif each == "-flipExistingDDS":
                self.checkBox_ConvertToDDS.setChecked(True)
                self.checkBox_FlipExistingDDS.setChecked(True)
            elif each == "-highQualityDDS":
                self.checkBox_ConvertToDDS.setChecked(True)
                self.checkBox_Prefab.setChecked(True)
            elif each == "-flipv":
                self.checkBox_FlipV.setChecked(True)
            elif each == "-centermeshes":
                self.checkBox_CenterMeshes.setChecked(True)
            elif each == "-keepExported":
                self.checkBox_KeepExported.setChecked(True)
            elif each == "-doNotGenerateMainLayer":
                self.checkBox_NoMainLayer.setChecked(True)
            elif each == "-audit":
                self.checkBox_Audit.setChecked(True)
            elif each == "-skiplod":
                self.checkBox_SkipLOD.setChecked(True)
                self.lineEdit_SkipLOD.setText(elements[index + 1])
            elif each == "-terrainlod":
                self.checkBox_TerrainLOD.setChecked(True)
                self.lineEdit_TerrainLOD.setText(elements[index + 1])
            elif each == "-logFile":
                self.checkBox_EnableLog.setChecked(True)
                self.comboBox_LogFile.addItem(elements[index + 1])
            elif each == "-defaultZoneRegex":
                self.checkBox_ZoneReg.setChecked(True)
                self.lineEdit_ZoneReg.setText(elements[index + 1])

        # make sure all the paths are filled in
        if self.lineEdit_TextureOutput.text() == "":
            self.lineEdit_TextureOutput.setText("textures")
        if self.lineEdit_PhysicsOutput.text() == "":
            self.lineEdit_PhysicsOutput.setText("physicsData")
        if self.lineEdit_LayerOutput.text() == "":
            self.lineEdit_LayerOutput.setText("DefaultScene")
        if self.lineEdit_MeshOutput.text() == "":
            self.lineEdit_MeshOutput.setText("meshes")


    def prepareCommand(self):
        result = ""
        args = self.getArguments()
        # read path settings args[""]
        converter = args["converter"]
        result += converter

        inputFile = args["inputFile"]
        result += " /" + inputFile

        openflightPath = args["openflightPath"]
        result = result + " -openflightPath " + openflightPath

        textureInputPath = args["textureInputPath"]
        result = result + " -textureInputPath " + textureInputPath

        configFile = args["configFile"]
        result = result + " -configuration " + configFile

        workPath = args["workPath"]
        result = result + " -workPath " + workPath

        textureOutputPath = args["textureOutputPath"]  # seems to be predefined by default
        result = result + " -textureOutputPath " + textureOutputPath

        meshOutputPath = args["meshOutputPath"]
        result = result + " -meshOutputPath " + meshOutputPath

        layerOutputPath = args["layerOutputPath"]
        result = result + " -layerOutputPath " + layerOutputPath

        physicsOutputPath = args["physicsOutputPath"] # seems to be predefined by default
        result = result + " -physicsOutputPath " + physicsOutputPath

        # read exporting options args[""]
        b_prefab = args["b_prefab"]
        if b_prefab:
            result += " -prefab"

        b_generate_collision_data = args["b_generate_collision_data"]
        if b_generate_collision_data:
            result += " -C"

        b_make_pivoting_zones = args["b_make_pivoting_zones"]
        if b_make_pivoting_zones:
            result += " -ZP"

        b_export_binary = args["b_export_binary"]
        if b_export_binary:
            result += " -Binary"

        b_convert_to_dds = args["b_convert_to_dds"]
        if b_convert_to_dds:
            result += " -convertToDDS"

        b_flip_existing_dds = args["b_flip_existing_dds"]
        if b_flip_existing_dds:
            result += " -flipExistingDDS"

        b_high_quality_dds = args["b_high_quality_dds"]
        if b_high_quality_dds:
            result += " -highQualityDDS"

        b_flip_v = args["b_flip_v"]
        if b_flip_v:
            result += " -flipv"

        b_center_mesh = args["b_center_mesh"]
        if b_center_mesh:
            result += " -centermeshes"

        b_keep_exported = args["b_keep_exported"]
        if b_keep_exported:
            result += " -keepExported"

        b_no_main_layer = args["b_no_main_layer"]
        if b_no_main_layer:
            result += " -doNotGenerateMainLayer"

        b_audit = args["b_audit"]
        if b_audit:
            result += " -audit"

        b_skip_lod = args["b_skip_lod"]
        if b_skip_lod:
            skipLOD = args["skipLOD"]
            result += " -skiplod " + skipLOD

        b_terrain_lod = args["b_terrain_lod"]
        if b_terrain_lod:
            terrain_LOD = args["terrain_LOD"]
            result += " -terrainlod " + terrain_LOD

        b_enable_log = args["b_enable_log"]
        if b_enable_log:
            logFile = args["logFile"]
            result += " -logFile " + logFile

        b_zone_reg = args["b_zone_reg"]
        if b_zone_reg:
            zoneReg = args["zoneReg"]
            result += " -defaultZoneRegex " + zoneReg
        b_addi_cmd = args["b_addi_cmd"]

        if b_addi_cmd:
            addi_cmd = args["addi_cmd"]
            for each in addi_cmd:
                result += " " + each

        return result

    # move the widget to the center of CURRENT SCREEN (in case of dual screens)
    def moveToScreenCenter(self, widget):
        desktop = QApplication.desktop()
        screenRct = desktop.availableGeometry(desktop.screenNumber(QCursor.pos()))
        desk_x = screenRct.width()
        desk_y = screenRct.height()
        x = widget.width()
        y = widget.height()
        widget.move(desk_x / 2 - x / 2 + screenRct.left(), desk_y / 2 - y / 2 + screenRct.top())

    def resetGUI(self):
        self.comboBox_Converter.clear()
        self.comboBox_Converter.setStyleSheet(self.normalStyle)
        self.comboBox_InputFile.clear()
        self.comboBox_InputFile.setStyleSheet(self.normalStyle)
        self.comboBox_OpenFlightPath.clear()
        self.comboBox_OpenFlightPath.setStyleSheet(self.normalStyle)
        self.comboBox_TextureInput.clear()
        self.comboBox_TextureInput.setStyleSheet(self.normalStyle)
        self.comboBox_ConfigFile.clear()
        self.comboBox_ConfigFile.setStyleSheet(self.normalStyle)
        self.comboBox_WorkPath.clear()
        self.comboBox_WorkPath.setStyleSheet(self.normalStyle)
        self.lineEdit_TextureOutput.clear()
        self.lineEdit_TextureOutput.setStyleSheet(self.normalStyle)
        self.lineEdit_MeshOutput.clear()
        self.lineEdit_MeshOutput.setStyleSheet(self.normalStyle)
        self.lineEdit_LayerOutput.clear()
        self.lineEdit_LayerOutput.setStyleSheet(self.normalStyle)
        self.lineEdit_PhysicsOutput.clear()
        self.lineEdit_PhysicsOutput.setStyleSheet(self.normalStyle)

        self.checkBox_Prefab.setChecked(False)
        self.checkBox_GenerateCollisionData.setChecked(False)
        self.checkBox_MakePivotingZones.setChecked(False)
        self.radioButton_Binary.setChecked(False)
        self.radioButton_vForge.setChecked(True)
        self.checkBox_ConvertToDDS.setChecked(True)
        self.checkBox_FlipExistingDDS.setChecked(False)
        self.checkBox_HighQualityDDS.setChecked(False)
        self.checkBox_FlipV.setChecked(False)
        self.checkBox_CenterMeshes.setChecked(False)
        self.checkBox_KeepExported.setChecked(False)
        self.checkBox_NoMainLayer.setChecked(False)
        self.checkBox_Audit.setChecked(False)
        self.checkBox_SkipLOD.setChecked(False)
        self.lineEdit_SkipLOD.clear()
        self.checkBox_TerrainLOD.setChecked(False)
        self.lineEdit_TerrainLOD.clear()
        self.checkBox_EnableLog.setChecked(False)
        self.comboBox_LogFile.clear()
        self.checkBox_ZoneReg.setChecked(False)
        self.lineEdit_ZoneReg.clear()
        self.checkBox_AdditionalCommands.setChecked(False)
        self.lineEdit_AdditionalCommands.clear()

    def toggleShow(self):
        if self.showButton.text() == "Show Less":
            self.showButton.setText("Show More")
            self.showButton.setToolTip("Show more exporting options")

            # hide some fields
            self.comboBox_OpenFlightPath.hide()
            self.label_3.hide()
            self.pushButton__OpenFlightPath.hide()

            self.label_8.hide()
            self.comboBox_TextureInput.hide()
            self.pushButton_TextureInput.hide()

            self.label_19.hide()
            self.lineEdit_LayerOutput.hide()

            self.label_20.hide()
            self.lineEdit_PhysicsOutput.hide()

            self.label_18.hide()
            self.lineEdit_MeshOutput.hide()

            self.label_17.hide()
            self.lineEdit_TextureOutput.hide()

            self.groupBox_ExportingOptions.hide()

            self.groupBox_InputSettings.adjustSize()
            self.groupBox_OutputSettings.adjustSize()
            self.adjustSize()
            self.resize(520, self.height())
            self.moveToScreenCenter(self)

        else:
            self.showButton.setText("Show Less")
            self.showButton.setToolTip("Show less exporting options")

            # show some fields
            self.comboBox_OpenFlightPath.show()
            self.label_3.show()
            self.pushButton__OpenFlightPath.show()

            self.label_8.show()
            self.comboBox_TextureInput.show()
            self.pushButton_TextureInput.show()

            self.label_19.show()
            self.lineEdit_LayerOutput.show()

            self.label_20.show()
            self.lineEdit_PhysicsOutput.show()

            self.label_18.show()
            self.lineEdit_MeshOutput.show()

            self.label_17.show()
            self.lineEdit_TextureOutput.show()

            self.groupBox_ExportingOptions.show()
            self.adjustSize()
            self.resize(520, self.height())
            self.moveToScreenCenter(self)

    def parseBatchFile(self, batchFile, vars):
        filePath = os.path.dirname(batchFile)
        command = ""
        # read batch file line by line
        for line in open(batchFile, "r"):
            elements = line.split(" ")
            for index, each in enumerate(elements):
                if each.find("CALL") == 0:
                    dummyFile = elements[index + 1].rstrip("\n")
                    dots = dummyFile.count("../")
                    newPath = filePath
                    for x in range(0, dots):
                        newPath = os.path.dirname(newPath)
                    realFile = newPath + "/" + dummyFile.strip("../")
                    if os.path.isfile(realFile):
                        # read additional batch files and merge the dictionaries
                        vars = dict(vars, **self.parseBatchFile(realFile, vars)[0])

                elif each.find("set") == 0:
                    assignment = elements[index + 1].rstrip("\n").split("=")
                    dots = assignment[1].count("../")
                    newPath = filePath
                    # the relative folder is based on the work path
                    for x in range(0, dots - 1):
                        newPath = os.path.dirname(newPath)
                    if dots > 0:
                        assignment[1] = newPath + "/" + assignment[1].strip("../")
                    if assignment[1].find("./") > -1:
                        assignment[1] = newPath + "/" + assignment[1].strip("./")
                    if assignment[1].find(".\\") > -1:
                        assignment[1] = newPath + "/" + assignment[1].strip(".\\")

                    vars[assignment[0]] = assignment[1]

                # locate the converter command line
                elif line.find("-workPath") > -1 and line.find("-openflightPath") > -1:
                    if each.find("%") > -1:
                        key = "%"
                        begin = 0
                        positions = []
                        while True:
                            pos = each.find(key, begin)
                            if pos == -1:
                                break
                            else:
                                positions.append(pos)
                            begin = pos + 1
                            # replace the symbol using the value in the dictionary
                        symbol = each[positions[0] + 1:positions[1]]
                        # if the key is not in the dictionary yet, we do it later in the recursive reading
                        try:
                            each = each.replace("%" + symbol + "%", vars[symbol])
                        except KeyError:
                            # remove the unresolved symbols if there are no more files to read
                            each = each.replace("%" + symbol + "%", "")

                    command += each + " "

        return vars, command

    # override the close event to write the current values into the config file
    def closeEvent(self, e):
        self.writeSettings()
        e.accept()

    # drag a file in to the app
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            dragFile = event.mimeData().urls()[0].toLocalFile()
            fileName = os.path.splitext(os.path.basename(dragFile))[0]
            fileExtension = os.path.splitext(os.path.basename(dragFile))[1]
            if fileExtension == ".flt":
                self.comboBox_InputFile.setStyleSheet(self.hintStyle)
            elif fileExtension == ".xml":
                self.comboBox_ConfigFile.setStyleSheet(self.hintStyle)
            elif fileExtension == ".bat":
                self.comboBox_Profile.setStyleSheet(self.hintStyle)
            elif fileExtension == ".exe" and fileName.find("vFltConverter") > -1:
                self.comboBox_Converter.setStyleSheet(self.hintStyle)
            else:
                event.ignore()
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            dragFile = event.mimeData().urls()[0].toLocalFile()
            fileName = os.path.splitext(os.path.basename(dragFile))[0]
            fileExtension = os.path.splitext(os.path.basename(dragFile))[1]
            if fileExtension == ".flt":
                self.comboBox_InputFile.setStyleSheet(self.normalStyle)
                # fill in the path comboboxes automatically
                file = os.path.split(dragFile)
                self.comboBox_InputFile.clear()
                self.comboBox_InputFile.insertItem(0, file[1])
                self.comboBox_InputFile.setCurrentIndex(0)
                self.comboBox_OpenFlightPath.insertItem(0, file[0])
                self.comboBox_OpenFlightPath.setCurrentIndex(0)
                self.comboBox_TextureInput.insertItem(0, file[0])
                self.comboBox_TextureInput.setCurrentIndex(0)

                # list all the .flt files in the input file checkbox
                inputFiles = glob.glob(file[0] + "/*.flt")
                self.fltCount = len(inputFiles)
                for each in inputFiles:
                    if os.path.basename(each) != file[1]:
                        self.comboBox_InputFile.addItem(os.path.basename(each))

                # look for the config files in that folder and it's parent folder if it exists
                configFiles = glob.glob(file[0] + "/*config*.xml")
                configFiles += glob.glob(os.path.dirname(file[0]) + "/*config*.xml")
                self.comboBox_ConfigFile.clear()
                self.comboBox_ConfigFile.addItems(configFiles)

                self.comboBox_WorkPath.insertItem(0, file[0] + "/VisionExport")
                self.comboBox_WorkPath.setCurrentIndex(0)
                self.lineEdit_TextureOutput.setText("textures")
                self.lineEdit_MeshOutput.setText("meshes")
                self.lineEdit_LayerOutput.setText("DefaultScene")
                self.lineEdit_PhysicsOutput.setText("physicsData")

            elif fileExtension == ".xml":
                self.comboBox_ConfigFile.setStyleSheet(self.normalStyle)
                self.comboBox_ConfigFile.insertItem(0, dragFile)
                self.comboBox_ConfigFile.setCurrentIndex(0)

            elif fileExtension == ".bat":
                self.comboBox_Profile.setStyleSheet(self.normalStyle)
                fileName = os.path.basename(dragFile)
                # create a new profile
                self.comboBox_Profile.insertItem(0, os.path.splitext(fileName)[0])
                self.comboBox_Profile.setCurrentIndex(0)
                command = self.parseBatchFile(dragFile, {})[1]
                self.setArguments(command)

            elif fileExtension == ".exe" and fileName.find("vFltConverter") > -1:
                self.comboBox_Converter.setStyleSheet(self.normalStyle)
                self.comboBox_Converter.insertItem(0, dragFile)
                self.comboBox_Converter.setCurrentIndex(0)

            else:
                event.ignore()
            event.acceptProposedAction()
        else:
            event.ignore()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    style = open("Resources/darkorange.css").read()
    app.setStyleSheet(style)
    dialog = MainGui()
    dialog.show()
    sys.exit(app.exec_())