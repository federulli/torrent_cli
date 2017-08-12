from PyQt4 import QtGui, uic
import os
from gui.magnet_input_dialog import MagnetInputDialog
from PyQt4.QtCore import QTimer

headerNames = ["#", "Nombre", "Tamano", "Porcentaje", "Bajada", "Subida", "Seeds", "Peers", "Agregado", "Estado"]
gui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui")

from torrent.session import Session


class MainWindow:

    def __init__(self):
        self._window = uic.loadUi(os.path.join(gui_path, "mainwindow.ui"))
        self._magnet_input_dialog = MagnetInputDialog(self._window)
        self._table = self._window.torrent_table
        self._addMagnet = self._window.menuBar.findChild(QtGui.QMenu).actions()[0]
        self._addMagnet.triggered.connect(self._magnet_input_dialog.show)
        self._build_columns()
        self.tray = QtGui.QSystemTrayIcon(self._window)
        self.tray.show()
        self.tray.showMessage("prueba!!", "pepe")
        self._session = Session()
        self._timer = QTimer()
        self._timer.timeout.connect(self._timer_signal)
        self._timer.start(2)

    def _timer_signal(self):
        data = self._session.get_active_torrents_data()
        for x in range(0, len(data)):
            self.update_row(x, data[x])

    def _build_columns(self):
        self._table.setColumnCount(8)
        self._table.setHorizontalHeaderLabels(headerNames)

    def add_row(self, data):
        self._table.insertRow(self._table.rowCount())
        progress = QtGui.QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(0)
        self._table.setItem(self._table.rowCount() - 1, 1, QtGui.QTableWidgetItem(data["name"]))
        self._table.setCellWidget(self._table.rowCount() - 1, 3, progress)

    def update_row(self, index, data):
        if index >= self._table.rowCount():
            self.add_row(data)
        else:
            progress = self._table.cellWidget(index, 3)
            #progress.setValue(data["progress"])
            self._table.setItem(index, 4, QtGui.QTableWidgetItem(str(data["download_rate"])))
            self._table.setItem(index, 5, QtGui.QTableWidgetItem(data["upload_rate"]))
            self._table.setItem(index, 6, QtGui.QTableWidgetItem(data["seeds"]))
            self._table.setItem(index, 7, QtGui.QTableWidgetItem(data["peers"]))
            self._table.setItem(index, 9, QtGui.QTableWidgetItem(data["state"]))

    def show(self):
        self._window.show()

