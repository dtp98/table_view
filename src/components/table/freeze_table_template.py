import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QFile, QFileInfo, Qt, QByteArray, QTextStream, QStringDecoder
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QHeaderView, QTableView, QAbstractItemView

# datas = {
#     "Category 1": [
#         ("New Game 2", "Playnite", "", "", "Never", "Not Played", ""),
#         ("New Game 3", "Playnite", "", "", "Never", "Not Played", ""),
#     ],
#     "No Category": [
#         ("New Game", "Playnite", "", "", "Never", "Not Plated", ""),
#     ]
# }
#
#
# class GroupDelegate(QtWidgets.QStyledItemDelegate):
#     def __init__(self, parent=None):
#         super(GroupDelegate, self).__init__(parent)
#         self._plus_icon = QtGui.QIcon("../stuffs/add-fill.png")
#         self._minus_icon = QtGui.QIcon("../stuffs/subtract-fill.png")
#
#     def initStyleOption(self, option, index):
#         super(GroupDelegate, self).initStyleOption(option, index)
#         if not index.parent().isValid():
#             is_open = bool(option.state & QtWidgets.QStyle.State_Open)
#             option.features |= QtWidgets.QStyleOptionViewItem.HasDecoration
#             option.icon = self._minus_icon if is_open else self._plus_icon
#
#
# class GroupView(QtWidgets.QTreeView):
#     def __init__(self, model, parent=None):
#         super(GroupView, self).__init__(parent)
#         self.setIndentation(0)
#         self.setExpandsOnDoubleClick(False)
#         self.clicked.connect(self.on_clicked)
#         delegate = GroupDelegate(self)
#         self.setItemDelegateForColumn(0, delegate)
#         self.setModel(model)
#         self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
#         # self.header().setStyleSheet("background-color: #0D1225;")
#         self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
#         self.setStyleSheet("background-color: #0D1225;")
#
#     @QtCore.Slot(QtCore.QModelIndex)
#     def on_clicked(self, index):
#         if not index.parent().isValid() and index.column() == 0:
#             self.setExpanded(index, not self.isExpanded(index))
#
#
# class GroupModel(QtGui.QStandardItemModel):
#     def __init__(self, parent=None):
#         super(GroupModel, self).__init__(parent)
#         self.setColumnCount(8)
#         self.setHorizontalHeaderLabels(["", "Name", "Library", "Release Date", "Genre(s)", "Last Played", "Time Played", ""])
#         for i in range(self.columnCount()):
#             it = self.horizontalHeaderItem(i)
#             it.setForeground(QtGui.QColor("#eb5959"))
#
#     def add_group(self, group_name):
#         item_root = QtGui.QStandardItem()
#         item_root.setEditable(False)
#         item = QtGui.QStandardItem(group_name)
#         item.setEditable(False)
#         ii = self.invisibleRootItem()
#         i = ii.rowCount()
#         for j, it in enumerate((item_root, item)):
#             ii.setChild(i, j, it)
#             ii.setEditable(False)
#         for j in range(self.columnCount()):
#             it = ii.child(i, j)
#             if it is None:
#                 it = QtGui.QStandardItem()
#                 ii.setChild(i, j, it)
#             it.setBackground(QtGui.QColor("#002842"))
#             it.setForeground(QtGui.QColor("#F2F2F2"))
#         return item_root
#
#     def append_element_to_group(self, group_item, texts):
#         j = group_item.rowCount()
#         item_icon = QtGui.QStandardItem()
#         item_icon.setEditable(False)
#         item_icon.setIcon(QtGui.QIcon("../stuffs/gamepad-fill.png"))
#         item_icon.setBackground(QtGui.QColor("#0D1225"))
#         group_item.setChild(j, 0, item_icon)
#         for i, text in enumerate(texts):
#             item = QtGui.QStandardItem(text)
#             item.setEditable(False)
#             item.setBackground(QtGui.QColor("#0D1225"))
#             item.setForeground(QtGui.QColor("#F2F2F2"))
#             group_item.setChild(j, i+1, item)
#
#
# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#
#         model = GroupModel(self)
#         tree_view = GroupView(model)
#         self.setCentralWidget(tree_view)
#
#         for group, childrens in datas.items():
#             group_item = model.add_group(group)
#             for children in childrens:
#                 model.append_element_to_group(group_item, children)
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     w = MainWindow()
#     w.resize(720, 240)
#     w.show()
#     sys.exit(app.exec())


