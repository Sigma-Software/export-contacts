import platform

from PyQt5.QtCore import Qt, pyqtSignal, QSize, QObject
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QWidget, QCheckBox
)

from utils.key import get_email, get_email_service_address, get_username, get_password

PLATFORM = platform.system()

if PLATFORM == 'Windows':
    from ui.styles.Windows.styles import (
        user_form_styles,
        export_btn_disabled,
        export_btn_enabled
    )
elif PLATFORM == 'Darwin':
    from ui.styles.Darwin.styles import (
        user_form_styles,
        export_btn_disabled,
        export_btn_enabled
    )


class UserInputForm(QWidget):
    """Widget of the left side of application"""

    visible_domain = pyqtSignal()  # custom signal for visibility of excluded domain form
    connect_event = pyqtSignal()  # custom signal for connection to exchange server

    BACKGROUND_COLOR = '#2b2b2b'
    BUTTON_HEIGHT = 33
    BUTTON_WIDTH = 108
    HEADER_WIDTH = 350
    LOGO_HEIGHT = 100
    MAX_WIDTH = 480
    MIN_WIDTH = 370
    PIXMAP_WIDTH = 164
    PIXMAP_HEIGHT = 45
    ZERO_MARGIN = 0

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.layout = QVBoxLayout()  # main layout of widget

        # Initial configs for widget
        self.setStyleSheet(user_form_styles)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(
            QPalette.Background,
            QColor(self.BACKGROUND_COLOR)
        )
        self.setPalette(palette)
        self.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )
        self.setMinimumWidth(self.MIN_WIDTH)
        self.setMaximumWidth(self.MAX_WIDTH)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Header widget
        self.header_box = QGroupBox(parent=self)
        self.header_box.setFixedWidth(self.HEADER_WIDTH)
        self.header_layout = QVBoxLayout()

        logo = QLabel(parent=self.header_box, objectName='logo')
        logo_pix = QPixmap(':/resources/styles/common/icons/logo.png')
        logo.setPixmap(logo_pix)
        self.header_layout.addWidget(logo)
        self.header_box.setLayout(self.header_layout)

        # Common widgets
        self.user_data_box = QGroupBox(
            parent=self,
            objectName='user-form'
        )
        self.user_data_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.email_service_address = QLineEdit(parent=self.user_data_box)
        self.email_service_address.setPlaceholderText('Enter email service address')
        self.username = QLineEdit(parent=self.user_data_box)
        self.username.setPlaceholderText('Enter username')
        self.email = QLineEdit(parent=self.user_data_box)
        self.email.setPlaceholderText('Enter email')
        self.password = QLineEdit(parent=self.user_data_box)
        if get_password():
            placeholder_text = 'Enter new password'
        else:
            placeholder_text = 'Enter password'

        self.password.setPlaceholderText(placeholder_text)
        self.password.setEchoMode(QLineEdit.Password)  # hide password

        if get_email_service_address():
            self.email_service_address.setText(get_email_service_address())
        if get_username():
            self.username.setText(get_username())
        if get_email():
            self.email.setText(get_email())

        self.export_btn = QPushButton(
            'Export To...',
            parent=self.user_data_box,
            objectName='export_btn'
        )
        self.export_btn.setFixedSize(
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )

        self.on_new_user_input()

        self.email_service_address.textEdited.connect(self.on_new_user_input)
        self.username.textEdited.connect(self.on_new_user_input)
        self.email.textEdited.connect(self.on_new_user_input)
        self.password.textEdited.connect(self.on_new_user_input)

        self.export_btn.clicked.connect(self.connect_clicked_event)

        self.logo_sigma = QLabel(parent=self, objectName='logo_sigma')
        logo_pix = QPixmap(
            ':/resources/styles/common/icons/logo_sigma_outline.png'
        )
        logo_pix = logo_pix.scaled(
            self.PIXMAP_WIDTH,
            self.PIXMAP_HEIGHT,
            Qt.IgnoreAspectRatio
        )
        self.logo_sigma.setPixmap(logo_pix)
        self.logo_sigma.setFixedWidth(self.HEADER_WIDTH)
        self.logo_sigma.setFixedHeight(self.LOGO_HEIGHT)

    def on_new_user_input(self):
        """Slot for check if username, email and email_service_address are entered"""

        email_service_address = bool(self.email_service_address.text().strip())
        username = bool(self.username.text().strip())
        email = bool(self.email.text().strip())
        password = bool(self.password.text().strip() or get_password())

        if username and email and email_service_address and password:
            self.export_btn.setDisabled(False)
            self.export_btn.setStyleSheet(export_btn_enabled)
        else:
            self.export_btn.setDisabled(True)
            self.export_btn.setStyleSheet(export_btn_disabled)

    def connect_clicked_event(self):
        """Event for connection to exchange server"""
        self.connect_event.emit()


