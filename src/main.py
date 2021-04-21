import platform
import sys

from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow

app = QApplication(sys.argv)

PLATFORM = platform.system()

MIN_HEIGHT = 700
MAX_WIDTH = 1200
MAX_HEIGHT = 800

if PLATFORM == 'Windows':
    MIN_WIDTH = 1040
elif PLATFORM == 'Darwin':
    MIN_WIDTH = 1030

window = MainWindow(min_width=MIN_WIDTH, min_height=MIN_HEIGHT, max_width=MAX_WIDTH, max_height=MAX_HEIGHT)
window.show()
app.exec_()
