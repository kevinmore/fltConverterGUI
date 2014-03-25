from PySide.QtCore import *
from PySide.QtGui import *
import os

from configFileWizard import *

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import configFileDialog_Ui


class ConfigFileDialog(QDialog, configFileDialog_Ui.Ui_configFileDialog):
    def __init__(self, mainDialog, xml, parent=None):
        super(ConfigFileDialog, self).__init__(parent)
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.mainDialog = mainDialog
        self.xml = xml
        self.normalStyle = ""
        self.hintStyle = "border: 1px solid #7fb80e"
        self.readXML(xml)
        self.treeWidget.itemClicked.connect(self.showItemAttributes)
        self.treeWidget.itemDoubleClicked.connect(self.showWidget)
        self.treeWidget.currentItemChanged.connect(self.removeWidget)

        self.tableWidget.cellChanged.connect(self.saveItemAttributes)
        self.tableWidget.currentCellChanged.connect(self.leaveCell)
        self.tableWidget.cellDoubleClicked.connect(self.enterCell)

        self.pushButton_CopyTag.clicked.connect(self.copyTag)
        self.pushButton_AddTag.clicked.connect(self.addTag)
        self.pushButton_DelTag.clicked.connect(self.delTag)
        self.pushButton_UpTag.clicked.connect(self.upTag)
        self.pushButton_DownTag.clicked.connect(self.downTag)
        self.pushButton_OutdentTag.clicked.connect(self.outdentTag)
        self.pushButton_IndentTag.clicked.connect(self.indentTag)
        self.pushButton_AddAttribute.clicked.connect(self.addAttribute)
        self.pushButton_DelAttribute.clicked.connect(self.delAttribute)
        self.pushButton_ExpandAll.clicked.connect(lambda: self.treeWidget.expandAll())
        self.pushButton_CollapseAll.clicked.connect(lambda: self.treeWidget.collapseAll())
        self.pushButton_NewConfig.clicked.connect(self.newConfig)
        self.pushButton_DelConfig.clicked.connect(self.delConfig)

        self.pushButton_SaveAs.clicked.connect(self.saveAs)


    def readXML(self, xml):
        self.tableWidget.setRowCount(0)
        # if the xml in the main dialog is null, create a new one according to the template
        if xml == "":
            self.newConfig()
        else:
            try:
                tree = ET.ElementTree(file=xml)
                self.treeWidget.setHeaderLabel(xml)
                self.treeWidget.clear()
                # add root
                root = tree.getroot()
                rootItem = QTreeWidgetItem(self.treeWidget)
                rootItem.setText(0, root.tag)
                rootItem.setData(0, Qt.UserRole, root.attrib)
                self.searchChildren(root, rootItem)
                self.treeWidget.expandItem(rootItem)
            except Exception, err:
                QMessageBox.warning(self, "Can't parse xml", str(err)+"\nPlease make sure all the values are in quotes and all the tags are closed (including comments).")
                self.treeWidget.setHeaderLabel("")

    def saveAs(self):
        fileObj = QFileDialog.getSaveFileName(self, "Save the config file as...", filter="Xml files (*.xml)")
        fileName = fileObj[0]
        if len(fileName) > 0:
            open(fileName, "w").write(self.generateXML())
            self.xml = fileName
            self.readXML(fileName)

    # create an element tree from the tree widget
    def createTree(self):
        # there is only 1 root in an xml file
        rootItem = self.treeWidget.topLevelItem(0)
        root = ET.Element(rootItem.text(0))

        for index in range(0, rootItem.childCount()):
            self.createNode(root, rootItem.child(index))

        return ET.ElementTree(root)

    # recursive method to create nodes from the tree widget
    def createNode(self, parentNode, curItem):
        curNode = ET.SubElement(parentNode, curItem.text(0).split("(")[0].strip())
        data = curItem.data(0, Qt.UserRole)
        if data is not None:
            # data is a dictionary
            for (k, v) in data.items():
                curNode.set(k, v)
        for index in range(0, curItem.childCount()):
            self.createNode(curNode, curItem.child(index))

    # recursive method to find all the children nodes
    def searchChildren(self, parent, parentItem):
        for child in parent:
            childItem = QTreeWidgetItem(parentItem)
            try:
                childItem.setText(0, child.tag + " ( " + child.attrib["name"] + " )")
            except KeyError:
                childItem.setText(0, child.tag)
            childItem.setData(0, Qt.UserRole, child.attrib)
            self.searchChildren(child, childItem)

    def showItemAttributes(self):
        data = self.treeWidget.currentItem().data(0, Qt.UserRole)
        self.tableWidget.setRowCount(0)
        if data is None:
            return
        # data is a dictionary
        for (k, v) in data.items():
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            keyItem = QTableWidgetItem()
            valueItem = QTableWidgetItem()
            keyItem.setText(k)
            valueItem.setText(v)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, keyItem)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, valueItem)

    def saveItemAttributes(self):
        data = {}
        # save data into a dictionary
        for row in range(0, self.tableWidget.rowCount()):
            key = self.tableWidget.item(row, 0)
            value = self.tableWidget.item(row, 1)
            if key is not None and value is not None:
                data[key.text()] = value.text()
                if key.text() == "name":
                    text = self.treeWidget.currentItem().text(0)
                    ruleType = text.split("(")[0].strip()
                    self.treeWidget.currentItem().setText(0, ruleType + " ( " + data["name"] + " )")

        self.treeWidget.currentItem().setData(0, Qt.UserRole, data)


    def enterCell(self, row, column):
        tagName = self.treeWidget.currentItem().text(0).split("(")[0].strip()
        if column == 0:
            att = self.generateTagAttributes(tagName)
            if len(att) > 0:
                combo_Attribute = QComboBox()
                combo_Attribute.addItems(att)
                index = combo_Attribute.findText(self.tableWidget.currentItem().text())
                if index > -1:
                    combo_Attribute.setCurrentIndex(index)
                self.tableWidget.setCellWidget(row, column, combo_Attribute)

        elif column == 1:
            attribute = self.tableWidget.item(row, 0).text()

            if attribute == "enabled":
                comboBox_Value = QComboBox()
                comboBox_Value.addItems(["true", "false"])
                index = comboBox_Value.findText(self.tableWidget.currentItem().text())
                if index > -1:
                    comboBox_Value.setCurrentIndex(index)
                self.tableWidget.setCellWidget(row, column, comboBox_Value)

            elif attribute == "value":
                if tagName == "LogLevel":
                    comboBox_Value = QComboBox()
                    comboBox_Value.addItems(["Debug", "Info", "Warning", "Error", "Diagnostic", "DeepDiagnostic"])
                    index = comboBox_Value.findText(self.tableWidget.currentItem().text())
                    if index > -1:
                        comboBox_Value.setCurrentIndex(index)
                    self.tableWidget.setCellWidget(row, column, comboBox_Value)
                elif tagName == "UseLocalHeaderOffsets":
                    comboBox_Value = QComboBox()
                    comboBox_Value.addItems(["0", "1"])
                    index = comboBox_Value.findText(self.tableWidget.currentItem().text())
                    if index > -1:
                        comboBox_Value.setCurrentIndex(index)
                    self.tableWidget.setCellWidget(row, column, comboBox_Value)
                elif tagName == "ExportTickCount":
                    spinBox_Value = QSpinBox()
                    spinBox_Value.setRange(0, 99999999)
                    if self.tableWidget.currentItem() is not None:
                        spinBox_Value.setValue(int(self.tableWidget.currentItem().text()))
                    self.tableWidget.setCellWidget(row, column, spinBox_Value)
                elif tagName in ["DepthBiasScalar", "DepthSlopeScalar"]:
                    spinBox_Value = QDoubleSpinBox()
                    spinBox_Value.setRange(0, 99999999.99)
                    spinBox_Value.setDecimals(2)
                    if self.tableWidget.currentItem() is not None:
                        spinBox_Value.setValue(int(self.tableWidget.currentItem().text()))
                    self.tableWidget.setCellWidget(row, column, spinBox_Value)

            elif attribute == "hierarchySplit":
                comboBox_Value = QComboBox()
                comboBox_Value.addItems(["true", "false"])
                index = comboBox_Value.findText(self.tableWidget.currentItem().text())
                if index > -1:
                    comboBox_Value.setCurrentIndex(index)
                self.tableWidget.setCellWidget(row, column, comboBox_Value)

            elif attribute == "comparisonType":
                comboBox_Value = QComboBox()
                comboBox_Value.addItems(["WILDCARD_EQUAL_COMPARE", "WILDCARD_NOT_EQUAL_COMPARE", "EQUAL_COMPARE", "NOT_EQUAL_COMPARE", "REGEX"])
                index = comboBox_Value.findText(self.tableWidget.currentItem().text())
                if index > -1:
                    comboBox_Value.setCurrentIndex(index)
                self.tableWidget.setCellWidget(row, column, comboBox_Value)

            elif attribute in ["opCode", "fieldIndex", "pageInRadius", "pageOutRadius", "forceLoadedRadius"]:
                spinBox_Value = QSpinBox()
                spinBox_Value.setRange(0, 99999999)
                if self.tableWidget.currentItem() is not None:
                    spinBox_Value.setValue(int(self.tableWidget.currentItem().text()))
                self.tableWidget.setCellWidget(row, column, spinBox_Value)

            elif attribute in ["x", "y", "z", "k0", "k1", "k2", "k3", "k4"]:
                spinBox_Value = QDoubleSpinBox()
                spinBox_Value.setRange(-99999999.99, 99999999.99)
                spinBox_Value.setDecimals(2)
                if self.tableWidget.currentItem() is not None:
                    spinBox_Value.setValue(int(self.tableWidget.currentItem().text()))
                self.tableWidget.setCellWidget(row, column, spinBox_Value)

            elif attribute == "rule":
                # search rules...
                matches = self.treeWidget.findItems("Rule", Qt.MatchContains | Qt.MatchRecursive)
                rules = []
                for each in matches:
                    try:
                        # get the rule names
                        rules.append(each.text(0).split("(")[1].split(")")[0].strip())
                    except IndexError:
                        pass
                comboBox_Value = QComboBox()
                comboBox_Value.addItems(rules)
                if self.tableWidget.currentItem() is not None:
                    index = comboBox_Value.findText(self.tableWidget.currentItem().text())
                    if index > -1:
                        comboBox_Value.setCurrentIndex(index)
                self.tableWidget.setCellWidget(row, column, comboBox_Value)

            elif attribute == "nodeRule":
                # search rules...
                matches = self.treeWidget.findItems("NodeRule", Qt.MatchContains | Qt.MatchRecursive)
                rules = []
                for each in matches:
                    try:
                        # get the rule names
                        rules.append(each.text(0).split("(")[1].split(")")[0].strip())
                    except IndexError:
                        pass
                comboBox_Value = QComboBox()
                comboBox_Value.addItems(rules)
                if self.tableWidget.currentItem() is not None:
                    index = comboBox_Value.findText(self.tableWidget.currentItem().text())
                    if index > -1:
                        comboBox_Value.setCurrentIndex(index)
                self.tableWidget.setCellWidget(row, column, comboBox_Value)

            elif attribute == "fileRule":
                # search rules...
                matches = self.treeWidget.findItems("FileRule", Qt.MatchContains | Qt.MatchRecursive)
                rules = []
                for each in matches:
                    try:
                        # get the rule names
                        rules.append(each.text(0).split("(")[1].split(")")[0].strip())
                    except IndexError:
                        pass
                comboBox_Value = QComboBox()
                comboBox_Value.addItems(rules)
                if self.tableWidget.currentItem() is not None:
                    index = comboBox_Value.findText(self.tableWidget.currentItem().text())
                    if index > -1:
                        comboBox_Value.setCurrentIndex(index)
                self.tableWidget.setCellWidget(row, column, comboBox_Value)


    def leaveCell(self, currentRow, currentColumn, previousRow, previousColumn):
        if previousRow == -1 or previousColumn == -1:
            return

        widget = self.tableWidget.cellWidget(previousRow, previousColumn)
        currentText = ""
        if type(widget) == QComboBox:
            currentText = widget.currentText()
        elif type(widget) == QSpinBox:
            currentText = str(widget.value())

        if widget is None:
            return
        previousItem = self.tableWidget.item(previousRow, previousColumn)
        if previousItem is not None:
            previousItem.setText(currentText)
        else:
            newItem = QTableWidgetItem()
            newItem.setText(currentText)
            self.tableWidget.setItem(previousRow, previousColumn, newItem)

        self.tableWidget.removeCellWidget(previousRow, previousColumn)

    def generateTagItems(self, currentItem, type):
        if type == "add":
            tagName = currentItem.text(0).split("(")[0].strip()
        elif type == "show":
            tagName = currentItem.parent().text(0).split("(")[0].strip()

        childTags = []
        if tagName == "root":
            childTags = ["Logging", "TargetBasis", "ExportTickCount", "DepthBiasScalar", "DepthSlopeScalar",
                    "UseLocalHeaderOffsets", "Rules", "Meshes", "MeshGroups", "Entities", "Decorations",
                    "LightPoints", "Null", "Physics", "SpeedTrees", "TerrainLODs", "MeshOperation",
                    "Zones", "Materials"]
        elif tagName == "Logging":
            childTags = ["LogFltParse", "LogOverviewGeneration", "LogTextureHandling", "LogVisionGeneration",
                    "LogZoneExport", "LogToFile", "LogLevel"]
        elif tagName == "TargetBasis":
            childTags = ["Matrix"]
        elif tagName == "Matrix":
            childTags = ["Up", "Right", "Forward"]
        elif tagName == "Rules":
            childTags = ["NodeRule", "FileRule"]
        elif tagName == "NodeRule":
            childTags = ["AncillaryRule"]
        elif tagName == "Meshes" or tagName == "MeshGroups":
            childTags = ["MeshGroup"]
        elif tagName == "Entities":
            childTags = ["Entity"]
        elif tagName == "Decorations":
            childTags = ["DecorationGroup"]
        elif tagName == "LightPoints":
            childTags = ["LightPointGroup"]
        elif tagName == "Null":
            childTags = ["Null"]
        elif tagName == "Physics":
            childTags = ["ConvexHulls", "BaseGeometry", "MeshShapes", "Null", "PhysicsZone"]
        elif tagName == "ConvexHulls":
            childTags = ["Hull"]
        elif tagName == "BaseGeometry":
            childTags = ["Base"]
        elif tagName == "MeshShapes":
            childTags = ["Mesh"]
        elif tagName == "SpeedTrees":
            childTags = ["SpeedTreeGroup"]
        elif tagName == "TerrainLODs":
            childTags = ["TerrainLOD"]
        elif tagName == "MeshOperation":
            childTags = ["Recenter", "UseLocalHeaderOffsets", "SkipLOD", "NoShadows", "ChangeBasis"]
        elif tagName == "Zones":
            childTags = ["RootZone"]
        elif tagName == "RootZone":
            childTags = ["Zone", "Group"]
        elif tagName == "Materials":
            childTags = ["BlendType", "MappingType", "Shaders"]
        elif tagName == "BlendType":
            childTags = ["CustomBlend"]
        elif tagName == "MappingType":
            childTags = ["NormalMap", "SpecularMap", "DetailMap", "DiffuseMap", "IgnoreTexture"]
        elif tagName == "Shaders":
            childTags = ["Shader"]
        elif tagName == "Shader":
            childTags = ["Parameter", "Tag"]

        return childTags

    def showWidget(self, item, column):
        # do not show items for the invalid tags
        childTags = self.generateTagItems(self.treeWidget.currentItem(), "show")
        currentTag = self.treeWidget.currentItem().text(0)
        if len(childTags) > 0:
            # NOTE!!! it has to be a member, otherwise, it will be deleted by python garbage collection optimization
            self.tagComboBox = QComboBox()
            self.tagComboBox.addItems(childTags)
            self.treeWidget.setItemWidget(self.treeWidget.currentItem(), 0, self.tagComboBox)
            index = self.tagComboBox.findText(currentTag)
            if index > -1:
                self.tagComboBox.setCurrentIndex(index)

    def removeWidget(self, current, previous):
        if previous is None:
            return
        widget = self.treeWidget.itemWidget(previous, 0)
        if widget is None:
            return
        previous.setText(0, widget.currentText())
        self.treeWidget.removeItemWidget(previous, 0)

        # check if the tag has a name attribute
        for row in range(0, self.tableWidget.rowCount()):
            key = self.tableWidget.item(row, 0)
            value = self.tableWidget.item(row, 1)
            if key is not None and value is not None:
                if key.text() == "name":
                    text = widget.currentText()
                    previous.setText(0, text.split("(")[0].strip() + " ( " + value.text() + " )")

    def coypFromTag(self, curItem, parent):
        newItem = QTreeWidgetItem(parent)
        newItem.setText(0, curItem.text(0))
        newItem.setData(0, Qt.UserRole, curItem.data(0, Qt.UserRole))
        for index in range(0, curItem.childCount()):
            self.coypFromTag(curItem.child(index), newItem)

    def copyTag(self):
        curItem = self.treeWidget.currentItem()
        if curItem.text(0) == "root":
            return
        self.coypFromTag(curItem, curItem.parent())

    def addTag(self):
        if self.treeWidget.topLevelItemCount() == 0:
            return
        # remove the item widgets first, avoiding garbage collection crash
        widget = self.treeWidget.itemWidget(self.treeWidget.currentItem(), 0)
        if widget is not None and type(widget) is QComboBox:
            self.treeWidget.currentItem().setText(0, widget.currentText())
            self.treeWidget.removeItemWidget(self.treeWidget.currentItem(), 0)
        newItem = QTreeWidgetItem(self.treeWidget.currentItem())
        newItem.setText(0, "New Tag")

        # NOTE!!! it has to be a member, otherwise, it will be deleted by python garbage collection optimization
        self.tagComboBox = QComboBox()

        childTags = self.generateTagItems(self.treeWidget.currentItem(), "add")
        if len(childTags) > 0:
            self.tagComboBox.addItems(childTags)
            self.treeWidget.setItemWidget(newItem, 0, self.tagComboBox)
        else:
            newItem.setFlags(
            Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)

        self.treeWidget.setCurrentItem(newItem)
        self.treeWidget.editItem(newItem)
        # clear the table to prepare inserting data
        self.tableWidget.setRowCount(0)

    def delTag(self):
        if self.treeWidget.topLevelItemCount() == 0:
            return
        curItem = self.treeWidget.currentItem()
        if curItem.parent() is not None:
            curItem.parent().removeChild(curItem)
        else:
            curItem.takeChildren()

    def upTag(self):
        if self.treeWidget.topLevelItemCount() == 0:
            return
        curItem = self.treeWidget.currentItem()
        if curItem.parent() is not None:
            index = curItem.parent().indexOfChild(curItem)
            if index > 0:  # we don't need to move the top item
                upperItem = curItem.parent().child(index - 1)
                curItem.parent().removeChild(upperItem)
                curItem.parent().insertChild(index, upperItem)

    def downTag(self):
        if self.treeWidget.topLevelItemCount() == 0:
            return
        curItem = self.treeWidget.currentItem()
        if curItem.parent() is not None:
            index = curItem.parent().indexOfChild(curItem)
            if index < curItem.parent().childCount() - 1:  # we don't need to move the bottom item
                lowerItem = curItem.parent().child(index + 1)
                curItem.parent().removeChild(lowerItem)
                curItem.parent().insertChild(index, lowerItem)

    def outdentTag(self):
        if self.treeWidget.topLevelItemCount() == 0:
            return
        curItem = self.treeWidget.currentItem()
        parentItem = curItem.parent()
        if parentItem is not None and parentItem.parent() is not None:  # there can only be 1 root in xml file
            parentIndex = parentItem.parent().indexOfChild(parentItem)
            parentItem.removeChild(curItem)
            parentItem.parent().insertChild(parentIndex + 1, curItem)
            self.treeWidget.setCurrentItem(curItem)

    def indentTag(self):
        if self.treeWidget.topLevelItemCount() == 0:
            return
        curItem = self.treeWidget.currentItem()
        if (curItem.parent() is not None) and (
                curItem.parent().childCount() > 1):  # we don't indent the item when it is the only one
            index = curItem.parent().indexOfChild(curItem)
            if index > 0:
                broItem = curItem.parent().child(index - 1)
            else:
                broItem = curItem.parent().child(index + 1)
            curItem.parent().removeChild(curItem)
            broItem.insertChild(broItem.childCount(), curItem)
            self.treeWidget.setCurrentItem(curItem)

    def addAttribute(self):
        if self.treeWidget.topLevelItemCount() == 0:
            return
        self.tableWidget.insertRow(self.tableWidget.rowCount())

        tagName = self.treeWidget.currentItem().text(0).split("(")[0].strip()
        att = self.generateTagAttributes(tagName)
        if len(att) > 0:
            combo_Attribute = QComboBox()
            #combo_Attribute.currentIndexChanged.connect(lambda : pass)

            combo_Attribute.addItems(att)
            self.tableWidget.setCellWidget(self.tableWidget.rowCount()-1, 0, combo_Attribute)
        self.tableWidget.setCurrentCell(self.tableWidget.rowCount()-1, 0)

    def generateTagAttributes(self, tagName):
        if tagName == "LogToFile":
            att = ["enabled", "file"]
        elif tagName == "NodeRule":
            att = ["name", "hierarchySplit", "opCode", "fieldName", "fieldIndex", "comparisonValue", "comparisonType"]
        elif tagName == "FileRule":
            att = ["name", "comparisonValue", "comparisonType"]
        elif tagName == "AncillaryRule":
            att = ["name", "opCode", "fieldName", "fieldIndex", "comparisonValue", "comparisonType"]
        elif tagName == "SpeedTreeGroup":
            att = ["name", "rule", "speedtree"]
        elif tagName == "CustomBlend":
            att = ["rule", "k0", "k1", "k2", "k3", "k4"]
        elif tagName == "Shader":
            att = ["fileRule", "nodeRule", "lib", "effect"]

        elif tagName in ["LogFltParse", "LogOverviewGeneration", "LogTextureHandling", "LogVisionGeneration", "LogZoneExport"]:
            att = ["enabled"]
        elif tagName in ["LogLevel", "ExportTickCount", "DepthBiasScalar", "DepthSlopeScalar", "UseLocalHeaderOffsets"]:
            att = ["value"]
        elif tagName in ["Up", "Right", "Forward"]:
            att = ["x", "y", "z"]
        elif tagName in ["MeshGroup", "Null", "Hull", "Base", "Mesh", "TerrainLOD"]:
            att = ["name", "nodeRule", "fileRule"]
        elif tagName in ["Entity", "DecorationGroup", "LightPointGroup"]:
            att = ["name", "rule"]
        elif tagName in ["PhysicsZone", "RootZone"]:
            att = ["zoneName", "rule", "pageInRadius", "pageOutRadius", "forceLoadedRadius"]
        elif tagName in ["Group"]:
            att = ["name"]
        elif tagName in ["Zone", "Recenter", "UseLocalHeaderOffsets", "SkipLOD", "NoShadows", "ChangeBasis",
                         "NormalMap", "SpecularMap", "DetailMap", "DiffuseMap", "IgnoreTexture"]:
            att = ["rule"]
        elif tagName in ["Parameter",  "Tag"]:
            att = ["name", "value"]
        else:
            att = []

        return att

    def delAttribute(self):
        row = self.tableWidget.currentRow()
        if row > -1:
            self.tableWidget.removeRow(row)
            self.saveItemAttributes()

    # xml formatter
    def indent(self, elem, level=0):
        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def generateXML(self):
        root = self.createTree().getroot()
        self.indent(root)
        return ET.tostring(root)

    def newConfig(self):
        self.wizard = ConfigFileWizard(self)
        self.wizard.exec_()
        #self.mainDialog.moveToScreenCenter(self.wizard)

        """fileObj = QFileDialog.getSaveFileName(self, "New config file...", filter="Xml files (*.xml)")
        fileName = fileObj[0]
        if len(fileName) > 0:
            self.xml = fileName
            open(fileName, "w").write(
                "<root><Rules><FileRule name=\"flightFile\" comparisonType=\"REGEX\" comparisonValue=\".*flight.*\" />" +
                "<FileRule name=\"notFlightFile\" comparisonType=\"REGEX\" comparisonValue=\"(?!(.*flight.*)).*\" /></Rules>" +
                "<MeshOperation><SkipLOD rule=\"flightFile\"/></MeshOperation><Physics><MeshShapes><Mesh fileRule=\"notFlightFile\"/>" +
                "</MeshShapes><PhysicsZone rule=\"flightFile\" pageInRadius=\"100000\" pageOutRadius=\"200000\" forceLoadedRadius=\"1\"/></Physics>" +
                "<Zones><RootZone rule=\"flightFile\" pageInRadius=\"2000\" pageOutRadius=\"4000\" forceLoadedRadius=\"1000\"/></Zones></root>")
            self.readXML(fileName)
        else:
            self.treeWidget.setHeaderLabel("")"""

    def delConfig(self):
        self.treeWidget.clear()
        self.treeWidget.setHeaderLabel("")
        self.tableWidget.setRowCount(0)
        #os.remove(self.xml)

    def accept(self):
        # overwrite the current xml file
        if self.treeWidget.topLevelItemCount() == 0:
            return
        open(self.xml, "w").write(self.generateXML())
        self.mainDialog.comboBox_ConfigFile.insertItem(0, self.xml)
        self.mainDialog.comboBox_ConfigFile.setCurrentIndex(0)
        QDialog.accept(self)

    # drag a file in to the app, avoid accept dragging tree items
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls and len(event.mimeData().urls()) > 0:
            dragFile = event.mimeData().urls()[0].toLocalFile()
            fileExtension = os.path.splitext(os.path.basename(dragFile))[1]
            if fileExtension == ".xml":
                self.treeWidget.setStyleSheet(self.hintStyle)
            else:
                event.ignore()
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            dragFile = event.mimeData().urls()[0].toLocalFile()
            fileExtension = os.path.splitext(os.path.basename(dragFile))[1]
            event.acceptProposedAction()
            if fileExtension == ".xml":
                self.treeWidget.setStyleSheet(self.normalStyle)
                self.readXML(dragFile)
            else:
                event.ignore()
        else:
            event.ignore()
