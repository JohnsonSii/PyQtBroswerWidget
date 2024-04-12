import sys
import uuid

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, QWidget
from qfluentwidgets import setThemeColor, CommandBar, Action, LineEdit, FluentIcon, TabBar, PrimaryPushButton, \
    TabItem, InfoBar, InfoBarIcon, InfoBarPosition

from PyQt5.QtWebEngineWidgets import QWebEngineView

setThemeColor('#2A82E4')
INFORMATION, WARNING, ERROR, SUCCESS = 0, 1, 2, 3


class WebEngineView(QWebEngineView):
    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.mainWindow = mainWindow

    def createWindow(self, QWebEnginePage_WebWindowType):
        newWebview = WebEngineView(self.mainWindow)
        self.mainWindow.createTab(newWebview)
        return newWebview


class TabInterface(QFrame):
    def __init__(self, webview: QWidget, objectName, parent=None):
        super().__init__(parent)
        self.count = 0
        self.webview = webview
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.webview, 1)

        webview.setObjectName(objectName)
        self.setObjectName(f"interface-{objectName}")

    def getWebview(self):
        return self.webview

    def getUrlString(self):
        return self.webview.page().url().toString()

    def countIsEmpty(self):
        return self.count == 0

    def countUp(self):
        self.count += 1

    def countDown(self):
        if self.count - 1 >= 0:
            self.count -= 1


class BrowserWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # init components
        self.vBoxLayout = QVBoxLayout(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.commandBar = CommandBar(self)
        self.backAction = Action(FluentIcon.LEFT_ARROW, 'Back', self)
        self.forwardAction = Action(FluentIcon.RIGHT_ARROW, 'Forward', self)
        self.refreshAction = Action(FluentIcon.SYNC, 'Refresh', self)
        self.urlLineEdit = LineEdit(self)

        self.tabBar = TabBar(self)
        self.interface = QStackedWidget(self)

        self.setupUi()
        
    def setupUi(self):
        self.resize(1600, 900)

        self.commandBar.setMinimumWidth(160)
        self.commandBar.addAction(self.backAction)
        self.commandBar.addAction(self.forwardAction)
        self.commandBar.addAction(self.refreshAction)
        self.commandBar.removeAction(self.forwardAction)

        self.setForwardVisible(True)

        self.backAction.triggered.connect(self.onBackHandle)
        self.forwardAction.triggered.connect(self.onForwardHandle)
        self.refreshAction.triggered.connect(
            lambda: self.findChild(TabInterface,
                                   "interface-" + self.tabBar.currentTab().routeKey()).getWebview().reload())

        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(False)
        self.tabBar.setTabSelectedBackgroundColor(QtGui.QColor(255, 255, 255, 255), QtGui.QColor(255, 255, 255, 50))
        self.tabBar.setScrollable(False)
        # self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        self.tabBar.currentChanged.connect(self.onTabChanged)
        self.tabBar.tabAddRequested.connect(self.onTabAddRequested)
        self.tabBar.tabCloseRequested.connect(self.onTabClosed)

        self.urlLineEdit.returnPressed.connect(self.navigateToUrl)

        self.hBoxLayout.addWidget(self.commandBar)
        self.hBoxLayout.addWidget(self.urlLineEdit)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.interface, 1)

        # -------------- Test Start ----------------

        # self.tabBar.addTab("1", "1")
        # self.tabBar.addTab("2", "2")

        webview = WebEngineView(self)
        webview.setUrl(QUrl("https://www.baidu.com"))
        self.createTab(webview)

        # --------------- Test End -----------------

    def onTabChanged(self, index):
        changedTabBar: TabItem = self.tabBar.items[index]
        routeKey = changedTabBar.routeKey()
        urlString = self.findChild(TabInterface, "interface-" + routeKey).getUrlString()
        self.interface.setCurrentWidget(self.findChild(TabInterface, "interface-" + routeKey))
        self.urlLineEdit.setText(urlString)

    def onTabAddRequested(self):
        webview = WebEngineView(self)
        webview.setUrl(QUrl("https://www.baidu.com"))
        self.createTab(webview)

    def onTabClosed(self, index):
        currentTabBar = self.tabBar.currentTab()
        currentRouteKey = currentTabBar.routeKey()
        closedTabBar = self.tabBar.items[index]
        closedRouteKey = closedTabBar.routeKey()

        tabBarItems = self.tabBar.items

        if len(tabBarItems) <= 1:
            self.showTips(WARNING, "无法关闭最后一个标签页！")
            return

        if currentRouteKey == closedRouteKey:

            if len(tabBarItems) - 1 == index:
                self.tabBar.removeTab(index)
                self.tabBar.setCurrentTab(tabBarItems[index - 1].routeKey())
                self.onTabChanged(index - 1)
                self.findChild(TabInterface, "interface-" + closedRouteKey).close()
            else:
                self.tabBar.removeTab(index)
                self.tabBar.setCurrentTab(tabBarItems[index].routeKey())
                self.onTabChanged(index)
                self.findChild(TabInterface, "interface-" + closedRouteKey).close()

        else:
            self.tabBar.removeTab(index)
            self.findChild(TabInterface, "interface-" + closedRouteKey).close()

    def createTab(self, webview):
        routeKey = str(uuid.uuid4())

        self.tabBar.addTab(routeKey, "正在加载...")
        self.tabBar.setCurrentTab(routeKey)
        self.interface.addWidget(TabInterface(webview, routeKey))
        self.interface.setCurrentWidget(self.findChild(TabInterface, "interface-" + routeKey))
        # self.pages[routeKey] = webview

        webview.loadFinished.connect(self.onLoadFinished)
        webview.urlChanged.connect(self.renewUrlBar)

    def onLoadFinished(self, success):
        # print(self.tabBar.items[0].routeKey())
        if success:
            webview = self.sender()
            objectName = webview.objectName()
            # tabInterface = self.findChild(TabInterface, "interface-" + objectName)
            url = webview.url().toString()
            print(url)
            title = webview.page().title()
            finishedTabBar: TabItem = self.findTabItemByRouteKey(objectName)
            if finishedTabBar is not None:
                finishedTabBar.setText(title)
            # self.tabBar.setTabText(self.tabBar.currentIndex(), title)

    def findTabItemByRouteKey(self, routeKey):
        for item in self.tabBar.items:
            if item.routeKey() == routeKey:
                return item
        return None

    def renewUrlBar(self, url: QUrl):
        urlString = url.toString()
        self.urlLineEdit.setText(urlString)

    def onForwardHandle(self):
        tabInterface: TabInterface = self.findChild(TabInterface, self.tabBar.currentTab().routeKey())
        tabInterface.getWebview().forward()

    def onBackHandle(self):
        tabInterface: TabInterface = self.findChild(TabInterface, self.tabBar.currentTab().routeKey())
        tabInterface.getWebview().back()

    def setForwardVisible(self, visible):
        if not visible:
            self.commandBar.removeAction(self.forwardAction)
            self.commandBar.setMinimumWidth(107)
        else:
            self.commandBar.insertAction(self.forwardAction, self.forwardAction)
            self.commandBar.setMinimumWidth(160)

    def showTips(self, tipType, content):
        if tipType == 0:
            icon = InfoBarIcon.INFORMATION
            title = "信息"
        elif tipType == 1:
            icon = InfoBarIcon.WARNING
            title = "警告"
        elif tipType == 2:
            icon = InfoBarIcon.ERROR
            title = "错误"
        else:
            icon = InfoBarIcon.SUCCESS
            title = "成功"

        infoBar = InfoBar(
            icon=icon,
            title=title,
            content=content,
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

        infoBar.show()

    def navigateToUrl(self):
        url = QUrl(self.urlLineEdit.text())
        if url.scheme() == '':
            url.setScheme('http')
        routeKey = self.tabBar.currentTab().routeKey()
        interface: TabInterface = self.findChild(TabInterface, "interface-" + routeKey)
        interface.getWebview().setUrl(url)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = BrowserWidget()
    w.show()
    app.exec()
