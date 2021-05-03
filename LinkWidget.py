from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functions import relpath
import sys

class Link_container(QWidget):
    def __init__(self,iconpath:str,titletext:str,linktext:str):
        super().__init__()
        self.iconpath = iconpath
        self.titletext = titletext
        self.linktext = linktext

        self.setStyleSheet("""
            QWidget{
                background-color: #779A32;
                max-height: 30px;
                /*min-height: 30px;
                min-width: 450px;*/
            } """)

        self.container = QHBoxLayout()
        self.container.setContentsMargins(0,0,0,0)
        self.container.setSpacing(0)

        self.icon = self.IconInit(self.iconpath,30)

        self.title = QLineEdit()
        self.title.setStyleSheet(""" 
            QLineEdit{
                border: 0px;
                max-height: 30px;
                color: black;
                font-family: Eras Bold ITC;
                font-size: 20px;
                background-color: white;
            } 
            QLineEdit:read-only{
                border: 0px;
                max-height: 30px;
                color: #E6F0D1;
                font-family: Eras Bold ITC;
                font-size: 20px;
                background-color: #779A32;
            } """)
        self.title.setText(self.titletext)
        self.title.setReadOnly(True)

        self.container.addWidget(self.icon)
        self.container.addWidget(self.title)

        self.setLayout(self.container)

    def IconInit(self,path,heigth): #returns a QLabel with resized image

        image = QLabel()
        icon = QPixmap(path)
        icon = icon.scaledToHeight(heigth)
        image.setPixmap(icon)

        return image

    def mouseDoubleClickEvent(self,*args):  #make 
        self.title.setReadOnly(False)




class valami(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(Link_container(
            relpath(r"Images\Trash.png"),
            "Qt Style Sheets | Qt Widgets 5.15.3",
            "https://doc.qt.io/qt-5/stylesheet.html"
        ))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = valami()
window.show()
app.exec_()