class UserInputFormMacOS(UserInputForm):
    """Widget of the left side of application for MacOS"""

    FORM_HEIGHT = 330
    HEADER_WIDTH = 350
    ICON_HEIGHT = 24
    ICON_WIDTH = 45
    INPUT_WIDTH = 227
    MARGIN_BOTTOM = 45
    MARGIN_TOP = 40
    SPACER_TOP = 80
    SPACER_BOTTOM = 10
    SPACING = 20
    WIDTH = 400

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.setStyleSheet(user_form_styles)

        #  Header Box
        self.header_layout.setContentsMargins(
            self.ZERO_MARGIN,
            self.MARGIN_TOP,
            self.ZERO_MARGIN,
            self.MARGIN_BOTTOM
        )
        self.header_layout.setSpacing(self.SPACING)
        self.header_box.setFixedWidth(self.HEADER_WIDTH)

        self.header_layout.addSpacerItem(QSpacerItem(
            self.ZERO_MARGIN,
            self.SPACER_TOP,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum)
        )
        self.header_layout.addWidget(QLabel(
            'Connect',
            parent=self.header_box,
            objectName='header-title'
        ))
        self.header_layout.addSpacerItem(QSpacerItem(
            self.ZERO_MARGIN,
            self.SPACER_BOTTOM,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum)
        )
        self.header_layout.addWidget(QLabel(
            'Enter your Exchange credentials.\n'
            'Unique recipients will be exported from the specified email',
            parent=self.header_box,
            objectName='info'
        ))
        self.header_layout.setSpacing(self.ZERO_MARGIN)
        self.layout.addWidget(self.header_box, alignment=Qt.AlignHCenter)

        # User Data Box
        self.user_data_box.setFixedSize(
            self.WIDTH,
            self.FORM_HEIGHT
        )
        user_data_layout = QFormLayout()
        user_data_layout.setVerticalSpacing(self.SPACING)
        user_data_layout.setLabelAlignment(Qt.AlignRight)
        user_data_layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )
        self.user_data_box.setLayout(user_data_layout)

        self.email_service_address.setFixedWidth(self.INPUT_WIDTH)
        self.username.setFixedWidth(self.INPUT_WIDTH)
        self.email.setFixedWidth(self.INPUT_WIDTH)
        self.password.setFixedWidth(self.INPUT_WIDTH)

        #  Remove blue borders around focused QLineEdit
        self.email_service_address.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.username.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.password.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.email.setAttribute(Qt.WA_MacShowFocusRect, False)

        user_data_layout.addRow(QLabel(
            'Email service address:',
            parent=self.user_data_box,
            objectName='email_service_address-title'
        ), self.email_service_address)
        user_data_layout.addRow(QLabel(
            'Username:',
            parent=self.user_data_box,
            objectName='username-title'
        ), self.username)
        user_data_layout.addRow(QLabel(
            'Email:',
            parent=self.user_data_box,
            objectName='email-title'
        ), self.email)
        user_data_layout.addRow(QLabel(
            'Password:',
            parent=self.user_data_box,
            objectName='password-title'
        ), self.password)

        self.save_credentials = QCheckBox(
            'Save credentials in KeyChain',
            parent=self.user_data_box
        )
        user_data_layout.addRow(None, self.save_credentials)
        self.exclude_domain_switcher = QPushButton(
            '\t\t\tSpecify the domain(s)\n\t\t\tto be excluded from the export',
            parent=self.user_data_box,
            objectName='exclude-switcher'
        )

        self.exclude_domain_switcher.setFlat(True)
        self.exclude_domain_switcher.setCheckable(True)
        self.exclude_domain_switcher.setChecked(False)
        self.exclude_domain_switcher.setIconSize(QSize(
            self.ICON_WIDTH,
            self.ICON_HEIGHT
        ))

        self.switcher_off_icon = QIcon(
            ':/resources/styles/Darwin/icons/switcher.png'
        )
        self.switcher_on_icon = QIcon(
            ':/resources/styles/Darwin/icons/switcher-on.png'
        )

        self.exclude_domain_switcher.setIcon(self.switcher_off_icon)
        self.exclude_domain_switcher.clicked.connect(
            self.exclude_domain_switcher_changed
        )

        user_data_layout.addRow(QLabel(
            'Exclude domain:',
            parent=self.user_data_box,
            objectName='exclude-title'
        ), self.exclude_domain_switcher)

        user_data_layout.addItem(QSpacerItem(
            self.ZERO_MARGIN,
            self.SPACER_BOTTOM,
            QSizePolicy.MinimumExpanding,
            QSizePolicy.Minimum)
        )
        user_data_layout.addWidget(self.export_btn)

        self.layout.addWidget(
            self.user_data_box,
            alignment=Qt.AlignHCenter | Qt.AlignTop
        )
        self.layout.addWidget(
            self.logo_sigma,
            alignment=Qt.AlignHCenter
        )

        self.setLayout(self.layout)

    def exclude_domain_switcher_changed(self):
        """Event for setting visibility of excluded domain form on MacOS"""

        if self.exclude_domain_switcher.isChecked():
            self.exclude_domain_switcher.setIcon(self.switcher_on_icon)
        else:
            self.exclude_domain_switcher.setIcon(self.switcher_off_icon)
        self.visible_domain.emit()


