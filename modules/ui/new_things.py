from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys

if __name__ != "__main__":
    from ..functions import *
    from .LinkContainer import Link_container

class newSession(QPushButton):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QPushButton{
                max-width: 160px;
                min-width: 160px;
                max-height: 40px;
                min-height: 40px;

                margin: 5px;
                border-radius: 20px;

                color: #E6F0D1;
                font-size: 20px;

                background-color: #779A32;
            }
            QPushButton:pressed {
                background-color: #E6F0D1;
                color:#779A32
            }
            QPushButton:pressed:hover {
                border-color: #779A32
            }
            QPushButton:hover {
                border: 3px solid #E6F0D1;
            }""")

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self,event):
        super().paintEvent(event)

        painter  = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(64,83,27))

        cross_size = 24
        painter.drawRect(int(self.size().width()/2-(cross_size/6)), int(self.size().height()/2-(cross_size/2)),int(cross_size/3),cross_size)
        painter.drawRect(int(self.size().width()/2-(cross_size/2)), int(self.size().height()/2-(cross_size/6)),cross_size,int(cross_size/3))

        painter.end()

class newSessionEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QLineEdit{
                max-width: 160px;
                min-width: 160px;
                max-height: 40px;
                min-height: 40px;
                margin: 5px;
                border-radius: 20px;
                border: 3px solid #E6F0D1;
                color: #E6F0D1;
                font-size: 20px;
                background-color: #779A32;
            }""")
        self.setAlignment(Qt.AlignCenter)

class newLink(QPushButton):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QPushButton{
                max-width: 50px;
                min-width: 50px;
                max-height: 24px;
                min-height: 24px;

                margin: 5px;
                border-radius: 12px;
                border: 2px solid #779A32;

                font-size: 20px;

                background-color: #779A32;
            }
            QPushButton:hover {
                border-color: #E6F0D1;
            }
            QPushButton:pressed:hover {
                background-color: #181F0A;
            }""")
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
    
    def paintEvent(self,event):
        super().paintEvent(event)

        painter  = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(64,83,27))

        cross_size = 18
        painter.drawRect(int(self.size().width()/2-(cross_size/6)), int(self.size().height()/2-(cross_size/2)),int(cross_size/3),cross_size)
        painter.drawRect(int(self.size().width()/2-(cross_size/2)), int(self.size().height()/2-(cross_size/6)),cross_size,int(cross_size/3))

        painter.end()

class newLinkEdit(QLineEdit):
    def __init__(self,session,database,layout):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.textChanged.connect(self.overText)
        self.setStyleSheet(""" 
            QLineEdit{
                max-height: 30px;
                min-height: 30px;
                min-width: 200px;

                color: #181F0A;
                font-family: Eras Bold ITC;
                font-size: 20px;
                background-color: #FFBF1F;

                border: 2px solid #E6F0D1;
            }
            QLineEdit:read-only{
                background-color: #181F0A;
            }""")
        self.returnPressed.connect(self.saveNewLink)

        self.session = session
        self.database = database
        self.root = layout


    def saveNewLink(self):
        self.setReadOnly(True)

        donwload_link(self.text(), self.session,self.database)
        self.root.addWidget(Link_container(get_url_title(self.text()),self.text(),self.session,self.database,self.root))

        self.deleteLater()

    def overText(self):
        width = self.fontMetrics().boundingRect(self.text()).width()
        self.setGeometry(QRect(self.x(),self.y(),width+15,self.height()))


class valami(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("QMainWindow{background-color: #181F0A}")

        self.container = QVBoxLayout()


        self.container.addWidget(newSession(),Qt.AlignCenter,Qt.AlignCenter)
        self.container.addWidget(newSessionEdit(),Qt.AlignCenter,Qt.AlignCenter)

        root = QWidget()
        root.setLayout(self.container)
        self.setCentralWidget(root)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = valami()
    window.show()
    app.exec_()