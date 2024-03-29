# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outside/views_ui/UpdateTime_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Upload_Time(object):
    def setupUi(self, Upload_Time):
        Upload_Time.setObjectName("Upload_Time")
        Upload_Time.resize(930, 437)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Upload_Time.sizePolicy().hasHeightForWidth())
        Upload_Time.setSizePolicy(sizePolicy)
        Upload_Time.setMaximumSize(QtCore.QSize(1000, 800))
        Upload_Time.setStyleSheet("background-color: rgb(39, 39, 39);\n"
"color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(39, 39, 39);\n"
"selection-background-color: rgb(15, 15, 15);")
        self.verticalLayout = QtWidgets.QVBoxLayout(Upload_Time)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Loop_radio = QtWidgets.QRadioButton(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Loop_radio.setFont(font)
        self.Loop_radio.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Loop_radio.setChecked(True)
        self.Loop_radio.setObjectName("Loop_radio")
        self.horizontalLayout.addWidget(self.Loop_radio, 0, QtCore.Qt.AlignHCenter)
        self.LoopGlobal_radio = QtWidgets.QRadioButton(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.LoopGlobal_radio.setFont(font)
        self.LoopGlobal_radio.setObjectName("LoopGlobal_radio")
        self.horizontalLayout.addWidget(self.LoopGlobal_radio, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.label_Start = QtWidgets.QLabel(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_Start.setFont(font)
        self.label_Start.setObjectName("label_Start")
        self.gridLayout.addWidget(self.label_Start, 0, 0, 1, 1)
        self.label_Step = QtWidgets.QLabel(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_Step.setFont(font)
        self.label_Step.setObjectName("label_Step")
        self.gridLayout.addWidget(self.label_Step, 0, 1, 1, 1)
        self.label_User = QtWidgets.QLabel(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_User.setFont(font)
        self.label_User.setObjectName("label_User")
        self.gridLayout.addWidget(self.label_User, 0, 2, 1, 1)
        self.label_Videos = QtWidgets.QLabel(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_Videos.setFont(font)
        self.label_Videos.setObjectName("label_Videos")
        self.gridLayout.addWidget(self.label_Videos, 0, 3, 1, 1)
        self.startTimeEdit_1 = QtWidgets.QDateTimeEdit(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.startTimeEdit_1.setFont(font)
        self.startTimeEdit_1.setCalendarPopup(True)
        self.startTimeEdit_1.setObjectName("startTimeEdit_1")
        self.gridLayout.addWidget(self.startTimeEdit_1, 1, 0, 1, 1)
        self.time_layout_1 = QtWidgets.QHBoxLayout()
        self.time_layout_1.setObjectName("time_layout_1")
        self.days_Spin_1 = QtWidgets.QSpinBox(Upload_Time)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.days_Spin_1.sizePolicy().hasHeightForWidth())
        self.days_Spin_1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.days_Spin_1.setFont(font)
        self.days_Spin_1.setObjectName("days_Spin_1")
        self.time_layout_1.addWidget(self.days_Spin_1)
        self.timeEdit_1 = QtWidgets.QTimeEdit(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.timeEdit_1.setFont(font)
        self.timeEdit_1.setObjectName("timeEdit_1")
        self.time_layout_1.addWidget(self.timeEdit_1)
        self.gridLayout.addLayout(self.time_layout_1, 1, 1, 1, 1)
        self.User_ComboBox_1 = QtWidgets.QComboBox(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.User_ComboBox_1.setFont(font)
        self.User_ComboBox_1.setObjectName("User_ComboBox_1")
        self.gridLayout.addWidget(self.User_ComboBox_1, 1, 2, 1, 1)
        self.videoCount_Spin_1 = QtWidgets.QSpinBox(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.videoCount_Spin_1.setFont(font)
        self.videoCount_Spin_1.setObjectName("videoCount_Spin_1")
        self.gridLayout.addWidget(self.videoCount_Spin_1, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.AddLoop_Button = QtWidgets.QPushButton(Upload_Time)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.AddLoop_Button.setFont(font)
        self.AddLoop_Button.setObjectName("AddLoop_Button")
        self.horizontalLayout_2.addWidget(self.AddLoop_Button)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Upload_Time)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Upload_Time)
        self.buttonBox.accepted.connect(Upload_Time.accept) # type: ignore
        self.buttonBox.rejected.connect(Upload_Time.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Upload_Time)

    def retranslateUi(self, Upload_Time):
        _translate = QtCore.QCoreApplication.translate
        Upload_Time.setWindowTitle(_translate("Upload_Time", "Upload Time Settings"))
        self.Loop_radio.setText(_translate("Upload_Time", "Loop (For Each User)"))
        self.LoopGlobal_radio.setText(_translate("Upload_Time", "Global Loop (For All Users)"))
        self.label_Start.setText(_translate("Upload_Time", "Start"))
        self.label_Step.setText(_translate("Upload_Time", "Step (days&time)"))
        self.label_User.setText(_translate("Upload_Time", "For User"))
        self.label_Videos.setText(_translate("Upload_Time", "Videos Count (0 = All)"))
        self.AddLoop_Button.setText(_translate("Upload_Time", "Add Loop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Upload_Time = QtWidgets.QDialog()
    ui = Ui_Upload_Time()
    ui.setupUi(Upload_Time)
    Upload_Time.show()
    sys.exit(app.exec_())
