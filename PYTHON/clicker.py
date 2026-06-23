from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class ClickerWindow(QMainWindow):
    def __init__(self):
        super(ClickerWindow,self).__init__()
        self.setGeometry(0,0,500,300)
        self.setWindowTitle("Clicker!")
        self.clickcount = 0
        self.margin = 10
        self.initUI()
        
    def initUI(self):
        self.font = QtGui.QFont()
        self.font.setPointSize(40)
        self.font.setBold(True)
        self.blue = QtGui.QPalette()
        self.blue.setColor(QtGui.QPalette.WindowText, QtGui.QColor("blue"))
        
        self.counter = QtWidgets.QLabel(self)
        self.counter.setText("Clicks: 0")
        self.counter.move(self.margin,self.margin)
        self.counter.setFont(self.font)
        self.counter.setPalette(self.blue)
        
        self.font.setPointSize(60)
        self.font.setBold(False)
        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setText("Click!") #whoops branch target buffer
        self.btn1.clicked.connect(self.clicked)
        self.btn1.move(self.margin,100)
        self.btn1.setFont(self.font)

        self.font.setPointSize(10)
        self.footer = QtWidgets.QLabel(self)
        self.footer.setText("Copyright Pacifiky 2025 All Rights Reserved")
        self.footer.move(self.margin,250)
        self.footer.setFont(self.font)
        
        self.update()
        
    def showUI(self):
        self.show()
    
    def clicked(self):
        self.clickcount+=1
        self.counter.setText("Clicks: " + str(self.clickcount))
        self.update()
        
    def update(self):
        self.counter.adjustSize()
        self.footer.adjustSize()
        self.btn1.adjustSize()

def runUI():
    app = QApplication(sys.argv)
    win = ClickerWindow()
    win.showUI()
    sys.exit(app.exec_())

runUI()