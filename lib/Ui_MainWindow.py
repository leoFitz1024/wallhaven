# -*- coding: utf-8 -*-
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QIcon
from PyQt5.QtWidgets import QMessageBox, QMainWindow

from lib.Wallhaven import Wallhaven


class Ui_MainWindow(QMainWindow):

    def __init__(self, mainExe: Wallhaven):
        super(Ui_MainWindow, self).__init__()
        self.purity_item_map = {}
        self.category_item_map = {}
        self.sorting_item_map = {}
        self.ratios_item_map = {}
        self.time_item_map = {}
        self.mainExe = mainExe
        # temp config
        self.temp_auto_run = 0
        self.config_is_changed = False
        self.temp_purity = 0b110
        self.temp_categories = 0b111
        self.temp_top_range = 3
        self.temp_sorting = "Random"
        self.temp_ratios_list = set([])
        self.temp_schedule_time = 0
        self.temp_images_dir = None

    def init_Ui(self):
        self.setObjectName("MainWindow")
        self.resize(393, 483)
        self.setMaximumSize(QtCore.QSize(393, 483))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(393, 483))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setStyleSheet("background-color:rgb(249, 249, 249)")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.img_set_table = QtWidgets.QWidget()
        self.img_set_table.setObjectName("img_set_table")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.img_set_table)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.purity_box = QtWidgets.QGroupBox(self.img_set_table)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.purity_box.setFont(font)
        self.purity_box.setFocusPolicy(QtCore.Qt.NoFocus)
        self.purity_box.setObjectName("purity_box")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.purity_box)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(9, 9, -1, -1)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.purity_sfw = QtWidgets.QCheckBox(self.purity_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.purity_sfw.setFont(font)
        self.purity_sfw.setFocusPolicy(QtCore.Qt.NoFocus)
        self.purity_sfw.setChecked(False)
        self.purity_sfw.setObjectName("purity_sfw")
        self.horizontalLayout.addWidget(self.purity_sfw)
        self.purity_sketchy = QtWidgets.QCheckBox(self.purity_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.purity_sketchy.setFont(font)
        self.purity_sketchy.setFocusPolicy(QtCore.Qt.NoFocus)
        self.purity_sketchy.setObjectName("purity_sketchy")
        self.horizontalLayout.addWidget(self.purity_sketchy)
        self.gridLayout_5.addWidget(self.purity_box, 0, 0, 1, 1)
        self.category_box = QtWidgets.QGroupBox(self.img_set_table)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.category_box.setFont(font)
        self.category_box.setFocusPolicy(QtCore.Qt.NoFocus)
        self.category_box.setObjectName("category_box")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.category_box)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cate_general = QtWidgets.QCheckBox(self.category_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.cate_general.setFont(font)
        self.cate_general.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cate_general.setChecked(False)
        self.cate_general.setObjectName("cate_general")
        self.horizontalLayout_2.addWidget(self.cate_general)
        self.cate_anime = QtWidgets.QCheckBox(self.category_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.cate_anime.setFont(font)
        self.cate_anime.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cate_anime.setChecked(False)
        self.cate_anime.setObjectName("cate_anime")
        self.horizontalLayout_2.addWidget(self.cate_anime)
        self.cate_people = QtWidgets.QCheckBox(self.category_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.cate_people.setFont(font)
        self.cate_people.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cate_people.setObjectName("cate_people")
        self.horizontalLayout_2.addWidget(self.cate_people)
        self.gridLayout_5.addWidget(self.category_box, 1, 0, 1, 1)
        self.sorting_box = QtWidgets.QGroupBox(self.img_set_table)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sorting_box.setFont(font)
        self.sorting_box.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sorting_box.setObjectName("sorting_box")
        self.gridLayout = QtWidgets.QGridLayout(self.sorting_box)
        self.gridLayout.setObjectName("gridLayout")
        self.sorting_views = QtWidgets.QRadioButton(self.sorting_box)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sorting_views.setFont(font)
        self.sorting_views.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sorting_views.setObjectName("sorting_views")
        self.gridLayout.addWidget(self.sorting_views, 0, 1, 1, 1)
        self.sorting_favorites = QtWidgets.QRadioButton(self.sorting_box)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sorting_favorites.setFont(font)
        self.sorting_favorites.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sorting_favorites.setObjectName("sorting_favorites")
        self.gridLayout.addWidget(self.sorting_favorites, 1, 1, 1, 1)
        self.sorting_hot = QtWidgets.QRadioButton(self.sorting_box)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sorting_hot.setFont(font)
        self.sorting_hot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sorting_hot.setObjectName("sorting_hot")
        self.gridLayout.addWidget(self.sorting_hot, 1, 2, 1, 1)
        self.sorting_toplist = QtWidgets.QRadioButton(self.sorting_box)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sorting_toplist.setFont(font)
        self.sorting_toplist.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sorting_toplist.setChecked(True)
        self.sorting_toplist.setObjectName("sorting_toplist")
        self.gridLayout.addWidget(self.sorting_toplist, 2, 0, 1, 1)
        self.top_range_box = QtWidgets.QComboBox(self.sorting_box)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.top_range_box.setFont(font)
        self.top_range_box.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.top_range_box.setStyleSheet("QComboBox {\n"
                                         "     border:1px solid gray;\n"
                                         "     border-radius: 3px;\n"
                                         "     padding:1px 2px 1px 2px;\n"
                                         "     min-width:9em;\n"
                                         "}\n"
                                         "QComboBox::drop-down {\n"
                                         "     subcontrol-origin:padding;\n"
                                         "     subcontrol- position:top right;\n"
                                         "     width:20px;\n"
                                         "     border-left-width:1px;\n"
                                         "     border-left-color:darkgray;\n"
                                         "     border-left-style:solid;  /* just a single line */\n"
                                         "     border-top-right-radius:3px;  /* same radius as the QComboBox */\n"
                                         "     border-bottom-right-radius:3px;\n"
                                         "}\n"
                                         " \n"
                                         "QComboBox::down-arrow {\n"
                                         "     image:url(icon/down_arrow.png);\n"
                                         "    width: 15px;\n"
                                         "    height:15px;\n"
                                         "}")
        self.top_range_box.setObjectName("top_range_box")
        self.top_range_box.addItem("")
        self.top_range_box.addItem("")
        self.top_range_box.addItem("")
        self.top_range_box.addItem("")
        self.top_range_box.addItem("")
        self.top_range_box.addItem("")
        self.top_range_box.addItem("")
        self.gridLayout.addWidget(self.top_range_box, 2, 1, 1, 1)
        self.sorting_data_added = QtWidgets.QRadioButton(self.sorting_box)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sorting_data_added.setFont(font)
        self.sorting_data_added.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sorting_data_added.setObjectName("sorting_data_added")
        self.gridLayout.addWidget(self.sorting_data_added, 0, 2, 1, 1)
        self.sorting_relevance = QtWidgets.QRadioButton(self.sorting_box)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sorting_relevance.setFont(font)
        self.sorting_relevance.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sorting_relevance.setObjectName("sorting_relevance")
        self.gridLayout.addWidget(self.sorting_relevance, 0, 0, 1, 1)
        self.sorting_random = QtWidgets.QRadioButton(self.sorting_box)
        font = QtGui.QFont()
        font.setFamily("Bell MT")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sorting_random.setFont(font)
        self.sorting_random.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sorting_random.setObjectName("sorting_random")
        self.gridLayout.addWidget(self.sorting_random, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.sorting_box, 2, 0, 1, 1)
        self.ratios_box = QtWidgets.QGroupBox(self.img_set_table)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratios_box.setFont(font)
        self.ratios_box.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratios_box.setObjectName("ratios_box")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.ratios_box)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.ratio_10x9 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_10x9.setFont(font)
        self.ratio_10x9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_10x9.setObjectName("ratio_10x9")
        self.gridLayout_2.addWidget(self.ratio_10x9, 1, 0, 1, 1)
        self.ratio_48x9 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_48x9.setFont(font)
        self.ratio_48x9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_48x9.setObjectName("ratio_48x9")
        self.gridLayout_2.addWidget(self.ratio_48x9, 2, 1, 1, 1)
        self.ratio_10x16 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_10x16.setFont(font)
        self.ratio_10x16.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_10x16.setObjectName("ratio_10x16")
        self.gridLayout_2.addWidget(self.ratio_10x16, 2, 2, 1, 1)
        self.ratio_3x2 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_3x2.setFont(font)
        self.ratio_3x2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_3x2.setObjectName("ratio_3x2")
        self.gridLayout_2.addWidget(self.ratio_3x2, 1, 3, 1, 1)
        self.ratio_9x16 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_9x16.setFont(font)
        self.ratio_9x16.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_9x16.setObjectName("ratio_9x16")
        self.gridLayout_2.addWidget(self.ratio_9x16, 0, 2, 1, 1)
        self.ratio_5x4 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_5x4.setFont(font)
        self.ratio_5x4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_5x4.setObjectName("ratio_5x4")
        self.gridLayout_2.addWidget(self.ratio_5x4, 3, 3, 1, 1)
        self.ratio_4x3 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_4x3.setFont(font)
        self.ratio_4x3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_4x3.setObjectName("ratio_4x3")
        self.gridLayout_2.addWidget(self.ratio_4x3, 2, 3, 1, 1)
        self.ratio_1x1 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_1x1.setFont(font)
        self.ratio_1x1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_1x1.setObjectName("ratio_1x1")
        self.gridLayout_2.addWidget(self.ratio_1x1, 0, 3, 1, 1)
        self.ratio_21x9 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_21x9.setFont(font)
        self.ratio_21x9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_21x9.setObjectName("ratio_21x9")
        self.gridLayout_2.addWidget(self.ratio_21x9, 0, 1, 1, 1)
        self.ratio_16x9 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_16x9.setFont(font)
        self.ratio_16x9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_16x9.setObjectName("ratio_16x9")
        self.gridLayout_2.addWidget(self.ratio_16x9, 0, 0, 1, 1)
        self.ratio_32x9 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_32x9.setFont(font)
        self.ratio_32x9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_32x9.setObjectName("ratio_32x9")
        self.gridLayout_2.addWidget(self.ratio_32x9, 1, 1, 1, 1)
        self.ratio_9x18 = QtWidgets.QCheckBox(self.ratios_box)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ratio_9x18.setFont(font)
        self.ratio_9x18.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ratio_9x18.setObjectName("ratio_9x18")
        self.gridLayout_2.addWidget(self.ratio_9x18, 1, 2, 1, 1)
        self.gridLayout_5.addWidget(self.ratios_box, 3, 0, 1, 1)
        self.tabWidget.addTab(self.img_set_table, "")
        self.sys_set_tab = QtWidgets.QWidget()
        self.sys_set_tab.setObjectName("sys_set_tab")
        self.groupBox = QtWidgets.QGroupBox(self.sys_set_tab)
        self.groupBox.setGeometry(QtCore.QRect(9, 41, 351, 91))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.time_10m = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.time_10m.setFont(font)
        self.time_10m.setFocusPolicy(QtCore.Qt.NoFocus)
        self.time_10m.setObjectName("time_10m")
        self.gridLayout_3.addWidget(self.time_10m, 0, 1, 1, 1)
        self.time_30m = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.time_30m.setFont(font)
        self.time_30m.setFocusPolicy(QtCore.Qt.NoFocus)
        self.time_30m.setObjectName("time_30m")
        self.gridLayout_3.addWidget(self.time_30m, 0, 2, 1, 1)
        self.time_3h = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.time_3h.setFont(font)
        self.time_3h.setFocusPolicy(QtCore.Qt.NoFocus)
        self.time_3h.setObjectName("time_3h")
        self.gridLayout_3.addWidget(self.time_3h, 1, 1, 1, 1)
        self.time_1h = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.time_1h.setFont(font)
        self.time_1h.setFocusPolicy(QtCore.Qt.NoFocus)
        self.time_1h.setObjectName("time_1h")
        self.gridLayout_3.addWidget(self.time_1h, 1, 0, 1, 1)
        self.time_close = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.time_close.setFont(font)
        self.time_close.setFocusPolicy(QtCore.Qt.NoFocus)
        self.time_close.setChecked(True)
        self.time_close.setObjectName("time_close")
        self.gridLayout_3.addWidget(self.time_close, 0, 0, 1, 1)
        self.time_5h = QtWidgets.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.time_5h.setFont(font)
        self.time_5h.setFocusPolicy(QtCore.Qt.NoFocus)
        self.time_5h.setObjectName("time_5h")
        self.gridLayout_3.addWidget(self.time_5h, 1, 2, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.sys_set_tab)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 140, 351, 101))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.img_path_label = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.img_path_label.setFont(font)
        self.img_path_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.img_path_label.setObjectName("img_path_label")
        self.horizontalLayout_4.addWidget(self.img_path_label)
        self.img_path = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.img_path.setFont(font)
        self.img_path.setFocusPolicy(QtCore.Qt.TabFocus)
        self.img_path.setObjectName("img_path")
        self.horizontalLayout_4.addWidget(self.img_path)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.err_path_tip = QtWidgets.QLabel(self.groupBox_2)
        self.err_path_tip.setEnabled(True)
        self.err_path_tip.hide()
        self.err_path_tip.setStyleSheet("color:rgb(255, 105, 5)")
        self.err_path_tip.setAlignment(QtCore.Qt.AlignCenter)
        self.err_path_tip.setWordWrap(False)
        self.err_path_tip.setObjectName("err_path_tip")
        self.verticalLayout.addWidget(self.err_path_tip)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.open_dir_btn = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.open_dir_btn.setFont(font)
        self.open_dir_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.open_dir_btn.setStyleSheet("\n"
                                        "QPushButton\n"
                                        "{\n"
                                        "    background-color: #ffffff; /*背景色*/ \n"
                                        "    border-style: outset;\n"
                                        "    border-width: 1px;\n"
                                        "    border-radius:3px; /*边界圆滑*/\n"
                                        "    border-color: rgb(189, 188, 191);\n"
                                        "    color:black; /*字体颜色*/\n"
                                        "    padding: 2px;\n"
                                        "}\n"
                                        " \n"
                                        "QPushButton:hover\n"
                                        "{\n"
                                        "    background-color: rgb(226, 241, 249);\n"
                                        "    border-width: 1px;\n"
                                        "    border-color: rgb(40, 99, 142);\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed\n"
                                        "{\n"
                                        "    background-color: #ffffff; /*伪状态经过时背景色*/ \n"
                                        "    border-style: inset;\n"
                                        "}\n"
                                        "")
        self.open_dir_btn.setAutoDefault(False)
        self.open_dir_btn.setDefault(False)
        self.open_dir_btn.setFlat(False)
        self.open_dir_btn.setObjectName("open_dir_btn")
        self.horizontalLayout_3.addWidget(self.open_dir_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.change_dir_btn = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change_dir_btn.sizePolicy().hasHeightForWidth())
        self.change_dir_btn.setSizePolicy(sizePolicy)
        self.change_dir_btn.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.change_dir_btn.setFont(font)
        self.change_dir_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.change_dir_btn.setStyleSheet("\n"
                                          "QPushButton\n"
                                          "{\n"
                                          "    background-color: #ffffff; /*背景色*/ \n"
                                          "    border-style: outset;\n"
                                          "    border-width: 1px;\n"
                                          "    border-radius:3px; /*边界圆滑*/\n"
                                          "    border-color: rgb(189, 188, 191);\n"
                                          "    color:black; /*字体颜色*/\n"
                                          "    padding: 2px;\n"
                                          "}\n"
                                          " \n"
                                          "QPushButton:hover\n"
                                          "{\n"
                                          "    background-color: rgb(226, 241, 249);\n"
                                          "    border-width: 1px;\n"
                                          "    border-color: rgb(40, 99, 142);\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:pressed\n"
                                          "{\n"
                                          "    background-color: #ffffff; /*伪状态经过时背景色*/ \n"
                                          "    border-style: inset;\n"
                                          "}\n"
                                          "")
        self.change_dir_btn.setObjectName("change_dir_btn")
        self.horizontalLayout_3.addWidget(self.change_dir_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.sys_set_tab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.autoRun = QtWidgets.QCheckBox(self.sys_set_tab)
        self.autoRun.setGeometry(QtCore.QRect(10, 10, 91, 16))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.autoRun.setFont(font)
        self.autoRun.setObjectName("autoRun")
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setIcon(self, icon: QIcon):
        self.setWindowIcon(icon)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "wallhaven v1.0"))
        self.purity_box.setTitle(_translate("MainWindow", "内容筛选"))
        self.purity_sfw.setToolTip(_translate("MainWindow", "正经图片"))
        self.purity_sfw.setText(_translate("MainWindow", "SFW"))
        self.purity_sketchy.setToolTip(_translate("MainWindow", "带点颜色"))
        self.purity_sketchy.setText(_translate("MainWindow", "Sketchy"))
        self.category_box.setTitle(_translate("MainWindow", "风格选择"))
        self.cate_general.setText(_translate("MainWindow", "普通"))
        self.cate_anime.setText(_translate("MainWindow", "二次元"))
        self.cate_people.setText(_translate("MainWindow", "三次元"))
        self.sorting_box.setTitle(_translate("MainWindow", "排序方式"))
        self.sorting_views.setText(_translate("MainWindow", "Views"))
        self.sorting_favorites.setText(_translate("MainWindow", "Favorites"))
        self.sorting_hot.setText(_translate("MainWindow", "Hot"))
        self.sorting_toplist.setText(_translate("MainWindow", "Toplist"))
        self.top_range_box.setItemText(0, _translate("MainWindow", "Last Day"))
        self.top_range_box.setItemText(1, _translate("MainWindow", "Last 3 Days"))
        self.top_range_box.setItemText(2, _translate("MainWindow", "Last Week"))
        self.top_range_box.setItemText(3, _translate("MainWindow", "Last Month"))
        self.top_range_box.setItemText(4, _translate("MainWindow", "Last 3 Months"))
        self.top_range_box.setItemText(5, _translate("MainWindow", "Last 6 Months"))
        self.top_range_box.setItemText(6, _translate("MainWindow", "Last Year"))
        self.sorting_data_added.setText(_translate("MainWindow", "Date Added"))
        self.sorting_relevance.setText(_translate("MainWindow", "Relevance"))
        self.sorting_random.setText(_translate("MainWindow", "Random"))
        self.ratios_box.setTitle(_translate("MainWindow", "图片比例"))
        self.ratio_10x9.setText(_translate("MainWindow", "10x9"))
        self.ratio_48x9.setText(_translate("MainWindow", "48x9"))
        self.ratio_10x16.setText(_translate("MainWindow", "10x16"))
        self.ratio_3x2.setText(_translate("MainWindow", "3x2"))
        self.ratio_9x16.setText(_translate("MainWindow", "9x16"))
        self.ratio_5x4.setText(_translate("MainWindow", "5x4"))
        self.ratio_4x3.setText(_translate("MainWindow", "4x3"))
        self.ratio_1x1.setText(_translate("MainWindow", "1x1"))
        self.ratio_21x9.setText(_translate("MainWindow", "21x9"))
        self.ratio_16x9.setText(_translate("MainWindow", "16x9"))
        self.ratio_32x9.setText(_translate("MainWindow", "32x9"))
        self.ratio_9x18.setText(_translate("MainWindow", "9x18"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.img_set_table), _translate("MainWindow", "图片设置"))
        self.groupBox.setTitle(_translate("MainWindow", "定时切换"))
        self.time_10m.setText(_translate("MainWindow", "10分钟"))
        self.time_30m.setText(_translate("MainWindow", "30分钟"))
        self.time_3h.setText(_translate("MainWindow", "3小时"))
        self.time_1h.setText(_translate("MainWindow", "1小时"))
        self.time_close.setText(_translate("MainWindow", "关闭"))
        self.time_5h.setText(_translate("MainWindow", "5小时"))
        self.groupBox_2.setTitle(_translate("MainWindow", "图片存储位置"))
        self.img_path_label.setText(_translate("MainWindow", "路径："))
        self.err_path_tip.setText(_translate("MainWindow", "配置文件中路径不合法，已使用默认路径。"))
        self.open_dir_btn.setText(_translate("MainWindow", "打开路径"))
        self.change_dir_btn.setText(_translate("MainWindow", "更改"))
        self.autoRun.setText(_translate("MainWindow", "开机自启"))
        self.autoRun.hide()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sys_set_tab), _translate("MainWindow", "系统设置"))
        self.load_Controls()
        self.bindEvent()

    def show_ui(self):
        self.init_ui_by_config()
        self.show()

    def load_Controls(self):
        # add purity
        self.purity_item_map[self.purity_sketchy.text()] = self.purity_sketchy
        self.purity_item_map[self.purity_sfw.text()] = self.purity_sfw
        # add category
        self.category_item_map[self.cate_general.text()] = self.cate_general
        self.category_item_map[self.cate_anime.text()] = self.cate_anime
        self.category_item_map[self.cate_people.text()] = self.cate_people
        # add sorting
        self.sorting_item_map[self.sorting_hot.text()] = self.sorting_hot
        self.sorting_item_map[self.sorting_random.text()] = self.sorting_random
        self.sorting_item_map[self.sorting_relevance.text()] = self.sorting_relevance
        self.sorting_item_map[self.sorting_toplist.text()] = self.sorting_toplist
        self.sorting_item_map[self.sorting_views.text()] = self.sorting_views
        self.sorting_item_map[self.sorting_favorites.text()] = self.sorting_favorites
        # add ratios
        self.ratios_item_map[self.ratio_16x9.text()] = self.ratio_16x9
        self.ratios_item_map[self.ratio_10x9.text()] = self.ratio_10x9
        self.ratios_item_map[self.ratio_21x9.text()] = self.ratio_21x9
        self.ratios_item_map[self.ratio_32x9.text()] = self.ratio_32x9
        self.ratios_item_map[self.ratio_48x9.text()] = self.ratio_48x9
        self.ratios_item_map[self.ratio_9x16.text()] = self.ratio_9x16
        self.ratios_item_map[self.ratio_9x18.text()] = self.ratio_9x18
        self.ratios_item_map[self.ratio_10x16.text()] = self.ratio_10x16
        self.ratios_item_map[self.ratio_1x1.text()] = self.ratio_1x1
        self.ratios_item_map[self.ratio_3x2.text()] = self.ratio_3x2
        self.ratios_item_map[self.ratio_4x3.text()] = self.ratio_4x3
        self.ratios_item_map[self.ratio_5x4.text()] = self.ratio_5x4
        # add time
        self.time_item_map[self.time_close.text()] = self.time_close
        self.time_item_map[self.time_10m.text()] = self.time_10m
        self.time_item_map[self.time_30m.text()] = self.time_30m
        self.time_item_map[self.time_1h.text()] = self.time_1h
        self.time_item_map[self.time_3h.text()] = self.time_3h
        self.time_item_map[self.time_5h.text()] = self.time_5h

    def bindEvent(self):
        """绑定事件"""
        self.open_dir_btn.clicked.connect(self.open_img_dir)
        self.change_dir_btn.clicked.connect(self.change_img_dir)
        self.top_range_box.currentIndexChanged.connect(self.change_top_range)
        # self.autoRun.stateChanged.connect(self.change_auto_run)

        for purity_item in self.purity_item_map.values():
            purity_item.stateChanged.connect(self.change_purity)

        for category_item in self.category_item_map.values():
            category_item.stateChanged.connect(self.change_category)

        for sorting_item in self.sorting_item_map.values():
            sorting_item.toggled.connect(self.change_sorting)

        for ratios_item in self.ratios_item_map.values():
            ratios_item.stateChanged.connect(self.change_ratio)

        for time_item in self.time_item_map.values():
            time_item.toggled.connect(self.change_time)

    def init_ui_by_config(self):
        if self.mainExe.error_path:
            self.err_path_tip.show()
        else:
            self.err_path_tip.hide()
        # load purity
        if (self.mainExe.purity >> 2) & 1 == 1:
            self.purity_sfw.setChecked(True)
        if (self.mainExe.purity >> 1) & 1 == 1:
            self.purity_sketchy.setChecked(True)

        # load category
        if (self.mainExe.categories >> 2) & 1 == 1:
            self.cate_general.setChecked(True)
        if (self.mainExe.categories >> 1) & 1 == 1:
            self.cate_anime.setChecked(True)
        if self.mainExe.categories & 1 == 1:
            self.cate_people.setChecked(True)

        # load sorting
        self.sorting_item_map[self.mainExe.sorting].setChecked(True)
        self.top_range_box.setCurrentIndex(self.mainExe.top_range)
        if self.mainExe.sorting == "Toplist":
            self.top_range_box.show()
        else:
            self.top_range_box.hide()

        # load ratios
        for ratio in self.mainExe.ratios_list:
            self.ratios_item_map[ratio].setChecked(True)

        # load auto run
        if self.mainExe.auto_run == 1:
            self.autoRun.setChecked(True)

        # load time
        if self.mainExe.schedule_time == 0:
            self.time_close.setChecked(True)
        if self.mainExe.schedule_time == 600:
            self.time_10m.setChecked(True)
        if self.mainExe.schedule_time == 1800:
            self.time_30m.setChecked(True)
        if self.mainExe.schedule_time == 3600:
            self.time_1h.setChecked(True)
        if self.mainExe.schedule_time == 10800:
            self.time_3h.setChecked(True)
        if self.mainExe.schedule_time == 18000:
            self.time_5h.setChecked(True)

        # load img_dir
        self.temp_images_dir = self.mainExe.images_dir
        fontMetrics = QFontMetrics(self.img_path.font())
        if fontMetrics.width(self.mainExe.images_dir) > 277:
            strDes = QFontMetrics(self.img_path.font()).elidedText(self.mainExe.images_dir, Qt.ElideMiddle,
                                                                   275)
            self.img_path.setText(strDes)
        else:
            self.img_path.setText(self.mainExe.images_dir)
        # self.img_path.setEnabled(False)

    def change_img_dir(self):
        self.hide_err_path_tips()
        images_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "选择文件夹",
                                                                self.mainExe.images_dir)  # 起始路径
        if images_dir != "":
            self.temp_images_dir = images_dir
            fontMetrics = QFontMetrics(self.img_path.font())
            if fontMetrics.width(self.temp_images_dir) > 277:
                strDes = QFontMetrics(self.img_path.font()).elidedText(self.temp_images_dir, Qt.ElideMiddle,
                                                                       275)
                self.img_path.setText(strDes)
            else:
                self.img_path.setText(self.temp_images_dir)

    def open_img_dir(self):
        self.hide_err_path_tips()
        if os.path.exists(self.mainExe.images_dir):
            os.startfile(self.mainExe.images_dir)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '文件夹不存在。')
            msg_box.exec_()

    def hide_err_path_tips(self):
        self.mainExe.error_path = False
        self.err_path_tip.hide()

    def change_top_range(self):
        """修改排序时间范围"""
        self.temp_top_range = self.top_range_box.currentIndex()

    def change_purity(self):
        """修改内容筛选触发"""
        curPurity = self.sender().text()
        isChecked = self.sender().isChecked()
        if curPurity == 'SFW':
            n = 2
        elif curPurity == 'Sketchy':
            n = 1
        else:
            n = 0
        if isChecked:
            self.temp_purity |= (1 << n)
        else:
            self.temp_purity &= ~(1 << n)
        if self.temp_purity == 0b000:
            self.temp_purity = 0b100
        # print('{:03b}'.format(self.mainExe.purity))

    def change_category(self):
        """修改类型筛选触发"""
        curCategory = self.sender().text()
        isChecked = self.sender().isChecked()
        if curCategory == '普通':
            n = 2
        elif curCategory == '二次元':
            n = 1
        else:
            n = 0
        if isChecked:
            self.temp_categories |= (1 << n)
        else:
            self.temp_categories &= ~(1 << n)
        if self.temp_categories == 0b000:
            self.temp_categories = 0b110
        # print('{:03b}'.format(self.mainExe.categories))

    def change_sorting(self):
        """修改排序触发"""
        curSorting = self.sender().text()
        isChecked = self.sender().isChecked()
        if isChecked:
            if curSorting == "Toplist":
                self.top_range_box.show()
            else:
                self.top_range_box.hide()
            self.temp_sorting = curSorting

    def change_ratio(self):
        """修改比例触发"""
        curRatio = self.sender().text()
        isChecked = self.sender().isChecked()
        if isChecked:
            self.temp_ratios_list.add(curRatio)
        if not isChecked:
            self.temp_ratios_list.remove(curRatio)

    def change_auto_run(self):
        """修改开机自启"""
        isChecked = self.sender().isChecked()
        if isChecked:
            self.temp_auto_run = 1
        if not isChecked:
            self.temp_auto_run = 0

    def change_time(self):
        """修改定时触发"""
        curTime = self.sender().text()
        isChecked = self.sender().isChecked()
        if isChecked:
            if "关闭" == curTime:
                self.temp_schedule_time = 0
            if "10分钟" == curTime:
                self.temp_schedule_time = 600
            if "30分钟" == curTime:
                self.temp_schedule_time = 1800
            if "1小时" == curTime:
                self.temp_schedule_time = 3600
            if "3小时" == curTime:
                self.temp_schedule_time = 10800
            if "5小时" == curTime:
                self.temp_schedule_time = 18000

    def check_change(self):
        """检查有没有修改配置"""
        if self.temp_purity != self.mainExe.purity:
            self.mainExe.purity = self.temp_purity
            self.config_is_changed = True
        if self.temp_categories != self.mainExe.categories:
            self.mainExe.categories = self.temp_categories
            self.config_is_changed = True
        if self.temp_sorting != self.mainExe.sorting:
            self.mainExe.sorting = self.temp_sorting
            self.config_is_changed = True
        if self.temp_top_range != self.mainExe.top_range:
            self.mainExe.top_range = self.temp_top_range
            self.config_is_changed = True
        if self.temp_ratios_list != self.mainExe.ratios_list:
            self.mainExe.ratios_list = self.temp_ratios_list.copy()
            self.config_is_changed = True
        if self.temp_auto_run != self.mainExe.auto_run:
            self.mainExe.auto_run = self.temp_auto_run
        if self.temp_schedule_time != self.mainExe.schedule_time:
            self.mainExe.schedule_time = self.temp_schedule_time
        if self.temp_images_dir != self.mainExe.images_dir:
            self.mainExe.images_dir = self.temp_images_dir
            self.config_is_changed = True
        return self.config_is_changed

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.hide_err_path_tips()
        if self.check_change():
            self.mainExe.images_ids = self.mainExe.images_ids[0:self.mainExe.current_bg_index]
        self.mainExe.do_schedule_time()
        self.mainExe.do_change_auto_run()
        self.mainExe.save_config()
