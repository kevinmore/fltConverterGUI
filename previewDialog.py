from PySide.QtCore import *
from PySide.QtGui import *
import os
import previewDialog_Ui
class PreviewDialog(QDialog, previewDialog_Ui.Ui_resultDialog):

    def __init__(self, args, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self.setupUi(self)

        self.result = ""

        # read path settings args[""]
        converter = args["converter"]
        self.result += converter

        inputFile = args["inputFile"]
        self.result += " /" + inputFile

        openflightPath = args["openflightPath"]
        self.result = self.result + " -openflightPath " + openflightPath

        textureInputPath = args["textureInputPath"]
        self.result = self.result + " -textureInputPath " + textureInputPath

        configFile = args["configFile"]
        self.result = self.result + " -configuration " + configFile

        workPath = args["workPath"]
        self.result = self.result + " -workPath " + workPath

        textureOutputPath = args["textureOutputPath"]  # seems to be predefined by default
        meshOutputPath = args["meshOutputPath"]
        self.result = self.result + " -meshOutputPath " + meshOutputPath

        layerOutputPath = args["layerOutputPath"]
        self.result = self.result + " -layerOutputPath " + layerOutputPath

        physicsOutputPath = args["physicsOutputPath"] # seems to be predefined by default

        # read exporting options args[""]
        b_prefab = args["b_prefab"]
        if b_prefab:
            self.result += " -prefab"

        b_generate_collision_data = args["b_generate_collision_data"]
        if b_generate_collision_data:
            self.result += " -C"

        b_make_pivoting_zones = args["b_make_pivoting_zones"]
        if b_make_pivoting_zones:
            self.result += " -ZP"

        b_export_binary = args["b_export_binary"]
        if b_make_pivoting_zones:
            self.result += " -Binary"

        b_convert_to_dds = args["b_convert_to_dds"]
        if b_convert_to_dds:
            self.result += " -convertToDDS"

        b_flip_existing_dds = args["b_flip_existing_dds"]
        if b_flip_existing_dds:
            self.result += " -flipExistingDDS"

        b_high_quality_dds = args["b_high_quality_dds"]
        if b_high_quality_dds:
            self.result += " -highQualityDDS"

        b_flip_v = args["b_flip_v"]
        if b_flip_v:
            self.result += " -flipv"

        b_center_mesh = args["b_center_mesh"]
        if b_center_mesh:
            self.result += " -centermeshes"

        b_keep_exported = args["b_keep_exported"]
        if b_keep_exported:
            self.result += " -keepExported"

        b_no_main_layer = args["b_no_main_layer"]
        if b_no_main_layer:
            self.result += " -doNotGenerateMainLayer"

        b_audit = args["b_audit"]
        if b_audit:
            self.result += " -audit"

        b_skip_lod = args["b_skip_lod"]
        if b_skip_lod:
            skipLOD = args["skipLOD"]
            self.result += " -skiplod " + skipLOD

        b_terrain_lod = args["b_terrain_lod"]
        if b_terrain_lod:
            terrain_LOD = args["terrain_LOD"]
            self.result += " -terrainlod " + terrain_LOD

        b_enable_log = args["b_enable_log"]
        if b_enable_log:
            logFile = args["logFile"]
            self.result += " -logFile " + logFile

        b_zone_reg = args["b_zone_reg"]
        if b_zone_reg:
            zoneReg = args["zoneReg"]
            self.result += " -defaultZoneRegex " + zoneReg

        # display the result
        self.textBrowser.setText(self.result)


        # implement signals and slots
        self.saveButton.clicked.connect(self.saveAs)
        self.copyButton.clicked.connect(lambda: QClipboard().setText(self.result))
        self.convertButton.clicked.connect(self.converting)  # using a thread is a more elegant way

    def saveAs(self):
        fileObj = QFileDialog.getSaveFileName(self, "Save the file as...", filter="Batch files (*.bat)")
        fileName = fileObj[0]
        if len(fileName) > 0:
            open(fileName, "w").write(self.result)

    def converting(self):
        # disable the run button first
        self.convertButton.setEnabled(False)

        # start a thread to convert the data
        self.convertTheread = ConvertThread(self.result)
        self.convertTheread.start()


class ConvertThread(QThread):
    def __init__(self, result, parent=None):
        super(ConvertThread, self).__init__(parent)
        self.result = result

    def run(self):
        os.system(self.result)
