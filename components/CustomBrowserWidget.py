from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from qfluentwidgets import setThemeColor, CommandBar, Action, LineEdit, FluentIcon, TabBar

from PyQt5.QtWebEngineWidgets import QWebEngineView

setThemeColor('#2A82E4')


# class TabInterface(QtWidgets.QFrame):
#     def __init__(self, webview, objectName, parent=None):
#         super().__init__(parent=parent)
#
#         self.vBoxLayout = QtWidgets.QVBoxLayout(self)
#         self.vBoxLayout.addWidget(webview)
#
#         self.setObjectName(objectName)


class BrowserWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(1600, 900)

        self.vBoxLayout = QtWidgets.QVBoxLayout(self)
        self.hBoxLayout = QtWidgets.QHBoxLayout(self)

        # 控件栏
        self.commandBar = CommandBar()
        self.commandBar.setMinimumWidth(160)
        self.commandBar.addAction(Action(FluentIcon.LEFT_ARROW, 'Back'))
        self.commandBar.addAction(Action(FluentIcon.RIGHT_ARROW, 'Forward'))
        self.commandBar.addAction(Action(FluentIcon.SYNC, 'Refresh'))

        # 导航栏
        self.urlLineEdit = LineEdit()
        # self.urlLineEdit.returnPressed.connect(self.navigateToUrl)

        self.hBoxLayout.addWidget(self.commandBar)
        self.hBoxLayout.addWidget(self.urlLineEdit)

        # 标签栏
        self.tabBar = TabBar(self)

        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(True)
        self.tabBar.setTabSelectedBackgroundColor(QtGui.QColor(255, 255, 255, 255), QtGui.QColor(255, 255, 255, 50))
        self.tabBar.setScrollable(True)
        # self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

        self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)
        # self.tabBar.currentChanged.connect(lambda i: print(self.tabBar.tabText(i)))
        # self.tabBar.currentChanged.connect(self.onTabChanged)
        # self.tabBar.tabAddRequested.connect(self.onTabAddRequested)

        self.interface = QtWidgets.QStackedWidget(self)
        self.interface.setObjectName("interface")

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.interface, 1)

        self.setLayout(self.vBoxLayout)

        # ----------------------- 测试 -----------------------
        self.webview = QWebEngineView(self)
        self.webview.load(QtCore.QUrl("https://www.baidu.com"))
        self.webview.urlChanged.connect(self.renewUrlBar)
        # self.createTab(self.webview)

        # ----------------------- END -----------------------

    # def createTab(self, webview):
    #     # print(webview.url())
    #     # routeKey = self.currentUrl
    #     self.tabBar.addTab(routeKey, routeKey)
    #     self.interface.addWidget(TabInterface(webview, routeKey, self))
    #
    # def navigateToUrl(self):
    #     url = QtCore.QUrl(self.urlLineEdit.text())
    #     self.webview.setUrl(url)
    #
    def renewUrlBar(self, url):
        url = url.toString()
        self.urlLineEdit.setText(url)
        # self.createTab(self.webview)
        # self.urlbar.setCursorPosition(0)
    #
    # def onTabChanged(self, index):
    #     objectName = self.tabBar.currentTab().routeKey()
    #     self.interface.setCurrentWidget(self.findChild(TabInterface, objectName))
    #     # self.interface.setCurrentWidget(self.interface)
    #
    # def onTabAddRequested(self):
    #     text = f'硝子酱一级棒卡哇伊×{self.tabBar.count()}'
    #     self.addTab(text, text, 'resource/Smiling_with_heart.png')


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = BrowserWidget()
    w.show()
    sys.exit(app.exec_())
