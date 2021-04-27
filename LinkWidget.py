from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os

def relpath(path): #working with relatve paths with origin main script
    dirpath = os.path.dirname(__file__)
    return os.path.join(dirpath,path)

class Link_container(QWidget):
    def __init__(self,iconpath:str,titletext:str,linktext:str):
        super().__init__()
        self.iconpath = iconpath
        self.titletext = titletext
        self.linktext = linktext
        self.container = QHBoxLayout()

        self.container.setContentsMargins(0,0,0,0)
        self.container.setSpacing(0)
        

        self.setStyleSheet("""
            QWidget{
                background-color: #779A32;
                max-height: 30px;
                /*min-height: 30px;
                min-width: 450px;*/
            } """)

        self.icon = self.ImageInit(self.iconpath,30)
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

    def ImageInit(self,path,heigth): #returns a QLabel with resized image

        image = QLabel()
        icon = QPixmap(path)
        icon = icon.scaledToHeight(heigth)
        image.setPixmap(icon)

        return image

class valami(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(Link_container(
            relpath(r"Images\Trash.png"),
            "Qt learn",
            "www.google.com"
        ))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = valami()
window.show()
app.exec_()
