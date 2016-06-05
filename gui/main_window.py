from PyQt4 import QtGui, uic
import os

headerNames = ["#", "Nombre", "Tamano", "Porcentaje", "Bajada", "Subida", "Seeds", "Peers", "Agregado", "Estado"]


class MainWindow():
    def __init__(self):
        self.__window = uic.loadUi('%s\ui\mainwindow.ui' % os.path.dirname(os.path.realpath(__file__)))
        self.__dialog = uic.loadUi('%s\ui\magnetinput.ui' % os.path.dirname(os.path.realpath(__file__)))
        self.__dialog.buttonBox.buttons()[0].clicked.connect(self.accept)
        self.__table = self.__window.torrent_table
        self.__addMagnet = self.__window.menuBar.children()[1].actions()[0]
        self.__build_columns()
        self.__build_menu()

    def __build_menu(self):
        self.__addMagnet.triggered.connect(self.on_add_magnet)

    def __build_columns(self):
        self.__table.setColumnCount(8)
        self.__table.setHorizontalHeaderLabels(headerNames)

    def on_add_magnet(self):
        self.__dialog.show()

    def accept(self):
        magent_uri = str(self.__dialog.magnetUri.toPlainText())
        print magent_uri

    def add_row(self, data):
        self.__table.insertRow(self.__table.rowCount())
        progress = QtGui.QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0)
        self.__table.setItem(self.__table.rowCount() - 1, 1, QtGui.QTableWidgetItem(data["name"]))
        self.__table.setCellWidget(self.__table.rowCount() - 1, 3, progress)

    def update_row(self, index, data):
        if index > self.__table.rowCount():
            self.add_row(data)
        else:
            progress = self.__table.cellWidget(index, 3)
            progress.setValue(data["progress"])
            self.__table.setItem(index, 4, QtGui.QTableWidgetItem(str(data["download_rate"])))
            self.__table.setItem(index, 5, QtGui.QTableWidgetItem(data["upload_rate"]))
            self.__table.setItem(index, 6, QtGui.QTableWidgetItem(data["seeds"]))
            self.__table.setItem(index, 7, QtGui.QTableWidgetItem(data["peers"]))
            self.__table.setItem(index, 9, QtGui.QTableWidgetItem(data["state"]))

    def show(self):
        self.__window.show()

