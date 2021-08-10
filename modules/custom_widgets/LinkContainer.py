from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from modules.functions import *
import sys


class TitleEdit(QLineEdit):
    def __init__(self,title:str,url:str,session:str,database=None):
        super().__init__()

        self.title = title
        self.url = url
        self.session = session
        self.database = database
        self.setStyleSheet(""" 
            QLineEdit{
                border: 0px;
                max-height: 30px;
                min-width: 250px;
                color: black;
                font-size: 20px;
                background-color: white;
            } 
            QLineEdit:read-only{
                color: #E6F0D1;
                background-color: #779A32;
            } """)
        self.setText(self.title)
        self.setReadOnly(True)
        self.returnPressed.connect(self.TitleChanged)

    def mouseDoubleClickEvent(self, event): #make the title editable
        self.oldtitle = self.title
        if self.isReadOnly() == True:
            self.setReadOnly(False)

    def TitleChanged(self): #return to uneditable mode with the edited title
        self.setReadOnly(True)
        self.title = self.text()

        if self.title is not self.oldtitle:
            modify_title(oldtitle=self.oldtitle,newtitle=self.title,session=self.session,database=self.database)

class Launch_TickBox(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setFixedSize(30,30)

        self.hoverstate = False


    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
    
    def paintEvent(self,event):
        painter  = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(119,154,50))
        painter.drawRect(0,0,30,30)

        painter.setBrush(QColor(64,83,27))
        painter.drawEllipse(2,2,26,26)

        if not self.hoverstate and not self.isChecked(): #not checked not hover

            painter.setBrush(QColor(230,240,209))
            painter.drawEllipse(3,3,24,24)

        elif not self.hoverstate and self.isChecked(): #checked not hover

            painter.setBrush(QColor(230,240,209))
            painter.drawEllipse(3,3,24,24)

            painter.setBrush(QColor(64,83,27))
            painter.drawEllipse(5,5,20,20)

        elif self.hoverstate and not self.isChecked(): #not checked hover

            painter.setBrush(QColor(209,255,112))
            painter.drawEllipse(3,3,24,24)

        elif self.hoverstate and self.isChecked(): #checked hover

            painter.setBrush(QColor(209,255,112))
            painter.drawEllipse(3,3,24,24)

            painter.setBrush(QColor(64,83,27))
            painter.drawEllipse(5,5,20,20)

        painter.end()

    def event(self,event):
        if event.type() == QEvent.HoverEnter:
            self.hoverstate = True
        elif event.type() == QEvent.HoverLeave:
            self.hoverstate = False
        return super().event(event)

class Link_container(QWidget):
    def __init__(self,titletext:str,linktext:str,session:str,database=None):
        super().__init__()
        self.titletext = titletext
        self.linktext = linktext
        self.session = session
        self.database = database
        self.launchable = False
        
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet("""
            QWidget{
                background-color: #779A32;
                max-height: 30px;
                min-height: 30px;
            } 
            QPushButton{
                max-width: 30px;
                min-width: 30px;
            }""")

        self.container = QHBoxLayout()
        self.container.setSpacing(0)
        self.container.setContentsMargins(20,0,20,0)

        self.icon = self.IconInit()
        self.icon.setAttribute(Qt.WA_TranslucentBackground)

        self.title = TitleEdit(self.titletext,self.linktext,session=self.session,database=self.database)

        self.check = QPushButton()
        self.check.setCheckable(True)
        self.check.setIcon(QIcon(CHECK_URL))
        self.check.setIconSize(QSize(30,30))
        self.check.clicked.connect(self.check_url)

        self.tickbox = Launch_TickBox()
        self.tickbox.stateChanged.connect(self.launch_state)

        self.settings = QPushButton()
        self.settings.setStyleSheet("""
            QPushButton{
                max-height: 30px; 
                min-height: 30px;
                max-width: 30px;
                min-width: 30px;
                background: #779A32 url(C:/Users/borhe/Downloads/ItWork/Projects/Usehan/Usehan/Images/settings3.png) no-repeat center center;
            }
            QPushButton:hover {
                background: #779A32 url(C:/Users/borhe/Downloads/ItWork/Projects/Usehan/Usehan/Images/settings3hover.png) no-repeat center center;
            }
        """)
        #self.settings.setIcon(QIcon(DELETE_URL))
        #self.settings.setIconSize(QSize(30,30))

        self.container.addWidget(self.icon)
        self.container.addWidget(self.title)
        self.container.addWidget(self.check)
        self.container.addWidget(self.tickbox)
        self.container.addWidget(self.settings)

        self.setLayout(self.container)

    def IconInit(self): #returns a QLabel with resized image

        image = QLabel()
        iconpath = relpath(r"icons\{0}.png".format(hash_title(self.linktext))) #get filepath by title hash

        #set basic icon for not downloadable url icon images
        if os.path.exists(iconpath) == False:
            iconpath = relpath(LOAD_NO_ICON)
            
        icon = QPixmap(iconpath)
        image.setPixmap(icon)

        return image

    def check_url(self, url):
        if self.check.isChecked():
            self.title.setReadOnly(False)
            self.title.setText(self.linktext)
            
        else:
            self.title.setReadOnly(True)
            self.title.setText(self.titletext)

    def launch_state(self):
        self.launchable = self.tickbox.isChecked()

if __name__ == "__main__":
    class valami(QMainWindow):
        def __init__(self):
            super().__init__()

            layout = QVBoxLayout()

            #data = json.load(open(DATABASE,"r"))
            #data = data["Embedd Python"]
            #for i in data:
            #    layout.addWidget(Link_container(i["title"],i["url"]))

            layout.addWidget(Launch_TickBox())
            widget = QWidget()
            #widget.setStyleSheet(""" 
            #    QWidget{
            #        background-color: #181F0A;
             #   } """)
            widget.setLayout(layout)
            self.setCentralWidget(widget)


    app = QApplication(sys.argv)

    window = valami()
    window.show()
    app.exec_()
