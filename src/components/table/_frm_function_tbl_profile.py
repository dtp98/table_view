from PySide6 import QtGui
from PySide6.QtCore import QCoreApplication, QObject, Signal, Qt

from typing import TYPE_CHECKING

from PySide6.QtCore import QSize, QCoreApplication
from PySide6.QtGui import QIcon, QCursor, QPixmap, QColor, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QComboBox, QCheckBox, QMenu, QPushButton, QLineEdit, QStylePainter, QStyle

if TYPE_CHECKING:
    from main import MainWindow


class SinalMng(QObject):
  sinal_remove_input_frm_text_filter = Signal(str)

class TblProfileFunction():
    
    def __init__(self, mainWindow):
        self._main_window: MainWindow = mainWindow
        self._sinal_mng = SinalMng()
        self._mode = "icontext" # icontext || icon

    def setupUi(self):
        self._main_window.ui.btn_create_new_profile.clicked.connect(lambda: self._main_window.modalFormProfile.show_modal(browser_type='chrome'))

        self._main_window.ui.btn_tbl_profile_delete_all_selected.clicked.connect(self.delete_profiles)
        self._main_window.ui.cb_select_all_tbl_profile.clicked.connect(self.select_all_row_tbl_profile)
        self._main_window.ui.txt_top_frm_search_tbl_profile.returnPressed.connect(self.search_profile)
        self._main_window.ui.frm_filter_profile_state.hide()
        self.setup_filter_field()
        self.add_sl_filter_event_listener()

        self._main_window.ui.lbl_num_result_profile_filter.setStyleSheet('font-weight: bold;color: #fff;')
        self._sinal_mng.sinal_remove_input_frm_text_filter.connect(self.update_relationship_filter_field)
        self.frm_filter_by_status_input = self._main_window.FrmFilterResult(input_field_name="Status", sinal_remove=self._sinal_mng.sinal_remove_input_frm_text_filter)
        self.frm_filter_by_status_input.btn_clear.clicked.connect(self.clicked_btn_clear_filter)
        self._main_window.ui.hlo_frm_outer_custom_frm_filter_input.addWidget(self.frm_filter_by_status_input)
        
        self._main_window.ui.btn_reset_search_field_profile_page.setCursor(QCursor(Qt.PointingHandCursor))
        self._main_window.ui.btn_reset_search_field_profile_page.setMinimumHeight(26)
        self._main_window.ui.btn_reset_search_field_profile_page.setStyleSheet('''
          QPushButton {
            color: #fca5b5;
            font-weight: bold;
            border-radius: 5px;
          }
        ''')

        self._main_window.ui.btn_reset_search_field_profile_page.hide()
        self._main_window.ui.btn_reset_search_field_profile_page.clicked.connect(self.remove_search_result)
        self._main_window.ui.txt_top_frm_search_tbl_profile.textChanged.connect(self.show_btn_clear)
        
        
        self._main_window.ui.btn_add_user_frm_profile_function.clicked.connect(lambda: self.clicked_btn_frm_profile_function("btn_add_user_frm_profile_function"))
        self._main_window.ui.btn_transfer_frm_profile_function.clicked.connect(lambda: self.clicked_btn_frm_profile_function("btn_transfer_frm_profile_function"))
        self._main_window.ui.btn_renew_frm_profile_function.clicked.connect(lambda: self.clicked_btn_frm_profile_function("btn_renew_frm_profile_function"))

        self.setup_stylesheet()
        self.set_status_frm_button_multi_action(False)
      
        self.cb_filter_profile_by_status.setMinimumWidth(100)
        self._main_window.ui.sl_page_size.setMinimumWidth(60)

    def clicked_btn_clear_filter(self):
      self.reset_filter_status()
      # self._main_window.profileCTL.refresh_tbl_profile()

    def clicked_btn_frm_profile_function(self, btn_name):
      if btn_name == "btn_add_user_frm_profile_function":
        self._main_window.profileSettingPages.show_profile_selected_on_page_add_user()
      elif btn_name == "btn_transfer_frm_profile_function":
        self._main_window.profileSettingPages.show_profile_selected_on_page_transfer()
      elif btn_name == "btn_renew_frm_profile_function":
        self._main_window.profileSettingPages.show_profile_selected_on_page_renew()

      self._main_window.bottomMenu.set_hide_frm_bottom_side()
      
    def remove_search_result(self):
      self._main_window.ui.txt_top_frm_search_tbl_profile.setEnabled(True)
      self._main_window.ui.txt_top_frm_search_tbl_profile.setText("")
      self._main_window.ui.btn_reset_search_field_profile_page.hide()
      self._main_window.profileCTL.run_worker_get_and_show_profiles()

      
    def show_btn_clear(self):
      if self._main_window.ui.txt_top_frm_search_tbl_profile.text() == "":
        self._main_window.ui.btn_reset_search_field_profile_page.hide()

        
    def setup_stylesheet(self):
      for item in self._main_window.ui.frm_function_tbl_profile.findChildren(QPushButton):
        item.setMinimumHeight(26)
        item.setCursor(QCursor(Qt.PointingHandCursor))
        
      for item in self._main_window.ui.frm_function_tbl_profile.findChildren(QLineEdit):
        item.setMinimumHeight(26)
        item.setMaximumHeight(26)

      for item in self._main_window.ui.frm_function_tbl_profile.findChildren(QCheckBox):
        item.setMinimumHeight(26)
        item.setCursor(QCursor(Qt.PointingHandCursor))
        
        
      self._main_window.ui.frm_function_tbl_profile.setStyleSheet('''
        QPushButton, QLineEdit, QCheckBox QComboBox {
          border: 1px solid transparent;
          border-radius: 5px;
          padding-left: 15px;
          padding-right: 15px;
        }
        
        QWidget:hover {
          border: 1px solid transparent;
        }
        
        QCheckBox {
          margin-top: 2px;
        }

        #btn_create_new_profile {
          padding-left: 15px;
          padding-right: 15px;
          background-color: #009688;
          color: #fff;
        }
        #btn_create_new_profile:hover {
          background-color: #4db6ac;
        }
        
        #frm_search_tbl_profile {
          border: 1px solid #515151;
          border-radius: 5px;
          height: 30px;
        }
        
        #frm_search_tbl_profile:hover {
          border: 1px solid #009688;
        }
        
        #frm_search_tbl_profile:focus {
          border: 1px solid #009688;
        }
        
        #btn_reset_search_field_profile_page {
          padding: 0px;
          height: 30px;
          max-width: 30px;
          width: 30px !important;
        }
        #btn_reset_search_field_profile_page:hover {
          background: transparent;
        }
      ''')
      self._main_window.ui.btn_reset_search_field_profile_page.setMaximumWidth(16)
      self._main_window.ui.frm_search_tbl_profile.setMaximumWidth(200)
      self._main_window.ui.frm_search_tbl_profile.setMinimumWidth(100)

      
    def set_status_frm_button_multi_action(self, status):
      if status == True:
        self._main_window.ui.btn_tbl_profile_delete_all_selected.setEnabled(True)
        self._main_window.ui.btn_add_user_frm_profile_function.setEnabled(True)
        self._main_window.ui.btn_transfer_frm_profile_function.setEnabled(True)
        self._main_window.ui.btn_renew_frm_profile_function.setEnabled(True)
        self.set_button_enable_mode()
      else:
        self._main_window.ui.btn_tbl_profile_delete_all_selected.setEnabled(False)
        self._main_window.ui.btn_add_user_frm_profile_function.setEnabled(False)
        self._main_window.ui.btn_transfer_frm_profile_function.setEnabled(False)
        self._main_window.ui.btn_renew_frm_profile_function.setEnabled(False)
        self.set_button_disabled_mode()

    def set_button_enable_mode(self):
      icon = QIcon()
      pixm = self.svg_to_pixmap(u":/IconBold/resources/IconBold/Delete.svg", 23, 23, QColor(255, 255, 255))
      icon.addPixmap(pixm)
      self._main_window.ui.btn_tbl_profile_delete_all_selected.setIcon(icon)

      icon = QIcon()
      pixm = self.svg_to_pixmap(u":/IconBold/resources/IconBold/Add User.svg", 23, 23, QColor(255, 255, 255))
      icon.addPixmap(pixm)
      self._main_window.ui.btn_add_user_frm_profile_function.setIcon(icon)

      icon = QIcon()
      pixm = self.svg_to_pixmap(u":/IconBold/resources/IconBold/Login.svg", 23, 23, QColor(255, 255, 255))
      icon.addPixmap(pixm)
      self._main_window.ui.btn_transfer_frm_profile_function.setIcon(icon)

      icon = QIcon()
      pixm = self.svg_to_pixmap(u":/IconBold/resources/IconBold/Paper Upload.svg", 23, 23, QColor(255, 255, 255))
      icon.addPixmap(pixm)
      self._main_window.ui.btn_renew_frm_profile_function.setIcon(icon)

    def set_button_disabled_mode(self):
      icon = QIcon()
      pixm = self.svg_to_pixmap(u":/IconBold/resources/IconBold/Delete.svg", 23, 23, QColor("black"))
      icon.addPixmap(pixm)
      self._main_window.ui.btn_tbl_profile_delete_all_selected.setIcon(icon)
      
      icon = QIcon()
      pixm = self.svg_to_pixmap(u":/IconBold/resources/IconBold/Add User.svg", 23, 23, QColor("black"))
      icon.addPixmap(pixm)
      self._main_window.ui.btn_add_user_frm_profile_function.setIcon(icon)
      
      icon = QIcon()
      pixm = self.svg_to_pixmap(u":/IconBold/resources/IconBold/Login.svg", 23, 23, QColor("black"))
      icon.addPixmap(pixm)
      self._main_window.ui.btn_transfer_frm_profile_function.setIcon(icon)
      
      icon = QIcon()
      pixm = self.svg_to_pixmap(u":/IconBold/resources/IconBold/Paper Upload.svg", 23, 23, QColor("black"))
      icon.addPixmap(pixm)
      self._main_window.ui.btn_renew_frm_profile_function.setIcon(icon)

    def svg_to_pixmap(self, svg_filename: str, width: int, height: int, color: QColor) -> QPixmap:
      renderer = QSvgRenderer(svg_filename)
      pixmap = QPixmap(width, height)
      pixmap.fill(Qt.GlobalColor.transparent)
      painter = QPainter(pixmap)
      renderer.render(painter)  # this is the destination, and only its alpha is used!
      painter.setCompositionMode(
        painter.CompositionMode.CompositionMode_SourceIn)
      painter.fillRect(pixmap.rect(), color)
      painter.end()
      return pixmap
      
    def setup_filter_field(self):
      self.cb_filter_profile_by_status = self._main_window.ComboboxMultiSelect(self._main_window)
      self.cb_filter_profile_by_status_menu = self._main_window.MenuMultiSelect(self.cb_filter_profile_by_status, ["Alive", "Expired"])
      # self.cb_filter_profile_by_status_menu = QMenu()
      # self.cb_filter_profile_by_status.setMenu(self.cb_filter_profile_by_status_menu)
      self.cb_filter_profile_by_status.setMenu(self.cb_filter_profile_by_status_menu)
      # self.cb_filter_profile_by_status.currentTextChanged.connect(lambda: self.on_filter_state_changed(self.cb_filter_profile_by_status))

      self._main_window.ui.hlo_frm_filter_profile_by_status.addWidget(self.cb_filter_profile_by_status)
      
    def update_relationship_filter_field(self, filter_text):
      for item in self.cb_filter_profile_by_status_menu.findChildren(QCheckBox):
        if item.text().lower() == filter_text:
          item.setChecked(False)
      
    def add_sl_filter_event_listener(self):
      for item in self.cb_filter_profile_by_status_menu.findChildren(QCheckBox):
        item.stateChanged.connect(lambda: self.on_checkbox_item_state_changed())
      
    def on_filter_state_changed(self, elm):
      self._main_window.ui.frm_filter_profile_state.show()

    def on_checkbox_item_state_changed(self):
      # self._main_window.ui.frm_filter_profile_state.hide()
      filter_text = ""
      num_checked = 0
      for item in self.cb_filter_profile_by_status.menu.findChildren(QCheckBox):
        if item.isChecked():
          num_checked += 1
          filter_text += item.text() + ","
      
      
      if filter_text == "" or filter_text == "All,":
        # self.frm_filter_by_status_input.frm_filter_content_items
        self._main_window.ui.frm_filter_profile_state.hide()
        self.cb_filter_profile_by_status.setText("Status")
        self._main_window.profileCTL.run_worker_get_and_show_profiles()
        return 
      
      #print('vanzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
      self.setup_frm_outer_custom_frm_filter_input()
      self._main_window.tblProfile._is_filter_mode = True
      filter_text = filter_text[0: len(filter_text) - 1].lower()
      if num_checked == 0:
        self.cb_filter_profile_by_status.setText("Status")
      else:
        self.cb_filter_profile_by_status.setText(QCoreApplication.translate("MainWindow", f"{num_checked} checked", None))
      self._main_window.profileCTL.run_worker_filter_profiles(filter_text)

    def reset_filter_status(self):
      self.cb_filter_profile_by_status.setText("Status")
      for item in self.cb_filter_profile_by_status_menu.findChildren(QCheckBox):
          item.setChecked(False)
      self._main_window.ui.frm_filter_profile_state.hide()
      self._main_window.profileCTL.refresh_tbl_profile()
      
    def setup_frm_outer_custom_frm_filter_input(self):
      # self.frm_filter_by_status_input.deleteLater()
      self.frm_filter_by_status_input.update_state(self.cb_filter_profile_by_status_menu)

      
      
    def search_profile(self):
      if self._main_window.ui.txt_top_frm_search_tbl_profile.text() == "":
        self._main_window.show_tray_message(msg="Input data invalid")
        return 
      self._main_window.ui.txt_top_frm_search_tbl_profile.setEnabled(False)
      self._main_window.ui.btn_reset_search_field_profile_page.show()
      search_text = self._main_window.ui.txt_top_frm_search_tbl_profile.text()
      self._main_window.profileCTL.run_worker_search_profiles(search_text)
      
    def delete_profiles(self):
      arr_profile_id = self._main_window.tblProfile.get_selected_profiles()
      self._main_window.dialogControler.warningDeleteProfiles.show_dialog("Warning", "Are you sure you want delete profile ", arr_profile_id)
      
    def select_all_row_tbl_profile(self):
      if self._main_window.ui.cb_select_all_tbl_profile.isChecked():
        self._main_window.tblProfile.selectAll()
        self.set_status_frm_button_multi_action(True)
        self._main_window.ui.cb_select_all_tbl_profile.setText(
          QCoreApplication.translate("MainWindow", f'({str(len(self._main_window.arr_profile))}) entries selected', None))
      else:
        self._main_window.tblProfile.clearSelection()
        self.set_status_frm_button_multi_action(False)
        self._main_window.ui.cb_select_all_tbl_profile.setText(
          QCoreApplication.translate("MainWindow", f'Select All', None))
        
    def screen_setup(self, mode):
      if mode == "icontext":
        if self._mode != "icontext":
          self.show_all_text_elm()
          self._mode = "icontext"
      elif mode == "icon":
        if self._mode != "icon":
          self.hide_all_text_elm()
          self._mode = "icon"
        
        
    def hide_all_text_elm(self):
      self._main_window.ui.btn_tbl_profile_delete_all_selected.setText("")
      self._main_window.ui.btn_add_user_frm_profile_function.setText("")
      self._main_window.ui.btn_transfer_frm_profile_function.setText("")
      self._main_window.ui.btn_renew_frm_profile_function.setText("")
      
      self._main_window.ui.btn_refresh_tbl_profile.setText("")
      self._main_window.ui.btn_create_new_profile.setText("")
      
      self._main_window.ui.btn_tbl_profile_delete_all_selected.setMaximumWidth(40)
      self._main_window.ui.btn_add_user_frm_profile_function.setMaximumWidth(40)
      self._main_window.ui.btn_transfer_frm_profile_function.setMaximumWidth(40)
      self._main_window.ui.btn_renew_frm_profile_function.setMaximumWidth(40)


    def show_all_text_elm(self):
      self._main_window.ui.btn_tbl_profile_delete_all_selected.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
      self._main_window.ui.btn_add_user_frm_profile_function.setText(QCoreApplication.translate("MainWindow", u"Add User", None))
      self._main_window.ui.btn_transfer_frm_profile_function.setText(QCoreApplication.translate("MainWindow", u"Transfer", None))
      self._main_window.ui.btn_renew_frm_profile_function.setText(QCoreApplication.translate("MainWindow", u"Renewal", None))

      self._main_window.ui.btn_refresh_tbl_profile.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
      self._main_window.ui.btn_create_new_profile.setText(QCoreApplication.translate("MainWindow", u"New Profile", None))
      
      self._main_window.ui.btn_tbl_profile_delete_all_selected.setMaximumWidth(260)
      self._main_window.ui.btn_add_user_frm_profile_function.setMaximumWidth(260)
      self._main_window.ui.btn_transfer_frm_profile_function.setMaximumWidth(260)
      self._main_window.ui.btn_renew_frm_profile_function.setMaximumWidth(260)




