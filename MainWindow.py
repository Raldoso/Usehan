from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os

app = QApplication(sys.argv)
dirpath = os.path.dirname(__file__)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        #self.setWindowFlags(Qt.FramelessWindowHint)

        #LAYOUT INITIALISATIOn
        rootLayout = QVBoxLayout()
        rootLayout.setContentsMargins(0,0,0,0)
        rootLayout.setSpacing(0)

        titleLayout = QHBoxLayout()
        titleLayout.setContentsMargins(0,0,0,0) 
        titleLayout.setSpacing(0)
        titleLayout.setAlignment(Qt.AlignRight)

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0,0,0,0)
        contentLayout.setSpacing(0)

        tabLayout = QVBoxLayout()
        tabLayout.setContentsMargins(0,0,0,0)
        tabLayout.setSpacing(0)
        tabLayout.setAlignment(Qt.AlignTop)

        SessionLayout = QVBoxLayout()
        SessionLayout.setContentsMargins(0,0,0,0)
        SessionLayout.setSpacing(0)
        SessionLayout.setAlignment(Qt.AlignTop)

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

        SessionLayout.addWidget(session1)
        SessionLayout.addWidget(session2)

        Sessions = QWidget()
        Sessions.setProperty("SessionLayout","true")
        Sessions.setLayout(SessionLayout)

        #TAB VIEW
        search = QLineEdit()
        search.setProperty("searchbar","true")

        tabLayout.addWidget(search)
        tabLayout.addWidget(Sessions)

        tabs = QWidget()
        tabs.setLayout(tabLayout)

        #CONTENT VIEW
        contentLayout.addWidget(tabs)
        
        content = QWidget()
        content.setProperty("content","true")
        content.setLayout(contentLayout)

        #TITLEBAR VIEW
        exitbutton = QPushButton()
        exitbutton.setText("X")
        exitbutton.clicked.connect(lambda: sys.exit())
        exitbutton.setProperty("exit","true")

        titleLayout.addWidget(exitbutton)

        title = QWidget()
        title.setProperty("titlebar","true")
        title.setLayout(titleLayout)

        #ROOT VIEW
        rootLayout.addWidget(title)
        rootLayout.addWidget(content)

        root = QWidget()
        #root = QSizeGrip(self)
        root.setLayout(rootLayout)

        #END
        self.setCentralWidget(root)


    def pressed(self):
        print(f"hello")

#Apply stylesheet
file = open(os.path.join(dirpath,"style.qss"),"r")
file = file.read()
app.setStyleSheet(file)

window = Window()
window.show()
app.exec_()

