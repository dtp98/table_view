from PySide6.QtCore import QSize, QCoreApplication
from PySide6.QtGui import QMovie, QIcon, Qt
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QLabel, QPushButton, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QFrame, QTableView


class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent: QTableView, model=None):
        super(ButtonDelegate, self).__init__(parent)
        self._tbl_name = parent.objectName()
        self.model = model

    def paint(self, painter, option, index):
        super(ButtonDelegate, self).paint(painter, option, index)
        if not self.parent().indexWidget(index) and not index.parent().isValid():
            option.features |= QStyleOptionViewItem.HasDecoration
            index_row = index.row()
            index_col = index.column()

            try:
                profile_duration = self.parent().model().index(index_row, 6).data()
                proxy_duration = self.parent().model().index(index_row, 8).data()
            except Exception as e:
                import traceback
                traceback.print_exc()

            lbl_progress_icon = QLabel(
                self.tr('open'),
                self.parent()
            )
            lbl_progress_icon.setObjectName('lbl_progress_icon_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))
            lbl_progress_icon.hide()
            lbl_progress_icon.setFixedSize(QSize(25, 23))
            movie = QMovie(":/IconGif/resources/IconGif/Eclipse-0.3s-23px.gif")
            lbl_progress_icon.setMovie(movie)
            # movie.start()
            lbl_progress_icon.setStyleSheet('border: none;width:25px;')

            # table_profile.findChild(ten, loai)
            # lbl_progress_icon = table_profile.findChild("lbl_progress_icon_tbl_profile_2_2", QLabel)

            btn_label_new = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"New", None)),
                self.parent()
            )

            btn_label_new.setFixedSize(QSize(40, 16))
            btn_label_new.setStyleSheet(""" QPushButton {
                color:white;
                background-color: #07a181;
                font-size: 11px;
                font-weight: bold;
                border: none;
                margin: 0px 4px;
                padding: 0px 2px;
                width: 40px;
                }""")
            btn_label_new.setObjectName(
                'btn_label_new_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))
            btn_label_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
            btn_label_new.hide()


            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Play.svg", QSize(), QIcon.Normal, QIcon.Off)
            btn_open_profile = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_open_profile.setIcon(icon)
            btn_open_profile.setFixedSize(QSize(23, 23))
            btn_open_profile.setToolTip(QCoreApplication.translate("MainWindow", u"Open", None))
            btn_open_profile.setObjectName('btn_open_profile_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))


            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Close Square.svg", QSize(), QIcon.Normal, QIcon.Off)
            btn_remote_close_profile = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_remote_close_profile.setIcon(icon)
            btn_remote_close_profile.setFixedSize(QSize(23, 23))
            btn_remote_close_profile.setToolTip(QCoreApplication.translate("MainWindow", u"Remote Close", None))
            btn_remote_close_profile.setObjectName('btn_remote_close_profile_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))
            btn_remote_close_profile.hide()

            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/CloseRed.svg", QSize(), QIcon.Normal, QIcon.Off)
            btn_close_profile = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_close_profile.setIcon(icon)
            btn_close_profile.setFixedSize(QSize(23, 23))
            btn_close_profile.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
            btn_close_profile.setObjectName('btn_close_profile_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))
            btn_close_profile.hide()

            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Edit Square.svg",
                         QSize(), QIcon.Normal, QIcon.Off)
            btn_edit_profile = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_edit_profile.setIcon(icon)
            btn_edit_profile.setFixedSize(QSize(23, 23))
            btn_edit_profile.setToolTip(QCoreApplication.translate("MainWindow", u"Edit profile", None))
            btn_edit_profile.setObjectName('btn_edit_profile_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))

            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Add User.svg", QSize(), QIcon.Normal, QIcon.Off)
            btn_add_user = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_add_user.setIcon(icon)
            btn_add_user.setFixedSize(QSize(23, 23))
            btn_add_user.setToolTip(QCoreApplication.translate("MainWindow", u"Add user", None))
            btn_add_user.setObjectName(
                'btn_add_user_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))

            # icon = QIcon()
            # icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Download.svg", QSize(), QIcon.Normal, QIcon.Off)
            # btn_backup_setting = QPushButton(
            #     self.tr(QCoreApplication.translate("MainWindow", u"", None)),
            #     self.parent(),
            #     clicked=self.parent().cellButtonClicked
            # )
            # btn_backup_setting.setIcon(icon)
            # btn_backup_setting.setFixedSize(QSize(23, 23))
            # btn_backup_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Backup setting", None))
            # btn_backup_setting.setObjectName(
            #     'btn_backup_setting_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))
            # 
            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Filter.svg", QSize(), QIcon.Normal, QIcon.Off)
            btn_transfer = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_transfer.setIcon(icon)
            btn_transfer.setFixedSize(QSize(23, 23))
            btn_transfer.setToolTip(QCoreApplication.translate("MainWindow", u"Transfer profile", None))
            btn_transfer.setObjectName(
                'btn_transfer_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))

            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Paper Plus.svg", QSize(), QIcon.Normal, QIcon.Off)
            btn_duplicate = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_duplicate.setIcon(icon)
            btn_duplicate.setFixedSize(QSize(23, 23))
            btn_duplicate.setToolTip(QCoreApplication.translate("MainWindow", u"Duplicate profile", None))
            btn_duplicate.setObjectName(
                'btn_duplicate_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))

            icon = QIcon()
            icon.addFile(u":/IconPrimaryColor/resources/IconPrimaryColor/Paper Negative.svg", QSize(), QIcon.Normal, QIcon.Off)
            btn_renew = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_renew.setIcon(icon)
            btn_renew.setFixedSize(QSize(23, 23))
            btn_renew.setToolTip(QCoreApplication.translate("MainWindow", u"Renew profile", None))
            btn_renew.setObjectName(
                'btn_renew_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))

            icon = QIcon()
            icon.addFile(
                u":/IconPrimaryColor/resources/IconPrimaryColor/Delete.svg",
                QSize(), QIcon.Normal, QIcon.Off)
            btn_delete_profile = QPushButton(
                self.tr(QCoreApplication.translate("MainWindow", u"", None)),
                self.parent(),
                clicked=self.parent().cellButtonClicked
            )
            btn_delete_profile.setIcon(icon)
            btn_delete_profile.setFixedSize(QSize(23, 23))
            btn_delete_profile.setToolTip(QCoreApplication.translate("MainWindow", u"Delete", None))
            btn_delete_profile.setObjectName('btn_delete_profile_{0}|||{1}|||{2}'.format(self._tbl_name, index_row, index_col))

            lbl_progress_icon.index = [index_row, index_col]
            btn_open_profile.index = [index_row, index_col]
            btn_remote_close_profile.index = [index_row, index_col]
            btn_close_profile.index = [index_row, index_col]
            btn_label_new.index = [index_row, index_col]
            btn_add_user.index = [index_row, index_col]
            btn_edit_profile.index = [index_row, index_col]
            # btn_backup_setting.index = [index_row, index_col]
            btn_transfer.index = [index_row, index_col]
            btn_duplicate.index = [index_row, index_col]
            btn_renew.index = [index_row, index_col]
            btn_delete_profile.index = [index_row, index_col]

            # config show hide
            if profile_duration not in ["None", ""]:
                if profile_duration != None:
                    arr_value = profile_duration.split(" ")
                    if int(arr_value[0]) < 0:
                        btn_open_profile.setToolTip(QCoreApplication.translate("MainWindow", u"Renew to open profile", None))
                        btn_open_profile.setDisabled(True)
                        btn_open_profile.setCursor(Qt.CursorShape.ForbiddenCursor)
                        btn_close_profile.hide()
                        btn_edit_profile.hide()
                        btn_add_user.hide()
                        # btn_backup_setting.hide()
                        btn_transfer.hide()
                        btn_duplicate.hide()

            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(btn_label_new)
            h_box_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Minimum))
            h_box_layout.addWidget(lbl_progress_icon)
            h_box_layout.addWidget(btn_open_profile)
            h_box_layout.addWidget(btn_remote_close_profile)
            h_box_layout.addWidget(btn_close_profile)
            h_box_layout.addWidget(btn_edit_profile)
            # h_box_layout.addWidget(btn_add_user)
            # h_box_layout.addWidget(btn_backup_setting)
            # h_box_layout.addWidget(btn_transfer)
            h_box_layout.addWidget(btn_duplicate)
            # h_box_layout.addWidget(btn_renew)
            h_box_layout.addWidget(btn_delete_profile)

            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)

            widget = QFrame()
            widget.setStyleSheet('''
                QFrame {
                    padding-top: 3px;
                    padding-right: 9px;
                    border-left: 1px solid rgb(62, 73, 83);
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
