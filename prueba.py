from PyQt4 import QtCore, QtGui, uic

import sys
from gui.main_window import MainWindow

def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
