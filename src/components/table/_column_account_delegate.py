from PySide6.QtCore import QSize, QCoreApplication
from PySide6.QtGui import QMovie, QIcon, Qt
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QLabel, QPushButton, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QFrame


class ColumnAccountDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, tbl_name=None, dist_data_is_new=None, _context=None, model=None):
        super(ColumnAccountDelegate, self).__init__(parent)
        self._tbl_name = tbl_name
        self._dist_data_is_new = dist_data_is_new
        self._main_window = _context
        self._model = model

    def paint(self, painter, option, index):
        super(ColumnAccountDelegate, self).paint(painter, option, index)
        if not self.parent().indexWidget(index) and not index.parent().isValid():
            option.features |= QStyleOptionViewItem.HasDecoration
            index_row = index.row()
            index_col = index.column()
            profile_duration = self.parent().model().index(index_row, 6).data()
            proxy_duration = self.parent().model().index(index_row, 8).data()
            
            profile_name = self._model._data[index_row][index_col]

            lbl_profile_account = QLabel(
                self.tr(f'{profile_name}'),
                self.parent()
            )
            lbl_profile_account.setObjectName('lbl_profile_account{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))
            # lbl_profile_account.setFixedSize(QSize(100, 23))


            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Edit.svg", QSize(), QIcon.Normal, QIcon.Off)
            btn_edit_account = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_edit_account.setIcon(icon)
            btn_edit_account.setFixedSize(QSize(23, 23))
            btn_edit_account.setToolTip(QCoreApplication.translate("MainWindow", u"Open", None))
            btn_edit_account.setObjectName('btn_edit_account_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))

            # btn_icon_browser.index = [index_row, index_col]
            lbl_profile_account.index = [index_row, index_col]
            btn_edit_account.index = [index_row, index_col]

            # config show hide
            if profile_duration not in ["None", ""]:
                arr_value = profile_duration.split(" ")
                if int(arr_value[0]) < 0:
                    btn_edit_account.hide()

            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(lbl_profile_account)
            h_box_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Minimum))
            h_box_layout.addWidget(btn_edit_account)

            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignRight)
            widget = QFrame()
            # widget.setFixedSize(150, 23)
            widget.setStyleSheet('''
                QFrame {
                    padding-top: 3px;
                    padding-right: 9px;
                    background: transparent;
                }
                QPushButton {
                    border: 1px solid transparent;
                    padding-top: 3px;
                    background: transparent;
                }
                QPushButton:hover {
                    border: 1px solid transparent;
                    background-color: #4E5157; 
                    padding-top: 3px;
                }
            ''')        #546370;
            widget.setLayout(h_box_layout)
            # btn_edit_profile.widget = widget
            self.parent().setIndexWidget(
                index,
                widget
            )
