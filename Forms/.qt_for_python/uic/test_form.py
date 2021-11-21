# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'z:\OneDrive\HTML Parser\Python\Forms\test_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("z:\\OneDrive\\HTML Parser\\Python\\Forms\\../ICOs/DrEvil.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(243, 243, 243);")
        self.cb_url = QtWidgets.QCheckBox(Form)
        self.cb_url.setEnabled(False)
        self.cb_url.setGeometry(QtCore.QRect(30, 340, 100, 30))
        self.cb_url.setCheckable(True)
        self.cb_url.setObjectName("cb_url")
        self.cb_textfile = QtWidgets.QCheckBox(Form)
        self.cb_textfile.setGeometry(QtCore.QRect(30, 10, 100, 30))
        self.cb_textfile.setChecked(True)
        self.cb_textfile.setObjectName("cb_textfile")
        self.linedit_url = QtWidgets.QLineEdit(Form)
        self.linedit_url.setEnabled(False)
        self.linedit_url.setGeometry(QtCore.QRect(30, 370, 570, 30))
        self.linedit_url.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(255, 255, 255);")
        self.linedit_url.setObjectName("linedit_url")
        self.list_textfile = QtWidgets.QListWidget(Form)
        self.list_textfile.setGeometry(QtCore.QRect(30, 40, 570, 300))
        self.list_textfile.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 8pt \"MS Shell Dlg 2\";")
        self.list_textfile.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.list_textfile.setObjectName("list_textfile")
        self.pushbutton_run = QtWidgets.QPushButton(Form)
        self.pushbutton_run.setGeometry(QtCore.QRect(30, 420, 570, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushbutton_run.setFont(font)
        self.pushbutton_run.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.pushbutton_run.setCheckable(False)
        self.pushbutton_run.setObjectName("pushbutton_run")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.cb_textfile, self.list_textfile)
        Form.setTabOrder(self.list_textfile, self.cb_url)
        Form.setTabOrder(self.cb_url, self.linedit_url)
        Form.setTabOrder(self.linedit_url, self.pushbutton_run)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Test form"))
        self.cb_url.setText(_translate("Form", "URL ?"))
        self.cb_textfile.setText(_translate("Form", "Text File ?"))
        self.pushbutton_run.setText(_translate("Form", "Τρέχα"))
