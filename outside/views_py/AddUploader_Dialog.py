# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outside/views_ui/AddUploader_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddUser_Dialog(object):
    def setupUi(self, AddUser_Dialog):
        AddUser_Dialog.setObjectName("AddUser_Dialog")
        AddUser_Dialog.resize(485, 221)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddUser_Dialog.sizePolicy().hasHeightForWidth())
        AddUser_Dialog.setSizePolicy(sizePolicy)
        AddUser_Dialog.setMinimumSize(QtCore.QSize(360, 200))
        AddUser_Dialog.setMaximumSize(QtCore.QSize(600, 280))
        AddUser_Dialog.setBaseSize(QtCore.QSize(480, 220))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        AddUser_Dialog.setFont(font)
        AddUser_Dialog.setStyleSheet("background-color: rgb(39, 39, 39);\n"
"color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(39, 39, 39);\n"
"selection-background-color: rgb(15, 15, 15);")
        self.verticalLayout = QtWidgets.QVBoxLayout(AddUser_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AddUser_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Account_textbox = QtWidgets.QLineEdit(AddUser_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.Account_textbox.setFont(font)
        self.Account_textbox.setObjectName("Account_textbox")
        self.verticalLayout.addWidget(self.Account_textbox)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(AddUser_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Gmail_textbox = QtWidgets.QLineEdit(AddUser_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Gmail_textbox.sizePolicy().hasHeightForWidth())
        self.Gmail_textbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.Gmail_textbox.setFont(font)
        self.Gmail_textbox.setObjectName("Gmail_textbox")
        self.horizontalLayout.addWidget(self.Gmail_textbox)
        self.lineEdit_3 = QtWidgets.QLineEdit(AddUser_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(126, 32))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(126, 32))
        self.lineEdit_3.setBaseSize(QtCore.QSize(126, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_3.setMaxLength(10)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout.addWidget(self.lineEdit_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddUser_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.buttonBox.setFont(font)
        self.buttonBox.setStyleSheet("color: rgb(255, 255, 255);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddUser_Dialog)
        self.buttonBox.accepted.connect(AddUser_Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(AddUser_Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AddUser_Dialog)

    def retranslateUi(self, AddUser_Dialog):
        _translate = QtCore.QCoreApplication.translate
        AddUser_Dialog.setWindowTitle(_translate("AddUser_Dialog", "Add Uploader"))
        self.label.setText(_translate("AddUser_Dialog", "Account Name"))
        self.label_2.setText(_translate("AddUser_Dialog", "Gmail"))
        self.lineEdit_3.setText(_translate("AddUser_Dialog", "@gmail.com"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddUser_Dialog = QtWidgets.QDialog()
    ui = Ui_AddUser_Dialog()
    ui.setupUi(AddUser_Dialog)
    AddUser_Dialog.show()
    sys.exit(app.exec_())
