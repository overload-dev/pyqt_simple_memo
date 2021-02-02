import sys
import csv
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt

from modules import *

form_main = uic.loadUiType("views/main.ui")[0]


class WindowClass(QMainWindow, form_main):

    def __init__(self):
        super().__init__(flags=Qt.Window)
        self.setupUi(self)
        self._tree = Modules(self.memo_tree, self.memo_content)
        self._tree.load_initial_memos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
