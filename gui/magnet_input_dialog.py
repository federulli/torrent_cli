from PyQt4 import QtGui, uic
from PyQt4.QtCore import QTimer
import os
from Tkinter import Tk
import re

import urllib

gui_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui")


class MagnetInputDialog:

    def __init__(self, parent):
        self.__dialog = uic.loadUi(os.path.join(gui_path, 'magnetinput.ui'))
        self._timer = QTimer()
        # Timer para verificar que se ingreso magnet y destino
        self._timer_ok = QTimer()
        self._timer_ok.start(1000)
        self._timer_ok.timeout.connect(self.__tick_ok)
        # Boton Aceptar
        self.__dialog.buttonBox.buttons()[0].clicked.connect(self.__ok)
        self.__dialog.buttonBox.buttons()[0].setDisabled(True)
        # Boton Cancelar
        self.__dialog.buttonBox.buttons()[1].clicked.connect(self.__cancel)
        self.__save_dlg = QtGui.QFileDialog(parent)
        self.__save_dlg.setWindowTitle('Print Things')
        self.__save_dlg.setViewMode(QtGui.QFileDialog.Detail)
        self.__dialog.DestSelectionButton.clicked.connect(self.__open_file_picker)
        # Seteo el timer q va a verificar si hay un magnet link valido
        self._timer.timeout.connect(self.__tick)
        self.__magnet_link = None
        self.__dest_dir = None

    def __tick_ok(self):
        if self.__magnet_link and self.__dest_dir:
            self.__dialog.buttonBox.buttons()[0].setDisabled(False)
            self._timer_ok.stop()

    def __open_file_picker(self):
        self.__dest_dir = self.__save_dlg.getExistingDirectory()

    def __ok(self):
        """
        Metodo que se ejecuta al apretar boton aceptar
        """
        #mag = re.sub(r"^magnet.*&dn=([^&]*).*", r"\1", magnet_uri)
        #self.__magnet_link = urllib.unquote_plus(mag)

    def get_magnet_link(self):
        return self.__magnet_link

    def get_dir_dest(self):
        return self.__dest_dir

    def __cancel(self):
        self._timer.stop()
        self._timer_ok.stop()

    def __tick(self):
        # Verifica que lo q haya en el porta papeles sea un magnet link
        clipboard_text = Tk().clipboard_get()
        # mejorar la expresion regular
        self.__magnet_link = re.search(r"^magnet.*", clipboard_text)
        print clipboard_text
        if self.__magnet_link:
            self.__dialog.MagnetUriLabel.setText("Se encontro un Magnet Link Valido en el porta papeles")
            self._timer.stop()

    def show(self):
        text = "No se encuentro un Magnet Link en el porta papeles"
        self.__dialog.MagnetUriLabel.setText(text)
        self._timer.start(1000)
        self.__dialog.show()
