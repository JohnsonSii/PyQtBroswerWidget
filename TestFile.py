# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

import warnings
from qfluentwidgets import setThemeColor

warnings.filterwarnings("ignore", category=DeprecationWarning)
setThemeColor("#0074D9")


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    app.exec()
