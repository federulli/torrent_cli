from PyQt4 import QtCore, QtGui, uic
#somewhere in constructor:
#uic.loadUi('mainwindow.ui')
import sys
from gui.main_window import MainWindow

def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    if len(sys.argv) > 0:
        f=open("h:\pepe.txt", "w")
        f.write(str(sys.argv))
    main()