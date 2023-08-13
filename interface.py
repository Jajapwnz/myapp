from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1184, 657)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)



        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")

        # Создаем вкладку "принято на хранение"
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setStyleSheet("")
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.tableWidget = QtWidgets.QTableWidget(self.tab_1)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setVisible(False)


        # Задаем горизонтальные заголовки и растягиваем столбцы
        horizontal_headers = ["код", "наименование", "количество", "единица измерения", "дата", "документ",
                              "место хранения", "до", "контакты"]
        self.tableWidget.setHorizontalHeaderLabels(horizontal_headers)
        for column in range(self.tableWidget.columnCount()):
            self.tableWidget.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: grey }")

        self.gridLayout_4.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "принято на хранение")

        # Создаем вкладку "возвращено"
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(9)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.verticalHeader().setVisible(False)

        # Задаем горизонтальные заголовки и растягиваем столбцы
        self.tableWidget_3.setHorizontalHeaderLabels(horizontal_headers)
        for column in range(self.tableWidget_3.columnCount()):
            self.tableWidget_3.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        self.tableWidget_3.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: grey }")

        self.gridLayout_3.addWidget(self.tableWidget_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "возвращено")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "поиск..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "принято на хранение"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "возвращено"))




