from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os

app = QApplication(sys.argv)
dirpath = os.path.dirname(__file__)

class Color(QWidget):  #custom widget
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        self.resize(30,30)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.LayoutInit()
        self.WindowFilling()

    def LayoutInit(self):
        
        self.rootLayout = QVBoxLayout()
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.rootLayout.setSpacing(0)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.setContentsMargins(0,0,0,0)
        self.titleLayout.setSpacing(0)
        self.titleLayout.setAlignment(Qt.AlignRight)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setContentsMargins(0,0,0,0)
        self.contentLayout.setSpacing(0)

        self.tabLayout = QVBoxLayout()
        self.tabLayout.setContentsMargins(0,0,0,0)
        self.tabLayout.setSpacing(0)
        self.tabLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.SessionLayout = QVBoxLayout()
        self.SessionLayout.setContentsMargins(0,0,0,0)
        self.SessionLayout.setSpacing(0)
        self.SessionLayout.setAlignment(Qt.AlignTop)

    def WindowFilling(self):

        #SESSION VIEW
        session1 = QPushButton()
        session1.setText("Learn Qt")
        session1.clicked.connect(self.pressed)
        session1.setProperty("sessionbutton","true")
        session1.setCheckable(True)

        session2 = QPushButton()
        session2.setText("Github")
        session2.clicked.connect(self.pressed)
        session2.setProperty("sessionbutton","true")

        self.SessionLayout.addWidget(session1)
        self.SessionLayout.addWidget(session2)
        self.SessionLayout.addWidget(Color("red"))

        Sessions = QWidget()
        Sessions.setProperty("self.SessionLayout","true")
        Sessions.setLayout(self.SessionLayout)

        #TAB VIEW
        search = QLineEdit()
        search.setProperty("searchbar","true")

        self.tabLayout.addWidget(search)
        self.tabLayout.addWidget(Sessions)

        tabs = QWidget()
        tabs.setProperty("tabs","true")
        tabs.setLayout(self.tabLayout)

        #CONTENT VIEW
        self.contentLayout.addWidget(tabs)
        self.contentLayout.addWidget(QPushButton())

        content = QWidget()
        content.setProperty("content","true")
        content.setLayout(self.contentLayout)

        #TITLEBAR VIEW
        exitbutton = QPushButton()
        exitbutton.setText("X")
        exitbutton.clicked.connect(lambda: sys.exit())
        exitbutton.setProperty("exit","true")

        self.titleLayout.addWidget(exitbutton)

        title = QWidget()
        title.setProperty("titlebar","true")
        title.setLayout(self.titleLayout)

        #ROOT VIEW
        self.rootLayout.addWidget(title)
        self.rootLayout.addWidget(content)

        root = QWidget()
        root.setLayout(self.rootLayout)

        #END
        self.setCentralWidget(root)


    def pressed(self):
        print(f"hello")

#Apply stylesheet
style1 = open(os.path.join(dirpath,"QSS","widgets.qss"),"r").read()
style2 = open(os.path.join(dirpath,"QSS","layouts.qss"),"r").read()
app.setStyleSheet(style1 + style2)

window = Window()
window.show()
app.exec_()

