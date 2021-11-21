import os
import sys
from random import randint
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("test_form.ui", self)
        self.list_init()
        self.sayings_list = self.sayings_load()

        self.cb_textfile.stateChanged.connect(self.cb_textfile_changed)
        self.cb_url.stateChanged.connect(self.cb_url_checked)
        self.pushbutton_run.clicked.connect(self.pushbutton_run_clicked)

    def cb_textfile_changed(self) :
        if self.cb_textfile.isChecked() :
            self.cb_url.setChecked(False)
            self.cb_url.setDisabled(True)
            self.linedit_url.setDisabled(True)
            self.list_textfile.setDisabled(False)
        else :
            self.cb_url.setDisabled(False)
            self.cb_url.setChecked(True)
            self.linedit_url.setDisabled(False)
            self.list_textfile.setDisabled(True)

    def cb_url_checked(self) :
        if self.cb_url.isChecked() :
            # self.cb_url.setChecked(True)
            # self.cb_url.setDisabled(True)
            # self.linedit_url.setDisabled(True)
            self.cb_textfile.setChecked(False)
            self.list_textfile.setDisabled(True)
        else :
            self.cb_url.setDisabled(True)
            self.cb_url.setChecked(False)
            self.cb_textfile.setChecked(True)
            self.linedit_url.setDisabled(True)
            self.list_textfile.setDisabled(False)

    def pushbutton_run_clicked(self) :
        saying_idx = randint(0, len(self.sayings_list))
        print("Σιωπή θα απαγγείλω: " + self.sayings_list[saying_idx])
        self.pushbutton_run.setText("Τρέξε... να γλυτώσεις... τώρα τρέξε... αν σε πιάσω μπορεί να νιώσεις")

    def list_init(self) :
        self.url_list = self.txt_to_list()
        for item in self.url_list :
         print(item)
        self.list_textfile.addItems(self.url_list)
    
    def txt_to_list(self):
        url_list = []
        if os.path.exists("Z://OneDrive//HTML Parser//Python//Forms//testtext.txt") == True :
            text_file = open("Z://OneDrive//HTML Parser//Python//Forms//testtext.txt")
            lines = text_file.readlines()
            text_file.close()
            url_idx = 0
            for line in lines :
                if line.find("http") == 0 :
                    url_idx += 1
                    url_list.append(str(url_idx) + ": " + line.strip())
                else :
                    continue
        else :
            url_list.append("File not found.")
        
        return(url_list)

    def sayings_load(self) :
        sayings_list = []
        if os.path.exists("Z://OneDrive//HTML Parser//Python//Forms//sayings.txt") == True :
            text_file = open("Z://OneDrive//HTML Parser//Python//Forms//sayings.txt", "r", encoding="utf-8")
            lines = text_file.readlines()
            text_file.close()
            for line in lines :
                sayings_list.append(line.strip())
        else :
            sayings_list.append("Είναι η ζωή μου άδεια.")
        
        return(sayings_list)


# main
app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(480)
widget.setFixedWidth(640)
widget.show()
# mainwindow.list_init()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

