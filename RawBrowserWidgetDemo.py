from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resize(1600, 900)

        self.tabWidget = QTabWidget()
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)

        self.setCentralWidget(self.tabWidget)

        self.webview = WebEngineView(self)
        self.webview.load(QUrl("http://www.baidu.com"))
        self.create_tab(self.webview)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction("后退", self)
        back_btn.triggered.connect(self.webview.back)
        navtb.addAction(back_btn)

        next_btn = QAction("前进", self)
        next_btn.triggered.connect(self.webview.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("刷新", self)
        reload_btn.triggered.connect(self.webview.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("主页", self)
        navtb.addAction(home_btn)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addSeparator()
        navtb.addWidget(self.urlbar)

        self.webview.urlChanged.connect(self.renew_urlbar)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.webview.setUrl(q)

    def renew_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def create_tab(self, webview):
        tab = QWidget()
        self.tabWidget.addTab(tab, "新建标签页")
        self.tabWidget.setCurrentWidget(tab)

        layout = QHBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(webview)

        # 连接新标签页加载完成的信号到槽函数
        webview.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, success):
        if success:
            webview = self.sender()
            title = webview.page().title()
            index = self.tabWidget.indexOf(webview.parentWidget())
            self.tabWidget.setTabText(index, title[:10])  # 设置标签页标题为页面标题的前10个字符
            self.urlbar.setText(webview.url().toString())  # 更新URL输入栏

    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()


class WebEngineView(QWebEngineView):
    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.create_tab(new_webview)
        return new_webview


app = QApplication(sys.argv)
browser = MainWindow()
browser.show()
sys.exit(app.exec_())
