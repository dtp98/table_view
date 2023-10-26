from PySide6.QtGui import QMovie, Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QFrame, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy


class ModalBusy(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setObjectName('profile_busy_box')
        self._main_window = parent
        self.hide()
        # self.setStyleSheet('background: rgba(47, 54, 64,0.7);')
        backLayout = QVBoxLayout(self)
        backLayout.setContentsMargins(0, 0, 0, 0)
        backLayout.setSpacing(0)

        frm_contain_progress = QFrame()
        frm_contain_progress.setStyleSheet('background: rgba(47, 54, 64,0.3);')
        layout_frm_contain_progress = QVBoxLayout(frm_contain_progress)
        layout_frm_contain_progress.setContentsMargins(0, 0, 0, 0)
        layout_frm_contain_progress.setSpacing(0)

        frm_indicator = QFrame()
        layout_frm_indicator = QHBoxLayout(frm_indicator)
        self.moviebusy = QMovie(":/icon/gif/Pulse-1s-60px.gif")
        self.lbl_progress_indicate = QLabel('')
        self.lbl_progress_indicate.setStyleSheet('background-color:transparent;')
        self.lbl_progress_indicate.setMovie(self.moviebusy)

        layout_frm_indicator.addItem(QSpacerItem(40, 18, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_frm_indicator.addWidget(self.lbl_progress_indicate, alignment=Qt.AlignCenter)
        layout_frm_indicator.addItem(QSpacerItem(40, 18, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_frm_contain_progress.addWidget(frm_indicator)

        backLayout.addWidget(frm_contain_progress)

        self._main_window.layout().addWidget(self)

        # self.centralWidget().setCurrentWidget(self.busy_box_widget)

    def show_busy_modal(self):
        self._main_window.setCurrentWidget(self)
        self.show()
        self.moviebusy.start()

    def hide_busy_modal(self):
        self.hide()
        self.moviebusy.stop()