class FreezeTableWidget(QTableView):
    def __init__(self, model):
        super(FreezeTableWidget, self).__init__()
        self.setModel(model)
        self.lastCol = self.model().columnCount() - 1
        self.frozenTableView = QTableView(self)
        self.init()
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(
            self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(
            self.frozenTableView.verticalScrollBar().setValue)

    def init(self):
        self.frozenTableView.setModel(self.model())
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.horizontalHeader().setSectionResizeMode(
                QHeaderView.Fixed)
        self.viewport().stackUnder(self.frozenTableView)

        self.frozenTableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: #8EDE21;
                         selection-background-color: #999;
            }''')   # for demo purposes

        self.frozenTableView.setSelectionModel(self.selectionModel())
        # self.frozenTableView.setLayoutDirection(Qt.RightToLeft)
        for col in range(0, self.model().columnCount()):
            if col < self.lastCol:
                self.frozenTableView.setColumnHidden(col, True)
        self.frozenTableView.setColumnWidth(self.lastCol, self.columnWidth(self.lastCol))
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.show()
        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex == self.lastCol:
            self.frozenTableView.setColumnWidth(self.lastCol, newSize)
        self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        super(FreezeTableWidget, self).resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor(self, cursorAction, modifiers):
        current = super(FreezeTableWidget, self).moveCursor(cursorAction, modifiers)
        if (cursorAction == QAbstractItemView.MoveLeft and
                current.column() < self.lastCol and
                self.visualRect(current).topLeft().x() < self.frozenTableView.columnWidth(self.lastCol)):
            newValue = (self.horizontalScrollBar().value() +
                        self.visualRect(current).topLeft().x() -
                        self.frozenTableView.columnWidth(self.lastCol))
            self.horizontalScrollBar().setValue(newValue)
        return current

    def scrollTo(self, index, hint):
        if index.column() < self.lastCol:
            super(FreezeTableWidget, self).scrollTo(index, hint)

    def updateFrozenTableGeometry(self):
        x_position = self.verticalHeader().width() + self.frameWidth()
        for col in range(0, self.lastCol):
            x_position += self.columnWidth(col)
        x_viewPort = self.verticalHeader().width() + self.viewport().width() - self.columnWidth(self.lastCol) + self.frameWidth()
        self.frozenTableView.setGeometry(x_position if x_position < x_viewPort else x_viewPort,
                self.frameWidth(), self.columnWidth(self.lastCol),
                self.viewport().height() + self.horizontalHeader().height())


def main(args):
    # def split_and_strip(s, splitter):
    #     return [s.strip() for s in line.split(splitter)]

    app = QApplication(args)
    model = QStandardItemModel()
    data = [
        ["France", "Norway", "YDS", "UK(tech.)", "UK(adj.)", "UIAA", "Ger", "Australia", "Finland", "Brazil"],
        [1,0, 5.2,0, 0, "I", "I",0, 0, "Isup"],
        [2,0, 5.3,0,0 , "II", "II", 11,0, "II"],
        [3, 3, 5.4,0, 0, "III", "III", 12,0, "IIsup"],
        [4, 4, 5.5, "4a", "VD", "IV", "IV", 12,0, "III"],
        ["5a", 5 , 5.6,0, "S", "V" , "V", 13, 5 , "IIIsup"],
        ["5b", 5, 5.7, "4b", "HS", "V", "VI", 14, 5, "IV"],
        ["5c", 5 , 5.8,0, "VS", "VI", "VIIa", 16, 5, "IVsup"],
        [6, 6, 5.9, 5, "HVS", "VI", "VIIb", 17,0, "V"],
    ]
    header = data[0]
    model.setHorizontalHeaderLabels(header)
    row = 0
    for x in range(1, len(data)):
        fields = data[x]
        for col, field in enumerate(fields):
            newItem = QStandardItem(field)
            model.setItem(row, col, newItem)
        row += 1
    tableView = FreezeTableWidget(model)
    tableView.setWindowTitle("Frozen Column Example")
    tableView.resize(560, 680)
    tableView.show()
    return app.exec()


if __name__ == '__main__':
    main(sys.argv)




