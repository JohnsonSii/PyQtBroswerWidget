from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class WebEngineView(QWebEngineView):
    def __init__(self, dependentWindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.dependentWindow = dependentWindow

    def createWindow(self, QWebEnginePage_WebWindowType):
        newWebview = WebEngineView(self.dependentWindow)
        self.dependentWindow.createTab(newWebview)
        newWebview.setUrl(self.url())
        return newWebview
