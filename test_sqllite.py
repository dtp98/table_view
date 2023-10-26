import sys
import datetime
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sqlite3
import re

class MyTableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

headers = ["","name", "city", "phone"]
class cl_form_5(QWidget):
    def __init__(self):
        super().__init__()
        self.le_SQL = QLineEdit(self)
        self.le_SQL.setGeometry(10,10,200,35)
        self.le_SQL.setPlaceholderText('loc theo SQL')
        self.le_SQL.textChanged.connect(self.etc_le_SQL)


        self.le_Search = QLineEdit(self)
        self.le_Search.setGeometry(250,10,200,35)
        self.le_Search.setPlaceholderText('loc theo filter fixed string')
        self.le_Search.textChanged.connect(self.etc_le_Search)

        self.sodong = QLineEdit(self)
        self.sodong.setGeometry(20,550,400,35)

        self.tbv_danhsach = QTableView(self)
        self.tbv_danhsach.setGeometry(10,50,700,500)

        
        self.model = QStandardItemModel(self)
        self.db=sqlite3.connect('data')
        self.data=self.db.execute("select * from nguoi").fetchall()

        for i in range(len(self.data)):
            self.item = QStandardItem()
            self.item.setCheckable(True)
            self.model.setItem(i, 0, self.item)
            for j in range(2,5):
                self.model.setItem(i,j-1,QStandardItem(str(self.data[i][j-1])))

        # self.model = MyTableModel(self.data, headers)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.tbv_danhsach.setModel(self.proxy)
        self.tbv_danhsach.setColumnWidth(0,30)
        self.sodong.setText(str(self.model.rowCount()))

        # # Set the custom header view
        header_view = QHeaderView(Qt.Horizontal, self.tbv_danhsach)
        self.tbv_danhsach.setHorizontalHeader(header_view)
        header_view.setSectionsClickable(True)
        header_view.sectionClicked.connect(self.change_check_box)
       
    def change_check_box(self,logical_index):

            if(logical_index == 0):
                model = self.tbv_danhsach.model()
                
                for row in range(model.rowCount()):
                    index = model.index(row, 0)
                    
                    model.setData(index, Qt.Checked, Qt.CheckStateRole)
                    
    def etc_le_SQL(self,text):
        bg = datetime.datetime.now()

        self.model.clear()
        dt = self.db.execute("select * from nguoi where name like '%" + text +"%'").fetchall()
        for i in range(len(dt)):
            for j in range(4):
                self.model.setItem(i,j,QStandardItem(str(dt[i][j])))

        self.tbv_danhsach.setModel(self.model)
        kt = datetime.datetime.now()
        self.sodong.setText(str(bg) + "------" + str(kt))

    def etc_le_Search(self,text):
        index = 1 #loc theo cot 0
        bg = datetime.datetime.now()
        
        self.proxy.setFilterKeyColumn(index)
        self.proxy.setFilterFixedString(text)
        
        kt = datetime.datetime.now()
        self.sodong.setText(str(bg) + "------" + str(kt))
app=QApplication()
window=cl_form_5()
window.show()
app.exec()


##################################fill corner#######################
# from PySide6.QtWidgets import QApplication,QAbstractButton, QMainWindow, QTableView, QWidget, QVBoxLayout, QLabel
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QStandardItemModel
# import sys


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     table = QTableView()
#     corner = table.findChild(QAbstractButton)

#     table.clicked.connect(lambda: print('cell'))
#     table.horizontalHeader().sectionClicked.connect(lambda: print('col'))
#     table.verticalHeader().sectionClicked.connect(lambda: print('row'))
#     corner.clicked.connect(lambda: print('corner'))

#     model = QStandardItemModel(3, 4, table)
#     table.setModel(model)
#     table.show()
#     sys.exit(app.exec())
#############################HEADER CLICKED############################
# from PySide6.QtWidgets import QApplication,QHeaderView,QAbstractButton, QMainWindow, QTableView, QWidget, QVBoxLayout, QLabel
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QStandardItemModel,QStandardItem


# class CustomHeaderView(QHeaderView):
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             # Get the index of the clicked column
#             logical_index = self.logicalIndexAt(event.pos().x())
#             print(f"Header column {logical_index} clicked!")
#         super().mousePressEvent(event)

# app = QApplication([])
# window = QMainWindow()

# # Create a QTableView
# table_view = QTableView(window)

# # Create a QStandardItemModel to populate the table view with data
# model = QStandardItemModel()
# table_view.setModel(model)

# # Populate the table model with some data (example)
# model.setHorizontalHeaderLabels(["Column 1", "Column 2"])
# for i in range(5):
#     row_items = [f"Row {i+1}, Col 1", f"Row {i+1}, Col 2"]
#     model.appendRow([QStandardItem(item) for item in row_items])

# # Get the horizontal header of the table view
# header = table_view.horizontalHeader()

# # Set the custom header view
# header_view = CustomHeaderView(Qt.Horizontal, table_view)
# table_view.setHorizontalHeader(header_view)

# window.setCentralWidget(table_view)
# window.show()
# app.exec()
