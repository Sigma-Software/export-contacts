import platform

from PyQt5.QtCore import Qt, QSize, QObject
from PyQt5.QtGui import QPalette, QPixmap, QIcon, QBrush
from PyQt5.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayoutItem,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QScrollBar,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget
)

from ui.widgets.popup import ErrorPopUp
from ui.widgets.crisp import Crisp

PLATFORM = platform.system()

if PLATFORM == 'Windows':
    from ui.styles.Windows.styles import (
        exclude_domains_styles,
        domains_visible_style,
        domains_invisible_style
    )
elif PLATFORM == 'Darwin':
    from ui.styles.Darwin.styles import (
        exclude_domains_styles,
        domains_visible_style,
        domains_invisible_style
    )


class DomainsForm(QWidget):
    """Widget of the right side of application"""

    ADD_BUTTON_SIZE = 13
    BACKGROUND_IMAGE_SIZE = 800
    DOMAIN_SPACING = 10
    EMPTY_SPACER = 0
    INFO_HEIGHT = 210
    INFO_MARGIN_TOP = 30
    INFO_SPACING = 10
    INPUT_LENGTH = 25
    MARGIN = 4
    PADDING = 23
    POPUP_WIDTH = 1
    ROW_WIDTH = 0
    SPACING = 5
    ZERO_MARGIN = 0

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.domain_list = []

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        background_image = QPixmap(
            ':/resources/styles/common/icons/background.png'
        )
        background_image = background_image.scaled(
            self.BACKGROUND_IMAGE_SIZE,
            self.BACKGROUND_IMAGE_SIZE,
            Qt.IgnoreAspectRatio
        )
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

        self.setStyleSheet(exclude_domains_styles)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(self.ZERO_MARGIN)

        self.box = QGroupBox()
        self.layout = QVBoxLayout()
        self.box.setLayout(self.layout)
        self.layout.setSpacing(self.ZERO_MARGIN)
        self.layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )

        self.popup_layout = QHBoxLayout()
        self.popup = ErrorPopUp('')
        self.popup.setObjectName('popup')
        self.popup.setVisible(False)
        self.popup.setLayoutDirection(Qt.RightToLeft)

        self.info_box = QGroupBox(parent=self, objectName='info-box')
        self.info_layout = QVBoxLayout()
        self.info_box.setLayout(self.info_layout)
        self.info_layout.addWidget(QLabel(
            'Welcome to\nExportContact tool',
            parent=self.info_box,
            objectName='header-title'
        ))
        self.info_layout.addWidget(QLabel(
            'Get all recipients from your "Sent Items" folder\n'
            'except the included domains',
            parent=self.info_box,
            objectName='header-text'
        ), alignment=Qt.AlignTop)
        self.layout.addWidget(self.info_box, alignment=Qt.AlignTop)

        self.input_group_box = QGroupBox(parent=self)

        self.title_input = QLineEdit(
            parent=self.input_group_box,
            objectName='title-input'
        )
        self.title_input.setMaxLength(self.INPUT_LENGTH)
        self.title_input.setPlaceholderText('Enter domain name')
        self.title_input.textEdited.connect(
            lambda: self.popup_layout.itemAt(1).widget().setVisible(False)
        )
        self.title_input.setVisible(False)
        self.title_input_layout = QHBoxLayout()
        self.title_input_layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )
        self.title_input_layout.setSpacing(self.ZERO_MARGIN)
        self.title_add_btn = QPushButton(
            parent=self.input_group_box,
            objectName='title-add-btn'
        )
        self.title_add_btn.setFlat(True)
        self.title_input.returnPressed.connect(
            lambda: self.on_add_domain(self.title_input)
        )
        self.title_add_btn.clicked.connect(
            lambda: self.on_add_domain(self.title_input)
        )

        self.scroll = QScrollArea(parent=self)
        self.domain_form = QGroupBox(
            parent=self.scroll,
            objectName='domains-form'
        )
        self.scroll.setWidget(self.domain_form)
        self.scroll.setWidgetResizable(True)

        self.domain_form_layout = QVBoxLayout()
        self.domain_form.setLayout(self.domain_form_layout)

    def on_add_domain(self, title):
        """Slot for adding new excluded domain"""
        if title.text().strip():
            self.domain_list.append(title.text())
            self.render_domains()
            title.clear()

    def on_delete_excluded_domain(self):
        """Slot for deleting excluded domain crisp"""
        del_crisp: QObject = self.sender()
        self.domain_list.remove(del_crisp.title)
        self.render_domains()

    def erase_domains(self):
        """Slot for removing all the crisps from excluded domain form"""
        for layout_index in reversed(range(self.domain_form_layout.count())):
            row: QLayoutItem = self.domain_form_layout.itemAt(layout_index)

            if row.spacerItem():
                self.domain_form_layout.removeItem(row.spacerItem())
                continue

            for widget_index in reversed(range(row.count())):
                if row.itemAt(widget_index).spacerItem():
                    row.removeItem(row.itemAt(widget_index))
                else:
                    row.itemAt(widget_index).widget().deleteLater()

            row.layout().deleteLater()

    def render_domains(self):
        """Slot for drawing excluded domains"""

        self.erase_domains()

        row_layout = QHBoxLayout()
        row_layout.addSpacerItem(QSpacerItem(
            self.EMPTY_SPACER,
            self.EMPTY_SPACER,
            QSizePolicy.MinimumExpanding,
            QSizePolicy.Minimum
        ))
        self.domain_form_layout.addSpacerItem(QSpacerItem(
            self.EMPTY_SPACER,
            self.EMPTY_SPACER,
            QSizePolicy.Minimum,
            QSizePolicy.MinimumExpanding
        ))
        spacing = self.DOMAIN_SPACING
        padding = self.PADDING
        margin = self.MARGIN
        row_width = self.ROW_WIDTH

        for domain in self.domain_list:
            new_crisp = Crisp(domain)
            new_crisp.clicked.connect(self.on_delete_excluded_domain)

            if (row_width + new_crisp.width + spacing - padding + margin >=
                    self.domain_form.width()):
                row_width = self.ROW_WIDTH
                row_layout = QHBoxLayout()
                row_layout.addSpacerItem(QSpacerItem(
                    self.EMPTY_SPACER,
                    self.EMPTY_SPACER,
                    QSizePolicy.MinimumExpanding,
                    QSizePolicy.Minimum
                ))
            row_width += new_crisp.width + spacing
            widget_position = row_layout.count() - 1
            layout_position = self.domain_form_layout.count() - 1
            row_layout.insertWidget(
                widget_position,
                new_crisp,
                alignment=Qt.AlignLeft
            )
            self.domain_form_layout.insertLayout(layout_position, row_layout)

    def change_domain_form_visibility(self, is_visible):
        """Slot for change visibility of domain form"""
        self.exclude_label.setVisible(is_visible)
        self.title_input.setVisible(is_visible)
        self.title_add_btn.setVisible(is_visible)
        self.domain_form.setVisible(is_visible)

        if is_visible:
            self.info_box.setStyleSheet(domains_visible_style)
        else:
            self.domain_list = []
            self.erase_domains()
            self.info_box.setStyleSheet(domains_invisible_style)


