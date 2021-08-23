from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import sys

from ..functions import *


class settingsButton(QPushButton):
    def __init__(self,text,icon):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName(u"widgetset")

        self.texts = text
        self.Icon = icon

        self.content = QHBoxLayout()
        self.content.setContentsMargins(0,0,0,0)
        self.content.setSpacing(0)

        self.settingsText = QLabel()
        self.settingsText.setObjectName(u"textset")
        self.settingsText.setStyleSheet("""
            QLabel{
                max-width: 175px;
                min-width: 175px;

                padding: 0 0 0 10;

                color: #E6F0D1;
                font-size: 20px;
                text-align: left;
            }""")
        self.settingsText.setText(self.texts)

        self.settingsIcon = QLabel()
        self.settingsIcon.setObjectName(u"iconset")
        self.settingsIcon.setPixmap(QPixmap(self.Icon).scaled(25,25))
        self.settingsIcon.setStyleSheet("""
            QLabel{
                max-width: 30px;
                min-width: 30px;
                }""")

        self.content.addWidget(self.settingsText)
        self.content.addWidget(self.settingsIcon,Qt.AlignCenter,Qt.AlignRight)
        self.setStyleSheet("""
            QWidget{
                max-height: 30px;
                min-height: 30px;
            }
            #widgetset:hover{
                    background-color: #FFBF1F;
            }
            #widgetset{
                max-width: 200px;
                min-width: 200px;

                background-color: #779A32;
            }""")

        self.setLayout(self.content)

class SessionSettingsContainer(QWidget):
    def __init__(self,session,database,linklayout,sessionlayout,buttons):
        super().__init__()

        self.setObjectName(u"layout")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""
            #layout{
                max-width: 200px;
                min-width: 200px;
                background-color: #181F0A;
            }""")

        self.session = session
        self.database = database
        self.linklayout = linklayout
        self.sessionlayout = sessionlayout
        self.buttons = buttons

        self.container = QVBoxLayout()
        self.container.addSpacing(0)
        self.container.setContentsMargins(0,0,0,0)
        self.container.setAlignment(Qt.AlignTop)

        self.delete = settingsButton("Delete Session",DELETE_URL)
        self.delete.clicked.connect(self.DeleteSession)

        self.container.addWidget(self.delete)
        self.setLayout(self.container)

    def DeleteSession(self):
        delete_session(self.session,self.database) #UPDATE DATABASE
        for i in range(self.linklayout.count()): #UPDATE LINKLAYOUT
            self.linklayout.itemAt(i).widget().deleteLater()
        for i in range(self.sessionlayout.count()): #DELETE SESSION BUTTONS
            if self.sessionlayout.itemAt(i).widget().text() == self.session:
                self.sessionlayout.itemAt(i).widget().deleteLater()
                self.buttons.remove(self.sessionlayout.itemAt(i).widget())



class LinkSettingsContainer(QWidget): #POPUP WIDGET FOR LINK MODIFICATIONS
    def __init__(self,titleEdit,url,session,database,rootlayout):
        super().__init__()

        self.setObjectName(u"layout")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""
            #layout{
                max-width: 200px;
                min-width: 200px;
                background-color: #181F0A;
            }""")

        self.url = url
        self.session = session
        self.title = titleEdit
        self.database = database
        self.rootlayout = rootlayout

        self.container = QVBoxLayout()
        self.container.addSpacing(0)
        self.container.setContentsMargins(0,0,0,0)
        self.container.setAlignment(Qt.AlignTop)

        self.restore = settingsButton("Restore title",RESTORE_TITLE)
        self.restore.clicked.connect(self.RestoreTitle)

        self.delete = settingsButton("Delete link",DELETE_URL)
        self.delete.clicked.connect(self.DeleteLink)

        self.container.addWidget(self.restore)
        self.container.addWidget(self.delete)

        self.setLayout(self.container)

    def RestoreTitle(self):
        original_title = get_url_title(self.url)
        modify_title(self.title.text(),original_title,self.session,self.database)
        self.title.setText(original_title)
        

    def DeleteLink(self):
        delete_link(self.url,self.session,self.database)
        for i in range(self.rootlayout.count()):
            if self.rootlayout.itemAt(i).widget().linktext == self.url:
                self.rootlayout.itemAt(i).widget().deleteLater()

        self.deleteLater()



if __name__ == "__main__":
    class valami(QMainWindow):
        def __init__(self):
            super().__init__()

            

            #layout = LinkSettingsContainer("","")

            #self.setCentralWidget(layout)


    app = QApplication(sys.argv)

    #window = valami()
    #window = LinkSettingsContainer("","")
    #window.show()
    #app.exec_()