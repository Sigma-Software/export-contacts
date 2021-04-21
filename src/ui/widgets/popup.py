import platform

from PyQt5.QtCore import Qt, QSize, QObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSizePolicy,
    QWidget
)


PLATFORM: str = platform.system()

if PLATFORM == 'Windows':
    from ui.styles.Windows.styles import (
        error_popup_style,
        success_popup_style
    )
elif PLATFORM == 'Darwin':
    from ui.styles.Darwin.styles import (
        error_popup_style,
        success_popup_style
    )


class PopUp(QWidget):
    """Custom PopUp notification widget"""

    BODY_WIDTH = 530
    COL_ROW_SPAN = 1
    ERROR_MESSAGE = 'Error'
    FIRST_COL = 0
    FIRST_ROW = 1
    ICON_SIZE = 30
    MARGIN_RIGHT = 5
    MAX_HEIGHT = 105
    MESSAGE_WIDTH = 450
    MIN_HEIGHT = 85
    SECOND_ROW = 2
    SECOND_COL = 1
    STRETCH_HIGH = 20
    STRETCH_WIDTH = 0
    SUCCESS_MESSAGE = 'Success'
    THIRD_COL = 2
    WIDTH = 538
    ZERO_MARGIN = 0

    def __init__(self, message: str, parent: QObject = None):
        super().__init__(parent)

        self.icon_size: int = self.ICON_SIZE

        self.setMinimumSize(self.WIDTH, self.MIN_HEIGHT)
        self.setMaximumSize(self.WIDTH, self.MAX_HEIGHT)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )
        self.main_layout.setSpacing(self.ZERO_MARGIN)

        self.main_group_box = QGroupBox(objectName="main")
        self.group_box_layout = QHBoxLayout()
        self.group_box_layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )
        self.group_box_layout.setSpacing(self.ZERO_MARGIN)
        self.group_box = QGroupBox(parent=self, objectName="body")
        self.group_box.setFixedWidth(self.BODY_WIDTH)

        self.body_layout = QGridLayout()
        self.body_layout.setVerticalSpacing(self.ZERO_MARGIN)
        self.body_layout.setHorizontalSpacing(self.ZERO_MARGIN)
        self.body_layout.setColumnStretch(
            self.STRETCH_WIDTH,
            self.STRETCH_HIGH
        )
        self.body_layout.setContentsMargins(
            self.ZERO_MARGIN,
            self.ZERO_MARGIN,
            self.MARGIN_RIGHT,
            self.ZERO_MARGIN
        )
        self.body_layout.setAlignment(Qt.AlignRight)

        self.icon = QLabel(parent=self.group_box, objectName='icon')
        self.icon.setPixmap(QPixmap())

        self.type_widget = QLabel(parent=self.group_box, objectName='type-msg')

        self.message_widget = QLabel(parent=self.group_box, objectName='message')
        self.message_widget.setFixedWidth(self.MESSAGE_WIDTH)

        self.message_widget.setWordWrap(True)
        self.message: str = message
        self.message_widget.setText(self.message)

        self.close_btn = QPushButton(objectName='close-btn')
        self.close_btn.setFlat(True)
        self.close_btn.setIcon(QIcon(
            f':/resources/styles/{PLATFORM}/icons/close-green.png'
        ))
        self.close_btn.setIconSize(QSize(self.icon_size, self.icon_size))
        self.close_btn.clicked.connect(self.on_click_popup)

        self.body_layout.addWidget(
            self.close_btn,
            self.FIRST_ROW,
            self.FIRST_COL,
            self.COL_ROW_SPAN,
            self.COL_ROW_SPAN,
            alignment=Qt.AlignLeft
        )
        self.body_layout.addWidget(
            self.type_widget,
            self.FIRST_ROW,
            self.SECOND_COL
        )
        self.body_layout.addWidget(
            self.icon,
            self.FIRST_ROW,
            self.THIRD_COL
        )
        self.body_layout.addWidget(
            self.message_widget,
            self.SECOND_ROW,
            self.SECOND_COL
        )

        self.group_box.setLayout(self.body_layout)
        self.group_box_layout.addWidget(self.group_box, alignment=Qt.AlignLeft)
        self.main_group_box.setLayout(self.group_box_layout)

        self.main_layout.addWidget(self.main_group_box)
        self.setVisible(True)
        self.setLayout(self.main_layout)

    def on_click_popup(self):
        """Slot for closing popup"""
        self.setVisible(False)


class ErrorPopUp(PopUp):
    def __init__(self, message: str, parent: QObject = None):
        super().__init__(message, parent)

        self.setStyleSheet(error_popup_style)
        self.type_widget.setText(self.ERROR_MESSAGE)
        self.icon.setPixmap(QPixmap(
            f':/resources/styles/{PLATFORM}/icons/error.png'
        ))
        self.close_btn.setIcon(QIcon(
            f':/resources/styles/{PLATFORM}/icons/close-red.png'
        ))


class SuccessPopUp(PopUp):
    def __init__(self, message: str, parent: QObject = None):
        super().__init__(message, parent)

        self.setStyleSheet(success_popup_style)
        self.type_widget.setText(self.SUCCESS_MESSAGE)
        self.icon.setPixmap(QPixmap(
            f':/resources/styles/{PLATFORM}/icons/success.png'
        ))
        self.close_btn.setIcon(QIcon(
            f':/resources/styles/{PLATFORM}/icons/close-green.png'
        ))
