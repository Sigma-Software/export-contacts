import platform

from PyQt5.QtCore import pyqtSignal, QSize, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


PLATFORM = platform.system()

if PLATFORM == 'Windows':
    from ui.styles.Windows.styles import crisp_styles
elif PLATFORM == 'Darwin':
    from ui.styles.Darwin.styles import crisp_styles


class Crisp(QWidget):
    """Custom domain crisp widget"""

    clicked = pyqtSignal()

    HEIGHT_MAC = 30
    HEIGHT_WIN = 30
    ICON_SIZE_MAC = 14
    ICON_SIZE_WIN = 10
    PADDING = 33
    PIXELS_PER_CHAR = 8.5
    ZERO_MARGIN = 0

    def __init__(self, title: str, parent: QObject = None):
        super().__init__(parent)

        self.title = title

        padding: int = self.PADDING
        pixels_per_char: float = self.PIXELS_PER_CHAR
        close_icn_size: int
        if PLATFORM == 'Windows':
            close_icn_size = self.ICON_SIZE_WIN
            self.setFixedHeight(self.HEIGHT_WIN)
        elif PLATFORM == 'Darwin':
            close_icn_size = self.ICON_SIZE_MAC
            self.setFixedHeight(self.HEIGHT_MAC)

        icon = QIcon(f':/resources/styles/{PLATFORM}/icons/close-white.png')

        layout = QHBoxLayout()
        layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )
        layout.setSpacing(self.ZERO_MARGIN)
        self.setLayout(layout)

        crisp_title = QLabel(self.title, parent=self, objectName='crisp-title')
        self.resize(crisp_title.sizeHint())
        self.close_crisp = QPushButton(parent=self, objectName='close-crisp')
        self.close_crisp.setFlat(True)
        self.close_crisp.setIcon(icon)
        self.close_crisp.setIconSize(QSize(close_icn_size, close_icn_size))
        self.close_crisp.clicked.connect(self.clicked)

        self.width: int = len(title) * pixels_per_char + padding + close_icn_size
        self.setFixedWidth(self.width)
        layout.addWidget(crisp_title)
        layout.addWidget(self.close_crisp)

        self.setStyleSheet(crisp_styles)