class DomainsFormMac(DomainsForm):

    FORM_MARGIN_BOTTOM = 10
    FORM_MARGIN_TOP = 20
    INFO_WIDTH = 370
    INPUT_HEIGHT = 20
    INPUT_MARGIN = 5
    INPUT_WIDTH = 235
    MAX_HEIGHT = 800
    MIN_HEIGHT = 0
    POPUP_HEIGHT = 150
    SCROLL_HEIGHT = 250
    SCROLL_WIDTH = 262
    WIDTH = 250

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.title_input.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.main_layout.setContentsMargins(
            self.ZERO_MARGIN,
            self.FORM_MARGIN_TOP,
            self.FORM_MARGIN_BOTTOM,
            self.ZERO_MARGIN
        )

        self.popup_layout.addSpacerItem(QSpacerItem(
            self.POPUP_WIDTH,
            self.POPUP_HEIGHT,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum
        ))
        self.popup_layout.addWidget(self.popup)
        self.main_layout.addLayout(self.popup_layout)

        self.info_box.setFixedSize(
            self.INFO_WIDTH,
            self.INFO_HEIGHT
        )

        self.info_layout.setContentsMargins(
            self.ZERO_MARGIN,
            self.INFO_MARGIN_TOP,
            self.ZERO_MARGIN,
            self.ZERO_MARGIN
        )
        self.info_layout.setSpacing(self.INFO_SPACING)

        self.input_group_layout = QFormLayout()
        self.input_group_layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN,
        )
        self.input_group_box.setLayout(self.input_group_layout)

        self.exclude_label = QLabel(
            'Exclude domain:',
            parent=self.input_group_box,
            objectName='exclude-label'
        )
        self.exclude_label.setVisible(False)

        self.title_input_group_box = QGroupBox(parent=self.input_group_box)
        self.title_input_group_box.setLayout(self.title_input_layout)
        self.title_input_group_box.setFixedWidth(self.INPUT_WIDTH)
        self.title_input.setFixedHeight(self.INPUT_HEIGHT)
        self.title_input.setVisible(False)
        self.title_add_btn.setFixedHeight(self.INPUT_HEIGHT)
        title_add_icon = QIcon(':/resources/styles/Darwin/icons/plus-icon.png')
        self.title_add_btn.setIcon(title_add_icon)
        self.title_add_btn.setIconSize(QSize(
            self.ADD_BUTTON_SIZE,
            self.ADD_BUTTON_SIZE
        ))
        self.title_add_btn.setVisible(False)
        self.title_input_layout.addWidget(self.title_input)
        self.title_input_layout.addWidget(self.title_add_btn)

        self.input_group_layout.addRow(
            self.exclude_label,
            self.title_input_group_box
        )

        self.scroll.setFixedHeight(self.SCROLL_HEIGHT)
        self.scroll.setFixedWidth(self.SCROLL_WIDTH)
        scroll_bar = QScrollBar()
        self.scroll.setVerticalScrollBar(scroll_bar)

        self.domain_form_layout.setContentsMargins(
            self.ZERO_MARGIN,
            self.INPUT_MARGIN,
            self.ZERO_MARGIN,
            self.INPUT_MARGIN
        )
        self.domain_form_layout.setSpacing(self.SPACING)
        self.domain_form.setMinimumSize(
            self.WIDTH,
            self.MIN_HEIGHT
        )
        self.domain_form.setMaximumSize(
            self.WIDTH,
            self.MAX_HEIGHT
        )
        self.domain_form.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.Minimum
        )
        self.domain_form.setVisible(False)

        self.input_group_layout.addWidget(self.scroll)
        self.layout.addWidget(self.input_group_box, alignment=Qt.AlignTop)
        self.layout.addSpacerItem(QSpacerItem(
            self.EMPTY_SPACER,
            self.EMPTY_SPACER,
            QSizePolicy.Minimum,
            QSizePolicy.MinimumExpanding
        ))

        self.main_layout.addWidget(self.box, alignment=Qt.AlignHCenter)
        self.setLayout(self.main_layout)


