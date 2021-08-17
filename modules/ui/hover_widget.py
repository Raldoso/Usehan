from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#hoverstate return if mouse is over the widget

class Hovered_Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.hoverstate =  False
        self.prev_state = False
        self.setAttribute(Qt.WA_Hover)
        self.setStyleSheet("""
                QWidget:hover{
                    background-color: #ffffff;
                    /*border: 3px solid #E6F0D1;*/
                    
                    }""")

    def event(self, event):
        if event.type() == QEvent.HoverEnter:
            self.prev_state = self.hoverstate
            self.hoverstate = True
        elif event.type() == QEvent.HoverLeave:
            self.hoverstate = self.prev_state
        return super().event(event)