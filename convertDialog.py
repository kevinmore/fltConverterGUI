from PySide.QtCore import *
from PySide.QtGui import *
import os
import subprocess

import convertDialog_Ui


class ConvertDialog(QDialog, convertDialog_Ui.Ui_convertDialog):
    jobDone = False

    def __init__(self, mainDialog, parent=None):
        super(ConvertDialog, self).__init__(parent)
        self.setupUi(self)
        self.mainDialog = mainDialog
        # start a thread to convert the data
        self.convertTheread = ConvertThread(mainDialog.prepareCommand(), mainDialog.getArguments(), self)
        self.convertTheread.start()

    # override the close event to kill the converting thread
    def closeEvent(self, e):
        if not self.jobDone:
            subprocess.call("TASKKILL /F /IM " + self.mainDialog.converterName)  # force kill the converter task
        self.convertTheread.terminate()
        self.mainDialog.convertButton.setEnabled(True)
        e.accept()

    def convertDone(self):
        self.jobDone = True
        # make sure the progressbar is full when the thread is done
        self.progressBar.setValue(100)
        # enable the convert button on the main dialog
        self.mainDialog.convertButton.setEnabled(True)


class ConvertThread(QThread):
    signal_content = Signal(str)
    signal_progress = Signal(float)
    signal_convertDone = Signal()
    processId = None

    def __init__(self, result, args, convertDialog, parent=None):
        super(ConvertThread, self).__init__(parent)
        self.result = result
        self.args = args
        self.convertDialog = convertDialog

        # connect the signals and slots to display the shell output and fill the progress bar
        self.signal_content.connect(self.convertDialog.textBrowser.append)
        self.signal_progress.connect(self.convertDialog.progressBar.setValue)
        self.signal_convertDone.connect(self.convertDialog.convertDone)

    def run(self):
        p = subprocess.Popen(self.result, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.processId = p.pid
        taskFinished = -1
        while True:
            buff = p.stdout.readline()
            # maybe a little hack, trying to check the output
            if buff.find("Exporting") > -1:
                taskFinished += 1

            # emit signals for the text browser and the progress bar
            self.signal_content.emit(buff)
            self.signal_progress.emit(taskFinished * 100 / self.convertDialog.mainDialog.fltCount)

            self.msleep(10)

            if not buff:
                break

        # converting done
        self.signal_convertDone.emit()

        # kill the this process
        p.wait()

        # open explorer at export path, works for windows only
        try:
            os.startfile(self.args["workPath"])
        except Exception:
            pass
