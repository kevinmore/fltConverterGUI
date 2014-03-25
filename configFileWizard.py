from PySide.QtCore import *
from PySide.QtGui import *

import configFileWizard_Ui


class ConfigFileWizard(QWizard, configFileWizard_Ui.Ui_Wizard):
    def __init__(self, configFileDialog, parent=None):
        super(ConfigFileWizard, self).__init__(parent)

        self.configFileDialog = configFileDialog
        self.args = {}
        self.setupUi(self)
        self.wizardPage0.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/Resources/campus.png"))

        self.pushButton_ConfigFile.clicked.connect(self.chooseConfigFile)
        self.comboBox_ConfigFilePath.addItem(configFileDialog.mainDialog.comboBox_WorkPath.currentText())

    def getArguments(self):
        if self.radioButton_Customized.isChecked():
            TerrainCmpType = self.comboBox_TerrainCmpType.currentText()
            TerrainExp = self.lineEdit_TerrainExp.text()
            TerrainPageIn = str(self.spinBox_TerrainPageIn.value())
            TerrainPageOut = str(self.spinBox__TerrainPageOut.value())
            TerrainForceLoad = str(self.spinBox__TerrainForceLoad.value())
            MeshCmpType = self.comboBox_MeshCmpType.currentText()
            MeshExp = self.lineEdit_MeshExp.text()
            PhysicsPageIn = str(self.spinBox_PhysicsPageIn.value())
            PhysicsPageOut = str(self.spinBox_PhysicsPageOut.value())
            PhysicsForceLoad = str(self.spinBox_PhysicsForceLoad.value())
            TreeCmpType = self.comboBox_TreeCmpType.currentText()
            TreeExp = self.lineEdit_TreeExp.text()
            TreeReplacement = self.lineEdit_TreeReplacement.text()
            ConfigFilePath = self.comboBox_ConfigFilePath.currentText()
            ConfigFileName = self.lineEdit_ConfigFile.text()

            args = {"Terrain Comparison Type": TerrainCmpType, "Terrain Expression": TerrainExp,
                    "Terrain Page In Radius": TerrainPageIn, "Terrain Page Out Radius": TerrainPageOut,
                    "Terrain Force Loaded Radius": TerrainForceLoad, "Mesh Comparison Type": MeshCmpType,
                    "Mesh Expression": MeshExp, "Physics Page In Radius": PhysicsPageIn,
                    "Physics Page Out Radius": PhysicsPageOut,"Physics Force Loaded Radius": PhysicsForceLoad,
                    "SpeedTree Comparison Type": TreeCmpType, "SpeedTree Expression": TreeExp,
                    "SpeedTree Replacement": TreeReplacement, "ConfigFile": ConfigFilePath + "/" + ConfigFileName}

        else:
            args = {"Terrain Comparison Type": "REGEX", "Terrain Expression": ".*flight.*",
                    "Terrain Page In Radius": "2000", "Terrain Page Out Radius": "4000",
                    "Terrain Force Loaded Radius": "1000", "Mesh Comparison Type": "REGEX",
                    "Mesh Expression": "(?!(.*flight.*)).*", "Physics Page In Radius": "100000",
                    "Physics Page Out Radius": "200000", "Physics Force Loaded Radius": "1",
                    "ConfigFile": self.comboBox_ConfigFilePath.currentText() + "/" + self.lineEdit_ConfigFile.text()}

        return args

    def generateXML(self):
        xml = ("<root><Rules><FileRule name=\"flightFile\" comparisonType=\""+self.args["Terrain Comparison Type"]+"\" comparisonValue=\""+self.args["Terrain Expression"]+"\" />" +
                "<FileRule name=\"notFlightFile\" comparisonType=\""+self.args["Mesh Comparison Type"]+"\" comparisonValue=\""+self.args["Mesh Expression"]+"\" /></Rules>" +
                "<MeshOperation><SkipLOD rule=\"flightFile\"/></MeshOperation><Physics><MeshShapes><Mesh fileRule=\"notFlightFile\"/>" +
                "</MeshShapes><PhysicsZone rule=\"flightFile\" pageInRadius=\""+self.args["Physics Page In Radius"]+"\" pageOutRadius=\""+self.args["Physics Page Out Radius"]+"\" forceLoadedRadius=\""+self.args["Physics Force Loaded Radius"]+"\"/></Physics>" +
                "<Zones><RootZone rule=\"flightFile\" pageInRadius=\""+self.args["Terrain Page In Radius"]+"\" pageOutRadius=\""+self.args["Terrain Page Out Radius"]+"\" forceLoadedRadius=\""+self.args["Terrain Force Loaded Radius"]+"\"/></Zones></root>")

        return xml

    def chooseConfigFile(self):
        fileObj = QFileDialog.getSaveFileName(self, "New config file...", dir=self.comboBox_ConfigFilePath.currentText(), filter="Xml files (*.xml)")
        configFile = fileObj[0]
        # validate the file
        if len(configFile) > 0:
            self.comboBox_ConfigFilePath.insertItem(0, configFile)
            self.comboBox_ConfigFilePath.setCurrentIndex(0)

    def nextId(self, *args, **kwargs):
        cur_id = self.currentId()
        if cur_id == 0:
            if self.radioButton_Typical.isChecked():
                return 6
            else:
                return 1
        elif cur_id < 6:
            cur_id += 1
            return cur_id
        else:
            if self.radioButton_Typical.isChecked():
                self.textBrowser.setText("Setup Type: Typical")
            else:
                self.textBrowser.setText("Setup Type: Customized")

            self.args = self.getArguments()
            for (k, v) in self.args.items():
                self.textBrowser.append("\n" + k + ":    " + v)

            return -1

    def accept(self, *args, **kwargs):
        try:
            fileName = self.comboBox_ConfigFilePath.currentText()
            xml = self.generateXML()
            open(fileName, "w").write(xml)
            self.configFileDialog.readXML(fileName)
            QWizard.accept(self)
        except Exception, err:
                QMessageBox.warning(self, "Can't create config file", str(err)+"\nPlease make sure the file can be saved here.(Folder does not exist? Read only?)")



