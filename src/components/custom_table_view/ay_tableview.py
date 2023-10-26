import time

from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QTableView, QProxyStyle, QStyleOption, QAbstractItemView, QHeaderView, \
  QStyledItemDelegate, QStyle

from .ay_table_view_model import AYTableViewModel
from ._button_delegate import ButtonDelegate


class DisabledEditingDelegate(QStyledItemDelegate):
  def createEditor(self, parent, option, index):
    return None  # Disable editing

class AYTableView(QTableView):
  # class DropmarkerStyle(QProxyStyle):
  #   def drawPrimitive(self, element, option, painter, widget=None):
  #     """Draw a line across the entire row rather than just the column we're hovering over.
  #     This may not always work depending on global style - for instance I think it won't
  #     work on OSX."""
  #     if str(element) == "PrimitiveElement.PE_IndicatorItemViewItemDrop" and not option.rect.isNull():  # element == self.PE_IndicatorItemViewItemDrop and
  #       option_new = QStyleOption(option)
  #       option_new.rect.setLeft(0)
  #       if widget:
  #         option_new.rect.setRight(widget.width())
  #       option = option_new
  #     super().drawPrimitive(element, option, painter, widget)

  def __init__(self, data: list, columns, header_setup):
    super(AYTableView, self).__init__()
    self.setObjectName("tbl_profile")
    self._header_setup = header_setup
    self._columns = columns
    self._column_count = len(columns)
    # self.setStyle(self.DropmarkerStyle())
    self.setup_table_style()
    self.setupUi()
    self._model = None
    

  
  def set_data(self, data):
    print('data____prxy', data)
    self._model = AYTableViewModel(self, columns=self._columns, data=data)
    self.setModel(self._model)

    for index, setup in enumerate(self._header_setup, 0):
      if setup != None:
        mode = setup.split('.')[0]
        if mode == 'Fixed': # Fixed, ResizeToContent, Stretch
          size = setup.split('.')[1]
          try:
            print('index______________________')
            print(index)
            self.header.setSectionResizeMode(index, QHeaderView.Fixed)
            self.setColumnWidth(index, int(size))  # ID
          except Exception as e:
            print(e)

  def setupUi(self):
    header_tbl_profile = self.horizontalHeader()
    header_tbl_profile.setMinimumWidth(200)
    self.horizontalHeader().setStretchLastSection(True)
    self.viewport().setContentsMargins(0, 0, 0, 0)

    self.setItemDelegateForColumn(3, ButtonDelegate(self, model=self.model()))

    
  def setup_table_style(self):
    self.verticalHeader().hide()
    self.header = self.horizontalHeader()
    self.header.setDefaultAlignment(Qt.AlignLeft)

    self.setStyleSheet("""
                QTableView {
                    background-color: #2B2D30;
                    border: none;
                    padding: 0px;
                    border: none;
                    gridline-color: transparent;
                    color: #b6b6b6;
                }

                QTableView::item {
                    padding-left: 0px;
                    padding-right: 5px;
                }

                QHeaderView::section {
                    background-color: #2B2D30;
                    max-width: 30px;
                    border: 1px solid transparent;
                    border-style: none;
                    border-bottom: 1px solid #515151;
                    border-right: 1px solid transparent;
                    text-align: left;
                }

                QTableView::item:selected {
                    background-color: rgba(54, 56, 60, 0.8);
                }

                QTableView::section {
                    background-color: rgb(62, 73, 83);
                    max-width: 30px;
                    text-align: left;
                }

                QTableView::horizontalHeader {
                    background-color: rgb(62, 73, 83);
                }

                QTableView::section:horizontal {
                    background-color: rgb(72, 84, 96);
                    padding: 0px;
                }


                QTableView::section:vertical {
                    border: 1px solid red;
                }

                QTableView .QScrollBar:horizontal {
                    border: none;
                    background: rgb(52, 59, 72);
                    min-height: 8px;
                    border-radius: 0px;
                    max-width: 79em;
                }
                
                QScrollBar:vertical {
                    border: none;
                    background: rgb(52, 59, 72);
                    width: 4px;
                    margin: 21px 0 21px 0;
                    border-radius: 0px;
                }
                
                QScrollBar::handle:vertical {
                    background: #4db6ac;
                    min-height: 25px;
                    border-radius: 0px;
                }
                
                
                QScrollBar::add-line:vertical {
                    border: none;
                    background: rgb(55, 63, 77);
                    height: 20px;
                    border-bottom-left-radius: 0px; 
                    border-bottom-right-radius: 0px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                
                QScrollBar::sub-line:vertical {
                    border: none;
                    background: rgb(55, 63, 77);
                    height: 20px;
                    border-top-left-radius: 0px;
                    border-top-right-radius: 0px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }
                
                QScrollBar::up-arrow:vertical,
                QScrollBar::down-arrow:vertical {
                    background: none;
                }
                
                QScrollBar::add-page:vertical,
                QScrollBar::sub-page:vertical {
                    background: none;
                }


        """)
    self.setViewportMargins(0, 0, 0, 0)

  # def enterEvent(self, index):
  #   print('index______111', index)
  #   self._model.setHoveredIndex(index)
  #   self.viewport().update()


  # def leaveEvent(self, index):
  #   self._model.setHoveredIndex(QModelIndex())
  #   self.viewport().update()
  
  # def paintEvent(self, event):
  #   print('paint_event____________')
  #   hovered_index = self._model.hovered_index
  #   # if hovered_index.isValid():
  #   option = QStyleOption()
  #   option.initFrom(self)
  #   painter = QPainter(self)
  # 
  #   # Set pen color and width
  #   pen = QPen()
  #   pen.setColor(QColor(255, 0, 0))
  #   pen.setWidth(2)
  #   painter.setPen(pen)
  # 
  #   # Set brush color
  #   brush = QColor(0, 0, 255)
  #   painter.setBrush(brush)
  #   style = self.style()
  #   # style.drawPrimitive(QStyle.PE_PanelItemViewItem, option, painter)


  def cellButtonClicked(self, arg=None):
    btn = self.sender()
    btn_name = btn.objectName()
    print(btn_name)

    # index_row = int(btn_name.split('|||')[1])
    # id_profile = self._model.index(index_row, 1).data()
    # profile_name = self._model._data[index_row][3]

    time.sleep(5)