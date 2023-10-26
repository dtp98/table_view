import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QHBoxLayout
from PySide6.QtCore import QCoreApplication, QSize

from src import AYTableView
import resources_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._main_layout = QHBoxLayout()
        header_setup = ["Fixed.30", "Fixed.200", None, None]

        columns = [
          '#',
          QCoreApplication.translate("MainWindow", u"Profile Name", None),
          QCoreApplication.translate("MainWindow", u"Proxy Info", None),
          QCoreApplication.translate("MainWindow", u"Activity", None),
        ]

        data = [
            ["1", "ho so 1", "http:192.168.1.1:6000:username:pass", None],
            ["2", "ho so 2", "http:192.168.1.1:6000:username:pass", None],
            ["3", "ho so 3", "http:192.168.1.1:6000:username:pass", None]
        ]

        self._table = AYTableView(data=[], columns=columns, header_setup=header_setup)
        self._table.set_data(data=data)
        self.setCentralWidget(self._table)
        self.resize(QSize(800, 600))



app=QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()
