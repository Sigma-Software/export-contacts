"""File with window UI"""

import os
import platform
from argparse import ArgumentParser

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QScreen
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsBlurEffect,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)

from domain.entities import ExportContactException
from ui.resources import resources  # DO NOT DELETE; it's needed for displaying images
from ui.styles.common.styles import progress_bar_style
from ui.widgets.popup import ErrorPopUp, SuccessPopUp
from utils.key import get_password, set_credentials
from utils.logger import LOGGER
from workflows.export import (
    connect_to_sent_items,
    export,
    get_all_emails_amount,
    is_email_address_valid
)

parser = ArgumentParser()
parser.add_argument(
    "--logging",
    help="Enable recording technical logs in file",
    action="store_true"
)
args = parser.parse_args()

if not args.logging:
    LOGGER.disabled = True

LOGGER.info('LOGGER START')

PLATFORM = platform.system()
if PLATFORM == 'Windows':
    from ui.widgets.user_input_form import UserInputFormWin as UserInputForm
    from ui.widgets.domains_form import DomainsFormWin as DomainsForm
elif PLATFORM == 'Darwin':
    from ui.widgets.user_input_form import UserInputFormMacOS as UserInputForm
    from ui.widgets.domains_form import DomainsFormMac as DomainsForm

LOGGER.info(f'System: {PLATFORM}')


