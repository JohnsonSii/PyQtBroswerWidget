from PyQt5 import QtWidgets, QtGui, QtCore
from qfluentwidgets import TabBar
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TabInterface(QtWidgets.QFrame):
    """ Tab interface """

    def __init__(self, widget, objectName, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(objectName)


class TabWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.tabBar = TabBar()

        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(True)
        self.tabBar.setTabSelectedBackgroundColor(QtGui.QColor(255, 255, 255, 255), QtGui.QColor(255, 255, 255, 50))
        self.tabBar.setScrollable(True)
        # self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

        self.tabBar.currentChanged.connect(self.onTabChanged)
        self.tabBar.tabAddRequested.connect(self.onTabAddRequested)

        self.interface = QtWidgets.QStackedWidget(self, objectName='interface')

        self.layout.addWidget(self.tabBar)
        self.layout.addWidget(self.interface)

        self.setLayout(self.layout)

    def onTabChanged(self, index: int):
        objectName = self.tabBar.currentTab().routeKey()
        self.interface.setCurrentWidget(self.findChild(TabInterface, objectName))
        self.interface.setCurrentWidget(self.interface)

    def onTabAddRequested(self):
        text = f'硝子酱一级棒卡哇伊×{self.tabBar.count()}'
        self.addTab(text, text, 'resource/Smiling_with_heart.png')

    def addTab(self, routeKey, widget):
        self.tabBar.addTab(routeKey, text)
        self.interface.addWidget(TabInterface(widget, routeKey, self))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = TabWidget()
    w.show()
    sys.exit(app.exec_())
