
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QSizePolicy

if TYPE_CHECKING:
  from main import MainWindow

class TblProfilePagination():
    def __init__(self, mainWindow):
        self.offset_showing_entries_tbl_profile = 0
        self.showing_entries_tbl_profile = 25
        self.current_page_tbl_profile = 1
        self._main_window: MainWindow = mainWindow
        self._main_window.ui.frm_pagination_profile.hide()
        self._main_window.ui.horizontalSpacer_19.changeSize(9, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)


    def setupUi(self):
        self._context.section_tbl_profile.lbl_total_page_tbl_profile.setText(str(self._context.total_page_tbl_profile))
        self._context.section_tbl_profile.txt_selected_page_tbl_profile.setText(
            str(self._context.current_page_tbl_profile))
        self._context.section_tbl_profile.lbl_total_page_tbl_profile.setText(
            str(self._context.total_page_tbl_profile))
        self._context.section_tbl_profile.lbl_offset_tbl_profile.setText(
            str(self._context.offset_showing_entries_tbl_profile + 1))
        self._context.section_tbl_profile.lbl_limit_tbl_profile.setText(
            str(self._context.total_tbl_profile) if int(self._context.total_tbl_profile) < int(
                self._context.offset_showing_entries_tbl_profile + self._context.showing_entries_tbl_profile) else str(
                self._context.offset_showing_entries_tbl_profile + self._context.showing_entries_tbl_profile))
        self._context.section_tbl_profile.lbl_total_tbl_profile.setText(str(self._context.total_tbl_profile))

        self.update_show_hide_paginate_button()
        self._context.num_row_tbl_profile = len(self._context.arr_profile)

    def connect_signal_to_slot(self):
        self._main_window.section_tbl_profile.sl_show_entitys_tbl_profile.currentIndexChanged.connect(
            self.re_paging_tbl_profile)
        # self.reload_sl_page_tbl_profile()
        self._main_window.section_tbl_profile.txt_selected_page_tbl_profile.textChanged.connect(
            self.show_selected_page_tbl_profile)

        self._main_window.section_tbl_profile.btn_pages_first_tbl_profile.clicked.connect(self.show_first_page_tbl_profile)
        self._main_window.section_tbl_profile.btn_pages_last_tbl_profile.clicked.connect(self.show_last_page_tbl_profile)
        self._main_window.section_tbl_profile.btn_pages_prev_tbl_profile.clicked.connect(
            self.show_previous_page_tbl_profile)
        self._main_window.section_tbl_profile.btn_pages_next_tbl_profile.clicked.connect(self.show_next_page_tbl_profile)


    def show_selected_page_tbl_profile(self):
        try:
            self._context.current_page_tbl_profile = int(
                self._context.section_tbl_profile.txt_selected_page_tbl_profile.text())
            self.update_show_hide_paginate_button()
        except ValueError as e:
            #print(e)
            pass

    def re_paging_tbl_profile(self, index):
        if index == 0:  # 25
            self._context.offset_showing_entries_tbl_profile = 0
            self._context.showing_entries_tbl_profile = 25
            self._context.current_page_tbl_profile = 1

        elif index == 1:  # 50
            self._context.offset_showing_entries_tbl_profile = 0
            self._context.showing_entries_tbl_profile = 50
            self._context.current_page_tbl_profile = 1

        elif index == 2:  # 100
            self._context.offset_showing_entries_tbl_profile = 0
            self._context.showing_entries_tbl_profile = 100
            self._context.current_page_tbl_profile = 1

        elif index == 3:  # 250
            self._context.offset_showing_entries_tbl_profile = 0
            self._context.showing_entries_tbl_profile = 250
            self._context.current_page_tbl_profile = 1

        elif index == 4:  # 500
            self._context.offset_showing_entries_tbl_profile = 0
            self._context.showing_entries_tbl_profile = 500
            self._context.current_page_tbl_profile = 1

        # self.load_tbl_profile()
        self.reload_sl_page_tbl_profile()
        self.update_show_hide_paginate_button()

    def show_previous_page_tbl_profile(self):
        if self._context.current_page_tbl_profile > 1:
            self._context.current_page_tbl_profile = self._context.current_page_tbl_profile - 1
            self._context.section_tbl_profile.txt_selected_page_tbl_profile.setText(
                str(self._context.current_page_tbl_profile))

    def show_next_page_tbl_profile(self):
        if self._context.current_page_tbl_profile < self._context.total_page_tbl_profile:
            self._context.current_page_tbl_profile = self._context.current_page_tbl_profile + 1
            self._context.section_tbl_profile.txt_selected_page_tbl_profile.setText(
                str(self._context.current_page_tbl_profile))

    def show_first_page_tbl_profile(self):
        self._context.current_page_tbl_profile = 1
        self._context.section_tbl_profile.txt_selected_page_tbl_profile.setText(
            str(self._context.current_page_tbl_profile))

    def show_last_page_tbl_profile(self):
        self._context.current_page_tbl_profile = self._context.total_page_tbl_profile
        self._context.section_tbl_profile.txt_selected_page_tbl_profile.setText(
            str(self._context.total_page_tbl_profile))

    def reload_sl_page_tbl_profile(self):
        self._context.section_tbl_profile.lbl_total_page_tbl_profile.setText(str(self._context.total_page_tbl_profile))
        self.update_show_hide_paginate_button()

    def update_show_hide_paginate_button(self):
        if self._context.current_page_tbl_profile <= 1:
            self._context.section_tbl_profile.btn_pages_first_tbl_profile.setEnabled(False)
            self._context.section_tbl_profile.btn_pages_prev_tbl_profile.setEnabled(False)
        else:
            self._context.section_tbl_profile.btn_pages_first_tbl_profile.setEnabled(True)
            self._context.section_tbl_profile.btn_pages_prev_tbl_profile.setEnabled(True)

        if self._context.current_page_tbl_profile >= self._context.total_page_tbl_profile:
            self._context.section_tbl_profile.btn_pages_next_tbl_profile.setEnabled(False)
            self._context.section_tbl_profile.btn_pages_last_tbl_profile.setEnabled(False)
        else:
            self._context.section_tbl_profile.btn_pages_next_tbl_profile.setEnabled(True)
            self._context.section_tbl_profile.btn_pages_last_tbl_profile.setEnabled(True)