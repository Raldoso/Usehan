from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from modules.functions import *
import sys


class TitleEdit(QLineEdit):
    def __init__(self,title:str):
        super().__init__()

        self.title = title
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
        if self.isReadOnly() == True:
            self.setReadOnly(False)

    def TitleChanged(self): #return to uneditable mode with the edited title
        self.setReadOnly(True)
        print(self.text())

class Link_container(QWidget):
    def __init__(self,titletext:str,linktext:str):
        super().__init__()
        self.titletext = titletext
        self.linktext = linktext
        
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

        self.title = TitleEdit(self.titletext)

        self.check = QPushButton()
        self.check.setCheckable(True)
        self.check.setIcon(QIcon(CHECK_URL))
        self.check.setIconSize(QSize(30,30))

        self.delete = QPushButton()
        self.delete.setIcon(QIcon(DELETE_URL))
        self.delete.setIconSize(QSize(30,30))

        self.container.addWidget(self.icon)
        self.container.addWidget(self.title)
        self.container.addWidget(self.check)
        self.container.addWidget(self.delete)

        self.setLayout(self.container)

    def IconInit(self): #returns a QLabel with resized image

        image = QLabel()
        iconpath = relpath(r"icons\{0}.png".format(hash_title(self.titletext))) #get filepath by title hash

        #set basic icon for not downloadable url icon images
        if os.path.exists(iconpath) == False:
            iconpath = relpath(LOAD_NO_ICON)
            
        icon = QPixmap(iconpath)
        image.setPixmap(icon)

        return image



if __name__ == "__main__":
    class valami(QMainWindow):
        def __init__(self):
            super().__init__()

            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignTop)

            data = json.load(open(DATABASE,"r"))

            data = data["Embedd Python"]

            for i in data:
                layout.addWidget(Link_container(i["title"],i["url"]))

            widget = QWidget()
            widget.setStyleSheet(""" 
                QWidget{
                    background-color: #181F0A;
                } """)
            widget.setLayout(layout)
            self.setCentralWidget(widget)


    app = QApplication(sys.argv)

    window = valami()
    window.show()
    app.exec_()