class MainWindow(QMainWindow):
    """Main widget of application"""

    PROGRESS_BAR_BODY_HEIGHT = 60
    PROGRESS_BAR_BODY_WIDTH = 650
    PROGRESS_BAR_HEIGHT = 12
    PROGRESS_BAR_WIDTH = 632
    ZERO_MARGIN = 0

    def __init__(self, **kwargs):
        super().__init__()

        self.min_width: int = kwargs['min_width']
        self.min_height: int = kwargs['min_height']
        self.max_width: int = kwargs['max_width']
        self.max_height: int = kwargs['max_height']

        self.set_window_size()

        main_widget = QWidget(parent=self)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        #  Basic configs for the window
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        main_layout.setSpacing(self.ZERO_MARGIN)

        self.setMinimumSize(self.min_width, self.min_height)
        self.setMaximumSize(self.max_width, self.max_height)
        main_layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )

        self.progress_group = QGroupBox(parent=self)
        self.progress_group.setFixedSize(
            self.PROGRESS_BAR_BODY_WIDTH,
            self.PROGRESS_BAR_BODY_HEIGHT
        )
        self.progress_layout = QVBoxLayout()
        self.progress_group.setLayout(self.progress_layout)

        self.progress_label = QLabel('', parent=self.progress_group)
        self.progress_layout.addWidget(
            self.progress_label,
            alignment=Qt.AlignLeft
        )

        self.progress_bar = QProgressBar(parent=self.progress_group)
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_bar.setFixedSize(
            self.PROGRESS_BAR_WIDTH,
            self.PROGRESS_BAR_HEIGHT
        )
        self.progress_bar.setTextVisible(False)
        self.progress_group.setStyleSheet(progress_bar_style)

        x_position = (self.geometry().width() // 2) - (self.progress_bar.width() // 2)
        y_position = (self.geometry().height() // 2) - (self.progress_bar.height() // 2)

        self.progress_group.move(x_position, y_position)
        self.progress_group.hide()
        self.max_progress_value = None
        #  Add left part of application
        self.user_form = UserInputForm(parent=main_widget)

        self.user_form.email_service_address.textEdited.connect(
            lambda: self.domain_form.popup_layout.itemAt(1).widget().setVisible(False)
        )
        self.user_form.username.textEdited.connect(
            lambda: self.domain_form.popup_layout.itemAt(1).widget().setVisible(False)
        )
        self.user_form.email.textEdited.connect(
            lambda: self.domain_form.popup_layout.itemAt(1).widget().setVisible(False)
        )
        self.user_form.password.textEdited.connect(
            lambda: self.domain_form.popup_layout.itemAt(1).widget().setVisible(False)
        )
        self.directory = None
        self.user_form.connect_event.connect(self.on_connect_event)
        self.user_form.visible_domain.connect(self.on_exclude_domains_switcher_toggle)
        main_layout.addWidget(self.user_form)

        #  Add right part of application
        self.domain_form = DomainsForm(parent=main_widget)
        main_layout.addWidget(self.domain_form)

        #  Set main widget of the window and set window title
        self.setCentralWidget(main_widget)
        self.setWindowTitle('ExportContacts tool')
        self.setWindowIcon(QIcon(
            f':/resources/styles/common/{"logo.ico" if PLATFORM == "Windows" else "logo.icns"}')
        )

    def set_window_size(self):
        screen: QScreen = QApplication.primaryScreen()
        screen_height: int = screen.size().height()
        screen_width: int = screen.size().width()

        height: int
        width: int
        if self.max_height >= screen_height >= self.min_height:
            height = screen_height
        elif screen_height > self.max_height:
            height = self.max_height
        else:
            height = self.min_height

        if self.max_width >= screen_width >= self.min_width:
            width = screen_width
        elif screen_width > self.max_width:
            width = self.max_width
        else:
            width = self.min_width

        center_width: int = (screen_width - width) // 2
        center_height: int = (screen_height - height) // 2

        self.setGeometry(center_width, center_height, width, height)

    def on_exclude_domains_switcher_toggle(self):
        """Slot for changing visibility of exclude domains form"""
        is_visible = self.sender().exclude_domain_switcher.isChecked()
        self.domain_form.change_domain_form_visibility(is_visible)

    def on_connect_event(self):
        """Slot for connection with exchange server and exporting contacts"""
        email: bool = is_email_address_valid(self.sender().email.text())
        domain_list: list = self.domain_form.domain_list

        if not email:
            message = 'Please enter a valid e-mail address.'
            error_popup = ErrorPopUp(message, parent=self.domain_form)
            self.domain_form.popup_layout.itemAt(1).widget().deleteLater()
            self.domain_form.popup_layout.insertWidget(
                1, error_popup, alignment=Qt.AlignLeft | Qt.AlignTop
            )
            LOGGER.error('Invalid email')
            return

        if self.sender().password.text().strip():
            password: str = self.sender().password.text().strip()
        elif get_password():
            password: str = get_password()
        else:
            return

        self.domain_form.setGraphicsEffect(QGraphicsBlurEffect())
        self.user_form.setGraphicsEffect(QGraphicsBlurEffect())
        self.domain_form.setDisabled(True)
        self.user_form.setDisabled(True)

        try:
            connection_data = connect_to_sent_items(
                username=self.sender().username.text().strip(),
                pwd=password,
                primary_email=self.sender().email.text().strip(),
                email_service_address=self.sender().email_service_address.text().strip()
            )

        except Exception as error:
            self.export_error(error)
            return

        if self.user_form.save_credentials.isChecked():
            set_credentials(
                self.sender().email_service_address.text().strip(),
                self.sender().username.text().strip(),
                self.sender().email.text().strip(),
                password
            )

        self.directory = QFileDialog.getExistingDirectory(
            self,
            'Select Directory',
            os.path.expanduser('~/Downloads')
        )

        if not self.directory:
            self.hide_progress_bar()
            return

        self.progress_bar.setValue(0)
        self.progress_group.show()

        export_contacts_thread = ExportContactsThread(
            connection_data=connection_data,
            username=self.sender().username.text(),
            domain_list=set(domain_list),
            path=self.directory,
            parent=self
        )

        export_contacts_thread.success.connect(self.export_success)
        export_contacts_thread.emails_amount.connect(self.set_maximum_value)
        export_contacts_thread.next_value.connect(self.change_progress_bar)
        export_contacts_thread.error.connect(self.export_error)
        export_contacts_thread.start()

    def set_maximum_value(self, max_value):
        self.max_progress_value = max_value

    def change_progress_bar(self, next_value):
        value = next_value * (100 / self.max_progress_value)
        self.progress_bar.setValue(value)
        self.progress_label.setText(f'Processing: {next_value}/{self.max_progress_value}')

    def export_success(self):
        self.hide_progress_bar()
        self.user_form.password.clear()
        success_message = 'Congratulations! The report has been generated successfully. \
        Now you can change the settings and generate another report.'
        success_popup = SuccessPopUp(success_message, parent=self.domain_form)
        self.domain_form.popup_layout.itemAt(1).widget().deleteLater()
        self.domain_form.popup_layout.insertWidget(
            1, success_popup, alignment=Qt.AlignLeft | Qt.AlignTop
        )

    def export_error(self, exception):
        self.hide_progress_bar()

        if isinstance(exception, ExportContactException):
            message = str(exception)
            LOGGER.error(f'Error. Full error text: {str(exception)}')
        else:
            message = 'Unknown error'
            LOGGER.error(f'Unknown error. Full error text: {str(exception)}')

        error_popup = ErrorPopUp(message, parent=self.domain_form)

        self.domain_form.popup_layout.itemAt(1).widget().deleteLater()
        self.domain_form.popup_layout.insertWidget(
            1, error_popup, alignment=Qt.AlignLeft | Qt.AlignTop
        )

    def hide_progress_bar(self):
        self.progress_group.hide()

        self.user_form.setGraphicsEffect(None)
        self.domain_form.setGraphicsEffect(None)

        self.domain_form.setDisabled(False)
        self.user_form.setDisabled(False)


class ExportContactsThread(QThread):
    success = pyqtSignal()
    error = pyqtSignal(Exception)
    emails_amount = pyqtSignal(int)
    next_value = pyqtSignal(int)

    def __init__(self, connection_data, username, domain_list, path, parent=None):
        super().__init__(parent)

        self.connection_data = connection_data
        self.username = username
        self.domain_list = domain_list
        self.path = path

    def run(self):

        try:
            self.emails_amount.emit(
                get_all_emails_amount(self.connection_data)
            )

            for index in export(self.connection_data, self.username, self.domain_list, self.path):
                self.next_value.emit(index)

        except ExportContactException as exception:
            self.error.emit(exception)
        else:
            self.success.emit()
