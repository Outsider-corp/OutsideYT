# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outside/views_ui/SelectDownloadVideos_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Download_Videos_Dialog(object):
    def setupUi(self, Download_Videos_Dialog):
        Download_Videos_Dialog.setObjectName("Download_Videos_Dialog")
        Download_Videos_Dialog.setWindowModality(QtCore.Qt.NonModal)
        Download_Videos_Dialog.resize(647, 358)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Download_Videos_Dialog.sizePolicy().hasHeightForWidth())
        Download_Videos_Dialog.setSizePolicy(sizePolicy)
        Download_Videos_Dialog.setMinimumSize(QtCore.QSize(500, 250))
        Download_Videos_Dialog.setMaximumSize(QtCore.QSize(1000, 500))
        Download_Videos_Dialog.setBaseSize(QtCore.QSize(560, 300))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 15, 15))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 15, 15))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 15, 15))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(39, 39, 39))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        Download_Videos_Dialog.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        Download_Videos_Dialog.setFont(font)
        Download_Videos_Dialog.setStyleSheet("background-color: rgb(39, 39, 39);\n"
"color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(39, 39, 39);\n"
"selection-background-color: rgb(15, 15, 15);")
        self.verticalLayout = QtWidgets.QVBoxLayout(Download_Videos_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.line_2 = QtWidgets.QFrame(Download_Videos_Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AddVideo_Button = QtWidgets.QPushButton(Download_Videos_Dialog)
        self.AddVideo_Button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddVideo_Button.sizePolicy().hasHeightForWidth())
        self.AddVideo_Button.setSizePolicy(sizePolicy)
        self.AddVideo_Button.setMinimumSize(QtCore.QSize(150, 0))
        self.AddVideo_Button.setBaseSize(QtCore.QSize(500, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.AddVideo_Button.setFont(font)
        self.AddVideo_Button.setObjectName("AddVideo_Button")
        self.horizontalLayout.addWidget(self.AddVideo_Button)
        self.AddPlaylist_Button = QtWidgets.QPushButton(Download_Videos_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddPlaylist_Button.sizePolicy().hasHeightForWidth())
        self.AddPlaylist_Button.setSizePolicy(sizePolicy)
        self.AddPlaylist_Button.setMinimumSize(QtCore.QSize(170, 0))
        self.AddPlaylist_Button.setBaseSize(QtCore.QSize(500, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.AddPlaylist_Button.setFont(font)
        self.AddPlaylist_Button.setObjectName("AddPlaylist_Button")
        self.horizontalLayout.addWidget(self.AddPlaylist_Button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(15, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Import_links_Button = QtWidgets.QPushButton(Download_Videos_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Import_links_Button.sizePolicy().hasHeightForWidth())
        self.Import_links_Button.setSizePolicy(sizePolicy)
        self.Import_links_Button.setMinimumSize(QtCore.QSize(200, 0))
        self.Import_links_Button.setBaseSize(QtCore.QSize(500, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.Import_links_Button.setFont(font)
        self.Import_links_Button.setObjectName("Import_links_Button")
        self.horizontalLayout_2.addWidget(self.Import_links_Button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.line = QtWidgets.QFrame(Download_Videos_Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Select_channel_Button = QtWidgets.QPushButton(Download_Videos_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Select_channel_Button.sizePolicy().hasHeightForWidth())
        self.Select_channel_Button.setSizePolicy(sizePolicy)
        self.Select_channel_Button.setMinimumSize(QtCore.QSize(130, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.Select_channel_Button.setFont(font)
        self.Select_channel_Button.setObjectName("Select_channel_Button")
        self.horizontalLayout_3.addWidget(self.Select_channel_Button)
        self.channel_link_textBox = QtWidgets.QLineEdit(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.channel_link_textBox.setFont(font)
        self.channel_link_textBox.setObjectName("channel_link_textBox")
        self.horizontalLayout_3.addWidget(self.channel_link_textBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.Last_video_radioButton = QtWidgets.QRadioButton(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Last_video_radioButton.setFont(font)
        self.Last_video_radioButton.setChecked(True)
        self.Last_video_radioButton.setObjectName("Last_video_radioButton")
        self.horizontalLayout_5.addWidget(self.Last_video_radioButton)
        self.Random_video_radioButton = QtWidgets.QRadioButton(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Random_video_radioButton.setFont(font)
        self.Random_video_radioButton.setChecked(False)
        self.Random_video_radioButton.setObjectName("Random_video_radioButton")
        self.horizontalLayout_5.addWidget(self.Random_video_radioButton)
        self.Period_radioButton = QtWidgets.QRadioButton(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Period_radioButton.setFont(font)
        self.Period_radioButton.setObjectName("Period_radioButton")
        self.horizontalLayout_5.addWidget(self.Period_radioButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.Count_label = QtWidgets.QLabel(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Count_label.setFont(font)
        self.Count_label.setObjectName("Count_label")
        self.horizontalLayout_7.addWidget(self.Count_label)
        self.Count_videos_spinBox = QtWidgets.QSpinBox(Download_Videos_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Count_videos_spinBox.sizePolicy().hasHeightForWidth())
        self.Count_videos_spinBox.setSizePolicy(sizePolicy)
        self.Count_videos_spinBox.setMinimumSize(QtCore.QSize(50, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Count_videos_spinBox.setFont(font)
        self.Count_videos_spinBox.setObjectName("Count_videos_spinBox")
        self.horizontalLayout_7.addWidget(self.Count_videos_spinBox)
        self.Start_label = QtWidgets.QLabel(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Start_label.setFont(font)
        self.Start_label.setObjectName("Start_label")
        self.horizontalLayout_7.addWidget(self.Start_label)
        self.Start_date = QtWidgets.QDateEdit(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Start_date.setFont(font)
        self.Start_date.setObjectName("Start_date")
        self.horizontalLayout_7.addWidget(self.Start_date)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem8)
        self.End_label = QtWidgets.QLabel(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.End_label.setFont(font)
        self.End_label.setObjectName("End_label")
        self.horizontalLayout_7.addWidget(self.End_label)
        self.End_date = QtWidgets.QDateEdit(Download_Videos_Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.End_date.setFont(font)
        self.End_date.setObjectName("End_date")
        self.horizontalLayout_7.addWidget(self.End_date)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem9)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        spacerItem10 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem10)
        self.buttonBox = QtWidgets.QDialogButtonBox(Download_Videos_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setBaseSize(QtCore.QSize(600, 270))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignBottom)

        self.retranslateUi(Download_Videos_Dialog)
        self.buttonBox.accepted.connect(Download_Videos_Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Download_Videos_Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Download_Videos_Dialog)

    def retranslateUi(self, Download_Videos_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Download_Videos_Dialog.setWindowTitle(_translate("Download_Videos_Dialog", "Select Videos for downloading"))
        self.AddVideo_Button.setText(_translate("Download_Videos_Dialog", "Add Video"))
        self.AddPlaylist_Button.setText(_translate("Download_Videos_Dialog", "Add Playlist"))
        self.Import_links_Button.setText(_translate("Download_Videos_Dialog", "Import links from File"))
        self.Select_channel_Button.setText(_translate("Download_Videos_Dialog", "  Select channel  "))
        self.Last_video_radioButton.setText(_translate("Download_Videos_Dialog", "Last Videos"))
        self.Random_video_radioButton.setText(_translate("Download_Videos_Dialog", "Random Videos"))
        self.Period_radioButton.setText(_translate("Download_Videos_Dialog", "Period of Time"))
        self.Count_label.setText(_translate("Download_Videos_Dialog", "Count"))
        self.Start_label.setText(_translate("Download_Videos_Dialog", "Start"))
        self.End_label.setText(_translate("Download_Videos_Dialog", "End"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Download_Videos_Dialog = QtWidgets.QDialog()
    ui = Ui_Download_Videos_Dialog()
    ui.setupUi(Download_Videos_Dialog)
    Download_Videos_Dialog.show()
    sys.exit(app.exec_())
