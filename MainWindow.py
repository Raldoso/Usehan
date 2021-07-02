from LinkContainer import Link_container
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from modules.functions import *
import sys

app = QApplication(sys.argv)
data = json.load(open(DATABASE,"r"))

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.buttons = []

        self.LayoutInit()
        self.initUI()
        self.initSession()

    def LayoutInit(self):
        
        self.rootLayout = QVBoxLayout()
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.rootLayout.setSpacing(0)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.setContentsMargins(0,0,0,0)
        self.titleLayout.setSpacing(0)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setContentsMargins(0,0,0,0)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setAlignment(Qt.AlignLeft)

        self.tabLayout = QVBoxLayout()
        self.tabLayout.setContentsMargins(0,0,0,0)
        self.tabLayout.setSpacing(0)
        self.tabLayout.setAlignment(Qt.AlignTop)

        self.SessionLayout = QVBoxLayout()
        self.SessionLayout.setContentsMargins(0,0,0,0)
        self.SessionLayout.setSpacing(0)
        self.SessionLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.contentRootLayout = QVBoxLayout()
        self.contentRootLayout.setContentsMargins(0,0,0,0)
        self.contentRootLayout.setSpacing(0)
        self.contentRootLayout.setAlignment(Qt.AlignTop)

        self.contentTitleLayout = QVBoxLayout()
        self.contentTitleLayout.setContentsMargins(0,0,0,0)
        self.contentTitleLayout.setSpacing(0)
        self.contentTitleLayout.setAlignment(Qt.AlignLeft)
        
        self.contentLinkLayout = QVBoxLayout()
        self.contentLinkLayout.setContentsMargins(0,0,0,0)
        self.contentLinkLayout.setSpacing(5)
        self.contentLinkLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

    def initUI(self):

        #SESSION VIEW
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

        #CONTENT TITLE VIEW
        
        launch = QPushButton()
        launch.setText("Launch")
        launch.setStyleSheet("""
            QPushButton{
                max-width: 140px;
                min-width: 140px;
                max-height: 40px;
                min-height: 40px;
                background-color: #deeb34;
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;
                font: bold 25px;
                color: #181F0A;
                margin-top: 15px;
                margin-left: 20px;
                margin-bottom: 20px;
                }""")

        self.contentTitleLayout.addWidget(launch)

        contentTitle = QWidget()
        contentTitle.setLayout(self.contentTitleLayout)
        #CONTENT LINK VIEW

        contentLink = QWidget()
        contentLink.setLayout(self.contentLinkLayout)

        #CONTENT ROOT VIEWű
        self.contentRootLayout.addWidget(contentTitle)
        self.contentRootLayout.addWidget(contentLink)

        contentRoot = QWidget()
        contentRoot.setLayout(self.contentRootLayout)

        #CONTENT VIEW
        self.contentLayout.addWidget(tabs)
        self.contentLayout.addWidget(contentRoot)

        content = QWidget()
        content.setProperty("content","true")
        content.setLayout(self.contentLayout)

        #TITLEBAR VIEW
        titletext = QLabel()
        titletext.setStyleSheet(""" 
            QLabel {
                color: #E6F0D1;
                margin-left: 5px;
                font-size: 30px;
                font-weight: bold;
                }""")
        titletext.setText("Usehan")

        exitbutton = QPushButton()
        exitbutton.setText("X")
        exitbutton.clicked.connect(lambda: sys.exit())
        exitbutton.setProperty("exit","true")

        self.titleLayout.addWidget(titletext)
        self.titleLayout.addWidget(exitbutton)
        self.titleLayout.setAlignment(titletext,Qt.AlignLeft)
        self.titleLayout.setAlignment(Qt.AlignVCenter)

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

    #DETECT WINDOW POSITION WHEN MOUSE PRESSED
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)
    #CHANGE WINDOW POSITION RELATIVE TO MOUSE POSITION
    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)
    #SET BACK EVERYTHING TO DEFAULT
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)


    def resizeEvent(self, event):
        print(event)

        
    #READ DATA FROM DAATBASE AND SHOW IT
    def initSession(self):
        data = json.load(open(DATABASE,"r"))
        titles = [title for title in data.keys()]
        titles.sort()

        for title in titles:
            if len(title) > 14:
                print(f"Session name must be less than 14 characters: {title}")
                sys.exit()
            button = QPushButton(title,self)
            button.setCheckable(True)
            button.clicked.connect(self.clickeds)
            button.setProperty("sessionbutton","true")
            self.SessionLayout.addWidget(button)
            self.buttons.append(button)

    def clickeds(self):

        sender = self.sender()
        title = sender.text()
        links = data[title]

        #sessionbuttom style change
        if sender.isChecked():
            for i in self.buttons:
                i.setChecked(False)
        sender.setChecked(True)

        #clear layout
        for i in reversed(range(self.contentLinkLayout.count())): 
            self.contentLinkLayout.itemAt(i).widget().setParent(None)

        #paste new session links
        for link in links:
            self.contentLinkLayout.addWidget(Link_container(link["title"],link["url"]))


        


#Apply stylesheet
style1 = open(relpath(r"QSS\widgets.qss"),"r").read()
style2 = open(relpath(r"QSS\layouts.qss"),"r").read()
app.setStyleSheet(style1 + style2)

window = Window()
window.show()
app.exec_()