class UserInputFormWin(UserInputForm):
    """Widget of the left side of application for Windows"""

    FORM_HEIGHT = 518
    HEIGHT = 32
    ICON_HEIGHT = 18
    ICON_WIDTH = 43
    MARGIN_RIGHT = 100
    MARGIN_TOP = 25
    SPACING = 10
    SWITCHER_CHECKED = 'On'
    SWITCHER_UNCHECKED = 'Off'
    WIDTH = 350

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        #  Header Box
        self.header_layout.addWidget(QLabel(
            'Connect',
            parent=self.header_box,
            objectName='header-title'
        ))
        self.header_layout.addWidget(QLabel(
            'Enter your Exchange credentials.\n'
            'Unique recipients will be exported from the specified email',
            parent=self.header_box,
            objectName='info'
        ), alignment=Qt.AlignTop)

        self.header_layout.setContentsMargins(
            self.ZERO_MARGIN,
            self.MARGIN_TOP,
            self.ZERO_MARGIN,
            self.ZERO_MARGIN
        )
        self.header_layout.setSpacing(self.SPACING)

        self.layout.addWidget(self.header_box, alignment=Qt.AlignHCenter)

        # User Data Box
        user_data_layout = QVBoxLayout()
        user_data_layout.setContentsMargins(
            self.ZERO_MARGIN,
            self.ZERO_MARGIN,
            self.ZERO_MARGIN,
            self.MARGIN_RIGHT
        )
        self.user_data_box.setLayout(user_data_layout)
        self.user_data_box.setFixedHeight(self.FORM_HEIGHT)
        self.user_data_box.setFixedWidth(self.WIDTH)

        self.email_service_address.setFixedHeight(self.HEIGHT)
        self.username.setFixedHeight(self.HEIGHT)
        self.email.setFixedHeight(self.HEIGHT)
        self.password.setFixedHeight(self.HEIGHT)

        user_data_layout.addWidget(QLabel(
            'Email service address',
            parent=self.user_data_box,
            objectName='email_service_address-title'
        ))
        user_data_layout.addWidget(self.email_service_address)
        user_data_layout.addWidget(QLabel(
            'Username',
            parent=self.user_data_box,
            objectName='username-title'
        ))
        user_data_layout.addWidget(self.username)
        user_data_layout.addWidget(QLabel(
            'Email',
            parent=self.user_data_box,
            objectName='email-title'
        ))
        user_data_layout.addWidget(self.email)
        user_data_layout.addWidget(QLabel(
            'Password',
            parent=self.user_data_box,
            objectName='password-title'
        ))
        user_data_layout.addWidget(self.password)

        self.save_credentials = QCheckBox(
            'Save credentials in Credential Manager',
            parent=self.user_data_box
        )
        user_data_layout.addWidget(self.save_credentials, alignment=Qt.AlignLeft)
        user_data_layout.addWidget(QLabel(
            'Exclude domain',
            parent=self.user_data_box,
            objectName='exclude-title'
        ))

        self.exclude_domain_switcher = QPushButton(
            self.SWITCHER_UNCHECKED,
            parent=self.user_data_box,
            objectName='exclude-switcher'
        )
        self.exclude_domain_switcher.setFlat(True)
        self.exclude_domain_switcher.setCheckable(True)
        self.exclude_domain_switcher.setChecked(False)
        self.exclude_domain_switcher.setIconSize(QSize(
            self.ICON_WIDTH,
            self.ICON_HEIGHT
        ))

        self.switcher_off_icon = QIcon(
            ':/resources/styles/Windows/icons/switcher.png'
        )
        self.switcher_on_icon = QIcon(
            ':/resources/styles/Windows/icons/switcher-on.png'
        )

        self.exclude_domain_switcher.setIcon(self.switcher_off_icon)
        self.exclude_domain_switcher.clicked.connect(self.exclude_domain_switcher_changed)

        user_data_layout.addWidget(self.exclude_domain_switcher, alignment=Qt.AlignLeft)
        user_data_layout.addWidget(QLabel(
            'Specify the domain(s) to be excluded from the export',
            parent=self.user_data_box,
            objectName='exclude-info'
        ))
        user_data_layout.addWidget(self.export_btn)

        self.layout.addWidget(self.user_data_box, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.logo_sigma, alignment=Qt.AlignHCenter)
        self.setLayout(self.layout)

    def exclude_domain_switcher_changed(self):
        """Event for setting visibility of excluded domain form on Windows"""

        if self.exclude_domain_switcher.isChecked():
            self.exclude_domain_switcher.setText(
                self.SWITCHER_CHECKED
            )
            self.exclude_domain_switcher.setIcon(self.switcher_on_icon)
        else:
            self.exclude_domain_switcher.setIcon(self.switcher_off_icon)
            self.exclude_domain_switcher.setText(
                self.SWITCHER_UNCHECKED
            )

        self.visible_domain.emit()
