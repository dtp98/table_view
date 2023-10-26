import time
import traceback
from typing import TYPE_CHECKING
from subprocess import CREATE_NO_WINDOW, Popen

from PySide6 import QtCore
from PySide6.QtCore import Qt, QModelIndex, QItemSelection, QCoreApplication
from PySide6.QtGui import QMovie, QMouseEvent
from PySide6.QtWidgets import QHeaderView, QPushButton, QLabel, QTreeView, QAbstractItemView, QTableView, QProxyStyle, \
  QStyleOption, QTableWidgetItem, QStackedLayout

if TYPE_CHECKING:
  from main import MainWindow

from ._button_delegate import ButtonDelegate
from ._column_name_delegate import ColumnNameDelegate
from ._column_account_delegate import ColumnAccountDelegate
from ._column_note_delegate import ColumnNoteDelegate
from ._column_proxy_delegate import ColumnProxyDelegate
from ._frozen_table_view import FrozenTableView
from ._table_profile_model import TableProfileModel
from ._frm_function_tbl_profile import TblProfileFunction

import global_var


class TblProfile(QTableView):
  class DropmarkerStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
      """Draw a line across the entire row rather than just the column we're hovering over.
      This may not always work depending on global style - for instance I think it won't
      work on OSX."""
      if str(
        element) == "PrimitiveElement.PE_IndicatorItemViewItemDrop" and not option.rect.isNull():  # element == self.PE_IndicatorItemViewItemDrop and
        option_new = QStyleOption(option)
        option_new.rect.setLeft(0)
        if widget:
          option_new.rect.setRight(widget.width())
        option = option_new
      super().drawPrimitive(element, option, painter, widget)

  def __init__(self, mainWindow):
    super(TblProfile, self).__init__()
    self._main_window: MainWindow = mainWindow

    self.frozenTableView = FrozenTableView(self, self._main_window)
    

    self._main_window.tbl_profile = self
    self.setObjectName('tbl_profile')

    self._is_filter_mode = False

    self._column_count = 11

    self._model = TableProfileModel(self._main_window, column=self._column_count, row=0, data=[])

    self.setDragEnabled(True)
    self.setAcceptDrops(True)
    self.setDragDropOverwriteMode(False)
    self.setStyle(self.DropmarkerStyle())
    self.last_drop_row = None
    self.lastCol = 10

    self.frozenTableView.setModel(self._model)
    self.frozenTableView.setupUi()
    self.setupUi(self._model)

    self.setup_table_style()

    self.tblProfileFunction = TblProfileFunction(self._main_window)
    self.tblProfileFunction.setupUi()

    _movie = QMovie()
    movie = QMovie(":/IconGif/resources/IconGif/Pulse-1s-40px.gif")
    movie.start()
    self._main_window.ui.lbl_tbl_profile_progress.setMovie(movie)

    self._main_window.ui.stk_pages_left_content.layout().setStackingMode(QStackedLayout.StackAll)
    self._main_window.ui.stk_pages_left_content.setCurrentWidget(self._main_window.ui.profile_page)

    self.pressed.connect(self.selection_changed)
    self._main_window.ui.layout_frm_of_tbl_profile.addWidget(self)

 

  def setup_table_style(self):
    self.header = self.horizontalHeader()
    self.header.setDefaultAlignment(Qt.AlignLeft)


    
    self.verticalHeader().hide()
    self.setStyleSheet("""
            QTableView {
                padding: 5px;
                border: none;
                gridline-color: transparent;
                color: #b6b6b6;
            }

            QTableView::item {
                padding-left: 0px;
                padding-right: 5px;
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

    """)
    self.setViewportMargins(0, 0, 0, 0)
    self.setSortingEnabled(True)
    self.setDragEnabled(True)

  def setupUi(self, model, tbl_name=None, arr_data_is_new=None):
    # self.setModel(model)
    header_tbl_profile = self.horizontalHeader()
    # header_tbl_profile.setSectionResizeMode(3, QHeaderView.Fixed)
    # self.setColumnWidth(3, 250)  # ID
    header_tbl_profile.setMinimumWidth(200)

    self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
    self.verticalHeader().sectionResized.connect(self.updateSectionHeight)

    self.horizontalHeader().setStretchLastSection(True)

    self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    self.viewport().stackUnder(self.frozenTableView)
    self.viewport().setContentsMargins(0, 0, 0, 0)

  def show_swap_profile_index_status_for_user(self, resp):
    self._main_window.show_tray_message('Info', "Profile index replaced", 5)
    self._main_window.profileCTL.run_worker_get_and_show_profiles()

  def update_model(self):
    model = TableProfileModel(self._main_window, column=11, row=len(self._model._data), data=self._model._data)
    self.setModel(model)
    self.frozenTableView.setModel(model)

    self.updateFrozenTableGeometry()
    self.frozenTableView.setFocusPolicy(Qt.NoFocus)
    self.frozenTableView.configTable(self.selectionModel())

    self.frozenTableView.setItemDelegateForColumn(10, ButtonDelegate(self.frozenTableView, "tbl_profile",
                                                                     _context=self._main_window, model=model))
    self.setItemDelegateForColumn(3, ColumnNameDelegate(self, "tbl_profile", _context=self._main_window, model=model))
    self.setItemDelegateForColumn(4,
                                  ColumnAccountDelegate(self, "tbl_profile", _context=self._main_window, model=model))
    self.setItemDelegateForColumn(5, ColumnNoteDelegate(self, "tbl_profile", _context=self._main_window, model=model))
    self.setItemDelegateForColumn(8, ColumnProxyDelegate(self, "tbl_profile", _context=self._main_window, model=model))

    self.configUiTblProfile()
    if self._main_window.modalFormProfile.close_clicked == True:
      self._main_window.modalFormProfile.close()
      self._main_window.modalFormProfile.close_clicked = False

    # self._main_window.tblProfile.tblProfileFunction.select_all_row_tbl_profile()

    if self._is_filter_mode == True:
      self._is_filter_mode = False
      result_count = f"{str(len(self._main_window.arr_profile))}"
      self._main_window.ui.lbl_num_result_profile_filter.setText(
        QCoreApplication.translate("MainWindow", result_count, None))
      self._main_window.ui.lbl_result_text_profile_filter.setText(
        QCoreApplication.translate("MainWindow", " results found", None))
      self._main_window.ui.frm_filter_profile_state.show()

    self._main_window.tblProfile.verticalScrollBar().setValue(self._main_window.tblProfile.verticalScrollBar().property("last_value"))

    # #print(192, "after", self._main_window.tblProfile.verticalScrollBar().value())
    

  def configUiTblProfile(self):
    self.verticalHeader().hide()
    self.setStyleSheet("""
                QTableView {
                    padding: 0px;
                    border: none;
                    gridline-color: transparent;
                    color: #b6b6b6;
                }

                QTableView::item {
                    padding-left: 0px;
                    padding-right: 5px;
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

        """)
    self.setViewportMargins(0, 0, 0, 0)
    header_tbl_outlook = self.horizontalHeader()
    header_tbl_outlook.setSectionResizeMode(2, QHeaderView.ResizeToContents)
    header_tbl_outlook.setMaximumSectionSize(500)
    header_tbl_outlook.setMinimumSectionSize(40)
    # header_tbl_outlook.setStretchLastSection(True)
    # header_tbl_outlook.setSectionResizeMode(3, QHeaderView.Stretch)
    # header_tbl_outlook.setSectionResizeMode(4, QHeaderView.Fixed)
    # header_tbl_outlook.setSectionResizeMode(3, QHeaderView.Stretch)
    # header_tbl_outlook.setSectionResizeMode(9, QHeaderView.Stretch)
    # header_tbl_outlook.setSectionResizeMode(8, QHeaderView.ResizeToContents)
    
    header_tbl_outlook.setSectionResizeMode(2, QHeaderView.Fixed)
    header_tbl_outlook.setSectionResizeMode(3, QHeaderView.Fixed)
    header_tbl_outlook.setSectionResizeMode(4, QHeaderView.Fixed)
    header_tbl_outlook.setSectionResizeMode(5, QHeaderView.Fixed)
    header_tbl_outlook.setSectionResizeMode(6, QHeaderView.Fixed)
    header_tbl_outlook.setSectionResizeMode(7, QHeaderView.Fixed)
    header_tbl_outlook.setSectionResizeMode(8, QHeaderView.Fixed)
    header_tbl_outlook.setSectionResizeMode(9, QHeaderView.Fixed)
    
    self.setColumnHidden(0, True)  # browser type
    self.setColumnHidden(1, True)  # id
    self.setColumnHidden(4, True)  # id
    self.setColumnHidden(7, False)  # status
    self.setColumnWidth(2, 50)  # STT
    self.setColumnWidth(3, 250)  # Profile Name
    self.setColumnWidth(4, 150)  # Account
    self.setColumnWidth(5, 250)  # Remark
    self.setColumnWidth(6, 120)  # Duration
    self.setColumnWidth(7, 70)  # Status
    self.setColumnWidth(8, 200)  # Proxy
    self.setColumnWidth(9, 120)  # Proxy
    # header_tbl_outlook.setSpan(0, 0, 1, 6)

    self._main_window.ui.stk_pages_left_content.setCurrentWidget(self._main_window.ui.profile_page)
    self._main_window.ui.stk_crus_profile.setCurrentWidget(self._main_window.ui.page_create_and_edit_profile)

  def updateSectionWidth(self, logicalIndex, oldSize, newSize):
    if logicalIndex == self.lastCol:
      self.frozenTableView.setColumnWidth(self.lastCol, newSize)
    self.updateFrozenTableGeometry()

  def updateSectionHeight(self, logicalIndex, oldSize, newSize):
    self.frozenTableView.setRowHeight(logicalIndex, newSize)

  def resizeEvent(self, event):
    super(TblProfile, self).resizeEvent(event)
    self.updateFrozenTableGeometry()

  def moveCursor(self, cursorAction, modifiers):
    current = super(TblProfile, self).moveCursor(cursorAction, modifiers)
    if (cursorAction == QAbstractItemView.MoveLeft and current.column() < self.lastCol and
      self.visualRect(current).topLeft().x() < (self.frozenTableView.columnWidth(self.lastCol))):
      newValue = (self.horizontalScrollBar().value() +
                  self.visualRect(current).topLeft().x() - self.frozenTableView.columnWidth(self.lastCol))
      self.horizontalScrollBar().setValue(newValue)
    return current

  def scrollTo(self, index, hint):
    if index.column() < self.lastCol:
      super(TblProfile, self).scrollTo(index, hint)

  def updateFrozenTableGeometry(self):
    x_position = self.verticalHeader().width() + self.frameWidth()
    for col in range(0, self.lastCol):
      x_position += self.columnWidth(col)
    x_viewPort = self.verticalHeader().width() + self.viewport().width() - self.columnWidth(
      self.lastCol) + self.frameWidth()
    self.frozenTableView.setGeometry(x_position if x_position < x_viewPort else x_viewPort,
                                     self.frameWidth(), self.columnWidth(self.lastCol),
                                     self.viewport().height() + self.horizontalHeader().height())

  # def updateFrozenTableGeometry(self):
  #     #print("updateFrozenTableGeometry>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
  #     try:
  #         x_viewPort = self.verticalHeader().width() + self.viewport().width() - self.columnWidth(self.lastCol) - \
  #                      self.columnWidth(self.lastCol - 1) - self.columnWidth(self.lastCol - 2)
  #         self.frozenTableView.setGeometry(
  #             x_viewPort,
  #             0,
  #             self.columnWidth(self.lastCol) + 6 + self.columnWidth(self.lastCol - 1) +
  #             self.columnWidth(self.lastCol - 2) + self.frameWidth(),
  #             self.viewport().height() + self.horizontalHeader().height() + 11
  #         )
  #     except Exception as e:
  #         #print('>>>>>>>updateFrozenTableGeometry')
  #         #print(e)
  #         pass

  def cellButtonClicked(self, arg=None):
    btn = self.sender()
    btn_name = btn.objectName()
    index_row = int(btn_name.split('|||')[1])
    id_profile = self._model.index(index_row, 1).data()
    profile_name = self._model._data[index_row][3]

    if "btn_edit_profile_name" in btn_name:
      self._main_window.profile_id_updating = id_profile
      self._main_window.profile_name_updating = profile_name
      self._main_window.dialogControler.editProfileName.show_dialog("Update Profile Name",
                                                                    "Please enter new Profile Name")

    elif "btn_edit_profile_note" in btn_name:
      self._main_window.profile_id_updating = id_profile
      self._main_window.profile_note_updating = self._model._data[index_row][5]
      self._main_window.profile_name_updating = profile_name
      self._main_window.dialogControler.editProfileNote.show_dialog("Update Profile Note",
                                                                    "Please enter new Profile Note")

    elif "btn_edit_profile_proxy" in btn_name:
      self._main_window.profile_id_updating = id_profile
      proxy = self._main_window.profileCTL.get_proxy_by_id_profile(id_profile)
      self._main_window.dialogControler.editProfileProxy.show_dialog("Update Profile Proxy",
                                                                     "Please enter new Profile Proxy", proxy)

    elif "btn_edit_account" in btn_name:
      self._main_window.profile_id_updating = id_profile
      self._main_window.profile_note_updating = self._model._data[index_row][5]
      self._main_window.dialogControler.editProfileAccount.show_dialog("Profile Account Edit",
                                                                       f"Profile Name: {profile_name}")

  def dropEvent(self, event):
    sender = event.source()
    super().dropEvent(event)
    dropRow = self.last_drop_row
    destination = self.objectName()
    to_index = self.indexAt(event.pos()).row()

    selectedRows = sender.getselectedRowsFast()

    #print('selectedRows_____________')
    #print(selectedRows)

    arr_id_profile = []

    model = sender.model()
    for srow in selectedRows:
      id = model.index(srow, 1).data()
      arr_id_profile.append(int(id))

    #print('arr_id_profile________________')
    #print(arr_id_profile)
    #print('to_index________________')
    #print(to_index)

    # if len(arr_id_profile) == 1:
    #   profile_source_id = arr_id_profile[0]
    #   profile_target_id = model.index(to_index, 1).data()
    #   self._main_window.dialogControler.replaceProfileIndex.show_dialog(profile_source_id, profile_target_id)

    event.accept()

  def find_btn(self, type_btn, tbl_name, row, col):
    btn = None
    if tbl_name == "tbl_outlook":
      btn = self._context.tbl_outlook.findChild(QPushButton, f'{type_btn}_{tbl_name}|||{row}|||{col}')
    elif tbl_name == "tbl_hotmail":
      btn = self._context.tbl_hotmail.findChild(QPushButton, f'{type_btn}_{tbl_name}|||{row}|||{col}')
    elif tbl_name == "tbl_gmail":
      btn = self._context.tbl_gmail.findChild(QPushButton, f'{type_btn}_{tbl_name}|||{row}|||{col}')
    return btn

  def getselectedRowsFast(self):
    selectedRows = []
    # for item in self.selectedItems():
    for item in self.selectedIndexes():
      if item.row() not in selectedRows:
        selectedRows.append(item.row())
    selectedRows.sort()
    return selectedRows

  def closeProfile(self, btn):
    btnName = btn.objectName()
    profile_index_row = int(btnName.split('|||')[1])
    # global_var.list_profile_closed.append(
    #     self._model.index(profile_index_row, 1).data())
    id_profile = self._model.index(profile_index_row, 1).data()
    for profile_opened in global_var.list_profile_opened:
      if profile_opened["profile_id"] == id_profile:
        try:
          Popen("TASKKILL /F /PID {pid} /T".format(pid=profile_opened["process_pid"]), shell=True,
                creationflags=CREATE_NO_WINDOW)
        except Exception as e:
          #print(e)
          pass
        global_var.list_profile_opened.remove(profile_opened)
        global_var.list_profile_closed.append(profile_opened)
        
        global_var.list_profile_id_opened.remove(int(profile_opened["profile_id"]))
        global_var.list_profile_id_closed.append(int(profile_opened["profile_id"]))
        break

  def get_index_row_by_id(self):
    return 58

  def update_profile_status(self, dict_table_state):
    #print('TblProfile:::::update_profile_status::: websocket')
    
    # #print("Load Table" , dict_table_state)
    column = self.lastCol
    if dict_table_state['state'] == "opened":
      row = self._main_window.dict_current_profile_show_on_table[dict_table_state['profile_id']]
      lbl_progress = self.findChild(QLabel, "lbl_progress_icon_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_close_profile = self.findChild(QPushButton,
                                         "btn_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_open_profile = self.findChild(QPushButton,
                                        "btn_open_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      if lbl_progress:
        lbl_progress.hide()
      btn_close_profile.show()
      btn_open_profile.hide()
    elif dict_table_state['state'] == "closing":
      row = self._main_window.dict_current_profile_show_on_table[dict_table_state['profile_id']]
      lbl_progress = self.findChild(QLabel, "lbl_progress_icon_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_close_profile = self.findChild(QPushButton,
                                         "btn_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_open_profile = self.findChild(QPushButton,
                                        "btn_open_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      if lbl_progress:
        lbl_progress.show()
      btn_close_profile.hide()
      btn_open_profile.hide()
    elif dict_table_state['state'] == "closed":
      row = self._main_window.dict_current_profile_show_on_table[dict_table_state['profile_id']]
      lbl_progress = self.findChild(QLabel, "lbl_progress_icon_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_close_profile = self.findChild(QPushButton,
                                         "btn_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_open_profile = self.findChild(QPushButton,
                                        "btn_open_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      if lbl_progress:
        lbl_progress.hide()
      btn_close_profile.hide()
      btn_open_profile.show()

  def update_ui_profile_state_run_on_other_device_from_socket(self, id):
    column = self.lastCol
    #print('self._main_window.dict_current_profile_show_on_table____________', self._main_window.dict_current_profile_show_on_table)
    try:
      row = self._main_window.dict_current_profile_show_on_table[id]
    except Exception as e:
      print(498, "Error", e)
      return 
    lbl_progress = self.findChild(QLabel, "lbl_progress_icon_{0}|||{1}|||{2}".format('tbl_profile', row, column))
    btn_close_profile = self.findChild(QPushButton,
                                       "btn_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
    btn_open_profile = self.findChild(QPushButton,
                                      "btn_open_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
    btn_remote_close_profile = self.findChild(QPushButton,
                                              "btn_remote_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row,
                                                                                                column))
    if btn_close_profile:
      btn_close_profile.hide()
    if btn_open_profile:
      btn_open_profile.hide()
    if lbl_progress:
      lbl_progress.hide()
    if btn_remote_close_profile:
      btn_remote_close_profile.show()
    # global_var.list_profile_opened.append(id)
    
    
    # try:
    #   column = self.lastCol
    #   row = self._main_window.dict_current_profile_show_on_table[id]
    #   lbl_progress = self.findChild(QLabel, "lbl_progress_icon_{0}|||{1}|||{2}".format('tbl_profile', row, column))
    #   btn_close_profile = self.findChild(QPushButton, "btn_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
    #   btn_open_profile = self.findChild(QPushButton, "btn_open_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
    #   btn_remote_close_profile = self.findChild(QPushButton, "btn_remote_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
    #   if btn_close_profile:
    #     btn_close_profile.hide()
    #   if btn_open_profile:
    #     btn_open_profile.hide()
    #   if lbl_progress:
    #     lbl_progress.hide()
    #   btn_remote_close_profile.show()
    #   # global_var.list_profile_opened.append(id)
    # 
    # except Exception as e:
    #   #print(484, 'Err ::: update_ui_profile_state_from_socket', e)


  def update_ui_profile_state_from_socket(self, id):
    try:
      column = self.lastCol
      row = self._main_window.dict_current_profile_show_on_table[id]
      lbl_progress = self.findChild(QLabel, "lbl_progress_icon_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_close_profile = self.findChild(QPushButton, "btn_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_open_profile = self.findChild(QPushButton, "btn_open_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))
      btn_remote_close_profile = self.findChild(QPushButton, "btn_remote_close_profile_{0}|||{1}|||{2}".format('tbl_profile', row, column))

      btn_close_profile.hide()
      btn_open_profile.show()
      lbl_progress.hide()
      btn_remote_close_profile.hide()
      # global_var.list_profile_opened.append(id)

    except Exception as e:
      #print(503, 'Err ::: update_ui_profile_state_from_socket', e)
      pass

  def mousePressEvent(self, event):
    if self._main_window.sticky_frame.isVisible():
      self._main_window.sticky_frame.hide()
    # indexes = self.selectionModel().selectedRows()
    # #print(len(indexes))
    super().mousePressEvent(event)

  def get_selected_profiles(self):
    arr_id_profile = []
    indexes = self.getselectedRowsFast()
    model = self.model()
    for index in indexes:
      id = model.index(index, 1).data()
      arr_id_profile.append(int(id))
    if len(arr_id_profile):
      self._main_window.ui.cb_select_all_tbl_profile.setChecked(True)
    else:
      self._main_window.ui.cb_select_all_tbl_profile.setChecked(False)
    return arr_id_profile

  def selection_changed(self):
    indexes = self.selectionModel().selectedRows()
    if len(indexes):
      self._main_window.ui.cb_select_all_tbl_profile.setText(
        QCoreApplication.translate("MainWindow", f'({str(len(indexes))}) entries selected', None))
      self._main_window.ui.cb_select_all_tbl_profile.setChecked(True)
      self.tblProfileFunction.set_status_frm_button_multi_action(True)

    else:
      self._main_window.ui.cb_select_all_tbl_profile.setText(
        QCoreApplication.translate("MainWindow", f'Select All', None))
      self._main_window.ui.cb_select_all_tbl_profile.setChecked(False)
      self.tblProfileFunction.set_status_frm_button_multi_action(False)
      
    if len(indexes) == 1 and self._main_window.ui.lbl_title_right_extra_profile.text() == "Duplicate profile":
      index_row = indexes[0].row()
      id_profile = self.model().index(index_row, 1).data()
      profile_name = self.model().index(index_row, 3).data()
      self.selectRow(index_row)
      self._main_window.profileSettingPages.show_page_duplicate(id_profile, profile_name)


  def getselectedRowsFast(self):
    selectedRows = []
    # for item in self.selectedItems():
    for item in self.selectedIndexes():
      if item.row() not in selectedRows:
        selectedRows.append(item.row())
    selectedRows.sort()
    return selectedRows

  # def resizeEvent(self, event):
  #   super(TblProfile, self).resizeEvent(event)
  #   super(FrozenTableView, self.frozenTableView).resizeEvent(event)
  # 
  #   print('tblprf resizeEvent')
  #   print(event.size().width())
  #   media_breakpoint = {
  #     "md": 800,
  #     "lg": 1200,
  #     "xl": 1400
  #   }
  # 
  #   tbl_profile_breakpoint = {
  #     "md": 1200,
  #     "lg": 1200,
  #     "xl": 1400,
  #     "xxl": 1600
  #   }
  #   print("self.tblProfile.width()")
  #   print(event.size().width())
  #   self.tblProfileFunction.screen_setup(event.size().width())
  #     
      