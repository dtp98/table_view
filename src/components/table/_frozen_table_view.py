from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QTableWidgetItem, QTableView, QLabel, QProxyStyle, QStyleOption, QHeaderView, \
  QAbstractItemView

from ._button_delegate import ButtonDelegate

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from main import MainWindow


class FrozenTableView(QTableView):
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

  def __init__(self, parent=None, context=None):
    super(FrozenTableView, self).__init__()
    self._main_window: MainWindow = context
    self.setParent(parent)
    self.dist_btn_data_new = {}
    self.last_drop_row = None
    self.lastCol = 10

  def setupUi(self):
    self.verticalScrollBar().valueChanged.connect(
      self.parent().verticalScrollBar().setValue)
    self.parent().verticalScrollBar().valueChanged.connect(
      self.verticalScrollBar().setValue)
    self.setFocusPolicy(Qt.NoFocus)
    self.verticalHeader().hide()
    self.horizontalHeader().setSectionResizeMode(self.lastCol, QHeaderView.ResizeMode.Fixed)
    self.setMinimumWidth(110)
    self.horizontalHeader().setMinimumSectionSize(110)
    self.setDragEnabled(True)
    self.setAcceptDrops(True)
    self.setDragDropOverwriteMode(False)
    self.setStyle(self.DropmarkerStyle())
    
    for col in range(0, self.lastCol):
      self.setColumnHidden(col, True)

    # self.setItemDelegateForColumn(9, ButtonDelegate(self, "tbl_profile", _context=self._main_window, model=self.model()))

  def configTable(self, selectionModel):
    self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
    self.setSelectionModel(selectionModel)

  def data(self, index, role):
    if role == Qt.BackgroundRole:
      return QColor(18, 219, 187)
      # return QBrush(Qt.yellow)

  def cellButtonClicked(self, arg=None):
    btn = self.sender()
    btn_name = btn.objectName()
    index_row = int(btn_name.split('|||')[1])
    id_profile = self.model().index(index_row, 1).data()
    profile_name = self._main_window.tblProfile._model._data[index_row][3]
    self.profile_id_selected = id_profile

    if "btn_open_profile" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      btn.hide()
      # lbl_progress_icon = self.findChild(QLabel,'lbl_progress_icon_{0}|||{1}|||{2}'.format(btn_name.replace("btn_open_profile_", ""), index_row, self._main_window.tblProfile.lastCol))
      lbl_progress_icon = self.findChild(QLabel,'lbl_progress_icon_{0}'.format(btn_name.replace("btn_open_profile_", "")))
      lbl_progress_icon.show()
      lbl_progress_icon.movie().start()

      if self._main_window.ui.btn_super_admin.isVisible():
        self._main_window.profileCTL.run_worker_open_profile(index_row, id_profile)
      else:
        self.run_worker_get_and_check_permission(index_row, id_profile, btn, lbl_progress_icon)

    elif "btn_close_profile" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      btn.hide()
      lbl_progress_icon = self.findChild(QLabel,'lbl_progress_icon_{0}'.format(btn_name.replace("btn_close_profile_", "")))
      lbl_progress_icon.show()
      lbl_progress_icon.movie().start()
      self._main_window.tblProfile.closeProfile(btn, )

    elif "btn_edit_profile" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      self._main_window.ui.stk_crus_profile.setCurrentWidget(
        self._main_window.ui.page_page_create_and_edit_profile_busy)

      self._main_window.modalFormProfile.show_edit_form()
      self._main_window.profileCTL.run_worker_get_profile_info(id_profile)
      # self._main_window.profileEditForm.setup_form_edit(id_profile, profile_name)

    elif "btn_add_user" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      self._main_window.profileSettingPages.show_page_add_user_profile(id_profile, profile_name)

    elif "btn_backup_setting" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      self._main_window.profileSettingPages.show_page_backup_setting(id_profile, profile_name)

    elif "btn_transfer" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      self._main_window.profileSettingPages.show_page_transfer(id_profile, profile_name)

    elif "btn_duplicate" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      #print("Duplicate profile show")
      self._main_window.profileSettingPages.show_page_duplicate(id_profile, profile_name)
      self._main_window.tblProfile.tblProfileFunction.hide_all_text_elm()

    elif "btn_renew" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      self._main_window.profileSettingPages.show_page_renew(id_profile, profile_name)

    elif "btn_delete_profile" in btn_name:
      self.selectRow(index_row)
      self._main_window.tblProfile.selectRow(index_row)
      #print('zzzzzzzz')
      if self._main_window.profileCTL.is_profile_opened(id_profile):
          return
      self._main_window.dialogControler.warningDeleteProfile.show_dialog(
        title="Warning", 
        message=QCoreApplication.translate("MainWindow", "Are you sure you want to delete profile ", None) + f"'{profile_name}'",
        profile_id=id_profile)

  def getselectedRowsFast(self):
    selectedRows = []
    # for item in self.selectedItems():
    for item in self.selectedIndexes():
      if item.row() not in selectedRows:
        selectedRows.append(item.row())
    selectedRows.sort()
    return selectedRows


  def run_worker_get_and_check_permission(self, index_row, id_profile, btn, lbl_progress):
    print("Checking permissions")
    if (6 in self._main_window.workgroup_permissions and  self._main_window.ui.btn_super_admin.isHidden()) or self._main_window.ui.btn_super_admin.isVisible():
      self._main_window.profileCTL.run_worker_open_profile(index_row, id_profile)
    else:
      self._main_window.dialog_signal.emit(["Warning", f"You do not have permission to open profile!"])
      lbl_progress.hide()
      lbl_progress.movie().stop()
      btn.show()


