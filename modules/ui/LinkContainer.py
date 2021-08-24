from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from .settings import LinkSettingsContainer
import sys
import os

if __name__ != "__main__":
    from modules.functions import *

class TitleEdit(QLineEdit):
    def __init__(self,parent,title:str,url:str,session:str,database=None):
        super().__init__()

        self.title = title
        self.url = url
        self.session = session
        self.database = database
        self.setStyleSheet(""" 
            QLineEdit{
                border: 0px;
                max-height: 30px;
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
        self.parent = parent
        self.returnPressed.connect(self.TitleChanged)

    def mouseDoubleClickEvent(self, event): #make the title editable
        self.oldtitle = self.title
        if self.isReadOnly() == True:
            self.setReadOnly(False)

    def TitleChanged(self): #return to uneditable mode with the edited title
        self.setReadOnly(True)
        self.title = self.text()
        if self.title != self.oldtitle:
            modify_title(oldtitle=self.oldtitle,newtitle=self.title,session=self.session,database=self.database)
        self.parent.titletext = self.title

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

        painter.setBrush(QColor(64,83,27)) #dark
        painter.drawEllipse(3,3,24,24)

        if not self.hoverstate and not self.isChecked(): #not checked not hover

            painter.setBrush(QColor(230,240,209)) #light
            painter.drawEllipse(5,5,20,20)

        elif not self.hoverstate and self.isChecked(): #checked not hover

            painter.setBrush(QColor(230,240,209)) #light
            painter.drawEllipse(5,5,20,20)

            painter.setBrush(QColor(64,83,27)) #dark
            painter.drawEllipse(8,8,14,14)

        elif self.hoverstate and not self.isChecked(): #not checked hover

            painter.setBrush(QColor(209,255,112)) #light
            painter.drawEllipse(5,5,20,20)

        elif self.hoverstate and self.isChecked(): #checked hover

            painter.setBrush(QColor(209,255,112)) #light
            painter.drawEllipse(5,5,20,20)

            painter.setBrush(QColor(64,83,27)) #dark
            painter.drawEllipse(8,8,14,14)

        painter.end()

    def event(self,event):
        if event.type() == QEvent.HoverEnter:
            self.hoverstate = True
        elif event.type() == QEvent.HoverLeave:
            self.hoverstate = False
        return super().event(event)

class Link_container(QWidget):
    def __init__(self,titletext:str,linktext:str,session:str,database=None,rootlayout = None):
        super().__init__()
        self.titletext = titletext
        self.linktext = linktext
        self.session = session
        self.database = database
        self.launchable = False
        self.rootlayout = rootlayout
        
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

        self.title = TitleEdit(self,self.titletext,self.linktext,session=self.session,database=self.database)

        self.check = QPushButton()
        self.check.setCheckable(True)
        self.check.setStyleSheet("""
                QPushButton{
                   background: #779A32 url(./Images/csek3.png) no-repeat center center;
                   max-height: 30px;
                   max-width: 30px;
                }
                QPushButton:checked{
                    background: #779A32 url(./Images/uncsek4.png) no-repeat center center;
                
                }""")
        self.check.clicked.connect(self.check_url)

        self.tickbox = Launch_TickBox()
        self.tickbox.stateChanged.connect(self.launch_state)

        self.settings_btn = QPushButton()
        self.settings_btn.setCheckable(True)
        self.settings_btn.setStyleSheet("""
            QPushButton{
                max-height: 30px; 
                min-height: 30px;
                max-width: 30px;
                min-width: 30px;
                background: #779A32 url(./Images/settings3.png) no-repeat center center;
            }
            QPushButton:hover {
                background: #779A32 url(./Images/settings3hover.png) no-repeat center center;
            }
            QPushButton:checked {
                background: #779A32 url(./Images/settings3hoverotate.png) no-repeat center center;
            }
            """)
        self.settings_btn.clicked.connect(self.ShowSettings)


        self.container.addWidget(self.icon)
        self.container.addWidget(self.title)
        self.container.addWidget(self.tickbox)
        self.container.addWidget(self.check)
        self.container.addWidget(self.settings_btn)

        self.setLayout(self.container)

    def IconInit(self): #returns a QLabel with resized image

        image = QLabel()
        iconpath = relpath(r"icons\{0}.png".format(hash_url(self.linktext))) #get filepath by title hash

        #set basic icon for not downloadable url icon images
        if os.path.exists(iconpath) == False:
            iconpath = relpath(LOAD_NO_ICON)
            
        icon = QPixmap(iconpath)
        image.setPixmap(icon)

        return image

    def check_url(self):
        if self.check.isChecked():
            self.title.setReadOnly(False)
            self.title.setText(self.linktext)
            
        else:
            self.title.setReadOnly(True)
            self.title.setText(self.titletext)

    def launch_state(self):
        self.launchable = self.tickbox.isChecked()

    def ShowSettings(self):
        self.settings = LinkSettingsContainer(self.title,self.linktext,self.session,self.database,self.rootlayout)
        corx = self.mapToGlobal(self.settings_btn.pos()).x()
        cory = self.mapToGlobal(self.settings_btn.pos()).y()
        if self.settings_btn.isChecked():
            self.settings.move(QPoint(corx,cory+30))
            self.settings.show()
        else:
            self.settings.deleteLater()


if __name__ == "__main__":
    class valami(QMainWindow):
        def __init__(self):
            super().__init__()


            layout = QVBoxLayout()
            layout.addSpacing(0)
            layout.setContentsMargins(0,0,0,0)
            layout.setAlignment(Qt.AlignTop)
         

            path = "\\".join(os.path.normpath(__file__).split(os.sep)[:-3])
            


            #layout.addWidget(settingsButton("Check link",os.path.join(path,r"Images\csek3.png"),None))
            #layout.addWidget(settingsButton("Reset title",os.path.join(path,r"Images\refresh2.png"),None))
            #layout.addWidget(settingsButton("Delete title",DELETE_URL,None))
            widget = QWidget()
            widget.setObjectName(u"BGset")
            widget.setStyleSheet(""" 
                #BGset{
                    background-color: #181F0A;
                } """)
            widget.setLayout(layout)
            self.setCentralWidget(widget)
            self.setLayout(layout)

    app = QApplication(sys.argv)

    window = valami()
    window.show()
    app.exec_()
