# from PySide6.QtCore import Qt
# from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QLabel, QStyledItemDelegate
# from PySide6.QtGui import *


# app = QApplication([])
# window = QMainWindow()

# table_view = QTableView()
# model = QStandardItemModel()
# table_view.setModel(model)

# num_rows = 5
# num_columns = 3

# model.setRowCount(num_rows)
# model.setColumnCount(num_columns)

# row_index = 0
# column_index = 0
# # label_text = "Hello World"

# label_item = QStandardItem()
# # label_item.setData(label_text, Qt.DisplayRole)
# icon = QIcon("delete.png")
# label_item.setData(icon,Qt.DecorationRole)
# model.setItem(row_index, column_index, label_item)


# widget = QWidget()
# layout = QVBoxLayout(widget)
# layout.addWidget(table_view)

# window.setCentralWidget(widget)
# window.show()

# app.exec()

from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QStandardItemModel, QIcon, QPixmap, QStandardItem
from PyQt5.QtCore import *

app = QApplication([])

# Tạo mô hình dữ liệu
model = QStandardItemModel()

# Thêm dữ liệu vào mô hình
icon = QIcon("delete.png") # Thay "path_to_icon" bằng đường dẫn tới biểu tượng của bạn
item = QStandardItem()
item.setText("Item with icon")
model.appendRow(item)

# Tạo table view
tableview = QTableView()
tableview.setModel(model)

# Đặt kích thước cột cho phù hợp
tableview.setColumnWidth(0, 200) # Thay 0 bằng số cột bạn muốn đặt kích thước

# Thiết lập biểu tượng và căn chỉnh phần tử
index = model.index(0, 0)
widget = QWidget()
layout = QHBoxLayout(widget)
icon_label = QLabel()
icon_label.setPixmap(icon.pixmap(24 , 24)) # Kích thước biểu tượng - thay đổi nếu cần
label = QLabel()
label.setText(model.data(index))
layout.addWidget(label)
layout.addWidget(icon_label)
layout.setAlignment(label, Qt.AlignRight)
layout.setContentsMargins(0, 0, 0, 0)
widget.setLayout(layout)

# Hiển thị table view
tableview.setIndexWidget(index, widget)
tableview.show()

app.exec_()

