# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outside/views_ui/UsersList_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UsersList_Dialog(object):
    def setupUi(self, UsersList_Dialog):
        UsersList_Dialog.setObjectName("UsersList_Dialog")
        UsersList_Dialog.resize(591, 299)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UsersList_Dialog.sizePolicy().hasHeightForWidth())
        UsersList_Dialog.setSizePolicy(sizePolicy)
        UsersList_Dialog.setMinimumSize(QtCore.QSize(400, 200))
        UsersList_Dialog.setMaximumSize(QtCore.QSize(1000, 600))
        UsersList_Dialog.setBaseSize(QtCore.QSize(500, 250))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        UsersList_Dialog.setFont(font)
        UsersList_Dialog.setStyleSheet("background-color: rgb(39, 39, 39);\n"
"color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(39, 39, 39);\n"
"selection-background-color: rgb(15, 15, 15);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(UsersList_Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addUser_Button = QtWidgets.QPushButton(UsersList_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.addUser_Button.setFont(font)
        self.addUser_Button.setStyleSheet("color: rgb(255, 255, 255);")
        self.addUser_Button.setObjectName("addUser_Button")
        self.horizontalLayout.addWidget(self.addUser_Button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(UsersList_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.DefUser_ComboBox = QtWidgets.QComboBox(UsersList_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DefUser_ComboBox.sizePolicy().hasHeightForWidth())
        self.DefUser_ComboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.DefUser_ComboBox.setFont(font)
        self.DefUser_ComboBox.setObjectName("DefUser_ComboBox")
        self.horizontalLayout.addWidget(self.DefUser_ComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Users_Table = QtWidgets.QTableView(UsersList_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.Users_Table.setFont(font)
        self.Users_Table.setObjectName("Users_Table")
        self.verticalLayout.addWidget(self.Users_Table)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.CheckCookies_Button = QtWidgets.QPushButton(UsersList_Dialog)
        self.CheckCookies_Button.setObjectName("CheckCookies_Button")
        self.horizontalLayout_2.addWidget(self.CheckCookies_Button)
        self.ALive_Cookies_Button = QtWidgets.QPushButton(UsersList_Dialog)
        self.ALive_Cookies_Button.setObjectName("ALive_Cookies_Button")
        self.horizontalLayout_2.addWidget(self.ALive_Cookies_Button)
        self.buttonBox = QtWidgets.QDialogButtonBox(UsersList_Dialog)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.buttonBox.setFont(font)
        self.buttonBox.setStyleSheet("color: rgb(255, 255, 255);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Discard|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(UsersList_Dialog)
        self.buttonBox.accepted.connect(UsersList_Dialog.accept) # type: ignore
        self.buttonBox.accepted.connect(UsersList_Dialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(UsersList_Dialog)

    def retranslateUi(self, UsersList_Dialog):
        _translate = QtCore.QCoreApplication.translate
        UsersList_Dialog.setWindowTitle(_translate("UsersList_Dialog", "Users List"))
        self.addUser_Button.setText(_translate("UsersList_Dialog", " Add User "))
        self.label.setText(_translate("UsersList_Dialog", "Default:"))
        self.CheckCookies_Button.setText(_translate("UsersList_Dialog", " Check Cookies "))
        self.ALive_Cookies_Button.setText(_translate("UsersList_Dialog", " Check Cookies Life "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UsersList_Dialog = QtWidgets.QDialog()
    ui = Ui_UsersList_Dialog()
    ui.setupUi(UsersList_Dialog)
    UsersList_Dialog.show()
    sys.exit(app.exec_())