class DomainsFormWin(DomainsForm):

    FORM_MARGIN_LEFT = 14
    FORM_MARGIN_RIGHT = 15
    FORM_MARGIN_TOP = 20
    INFO_WIDTH = 405
    INPUT_BOX_HEIGHT = 90
    INPUT_HEIGHT = 32
    MARGIN_LEFT = 1
    MARGIN_TOP = 5
    POPUP_HEIGHT = 105
    SCROLL_HEIGHT = 350

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.main_layout.setContentsMargins(
            self.FORM_MARGIN_LEFT,
            self.FORM_MARGIN_TOP,
            self.FORM_MARGIN_RIGHT,
            self.ZERO_MARGIN,
        )

        self.popup_layout.addSpacerItem(QSpacerItem(
            self.POPUP_WIDTH,
            self.POPUP_HEIGHT,
            QSizePolicy.Minimum,
            QSizePolicy.Minimum
        ))
        self.popup_layout.addWidget(self.popup)

        self.main_layout.addLayout(self.popup_layout)

        self.info_box.setFixedSize(
            self.INFO_WIDTH,
            self.INFO_HEIGHT
        )
        self.info_layout.setContentsMargins(
            self.ZERO_MARGIN,
            self.INFO_MARGIN_TOP,
            self.ZERO_MARGIN,
            self.ZERO_MARGIN
        )
        self.info_layout.setSpacing(self.INFO_SPACING)

        self.input_group_box.setFixedHeight(self.INPUT_BOX_HEIGHT)
        self.input_group_layout = QVBoxLayout()
        self.input_group_layout.setContentsMargins(
            self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN, self.ZERO_MARGIN
        )
        self.input_group_box.setLayout(self.input_group_layout)

        self.exclude_label = QLabel(
            'Exclude domain',
            parent=self.input_group_box,
            objectName='exclude-label'
        )
        self.exclude_label.setVisible(False)
        self.input_group_layout.addWidget(
            self.exclude_label,
            alignment=Qt.AlignBottom
        )

        self.title_input.setFixedHeight(self.INPUT_HEIGHT)
        self.title_add_btn.setFixedHeight(self.INPUT_HEIGHT)
        title_add_icon = QIcon(':/resources/styles/Windows/icons/plus-icon.png')
        self.title_add_btn.setIcon(title_add_icon)
        self.title_add_btn.setIconSize(QSize(
            self.ADD_BUTTON_SIZE,
            self.ADD_BUTTON_SIZE
        ))
        self.title_add_btn.setVisible(False)
        self.title_input_layout.addWidget(self.title_input)
        self.title_input_layout.addWidget(self.title_add_btn)

        self.input_group_layout.addLayout(self.title_input_layout)

        self.layout.addWidget(self.input_group_box, alignment=Qt.AlignTop)

        self.scroll.setFixedHeight(self.SCROLL_HEIGHT)
        self.domain_form_layout.setContentsMargins(
            self.MARGIN_LEFT,
            self.MARGIN_TOP,
            self.ZERO_MARGIN,
            self.ZERO_MARGIN
        )
        self.domain_form_layout.setSpacing(self.SPACING)
        self.domain_form.setVisible(False)

        self.layout.addWidget(self.scroll, alignment=Qt.AlignTop)
        self.layout.addSpacerItem(QSpacerItem(
            self.ZERO_MARGIN,
            self.ZERO_MARGIN,
            QSizePolicy.Minimum,
            QSizePolicy.MinimumExpanding))

        self.main_layout.addWidget(self.box, alignment=Qt.AlignHCenter)
        self.setLayout(self.main_layout)
