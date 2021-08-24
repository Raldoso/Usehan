from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from modules.functions import *
from modules.ui.LinkContainer import Link_container
from modules.ui.resize_grid import SideGrip
from modules.ui.hover_widget import Hovered_Widget
from modules.ui.new_things import newLink, newLinkEdit, newSession, newSessionEdit
from modules.ui.settings import SessionSettingsContainer
import sys

app = QApplication(sys.argv)
data = json.load(open(DATABASE,"r"))

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setWindowFlags(Qt.FramelessWindowHint)
        
 
        self.setMinimumWidth(600)
        self.buttons = []
        self.current_session = ""

        #init resize grips
        self.gripSize = 4
        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge), 
            SideGrip(self, Qt.TopEdge), 
            SideGrip(self, Qt.RightEdge), 
            SideGrip(self, Qt.BottomEdge), 
            ]
        # corner grips should be "on top" of everything, otherwise the side grips
        # will take precedence on mouse events, so we are adding them *after*;
        # alternatively, widget.raise_() can be used
        self.cornerGrips = [QSizeGrip(self) for i in range(4)]

        self.LayoutInit()
        self.initUI()
        self.initSession()

    #INITIALISATIONS
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

        self.contentTitleLayout = QHBoxLayout()
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
        launch.clicked.connect(self.launch)
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
                margin: 15 8 20 20;
                }
            QPushButton:pressed{
                background-color: #FFBF1F;
            }
            QPushButton:hover{
                border: 3px solid #E6F0D1;
                }""")

        #EXCEPTION ABOUT self.
        self.sessionSettings = QPushButton()
        self.sessionSettings.setCheckable(True)
        self.sessionSettings.clicked.connect(self.showSessionSettings)
        self.sessionSettings.setStyleSheet("""
            QPushButton{
                    max-height: 40px; 
                    min-height: 40px;
                    max-width: 40px;
                    min-width: 40px;
                    border-top-right-radius: 20px;
                    border-bottom-right-radius: 20px;
                    margin: 15 0 20 8;
                    background: #779A32 url(Images/settings3.png) no-repeat center center;
                }
                QPushButton:hover{
                    background: #779A32 url(Images/settings3hover.png) no-repeat center center;
                }
                QPushButton:checked{
                    background: #779A32 url(Images/settings3hoverotate.png) no-repeat center center;
                }
            """)

        #EXCEPTION ABOUT self.
        self.new_link = newLink()
        self.new_link.setDisabled(True)
        self.new_link.clicked.connect(self.addnewLink)

        self.contentTitleLayout.addWidget(launch)
        self.contentTitleLayout.addWidget(self.sessionSettings)
        self.contentTitleLayout.addWidget(self.new_link,Qt.AlignCenter,Qt.AlignRight)

        contentTitle = QWidget()
        contentTitle.setLayout(self.contentTitleLayout)

        #CONTENT LINK VIEW
        contentLink = QWidget()
        contentLink.setLayout(self.contentLinkLayout)

        #CONTENT ROOT VIEW
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
                    background-color: #40531B;
                    margin-left: 5px;
                    font-size: 30px;
                    font-weight: bold;
                    }""")
        titletext.setText("Usehan")

        exitbutton = QPushButton()
        exitbutton.setText("X")
        exitbutton.clicked.connect(lambda: sys.exit())
        exitbutton.setStyleSheet("""
                QPushButton{
                    max-width: 40px;
                    min-width: 40px;
                    max-height: 40px;
                    min-height: 40px;
                    color: #E6F0D1;
                    font-weight: bold;
                    font-family: Eras Bold ITC;
                    font-size: 20px;
                    background-color: #779A32;
                }
                QPushButton:hover {
                    border: 3px solid #E6F0D1;
                }""")

        self.titleLayout.addWidget(titletext,Qt.AlignVCenter,Qt.AlignLeft)
        self.titleLayout.addWidget(exitbutton,Qt.AlignVCenter,Qt.AlignRight)
        #EXCEPTION ABOUT self.
        self.title = Hovered_Widget()
        self.title.setFixedHeight(40)
        self.title.setLayout(self.titleLayout)

        #ROOT VIEW
        self.rootLayout.addWidget(self.title)
        self.rootLayout.addWidget(content)

        root = QWidget()
        root.setLayout(self.rootLayout)
        
        #END
        self.setCentralWidget(root)

    #WINDOW MOVEMENT MANEGEMENT
    def mousePressEvent(self, event):   #DETECT WINDOW POSITION WHEN MOUSE PRESSED
        if event.button() == Qt.LeftButton and self.title.hoverstate == True:
            self.offset = event.pos()
        else:
            self.offset = None
            super().mousePressEvent(event)
    def mouseMoveEvent(self, event):    #CHANGE WINDOW POSITION RELATIVE TO MOUSE POSITION

        #not proud
        try:
            self.offset
        except:
            self.offset = None
        
        if self.offset is not None and event.buttons() == Qt.LeftButton and self.title.hoverstate == True:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event): #SET BACK EVERYTHING TO DEFAULT
        self.offset = None
        super().mouseReleaseEvent(event)

    #DOWNLOAD AND APPEND A NEW LINK TO UI AND database
    def addnewLink(self):
        current_session = ""
        for i in self.buttons:
            if i.isChecked():
                current_session = i.text()

        self.newinput = newLinkEdit(current_session,data,self.contentLinkLayout)

        self.newinput.move(self.geometry().x()+self.width()//2, self.geometry().y()+self.height()//2)
        self.newinput.show()
        #new_link_container = Link_container()

    #SESSION FUNCTION MANEGEMENT
    def initSession(self):     #READ SESSION NAMES FROM DATABASE AND SHOW IT

        titles = [title for title in data.keys()]
        titles.sort()

        for title in titles:
            if len(title) > 14:
                print(f"Session name must be less than 14 characters: {title}")
                sys.exit()
            else:
                button = QPushButton(title,self)
                button.setCheckable(True)
                button.clicked.connect(self.session_clicked)
                button.setProperty("sessionbutton","true")
                self.SessionLayout.addWidget(button)
                self.buttons.append(button)

        self.NewSesBtn = newSession()
        self.NewSesBtn.clicked.connect(self.initNewSessions)
        self.SessionLayout.addWidget(self.NewSesBtn)

        self.NewSesEdit = newSessionEdit()
        self.NewSesEdit.returnPressed.connect(self.createNewSession)
    def session_clicked(self): #CLICKING ON SESION WILL FILL CONTENT WITH LINKS

        self.new_link.setDisabled(False)

        sender = self.sender()
        title = sender.text()
        self.current_session = sender.text()
        links = data[title]

        #sessionbuttom style change
        if sender.isChecked():
            for i in self.buttons:
                i.setChecked(False)
        sender.setChecked(True)

        #clear layout
        for i in reversed(range(self.contentLinkLayout.count())):
            self.contentLinkLayout.itemAt(i).widget().deleteLater()

        #paste new session links
        for link in links:
            self.contentLinkLayout.addWidget(Link_container(link["title"],link["url"],session = title,database = data, rootlayout=self.contentLinkLayout))
    def launch(self):          #LAUNCH SELECTED LINKS IN DEFAULT BROWSER
        for i in reversed(range(self.contentLinkLayout.count())):
            if self.contentLinkLayout.itemAt(i).widget().launchable:
                webbrowser.open(self.contentLinkLayout.itemAt(i).widget().linktext,new=0, autoraise=True)
    def initNewSessions(self): #CREATE LINEEDIT FOR SESSION NAME ENTERING
        self.SessionLayout.itemAt(self.SessionLayout.count()-1).widget().deleteLater()
        self.SessionLayout.addWidget(self.NewSesEdit)
    def createNewSession(self):#CREATE FINAL SESSION BUTTON AND DELETE LINEEDIT
        save_new_session(self.NewSesEdit.text(),data)

        button = QPushButton(self.NewSesEdit.text())
        button.setCheckable(True)
        button.clicked.connect(self.session_clicked)
        button.setProperty("sessionbutton","true")
        self.buttons.append(button)

        #add final session button to layout
        self.SessionLayout.itemAt(self.SessionLayout.count()-1).widget().deleteLater()
        self.SessionLayout.addWidget(button)

        #create new newses button for future session creations
        self.NewSesBtn = newSession()
        self.NewSesBtn.clicked.connect(self.initNewSessions)
        self.NewSesEdit = newSessionEdit()
        self.NewSesEdit.returnPressed.connect(self.createNewSession)
        self.SessionLayout.addWidget(self.NewSesBtn)
    def showSessionSettings(self):
        self.settings = SessionSettingsContainer(self.current_session,data,self.contentLinkLayout,self.SessionLayout,self.buttons)
        corx = self.mapToGlobal(self.sessionSettings.pos()).x()
        cory = self.mapToGlobal(self.sessionSettings.pos()).y()
        if self.sessionSettings.isChecked():
            self.settings.move(QPoint(corx+200,cory+105))
            self.settings.show()
        else:
            self.settings.deleteLater()

    #WINDOW RESIZE MANEGEMENT
    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()
    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
           QRect(outRect.topLeft(), inRect.topLeft()))
        # top right
        self.cornerGrips[1].setGeometry(
           QRect(outRect.topRight(), inRect.topRight()).normalized())
        # bottom right
        self.cornerGrips[2].setGeometry(
           QRect(inRect.bottomRight(), outRect.bottomRight()))
        # bottom left
        self.cornerGrips[3].setGeometry(
           QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(), 
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(), 
            inRect.width(), self.gripSize)
    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.updateGrips()


if __name__ == "__main__":
    #Apply stylesheet
    style1 = open(relpath(r"QSS\widgets.qss"),"r").read()
    style2 = open(relpath(r"QSS\layouts.qss"),"r").read()
    app.setStyleSheet(style1 + style2)
    window = Window()
    window.show()
    app.exec_()

