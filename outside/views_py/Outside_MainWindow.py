# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outside/views_ui/Outside_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_YouTubeOutside(object):
    def setupUi(self, YouTubeOutside):
        YouTubeOutside.setObjectName("YouTubeOutside")
        YouTubeOutside.resize(1031, 634)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(YouTubeOutside.sizePolicy().hasHeightForWidth())
        YouTubeOutside.setSizePolicy(sizePolicy)
        YouTubeOutside.setMinimumSize(QtCore.QSize(650, 400))
        YouTubeOutside.setBaseSize(QtCore.QSize(1000, 550))
        YouTubeOutside.setLayoutDirection(QtCore.Qt.LeftToRight)
        YouTubeOutside.setStyleSheet("alternate-background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);\n"
"border-color: rgb(129, 136, 136);\n"
"border-top-color: rgb(129, 136, 136);\n"
"selection-background-color: rgb(61, 61, 61);")
        YouTubeOutside.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(YouTubeOutside)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(350, 200))
        self.centralwidget.setBaseSize(QtCore.QSize(1036, 640))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.OutsideYT = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OutsideYT.sizePolicy().hasHeightForWidth())
        self.OutsideYT.setSizePolicy(sizePolicy)
        self.OutsideYT.setMinimumSize(QtCore.QSize(300, 200))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.OutsideYT.setFont(font)
        self.OutsideYT.setStyleSheet("background-color: rgb(39, 39, 39);\n"
"alternate-background-color: rgb(39, 39, 39);\n"
"selection-background-color: rgb(15, 15, 15);")
        self.OutsideYT.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.OutsideYT.setUsesScrollButtons(True)
        self.OutsideYT.setDocumentMode(False)
        self.OutsideYT.setTabsClosable(False)
        self.OutsideYT.setMovable(False)
        self.OutsideYT.setTabBarAutoHide(False)
        self.OutsideYT.setProperty("Anchor", "")
        self.OutsideYT.setObjectName("OutsideYT")
        self.UploadPage = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UploadPage.sizePolicy().hasHeightForWidth())
        self.UploadPage.setSizePolicy(sizePolicy)
        self.UploadPage.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.UploadPage.setObjectName("UploadPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.UploadPage)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Upload_SelectAll_CheckBox = QtWidgets.QCheckBox(self.UploadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Upload_SelectAll_CheckBox.setFont(font)
        self.Upload_SelectAll_CheckBox.setChecked(True)
        self.Upload_SelectAll_CheckBox.setObjectName("Upload_SelectAll_CheckBox")
        self.horizontalLayout_3.addWidget(self.Upload_SelectAll_CheckBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.Upload_Check_Button = QtWidgets.QPushButton(self.UploadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Upload_Check_Button.setFont(font)
        self.Upload_Check_Button.setObjectName("Upload_Check_Button")
        self.horizontalLayout_3.addWidget(self.Upload_Check_Button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.Upload_UploadTime_Button = QtWidgets.QPushButton(self.UploadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Upload_UploadTime_Button.setFont(font)
        self.Upload_UploadTime_Button.setObjectName("Upload_UploadTime_Button")
        self.horizontalLayout_3.addWidget(self.Upload_UploadTime_Button, 0, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.Upload_ClearUTime_Button = QtWidgets.QPushButton(self.UploadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Upload_ClearUTime_Button.setFont(font)
        self.Upload_ClearUTime_Button.setObjectName("Upload_ClearUTime_Button")
        self.horizontalLayout_3.addWidget(self.Upload_ClearUTime_Button)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.Upload_SelectVideos_Button = QtWidgets.QPushButton(self.UploadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Upload_SelectVideos_Button.sizePolicy().hasHeightForWidth())
        self.Upload_SelectVideos_Button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Upload_SelectVideos_Button.setFont(font)
        self.Upload_SelectVideos_Button.setObjectName("Upload_SelectVideos_Button")
        self.horizontalLayout_3.addWidget(self.Upload_SelectVideos_Button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem5 = QtWidgets.QSpacerItem(11, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem5)
        self.Upload_Table = QtWidgets.QTableView(self.UploadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Upload_Table.setFont(font)
        self.Upload_Table.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.Upload_Table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Upload_Table.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Upload_Table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.Upload_Table.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.Upload_Table.setAlternatingRowColors(True)
        self.Upload_Table.setTextElideMode(QtCore.Qt.ElideRight)
        self.Upload_Table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.Upload_Table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.Upload_Table.setGridStyle(QtCore.Qt.DotLine)
        self.Upload_Table.setSortingEnabled(True)
        self.Upload_Table.setObjectName("Upload_Table")
        self.verticalLayout_2.addWidget(self.Upload_Table)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Upload_Progress_Bar = QtWidgets.QProgressBar(self.UploadPage)
        self.Upload_Progress_Bar.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Upload_Progress_Bar.setFont(font)
        self.Upload_Progress_Bar.setProperty("value", 0)
        self.Upload_Progress_Bar.setInvertedAppearance(False)
        self.Upload_Progress_Bar.setObjectName("Upload_Progress_Bar")
        self.horizontalLayout.addWidget(self.Upload_Progress_Bar)
        self.Upload_Progress_Label = QtWidgets.QLabel(self.UploadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Upload_Progress_Label.sizePolicy().hasHeightForWidth())
        self.Upload_Progress_Label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Upload_Progress_Label.setFont(font)
        self.Upload_Progress_Label.setText("")
        self.Upload_Progress_Label.setTextFormat(QtCore.Qt.PlainText)
        self.Upload_Progress_Label.setWordWrap(True)
        self.Upload_Progress_Label.setObjectName("Upload_Progress_Label")
        self.horizontalLayout.addWidget(self.Upload_Progress_Label)
        self.Upload_delete_after_upload_checkBox = QtWidgets.QCheckBox(self.UploadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Upload_delete_after_upload_checkBox.setFont(font)
        self.Upload_delete_after_upload_checkBox.setObjectName("Upload_delete_after_upload_checkBox")
        self.horizontalLayout.addWidget(self.Upload_delete_after_upload_checkBox)
        self.Upload_ShowBrowser_checkBox = QtWidgets.QCheckBox(self.UploadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Upload_ShowBrowser_checkBox.setFont(font)
        self.Upload_ShowBrowser_checkBox.setObjectName("Upload_ShowBrowser_checkBox")
        self.horizontalLayout.addWidget(self.Upload_ShowBrowser_checkBox)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.Upload_Start = QtWidgets.QPushButton(self.UploadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Upload_Start.sizePolicy().hasHeightForWidth())
        self.Upload_Start.setSizePolicy(sizePolicy)
        self.Upload_Start.setMinimumSize(QtCore.QSize(122, 31))
        self.Upload_Start.setBaseSize(QtCore.QSize(122, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.Upload_Start.setFont(font)
        self.Upload_Start.setObjectName("Upload_Start")
        self.horizontalLayout.addWidget(self.Upload_Start, 0, QtCore.Qt.AlignRight)
        spacerItem7 = QtWidgets.QSpacerItem(40, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.OutsideYT.addTab(self.UploadPage, "")
        self.WatchPage = QtWidgets.QWidget()
        self.WatchPage.setObjectName("WatchPage")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.WatchPage)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Watch_SelectAll_CheckBox = QtWidgets.QCheckBox(self.WatchPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Watch_SelectAll_CheckBox.setFont(font)
        self.Watch_SelectAll_CheckBox.setChecked(True)
        self.Watch_SelectAll_CheckBox.setObjectName("Watch_SelectAll_CheckBox")
        self.horizontalLayout_4.addWidget(self.Watch_SelectAll_CheckBox)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.Watch_url_label = QtWidgets.QLabel(self.WatchPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Watch_url_label.setFont(font)
        self.Watch_url_label.setObjectName("Watch_url_label")
        self.horizontalLayout_4.addWidget(self.Watch_url_label)
        self.Watch_url_textBox = QtWidgets.QLineEdit(self.WatchPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Watch_url_textBox.setFont(font)
        self.Watch_url_textBox.setPlaceholderText("")
        self.Watch_url_textBox.setObjectName("Watch_url_textBox")
        self.horizontalLayout_4.addWidget(self.Watch_url_textBox)
        self.Watch_url_add_Button = QtWidgets.QPushButton(self.WatchPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Watch_url_add_Button.setFont(font)
        self.Watch_url_add_Button.setObjectName("Watch_url_add_Button")
        self.horizontalLayout_4.addWidget(self.Watch_url_add_Button)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.Watch_SelectVideos_Button = QtWidgets.QPushButton(self.WatchPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Watch_SelectVideos_Button.setFont(font)
        self.Watch_SelectVideos_Button.setObjectName("Watch_SelectVideos_Button")
        self.horizontalLayout_4.addWidget(self.Watch_SelectVideos_Button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem10 = QtWidgets.QSpacerItem(11, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem10)
        self.Watch_Table = QtWidgets.QTableView(self.WatchPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Watch_Table.setFont(font)
        self.Watch_Table.setObjectName("Watch_Table")
        self.verticalLayout.addWidget(self.Watch_Table)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.Watch_Progress_Bar = QtWidgets.QProgressBar(self.WatchPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Watch_Progress_Bar.setFont(font)
        self.Watch_Progress_Bar.setProperty("value", 0)
        self.Watch_Progress_Bar.setObjectName("Watch_Progress_Bar")
        self.horizontalLayout_6.addWidget(self.Watch_Progress_Bar)
        self.Watch_Progress_Label = QtWidgets.QLabel(self.WatchPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Watch_Progress_Label.sizePolicy().hasHeightForWidth())
        self.Watch_Progress_Label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Watch_Progress_Label.setFont(font)
        self.Watch_Progress_Label.setText("")
        self.Watch_Progress_Label.setTextFormat(QtCore.Qt.PlainText)
        self.Watch_Progress_Label.setWordWrap(True)
        self.Watch_Progress_Label.setObjectName("Watch_Progress_Label")
        self.horizontalLayout_6.addWidget(self.Watch_Progress_Label)
        self.Watch_ShowBrowser_checkBox = QtWidgets.QCheckBox(self.WatchPage)
        self.Watch_ShowBrowser_checkBox.setObjectName("Watch_ShowBrowser_checkBox")
        self.horizontalLayout_6.addWidget(self.Watch_ShowBrowser_checkBox)
        self.Watch_advanced_settings_Button = QtWidgets.QPushButton(self.WatchPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Watch_advanced_settings_Button.setFont(font)
        self.Watch_advanced_settings_Button.setObjectName("Watch_advanced_settings_Button")
        self.horizontalLayout_6.addWidget(self.Watch_advanced_settings_Button)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem11)
        self.Watch_Start = QtWidgets.QPushButton(self.WatchPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Watch_Start.sizePolicy().hasHeightForWidth())
        self.Watch_Start.setSizePolicy(sizePolicy)
        self.Watch_Start.setMinimumSize(QtCore.QSize(122, 31))
        self.Watch_Start.setBaseSize(QtCore.QSize(122, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.Watch_Start.setFont(font)
        self.Watch_Start.setObjectName("Watch_Start")
        self.horizontalLayout_6.addWidget(self.Watch_Start, 0, QtCore.Qt.AlignRight)
        spacerItem12 = QtWidgets.QSpacerItem(40, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem12)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.OutsideYT.addTab(self.WatchPage, "")
        self.DownloadPage = QtWidgets.QWidget()
        self.DownloadPage.setObjectName("DownloadPage")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.DownloadPage)
        self.verticalLayout_6.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(10)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.Download_SelectAll_CheckBox = QtWidgets.QCheckBox(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_SelectAll_CheckBox.setFont(font)
        self.Download_SelectAll_CheckBox.setChecked(True)
        self.Download_SelectAll_CheckBox.setObjectName("Download_SelectAll_CheckBox")
        self.horizontalLayout_8.addWidget(self.Download_SelectAll_CheckBox)
        spacerItem13 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem13)
        self.Download_url_label = QtWidgets.QLabel(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_url_label.setFont(font)
        self.Download_url_label.setObjectName("Download_url_label")
        self.horizontalLayout_8.addWidget(self.Download_url_label)
        self.Download_url_textBox = QtWidgets.QLineEdit(self.DownloadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Download_url_textBox.sizePolicy().hasHeightForWidth())
        self.Download_url_textBox.setSizePolicy(sizePolicy)
        self.Download_url_textBox.setMinimumSize(QtCore.QSize(120, 0))
        self.Download_url_textBox.setBaseSize(QtCore.QSize(120, 0))
        self.Download_url_textBox.setObjectName("Download_url_textBox")
        self.horizontalLayout_8.addWidget(self.Download_url_textBox)
        self.Download_url_add_Button = QtWidgets.QPushButton(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_url_add_Button.setFont(font)
        self.Download_url_add_Button.setObjectName("Download_url_add_Button")
        self.horizontalLayout_8.addWidget(self.Download_url_add_Button)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem14)
        self.Download_Save_to_label = QtWidgets.QLabel(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_Save_to_label.setFont(font)
        self.Download_Save_to_label.setObjectName("Download_Save_to_label")
        self.horizontalLayout_8.addWidget(self.Download_Save_to_label)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Download_User_Save_Mode_radioButton = QtWidgets.QRadioButton(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_User_Save_Mode_radioButton.setFont(font)
        self.Download_User_Save_Mode_radioButton.setChecked(True)
        self.Download_User_Save_Mode_radioButton.setObjectName("Download_User_Save_Mode_radioButton")
        self.verticalLayout_4.addWidget(self.Download_User_Save_Mode_radioButton)
        self.Download_Folder_Save_Mode_radioButton = QtWidgets.QRadioButton(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_Folder_Save_Mode_radioButton.setFont(font)
        self.Download_Folder_Save_Mode_radioButton.setObjectName("Download_Folder_Save_Mode_radioButton")
        self.verticalLayout_4.addWidget(self.Download_Folder_Save_Mode_radioButton)
        self.horizontalLayout_8.addLayout(self.verticalLayout_4)
        self.Download_Save_to_ComboBox = QtWidgets.QComboBox(self.DownloadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Download_Save_to_ComboBox.sizePolicy().hasHeightForWidth())
        self.Download_Save_to_ComboBox.setSizePolicy(sizePolicy)
        self.Download_Save_to_ComboBox.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_Save_to_ComboBox.setFont(font)
        self.Download_Save_to_ComboBox.setObjectName("Download_Save_to_ComboBox")
        self.horizontalLayout_8.addWidget(self.Download_Save_to_ComboBox)
        self.Download_Save_textBox = QtWidgets.QLineEdit(self.DownloadPage)
        self.Download_Save_textBox.setObjectName("Download_Save_textBox")
        self.horizontalLayout_8.addWidget(self.Download_Save_textBox)
        self.Download_Select_Path_Button = QtWidgets.QPushButton(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_Select_Path_Button.setFont(font)
        self.Download_Select_Path_Button.setObjectName("Download_Select_Path_Button")
        self.horizontalLayout_8.addWidget(self.Download_Select_Path_Button)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem15)
        self.Download_SelectVideos_Button = QtWidgets.QPushButton(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_SelectVideos_Button.setFont(font)
        self.Download_SelectVideos_Button.setObjectName("Download_SelectVideos_Button")
        self.horizontalLayout_8.addWidget(self.Download_SelectVideos_Button)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        spacerItem16 = QtWidgets.QSpacerItem(11, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem16)
        self.Download_Table = QtWidgets.QTableView(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_Table.setFont(font)
        self.Download_Table.setObjectName("Download_Table")
        self.verticalLayout_6.addWidget(self.Download_Table)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(10)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.Download_Progress_Bar = QtWidgets.QProgressBar(self.DownloadPage)
        self.Download_Progress_Bar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Download_Progress_Bar.sizePolicy().hasHeightForWidth())
        self.Download_Progress_Bar.setSizePolicy(sizePolicy)
        self.Download_Progress_Bar.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.Download_Progress_Bar.setFont(font)
        self.Download_Progress_Bar.setProperty("value", 0)
        self.Download_Progress_Bar.setObjectName("Download_Progress_Bar")
        self.horizontalLayout_10.addWidget(self.Download_Progress_Bar)
        self.Download_Progress_Label = QtWidgets.QLabel(self.DownloadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Download_Progress_Label.sizePolicy().hasHeightForWidth())
        self.Download_Progress_Label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Download_Progress_Label.setFont(font)
        self.Download_Progress_Label.setText("")
        self.Download_Progress_Label.setTextFormat(QtCore.Qt.PlainText)
        self.Download_Progress_Label.setWordWrap(True)
        self.Download_Progress_Label.setObjectName("Download_Progress_Label")
        self.horizontalLayout_10.addWidget(self.Download_Progress_Label)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.Download_Info_checkBox = QtWidgets.QCheckBox(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Download_Info_checkBox.setFont(font)
        self.Download_Info_checkBox.setChecked(True)
        self.Download_Info_checkBox.setObjectName("Download_Info_checkBox")
        self.verticalLayout_5.addWidget(self.Download_Info_checkBox)
        self.Download_Video_checkBox = QtWidgets.QCheckBox(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Download_Video_checkBox.setFont(font)
        self.Download_Video_checkBox.setChecked(True)
        self.Download_Video_checkBox.setObjectName("Download_Video_checkBox")
        self.verticalLayout_5.addWidget(self.Download_Video_checkBox)
        self.horizontalLayout_10.addLayout(self.verticalLayout_5)
        self.Download_advanced_settings_Button = QtWidgets.QPushButton(self.DownloadPage)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Download_advanced_settings_Button.setFont(font)
        self.Download_advanced_settings_Button.setObjectName("Download_advanced_settings_Button")
        self.horizontalLayout_10.addWidget(self.Download_advanced_settings_Button)
        self.Download_Start = QtWidgets.QPushButton(self.DownloadPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Download_Start.sizePolicy().hasHeightForWidth())
        self.Download_Start.setSizePolicy(sizePolicy)
        self.Download_Start.setMinimumSize(QtCore.QSize(122, 31))
        self.Download_Start.setBaseSize(QtCore.QSize(122, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.Download_Start.setFont(font)
        self.Download_Start.setObjectName("Download_Start")
        self.horizontalLayout_10.addWidget(self.Download_Start, 0, QtCore.Qt.AlignRight)
        spacerItem17 = QtWidgets.QSpacerItem(40, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem17)
        self.verticalLayout_6.addLayout(self.horizontalLayout_10)
        self.OutsideYT.addTab(self.DownloadPage, "")
        self.gridLayout.addWidget(self.OutsideYT, 2, 0, 1, 1)
        YouTubeOutside.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(YouTubeOutside)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 21))
        self.menubar.setObjectName("menubar")
        self.menuOutside_YouTube = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.menuOutside_YouTube.setFont(font)
        self.menuOutside_YouTube.setObjectName("menuOutside_YouTube")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.menuHelp.setFont(font)
        self.menuHelp.setObjectName("menuHelp")
        self.menuUsers_Lists = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.menuUsers_Lists.setFont(font)
        self.menuUsers_Lists.setObjectName("menuUsers_Lists")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        YouTubeOutside.setMenuBar(self.menubar)
        self.actionAbout_Outside_YT = QtWidgets.QAction(YouTubeOutside)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionAbout_Outside_YT.setFont(font)
        self.actionAbout_Outside_YT.setObjectName("actionAbout_Outside_YT")
        self.actionUploaders = QtWidgets.QAction(YouTubeOutside)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionUploaders.setFont(font)
        self.actionUploaders.setObjectName("actionUploaders")
        self.actionWatchers = QtWidgets.QAction(YouTubeOutside)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionWatchers.setFont(font)
        self.actionWatchers.setObjectName("actionWatchers")
        self.actionOpen_Main_Folder = QtWidgets.QAction(YouTubeOutside)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionOpen_Main_Folder.setFont(font)
        self.actionOpen_Main_Folder.setObjectName("actionOpen_Main_Folder")
        self.actionUpdate_sheet = QtWidgets.QAction(YouTubeOutside)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionUpdate_sheet.setFont(font)
        self.actionUpdate_sheet.setObjectName("actionUpdate_sheet")
        self.actionUploaders_2 = QtWidgets.QAction(YouTubeOutside)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionUploaders_2.setFont(font)
        self.actionUploaders_2.setObjectName("actionUploaders_2")
        self.actionWatchers_2 = QtWidgets.QAction(YouTubeOutside)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.actionWatchers_2.setFont(font)
        self.actionWatchers_2.setObjectName("actionWatchers_2")
        self.actionUpdate_Settings = QtWidgets.QAction(YouTubeOutside)
        self.actionUpdate_Settings.setObjectName("actionUpdate_Settings")
        self.actionDownloaders = QtWidgets.QAction(YouTubeOutside)
        self.actionDownloaders.setObjectName("actionDownloaders")
        self.menuOutside_YouTube.addSeparator()
        self.menuOutside_YouTube.addAction(self.actionOpen_Main_Folder)
        self.menuHelp.addAction(self.actionAbout_Outside_YT)
        self.menuUsers_Lists.addAction(self.actionUploaders_2)
        self.menuUsers_Lists.addSeparator()
        self.menuUsers_Lists.addAction(self.actionWatchers_2)
        self.menuSettings.addAction(self.actionUpdate_Settings)
        self.menubar.addAction(self.menuUsers_Lists.menuAction())
        self.menubar.addAction(self.menuOutside_YouTube.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(YouTubeOutside)
        self.OutsideYT.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(YouTubeOutside)

    def retranslateUi(self, YouTubeOutside):
        _translate = QtCore.QCoreApplication.translate
        YouTubeOutside.setWindowTitle(_translate("YouTubeOutside", "Outside YouTube"))
        self.Upload_SelectAll_CheckBox.setText(_translate("YouTubeOutside", "Select All"))
        self.Upload_Check_Button.setText(_translate("YouTubeOutside", "Check"))
        self.Upload_UploadTime_Button.setText(_translate("YouTubeOutside", "  Upload Time  "))
        self.Upload_ClearUTime_Button.setText(_translate("YouTubeOutside", " Clear Upload Time "))
        self.Upload_SelectVideos_Button.setText(_translate("YouTubeOutside", "  Select Videos  "))
        self.Upload_delete_after_upload_checkBox.setText(_translate("YouTubeOutside", "Delete after upload"))
        self.Upload_ShowBrowser_checkBox.setText(_translate("YouTubeOutside", "Show Browsers"))
        self.Upload_Start.setText(_translate("YouTubeOutside", "Start"))
        self.OutsideYT.setTabText(self.OutsideYT.indexOf(self.UploadPage), _translate("YouTubeOutside", "Upload"))
        self.Watch_SelectAll_CheckBox.setText(_translate("YouTubeOutside", "Select All"))
        self.Watch_url_label.setText(_translate("YouTubeOutside", "Url: "))
        self.Watch_url_add_Button.setText(_translate("YouTubeOutside", "Add"))
        self.Watch_SelectVideos_Button.setText(_translate("YouTubeOutside", "  Select Videos  "))
        self.Watch_ShowBrowser_checkBox.setText(_translate("YouTubeOutside", "Show Browsers"))
        self.Watch_advanced_settings_Button.setText(_translate("YouTubeOutside", "  Advanced Settings  "))
        self.Watch_Start.setText(_translate("YouTubeOutside", "Start"))
        self.OutsideYT.setTabText(self.OutsideYT.indexOf(self.WatchPage), _translate("YouTubeOutside", "Watch"))
        self.Download_SelectAll_CheckBox.setText(_translate("YouTubeOutside", "Select All"))
        self.Download_url_label.setText(_translate("YouTubeOutside", "Url:"))
        self.Download_url_add_Button.setText(_translate("YouTubeOutside", "Add"))
        self.Download_Save_to_label.setText(_translate("YouTubeOutside", "Save to"))
        self.Download_User_Save_Mode_radioButton.setText(_translate("YouTubeOutside", "User"))
        self.Download_Folder_Save_Mode_radioButton.setText(_translate("YouTubeOutside", "Folder"))
        self.Download_Select_Path_Button.setText(_translate("YouTubeOutside", "Select Path"))
        self.Download_SelectVideos_Button.setText(_translate("YouTubeOutside", "  Select Videos  "))
        self.Download_Info_checkBox.setText(_translate("YouTubeOutside", "Download Video Info"))
        self.Download_Video_checkBox.setText(_translate("YouTubeOutside", "Download Video"))
        self.Download_advanced_settings_Button.setText(_translate("YouTubeOutside", "Advanced Settings"))
        self.Download_Start.setText(_translate("YouTubeOutside", "Start"))
        self.OutsideYT.setTabText(self.OutsideYT.indexOf(self.DownloadPage), _translate("YouTubeOutside", "Download"))
        self.menuOutside_YouTube.setTitle(_translate("YouTubeOutside", "Shortcuts"))
        self.menuHelp.setTitle(_translate("YouTubeOutside", "Help"))
        self.menuUsers_Lists.setTitle(_translate("YouTubeOutside", "Users Lists"))
        self.menuSettings.setTitle(_translate("YouTubeOutside", "Settings"))
        self.actionAbout_Outside_YT.setText(_translate("YouTubeOutside", "About Outside YT"))
        self.actionUploaders.setText(_translate("YouTubeOutside", "Uploaders"))
        self.actionWatchers.setText(_translate("YouTubeOutside", "Watchers"))
        self.actionOpen_Main_Folder.setText(_translate("YouTubeOutside", "Open Main Folder (Ctrl+Shift+E)"))
        self.actionUpdate_sheet.setText(_translate("YouTubeOutside", "Update Page (F5)"))
        self.actionUploaders_2.setText(_translate("YouTubeOutside", "Uploaders"))
        self.actionWatchers_2.setText(_translate("YouTubeOutside", "Watchers"))
        self.actionUpdate_Settings.setText(_translate("YouTubeOutside", "Update Settings"))
        self.actionDownloaders.setText(_translate("YouTubeOutside", "Downloaders"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    YouTubeOutside = QtWidgets.QMainWindow()
    ui = Ui_YouTubeOutside()
    ui.setupUi(YouTubeOutside)
    YouTubeOutside.show()
    sys.exit(app.exec_())
