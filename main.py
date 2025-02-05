# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import os
import time
import shutil
import random
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import math


class Ui_MainWindow(object):
    working_directory = ""
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(400, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 360, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setEnabled(True)
        self.comboBox.setGeometry(QtCore.QRect(50, 200, 300, 30))
        self.comboBox.setMouseTracking(True)
        self.comboBox.setTabletTracking(False)
        self.comboBox.setAutoFillBackground(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 300, 300, 30))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 250, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(125, 40, 150, 130))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("gear.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 26))
        self.menubar.setObjectName("menubar")
        self.menuYfcnhjqrb = QtWidgets.QMenu(self.menubar)
        self.menuYfcnhjqrb.setObjectName("menuYfcnhjqrb")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setCheckable(False)
        self.action.setObjectName("action")
        self.menuYfcnhjqrb.addAction(self.action)
        self.menubar.addAction(self.menuYfcnhjqrb.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.processing()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "App"))
        self.pushButton.setText(_translate("MainWindow", "Запуск"))
        self.comboBox.setItemText(0, _translate("MainWindow", "v1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "v2"))
        self.label.setText(_translate("MainWindow", "Нажмите \'Запуск\' для начла"))
        self.menuYfcnhjqrb.setTitle(_translate("MainWindow", "Настройки"))
        self.action.setText(_translate("MainWindow", "Путь.."))

    def processing(self):
        """
        Обработчик событий
        :return: -
        """
        self.action.triggered.connect(lambda: self.define_directory())
        self.pushButton.clicked.connect(lambda: self.work())

    def define_directory(self):
        """
        СОхраняет рабочую директорию, определяемую юзером
        :return: -
        """
        self.working_directory = QFileDialog.getExistingDirectory()

    def find_pair(self, lb: str):
        """
        Находит не обработанные файлы в директории
        :lb: метка, добавляемая к файлу
        :return: list с именами не обработанных файлов
        """
        _files = [str(elem) for elem in os.listdir(self.working_directory) if "_new_" not in str(elem)]
        _new = [str(elem) for elem in os.listdir(self.working_directory) if "_new_" in str(elem)]
        print(_files, _new)
        whitelist = []
        for i in _files:
            for j in _new:
                if f"{i[:-4]}_new_" in j:
                    whitelist.append(i)
        print(whitelist)
        return [elem for elem in os.listdir(self.working_directory) if elem not in whitelist and "_new_" not in elem
                and lb in elem]

    def work(self):
        if self.working_directory == "":
            self.label.setText("Выберите рабочую директорию!")
        else:
            self.label.setText("Подготовка... Ничего не нажимайте!")
            files = self.find_pair(self.comboBox.currentText())
            for i in range(len(files)):
                # отображаем прогресс текстом
                self.label.setText(f"Обработано {i + 1} из {len(files)} файлов")
                # делаем копию обрабатываемых файлов
                new_path_file = f'{self.working_directory}/{files[i][:-4]}' \
                                f'_new_{str(datetime.datetime.utcnow()).replace(":", ".")[:19]}.txt'
                shutil.copyfile(f'{self.working_directory}/{files[i]}', new_path_file)
                # обрабатываем файлы
                f = open(new_path_file, "w")
                f.write(f"{str(random.randint(0, 1000))} {'v1' if files[i].count('v1') != 0 else 'v2'}")
                f.close()
                # отображаем прогресс прогрессбаром
                self.progressBar.setValue(math.ceil((i+1)/len(files)*100))
                time.sleep(1)

            self.label.setText("Все файлы обработаны!")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
