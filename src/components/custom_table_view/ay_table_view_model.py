from PySide6.QtCore import QAbstractTableModel, Qt, QCoreApplication, QModelIndex
from PySide6.QtGui import QColor


# from asyncqt import QtCore


class AYTableViewModel(QAbstractTableModel):
  # https://stackoverflow.com/questions/64287713/how-can-you-set-header-labels-for-qtableview-columns
  def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
    if orientation == Qt.Horizontal and role == Qt.DisplayRole:
      # return f"Column {section + 1}"
      return self.columns[section]
    if orientation == Qt.Vertical and role == Qt.DisplayRole:
      return f"{section + 1}"

  def __init__(self, parent, columns, data):
    # self.setRowCount(0)
    self.columns = columns

    super(AYTableViewModel, self).__init__(parent)
    self._row = len(data)
    self._column = len(columns)
    self._data = data
    self.colors = dict()
    self.hovered_index = QModelIndex()

  def rowCount(self, n=None):
    return self._row or len(self._data)

  def columnCount(self, n=None):
    return self._column or len(self._data[0])

  def flags(self, index: QModelIndex) -> Qt.ItemFlags:
    flags = super().flags(index)
    flags |= Qt.ItemIsSelectable
    flags &= ~Qt.ItemIsEditable
    return flags
    # return Qt.ItemIsDropEnabled | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled #  | Qt.ItemIsEditable

  def setHoveredIndex(self, index):
    self.hovered_index = index

  def supportedDropActions(self) -> bool:
    return Qt.MoveAction | Qt.CopyAction

  def data(self, index, role=Qt.ForegroundRole):
    if index.isValid(): # text content cua cell
      if role == Qt.ItemDataRole.DisplayRole or role == Qt.EditRole:
        try:
          value = str(self._data[index.row()][index.column()])
        except:
          value = None
          pass
        return value or ""

      if role == Qt.BackgroundRole: # mau nen cell
        color = self.colors.get((index.row(), index.column()))
        if color is not None:
          return color

      if role == Qt.ForegroundRole: # mau cua text
        try:
          value = str(self._data[index.row()][index.column()])
        except IndexError:
          value = ""
          pass
        if value == "live":
          return QColor(18, 219, 187)
        elif value == 'blocked':
          return QColor(243, 156, 18)
        elif value == "no_check":
          return QColor(200, 214, 229)
        elif value == "dis":
          return QColor(227, 190, 195)
        elif value == "ver":
          return QColor(255, 139, 67)
        elif value == "pass_wrong":
          return QColor(133, 155, 228)
        elif value == "not_signin":
          return QColor(225, 112, 90)
        elif value == "acc_deleted":
          return QColor(225, 112, 90)
        elif value == "not_exists":
          return QColor(225, 255, 255)

      if role == Qt.TextAlignmentRole: # can chinh content trong cell
        return int(Qt.AlignLeft | Qt.AlignVCenter)

  # def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
  #   try:
  #     curentValue = self._data[index.row()][index.column()]
  #   except IndexError:
  #     curentValue = ' '
  #   if not index.isValid():
  #     return False

  #   if role == Qt.ItemDataRole.EditRole:
  #     #print(377, 'setData tableView')
  #     if value == "":
  #       return False
  #     if value != curentValue and value != "":
  #       try:
  #         self._data[index.row()][index.column()] = value
  #       except:
  #         return False
  #     else:
  #       self._data[index.row()][index.column()] = curentValue
  #     return True

  #   return False

  # @QtCore.Slot(int, int, QtCore.QVariant)
  def update_item(self, row, col, value):
    ix = self.index(row, col)
    self.setData(ix, value)

  def change_color(self, row, column, color):
    ix = self.index(row, column)
    self.colors[(row, column)] = color
    self.dataChanged.emit(ix, ix, (Qt.BackgroundRole,))
